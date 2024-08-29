import { fileURLToPath, URL } from "url";
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  // const env = loadEnv(mode, process.cwd(), '')
  return {
    plugins: [vue()],
  server: {
    port: 5174
  },
  resolve: {
    alias: [
      { find: '@', replacement: fileURLToPath(new URL('./src', import.meta.url)) },
      { find: '@assets', replacement: fileURLToPath(new URL('./src/assets', import.meta.url)) },
      { find: '@components', replacement: fileURLToPath(new URL('./src/components', import.meta.url)) },
      { find: '@layouts', replacement: fileURLToPath(new URL('./src/layouts', import.meta.url)) },
      { find: '@views', replacement: fileURLToPath(new URL('./src/views', import.meta.url)) },
    ],
  },
  }
})

