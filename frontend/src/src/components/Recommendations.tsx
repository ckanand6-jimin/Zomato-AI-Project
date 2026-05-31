import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { apiUrl } from '../api'

type Rec = { restaurant_id: string; rank: number; explanation: string }

type ApiResult = {
  recommendations?: Rec[]
  summary?: string
  fallback_used?: boolean
  model_version?: string | null
}

export default function Recommendations(){
  const [recs, setRecs] = useState<Rec[]>([])
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState('')
  const [fallbackUsed, setFallbackUsed] = useState(false)
  const [modelVersion, setModelVersion] = useState<string | null>(null)
  const [error, setError] = useState('')

  useEffect(()=>{
    const fetch = async () => {
      const raw = localStorage.getItem('zomato_prefs')
      if(!raw) return
      setLoading(true)
      setError('')
      try{
        const prefs = JSON.parse(raw)
        const r = await axios.post<ApiResult>(apiUrl('/api/recommend'), prefs)
        setRecs(r.data.recommendations || [])
        setSummary(r.data.summary || '')
        setFallbackUsed(Boolean(r.data.fallback_used))
        setModelVersion(r.data.model_version ?? null)
      }catch(e){
        setRecs([])
        setSummary('')
        setFallbackUsed(false)
        setModelVersion(null)
        setError('Unable to fetch recommendations. Please try again.')
      }finally{setLoading(false)}
    }
    window.addEventListener('zomato_prefs_changed', fetch)
    fetch()
    return ()=> window.removeEventListener('zomato_prefs_changed', fetch)
  }, [])

  if(loading) return (
    <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm shadow-slate-200/40">
      <p className="text-lg font-medium text-slate-900">Finding the best options for you...</p>
      <p className="mt-3 text-slate-600">This usually takes just a second.</p>
    </div>
  )

  if(error) return (
    <div className="rounded-[2rem] border border-rose-200 bg-rose-50 p-6 text-rose-700 shadow-sm">
      {error}
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-200/40">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-rose-600">Recommendations</p>
            <h2 className="mt-2 text-2xl font-semibold text-slate-950">Your best restaurant picks</h2>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            {fallbackUsed && (
              <span className="rounded-full bg-rose-50 px-4 py-2 text-sm font-semibold text-rose-700">Fallback used</span>
            )}
            {modelVersion && (
              <span className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700">Model: {modelVersion}</span>
            )}
          </div>
        </div>
        {summary && <p className="mt-4 text-slate-600">{summary}</p>}
      </div>

      {recs.length === 0 ? (
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm text-slate-700">
          <p className="font-semibold">No recommendations yet.</p>
          <p className="mt-2">Choose your preferences to discover the best restaurants for your selected city.</p>
        </div>
      ) : (
        <div className="grid gap-5 sm:grid-cols-2">
          {recs.map(r => (
            <article key={r.restaurant_id} className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md">
              <div className="mb-4 flex items-center justify-between gap-3">
                <div>
                  <span className="text-xs uppercase tracking-[0.32em] text-slate-500">Rank</span>
                  <p className="mt-2 text-3xl font-semibold text-slate-900">#{r.rank}</p>
                </div>
                <div className="rounded-3xl bg-rose-600 px-4 py-2 text-sm font-semibold text-white">AI pick</div>
              </div>
              <p className="text-lg font-semibold text-slate-900">{r.restaurant_id}</p>
              <p className="mt-4 text-slate-600 leading-7">{r.explanation}</p>
            </article>
          ))}
        </div>
      )}
    </div>
  )
}
