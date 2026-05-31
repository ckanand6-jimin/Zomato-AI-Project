import React from 'react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden">
      {/* Animated Background Glow */}
      <div className="absolute inset-0 bg-gradient-to-r from-violet-600/20 via-transparent to-violet-400/20 blur-3xl opacity-40 pointer-events-none" />
      <div className="absolute top-1/2 right-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl opacity-30 pointer-events-none" />

      <div className="relative">
        <div className="glass rounded-2xl glow p-8 md:p-12 border border-glass">
          <div className="max-w-3xl">
            {/* Label */}
            <div className="inline-flex items-center gap-2 rounded-full bg-violet-500/20 border border-violet-400/40 px-4 py-2 mb-6">
              <span className="relative inline-block h-2 w-2 rounded-full bg-violet-400 animate-pulse" />
              <span className="text-xs font-semibold uppercase tracking-widest text-violet-300">AI-Powered Discovery</span>
            </div>

            {/* Headline */}
            <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6 text-slate-100">
              Discover restaurants that <span className="bg-gradient-to-r from-violet-400 to-violet-300 bg-clip-text text-transparent">match your taste</span>
            </h1>

            {/* Description */}
            <p className="text-lg md:text-xl text-slate-300 mb-8 max-w-2xl leading-relaxed">
              AI-powered recommendations grounded in real restaurant data. Personalized filters for budget, cuisine, and rating with transparent reasoning.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row gap-4">
              <a href="#preferences" className="inline-flex items-center justify-center rounded-lg bg-gradient-to-r from-violet-600 to-violet-500 px-8 py-3 text-sm font-semibold text-white shadow-glow transition hover:shadow-glow-lg hover:-translate-y-0.5 active:translate-y-0">
                Set Preferences
              </a>
              <a href="#recommendations" className="inline-flex items-center justify-center rounded-lg border border-violet-500/50 bg-transparent px-8 py-3 text-sm font-semibold text-slate-100 transition hover:border-violet-400 hover:bg-violet-500/10">
                View Recommendations
              </a>
            </div>

            {/* Features Grid */}
            <div className="mt-12 grid gap-4 sm:grid-cols-3">
              {[
                { icon: '📊', label: 'Real Data', desc: 'Grounded restaurant records' },
                { icon: '🧠', label: 'AI Reasoning', desc: 'Transparent explanations' },
                { icon: '⚡', label: 'Lightning Fast', desc: 'Instant API responses' },
              ].map((feature, idx) => (
                <div key={idx} className="rounded-lg bg-slate-950/40 border border-slate-700/50 p-4">
                  <p className="text-2xl mb-2">{feature.icon}</p>
                  <p className="font-semibold text-slate-100 text-sm">{feature.label}</p>
                  <p className="text-xs text-slate-400 mt-1">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
