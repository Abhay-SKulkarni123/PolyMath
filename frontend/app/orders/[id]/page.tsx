"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";
import { Order } from "@/lib/types";

export default function OrderDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [downloading, setDownloading] = useState<number | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetchOrder();
  }, [id]);

  const fetchOrder = async () => {
    try {
      setLoading(true);
      const res = await api.get(`/api/orders/${id}/`);
      setOrder(res.data.data || res.data);
      setError("");
    } catch (err) {
      console.error("Order fetch error:", err);
      setError("Failed to load order");
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = async (downloadUrl: string, itemId: number) => {
    setDownloading(itemId);
    try {
      const response = await api.get(downloadUrl, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "product");
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
    } catch (err) {
      alert("Failed to download file");
    } finally {
      setDownloading(null);
    }
  };

  const [cancelling, setCancelling] = useState(false);

  const cancelOrder = async () => {
    if (!order) return;
    if (!window.confirm("Cancel this order? This cannot be undone.")) return;

    setCancelling(true);
    try {
      await api.post(`/api/orders/${order.id}/cancel/`);
      fetchOrder();
    } catch (err) {
      setError("Failed to cancel order");
    } finally {
      setCancelling(false);
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", position: "relative" }}>
        <div style={{ textAlign: "center", position: "relative", zIndex: 1 }}>
          <p style={{ color: "rgba(255,255,255,0.5)", marginTop: "60px" }}>Loading order...</p>
        </div>
      </div>
    );
  }

  if (!order) {
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
          <p style={{ color: "rgba(255,255,255,0.5)", marginBottom: "24px", marginTop: "40px" }}>
            Order not found
          </p>
          <Link
            href="/orders"
            style={{ color: "#c084fc", textDecoration: "none" }}
          >
            Back to orders
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>

      <div style={{ padding: "70px 40px 60px", position: "relative", zIndex: 1, boxSizing: "border-box" }}>
        <div style={{ maxWidth: "900px", margin: "0 auto", paddingTop: "30px" }}>
          <Link
            href="/orders"
            style={{
              color: "#c084fc",
              textDecoration: "none",
              fontSize: "14px",
            }}
          >
            ← Back to orders
          </Link>

          <h1
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "40px",
              fontWeight: 300,
              margin: "20px 0 32px",
              textShadow: "0 0 24px rgba(168,85,247,0.3)"
            }}
          >
            Order #{order.id}
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
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 320px",
              gap: "40px",
            }}
          >
            {/* Order Details */}
            <div>
              {/* Status */}
              <div
                style={{
                  backgroundColor: "#150a26",
                  border: "1px solid rgba(168,85,247,0.2)",
                  borderRadius: "12px",
                  padding: "20px",
                  marginBottom: "32px",
                }}
              >
                <p
                  style={{
                    fontSize: "12px",
                    color: "rgba(255,255,255,0.45)",
                    marginBottom: "8px",
                    textTransform: "uppercase",
                    fontWeight: 600,
                  }}
                >
                  Status
                </p>
                <span
                  style={{
                    fontSize: "14px",
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
                    padding: "8px 16px",
                    borderRadius: "9999px",
                    textTransform: "capitalize",
                    display: "inline-block",
                  }}
                >
                  {order.status}
                </span>

                <p
                  style={{
                    fontSize: "12px",
                    color: "rgba(255,255,255,0.4)",
                    marginTop: "16px",
                  }}
                >
                  Placed on{" "}
                  {order.created_at
                    ? new Date(order.created_at).toLocaleDateString()
                    : "N/A"}
                </p>

                {order.status !== "completed" && order.status !== "cancelled" && (
                  <button
                    onClick={cancelOrder}
                    disabled={cancelling}
                    style={{
                      marginTop: "16px",
                      backgroundColor: "rgba(220,38,38,0.15)",
                      color: "#fca5a5",
                      border: "1px solid rgba(220,38,38,0.3)",
                      padding: "10px 20px",
                      borderRadius: "8px",
                      cursor: cancelling ? "not-allowed" : "pointer",
                      fontSize: "13px",
                      fontWeight: 600,
                      opacity: cancelling ? 0.6 : 1
                    }}
                  >
                    {cancelling ? "Cancelling..." : "Cancel Order"}
                  </button>
                )}
              </div>

              {/* Items */}
              <div
                style={{
                  backgroundColor: "#150a26",
                  border: "1px solid rgba(168,85,247,0.2)",
                  borderRadius: "12px",
                  padding: "20px",
                  marginBottom: "32px",
                }}
              >
                <h3
                  style={{
                    fontSize: "16px",
                    fontWeight: 700,
                    marginBottom: "16px",
                    color: "#ffffff"
                  }}
                >
                  Order Items
                </h3>

                {order.items && order.items.length > 0 ? (
                  order.items.map((item, idx) => (
                    <div
                      key={idx}
                      style={{
                        borderBottom:
                          idx < (order.items?.length || 0) - 1
                            ? "1px solid rgba(168,85,247,0.15)"
                            : "none",
                        paddingBottom: "16px",
                        marginBottom: "16px",
                      }}
                    >
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "start",
                          marginBottom: "12px",
                        }}
                      >
                        <div>
                          <p style={{ fontSize: "14px", fontWeight: 600, color: "#ffffff" }}>
                            {item.product_name}
                          </p>
                          <p style={{ fontSize: "12px", color: "rgba(255,255,255,0.45)" }}>
                            Type: {item.product_type} • Qty: {item.quantity}
                          </p>
                        </div>
                        <p style={{ fontSize: "14px", fontWeight: 700, color: "#c084fc" }}>
                          ₹
                          {item.item_total
                            ? item.item_total.toFixed(2)
                            : "0.00"}
                        </p>
                      </div>

                      {/* Download Button for Digital Products */}
                      {item.download_url && (
                        <button
                          onClick={() =>
                            downloadFile(item.download_url!, item.id)
                          }
                          disabled={downloading === item.id}
                          style={{
                            fontSize: "12px",
                            color: "#c084fc",
                            background: "none",
                            border: "none",
                            cursor:
                              downloading === item.id
                                ? "not-allowed"
                                : "pointer",
                            fontWeight: 500,
                            opacity: downloading === item.id ? 0.5 : 1,
                          }}
                        >
                          {downloading === item.id
                            ? "Downloading..."
                            : "⬇ Download"}
                        </button>
                      )}
                    </div>
                  ))
                ) : (
                  <p style={{ fontSize: "14px", color: "rgba(255,255,255,0.45)" }}>
                    No items in this order
                  </p>
                )}
              </div>

              {/* Shipping Address */}
              <div
                style={{
                  backgroundColor: "#150a26",
                  border: "1px solid rgba(168,85,247,0.2)",
                  borderRadius: "12px",
                  padding: "20px",
                }}
              >
                <p
                  style={{
                    fontSize: "12px",
                    color: "rgba(255,255,255,0.45)",
                    marginBottom: "8px",
                    textTransform: "uppercase",
                    fontWeight: 600,
                  }}
                >
                  Shipping Address
                </p>
                <p style={{ fontSize: "14px", lineHeight: 1.7, color: "rgba(255,255,255,0.75)" }}>
                  {order.shipping_address || "No address provided"}
                </p>
              </div>
            </div>

            {/* Summary */}
            <div
              style={{
                backgroundColor: "#150a26",
                border: "1px solid rgba(168,85,247,0.2)",
                borderRadius: "12px",
                padding: "20px",
                height: "fit-content",
              }}
            >
              <h3
                style={{
                  fontSize: "14px",
                  fontWeight: 700,
                  marginBottom: "16px",
                  color: "#ffffff"
                }}
              >
                Order Summary
              </h3>
              <div
                style={{
                  marginBottom: "16px",
                  paddingBottom: "16px",
                  borderBottom: "1px solid rgba(168,85,247,0.15)",
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "13px",
                    marginBottom: "8px",
                    color: "rgba(255,255,255,0.7)"
                  }}
                >
                  <span>Subtotal</span>
                  <span>₹{order.total_price}</span>
                </div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "13px",
                    color: "rgba(255,255,255,0.7)"
                  }}
                >
                  <span>Shipping</span>
                  <span>Free</span>
                </div>
              </div>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  fontSize: "16px",
                  fontWeight: 700,
                  color: "#ffffff"
                }}
              >
                <span>Total</span>
                <span style={{ color: "#c084fc" }}>₹{order.total_price}</span>
              </div>

              <Link
                href="/products"
                style={{
                  display: "block",
                  marginTop: "24px",
                  padding: "12px",
                  backgroundColor: "#9333ea",
                  color: "#ffffff",
                  borderRadius: "10px",
                  textAlign: "center",
                  textDecoration: "none",
                  fontSize: "13px",
                  fontWeight: 600,
                  boxShadow: "0 0 20px rgba(147,51,234,0.4)"
                }}
              >
                Continue shopping
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}