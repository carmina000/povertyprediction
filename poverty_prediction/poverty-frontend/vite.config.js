import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // This proxy tells the frontend to forward any request starting with /api
    // to your running Flask backend server at port 5000.
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        // The rewrite removes the /api prefix before sending it to Flask
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
    // Prevent the server from automatically opening the browser tab:
    open: false 
  }
})