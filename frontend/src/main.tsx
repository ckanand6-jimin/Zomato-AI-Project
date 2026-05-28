import React from 'react'
import { createRoot } from 'react-dom/client'
import './styles/tailwind.css'
import App from './src/App'

createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
