import typography from '@tailwindcss/typography';
import forms from '@tailwindcss/forms';
import aspectRatio from '@tailwindcss/aspect-ratio';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      screens: {
        sm: '480px',
        md: '768px',
        lg: '976px',
        xl: '1440px',
      },
      colors: {
        'primary': '#580726',
        'light-text': 'white',
        'dark-text': 'black',
        'error': 'rgba(255, 0, 0, 220)',
        'urgent': 'rgba(255, 0, 0, 200)',
        'success': 'rgba(0, 0, 255, 255)',
      }
    },
  },
  plugins: [
    typography,
    forms,
    aspectRatio,
  ],
}