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
    <form className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm shadow-slate-200/50" onSubmit={onFind}>
      <div className="space-y-1">
        <p className="text-sm font-semibold text-slate-900">Tell us your taste</p>
        <p className="text-sm text-slate-500">Choose a city and the filters that matter most.</p>
      </div>

      <div className="space-y-3">
        <label className="block text-sm font-medium text-slate-700">Location</label>
        <select
          className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-rose-500 focus:ring-2 focus:ring-rose-100"
          value={location}
          onChange={e => setLocation(e.target.value)}
        >
          {cities.length === 0 ? <option value="">Loading cities...</option> : null}
          {cities.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>

      <div className="space-y-3">
        <p className="text-sm font-medium text-slate-700">Budget tier</p>
        <div className="grid grid-cols-3 gap-3">
          {['low', 'medium', 'high'].map(option => (
            <button
              key={option}
              type="button"
              onClick={() => setBudget(option as 'low'|'medium'|'high')}
              className={`rounded-3xl border px-4 py-3 text-sm font-semibold transition ${budget === option ? 'border-rose-600 bg-rose-50 text-rose-700' : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50'}`}
            >
              {option.charAt(0).toUpperCase() + option.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        <label className="block text-sm font-medium text-slate-700">Cuisine preferences</label>
        <input
          className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-rose-500 focus:ring-2 focus:ring-rose-100"
          value={cuisine}
          onChange={e => setCuisine(e.target.value)}
          placeholder="e.g. Indian, Chinese, Italian"
        />
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between text-sm font-medium text-slate-700">
          <span>Minimum rating</span>
          <span className="text-slate-500">{minRating.toFixed(1)}</span>
        </div>
        <input
          type="range"
          min={0}
          max={5}
          step={0.1}
          value={minRating}
          onChange={e => setMinRating(parseFloat(e.target.value))}
          className="w-full accent-rose-500"
        />
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:justify-between">
        <button
          type="button"
          onClick={resetForm}
          className="rounded-full border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
        >
          Reset
        </button>
        <button
          type="submit"
          className="rounded-full bg-rose-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-rose-200/70 transition hover:bg-rose-700"
        >
          Find Restaurants
        </button>
      </div>
    </form>
  )
}
