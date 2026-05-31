import React from 'react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-rose-50 via-slate-100 to-slate-50 px-6 py-10 shadow-xl shadow-slate-200/50">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(251,113,133,0.22),_transparent_35%),radial-gradient(circle_at_bottom_right,_rgba(14,165,233,0.16),_transparent_28%)]" />
      <div className="relative grid gap-8 lg:grid-cols-[max-content_minmax(0,1fr)] items-center">
        <div className="space-y-6 max-w-xl">
          <div className="inline-flex items-center gap-2 rounded-full bg-white/90 px-4 py-2 text-sm font-semibold text-rose-600 shadow-sm ring-1 ring-rose-100">
            AI-powered restaurant discovery
          </div>
          <h1 className="text-4xl sm:text-5xl font-semibold tracking-tight text-slate-950">Discover restaurants that match your taste</h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-700">AI-powered recommendations grounded in real restaurant data with personalized filters for budget, cuisine, and rating.</p>
          <div className="flex flex-col sm:flex-row gap-4">
            <a href="#preferences" className="inline-flex items-center justify-center rounded-full bg-rose-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-rose-300/40 transition hover:bg-rose-700">Get personalized picks</a>
            <a href="#recommendations" className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-6 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-50">See live recommendations</a>
          </div>
        </div>
        <div className="rounded-[1.75rem] border border-slate-200 bg-white/90 p-6 shadow-lg shadow-slate-200/40">
          <div className="flex items-center justify-between gap-4 mb-6">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-rose-600">Quick insight</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-950">Top rated by AI</h2>
            </div>
            <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-100 text-rose-700 text-xl">★</div>
          </div>
          <div className="space-y-4">
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Real candidate pool</p>
              <p className="mt-2 font-semibold text-slate-900">All restaurants come from the backend dataset.</p>
            </div>
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Transparent ranking</p>
              <p className="mt-2 font-semibold text-slate-900">When the AI is uncertain, the app serves safe fallback results.</p>
            </div>
            <div className="rounded-3xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Built for speed</p>
              <p className="mt-2 font-semibold text-slate-900">Connections to the API stay lightweight and fast.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
