import { useState, useEffect, useRef, useCallback } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Bot, Send, Mic, Video, Clock, AlertTriangle, Eye, EyeOff, X, ChevronRight } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { useInterviewStore } from '../store/interviewStore'
import api from '../services/api'

// Sound effects (simple Web Audio API beeps)
const playSound = (type) => {
  const ctx = new AudioContext()
  const osc = ctx.createOscillator()
  const gain = ctx.createGain()
  osc.connect(gain)
  gain.connect(ctx.destination)
  gain.gain.value = 0.1
  osc.start()
  if (type === 'ding') {
    osc.frequency.value = 880
    osc.stop(ctx.currentTime + 0.1)
  } else if (type === 'tick') {
    osc.frequency.value = 440
    osc.stop(ctx.currentTime + 0.05)
  } else if (type === 'success') {
    osc.frequency.value = 1320
    gain.gain.value = 0.15
    osc.stop(ctx.currentTime + 0.3)
  }
}

export default function InterviewMode() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { token } = useAuthStore()
  const {
    sessionId, questions, currentQuestionIndex, mode,
    answers, evaluations, timeRemaining,
    setSession, submitAnswer, addEvaluation, nextQuestion,
    setTimeRemaining, setTimerRunning, reset,
  } = useInterviewStore()

  // UI State
  const [step, setStep] = useState('setup') // setup | interview | complete
  const [selectedMode, setSelectedMode] = useState(searchParams.get('mode') || 'text')
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium')
  const [answerText, setAnswerText] = useState('')
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [chatMessages, setChatMessages] = useState([])
  const [isAiTyping, setIsAiTyping] = useState(false)
  const [lookingAway, setLookingAway] = useState(false)
  const [showWarning, setShowWarning] = useState(false)

  // Video refs
  const videoRef = useRef(null)
  const mediaStreamRef = useRef(null)
  const faceMeshRef = useRef(null)

  const isTextMode = selectedMode === 'text'

  // Timer effect
  useEffect(() => {
    let interval
    if (step === 'interview' && timeRemaining > 0) {
      setTimerRunning(true)
      interval = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 11 && prev > 1) playSound('tick')
          if (prev <= 1) {
            handleSubmitAnswer(true) // auto-submit on timeout
            return 0
          }
          return prev - 1
        })
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [step, currentQuestionIndex])

  // Setup interview
  const startInterview = async () => {
    try {
      const res = await api.post('/interview/start', null, {
        params: { mode: selectedMode, difficulty: selectedDifficulty, num_questions: 5 },
      })
      const data = res.data
      setSession(data.session_id, data.total_questions, selectedMode, selectedDifficulty)
      setCurrentQuestion(data.current_question)
      setChatMessages([{
        type: 'ai',
        text: `👋 Hello! I'm your AI interviewer. I'll ask you ${data.total_questions} questions. Let's start!\n\n**Q1:** ${data.current_question.text}`,
      }])
      setStep('interview')
      playSound('ding')

      if (selectedMode === 'video') {
        initVideo()
      }
    } catch (err) {
      console.error('Failed to start interview:', err)
    }
  }

  // Submit answer
  const handleSubmitAnswer = async (isTimeout = false) => {
    if (!answerText.trim() && !isTimeout) return
    if (!currentQuestion) return

    setIsSubmitting(true)
    const finalAnswer = isTimeout && !answerText.trim() ? 'No answer provided (time expired)' : answerText

    try {
      // Add user message to chat
      if (isTextMode) {
        setChatMessages((prev) => [...prev, { type: 'user', text: finalAnswer }])
        setIsAiTyping(true)
      }

      const res = await api.post('/interview/answer', null, {
        params: { session_id: sessionId, question_id: currentQuestion.id, answer_text: finalAnswer },
      })
      const result = res.data

      // Store evaluation
      addEvaluation(result.evaluation)

      if (isTextMode) {
        // Show evaluation feedback
        setTimeout(() => {
          setIsAiTyping(false)
          setChatMessages((prev) => [...prev, {
            type: 'evaluation',
            score: result.evaluation.score,
            feedback: result.evaluation.feedback,
          }])
          playSound('ding')

          if (result.has_next) {
            // Show next question
            setTimeout(() => {
              setChatMessages((prev) => [...prev, {
                type: 'ai',
                text: `**Q${result.next_question.number}:** ${result.next_question.text}`,
              }])
              setCurrentQuestion(result.next_question)
              nextQuestion()
              setAnswerText('')
              setTimeRemaining(120)
            }, 1500)
          } else {
            // Interview complete
            completeInterview()
          }
        }, 1000)
      } else {
        // Video mode — just advance
        if (result.has_next) {
          setCurrentQuestion(result.next_question)
          nextQuestion()
          setAnswerText('')
          setTimeRemaining(120)
        } else {
          completeInterview()
        }
      }
    } catch (err) {
      console.error('Failed to submit answer:', err)
      setIsAiTyping(false)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Complete interview
  const completeInterview = async () => {
    playSound('success')
    try {
      const res = await api.post(`/interview/complete/${sessionId}`)
      navigate(`/report/${res.data.report_id}`)
      reset()
    } catch (err) {
      console.error('Failed to complete interview:', err)
    }
  }

  // End early
  const handleEndEarly = () => {
    if (window.confirm('End interview early? You will receive a report based on answered questions.')) {
      completeInterview()
    }
  }

  // Video setup
  const initVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      mediaStreamRef.current = stream
      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }

      // Load MediaPipe Face Mesh
      const { FaceMesh } = await import('@mediapipe/face_mesh')
      const faceMesh = new FaceMesh({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
      })
      faceMesh.setOptions({ maxNumFaces: 1, refineLandmarks: true, minDetectionConfidence: 0.5 })
      faceMesh.onResults(onFaceMeshResults)
      faceMeshRef.current = faceMesh

      // Process video frames
      const processFrame = async () => {
        if (videoRef.current && faceMeshRef.current) {
          await faceMeshRef.current.send({ image: videoRef.current })
        }
        requestAnimationFrame(processFrame)
      }
      processFrame()
    } catch (err) {
      console.error('Camera access denied:', err)
      alert('Camera access is required for video interview mode')
    }
  }

  const onFaceMeshResults = (results) => {
    if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
      const landmarks = results.multiFaceLandmarks[0]
      // Nose tip is landmark 1
      const nose = landmarks[1]
      const isLookingAway = nose.x < 0.3 || nose.x > 0.7
      setLookingAway(isLookingAway)
      if (isLookingAway && !showWarning) {
        setShowWarning(true)
        playSound('tick')
      } else if (!isLookingAway) {
        setShowWarning(false)
      }
    }
  }

  useEffect(() => {
    return () => {
      // Cleanup
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(t => t.stop())
      }
      if (faceMeshRef.current) {
        faceMeshRef.current.close()
      }
      reset()
    }
  }, [])

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m}:${s.toString().padStart(2, '0')}`
  }

  // ===== RENDER =====

  // SETUP STEP
  if (step === 'setup') {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Start Your Interview</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">Configure your practice session</p>
        </div>

        {/* Mode Selection */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-100 dark:border-gray-700">
          <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Select Mode</h3>
          <div className="grid grid-cols-2 gap-4">
            {[
              { id: 'text', label: 'Text Chat', icon: Mic, desc: 'Type your answers' },
              { id: 'video', label: 'Video Interview', icon: Video, desc: 'Practice on camera' },
            ].map((m) => (
              <motion.button
                key={m.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedMode(m.id)}
                className={`p-4 rounded-xl border-2 text-left transition ${
                  selectedMode === m.id
                    ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20'
                    : 'border-gray-200 dark:border-gray-600 hover:border-indigo-300'
                }`}
              >
                <m.icon className={`w-6 h-6 mb-2 ${selectedMode === m.id ? 'text-indigo-500' : 'text-gray-400'}`} />
                <div className="font-semibold text-gray-900 dark:text-white">{m.label}</div>
                <div className="text-sm text-gray-500">{m.desc}</div>
              </motion.button>
            ))}
          </div>
        </div>

        {/* Difficulty */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-100 dark:border-gray-700">
          <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Select Difficulty</h3>
          <div className="flex gap-3">
            {['easy', 'medium', 'hard'].map((d) => (
              <button
                key={d}
                onClick={() => setSelectedDifficulty(d)}
                className={`flex-1 py-3 rounded-xl font-medium capitalize transition ${
                  selectedDifficulty === d
                    ? 'bg-indigo-500 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>

        {/* Info */}
        <div className="bg-indigo-50 dark:bg-indigo-900/20 rounded-xl p-4 text-sm text-indigo-800 dark:text-indigo-300">
          <p>📋 <strong>5 questions</strong> based on your resume • <strong>2 minutes</strong> per question • Real-time AI feedback</p>
        </div>

        {/* Start Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={startInterview}
          className="w-full py-4 bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-lg font-bold rounded-xl hover:shadow-xl hover:shadow-indigo-500/30 transition-all"
        >
          Begin Interview
        </motion.button>
      </div>
    )
  }

  // INTERVIEW STEP
  return (
    <div className="max-w-5xl mx-auto">
      {/* Header Bar */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="font-semibold text-gray-900 dark:text-white">
              Q{currentQuestionIndex + 1} of {questions}
            </div>
            <div className="text-xs text-gray-500">{currentQuestion?.category}</div>
          </div>
        </div>

        {/* Timer */}
        <div className={`flex items-center gap-2 px-4 py-2 rounded-lg font-mono text-lg font-bold ${
          timeRemaining <= 10 ? 'bg-red-100 dark:bg-red-900/30 text-red-600 animate-pulse' : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
        }`}>
          <Clock className="w-5 h-5" />
          {formatTime(timeRemaining)}
        </div>

        {/* Looking Away Warning */}
        {selectedMode === 'video' && showWarning && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center gap-2 px-4 py-2 bg-amber-100 dark:bg-amber-900/30 rounded-lg text-amber-700 dark:text-amber-400 font-medium"
          >
            <EyeOff className="w-5 h-5" />
            Looking Away!
          </motion.div>
        )}

        <button
          onClick={handleEndEarly}
          className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition"
        >
          <X className="w-6 h-6" />
        </button>
      </div>

      {/* Progress Bar */}
      <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full mb-6 overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-indigo-500 to-purple-600"
          initial={{ width: 0 }}
          animate={{ width: `${((currentQuestionIndex) / questions) * 100}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className={`${isTextMode ? 'lg:col-span-2' : 'lg:col-span-3'}`}>
          {/* Video Panel */}
          {!isTextMode && (
            <div className="bg-gray-900 rounded-2xl overflow-hidden mb-4 aspect-video relative">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover"
              />
              {/* Recording indicator */}
              <div className="absolute top-4 right-4 flex items-center gap-2 px-3 py-1 bg-red-600 rounded-full text-white text-xs font-medium">
                <span className="w-2 h-2 bg-white rounded-full animate-pulse" />
                REC
              </div>
              {/* Looking away overlay */}
              {showWarning && (
                <div className="absolute inset-0 bg-red-500/20 flex items-center justify-center">
                  <div className="bg-red-600 text-white px-6 py-3 rounded-xl font-bold flex items-center gap-2">
                    <EyeOff className="w-5 h-5" />
                    Please look at the camera
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Question Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-100 dark:border-gray-700 mb-4">
            <div className="flex items-start gap-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-xl flex items-center justify-center flex-shrink-0 avatar-glow">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="font-semibold text-gray-900 dark:text-white mb-1">
                  AI Interviewer
                </div>
                <div className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed">
                  {currentQuestion?.text}
                </div>
              </div>
            </div>

            {/* Answer Input */}
            {isTextMode ? (
              <div className="mt-4">
                <textarea
                  value={answerText}
                  onChange={(e) => setAnswerText(e.target.value)}
                  placeholder="Type your answer here..."
                  rows={5}
                  disabled={isSubmitting}
                  className="w-full p-4 rounded-xl border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white resize-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition"
                />
                <div className="flex items-center justify-between mt-3">
                  <span className="text-sm text-gray-500">
                    {answerText.split(' ').filter(Boolean).length} words
                  </span>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleSubmitAnswer(false)}
                    disabled={!answerText.trim() || isSubmitting}
                    className="px-6 py-2.5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-indigo-500/30 transition-all disabled:opacity-50 flex items-center gap-2"
                  >
                    <Send className="w-4 h-4" />
                    Submit Answer
                  </motion.button>
                </div>
              </div>
            ) : (
              <div className="mt-4 text-center">
                <p className="text-gray-500 dark:text-gray-400 mb-4">
                  Answer verbally — the timer will auto-submit when time runs out
                </p>
                <div className="text-4xl font-bold text-gray-300 dark:text-gray-600">
                  {formatTime(timeRemaining)}
                </div>
                <motion.button
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleSubmitAnswer(true)}
                  className="mt-4 px-6 py-2.5 bg-red-500 text-white font-semibold rounded-xl"
                >
                  End Answer (Time Up)
                </motion.button>
              </div>
            )}
          </div>
        </div>

        {/* Chat Panel (Text Mode) */}
        {isTextMode && (
          <div className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 flex flex-col h-[500px]">
            <div className="p-4 border-b border-gray-100 dark:border-gray-700 font-semibold text-gray-900 dark:text-white">
              Chat History
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <AnimatePresence>
                {chatMessages.map((msg, i) => {
                  if (msg.type === 'ai') {
                    return (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="flex gap-3"
                      >
                        <div className="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                          <Bot className="w-4 h-4 text-white" />
                        </div>
                        <div className="chat-bubble-ai px-4 py-3 max-w-[85%]">
                          <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                        </div>
                      </motion.div>
                    )
                  } else if (msg.type === 'user') {
                    return (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="flex justify-end"
                      >
                        <div className="chat-bubble-user px-4 py-3 max-w-[85%]">
                          <p className="text-sm">{msg.text}</p>
                        </div>
                      </motion.div>
                    )
                  } else if (msg.type === 'evaluation') {
                    return (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-gray-50 dark:bg-gray-700 rounded-xl p-4 text-sm"
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <span className={`font-bold text-lg ${
                            msg.score >= 70 ? 'text-green-600' : msg.score >= 50 ? 'text-amber-600' : 'text-red-600'
                          }`}>
                            Score: {msg.score}/100
                          </span>
                        </div>
                        <p className="text-gray-600 dark:text-gray-300">{msg.feedback}</p>
                      </motion.div>
                    )
                  }
                  return null
                })}

                {isAiTyping && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex gap-3"
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-gray-100 dark:bg-gray-700 rounded-xl px-4 py-3 flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
                      <span className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
                      <span className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
