"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await api.post("/api/auth/login/", { email, password });
      localStorage.setItem("access_token", res.data.tokens.access);
      localStorage.setItem("refresh_token", res.data.tokens.refresh);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      window.dispatchEvent(new Event("authChanged"));
      router.push("/products");
    } catch {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#0a0612",
        position: "relative"
      }}
    >
      <div
        style={{
          backgroundColor: "#150a26",
          padding: "48px",
          borderRadius: "24px",
          width: "100%",
          maxWidth: "420px",
          border: "1px solid rgba(168,85,247,0.25)",
          boxShadow: "0 24px 60px rgba(147,51,234,0.2)",
          position: "relative",
          zIndex: 1
        }}
      >
        <Link
          href="/"
          style={{
            fontFamily: "'Fraunces', serif",
            fontSize: "24px",
            fontWeight: 600,
            textDecoration: "none",
            color: "#ffffff",
            display: "block",
            marginBottom: "32px",
            textShadow: "0 0 20px rgba(168,85,247,0.4)"
          }}
        >
          🎬 Polymath
        </Link>

        <h1 style={{ fontSize: "24px", fontWeight: 700, marginBottom: "8px", color: "#ffffff" }}>
          Welcome back
        </h1>
        <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.5)", marginBottom: "32px" }}>
          Sign in to your account
        </p>

        {error && (
          <div
            style={{
              backgroundColor: "rgba(220,38,38,0.15)",
              color: "#fca5a5",
              border: "1px solid rgba(220,38,38,0.3)",
              padding: "12px 16px",
              borderRadius: "8px",
              fontSize: "14px",
              marginBottom: "24px",
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: "16px" }}>
            <label
              style={{
                fontSize: "13px",
                fontWeight: 500,
                display: "block",
                marginBottom: "6px",
                color: "rgba(255,255,255,0.6)"
              }}
            >
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              style={{
                width: "100%",
                padding: "12px 16px",
                borderRadius: "10px",
                border: "1px solid rgba(168,85,247,0.25)",
                backgroundColor: "#0a0612",
                color: "#ffffff",
                fontSize: "14px",
                outline: "none",
                boxSizing: "border-box",
              }}
              onFocus={(e) => { e.currentTarget.style.borderColor = "#c084fc"; }}
              onBlur={(e) => { e.currentTarget.style.borderColor = "rgba(168,85,247,0.25)"; }}
            />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label
              style={{
                fontSize: "13px",
                fontWeight: 500,
                display: "block",
                marginBottom: "6px",
                color: "rgba(255,255,255,0.6)"
              }}
            >
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              style={{
                width: "100%",
                padding: "12px 16px",
                borderRadius: "10px",
                border: "1px solid rgba(168,85,247,0.25)",
                backgroundColor: "#0a0612",
                color: "#ffffff",
                fontSize: "14px",
                outline: "none",
                boxSizing: "border-box",
              }}
              onFocus={(e) => { e.currentTarget.style.borderColor = "#c084fc"; }}
              onBlur={(e) => { e.currentTarget.style.borderColor = "rgba(168,85,247,0.25)"; }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px",
              borderRadius: "9999px",
              backgroundColor: "#9333ea",
              color: "#ffffff",
              fontSize: "14px",
              fontWeight: 600,
              border: "none",
              cursor: "pointer",
              opacity: loading ? 0.7 : 1,
              boxShadow: loading ? "none" : "0 0 24px rgba(147,51,234,0.45)",
              transition: "all 0.2s"
            }}
            onMouseEnter={(e) => { if (!loading) (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#a855f7"; }}
            onMouseLeave={(e) => { (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#9333ea"; }}
          >
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p
          style={{
            fontSize: "14px",
            color: "rgba(255,255,255,0.5)",
            textAlign: "center",
            marginTop: "24px",
          }}
        >
          Don't have an account?{" "}
          <Link
            href="/register"
            style={{
              color: "#c084fc",
              textDecoration: "none",
              fontWeight: 500,
            }}
          >
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}