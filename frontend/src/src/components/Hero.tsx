import React from 'react'

export default function Hero() {
  return (
    <section className="relative overflow-hidden py-6 md:py-8">
      {/* Animated Background Glow - Subtle */}
      <div className="absolute inset-0 bg-gradient-to-r from-violet-600/10 via-transparent to-violet-400/10 blur-3xl opacity-30 pointer-events-none" />

      <div className="relative">
        <div className="max-w-3xl">
          {/* Compact Label */}
          <div className="inline-flex items-center gap-2 rounded-full bg-violet-500/20 border border-violet-400/40 px-3 py-1.5 mb-3">
            <span className="relative inline-block h-1.5 w-1.5 rounded-full bg-violet-400 animate-pulse" />
            <span className="text-xs font-semibold uppercase tracking-widest text-violet-300">AI Discovery</span>
          </div>

          {/* Compact Headline */}
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-3 text-slate-100">
            Discover restaurants that <span className="bg-gradient-to-r from-violet-400 to-violet-300 bg-clip-text text-transparent">match your taste</span>
          </h1>

          {/* Short Description */}
          <p className="text-sm md:text-base text-slate-300 mb-4 max-w-2xl leading-relaxed">
            AI recommendations grounded in real data. Set your preferences below to get started.
          </p>

          {/* Quick CTA */}
          <a href="#preferences" className="inline-flex items-center justify-center rounded-lg bg-gradient-to-r from-violet-600 to-violet-500 px-6 py-2 text-sm font-semibold text-white shadow-glow transition hover:shadow-glow-lg hover:-translate-y-0.5">
            Start →
          </a>
        </div>
      </div>
    </section>
  )
}
