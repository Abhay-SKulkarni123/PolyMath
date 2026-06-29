import axios, { AxiosError } from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
const API_TIMEOUT = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || "30000");

export const api = axios.create({
  baseURL: API_URL,
  timeout: API_TIMEOUT,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("access_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    // Django's APPEND_SLASH only auto-redirects in some configs, and that
    // redirect can behave inconsistently in production (extra round-trip,
    // CORS preflight issues on the redirect itself). Safer to always send
    // the trailing slash ourselves, so the request hits the real endpoint
    // on the first try - this fixes 404s like /api/cinema/collections
    // (missing slash) vs /api/cinema/collections/ (correct).
    if (config.url) {
      const hasQuery = config.url.includes("?");
      if (!hasQuery && !config.url.endsWith("/")) {
        config.url = `${config.url}/`;
      } else if (hasQuery) {
        const [path, query] = config.url.split("?");
        if (!path.endsWith("/")) {
          config.url = `${path}/?${query}`;
        }
      }
    }

    return config;
  },
  (error) => Promise.reject(error),
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  },
);

export default api;
