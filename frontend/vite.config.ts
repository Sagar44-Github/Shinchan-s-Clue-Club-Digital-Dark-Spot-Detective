import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, strictPort: true },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('/node_modules/three/')) return 'three-core'
          if (id.includes('/node_modules/@react-three/')) return 'three-react'
          if (id.includes('/node_modules/three-stdlib/')) return 'three-extras'
          if (id.includes('/node_modules/framer-motion/')) return 'motion'
        },
      },
    },
  },
})
