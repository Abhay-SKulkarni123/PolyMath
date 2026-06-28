"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import SmartImage from "@/components/SmartImage";
import api from "@/lib/api";
import { Cart } from "@/lib/types";

export default function CartPage() {
  const router = useRouter();
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
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

  const updateQuantity = async (itemId: number, newQuantity: number) => {
    if (newQuantity < 1) return;
    try {
      await api.patch(`/api/cart/${itemId}/`, { quantity: newQuantity });
      fetchCart();
    } catch (err) {
      setError("Failed to update quantity");
    }
  };

  const removeItem = async (itemId: number) => {
    try {
      await api.delete(`/api/cart/${itemId}/`);
      fetchCart();
    } catch (err) {
      setError("Failed to remove item");
    }
  };

  const clearCart = async () => {
    try {
      await api.post("/api/cart/clear/");
      fetchCart();
    } catch (err) {
      setError("Failed to clear cart");
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", position: "relative" }}>
        <div style={{ textAlign: "center", position: "relative", zIndex: 1 }}>
          <p style={{ color: "rgba(255,255,255,0.5)", marginTop: "60px" }}>Loading cart...</p>
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
            style={{ fontSize: "18px", color: "rgba(255,255,255,0.5)", marginBottom: "24px", marginTop: "40px" }}
          >
            Your cart is empty
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
            Continue shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>

      <div style={{ padding: "70px 40px 60px", position: "relative", zIndex: 1, boxSizing: "border-box" }}>
        <div style={{ maxWidth: "1200px", margin: "0 auto", paddingTop: "30px" }}>
          <h1
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "40px",
              fontWeight: 300,
              marginBottom: "32px",
              textShadow: "0 0 24px rgba(168,85,247,0.3)"
            }}
          >
            Shopping Cart
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
              gridTemplateColumns: "1fr 350px",
              gap: "40px",
            }}
          >
            {/* Items */}
            <div>
              {cart.items &&
                cart.items.length > 0 &&
                cart.items.map((item) => {
                  const productCover = null; // Book covers intentionally disabled
                  return (
                    <div
                      key={item.id}
                      style={{
                        borderBottom: "1px solid rgba(168,85,247,0.15)",
                        paddingBottom: "24px",
                        marginBottom: "24px",
                        display: "grid",
                        gridTemplateColumns: "80px 1fr auto",
                        gap: "20px",
                        alignItems: "start",
                      }}
                    >
                      {/* Product Cover */}
                      <div
                        style={{
                          width: "80px",
                          height: "80px",
                          borderRadius: "12px",
                          overflow: "hidden",
                          border: "1px solid rgba(168,85,247,0.2)"
                        }}
                      >
                        <SmartImage
                          src={productCover}
                          alt={item.product?.name || "Product"}
                          icon={item.product?.knowledge_fields?.[0]?.icon || "📦"}
                          fontSize="28px"
                        />
                      </div>

                      {/* Product Info */}
                      <div>
                        {item.product && (
                          <>
                            <Link
                              href={`/products/${item.product.id}`}
                              style={{
                                textDecoration: "none",
                                color: "#ffffff",
                              }}
                            >
                              <h3
                                style={{
                                  fontSize: "16px",
                                  fontWeight: 600,
                                  marginBottom: "4px",
                                }}
                              >
                                {item.product.name || "Product"}
                              </h3>
                            </Link>
                            <p
                              style={{
                                fontSize: "13px",
                                color: "rgba(255,255,255,0.45)",
                                marginBottom: "12px",
                              }}
                            >
                              {item.product.vendor_name || "Vendor"}
                            </p>
                            <p style={{ fontSize: "18px", fontWeight: 700, color: "#c084fc" }}>
                              ₹{item.product.price || "0.00"}
                            </p>

                            {/* Quantity Controls */}
                            <div
                              style={{
                                display: "flex",
                                gap: "8px",
                                alignItems: "center",
                                marginTop: "12px",
                              }}
                            >
                              <button
                                onClick={() =>
                                  updateQuantity(item.id, item.quantity - 1)
                                }
                                style={{
                                  width: "32px",
                                  height: "32px",
                                  border: "1px solid rgba(168,85,247,0.3)",
                                  borderRadius: "6px",
                                  cursor: "pointer",
                                  fontSize: "14px",
                                  backgroundColor: "#150a26",
                                  color: "#ffffff",
                                }}
                              >
                                −
                              </button>
                              <span
                                style={{
                                  width: "40px",
                                  textAlign: "center",
                                  fontWeight: 600,
                                  color: "#ffffff"
                                }}
                              >
                                {item.quantity}
                              </span>
                              <button
                                onClick={() =>
                                  updateQuantity(item.id, item.quantity + 1)
                                }
                                style={{
                                  width: "32px",
                                  height: "32px",
                                  border: "1px solid rgba(168,85,247,0.3)",
                                  borderRadius: "6px",
                                  cursor: "pointer",
                                  fontSize: "14px",
                                  backgroundColor: "#150a26",
                                  color: "#ffffff",
                                }}
                              >
                                +
                              </button>
                            </div>
                          </>
                        )}
                      </div>

                      {/* Remove Button */}
                      <div style={{ textAlign: "right" }}>
                        <p
                          style={{
                            fontSize: "16px",
                            fontWeight: 700,
                            marginBottom: "12px",
                            color: "#ffffff"
                          }}
                        >
                          ₹{item.item_total ? item.item_total.toFixed(2) : "0.00"}
                        </p>
                        <button
                          onClick={() => removeItem(item.id)}
                          style={{
                            color: "#fca5a5",
                            background: "none",
                            border: "none",
                            cursor: "pointer",
                            fontSize: "13px",
                            fontWeight: 500,
                          }}
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  );
                })}
            </div>

            {/* Summary */}
            <div
              style={{
                backgroundColor: "#150a26",
                border: "1px solid rgba(168,85,247,0.2)",
                borderRadius: "16px",
                padding: "24px",
                height: "fit-content",
              }}
            >
              <h2
                style={{
                  fontSize: "16px",
                  fontWeight: 700,
                  marginBottom: "20px",
                  color: "#ffffff"
                }}
              >
                Order Summary
              </h2>

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
                    marginBottom: "8px",
                    fontSize: "14px",
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
                    marginBottom: "8px",
                    fontSize: "14px",
                    color: "rgba(255,255,255,0.7)"
                  }}
                >
                  <span>Shipping</span>
                  <span>Free</span>
                </div>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: "8px",
                    fontSize: "14px",
                    color: "rgba(255,255,255,0.7)"
                  }}
                >
                  <span>Tax</span>
                  <span>Calculated at checkout</span>
                </div>
              </div>

              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: "24px",
                  fontSize: "18px",
                  fontWeight: 700,
                  color: "#ffffff"
                }}
              >
                <span>Total</span>
                <span style={{ color: "#c084fc" }}>
                  ₹{cart && cart.total_price ? cart.total_price : "0.00"}
                </span>
              </div>

              <Link
                href="/checkout"
                style={{
                  width: "100%",
                  display: "block",
                  padding: "14px",
                  backgroundColor: "#9333ea",
                  color: "#ffffff",
                  borderRadius: "10px",
                  textAlign: "center",
                  textDecoration: "none",
                  fontSize: "14px",
                  fontWeight: 600,
                  marginBottom: "12px",
                  boxSizing: "border-box",
                  boxShadow: "0 0 20px rgba(147,51,234,0.4)"
                }}
              >
                Proceed to checkout
              </Link>

              <button
                onClick={clearCart}
                style={{
                  width: "100%",
                  padding: "12px",
                  backgroundColor: "transparent",
                  border: "1px solid rgba(168,85,247,0.25)",
                  borderRadius: "10px",
                  cursor: "pointer",
                  fontSize: "13px",
                  fontWeight: 500,
                  color: "rgba(255,255,255,0.6)",
                }}
              >
                Clear cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}