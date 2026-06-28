"use client";
import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import ProductCard from "@/components/ProductCard";
import api from "@/lib/api";
import { Product, KnowledgeField } from "@/lib/types";

function ProductsPageInner() {
  const searchParams = useSearchParams();
  const [products, setProducts] = useState<Product[]>([]);
  const [fields, setFields] = useState<KnowledgeField[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState(searchParams.get("search") || "");
  const [selectedField, setSelectedField] = useState(searchParams.get("field") || "");
  const [productType, setProductType] = useState(searchParams.get("type") || "");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    fetchFields();
  }, []);

  useEffect(() => {
    fetchProducts();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [search, selectedField, productType, currentPage]);

  const fetchFields = async () => {
    try {
      const res = await api.get("/api/products/fields/");
      setFields(res.data.results || res.data || []);
    } catch (err) {
      console.error("Fields error:", err);
    }
  };

  const fetchProducts = async () => {
    try {
      setLoading(true);
      let url = `/api/products/?page=${currentPage}`;

      if (search.trim()) url += `&search=${encodeURIComponent(search)}`;
      if (selectedField) url += `&field=${selectedField}`;
      if (productType) url += `&type=${productType}`;

      const res = await api.get(url);

      const data = res.data;
      setProducts(data.results || data || []);

      if (data.count) {
        setTotalCount(data.count);
        setTotalPages(Math.ceil(data.count / 12));
      }

      setError("");
    } catch (err) {
      console.error("Products error:", err);
      setError("Failed to load products");
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
  };

  const nextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>
      {/* paddingTop 70px clears the fixed navbar - no more overlap */}
      <div style={{ padding: "70px 40px 60px", position: "relative", zIndex: 1, boxSizing: "border-box" }}>
        <div style={{ maxWidth: "1400px", margin: "0 auto", paddingTop: "30px" }}>
          {/* Header */}
          <div style={{ marginBottom: "40px" }}>
            <h1
              style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "48px",
                fontWeight: 300,
                marginBottom: "12px",
                textShadow: "0 0 24px rgba(168,85,247,0.3)",
              }}
            >
              Browse Books
            </h1>
            <p style={{ fontSize: "16px", color: "rgba(255,255,255,0.55)" }}>
              Explore {totalCount} premium digital resources across {fields.length} knowledge fields
            </p>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleSearch} style={{ marginBottom: "40px" }}>
            <input
              type="text"
              placeholder="Search books..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{
                width: "100%",
                padding: "16px 20px",
                borderRadius: "10px",
                border: "1px solid rgba(168,85,247,0.25)",
                backgroundColor: "#150a26",
                color: "#ffffff",
                fontSize: "14px",
                boxSizing: "border-box",
                marginBottom: "16px",
                outline: "none",
              }}
              onFocus={(e) => {
                e.currentTarget.style.borderColor = "#c084fc";
              }}
              onBlur={(e) => {
                e.currentTarget.style.borderColor = "rgba(168,85,247,0.25)";
              }}
            />
            <button
              type="submit"
              style={{
                padding: "12px 28px",
                backgroundColor: "#9333ea",
                color: "#ffffff",
                border: "none",
                borderRadius: "10px",
                cursor: "pointer",
                fontSize: "14px",
                fontWeight: 600,
                boxShadow: "0 0 20px rgba(147,51,234,0.4)",
                transition: "all 0.2s",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#a855f7";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#9333ea";
              }}
            >
              Search
            </button>
          </form>

          {/* Filters */}
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: "20px",
              marginBottom: "40px",
            }}
          >
            <div>
              <label
                style={{
                  fontSize: "12px",
                  fontWeight: 600,
                  display: "block",
                  marginBottom: "8px",
                  color: "rgba(255,255,255,0.5)",
                }}
              >
                Knowledge Field
              </label>
              <select
                value={selectedField}
                onChange={(e) => {
                  setSelectedField(e.target.value);
                  setCurrentPage(1);
                }}
                style={{
                  width: "100%",
                  padding: "12px 16px",
                  borderRadius: "8px",
                  border: "1px solid rgba(168,85,247,0.25)",
                  backgroundColor: "#150a26",
                  color: "#ffffff",
                  fontSize: "14px",
                  boxSizing: "border-box",
                  cursor: "pointer",
                }}
              >
                <option value="">All Fields</option>
                {fields.map((field) => (
                  <option key={field.id} value={field.slug}>
                    {field.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label
                style={{
                  fontSize: "12px",
                  fontWeight: 600,
                  display: "block",
                  marginBottom: "8px",
                  color: "rgba(255,255,255,0.5)",
                }}
              >
                Product Type
              </label>
              <select
                value={productType}
                onChange={(e) => {
                  setProductType(e.target.value);
                  setCurrentPage(1);
                }}
                style={{
                  width: "100%",
                  padding: "12px 16px",
                  borderRadius: "8px",
                  border: "1px solid rgba(168,85,247,0.25)",
                  backgroundColor: "#150a26",
                  color: "#ffffff",
                  fontSize: "14px",
                  boxSizing: "border-box",
                  cursor: "pointer",
                }}
              >
                <option value="">All Types</option>
                <option value="digital">Digital</option>
                <option value="physical">Physical</option>
                <option value="experience">Experience</option>
              </select>
            </div>
          </div>

          {error && (
            <div
              style={{
                backgroundColor: "rgba(220,38,38,0.15)",
                color: "#fca5a5",
                border: "1px solid rgba(220,38,38,0.3)",
                padding: "16px",
                borderRadius: "8px",
                marginBottom: "24px",
              }}
            >
              {error}
            </div>
          )}

          {/* Products Grid */}
          {loading ? (
            <div
              style={{
                textAlign: "center",
                padding: "60px 20px",
                color: "rgba(255,255,255,0.5)",
              }}
            >
              Loading books...
            </div>
          ) : products.length === 0 ? (
            <div
              style={{
                textAlign: "center",
                padding: "60px 20px",
                color: "rgba(255,255,255,0.5)",
              }}
            >
              No books found. Try adjusting your filters.
            </div>
          ) : (
            <>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
                  gap: "24px",
                  marginBottom: "40px",
                }}
              >
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>

              {/* Pagination Controls */}
              <div
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  gap: "16px",
                  marginTop: "40px",
                  paddingTop: "40px",
                  borderTop: "1px solid rgba(168,85,247,0.15)",
                }}
              >
                <button
                  onClick={prevPage}
                  disabled={currentPage === 1}
                  style={{
                    padding: "12px 24px",
                    backgroundColor: currentPage === 1 ? "rgba(255,255,255,0.05)" : "#9333ea",
                    color: currentPage === 1 ? "rgba(255,255,255,0.3)" : "#ffffff",
                    border: currentPage === 1 ? "1px solid rgba(255,255,255,0.1)" : "none",
                    borderRadius: "8px",
                    cursor: currentPage === 1 ? "not-allowed" : "pointer",
                    fontSize: "14px",
                    fontWeight: 600,
                    boxShadow: currentPage === 1 ? "none" : "0 0 16px rgba(147,51,234,0.4)",
                  }}
                >
                  Previous
                </button>

                <div
                  style={{
                    display: "flex",
                    gap: "8px",
                    alignItems: "center",
                  }}
                >
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                    const pageNum = Math.max(1, currentPage - 2) + i;
                    if (pageNum > totalPages) return null;

                    return (
                      <button
                        key={pageNum}
                        onClick={() => setCurrentPage(pageNum)}
                        style={{
                          width: "36px",
                          height: "36px",
                          borderRadius: "6px",
                          border: pageNum === currentPage ? "1px solid #c084fc" : "1px solid rgba(168,85,247,0.25)",
                          backgroundColor: pageNum === currentPage ? "#9333ea" : "#150a26",
                          color: "#ffffff",
                          cursor: "pointer",
                          fontSize: "13px",
                          fontWeight: 600,
                          boxShadow: pageNum === currentPage ? "0 0 16px rgba(147,51,234,0.4)" : "none",
                        }}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                </div>

                <button
                  onClick={nextPage}
                  disabled={currentPage >= totalPages}
                  style={{
                    padding: "12px 24px",
                    backgroundColor: currentPage >= totalPages ? "rgba(255,255,255,0.05)" : "#9333ea",
                    color: currentPage >= totalPages ? "rgba(255,255,255,0.3)" : "#ffffff",
                    border: currentPage >= totalPages ? "1px solid rgba(255,255,255,0.1)" : "none",
                    borderRadius: "8px",
                    cursor: currentPage >= totalPages ? "not-allowed" : "pointer",
                    fontSize: "14px",
                    fontWeight: 600,
                    boxShadow: currentPage >= totalPages ? "none" : "0 0 16px rgba(147,51,234,0.4)",
                  }}
                >
                  Next
                </button>
              </div>

              <div
                style={{
                  textAlign: "center",
                  marginTop: "20px",
                  fontSize: "13px",
                  color: "rgba(255,255,255,0.4)",
                }}
              >
                Page {currentPage} of {totalPages} ({totalCount} total books)
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ProductsPage() {
  return (
    <Suspense
      fallback={
        <div
          style={{
            minHeight: "100vh",
            backgroundColor: "#0a0612",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <p style={{ color: "#ffffff" }}>Loading...</p>
        </div>
      }
    >
      <ProductsPageInner />
    </Suspense>
  );
}
