import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { apiUrl } from '../api'

export default function PreferencesForm() {
  const [cities, setCities] = useState<string[]>([])
  const [location, setLocation] = useState('')
  const [budget, setBudget] = useState<'low'|'medium'|'high'>('low')
  const [cuisine, setCuisine] = useState('')
  const [minRating, setMinRating] = useState(3.5)

  useEffect(() => {
    axios.get(apiUrl('/api/cities')).then(r => {
      const data = r.data || []
      setCities(data)
      if (!location && data.length > 0) {
        setLocation(data[0])
      }
    }).catch(() => setCities([]))
  }, [])

  const onFind = async (e: React.FormEvent) => {
    e.preventDefault()
    const prefs = { location, budget, cuisine: cuisine ? cuisine.split(',').map(s => s.trim()) : undefined, min_rating: minRating }
    localStorage.setItem('zomato_prefs', JSON.stringify(prefs))
    window.dispatchEvent(new Event('zomato_prefs_changed'))
  }

  const resetForm = () => {
    setLocation(cities[0] ?? '')
    setBudget('low')
    setCuisine('')
    setMinRating(3.5)
  }

  return (
    <form className="glass rounded-2xl glow-sm p-5 space-y-4" onSubmit={onFind}>
      {/* Header */}
      <div>
        <p className="text-xs font-semibold uppercase tracking-widest text-violet-400">Preferences</p>
        <h2 className="mt-1 text-base font-bold text-slate-100">Find restaurants</h2>
      </div>

      {/* Location */}
      <div className="space-y-2">
        <label className="block text-xs font-medium text-slate-300 uppercase tracking-wide">Location</label>
        <select
          className="w-full rounded-lg bg-slate-950/60 border border-glass px-3 py-2 text-slate-100 text-sm outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30"
          value={location}
          onChange={e => setLocation(e.target.value)}
        >
          {cities.length === 0 ? <option value="">Loading...</option> : null}
          {cities.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      {/* Budget */}
      <div className="space-y-2">
        <p className="text-xs font-medium text-slate-300 uppercase tracking-wide">Budget</p>
        <div className="grid grid-cols-3 gap-1.5">
          {(['low', 'medium', 'high'] as const).map(option => (
            <button
              key={option}
              type="button"
              onClick={() => setBudget(option)}
              className={`rounded-lg px-2.5 py-1.5 text-xs font-semibold transition ${
                budget === option
                  ? 'border border-violet-500 bg-violet-500/20 text-violet-300 shadow-glow-sm'
                  : 'border border-slate-700/50 bg-slate-950/60 text-slate-300 hover:border-violet-400/50'
              }`}
            >
              {option.charAt(0).toUpperCase() + option.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Cuisine */}
      <div className="space-y-2">
        <label className="block text-xs font-medium text-slate-300 uppercase tracking-wide">Cuisine</label>
        <input
          className="w-full rounded-lg bg-slate-950/60 border border-glass px-3 py-2 text-slate-100 text-sm placeholder-slate-500 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30"
          value={cuisine}
          onChange={e => setCuisine(e.target.value)}
          placeholder="e.g. Indian, Chinese"
        />
      </div>

      {/* Rating */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-xs font-medium text-slate-300 uppercase tracking-wide">Min. Rating</label>
          <span className="inline-flex rounded-full bg-violet-500/20 border border-violet-500/40 px-2 py-0.5 text-xs font-semibold text-violet-300">
            {minRating.toFixed(1)} ★
          </span>
        </div>
        <input
          type="range"
          min={0}
          max={5}
          step={0.1}
          value={minRating}
          onChange={e => setMinRating(parseFloat(e.target.value))}
          className="w-full accent-violet-500"
        />
      </div>

      {/* Actions */}
      <div className="flex flex-col gap-2 pt-1">
        <button
          type="submit"
          className="w-full rounded-lg bg-gradient-to-r from-violet-600 to-violet-500 px-3 py-2 text-xs font-semibold text-white shadow-glow transition hover:shadow-glow-lg hover:-translate-y-0.5 active:translate-y-0"
        >
          Find Restaurants
        </button>
        <button
          type="button"
          onClick={resetForm}
          className="w-full rounded-lg border border-slate-700/50 bg-slate-950/40 px-3 py-2 text-xs font-semibold text-slate-300 transition hover:border-violet-500/30 hover:bg-violet-500/10"
        >
          Reset
        </button>
      </div>
    </form>
  )
}
