"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import SmartImage from "@/components/SmartImage";
import api from "@/lib/api";
import { Collection } from "@/lib/types";

export default function CollectionsPage() {
  const [collections, setCollections] = useState<Collection[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState("all");

  const categories = [
    { key: "all", label: "All" },
    { key: "superhero", label: "Superhero" },
    { key: "fantasy", label: "Fantasy" },
    { key: "franchise", label: "Franchise" },
    { key: "series", label: "Web Series" },
    { key: "indian_epic", label: "Indian Epics" },
    { key: "indian_cinema", label: "Indian Cinema" },
    { key: "anime", label: "Anime" },
  ];

  useEffect(() => {
    fetchCollections();
  }, []);

  const fetchCollections = async () => {
    try {
      const res = await api.get("/api/cinema/collections/");
      const all = res.data.results || res.data || [];
      setCollections(all.filter((c: Collection) => c.movie_count > 0));
    } catch (err) {
      console.error("Failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const filtered = activeCategory === "all" ? collections : collections.filter((c) => c.category === activeCategory);

  if (loading) {
    return (
      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#0a0a0a",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <p style={{ color: "#ffffff" }}>Loading collections...</p>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>
      <div style={{ padding: "100px 60px 80px", position: "relative", zIndex: 1, boxSizing: "border-box" }}>
        <h1 style={{ fontFamily: "'Fraunces', serif", fontSize: "56px", fontWeight: 300, marginBottom: "8px" }}>
          All Collections
        </h1>
        <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "16px", marginBottom: "40px" }}>
          {collections.length} universes · {collections.reduce((sum, c) => sum + c.movie_count, 0)} titles
        </p>

        {/* Category Filter Pills */}
        <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "48px" }}>
          {categories.map((cat) => (
            <button
              key={cat.key}
              onClick={() => setActiveCategory(cat.key)}
              style={{
                padding: "9px 20px",
                borderRadius: "9999px",
                border: activeCategory === cat.key ? "none" : "1px solid rgba(255,255,255,0.2)",
                backgroundColor: activeCategory === cat.key ? "#7c3aed" : "transparent",
                color: activeCategory === cat.key ? "#ffffff" : "rgba(255,255,255,0.6)",
                cursor: "pointer",
                fontSize: "13px",
                fontWeight: 500,
                transition: "all 0.2s",
              }}
            >
              {cat.label}
            </button>
          ))}
        </div>

        
        {/* Collections Grid */}
        {/* Collections Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
            gap: "24px",
          }}
        >
          {filtered.map((collection) => {
            console.log({
              name: collection.name,
              banner: collection.banner_url,
              poster: collection.poster_url,
              movieCount: collection.movie_count,
            });

            return (
              <Link key={collection.id} href={`/collections/${collection.slug}`}>
                <div
                  style={{
                    borderRadius: "16px",
                    overflow: "hidden",
                    backgroundColor: "#111111",
                    border: "1px solid rgba(255,255,255,0.08)",
                    transition: "all 0.3s",
                    cursor: "pointer",
                  }}
                  onMouseEnter={(e) => {
                    const el = e.currentTarget as HTMLDivElement;
                    el.style.transform = "translateY(-8px)";
                    el.style.boxShadow = "0 24px 48px rgba(0,0,0,0.6)";
                    el.style.borderColor = "#7c3aed";
                  }}
                  onMouseLeave={(e) => {
                    const el = e.currentTarget as HTMLDivElement;
                    el.style.transform = "translateY(0)";
                    el.style.boxShadow = "none";
                    el.style.borderColor = "rgba(255,255,255,0.08)";
                  }}
                >
                  {/* Banner */}
                  <div
                    style={{
                      height: "160px",
                      backgroundImage: collection.banner_url
                        ? `url(${collection.banner_url})`
                        : "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
                      backgroundSize: "cover",
                      backgroundPosition: "center",
                      position: "relative",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <div
                      style={{
                        position: "absolute",
                        inset: 0,
                        background:
                          "linear-gradient(to top, #111111 0%, transparent 60%)",
                      }}
                    />
                    {!collection.banner_url && (
                      <span
                        style={{
                          fontSize: "64px",
                          position: "relative",
                          zIndex: 1,
                        }}
                      >
                        {collection.icon}
                      </span>
                    )}
                  </div>

                  {/* Info */}
                  <div style={{ padding: "20px" }}>
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "start",
                        marginBottom: "8px",
                      }}
                    >
                      <h3
                        style={{
                          fontFamily: "'Fraunces', serif",
                          fontSize: "18px",
                          fontWeight: 600,
                          color: "#ffffff",
                          margin: 0,
                        }}
                      >
                        {collection.icon} {collection.name}
                      </h3>

                      <span
                        style={{
                          backgroundColor: "rgba(124,58,237,0.2)",
                          color: "#a78bfa",
                          padding: "3px 10px",
                          borderRadius: "9999px",
                          fontSize: "11px",
                          fontWeight: 600,
                          whiteSpace: "nowrap",
                          marginLeft: "8px",
                        }}
                      >
                        {collection.movie_count}
                      </span>
                    </div>

                    <p
                      style={{
                        fontSize: "12px",
                        color: "rgba(255,255,255,0.5)",
                        lineHeight: 1.6,
                        marginBottom: "16px",
                        overflow: "hidden",
                        display: "-webkit-box",
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: "vertical",
                      }}
                    >
                      {collection.description}
                    </p>

                    {/* Preview Posters */}
                    <div style={{ display: "flex", gap: "6px" }}>
                      {collection.top_movies?.slice(0, 6).map((movie) => (
                        <div
                          key={movie.id}
                          style={{
                            width: "36px",
                            height: "54px",
                            borderRadius: "4px",
                            overflow: "hidden",
                            backgroundColor: "#1a1a2e",
                            flexShrink: 0,
                          }}
                        >
                          <SmartImage
                            src={movie.poster_url}
                            alt={movie.title}
                            icon="🎬"
                            fontSize="16px"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
