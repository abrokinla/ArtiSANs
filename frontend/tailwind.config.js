/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Airbnb Design System Colors
        'rausch': {
          DEFAULT: '#ff385c',
          deep: '#e00b41',
        },
        'luxe': {
          purple: '#460479',
        },
        'plus': {
          magenta: '#92174d',
        },
        'text': {
          primary: '#222222',
          focused: '#3f3f3f',
          secondary: '#6a6a6a',
          disabled: 'rgba(0, 0, 0, 0.24)',
          error: '#c13515',
          legal: '#428bff',
        },
        'bg': {
          secondary: '#f2f2f2',
          tertiary: '#f7f7f7',
        },
        'border': {
          DEFAULT: '#c1c1c1',
          light: 'rgba(0, 0, 0, 0.08)',
        },
      },
      fontFamily: {
        'sans': ['DM Sans', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
        'mono': ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace'],
      },
      borderRadius: {
        'sm': '8px',
        'md': '14px',
        'lg': '20px',
        'xl': '32px',
        'full': '50%',
      },
      boxShadow: {
        'card': 'rgba(0, 0, 0, 0.02) 0px 0px 0px 1px, rgba(0, 0, 0, 0.04) 0px 2px 6px, rgba(0, 0, 0, 0.1) 0px 4px 8px',
        'hover': 'rgba(0, 0, 0, 0.08) 0px 4px 12px',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      maxWidth: {
        '8xl': '88rem',
      },
    },
  },
  plugins: [],
}
