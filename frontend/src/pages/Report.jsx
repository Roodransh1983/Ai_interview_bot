import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, Mail, RefreshCw, Share2, Trophy, TrendingUp, ThumbsUp, AlertTriangle, Lightbulb, CheckCircle } from 'lucide-react'
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts'
import api from '../services/api'

export default function Report() {
  const { reportId } = useParams()
  const navigate = useNavigate()
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [sendingEmail, setSendingEmail] = useState(false)
  const [emailSent, setEmailSent] = useState(false)

  useEffect(() => {
    fetchReport()
  }, [reportId])

  const fetchReport = async () => {
    try {
      const res = await api.get(`/report/${reportId}`)
      setReport(res.data)
    } catch {
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const sendEmail = async () => {
    setSendingEmail(true)
    try {
      await api.post(`/report/${reportId}/email`)
      setEmailSent(true)
    } catch {
      alert('Failed to send email')
    } finally {
      setSendingEmail(false)
    }
  }

  const copyLink = () => {
    navigator.clipboard.writeText(window.location.href)
    alert('Link copied!')
  }

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto space-y-4">
        <div className="h-8 w-48 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
        <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded-2xl animate-pulse" />
        <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded-2xl animate-pulse" />
      </div>
    )
  }

  if (!report) return null

  // Prepare radar chart data
  const radarData = Object.entries(report.category_scores || {}).map(([cat, score]) => ({
    category: cat,
    score: Math.round(score),
    fullMark: 100,
  }))

  // Score color
  const scoreColor = report.total_score >= 80 ? '#22c55e' : report.total_score >= 60 ? '#eab308' : '#ef4444'

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Back Button */}
      <Link to="/dashboard" className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition">
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </Link>

      {/* Header Card */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-3xl p-8 text-white text-center"
      >
        <div className="text-7xl font-black mb-2">{report.total_score}<span className="text-3xl opacity-70">/100</span></div>
        <div className="text-2xl font-bold mb-1">Grade: {report.grade}</div>
        <p className="opacity-80">Interview completed on {new Date(report.created_at).toLocaleDateString()}</p>

        <div className="flex justify-center gap-6 mt-6 text-sm opacity-90">
          <div>
            <div className="text-xl font-bold">{report.average_answer_score}</div>
            <div className="opacity-70">Answer Score</div>
          </div>
          <div className="w-px bg-white/30" />
          <div>
            <div className="text-xl font-bold">{report.average_confidence}</div>
            <div className="opacity-70">Confidence</div>
          </div>
          <div className="w-px bg-white/30" />
          <div>
            <div className="text-xl font-bold">{report.total_questions}</div>
            <div className="opacity-70">Questions</div>
          </div>
        </div>
      </motion.div>

      {/* Category Radar + Summary Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Radar Chart */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-100 dark:border-gray-700"
        >
          <h3 className="font-bold text-gray-900 dark:text-white mb-4">Skills Radar</h3>
          {radarData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e5e7eb" />
                <PolarAngleAxis dataKey="category" tick={{ fontSize: 11, fill: '#6b7280' }} />
                <Radar
                  name="Score"
                  dataKey="score"
                  stroke="#6366f1"
                  fill="#6366f1"
                  fillOpacity={0.3}
                />
                <Tooltip
                  contentStyle={{ background: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }}
                  itemStyle={{ color: '#fff' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[260px] flex items-center justify-center text-gray-400">No data</div>
          )}
        </motion.div>

        {/* Strengths & Weaknesses */}
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-100 dark:border-gray-700"
        >
          <h3 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <ThumbsUp className="w-5 h-5 text-green-500" /> Strengths
          </h3>
          <div className="space-y-2">
            {(report.strengths || []).map((s, i) => (
              <div key={i} className="flex items-center gap-2 text-sm">
                <CheckCircle className="w-4 h-4 text-green-500" />
                <span className="text-gray-700 dark:text-gray-300">{s}</span>
              </div>
            ))}
          </div>

          {report.weaknesses?.length > 0 && (
            <>
              <h3 className="font-bold text-gray-900 dark:text-white mt-6 mb-4 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-red-500" /> Areas to Improve
              </h3>
              <div className="space-y-2">
                {(report.weaknesses || []).map((w, i) => (
                  <div key={i} className="flex items-center gap-2 text-sm">
                    <AlertTriangle className="w-4 h-4 text-red-500" />
                    <span className="text-gray-700 dark:text-gray-300">{w}</span>
                  </div>
                ))}
              </div>
            </>
          )}
        </motion.div>

        {/* Suggestions */}
        <motion.div
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-100 dark:border-gray-700"
        >
          <h3 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-amber-500" /> Suggestions
          </h3>
          <div className="space-y-3">
            {(report.suggestions || []).map((s, i) => (
              <div key={i} className="flex items-start gap-2 text-sm">
                <span className="text-amber-500 mt-0.5">💡</span>
                <span className="text-gray-700 dark:text-gray-300">{s}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Question Breakdown */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 overflow-hidden"
      >
        <div className="p-6 border-b border-gray-100 dark:border-gray-700">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white">Answer Breakdown</h3>
        </div>
        <div className="divide-y divide-gray-100 dark:divide-gray-700">
          {(report.breakdown || []).map((item, i) => (
            <div key={i} className="p-6">
              <div className="flex items-start justify-between gap-4 mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400 text-xs font-medium rounded">
                      Q{item.question_number}
                    </span>
                    <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded">
                      {item.category}
                    </span>
                  </div>
                  <p className="text-gray-900 dark:text-white font-medium mb-2">{item.question}</p>
                </div>
                <div className="text-right flex-shrink-0">
                  <div className={`text-2xl font-black ${
                    item.score >= 70 ? 'text-green-500' : item.score >= 50 ? 'text-amber-500' : 'text-red-500'
                  }`}>
                    {item.score}
                  </div>
                  <div className="text-xs text-gray-500">out of 100</div>
                </div>
              </div>

              <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-3 mb-3">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  <span className="font-medium text-gray-700 dark:text-gray-300">Your answer: </span>
                  {item.user_answer?.substring(0, 200)}{item.user_answer?.length > 200 ? '...' : ''}
                </p>
              </div>

              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-3">
                <p className="text-sm text-blue-800 dark:text-blue-300">{item.feedback}</p>
              </div>

              {item.keywords_matched?.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1">
                  {item.keywords_matched.map((kw) => (
                    <span key={kw} className="px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs rounded">
                      ✓ {kw}
                    </span>
                  ))}
                  {(item.keywords_missed || []).slice(0, 3).map((kw) => (
                    <span key={kw} className="px-2 py-0.5 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-xs rounded">
                      ✗ {kw}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Actions */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="flex flex-wrap gap-4"
      >
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={sendEmail}
          disabled={sendingEmail || emailSent}
          className="flex items-center gap-2 px-5 py-2.5 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-medium rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition disabled:opacity-50"
        >
          <Mail className="w-4 h-4" />
          {emailSent ? 'Email Sent!' : sendingEmail ? 'Sending...' : 'Send to Email'}
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={copyLink}
          className="flex items-center gap-2 px-5 py-2.5 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 font-medium rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition"
        >
          <Share2 className="w-4 h-4" />
          Share
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => navigate('/interview')}
          className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-medium rounded-xl hover:shadow-lg hover:shadow-indigo-500/30 transition-all"
        >
          <RefreshCw className="w-4 h-4" />
          Retake Interview
        </motion.button>

        <Link
          to="/leaderboard"
          className="flex items-center gap-2 px-5 py-2.5 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 font-medium rounded-xl hover:bg-amber-200 dark:hover:bg-amber-900/50 transition"
        >
          <Trophy className="w-4 h-4" />
          View Leaderboard
        </Link>
      </motion.div>
    </div>
  )
}
