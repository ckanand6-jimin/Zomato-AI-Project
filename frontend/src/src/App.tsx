import React from 'react'
import Hero from './components/Hero'
import PreferencesForm from './components/PreferencesForm'
import Recommendations from './components/Recommendations'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="text-xl font-semibold text-orange-600">Zomato AI Recommender</div>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-8">
        <Hero />
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <PreferencesForm />
          </div>
          <div className="lg:col-span-2">
            <Recommendations />
          </div>
        </div>
      </main>
    </div>
  )
}
