import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, FileText, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import api from '../services/api'
import { useAuthStore } from '../store/authStore'

export default function ResumeUpload() {
  const navigate = useNavigate()
  const { user, fetchMe } = useAuthStore()
  const fileInputRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  // If already uploaded, show current resume
  useState(() => {
    if (user?.resume_uploaded) {
      loadExistingResume()
    }
  }, [user])

  const loadExistingResume = async () => {
    try {
      const res = await api.get('/resume/')
      if (res.data?.skills?.length > 0) {
        setResult(res.data)
      }
    } catch {}
  }

  const handleFile = (selectedFile) => {
    if (!selectedFile) return
    const ext = selectedFile.name.split('.').pop()?.toLowerCase()
    if (!['pdf', 'docx', 'doc'].includes(ext)) {
      setError('Please upload a PDF or DOCX file')
      return
    }
    setFile(selectedFile)
    setError(null)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    handleFile(droppedFile)
  }

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await api.post('/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(res.data)
      await fetchMe() // Refresh user state
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to parse resume')
    } finally {
      setUploading(false)
    }
  }

  const removeFile = () => {
    setFile(null)
    setResult(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Upload Your Resume</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          We'll analyze your skills and generate personalized interview questions
        </p>
      </div>

      {/* Upload Zone */}
      {!result ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700 p-12 text-center"
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          style={{
            borderColor: dragging ? '#6366f1' : undefined,
            background: dragging ? 'rgba(99, 102, 241, 0.05)' : undefined,
          }}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.doc"
            onChange={(e) => handleFile(e.target.files[0])}
            className="hidden"
          />

          <div className="w-16 h-16 bg-indigo-100 dark:bg-indigo-900/50 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Upload className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
          </div>

          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {file ? file.name : 'Drop your resume here'}
          </h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
            {file ? `${(file.size / 1024 / 1024).toFixed(2)} MB` : 'PDF or DOCX, max 10MB'}
          </p>

          {file ? (
            <div className="flex items-center justify-center gap-3">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleUpload}
                disabled={uploading}
                className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-indigo-500/30 transition-all disabled:opacity-60 flex items-center gap-2"
              >
                {uploading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Upload className="w-5 h-5" />
                    Upload & Analyze
                  </>
                )}
              </motion.button>
              <button
                onClick={removeFile}
                className="px-4 py-3 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => fileInputRef.current?.click()}
              className="px-6 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 font-semibold rounded-xl hover:bg-gray-200 dark:hover:bg-gray-600 transition"
            >
              Browse Files
            </motion.button>
          )}

          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 flex items-center justify-center gap-2 text-red-500 text-sm"
            >
              <AlertCircle className="w-4 h-4" />
              {error}
            </motion.div>
          )}
        </motion.div>
      ) : (
        /* Parsed Resume Preview */
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {/* Success Banner */}
          <div className="bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl p-4 mb-6 flex items-center gap-3">
            <CheckCircle className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <span className="text-emerald-800 dark:text-emerald-200 font-medium">Resume parsed successfully!</span>
            <button
              onClick={() => { removeFile(); setFile(null) }}
              className="ml-auto text-sm text-emerald-600 dark:text-emerald-400 hover:underline"
            >
              Upload new
            </button>
          </div>

          {/* Skills */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 mb-4">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-indigo-500" />
              <h3 className="text-lg font-bold text-gray-900 dark:text-white">Skills Detected</h3>
              <span className="ml-auto text-sm text-gray-500 dark:text-gray-400">{result.skills?.length || 0} skills</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {(result.skills || []).map((skill, i) => (
                <motion.span
                  key={skill}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.02 }}
                  className="px-3 py-1.5 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 text-sm font-medium rounded-lg"
                >
                  {skill}
                </motion.span>
              ))}
            </div>
          </div>

          {/* Projects */}
          {result.projects?.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-6 mb-4">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-3">Projects</h3>
              <div className="space-y-2">
                {result.projects.map((proj, i) => (
                  <div key={i} className="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                    <p className="text-sm text-gray-700 dark:text-gray-300">{proj}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-4">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => navigate('/interview')}
              className="flex-1 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-indigo-500/30 transition-all"
            >
              Start Interview Now
            </motion.button>
          </div>
        </motion.div>
      )}
    </div>
  )
}
