import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuthStore } from './store/authStore'
import { useThemeStore } from './store/themeStore'

// Pages
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import ResumeUpload from './pages/ResumeUpload'
import InterviewMode from './pages/InterviewMode'
import Report from './pages/Report'
import Leaderboard from './pages/Leaderboard'

// Layout
import Navbar from './components/layout/Navbar'

function ProtectedRoute({ children }) {
  const { token } = useAuthStore()
  return token ? children : <Navigate to="/login" />
}

export default function App() {
  const { initTheme } = useThemeStore()
  const { token, fetchMe } = useAuthStore()

  useEffect(() => {
    initTheme()
  }, [])

  useEffect(() => {
    if (token) fetchMe()
  }, [token])

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Navbar><Dashboard /></Navbar>
              </ProtectedRoute>
            }
          />
          <Route
            path="/resume"
            element={
              <ProtectedRoute>
                <Navbar><ResumeUpload /></Navbar>
              </ProtectedRoute>
            }
          />
          <Route
            path="/interview"
            element={
              <ProtectedRoute>
                <Navbar><InterviewMode /></Navbar>
              </ProtectedRoute>
            }
          />
          <Route
            path="/report/:reportId"
            element={
              <ProtectedRoute>
                <Navbar><Report /></Navbar>
              </ProtectedRoute>
            }
          />
          <Route
            path="/leaderboard"
            element={
              <ProtectedRoute>
                <Navbar><Leaderboard /></Navbar>
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
