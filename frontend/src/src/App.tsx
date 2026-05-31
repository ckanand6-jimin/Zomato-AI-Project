import React from 'react'
import Hero from './components/Hero'
import PreferencesForm from './components/PreferencesForm'
import Recommendations from './components/Recommendations'

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-925 to-slate-950 text-slate-100">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b border-glass backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-9 w-9 rounded-lg bg-gradient-to-br from-violet-600 to-violet-500 flex items-center justify-center text-slate-950 font-bold text-sm shadow-glow">Z</div>
            <p className="text-sm font-semibold text-slate-100">Zomato AI</p>
          </div>
          <p className="text-xs text-slate-500">Discover with AI</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* Hero Section */}
        <Hero />

        {/* Main Content Grid - Recommendations Prominent */}
        <section className="mt-8 grid gap-8 lg:grid-cols-[320px_minmax(0,1fr)]">
          {/* Left: Preferences Control Panel - Compact */}
          <aside id="preferences" className="lg:sticky lg:top-20 lg:h-fit">
            <PreferencesForm />
          </aside>

          {/* Right: Recommendations Section - Main Focus */}
          <section id="recommendations">
            <Recommendations />
          </section>
        </section>
      </main>
    </div>
  )
}
