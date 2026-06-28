"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";
import { Order } from "@/lib/types";

export default function OrdersPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const res = await api.get("/api/orders/");
      setOrders(res.data.results || res.data || []);
      setError("");
    } catch (err) {
      console.error("Orders fetch error:", err);
      setError("Failed to load orders");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", position: "relative" }}>
        <div style={{ textAlign: "center", position: "relative", zIndex: 1 }}>
          <p style={{ color: "rgba(255,255,255,0.5)", marginTop: "60px" }}>Loading orders...</p>
        </div>
      </div>
    );
  }

  if (!orders || orders.length === 0) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", position: "relative" }}>
        <div
          style={{
            textAlign: "center",
            padding: "70px 40px 100px",
            position: "relative",
            zIndex: 1
          }}
        >
          <p
            style={{ fontSize: "18px", color: "rgba(255,255,255,0.5)", marginBottom: "24px", marginTop: "40px" }}
          >
            You haven't placed any orders yet
          </p>
          <Link
            href="/products"
            style={{
              backgroundColor: "#9333ea",
              color: "#ffffff",
              padding: "12px 28px",
              borderRadius: "9999px",
              textDecoration: "none",
              fontSize: "14px",
              fontWeight: 500,
              display: "inline-block",
              boxShadow: "0 0 20px rgba(147,51,234,0.4)"
            }}
          >
            Start shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>

      <div style={{ padding: "70px 40px 60px", position: "relative", zIndex: 1, boxSizing: "border-box" }}>
        <div style={{ maxWidth: "900px", margin: "0 auto", paddingTop: "30px" }}>
          <h1
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "40px",
              fontWeight: 300,
              marginBottom: "32px",
              textShadow: "0 0 24px rgba(168,85,247,0.3)"
            }}
          >
            Your Orders
          </h1>

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

          <div
            style={{ display: "flex", flexDirection: "column", gap: "16px" }}
          >
            {orders &&
              orders.length > 0 &&
              orders.map((order) => (
                <Link
                  key={order.id}
                  href={`/orders/${order.id}`}
                  style={{ textDecoration: "none", color: "inherit" }}
                >
                  <div
                    style={{
                      border: "1px solid rgba(168,85,247,0.2)",
                      borderRadius: "12px",
                      backgroundColor: "#150a26",
                      padding: "20px",
                      cursor: "pointer",
                      transition: "all 0.2s",
                    }}
                    onMouseEnter={(e) => {
                      const el = e.currentTarget as HTMLDivElement;
                      el.style.boxShadow = "0 8px 24px rgba(147,51,234,0.3)";
                      el.style.borderColor = "rgba(168,85,247,0.45)";
                    }}
                    onMouseLeave={(e) => {
                      const el = e.currentTarget as HTMLDivElement;
                      el.style.boxShadow = "none";
                      el.style.borderColor = "rgba(168,85,247,0.2)";
                    }}
                  >
                    <div
                      style={{
                        display: "grid",
                        gridTemplateColumns: "1fr 1fr 1fr auto",
                        gap: "20px",
                        alignItems: "center",
                      }}
                    >
                      {/* Order ID & Date */}
                      <div>
                        <p
                          style={{
                            fontSize: "12px",
                            color: "rgba(255,255,255,0.45)",
                            marginBottom: "4px",
                            textTransform: "uppercase",
                            fontWeight: 600,
                          }}
                        >
                          Order ID
                        </p>
                        <p style={{ fontSize: "16px", fontWeight: 700, color: "#ffffff" }}>
                          #{order.id}
                        </p>
                        <p
                          style={{
                            fontSize: "12px",
                            color: "rgba(255,255,255,0.4)",
                            marginTop: "8px",
                          }}
                        >
                          {order.created_at
                            ? new Date(order.created_at).toLocaleDateString()
                            : "N/A"}
                        </p>
                      </div>

                      {/* Items Count */}
                      <div>
                        <p
                          style={{
                            fontSize: "12px",
                            color: "rgba(255,255,255,0.45)",
                            marginBottom: "4px",
                            textTransform: "uppercase",
                            fontWeight: 600,
                          }}
                        >
                          Items
                        </p>
                        <p style={{ fontSize: "16px", fontWeight: 700, color: "#ffffff" }}>
                          {order.items ? order.items.length : 0} product
                          {(order.items?.length || 0) !== 1 ? "s" : ""}
                        </p>
                      </div>

                      {/* Total */}
                      <div>
                        <p
                          style={{
                            fontSize: "12px",
                            color: "rgba(255,255,255,0.45)",
                            marginBottom: "4px",
                            textTransform: "uppercase",
                            fontWeight: 600,
                          }}
                        >
                          Total
                        </p>
                        <p style={{ fontSize: "16px", fontWeight: 700, color: "#c084fc" }}>
                          ₹{order.total_price}
                        </p>
                      </div>

                      {/* Status */}
                      <div style={{ textAlign: "right" }}>
                        <span
                          style={{
                            fontSize: "12px",
                            fontWeight: 600,
                            backgroundColor:
                              order.status === "completed" ? "rgba(34,197,94,0.15)" :
                                order.status === "cancelled" ? "rgba(255,255,255,0.08)" : "rgba(245,158,11,0.15)",
                            color:
                              order.status === "completed" ? "#86efac" :
                                order.status === "cancelled" ? "rgba(255,255,255,0.5)" : "#fbbf24",
                            border:
                              order.status === "completed" ? "1px solid rgba(34,197,94,0.3)" :
                                order.status === "cancelled" ? "1px solid rgba(255,255,255,0.15)" : "1px solid rgba(245,158,11,0.3)",
                            padding: "6px 12px",
                            borderRadius: "9999px",
                            textTransform: "capitalize",
                          }}
                        >
                          {order.status}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}