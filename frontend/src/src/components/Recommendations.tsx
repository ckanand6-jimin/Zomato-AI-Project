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
        setError('Unable to fetch recommendations. Please check your preferences.')
      }finally{setLoading(false)}
    }
    window.addEventListener('zomato_prefs_changed', fetch)
    fetch()
    return ()=> window.removeEventListener('zomato_prefs_changed', fetch)
  }, [])

  if(loading) return (
    <div className="glass rounded-2xl glow-sm p-8 border border-glass">
      <div className="space-y-4">
        <div className="h-8 w-40 rounded bg-slate-700/30 animate-pulse" />
        <div className="h-4 w-full rounded bg-slate-700/20 animate-pulse" />
        <div className="h-4 w-3/4 rounded bg-slate-700/20 animate-pulse" />
      </div>
    </div>
  )

  if(error) return (
    <div className="glass rounded-2xl glow-sm p-8 border border-red-500/30 bg-red-500/10">
      <p className="text-red-300 font-semibold">{error}</p>
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <div className="glass rounded-2xl glow-sm p-6 border border-glass">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-violet-400">AI Results</p>
            <h2 className="mt-2 text-2xl font-bold text-slate-100">Your picks</h2>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {fallbackUsed && (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-orange-500/20 border border-orange-500/40 px-3 py-1.5 text-xs font-semibold text-orange-300">
                <span className="relative inline-block h-1.5 w-1.5 rounded-full bg-orange-400" />
                Fallback
              </span>
            )}
            {modelVersion && (
              <span className="rounded-full bg-slate-700/40 border border-slate-600/50 px-3 py-1.5 text-xs font-medium text-slate-300">
                {modelVersion}
              </span>
            )}
          </div>
        </div>
        {summary && <p className="mt-4 text-sm text-slate-300 leading-relaxed">{summary}</p>}
      </div>

      {/* Recommendations Grid */}
      {recs.length === 0 ? (
        <div className="glass rounded-2xl glow-sm p-12 border border-glass text-center">
          <p className="text-lg font-semibold text-slate-100">No recommendations yet</p>
          <p className="mt-2 text-slate-400">Choose your preferences to discover restaurants.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {recs.map((r, idx) => (
            <article
              key={r.restaurant_id}
              className="glass rounded-2xl glow-sm p-6 border border-glass group transition hover:shadow-glow-lg hover:border-violet-400/50 hover:-translate-y-1 cursor-default"
              style={{
                animationDelay: `${idx * 50}ms`,
              }}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-4">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-widest text-violet-400">Rank</span>
                  <p className="mt-1 text-3xl font-bold text-transparent bg-gradient-to-r from-violet-400 to-violet-300 bg-clip-text">
                    #{r.rank}
                  </p>
                </div>
                {/* AI Score Badge */}
                <div className="inline-flex items-center justify-center h-12 w-12 rounded-full bg-gradient-to-br from-violet-600 to-violet-500 shadow-glow text-white font-bold">
                  {(100 - r.rank * 10).toFixed(0)}
                </div>
              </div>

              {/* Restaurant Name */}
              <p className="text-lg font-semibold text-slate-100 mb-3 line-clamp-2">
                {r.restaurant_id}
              </p>

              {/* Explanation */}
              <p className="text-sm text-slate-300 leading-relaxed line-clamp-3">
                {r.explanation}
              </p>

              {/* Hover indicator */}
              <div className="mt-4 pt-4 border-t border-slate-700/50 opacity-0 group-hover:opacity-100 transition-opacity">
                <p className="text-xs text-violet-400 font-semibold">✓ AI Ranked</p>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  )
}
