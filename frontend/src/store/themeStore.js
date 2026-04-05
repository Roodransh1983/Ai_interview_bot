import { create } from 'zustand'

export const useThemeStore = create((set) => ({
  isDark: localStorage.getItem('theme') === 'dark' ||
    (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches),

  toggleTheme: () => {
    set((state) => {
      const newIsDark = !state.isDark
      localStorage.setItem('theme', newIsDark ? 'dark' : 'light')
      document.documentElement.classList.toggle('dark', newIsDark)
      return { isDark: newIsDark }
    })
  },

  initTheme: () => {
    const isDark = localStorage.getItem('theme') === 'dark' ||
      (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
    document.documentElement.classList.toggle('dark', isDark)
    set({ isDark })
  },
}))
