// API Configuration for the chat widget
// Dynamic URL that works for both local development and GitHub Pages
// In production (GitHub Pages), this will need to point to your deployed backend
let API_BASE_URL;

if (typeof window !== 'undefined') {
  // Client-side (browser) environment
  // For GitHub Pages, you'll need to update this to your deployed backend URL
  // For local development with backend running on localhost:8000:
  // API_BASE_URL = 'http://localhost:8000';

  // For GitHub Pages deployment, update this to your deployed backend URL
  // For example: 'https://your-deployed-backend.onrender.com' or similar
  API_BASE_URL = 'https://localhost:8000'; // Update this to your deployed backend URL
} else {
  // Server-side (build time) environment
  API_BASE_URL = 'http://localhost:8000'; // Default for builds
}

// Alternative: Use the current origin for same-domain deployment
// API_BASE_URL = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8000';

export const API_CONFIG = {
  BASE_URL: API_BASE_URL,
  ENDPOINTS: {
    CHAT: '/api/chat',
    SEARCH: '/api/search',
    HEALTH: '/api/health'
  },
  HEADERS: {
    'Content-Type': 'application/json',
  }
};

export default API_CONFIG;