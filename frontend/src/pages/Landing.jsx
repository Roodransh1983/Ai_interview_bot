import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Bot, Mic, Video, FileText, Zap, Shield } from 'lucide-react'

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-indigo-900">
      {/* Nav */}
      <nav className="p-6 flex justify-between items-center max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-2"
        >
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900 dark:text-white">AI Interview Bot</span>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex gap-4"
        >
          <Link
            to="/login"
            className="px-5 py-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition"
          >
            Login
          </Link>
          <Link
            to="/register"
            className="px-5 py-2 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-lg hover:shadow-lg hover:shadow-indigo-500/30 transition-all"
          >
            Get Started
          </Link>
        </motion.div>
      </nav>

      {/* Hero */}
      <main className="max-w-7xl mx-auto px-6 pt-20 pb-32">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-100 dark:bg-indigo-900/50 rounded-full text-indigo-600 dark:text-indigo-400 text-sm font-medium mb-6">
            <Zap className="w-4 h-4" />
            Powered by Custom AI — No External APIs
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
            Ace Your Next Interview with
            <span className="bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent"> AI-Powered Practice</span>
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-10 max-w-2xl mx-auto">
            Experience realistic interview simulations with custom AI that analyzes your answers,
            detects confidence levels, and gives you personalized feedback — all without external AI services.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="px-8 py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-lg font-semibold rounded-xl hover:shadow-xl hover:shadow-indigo-500/30 transition-all hover:scale-105"
            >
              Start Free Interview
            </Link>
            <Link
              to="/login"
              className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 text-lg font-semibold rounded-xl border border-gray-200 dark:border-gray-700 hover:border-indigo-300 dark:hover:border-indigo-600 transition-all"
            >
              Sign In
            </Link>
          </div>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-24 grid md:grid-cols-3 gap-8"
        >
          {[
            { icon: Mic, title: 'Text & Voice Mode', desc: 'Chat-based interviews or real-time video simulation with face detection.' },
            { icon: FileText, title: 'Resume Parsing', desc: 'Upload your resume and get questions tailored to your actual skills.' },
            { icon: Shield, title: 'Custom AI Engine', desc: 'Built entirely with TF-IDF, NLP, and ML — no OpenAI or external APIs.' },
          ].map((f, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 + i * 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-lg transition-shadow"
            >
              <div className="w-14 h-14 bg-indigo-100 dark:bg-indigo-900/50 rounded-xl flex items-center justify-center mb-5">
                <f.icon className="w-7 h-7 text-indigo-600 dark:text-indigo-400" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">{f.title}</h3>
              <p className="text-gray-600 dark:text-gray-400">{f.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </main>
    </div>
  )
}
