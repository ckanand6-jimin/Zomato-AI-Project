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

// Calculate match score as 100 - (rank * 3), ranging 95-80% for ranks 1-5
const getMatchScore = (rank: number) => Math.max(80, 100 - rank * 3)

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

    const handleReset = () => {
      setRecs([])
      setSummary('')
      setFallbackUsed(false)
      setModelVersion(null)
      setError('')
      setLoading(false)
    }

    window.addEventListener('zomato_prefs_changed', fetch)
    window.addEventListener('zomato_reset', handleReset)
    fetch()
    return ()=> {
      window.removeEventListener('zomato_prefs_changed', fetch)
      window.removeEventListener('zomato_reset', handleReset)
    }
  }, [])

  if(loading) return (
    <div className="glass rounded-2xl glow-sm p-8 border border-glass">
      <div className="space-y-4">
        <div className="h-6 w-32 rounded bg-slate-700/30 animate-pulse" />
        <div className="h-4 w-full rounded bg-slate-700/20 animate-pulse" />
        <div className="h-4 w-2/3 rounded bg-slate-700/20 animate-pulse" />
      </div>
    </div>
  )

  if(error) return (
    <div className="glass rounded-2xl glow-sm p-8 border border-red-500/30 bg-red-500/10">
      <p className="text-red-300 font-semibold">{error}</p>
    </div>
  )

  return (
    <div className="space-y-5">
      {/* Header Card */}
      <div className="glass rounded-2xl glow-sm p-6 border border-glass">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-violet-400">Powered by AI</p>
            <h2 className="mt-1 text-3xl font-bold text-slate-100">Recommendations</h2>
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
        {summary && <p className="mt-3 text-sm text-slate-300 leading-relaxed italic">{summary}</p>}
      </div>

      {/* Recommendations Grid or Empty State */}
      {recs.length === 0 ? (
        <div className="glass rounded-2xl glow-sm p-8 border border-glass text-center">
          <div className="inline-flex justify-center items-center h-12 w-12 rounded-full bg-violet-500/20 mb-4">
            <span className="text-xl">✨</span>
          </div>
          <p className="text-lg font-semibold text-slate-100">No recommendations yet</p>
          <p className="mt-2 text-sm text-slate-400">Set your preferences on the left to discover AI-ranked restaurants tailored to your taste.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {recs.map((r, idx) => {
            const matchScore = getMatchScore(r.rank)
            return (
              <article
                key={r.restaurant_id}
                className="glass rounded-xl glow-sm p-5 border border-glass group transition hover:shadow-glow-lg hover:border-violet-400/50 hover:-translate-y-0.5 cursor-default flex flex-col"
              >
                {/* Top Row: Rank + Match Score */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-widest text-slate-400">Rank</p>
                    <p className="text-2xl font-bold text-slate-100 leading-none">#{r.rank}</p>
                  </div>
                  {/* Match Score Badge */}
                  <div className="inline-flex flex-col items-center justify-center h-14 w-14 rounded-lg bg-gradient-to-br from-violet-600 to-violet-500 shadow-glow text-white font-bold flex-shrink-0">
                    <p className="text-xs font-semibold">Match</p>
                    <p className="text-lg">{matchScore}%</p>
                  </div>
                </div>

                {/* Restaurant Name */}
                <p className="text-base font-bold text-slate-100 mb-2 line-clamp-2 flex-shrink-0">
                  {r.restaurant_id}
                </p>

                {/* AI Reasoning */}
                <div className="flex-grow">
                  <p className="text-xs font-semibold uppercase tracking-widest text-violet-400 mb-1">AI Reasoning</p>
                  <p className="text-sm text-slate-300 leading-relaxed line-clamp-3">
                    {r.explanation}
                  </p>
                </div>

                {/* Footer indicator */}
                <div className="mt-3 pt-3 border-t border-slate-700/50 opacity-0 group-hover:opacity-100 transition-opacity">
                  <p className="text-xs text-violet-400 font-semibold">→ AI Ranked</p>
                </div>
              </article>
            )
          })}
        </div>
      )}
    </div>
  )
}
