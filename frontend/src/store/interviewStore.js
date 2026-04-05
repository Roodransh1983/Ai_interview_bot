import { create } from 'zustand'

export const useInterviewStore = create((set, get) => ({
  // Session state
  sessionId: null,
  questions: [],
  currentQuestionIndex: 0,
  mode: 'text',
  difficulty: 'medium',

  // Answer tracking
  answers: [],
  evaluations: [],
  isSubmitting: false,

  // Timer
  timeRemaining: 120,
  isTimerRunning: false,

  // WebSocket
  ws: null,

  // Actions
  setSession: (sessionId, questions, mode, difficulty) => set({
    sessionId,
    questions,
    currentQuestionIndex: 0,
    mode,
    difficulty,
    answers: [],
    evaluations: [],
    timeRemaining: 120,
  }),

  submitAnswer: (answer) => {
    set((state) => ({
      answers: [...state.answers, answer],
    }))
  },

  addEvaluation: (evaluation) => {
    set((state) => ({
      evaluations: [...state.evaluations, evaluation],
    }))
  },

  nextQuestion: () => {
    set((state) => ({
      currentQuestionIndex: state.currentQuestionIndex + 1,
      timeRemaining: 120,
    }))
  },

  setTimeRemaining: (seconds) => set({ timeRemaining: seconds }),
  setTimerRunning: (running) => set({ isTimerRunning: running }),

  connectWs: (token, onMessage) => {
    const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
    const ws = new WebSocket(`${WS_URL}/interview/ws`)

    ws.onopen = () => {
      ws.send(JSON.stringify({ token }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      onMessage(data)
    }

    ws.onerror = (error) => console.error('WebSocket error:', error)
    ws.onclose = () => console.log('WebSocket closed')

    set({ ws })
    return ws
  },

  sendWsMessage: (message) => {
    const { ws } = get()
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message))
    }
  },

  reset: () => set({
    sessionId: null,
    questions: [],
    currentQuestionIndex: 0,
    answers: [],
    evaluations: [],
    isSubmitting: false,
    timeRemaining: 120,
    isTimerRunning: false,
    ws: null,
  }),
}))
