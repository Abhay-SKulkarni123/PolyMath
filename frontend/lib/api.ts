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

    // KNOWN AXIOS BUG (axios/axios#1405): axios silently strips the
    // trailing slash when it internally joins baseURL + a relative url,
    // even though config.url is correct at this point in the interceptor.
    // Workaround: bypass axios's own URL-joining entirely by building
    // the full absolute URL ourselves and clearing baseURL for this
    // request, so axios has nothing left to "normalize".
    if (config.url && config.baseURL) {
      let path = config.url;
      const hasQuery = path.includes("?");

      if (!hasQuery && !path.endsWith("/")) {
        path = `${path}/`;
      } else if (hasQuery) {
        const [p, query] = path.split("?");
        path = p.endsWith("/") ? `${p}?${query}` : `${p}/?${query}`;
      }

      const base = config.baseURL.endsWith("/") ? config.baseURL.slice(0, -1) : config.baseURL;
      const cleanPath = path.startsWith("/") ? path : `/${path}`;

      config.url = `${base}${cleanPath}`;
      config.baseURL = ""; // nothing left for axios to join/strip
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
