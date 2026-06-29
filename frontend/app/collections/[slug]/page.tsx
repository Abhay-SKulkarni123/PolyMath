"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import SmartImage from "@/components/SmartImage";
import api from "@/lib/api";
import { Collection, Movie, Product } from "@/lib/types";

export default function CollectionDetailPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [collection, setCollection] = useState<Collection | null>(null);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [relatedBooks, setRelatedBooks] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [sort, setSort] = useState("order");

  useEffect(() => {
    fetchCollection();
  }, [slug]);

  const fetchCollection = async () => {
    try {
      setLoading(true);
      const [colRes, moviesRes] = await Promise.all([
        api.get(`/api/cinema/collections/${slug}/`),
        api.get(`/api/cinema/collections/${slug}/movies/`),
      ]);
      const colData = colRes.data.data || colRes.data;
      setCollection(colData);
      setMovies(moviesRes.data.results || moviesRes.data || []);

      try {
        const booksRes = await api.get("/api/products/?page=1");
        const allBooks: Product[] = booksRes.data.results || booksRes.data || [];
        const categoryKeywords: Record<string, string[]> = {
          superhero: ["comic", "marvel", "dc", "superhero"],
          fantasy: ["fantasy", "magic", "myth"],
          franchise: ["action", "adventure", "thriller"],
          series: ["drama", "crime", "mystery"],
          indian_epic: ["mythology", "hindu", "epic", "ramayana", "mahabharata"],
          indian_cinema: ["indian", "bollywood"],
          anime: ["anime", "manga", "japan"],
        };
        const keywords = categoryKeywords[colData.category] || [];
        const matched = allBooks.filter((b) => {
          const text = (b.name + " " + (b.description || "")).toLowerCase();
          return (
            keywords.some((k) => text.includes(k)) ||
            b.knowledge_fields?.some((f) => keywords.some((k) => f.name.toLowerCase().includes(k)))
          );
        });
        setRelatedBooks(matched.slice(0, 6));
      } catch (bookErr) {
        console.error("Related books fetch failed (non-critical):", bookErr);
        setRelatedBooks([]);
      }
    } catch (err) {
      console.error("Failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const sortedMovies = [...movies]
    .filter((m) => filter === "all" || m.type === filter)
    .sort((a, b) => {
      if (sort === "rating") return b.vote_average - a.vote_average;
      if (sort === "year") return (b.release_date || "").localeCompare(a.release_date || "");
      if (sort === "popularity") return b.popularity - a.popularity;
      return (a.order || 0) - (b.order || 0);
    });

  if (loading) {
    return (
      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#0a0612",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <p style={{ color: "#ffffff" }}>Loading collection...</p>
      </div>
    );
  }

  if (!collection) {
    return (
      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#0a0612",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <p style={{ color: "#ffffff" }}>Collection not found</p>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>
      <div
        style={{
          position: "relative",
          height: "85vh",
          zIndex: 1,
          backgroundImage: collection.banner_url
            ? `url(${collection.banner_url})`
            : "linear-gradient(135deg, #1a0a2e 0%, #2d1657 50%, #1a0a2e 100%)",
          backgroundSize: "cover",
          backgroundPosition: "center -20%",
          display: "flex",
          alignItems: "flex-end",
          boxSizing: "border-box",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to top, #0a0612 0%, rgba(10,6,18,0.5) 60%, rgba(10,6,18,0.3) 100%)",
          }}
        />
        <div style={{ position: "relative", zIndex: 1, padding: "0 60px 50px" }}>
          <Link
            href="/collections"
            style={{ color: "#c084fc", textDecoration: "none", fontSize: "13px", fontWeight: 500 }}
          >
            Back to All Collections
          </Link>
          <h1
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "52px",
              fontWeight: 700,
              margin: "12px 0 8px",
              textShadow: "0 2px 30px rgba(168,85,247,0.6)",
            }}
          >
            {collection.icon} {collection.name}
          </h1>
          <p
            style={{
              color: "rgba(255,255,255,0.7)",
              fontSize: "15px",
              marginBottom: "16px",
              maxWidth: "600px",
              lineHeight: 1.6,
            }}
          >
            {collection.description}
          </p>
          <span
            style={{
              backgroundColor: "rgba(168,85,247,0.2)",
              color: "#c084fc",
              padding: "8px 20px",
              borderRadius: "9999px",
              fontSize: "13px",
              fontWeight: 600,
              border: "1px solid rgba(168,85,247,0.4)",
              boxShadow: "0 0 20px rgba(168,85,247,0.2)",
            }}
          >
            {collection.movie_count} titles
          </span>
        </div>
      </div>

      <div
        style={{
          padding: "28px 60px",
          display: "flex",
          gap: "16px",
          alignItems: "center",
          flexWrap: "wrap",
          borderBottom: "1px solid rgba(168,85,247,0.15)",
          position: "relative",
          zIndex: 1,
          backgroundColor: "#0a0612",
        }}
      >
        <div style={{ display: "flex", gap: "8px" }}>
          {["all", "movie", "series"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{
                padding: "8px 18px",
                borderRadius: "9999px",
                border: filter === f ? "none" : "1px solid rgba(168,85,247,0.3)",
                backgroundColor: filter === f ? "#9333ea" : "transparent",
                color: filter === f ? "#ffffff" : "rgba(255,255,255,0.6)",
                cursor: "pointer",
                fontSize: "13px",
                fontWeight: 500,
                boxShadow: filter === f ? "0 0 16px rgba(147,51,234,0.5)" : "none",
                transition: "all 0.2s",
              }}
            >
              {f === "all" ? "All" : f === "movie" ? "Movies" : "Series"}
            </button>
          ))}
        </div>

        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: "12px" }}>
          <span style={{ color: "rgba(255,255,255,0.4)", fontSize: "13px" }}>Sort:</span>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value)}
            style={{
              backgroundColor: "#150a26",
              color: "#ffffff",
              border: "1px solid rgba(168,85,247,0.3)",
              borderRadius: "8px",
              padding: "8px 14px",
              fontSize: "13px",
              cursor: "pointer",
            }}
          >
            <option value="order">Watch Order</option>
            <option value="rating">Top Rated</option>
            <option value="year">Newest First</option>
            <option value="popularity">Most Popular</option>
          </select>
        </div>
      </div>

      <div style={{ padding: "32px 60px 80px", position: "relative", zIndex: 1 }}>
        <p style={{ color: "rgba(255,255,255,0.3)", fontSize: "12px", marginBottom: "24px" }}>
          Showing {sortedMovies.length} titles
        </p>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: "20px" }}>
          {sortedMovies.map((movie) => (
            <Link key={movie.id} href={`/movies/${movie.id}`} style={{ textDecoration: "none" }}>
              <div
                style={{ cursor: "pointer", transition: "all 0.3s" }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLDivElement).style.transform = "scale(1.05)";
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLDivElement).style.transform = "scale(1)";
                }}
              >
                <div
                  style={{
                    width: "100%",
                    aspectRatio: "2/3",
                    borderRadius: "10px",
                    overflow: "hidden",
                    backgroundColor: "#150a26",
                    marginBottom: "10px",
                    border: "1px solid rgba(168,85,247,0.15)",
                  }}
                >
                  <SmartImage src={movie.poster_url} alt={movie.title} icon="🎬" fontSize="28px" />
                </div>

                <p
                  style={{ fontSize: "12px", fontWeight: 600, color: "#ffffff", marginBottom: "4px", lineHeight: 1.3 }}
                >
                  {movie.order ? `${movie.order}. ` : ""}
                  {movie.title}
                </p>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "11px",
                    color: "rgba(255,255,255,0.4)",
                  }}
                >
                  <span style={{ color: "#c084fc" }}>{movie.vote_average?.toFixed(1)}/10</span>
                  <span>{movie.release_date?.split("-")[0]}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {relatedBooks.length > 0 && (
        <div
          style={{
            padding: "0 60px 80px",
            borderTop: "1px solid rgba(168,85,247,0.15)",
            position: "relative",
            zIndex: 1,
          }}
        >
          <div style={{ paddingTop: "40px" }}>
            <h2
              style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "26px",
                fontWeight: 600,
                marginBottom: "8px",
                textShadow: "0 0 20px rgba(168,85,247,0.3)",
              }}
            >
              📖 Related Books & Free eBooks
            </h2>
            <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "13px", marginBottom: "24px" }}>
              Deepen your understanding of this universe through reading
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: "20px" }}>
              {relatedBooks.map((book) => (
                <Link key={book.id} href={`/products/${book.id}`} style={{ textDecoration: "none" }}>
                  <div
                    style={{
                      borderRadius: "10px",
                      backgroundColor: "#150a26",
                      border: "1px solid rgba(168,85,247,0.2)",
                      padding: "16px",
                      cursor: "pointer",
                      transition: "all 0.3s",
                      height: "100%",
                      boxSizing: "border-box",
                    }}
                    onMouseEnter={(e) => {
                      const el = e.currentTarget as HTMLDivElement;
                      el.style.borderColor = "#c084fc";
                      el.style.boxShadow = "0 8px 24px rgba(147,51,234,0.3)";
                    }}
                    onMouseLeave={(e) => {
                      const el = e.currentTarget as HTMLDivElement;
                      el.style.borderColor = "rgba(168,85,247,0.2)";
                      el.style.boxShadow = "none";
                    }}
                  >
                    <div style={{ fontSize: "28px", marginBottom: "10px" }}>
                      {book.knowledge_fields?.[0]?.icon || "📖"}
                    </div>
                    <p
                      style={{
                        fontSize: "12px",
                        fontWeight: 600,
                        color: "#ffffff",
                        marginBottom: "8px",
                        lineHeight: 1.3,
                      }}
                    >
                      {book.name}
                    </p>
                    <p style={{ fontSize: "13px", fontWeight: 700, color: "#c084fc" }}>₹{book.price}</p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
