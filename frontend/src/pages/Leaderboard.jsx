import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Medal, Star, TrendingUp } from 'lucide-react'
import api from '../services/api'
import { useAuthStore } from '../store/authStore'

export default function Leaderboard() {
  const { user } = useAuthStore()
  const [leaderboard, setLeaderboard] = useState([])
  const [myRank, setMyRank] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLeaderboard()
  }, [])

  const fetchLeaderboard = async () => {
    try {
      const [lbRes, rankRes] = await Promise.all([
        api.get('/leaderboard/'),
        api.get('/leaderboard/me'),
      ])
      setLeaderboard(lbRes.data.leaderboard)
      setMyRank(rankRes.data)
    } catch {
      // handle
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto space-y-4">
        <div className="h-8 w-48 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
        {[1, 2, 3, 4, 5].map(i => (
          <div key={i} className="h-16 bg-gray-200 dark:bg-gray-700 rounded-xl animate-pulse" />
        ))}
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
          <Trophy className="w-8 h-8 text-amber-500" />
          Leaderboard
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Top performers based on average interview scores
        </p>
      </div>

      {/* My Rank Card */}
      {myRank?.rank && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="opacity-80 text-sm">Your Rank</p>
              <div className="text-5xl font-black">#{myRank.rank}</div>
            </div>
            <div className="text-right">
              <p className="opacity-80 text-sm">Your Average</p>
              <div className="text-3xl font-bold">{myRank.avg_score}</div>
              <p className="opacity-80 text-sm">{myRank.total_interviews} interviews</p>
            </div>
          </div>
        </motion.div>
      )}

      {/* Not ranked yet */}
      {!myRank?.rank && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl p-8 text-center border border-gray-100 dark:border-gray-700"
        >
          <TrendingUp className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">
            You're not on the leaderboard yet
          </h3>
          <p className="text-sm text-gray-500">Complete your first interview to compete!</p>
        </motion.div>
      )}

      {/* Top 3 Podium */}
      {leaderboard.length >= 3 && (
        <div className="flex items-end justify-center gap-4 py-6">
          {/* 2nd */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="flex flex-col items-center"
          >
            <div className="w-16 h-16 bg-gray-300 dark:bg-gray-600 rounded-full flex items-center justify-center text-2xl mb-2">
              🥈
            </div>
            <div className="text-center">
              <div className="font-bold text-gray-900 dark:text-white">{leaderboard[1].name}</div>
              <div className="text-sm text-gray-500">{leaderboard[1].avg_score}</div>
            </div>
            <div className="w-20 h-24 bg-gray-200 dark:bg-gray-700 rounded-t-xl mt-2 flex items-end justify-center pb-2 text-2xl font-black text-gray-400">
              2
            </div>
          </motion.div>

          {/* 1st */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0 }}
            className="flex flex-col items-center"
          >
            <div className="w-20 h-20 bg-gradient-to-br from-amber-300 to-amber-500 rounded-full flex items-center justify-center text-3xl mb-2 shadow-lg shadow-amber-500/30">
              🥇
            </div>
            <div className="text-center">
              <div className="font-bold text-gray-900 dark:text-white">{leaderboard[0].name}</div>
              <div className="text-sm text-gray-500">{leaderboard[0].avg_score}</div>
            </div>
            <div className="w-24 h-32 bg-gradient-to-t from-amber-400 to-amber-500 rounded-t-xl mt-2 flex items-end justify-center pb-3 text-3xl font-black text-white">
              1
            </div>
          </motion.div>

          {/* 3rd */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="flex flex-col items-center"
          >
            <div className="w-16 h-16 bg-orange-300 dark:bg-orange-600 rounded-full flex items-center justify-center text-2xl mb-2">
              🥉
            </div>
            <div className="text-center">
              <div className="font-bold text-gray-900 dark:text-white">{leaderboard[2].name}</div>
              <div className="text-sm text-gray-500">{leaderboard[2].avg_score}</div>
            </div>
            <div className="w-20 h-16 bg-orange-200 dark:bg-orange-900/50 rounded-t-xl mt-2 flex items-end justify-center pb-2 text-2xl font-black text-orange-300">
              3
            </div>
          </motion.div>
        </div>
      )}

      {/* Full List */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 overflow-hidden">
        <div className="p-4 border-b border-gray-100 dark:border-gray-700 flex gap-4 text-sm font-medium text-gray-500 dark:text-gray-400">
          <span className="w-8">#</span>
          <span className="flex-1">Name</span>
          <span className="w-20 text-right">Avg Score</span>
          <span className="w-20 text-right">Interviews</span>
        </div>
        <div className="divide-y divide-gray-100 dark:divide-gray-700">
          {leaderboard.map((entry, i) => {
            const isMe = entry.user_id === user?.id
            return (
              <motion.div
                key={entry.user_id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.03 }}
                className={`p-4 flex items-center gap-4 ${
                  isMe ? 'bg-indigo-50 dark:bg-indigo-900/20' : ''
                }`}
              >
                <span className="w-8 text-lg font-bold text-gray-400">
                  {i < 3 ? ['', '🥇', '🥈', '🥉'][i + 1] : i + 1}
                </span>
                <span className={`flex-1 font-medium ${isMe ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-900 dark:text-white'}`}>
                  {entry.name} {isMe && <span className="text-xs">(You)</span>}
                </span>
                <span className="w-20 text-right font-bold text-gray-900 dark:text-white">
                  {entry.avg_score}
                </span>
                <span className="w-20 text-right text-gray-500 text-sm">
                  {entry.total_interviews}
                </span>
              </motion.div>
            )
          })}
        </div>

        {leaderboard.length === 0 && (
          <div className="p-12 text-center text-gray-500 dark:text-gray-400">
            No participants yet. Be the first!
          </div>
        )}
      </div>
    </div>
  )
}
