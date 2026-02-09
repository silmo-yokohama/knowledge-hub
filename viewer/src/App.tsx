import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './components/Layout.tsx'
import { HeadlinesPage } from './pages/HeadlinesPage.tsx'
import { DeepDivePage } from './pages/DeepDivePage.tsx'
import { FavoritesPage } from './pages/FavoritesPage.tsx'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HeadlinesPage />} />
        <Route path="/headlines/:date?" element={<HeadlinesPage />} />
        <Route path="/deepdives" element={<DeepDivePage />} />
        <Route path="/deepdives/:month/:filename" element={<DeepDivePage />} />
        <Route path="/favorites" element={<FavoritesPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}
