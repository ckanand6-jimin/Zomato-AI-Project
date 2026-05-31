import React from 'react'
import Hero from './components/Hero'
import PreferencesForm from './components/PreferencesForm'
import Recommendations from './components/Recommendations'

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-925 to-slate-950 text-slate-100">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-glass backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-gradient-to-br from-violet-600 to-violet-400 flex items-center justify-center text-slate-950 font-bold text-lg shadow-glow">Z</div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-violet-400">AI Powered</p>
              <p className="text-lg font-semibold text-slate-100">Zomato Recommender</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Hero Section */}
        <Hero />

        {/* Main Content Grid */}
        <section className="mt-12 grid gap-8 lg:grid-cols-[380px_minmax(0,1fr)]">
          {/* Left: Preferences Control Panel */}
          <aside className="space-y-6">
            <PreferencesForm />
            
            {/* Quick Stats Card */}
            <div className="glass rounded-2xl p-6 glow-sm">
              <p className="text-xs font-semibold uppercase tracking-widest text-violet-400 mb-4">System Status</p>
              <div className="grid gap-3">
                <div className="rounded-xl bg-slate-950/60 p-3">
                  <p className="text-xs text-slate-400">Real Data</p>
                  <p className="mt-1 font-semibold text-slate-100">100% Grounded</p>
                </div>
                <div className="rounded-xl bg-slate-950/60 p-3">
                  <p className="text-xs text-slate-400">AI Reasoning</p>
                  <p className="mt-1 font-semibold text-slate-100">Explainable</p>
                </div>
              </div>
            </div>
          </aside>

          {/* Right: Recommendations Section */}
          <section>
            <Recommendations />
          </section>
        </section>
      </main>
    </div>
  )
}
