import { Link, useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Bot, Sun, Moon, LogOut, Menu, X, Trophy, LayoutDashboard, FileText, Mic } from 'lucide-react'
import { useThemeStore } from '../../store/themeStore'
import { useAuthStore } from '../../store/authStore'
import { useState } from 'react'

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/resume', label: 'Resume', icon: FileText },
  { path: '/interview', label: 'Interview', icon: Mic },
  { path: '/leaderboard', label: 'Leaderboard', icon: Trophy },
]

export default function Navbar({ children }) {
  const location = useLocation()
  const navigate = useNavigate()
  const { isDark, toggleTheme } = useThemeStore()
  const { user, logout } = useAuthStore()
  const [mobileOpen, setMobileOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      {/* Top Navbar */}
      <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg border-b border-gray-100 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/dashboard" className="flex items-center gap-2">
              <div className="w-9 h-9 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <span className="text-lg font-bold text-gray-900 dark:text-white hidden sm:block">AI Interview Bot</span>
            </Link>

            {/* Desktop Nav */}
            <div className="hidden md:flex items-center gap-1">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${
                      isActive
                        ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <item.icon className="w-4 h-4" />
                    {item.label}
                  </Link>
                )
              })}
            </div>

            {/* Right Side */}
            <div className="flex items-center gap-2">
              {/* Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
                aria-label="Toggle theme"
              >
                {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>

              {/* User Avatar */}
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white text-sm font-bold">
                  {user?.name?.charAt(0)?.toUpperCase() || 'U'}
                </div>
                <span className="hidden sm:block text-sm font-medium text-gray-700 dark:text-gray-300">
                  {user?.name || 'User'}
                </span>
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition ml-1"
                  aria-label="Logout"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>

              {/* Mobile Menu Toggle */}
              <button
                onClick={() => setMobileOpen(!mobileOpen)}
                className="md:hidden p-2 rounded-lg text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
              >
                {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Nav */}
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="md:hidden border-t border-gray-100 dark:border-gray-700"
          >
            <div className="px-4 py-3 space-y-1">
              {navItems.map((item) => {
                const isActive = location.pathname === item.path
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setMobileOpen(false)}
                    className={`flex items-center gap-3 px-3 py-3 rounded-lg text-sm font-medium transition ${
                      isActive
                        ? 'bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <item.icon className="w-5 h-5" />
                    {item.label}
                  </Link>
                )
              })}
            </div>
          </motion.div>
        )}
      </nav>

      {/* Page Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {children}
      </div>
    </div>
  )
}
