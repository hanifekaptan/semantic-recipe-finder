import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './assets/styles/global.css'
import App from './App'
import 'wicg-inert'

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <App />
    </StrictMode>,
)
