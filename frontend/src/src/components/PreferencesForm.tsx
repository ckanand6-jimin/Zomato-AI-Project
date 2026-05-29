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
    axios.get(apiUrl('/api/cities')).then(r => setCities(r.data || [])).catch(() => setCities([]))
  }, [])

  const onFind = async (e: React.FormEvent) => {
    e.preventDefault()
    const prefs = { location, budget, cuisine: cuisine ? cuisine.split(',').map(s=>s.trim()) : undefined, min_rating: minRating }
    // emit event for results component; simple approach: store in localStorage for now
    localStorage.setItem('zomato_prefs', JSON.stringify(prefs))
    window.dispatchEvent(new Event('zomato_prefs_changed'))
  }

  return (
    <form className="bg-white p-6 rounded shadow" onSubmit={onFind}>
      <label className="block text-sm font-medium text-gray-700">Location</label>
      <select className="mt-1 block w-full" value={location} onChange={e=>setLocation(e.target.value)}>
        <option value="">Select a city...</option>
        {cities.map(c => <option key={c} value={c}>{c}</option>)}
      </select>

      <label className="block mt-4 text-sm font-medium text-gray-700">Budget Tier</label>
      <div className="mt-2 flex gap-2">
        <button type="button" onClick={()=>setBudget('low')} className={`px-3 py-2 border ${budget==='low'?'border-orange-500':'border-gray-200'}`}>Low</button>
        <button type="button" onClick={()=>setBudget('medium')} className={`px-3 py-2 border ${budget==='medium'?'border-orange-500':'border-gray-200'}`}>Medium</button>
        <button type="button" onClick={()=>setBudget('high')} className={`px-3 py-2 border ${budget==='high'?'border-orange-500':'border-gray-200'}`}>High</button>
      </div>

      <label className="block mt-4 text-sm font-medium text-gray-700">Cuisine (comma separated)</label>
      <input className="mt-1 block w-full" value={cuisine} onChange={e=>setCuisine(e.target.value)} />

      <label className="block mt-4 text-sm font-medium text-gray-700">Minimum Rating</label>
      <input type="range" min={0} max={5} step={0.1} value={minRating} onChange={e=>setMinRating(parseFloat(e.target.value))} />
      <div className="text-sm text-gray-500">{minRating.toFixed(1)}</div>

      <div className="mt-6 flex justify-between">
        <button type="button" onClick={()=>{ setLocation(''); setBudget('low'); setCuisine(''); setMinRating(3.5)}} className="px-4 py-2 border rounded">Reset</button>
        <button type="submit" className="px-4 py-2 bg-orange-500 text-white rounded">Find Restaurants</button>
      </div>
    </form>
  )
}
