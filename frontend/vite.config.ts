import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy /api and /health to the local FastAPI backend during development.
      "/api": "http://localhost:8000",
      "/health": "http://localhost:8000",
    },
  },
});
