"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import SmartImage from "@/components/SmartImage";
import api from "@/lib/api";
import { Product } from "@/lib/types";

interface Movie {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
  vote_average: number;
  watch_url: string;
}

interface Ebook {
  id: number;
  title: string;
  author: string;
  description: string;
  url: string;
  cover: string;
}

export default function ProductDetailPage() {
  const params = useParams();
  const id = params.id as string;

  const [product, setProduct] = useState<Product | null>(null);
  const [relatedProducts, setRelatedProducts] = useState<Product[]>([]);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [ebooks, setEbooks] = useState<Ebook[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [addingToCart, setAddingToCart] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    fetchProductDetails();
  }, [id]);

  const fetchProductDetails = async () => {
    try {
      setLoading(true);
      setError("");

      const productRes = await api.get(`/api/products/${id}/`);
      const productData = productRes.data.data || productRes.data;
      setProduct(productData);

      const fieldSlug = productData.knowledge_fields?.[0]?.slug;

      if (fieldSlug) {
        const relatedRes = await api.get(`/api/products/?field=${fieldSlug}&limit=6`);
        const allProducts = relatedRes.data.results || relatedRes.data || [];
        const related = allProducts.filter((p: Product) => p.id !== parseInt(id));
        setRelatedProducts(related.slice(0, 5));

        try {
          const moviesRes = await api.get(`/api/tmdb/movies/?field=${fieldSlug}`);
          setMovies(moviesRes.data.results || moviesRes.data || []);
        } catch (err) {
          console.warn("Movies not available");
        }

        try {
          const ebooksRes = await api.get(`/api/ebooks/free/?field=${fieldSlug}`);
          setEbooks(ebooksRes.data.results || ebooksRes.data || []);
        } catch (err) {
          console.warn("Ebooks not available");
        }
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Failed to load product");
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async () => {
    if (!product) return;

    setAddingToCart(true);
    try {
      await api.post("/api/cart/add/", {
        product_id: product.id,
        quantity: quantity,
      });
      setSuccessMessage(`Added ${quantity} to cart!`);
      setTimeout(() => setSuccessMessage(""), 3000);
      setQuantity(1);
    } catch (err) {
      setError("Failed to add to cart");
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", position: "relative" }}>
        <div style={{ position: "relative", zIndex: 1 }}>
          <div style={{ textAlign: "center", padding: "100px 40px" }}>
            <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "16px" }}>Loading product...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", position: "relative" }}>
        <div style={{ position: "relative", zIndex: 1 }}>
          <div style={{ textAlign: "center", padding: "100px 40px" }}>
            <p style={{ color: "#fca5a5", fontSize: "16px", marginBottom: "24px" }}>Product not found</p>
            <Link
              href="/products"
              style={{
                backgroundColor: "#9333ea",
                color: "#ffffff",
                padding: "12px 28px",
                borderRadius: "9999px",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 600,
                display: "inline-block",
                boxShadow: "0 0 20px rgba(147,51,234,0.4)"
              }}
            >
              Back to products
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const fieldName = product.knowledge_fields?.[0]?.name || "Knowledge";
  // Book covers intentionally disabled - always show the icon/gradient fallback
  const coverImage = null;

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>

      <div style={{ padding: "70px 40px 60px", position: "relative", zIndex: 1, boxSizing: "border-box" }}>
        <div style={{ maxWidth: "1400px", margin: "0 auto", paddingTop: "30px" }}>
          <Link
            href="/products"
            style={{ color: "#c084fc", textDecoration: "none", fontSize: "13px", fontWeight: 500 }}
          >
            ← Back to products
          </Link>

          {successMessage && (
            <div style={{
              backgroundColor: "rgba(34,197,94,0.15)",
              color: "#86efac",
              border: "1px solid rgba(34,197,94,0.3)",
              padding: "12px 16px",
              borderRadius: "8px",
              marginTop: "16px",
              fontSize: "14px",
              fontWeight: 500
            }}>
              ✓ {successMessage}
            </div>
          )}

          {error && (
            <div style={{
              backgroundColor: "rgba(220,38,38,0.15)",
              color: "#fca5a5",
              border: "1px solid rgba(220,38,38,0.3)",
              padding: "12px 16px",
              borderRadius: "8px",
              marginTop: "16px",
              fontSize: "14px"
            }}>
              {error}
            </div>
          )}

          {/* Product Details Section */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "60px", marginTop: "40px", marginBottom: "80px" }}>
            <div>
              {/* Cover image - SmartImage falls back to a styled gradient card if missing/broken */}
              <div style={{
                width: "100%",
                aspectRatio: "1",
                borderRadius: "16px",
                marginBottom: "32px",
                overflow: "hidden",
                border: "1px solid rgba(168,85,247,0.2)",
                boxShadow: "0 16px 40px rgba(147,51,234,0.2)"
              }}>
                <SmartImage
                  src={coverImage}
                  alt={product.name}
                  icon={product.knowledge_fields?.[0]?.icon || "📚"}
                  fontSize="80px"
                />
              </div>
              <div style={{ display: "inline-flex", gap: "8px", flexWrap: "wrap" }}>
                {product.knowledge_fields?.map((field) => (
                  <Link
                    key={field.id}
                    href={`/products?field=${field.slug}`}
                    style={{
                      backgroundColor: "rgba(147,51,234,0.15)",
                      color: "#ffffff",
                      padding: "8px 16px",
                      borderRadius: "9999px",
                      textDecoration: "none",
                      fontSize: "12px",
                      fontWeight: 600,
                      border: "1px solid rgba(168,85,247,0.3)"
                    }}
                  >
                    {field.name}
                  </Link>
                ))}
              </div>
            </div>

            <div>
              {product.name.includes("⭐") && (
                <div style={{
                  display: "inline-block",
                  backgroundColor: "rgba(245,158,11,0.15)",
                  color: "#fbbf24",
                  border: "1px solid rgba(245,158,11,0.3)",
                  padding: "8px 16px",
                  borderRadius: "9999px",
                  fontSize: "12px",
                  fontWeight: 600,
                  marginBottom: "16px"
                }}>
                  ⭐ Featured Premium
                </div>
              )}

              <h1 style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "44px",
                fontWeight: 300,
                marginBottom: "16px",
                lineHeight: 1.2,
                textShadow: "0 0 24px rgba(168,85,247,0.3)"
              }}>
                {product.name.replace("⭐ ", "")}
              </h1>

              <p style={{ fontSize: "32px", fontWeight: 700, marginBottom: "24px", color: "#c084fc" }}>₹{product.price}</p>

              <p style={{
                fontSize: "15px",
                lineHeight: 1.8,
                color: "rgba(255,255,255,0.7)",
                marginBottom: "32px",
                whiteSpace: "pre-wrap"
              }}>
                {product.description}
              </p>

              <div style={{
                display: "inline-block",
                backgroundColor: "rgba(99,102,241,0.15)",
                color: "#a5b4fc",
                border: "1px solid rgba(99,102,241,0.3)",
                padding: "8px 16px",
                borderRadius: "8px",
                fontSize: "12px",
                fontWeight: 600,
                marginBottom: "32px",
                textTransform: "capitalize"
              }}>
                {product.type} Product
              </div>

              <div style={{ display: "flex", gap: "16px", alignItems: "center", marginBottom: "40px" }}>
                <div style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "12px",
                  border: "1px solid rgba(168,85,247,0.25)",
                  borderRadius: "10px",
                  padding: "12px 16px",
                  backgroundColor: "#150a26"
                }}>
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    style={{
                      width: "32px",
                      height: "32px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      fontSize: "16px",
                      fontWeight: 600,
                      color: "#ffffff"
                    }}
                  >
                    −
                  </button>
                  <span style={{ fontSize: "16px", fontWeight: 700, minWidth: "30px", textAlign: "center", color: "#ffffff" }}>
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    style={{
                      width: "32px",
                      height: "32px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                      fontSize: "16px",
                      fontWeight: 600,
                      color: "#ffffff"
                    }}
                  >
                    +
                  </button>
                </div>

                <button
                  onClick={addToCart}
                  disabled={addingToCart}
                  style={{
                    flex: 1,
                    padding: "16px 24px",
                    backgroundColor: "#9333ea",
                    color: "#ffffff",
                    border: "none",
                    borderRadius: "10px",
                    fontSize: "16px",
                    fontWeight: 600,
                    cursor: addingToCart ? "not-allowed" : "pointer",
                    opacity: addingToCart ? 0.7 : 1,
                    boxShadow: addingToCart ? "none" : "0 0 24px rgba(147,51,234,0.45)"
                  }}
                >
                  {addingToCart ? "Adding..." : "Add to Cart"}
                </button>
              </div>

              <div style={{ display: "flex", gap: "20px", fontSize: "14px", fontWeight: 500 }}>
                <Link href="/cart" style={{ color: "#c084fc", textDecoration: "none" }}>View Cart</Link>
                <span style={{ color: "rgba(168,85,247,0.3)" }}>•</span>
                <Link href="/products" style={{ color: "#c084fc", textDecoration: "none" }}>Continue Shopping</Link>
              </div>
            </div>
          </div>

          {/* Related Products - fixed-height cards so the grid is always even */}
          {relatedProducts.length > 0 && (
            <div style={{ marginBottom: "80px" }}>
              <div style={{ marginBottom: "32px" }}>
                <h2 style={{
                  fontFamily: "'Fraunces', serif",
                  fontSize: "32px",
                  fontWeight: 300,
                  marginBottom: "8px",
                  textShadow: "0 0 20px rgba(168,85,247,0.3)"
                }}>
                  More in {fieldName}
                </h2>
                <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "14px" }}>Explore {relatedProducts.length} related books</p>
              </div>

              <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
                gap: "20px"
              }}>
                {relatedProducts.map(relProduct => {
                  const relCover = null; // Book covers intentionally disabled
                  return (
                    <Link
                      key={relProduct.id}
                      href={`/products/${relProduct.id}`}
                      style={{ textDecoration: "none", color: "inherit" }}
                    >
                      <div style={{
                        border: "1px solid rgba(168,85,247,0.2)",
                        borderRadius: "12px",
                        backgroundColor: "#150a26",
                        cursor: "pointer",
                        transition: "all 0.3s",
                        height: "280px",
                        display: "flex",
                        flexDirection: "column",
                        overflow: "hidden"
                      }}
                        onMouseEnter={e => {
                          const el = e.currentTarget as HTMLDivElement;
                          el.style.boxShadow = "0 8px 24px rgba(147,51,234,0.3)";
                          el.style.transform = "translateY(-4px)";
                          el.style.borderColor = "rgba(168,85,247,0.5)";
                        }}
                        onMouseLeave={e => {
                          const el = e.currentTarget as HTMLDivElement;
                          el.style.boxShadow = "none";
                          el.style.transform = "translateY(0)";
                          el.style.borderColor = "rgba(168,85,247,0.2)";
                        }}
                      >
                        <div style={{ height: "140px", flexShrink: 0 }}>
                          <SmartImage
                            src={relCover}
                            alt={relProduct.name}
                            icon={relProduct.knowledge_fields?.[0]?.icon || "📚"}
                            fontSize="32px"
                          />
                        </div>
                        <div style={{ padding: "16px", display: "flex", flexDirection: "column", flex: 1 }}>
                          <h3 style={{
                            fontSize: "13px",
                            fontWeight: 600,
                            lineHeight: 1.4,
                            marginBottom: "8px",
                            flex: 1,
                            color: "#ffffff",
                            overflow: "hidden",
                            display: "-webkit-box",
                            WebkitLineClamp: 2,
                            WebkitBoxOrient: "vertical"
                          }}>
                            {relProduct.name.replace("⭐ ", "")}
                          </h3>
                          <p style={{ fontSize: "14px", fontWeight: 700, color: "#c084fc" }}>₹{relProduct.price}</p>
                        </div>
                      </div>
                    </Link>
                  );
                })}
              </div>
            </div>
          )}

          {/* Free eBooks Section */}
          {ebooks && ebooks.length > 0 && (
            <div style={{
              marginBottom: "80px",
              backgroundColor: "rgba(21,10,38,0.6)",
              border: "1px solid rgba(168,85,247,0.15)",
              borderRadius: "16px",
              padding: "40px"
            }}>
              <div style={{ marginBottom: "32px" }}>
                <h2 style={{
                  fontFamily: "'Fraunces', serif",
                  fontSize: "32px",
                  fontWeight: 300,
                  marginBottom: "8px",
                  textShadow: "0 0 20px rgba(168,85,247,0.3)"
                }}>
                  📚 Free eBooks to Read
                </h2>
                <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "14px" }}>
                  Complement your learning with {ebooks.length} curated free books from Project Gutenberg
                </p>
              </div>

              <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
                gap: "20px"
              }}>
                {ebooks.map((ebook) => (
                  <a
                    key={ebook.id}
                    href={ebook.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      textDecoration: "none",
                      color: "inherit",
                      display: "block"
                    }}
                  >
                    <div style={{
                      border: "1px solid rgba(168,85,247,0.2)",
                      borderRadius: "12px",
                      padding: "20px",
                      backgroundColor: "#150a26",
                      cursor: "pointer",
                      transition: "all 0.3s",
                      height: "260px",
                      display: "flex",
                      flexDirection: "column",
                      boxSizing: "border-box"
                    }}
                      onMouseEnter={e => {
                        const el = e.currentTarget as HTMLDivElement;
                        el.style.boxShadow = "0 8px 24px rgba(147,51,234,0.35)";
                        el.style.transform = "translateY(-6px)";
                        el.style.borderColor = "#c084fc";
                      }}
                      onMouseLeave={e => {
                        const el = e.currentTarget as HTMLDivElement;
                        el.style.boxShadow = "none";
                        el.style.transform = "translateY(0)";
                        el.style.borderColor = "rgba(168,85,247,0.2)";
                      }}
                    >
                      <div style={{ fontSize: "40px", marginBottom: "12px", textAlign: "center" }}>
                        {ebook.cover || "📖"}
                      </div>

                      <h3 style={{
                        fontSize: "14px",
                        fontWeight: 700,
                        lineHeight: 1.4,
                        marginBottom: "8px",
                        color: "#ffffff",
                        overflow: "hidden",
                        display: "-webkit-box",
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: "vertical"
                      }}>
                        {ebook.title}
                      </h3>

                      <p style={{
                        fontSize: "12px",
                        color: "rgba(255,255,255,0.5)",
                        marginBottom: "8px",
                        fontStyle: "italic"
                      }}>
                        {ebook.author}
                      </p>

                      <p style={{
                        fontSize: "12px",
                        color: "rgba(255,255,255,0.5)",
                        marginBottom: "12px",
                        flex: 1,
                        overflow: "hidden",
                        display: "-webkit-box",
                        WebkitLineClamp: 3,
                        WebkitBoxOrient: "vertical"
                      }}>
                        {ebook.description}
                      </p>

                      <div style={{
                        display: "flex",
                        alignItems: "center",
                        gap: "8px",
                        color: "#c084fc",
                        fontWeight: 600,
                        fontSize: "13px",
                        marginTop: "auto",
                        paddingTop: "12px",
                        borderTop: "1px solid rgba(168,85,247,0.15)"
                      }}>
                        📖 Read on Gutenberg
                        <span style={{ marginLeft: "auto" }}>→</span>
                      </div>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          )}

          {/* Movies Section */}
          {movies && movies.length > 0 && (
            <div>
              <div style={{ marginBottom: "32px" }}>
                <h2 style={{
                  fontFamily: "'Fraunces', serif",
                  fontSize: "32px",
                  fontWeight: 300,
                  marginBottom: "8px",
                  textShadow: "0 0 20px rgba(168,85,247,0.3)"
                }}>
                  🎬 Recommended Movies
                </h2>
                <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "14px" }}>Premium video content to complement your learning</p>
              </div>

              <div style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
                gap: "20px"
              }}>
                {movies.slice(0, 8).map((movie, idx) => (
                  <a
                    key={idx}
                    href={movie.watch_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ textDecoration: "none", color: "inherit", display: "block" }}
                  >
                    <div
                      style={{
                        borderRadius: "12px",
                        overflow: "hidden",
                        border: "1px solid rgba(168,85,247,0.2)",
                        backgroundColor: "#150a26",
                        transition: "all 0.3s",
                        cursor: "pointer"
                      }}
                      onMouseEnter={e => {
                        const el = e.currentTarget as HTMLDivElement;
                        el.style.boxShadow = "0 8px 24px rgba(147,51,234,0.35)";
                        el.style.transform = "translateY(-6px)";
                        el.style.borderColor = "#c084fc";
                      }}
                      onMouseLeave={e => {
                        const el = e.currentTarget as HTMLDivElement;
                        el.style.boxShadow = "none";
                        el.style.transform = "translateY(0)";
                        el.style.borderColor = "rgba(168,85,247,0.2)";
                      }}
                    >
                      <div style={{
                        width: "100%",
                        aspectRatio: "9/13",
                        position: "relative"
                      }}>
                        <SmartImage
                          src={movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : null}
                          alt={movie.title}
                          fontSize="32px"
                        />
                        <div style={{
                          position: "absolute",
                          inset: 0,
                          backgroundColor: "rgba(10,6,18,0.25)",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: "40px"
                        }}>
                          ▶️
                        </div>
                      </div>

                      <div style={{ padding: "12px" }}>
                        <h3 style={{
                          fontSize: "12px",
                          fontWeight: 600,
                          lineHeight: 1.3,
                          marginBottom: "4px",
                          minHeight: "32px",
                          color: "#ffffff",
                          overflow: "hidden",
                          display: "-webkit-box",
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: "vertical"
                        }}>
                          {movie.title}
                        </h3>
                        <p style={{ fontSize: "11px", color: "rgba(255,255,255,0.4)", marginBottom: "4px" }}>
                          {movie.release_date ? new Date(movie.release_date).getFullYear() : "N/A"}
                        </p>
                        <div style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "4px",
                          fontSize: "12px",
                          fontWeight: 600,
                          color: "#c084fc"
                        }}>
                          {movie.vote_average ? movie.vote_average.toFixed(1) : "N/A"}/10
                        </div>
                      </div>
                    </div>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}