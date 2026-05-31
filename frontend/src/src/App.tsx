import React from 'react'
import Hero from './components/Hero'
import PreferencesForm from './components/PreferencesForm'
import Recommendations from './components/Recommendations'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-xl shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-rose-500 flex items-center justify-center text-white font-semibold tracking-tight">Z</div>
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-rose-600">Zomato AI</p>
              <p className="text-lg font-semibold">Restaurant Recommender</p>
            </div>
          </div>
          <nav className="flex flex-wrap items-center gap-4 text-sm text-slate-600">
            <a className="hover:text-rose-600 transition" href="#preferences">Preferences</a>
            <a className="hover:text-rose-600 transition" href="#recommendations">Recommendations</a>
            <a className="hidden sm:inline-block rounded-full border border-slate-200 bg-slate-100 px-4 py-2 text-slate-700 hover:bg-white transition" href="#how-it-works">How it works</a>
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <Hero />

        <section className="mt-10 grid gap-8 xl:grid-cols-[360px_minmax(0,1fr)]">
          <div id="preferences" className="space-y-6">
            <PreferencesForm />
            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <p className="text-sm uppercase tracking-[0.24em] text-rose-600 mb-3">Fast facts</p>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-3xl bg-slate-50 p-4">
                  <p className="text-sm text-slate-500">Grounded data</p>
                  <p className="mt-2 font-semibold text-slate-900">100% real restaurant records</p>
                </div>
                <div className="rounded-3xl bg-slate-50 p-4">
                  <p className="text-sm text-slate-500">AI reasoning</p>
                  <p className="mt-2 font-semibold text-slate-900">Explainable recommendations</p>
                </div>
                <div className="rounded-3xl bg-slate-50 p-4">
                  <p className="text-sm text-slate-500">Smart filters</p>
                  <p className="mt-2 font-semibold text-slate-900">Budget, cuisine, rating</p>
                </div>
                <div className="rounded-3xl bg-slate-50 p-4">
                  <p className="text-sm text-slate-500">Instant results</p>
                  <p className="mt-2 font-semibold text-slate-900">Fast backend API calls</p>
                </div>
              </div>
            </div>
          </div>

          <div id="recommendations" className="space-y-6">
            <Recommendations />
          </div>
        </section>

        <section id="how-it-works" className="mt-16 rounded-[2rem] bg-gradient-to-r from-rose-50 via-slate-100 to-slate-50 px-6 py-10 shadow-sm border border-slate-200">
          <div className="grid gap-6 lg:grid-cols-3">
            <div className="lg:col-span-1">
              <p className="text-sm uppercase tracking-[0.32em] text-rose-600">How it works</p>
              <h2 className="mt-4 text-3xl font-semibold text-slate-900">A smarter way to choose your next meal</h2>
              <p className="mt-4 text-slate-600">The AI ranks restaurants from a filtered candidate pool so recommendations stay grounded, relevant, and explainable.</p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 lg:col-span-2">
              <div className="rounded-3xl bg-white p-6 shadow-sm border border-slate-200">
                <p className="text-sm font-semibold text-slate-900">Personalized filters</p>
                <p className="mt-3 text-slate-600">Budget, location, cuisine and rating filter the list before the AI ranks results.</p>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm border border-slate-200">
                <p className="text-sm font-semibold text-slate-900">Grounded ranking</p>
                <p className="mt-3 text-slate-600">If the LLM output cannot be trusted, the system gracefully falls back to a safe top-candidate ordering.</p>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm border border-slate-200">
                <p className="text-sm font-semibold text-slate-900">Clear explanations</p>
                <p className="mt-3 text-slate-600">Each recommendation includes a short explanation that tells you why it was selected.</p>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm border border-slate-200">
                <p className="text-sm font-semibold text-slate-900">Fast API calls</p>
                <p className="mt-3 text-slate-600">The backend uses a minimal REST API so the frontend stays fast and responsive.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}
