module.exports = {
  content: ['./index.html', './src/**/*.{ts,tsx,js,jsx}'],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#0f172a',
          925: '#131d2d',
          900: '#0f172a',
        },
        violet: {
          600: '#7c3aed',
          500: '#8b5cf6',
          400: '#a78bfa',
          300: '#c4b5fd',
        },
      },
      backgroundColor: {
        glass: 'rgba(15, 23, 42, 0.6)',
        'glass-light': 'rgba(15, 23, 42, 0.8)',
      },
      backdropFilter: {
        'blur-xl': 'blur(20px)',
      },
      boxShadow: {
        glow: '0 0 40px rgba(124, 58, 237, 0.25)',
        'glow-sm': '0 0 20px rgba(124, 58, 237, 0.15)',
        'glow-lg': '0 0 60px rgba(124, 58, 237, 0.3)',
        'glow-purple': '0 0 30px rgba(167, 139, 250, 0.2)',
      },
      borderColor: {
        'glass': 'rgba(124, 58, 237, 0.3)',
        'glass-light': 'rgba(124, 58, 237, 0.2)',
      },
      fontSize: {
        'display-xl': ['3.5rem', { lineHeight: '1.1', letterSpacing: '-0.02em' }],
      },
    },
  },
  plugins: [],
}
