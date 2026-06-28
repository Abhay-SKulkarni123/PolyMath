"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import SmartImage from "@/components/SmartImage";
import api from "@/lib/api";
import { Movie, Product } from "@/lib/types";

interface CollectionInfo {
  name: string;
  slug: string;
  icon: string;
}

interface MovieDetail {
  data: Movie;
  related: Movie[];
  collection: CollectionInfo;
}

const CATEGORY_KEYWORDS: Record<string, string[]> = {
  superhero: ["comic", "marvel", "dc", "superhero"],
  fantasy: ["fantasy", "magic", "myth"],
  franchise: ["action", "adventure", "thriller"],
  series: ["drama", "crime", "mystery"],
  indian_epic: ["mythology", "hindu", "epic", "ramayana", "mahabharata"],
  indian_cinema: ["indian", "bollywood"],
  anime: ["anime", "manga", "japan"],
};

export default function MovieDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [detail, setDetail] = useState<MovieDetail | null>(null);
  const [relatedBooks, setRelatedBooks] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMovie();
  }, [id]);

  const fetchMovie = async () => {
    try {
      setLoading(true);
      const res = await api.get(`/api/cinema/movies/${id}/`);
      setDetail(res.data);

      // Fetch the collection's category so we can match related books -
      // movie detail endpoint only returns name/slug/icon, not category,
      // so we look it up from the collections list (non-critical, fails silently)
      try {
        const colSlug = res.data.collection?.slug;
        if (colSlug) {
          const colRes = await api.get(`/api/cinema/collections/${colSlug}/`);
          const category = (colRes.data.data || colRes.data)?.category;

          const booksRes = await api.get("/api/products/?page=1");
          const allBooks: Product[] = booksRes.data.results || booksRes.data || [];
          const keywords = CATEGORY_KEYWORDS[category] || [];
          const matched = allBooks.filter((b) => {
            const text = (b.name + " " + (b.description || "")).toLowerCase();
            return (
              keywords.some((k) => text.includes(k)) ||
              b.knowledge_fields?.some((f) => keywords.some((k) => f.name.toLowerCase().includes(k)))
            );
          });
          setRelatedBooks(matched.slice(0, 4));
        }
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
        <p style={{ color: "#ffffff" }}>Loading...</p>
      </div>
    );
  }

  if (!detail) {
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
        <p style={{ color: "#ffffff" }}>Movie not found</p>
      </div>
    );
  }

  const movie = detail.data;
  const related = detail.related;
  const collection = detail.collection;

  const backdropUrl = movie.backdrop_url
    ? `url(${movie.backdrop_url})`
    : "linear-gradient(135deg, #1a0a2e 0%, #2d1657 100%)";

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>
      {/* Backdrop Hero */}
      <div
        style={{
          position: "relative",
          height: "75vh",
          backgroundImage: backdropUrl,
          backgroundSize: "cover",
          backgroundPosition: "center",
          boxSizing: "border-box",
          zIndex: 1,
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to right, rgba(10,6,18,0.95) 45%, rgba(45,22,87,0.35) 100%)",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            height: "200px",
            background: "linear-gradient(to top, #0a0612, transparent)",
          }}
        />

        <div
          style={{ position: "absolute", top: "55%", left: "60px", transform: "translateY(-50%)", maxWidth: "520px" }}
        >
          <Link
            href={`/collections/${collection.slug}`}
            style={{
              color: "#c084fc",
              textDecoration: "none",
              fontSize: "13px",
              fontWeight: 500,
              display: "inline-block",
              marginBottom: "16px",
            }}
          >
            {collection.icon} {collection.name}
          </Link>

          <h1
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "48px",
              fontWeight: 700,
              lineHeight: 1.1,
              marginBottom: "16px",
              textShadow: "0 0 30px rgba(168,85,247,0.5)",
            }}
          >
            {movie.title}
          </h1>

          <div
            style={{
              display: "flex",
              gap: "16px",
              marginBottom: "20px",
              fontSize: "14px",
              color: "rgba(255,255,255,0.7)",
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <span style={{ color: "#c084fc", fontWeight: 700, fontSize: "16px" }}>
              {movie.vote_average?.toFixed(1)} / 10
            </span>
            <span>{movie.release_date?.split("-")[0]}</span>
            <span
              style={{
                backgroundColor: "rgba(147,51,234,0.25)",
                color: "#c084fc",
                padding: "3px 10px",
                borderRadius: "9999px",
                fontSize: "11px",
                fontWeight: 600,
                textTransform: "capitalize",
                border: "1px solid rgba(168,85,247,0.4)",
              }}
            >
              {movie.type}
            </span>
          </div>

          <p
            style={{
              fontSize: "15px",
              lineHeight: 1.7,
              color: "rgba(255,255,255,0.78)",
              marginBottom: "32px",
              overflow: "hidden",
              display: "-webkit-box",
              WebkitLineClamp: 4,
              WebkitBoxOrient: "vertical",
            }}
          >
            {movie.overview}
          </p>

          <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
            <button
              onClick={() => window.open(movie.watch_url, "_blank")}
              style={{
                backgroundColor: "#9333ea",
                color: "#ffffff",
                padding: "14px 32px",
                borderRadius: "10px",
                border: "none",
                fontSize: "16px",
                fontWeight: 700,
                cursor: "pointer",
                boxShadow: "0 0 28px rgba(147,51,234,0.55)",
                transition: "all 0.2s",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#a855f7";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#9333ea";
              }}
            >
              Watch Free
            </button>
            <Link
              href={`/collections/${collection.slug}`}
              style={{
                backgroundColor: "rgba(255,255,255,0.1)",
                color: "#ffffff",
                padding: "14px 28px",
                borderRadius: "10px",
                textDecoration: "none",
                fontSize: "15px",
                fontWeight: 600,
                border: "1px solid rgba(168,85,247,0.3)",
              }}
            >
              More Like This
            </Link>
          </div>
        </div>

        {/* Poster Right - SmartImage handles broken/stale TMDB paths gracefully */}
        <div
          style={{
            position: "absolute",
            right: "80px",
            top: "55%",
            transform: "translateY(-50%)",
            width: "200px",
            aspectRatio: "2/3",
            borderRadius: "16px",
            overflow: "hidden",
            boxShadow: "0 24px 60px rgba(147,51,234,0.35), 0 32px 64px rgba(0,0,0,0.6)",
            border: "1px solid rgba(168,85,247,0.25)",
          }}
        >
          <SmartImage src={movie.poster_url} alt={movie.title} fontSize="40px" />
        </div>
      </div>

      {/* Related Movies */}
      {related && related.length > 0 && (
        <div style={{ padding: "60px 60px 40px", position: "relative", zIndex: 1 }}>
          <h2
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "26px",
              fontWeight: 600,
              marginBottom: "24px",
              textShadow: "0 0 20px rgba(168,85,247,0.3)",
            }}
          >
            More from {collection.icon} {collection.name}
          </h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))", gap: "16px" }}>
            {related.slice(0, 10).map((m) => (
              <Link key={m.id} href={`/movies/${m.id}`} style={{ textDecoration: "none" }}>
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
                      marginBottom: "8px",
                      border: "1px solid rgba(168,85,247,0.15)",
                    }}
                  >
                    <SmartImage src={m.poster_url} alt={m.title} fontSize="28px" />
                  </div>
                  <p
                    style={{
                      fontSize: "11px",
                      fontWeight: 600,
                      color: "#ffffff",
                      marginBottom: "3px",
                      lineHeight: 1.3,
                    }}
                  >
                    {m.title}
                  </p>
                  <span style={{ fontSize: "11px", color: "#c084fc" }}>{m.vote_average?.toFixed(1)}/10</span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Related Books and Free eBooks */}
      {relatedBooks.length > 0 && (
        <div
          style={{
            padding: "20px 60px 80px",
            borderTop: "1px solid rgba(168,85,247,0.15)",
            position: "relative",
            zIndex: 1,
          }}
        >
          <div style={{ paddingTop: "40px" }}>
            <h2
              style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "24px",
                fontWeight: 600,
                marginBottom: "8px",
                textShadow: "0 0 20px rgba(168,85,247,0.3)",
              }}
            >
              📖 Read the Source Material
            </h2>
            <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "13px", marginBottom: "24px" }}>
              Books and free ebooks related to this universe
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))", gap: "16px" }}>
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
                    <div style={{ fontSize: "24px", marginBottom: "10px" }}>
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
