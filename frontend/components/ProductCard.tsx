"use client";
import Link from "next/link";
import SmartImage from "@/components/SmartImage";
import { Product } from "@/lib/types";

export default function ProductCard({ product }: { product: Product }) {
  const typeColors: Record<string, string> = {
    physical: "#34d399",
    digital: "#c084fc",
    experience: "#fb923c",
  };
  const accent = typeColors[product.type] || "#c084fc";
  // Book covers intentionally disabled - always show the icon/gradient fallback, never a real image
  const coverImage = null;

  return (
    <Link href={`/products/${product.id}`} style={{ textDecoration: "none", color: "#ffffff" }}>
      <div
        style={{
          border: "1px solid rgba(168,85,247,0.18)",
          borderRadius: "16px",
          overflow: "hidden",
          transition: "all 0.3s",
          backgroundColor: "#150a26",
          cursor: "pointer",
        }}
        onMouseEnter={(e) => {
          const el = e.currentTarget as HTMLDivElement;
          el.style.boxShadow = "0 16px 40px rgba(147,51,234,0.3)";
          el.style.transform = "translateY(-4px)";
          el.style.borderColor = "rgba(168,85,247,0.5)";
        }}
        onMouseLeave={(e) => {
          const el = e.currentTarget as HTMLDivElement;
          el.style.boxShadow = "none";
          el.style.transform = "translateY(0)";
          el.style.borderColor = "rgba(168,85,247,0.18)";
        }}
      >
        {/* Cover image - SmartImage auto-falls-back to a styled gradient card if missing/broken */}
        <div style={{ height: "200px", position: "relative" }}>
          <SmartImage
            src={coverImage}
            alt={product.name}
            icon={product.knowledge_fields?.[0]?.icon || "📦"}
            fontSize="40px"
          />
        </div>

        <div style={{ padding: "20px" }}>
          <span style={{
            fontSize: "11px",
            fontWeight: 600,
            color: accent,
            backgroundColor: `${accent}22`,
            padding: "4px 10px",
            borderRadius: "9999px",
            textTransform: "uppercase",
            letterSpacing: "0.05em",
            border: `1px solid ${accent}40`
          }}>
            {product.type}
          </span>

          <h3 style={{
            fontSize: "15px",
            fontWeight: 600,
            margin: "12px 0 6px",
            lineHeight: 1.4,
            color: "#ffffff"
          }}>
            {product.name}
          </h3>

          <p style={{
            fontSize: "13px",
            color: "rgba(255,255,255,0.5)",
            marginBottom: "16px",
            lineHeight: 1.5,
            overflow: "hidden",
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical"
          }}>
            {product.description || "No description available."}
          </p>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "18px", fontWeight: 700, color: "#c084fc" }}>
              ₹{product.price}
            </span>
            <span style={{ fontSize: "12px", color: "rgba(255,255,255,0.4)" }}>
              {product.vendor_name}
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
}