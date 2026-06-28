"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { Cart } from "@/lib/types";

export default function CheckoutPage() {
  const router = useRouter();
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [address, setAddress] = useState("");
  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const res = await api.get("/api/cart/");
      setCart(res.data.data || res.data);
      setError("");
    } catch (err: any) {
      console.error("Cart fetch error:", err);
      setError("Failed to load cart");
    } finally {
      setLoading(false);
    }
  };

  const placeOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!address.trim()) {
      setError("Please enter a shipping address");
      return;
    }

    setPlacing(true);
    setError("");

    try {
      const res = await api.post("/api/orders/checkout/", {
        shipping_address: address,
      });

      const orderId = res.data.data?.id || res.data.id;
      localStorage.removeItem("cart");
      router.push(`/orders/${orderId}`);
    } catch (err: any) {
      console.error("Checkout error:", err);
      setError("Failed to place order. Please try again.");
    } finally {
      setPlacing(false);
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", position: "relative" }}>
        <div style={{ textAlign: "center", position: "relative", zIndex: 1 }}>
          <p style={{ color: "rgba(255,255,255,0.5)", marginTop: "60px" }}>Loading checkout...</p>
        </div>
      </div>
    );
  }

  if (!cart || !cart.items || cart.items.length === 0) {
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
            style={{ fontSize: "16px", color: "rgba(255,255,255,0.5)", marginBottom: "24px", marginTop: "40px" }}
          >
            Your cart is empty
          </p>
          <button
            onClick={() => router.push("/products")}
            style={{
              backgroundColor: "#9333ea",
              color: "#ffffff",
              padding: "12px 28px",
              borderRadius: "9999px",
              border: "none",
              cursor: "pointer",
              fontSize: "14px",
              fontWeight: 500,
              boxShadow: "0 0 20px rgba(147,51,234,0.4)"
            }}
          >
            Continue shopping
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>

      <div style={{ padding: "70px 40px 60px", position: "relative", zIndex: 1, boxSizing: "border-box" }}>
        <div style={{ maxWidth: "800px", margin: "0 auto", paddingTop: "30px" }}>
          <h1
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "40px",
              fontWeight: 300,
              marginBottom: "32px",
              textShadow: "0 0 24px rgba(168,85,247,0.3)"
            }}
          >
            Checkout
          </h1>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 320px",
              gap: "40px",
            }}
          >
            {/* Checkout Form */}
            <form onSubmit={placeOrder}>
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

              {/* Shipping Address */}
              <div style={{ marginBottom: "32px" }}>
                <label
                  style={{
                    fontSize: "13px",
                    fontWeight: 600,
                    display: "block",
                    marginBottom: "8px",
                    textTransform: "uppercase",
                    color: "rgba(255,255,255,0.5)",
                  }}
                >
                  Shipping Address
                </label>
                <textarea
                  value={address}
                  onChange={(e) => setAddress(e.target.value)}
                  placeholder="Enter your full shipping address"
                  required
                  style={{
                    width: "100%",
                    height: "120px",
                    padding: "14px 16px",
                    borderRadius: "10px",
                    border: "1px solid rgba(168,85,247,0.25)",
                    backgroundColor: "#150a26",
                    color: "#ffffff",
                    fontSize: "14px",
                    outline: "none",
                    fontFamily: "inherit",
                    boxSizing: "border-box",
                    resize: "vertical",
                  }}
                  onFocus={(e) => { e.currentTarget.style.borderColor = "#c084fc"; }}
                  onBlur={(e) => { e.currentTarget.style.borderColor = "rgba(168,85,247,0.25)"; }}
                />
              </div>

              {/* Order Items Review */}
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
                    fontSize: "14px",
                    fontWeight: 700,
                    marginBottom: "16px",
                    color: "#ffffff"
                  }}
                >
                  Order Items
                </h3>
                {cart.items &&
                  cart.items.length > 0 &&
                  cart.items.map((item) => (
                    <div
                      key={item.id}
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        paddingBottom: "12px",
                        marginBottom: "12px",
                        borderBottom: "1px solid rgba(168,85,247,0.15)",
                      }}
                    >
                      <div>
                        <p style={{ fontSize: "14px", fontWeight: 600, color: "#ffffff" }}>
                          {item.product?.name || "Product"}
                        </p>
                        <p style={{ fontSize: "12px", color: "rgba(255,255,255,0.45)" }}>
                          x{item.quantity}
                        </p>
                      </div>
                      <p style={{ fontSize: "14px", fontWeight: 700, color: "#c084fc" }}>
                        ₹{item.item_total ? item.item_total.toFixed(2) : "0.00"}
                      </p>
                    </div>
                  ))}
              </div>

              {/* Terms */}
              <div style={{ marginBottom: "32px" }}>
                <label
                  style={{
                    display: "flex",
                    gap: "12px",
                    alignItems: "flex-start",
                    fontSize: "13px",
                    color: "rgba(255,255,255,0.5)",
                  }}
                >
                  <input
                    type="checkbox"
                    required
                    style={{ marginTop: "4px", cursor: "pointer" }}
                  />
                  I agree to the terms and conditions
                </label>
              </div>

              {/* Place Order Button */}
              <button
                type="submit"
                disabled={placing}
                style={{
                  width: "100%",
                  padding: "16px",
                  backgroundColor: "#9333ea",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: "10px",
                  fontSize: "16px",
                  fontWeight: 600,
                  cursor: placing ? "not-allowed" : "pointer",
                  opacity: placing ? 0.7 : 1,
                  boxShadow: placing ? "none" : "0 0 24px rgba(147,51,234,0.45)"
                }}
              >
                {placing ? "Placing order..." : "Place order"}
              </button>
            </form>

            {/* Summary Sidebar */}
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
                  <span>
                    ₹{cart && cart.total_price ? cart.total_price : "0.00"}
                  </span>
                </div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "13px",
                    marginBottom: "8px",
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
                <span style={{ color: "#c084fc" }}>
                  ₹{cart && cart.total_price ? cart.total_price : "0.00"}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}