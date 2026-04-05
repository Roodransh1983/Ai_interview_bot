import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Play, FileText, TrendingUp, Clock, Award, ArrowRight, Mic, Video, Trophy } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import api from '../services/api'

export default function Dashboard() {
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const [recentInterviews, setRecentInterviews] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecentInterviews()
  }, [])

  const fetchRecentInterviews = async () => {
    try {
      const res = await api.get('/report/history/me')
      setRecentInterviews(res.data.slice(0, 5))
    } catch {
      // User might not have any interviews yet
    } finally {
      setLoading(false)
    }
  }

  const stats = [
    {
      label: 'Total Interviews',
      value: user?.total_interviews || 0,
      icon: Mic,
      color: 'from-blue-500 to-blue-600',
    },
    {
      label: 'Average Score',
      value: user?.avg_score || 0,
      icon: TrendingUp,
      color: 'from-green-500 to-green-600',
    },
    {
      label: 'Resume',
      value: user?.resume_uploaded ? 'Uploaded' : 'Missing',
      icon: FileText,
      color: user?.resume_uploaded
        ? 'from-emerald-500 to-emerald-600'
        : 'from-amber-500 to-amber-600',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center justify-between gap-4"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Welcome back, {user?.name?.split(' ')[0] || 'there'}! 👋
          </h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Ready for your next interview practice session?
          </p>
        </div>
        <Link
          to="/interview"
          className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-indigo-500/30 transition-all hover:scale-105"
        >
          <Play className="w-5 h-5" />
          Start Interview
        </Link>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {stats.map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`w-12 h-12 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</div>
            <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">{stat.label}</div>
          </motion.div>
        ))}
      </div>

      {/* Quick Start / Resume Warning */}
      {!user?.resume_uploaded && (
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-2xl p-6"
        >
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 bg-amber-100 dark:bg-amber-900/50 rounded-lg flex items-center justify-center flex-shrink-0">
              <FileText className="w-5 h-5 text-amber-600 dark:text-amber-400" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold text-amber-800 dark:text-amber-200">Upload your resume</h3>
              <p className="text-sm text-amber-700 dark:text-amber-300 mt-1">
                Get personalized questions based on your skills and experience. Upload now to unlock tailored interview questions.
              </p>
              <Link
                to="/resume"
                className="inline-flex items-center gap-1 text-sm font-medium text-amber-700 dark:text-amber-300 hover:underline mt-2"
              >
                Upload Resume <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </motion.div>
      )}

      {/* Interview Modes */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Choose Your Mode</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow cursor-pointer group"
            onClick={() => navigate('/interview?mode=text')}
          >
            <div className="w-14 h-14 bg-gradient-to-br from-indigo-400 to-indigo-600 rounded-xl flex items-center justify-center mb-4">
              <Mic className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Text Chat Mode</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Chat-based interview. Type your answers and get real-time feedback with AI evaluation.
            </p>
            <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 text-sm font-medium group-hover:gap-3 transition-all">
              Start Practice <ArrowRight className="w-4 h-4" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md transition-shadow cursor-pointer group"
            onClick={() => navigate('/interview?mode=video')}
          >
            <div className="w-14 h-14 bg-gradient-to-br from-purple-400 to-purple-600 rounded-xl flex items-center justify-center mb-4">
              <Video className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Video Interview Mode</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Real-time video simulation with face detection. Practice looking professional on camera.
            </p>
            <div className="flex items-center gap-2 text-purple-600 dark:text-purple-400 text-sm font-medium group-hover:gap-3 transition-all">
              Start Practice <ArrowRight className="w-4 h-4" />
            </div>
          </motion.div>
        </div>
      </div>

      {/* Recent Interviews */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Recent Interviews</h2>
          {recentInterviews.length > 0 && (
            <Link
              to="/leaderboard"
              className="flex items-center gap-1 text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
            >
              <Trophy className="w-4 h-4" /> View Leaderboard
            </Link>
          )}
        </div>

        {loading ? (
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-gray-100 dark:bg-gray-800 rounded-xl h-20 animate-pulse" />
            ))}
          </div>
        ) : recentInterviews.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-12 text-center border border-gray-100 dark:border-gray-700">
            <Clock className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">No interviews yet</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Complete your first interview to see your results here
            </p>
            <Link
              to="/interview"
              className="inline-flex items-center gap-2 px-5 py-2 bg-indigo-500 text-white rounded-lg text-sm font-medium hover:bg-indigo-600 transition"
            >
              Start Your First Interview
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {recentInterviews.map((interview, i) => (
              <motion.div
                key={interview.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-gray-900 dark:text-white">
                      Score: {interview.total_score}/100
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      Grade: {interview.grade} • {new Date(interview.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  {interview.total_score >= 80 && (
                    <span className="px-2 py-1 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 text-xs font-medium rounded-md">
                      Excellent
                    </span>
                  )}
                  <Link
                    to={`/report/${interview.id}`}
                    className="text-sm text-indigo-600 dark:text-indigo-400 font-medium hover:underline"
                  >
                    View Report
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
