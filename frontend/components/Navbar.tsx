"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const loadUser = () => {
      const stored = localStorage.getItem("user");

      if (stored) {
        try {
          setUser(JSON.parse(stored));
        } catch {
          setUser(null);
        }
      } else {
        setUser(null);
      }
    };

    loadUser();

    window.addEventListener("authChanged", loadUser);

    return () => {
      window.removeEventListener("authChanged", loadUser);
    };
  }, []);

  const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    setUser(null);

    window.dispatchEvent(new Event("authChanged"));

    router.push("/");
  };

  return (
    <nav
      style={{
        position: "sticky",
        top: 0,
        padding: "0 40px",
        height: "70px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: "rgba(8,6,16,0.15)",
        backdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(168,85,247,0.15)",
        transition: "all 0.3s ease",
        zIndex: 1000,
      }}
    >
      {/* Logo */}
      <Link href="/" style={{ textDecoration: "none", display: "flex", alignItems: "center", gap: "10px" }}>
        <span style={{ fontSize: "22px" }}>🎬</span>
        <span
          style={{
            fontFamily: "'Fraunces', serif",
            fontSize: "22px",
            fontWeight: 700,
            color: "#ffffff",
            letterSpacing: "-0.5px",
          }}
        >
          Polymath
        </span>
      </Link>

      {/* Nav Links */}
      <div style={{ display: "flex", gap: "28px", alignItems: "center" }}>
        <Link
          href="/"
          style={{
            color: "rgba(255,255,255,0.7)",
            textDecoration: "none",
            fontSize: "14px",
            fontWeight: 500,
            transition: "color 0.2s",
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
          onMouseLeave={(e) => (e.currentTarget.style.color = "rgba(255,255,255,0.7)")}
        >
          Home
        </Link>
        <Link
          href="/collections"
          style={{
            color: "rgba(255,255,255,0.7)",
            textDecoration: "none",
            fontSize: "14px",
            fontWeight: 500,
            transition: "color 0.2s",
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
          onMouseLeave={(e) => (e.currentTarget.style.color = "rgba(255,255,255,0.7)")}
        >
          Collections
        </Link>
        <Link
          href="/products"
          style={{
            color: "rgba(255,255,255,0.7)",
            textDecoration: "none",
            fontSize: "14px",
            fontWeight: 500,
            transition: "color 0.2s",
          }}
          onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
          onMouseLeave={(e) => (e.currentTarget.style.color = "rgba(255,255,255,0.7)")}
        >
          Books
        </Link>
        {user && (
          <Link
            href="/orders"
            style={{
              color: "rgba(255,255,255,0.7)",
              textDecoration: "none",
              fontSize: "14px",
              fontWeight: 500,
              transition: "color 0.2s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.color = "#ffffff")}
            onMouseLeave={(e) => (e.currentTarget.style.color = "rgba(255,255,255,0.7)")}
          >
            Orders
          </Link>
        )}
      </div>

      {/* Auth */}
      <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
        {user ? (
          <>
            <Link
              href="/cart"
              style={{
                color: "#ffffff",
                textDecoration: "none",
                fontSize: "18px",
                width: "36px",
                height: "36px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                borderRadius: "50%",
                backgroundColor: "rgba(255,255,255,0.1)",
              }}
            >
              🛒
            </Link>
            <span style={{ color: "rgba(255,255,255,0.5)", fontSize: "13px" }}>{user.first_name || user.email}</span>
            <button
              onClick={logout}
              style={{
                backgroundColor: "rgba(255,255,255,0.1)",
                color: "#ffffff",
                border: "1px solid rgba(255,255,255,0.2)",
                padding: "8px 18px",
                borderRadius: "9999px",
                cursor: "pointer",
                fontSize: "13px",
                fontWeight: 500,
                transition: "all 0.2s",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "rgba(255,255,255,0.2)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "rgba(255,255,255,0.1)";
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link
              href="/login"
              style={{ color: "rgba(255,255,255,0.7)", textDecoration: "none", fontSize: "14px", fontWeight: 500 }}
            >
              Login
            </Link>
            <Link
              href="/register"
              style={{
                backgroundColor: "#7c3aed",
                color: "#ffffff",
                textDecoration: "none",
                padding: "9px 22px",
                borderRadius: "9999px",
                fontSize: "13px",
                fontWeight: 600,
                transition: "all 0.2s",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLAnchorElement).style.backgroundColor = "#6d28d9";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLAnchorElement).style.backgroundColor = "#7c3aed";
              }}
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
