import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { apiUrl } from '../api'

type Rec = { restaurant_id: string; rank: number; explanation: string }

export default function Recommendations(){
  const [recs, setRecs] = useState<Rec[]>([])
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState('')

  useEffect(()=>{
    const fetch = async () => {
      const raw = localStorage.getItem('zomato_prefs')
      if(!raw) return
      setLoading(true)
      try{
        const prefs = JSON.parse(raw)
        const r = await axios.post(apiUrl('/api/recommend'), prefs)
        setRecs(r.data.recommendations || [])
        setSummary(r.data.summary || '')
      }catch(e){
        setRecs([])
      }finally{setLoading(false)}
    }
    window.addEventListener('zomato_prefs_changed', fetch)
    fetch()
    return ()=> window.removeEventListener('zomato_prefs_changed', fetch)
  }, [])

  if(loading) return <div className="p-6 bg-white rounded shadow">Generating personalized recommendations…</div>

  return (
    <div>
      {summary && <div className="mb-4 p-4 bg-blue-50 rounded">{summary}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recs.map(r => (
          <div key={r.restaurant_id} className="bg-white p-4 rounded shadow">
            <div className="text-sm text-gray-500">#{r.rank}</div>
            <div className="font-semibold">{r.restaurant_id}</div>
            <div className="mt-2 text-gray-700">{r.explanation}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
