"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/api/auth/register/", form);
      const res = await api.post("/api/auth/login/", {
        email: form.email,
        password: form.password,
      });
      localStorage.setItem("access_token", res.data.tokens.access);
      localStorage.setItem("refresh_token", res.data.tokens.refresh);
      localStorage.setItem("user", JSON.stringify(res.data.user));
      router.push("/products");
    } catch (err: unknown) {
      setError("Registration failed. Please check your details.");
    } finally {
      setLoading(false);
    }
  };

  const fields = [
    { name: "first_name", label: "First name", type: "text", placeholder: "Abhay" },
    { name: "last_name", label: "Last name", type: "text", placeholder: "Kulkarni" },
    { name: "email", label: "Email", type: "email", placeholder: "you@example.com" },
    { name: "password", label: "Password", type: "password", placeholder: "••••••••" },
    { name: "confirm_password", label: "Confirm password", type: "password", placeholder: "••••••••" },
  ];

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#0a0612",
        padding: "40px 20px",
        position: "relative",
        boxSizing: "border-box"
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
          Create account
        </h1>
        <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.5)", marginBottom: "32px" }}>
          Join thousands of curious minds
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

        <form onSubmit={handleRegister}>
          {fields.map((field) => (
            <div key={field.name} style={{ marginBottom: "16px" }}>
              <label
                style={{
                  fontSize: "13px",
                  fontWeight: 500,
                  display: "block",
                  marginBottom: "6px",
                  color: "rgba(255,255,255,0.6)"
                }}
              >
                {field.label}
              </label>
              <input
                type={field.type}
                name={field.name}
                value={form[field.name as keyof typeof form]}
                onChange={handleChange}
                placeholder={field.placeholder}
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
          ))}

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
              marginTop: "8px",
              opacity: loading ? 0.7 : 1,
              boxShadow: loading ? "none" : "0 0 24px rgba(147,51,234,0.45)",
              transition: "all 0.2s"
            }}
            onMouseEnter={(e) => { if (!loading) (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#a855f7"; }}
            onMouseLeave={(e) => { (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#9333ea"; }}
          >
            {loading ? "Creating account..." : "Create account"}
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
          Already have an account?{" "}
          <Link
            href="/login"
            style={{
              color: "#c084fc",
              textDecoration: "none",
              fontWeight: 500,
            }}
          >
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}