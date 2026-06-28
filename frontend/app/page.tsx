"use client";
import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import SmartImage from "@/components/SmartImage";
import api from "@/lib/api";
import { Collection, Movie, Product } from "@/lib/types";

export default function HomePage() {
  const [collections, setCollections] = useState<Collection[]>([]);
  const [books, setBooks] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [heroMovie, setHeroMovie] = useState<Movie | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [collectionsRes, booksRes] = await Promise.all([
        api.get("/api/cinema/collections/"),
        api.get("/api/products/?page=1"),
      ]);

      const allCollections: Collection[] = collectionsRes.data.results || collectionsRes.data || [];
      const active = allCollections.filter((c) => c.movie_count > 0);
      setCollections(active);

      const allBooks: Product[] = booksRes.data.results || booksRes.data || [];
      setBooks(allBooks);

      const topMovies = active[0]?.top_movies || [];
      const hero = topMovies.find((m) => m.backdrop_path) || topMovies[0] || null;
      setHeroMovie(hero);
    } catch (err) {
      console.error("Failed to fetch:", err);
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
          backgroundImage: "radial-gradient(circle at 50% 0%, rgba(147,51,234,0.15) 0%, transparent 50%)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div style={{ textAlign: "center" }}>
          <p
            style={{
              color: "#ffffff",
              fontSize: "18px",
              marginBottom: "8px",
              textShadow: "0 0 20px rgba(168,85,247,0.5)",
            }}
          >
            Loading Polymath...
          </p>
          <p style={{ color: "rgba(255,255,255,0.4)", fontSize: "14px" }}>Your universe awaits</p>
        </div>
      </div>
    );
  }

  const movieCollections = collections.filter((c) => c.category !== "series");
  const seriesCollections = collections.filter((c) => c.category === "series");

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#0a0612", color: "#ffffff", position: "relative" }}>
      {/* HERO SECTION */}
      {heroMovie && (
        <div
          style={{
            position: "relative",
            marginTop: 0,
            height: "90vh",
            overflow: "hidden",
            marginBottom: "60px",
            zIndex: 1,
          }}
        >
          <div
            style={{
              position: "absolute",
              inset: 0,
              backgroundImage: heroMovie.backdrop_url
                ? `url(${heroMovie.backdrop_url})`
                : "linear-gradient(135deg, #1a0a2e 0%, #2d1657 50%, #1a0a2e 100%)",
              backgroundSize: "cover",
              backgroundPosition: "center 0.001%",
              filter: "brightness(0.65) saturate(1.1)",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: "linear-gradient(to right, rgba(10,6,18,0.85) 35%, rgba(80,20,160,0.15) 100%)",
            }}
          />
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: "linear-gradient(to top, #0a0612 0%, transparent 35%)",
            }}
          />
          <div
            style={{
              position: "absolute",
              bottom: "0",
              left: "0",
              width: "100%",
              height: "2px",
              background: "linear-gradient(to right, transparent, rgba(168,85,247,0.8), transparent)",
              boxShadow: "0 0 30px rgba(168,85,247,0.8)",
            }}
          />

          <div style={{ position: "absolute", bottom: "100px", left: "20px", maxWidth: "600px" }}>
            <div
              style={{
                display: "inline-block",
                backgroundColor: "rgba(147,51,234,0.25)",
                color: "#e9d5ff",
                padding: "6px 16px",
                borderRadius: "9999px",
                fontSize: "12px",
                fontWeight: 700,
                marginBottom: "20px",
                textTransform: "uppercase",
                letterSpacing: "1.5px",
                border: "1px solid rgba(168,85,247,0.5)",
                boxShadow: "0 0 24px rgba(168,85,247,0.35)",
              }}
            >
              Featured Tonight
            </div>
            <h1
              style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "64px",
                fontWeight: 700,
                lineHeight: 1.1,
                marginBottom: "20px",
                textShadow: "0 0 40px rgba(168,85,247,0.6), 0 2px 20px rgba(0,0,0,0.6)",
              }}
            >
              {heroMovie.title}
            </h1>
            <p
              style={{
                fontSize: "16px",
                lineHeight: 1.7,
                color: "rgba(255,255,255,0.82)",
                marginBottom: "32px",
                overflow: "hidden",
                display: "-webkit-box",
                WebkitLineClamp: 3,
                WebkitBoxOrient: "vertical",
              }}
            >
              {heroMovie.overview}
            </p>
            <div style={{ display: "flex", gap: "16px", alignItems: "center" }}>
              <button
                onClick={() => window.open(heroMovie.watch_url, "_blank")}
                style={{
                  backgroundColor: "#9333ea",
                  color: "#ffffff",
                  padding: "16px 32px",
                  borderRadius: "8px",
                  border: "none",
                  fontSize: "16px",
                  fontWeight: 700,
                  cursor: "pointer",
                  boxShadow: "0 0 32px rgba(147,51,234,0.6)",
                  transition: "all 0.2s",
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#a855f7";
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLButtonElement).style.backgroundColor = "#9333ea";
                }}
              >
                Watch Now
              </button>
              <Link
                href={`/movies/${heroMovie.id}`}
                style={{
                  backgroundColor: "rgba(255,255,255,0.1)",
                  color: "#ffffff",
                  padding: "16px 32px",
                  borderRadius: "8px",
                  textDecoration: "none",
                  fontSize: "16px",
                  fontWeight: 600,
                  border: "1px solid rgba(168,85,247,0.3)",
                }}
              >
                More Info
              </Link>
            </div>
            <div
              style={{
                display: "flex",
                gap: "20px",
                marginTop: "20px",
                fontSize: "14px",
                color: "rgba(255,255,255,0.6)",
              }}
            >
              <span style={{ color: "#c084fc", fontWeight: 600 }}>{heroMovie.vote_average?.toFixed(1)} / 10</span>
              <span>{heroMovie.release_date?.split("-")[0]}</span>
              <span style={{ textTransform: "capitalize" }}>{heroMovie.type}</span>
            </div>
          </div>
        </div>
      )}

      {/* BOOKS SECTION */}
      {books.length > 0 && (
        <div style={{ marginBottom: "60px", padding: "0 40px", position: "relative", zIndex: 1 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "24px" }}>
            <div>
              <h2
                style={{
                  fontFamily: "'Fraunces', serif",
                  fontSize: "28px",
                  fontWeight: 600,
                  color: "#ffffff",
                  marginBottom: "4px",
                  textShadow: "0 0 20px rgba(168,85,247,0.3)",
                }}
              >
                📚 Premium Knowledge Books
              </h2>
              <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "14px" }}>
                Buy, read free, or discover related movies
              </p>
            </div>
            <Link
              href="/products"
              style={{
                color: "#c084fc",
                textDecoration: "none",
                fontSize: "14px",
                fontWeight: 500,
                whiteSpace: "nowrap",
              }}
            >
              View all books
            </Link>
          </div>

          <div
            style={{
              display: "flex",
              gap: "16px",
              overflowX: "auto",
              scrollbarWidth: "none",
              msOverflowStyle: "none",
              paddingBottom: "8px",
            }}
          >
            {books.slice(0, 12).map((book) => (
              <BookCard key={book.id} book={book} />
            ))}
            <Link href="/products" style={{ textDecoration: "none", flexShrink: 0 }}>
              <div
                style={{
                  width: "150px",
                  height: "220px",
                  borderRadius: "10px",
                  border: "2px dashed rgba(168,85,247,0.3)",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: "8px",
                  cursor: "pointer",
                  color: "rgba(255,255,255,0.5)",
                  transition: "all 0.3s",
                }}
                onMouseEnter={(e) => {
                  const el = e.currentTarget as HTMLDivElement;
                  el.style.borderColor = "#c084fc";
                  el.style.color = "#c084fc";
                  el.style.boxShadow = "0 0 20px rgba(168,85,247,0.2)";
                }}
                onMouseLeave={(e) => {
                  const el = e.currentTarget as HTMLDivElement;
                  el.style.borderColor = "rgba(168,85,247,0.3)";
                  el.style.color = "rgba(255,255,255,0.5)";
                  el.style.boxShadow = "none";
                }}
              >
                <span style={{ fontSize: "24px" }}>📚</span>
                <span style={{ fontSize: "11px", fontWeight: 600, textAlign: "center" }}>View All Books</span>
              </div>
            </Link>
          </div>
        </div>
      )}

      {/* CINEMA COLLECTIONS SECTION */}
      <div style={{ padding: "0 40px 20px", position: "relative", zIndex: 1 }}>
        <div style={{ marginBottom: "32px" }}>
          <h2
            style={{
              fontFamily: "'Fraunces', serif",
              fontSize: "32px",
              fontWeight: 600,
              color: "#ffffff",
              marginBottom: "4px",
              textShadow: "0 0 24px rgba(168,85,247,0.35)",
            }}
          >
            🎬 Cinematic Universes
          </h2>
          <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "14px" }}>
            Explore {movieCollections.length} curated universes and franchises
          </p>
        </div>
      </div>

      <div style={{ padding: "0 40px", position: "relative", zIndex: 1 }}>
        {movieCollections.map((collection) => (
          <CollectionRow key={collection.id} collection={collection} />
        ))}
      </div>

      {/* WEB SERIES SECTION */}
      {seriesCollections.length > 0 && (
        <div style={{ padding: "0 40px 80px", position: "relative", zIndex: 1 }}>
          <div style={{ marginBottom: "32px", paddingTop: "20px", borderTop: "1px solid rgba(168,85,247,0.15)" }}>
            <h2
              style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "32px",
                fontWeight: 600,
                color: "#ffffff",
                marginBottom: "4px",
                textShadow: "0 0 24px rgba(168,85,247,0.35)",
              }}
            >
              📺 Must-Watch Series
            </h2>
            <p style={{ color: "rgba(255,255,255,0.5)", fontSize: "14px" }}>
              The greatest television ever made, curated for you
            </p>
          </div>
          {seriesCollections.map((collection) => (
            <CollectionRow key={collection.id} collection={collection} />
          ))}
        </div>
      )}
    </div>
  );
}

function BookCard({ book }: { book: Product }) {
  const [hovered, setHovered] = useState(false);
  const router = useRouter();
  const coverImage = null;

  return (
    <div
      onClick={() => router.push(`/products/${book.id}`)}
      style={{
        width: "150px",
        height: "220px",
        flexShrink: 0,
        borderRadius: "10px",
        backgroundColor: "#150a26",
        border: "1px solid rgba(168,85,247,0.2)",
        cursor: "pointer",
        transition: "all 0.3s",
        transform: hovered ? "scale(1.05)" : "scale(1)",
        boxShadow: hovered ? "0 12px 36px rgba(147,51,234,0.4)" : "none",
        position: "relative",
        overflow: "hidden",
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      {coverImage ? (
        <img src={coverImage} alt={book.name} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      ) : (
        <div
          style={{
            width: "100%",
            height: "100%",
            background: "linear-gradient(135deg, #1a0a2e 0%, #2d1657 50%, #1a0a2e 100%)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: "16px",
            boxSizing: "border-box",
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: "32px", marginBottom: "10px" }}>{book.knowledge_fields?.[0]?.icon || "📚"}</div>
          <p
            style={{
              fontSize: "11px",
              fontWeight: 600,
              color: "#ffffff",
              lineHeight: 1.3,
              margin: 0,
            }}
          >
            {book.name.replace("⭐ ", "")}
          </p>
        </div>
      )}

      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          background: "linear-gradient(to top, rgba(10,6,18,0.95) 0%, transparent 100%)",
          padding: "10px",
          paddingTop: "30px",
        }}
      >
        <p style={{ fontSize: "12px", fontWeight: 700, color: "#c084fc" }}>₹{book.price}</p>
        {hovered && (
          <div
            style={{
              marginTop: "4px",
              backgroundColor: "rgba(147,51,234,0.9)",
              color: "#ffffff",
              padding: "4px 10px",
              borderRadius: "6px",
              fontSize: "10px",
              fontWeight: 600,
              textAlign: "center",
            }}
          >
            View Book
          </div>
        )}
      </div>
    </div>
  );
}

function CollectionRow({ collection }: { collection: Collection }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: direction === "left" ? -500 : 500, behavior: "smooth" });
    }
  };

  const moviesToShow = (collection.top_movies || []).slice(0, 6);
  if (moviesToShow.length === 0) return null;

  return (
    <div style={{ marginBottom: "48px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
        <Link
          href={`/collections/${collection.slug}`}
          style={{ textDecoration: "none", color: "inherit", display: "flex", alignItems: "center", gap: "12px" }}
        >
          <span style={{ fontSize: "24px" }}>{collection.icon}</span>
          <div>
            <h2
              style={{
                fontFamily: "'Fraunces', serif",
                fontSize: "20px",
                fontWeight: 600,
                color: "#ffffff",
                margin: 0,
              }}
            >
              {collection.name}
            </h2>
            <p style={{ fontSize: "12px", color: "rgba(255,255,255,0.4)", margin: 0, marginTop: "2px" }}>
              {collection.movie_count} titles
            </p>
          </div>
          <span style={{ color: "#c084fc", fontSize: "13px", fontWeight: 500 }}>See all</span>
        </Link>

        <div style={{ display: "flex", gap: "8px" }}>
          <button
            onClick={() => scroll("left")}
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              border: "1px solid rgba(168,85,247,0.3)",
              backgroundColor: "rgba(147,51,234,0.1)",
              color: "#ffffff",
              cursor: "pointer",
              fontSize: "16px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {"<"}
          </button>
          <button
            onClick={() => scroll("right")}
            style={{
              width: "32px",
              height: "32px",
              borderRadius: "50%",
              border: "1px solid rgba(168,85,247,0.3)",
              backgroundColor: "rgba(147,51,234,0.1)",
              color: "#ffffff",
              cursor: "pointer",
              fontSize: "16px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {">"}
          </button>
        </div>
      </div>

      <div
        ref={scrollRef}
        style={{
          display: "flex",
          gap: "16px",
          overflowX: "auto",
          scrollbarWidth: "none",
          msOverflowStyle: "none",
          paddingBottom: "8px",
        }}
      >
        {moviesToShow.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}

        <Link href={`/collections/${collection.slug}`} style={{ textDecoration: "none", flexShrink: 0 }}>
          <div
            style={{
              width: "160px",
              aspectRatio: "2/3",
              borderRadius: "10px",
              border: "2px dashed rgba(168,85,247,0.3)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              gap: "12px",
              cursor: "pointer",
              color: "rgba(255,255,255,0.6)",
              transition: "all 0.3s",
            }}
            onMouseEnter={(e) => {
              const el = e.currentTarget as HTMLDivElement;
              el.style.borderColor = "#c084fc";
              el.style.color = "#c084fc";
              el.style.boxShadow = "0 0 24px rgba(168,85,247,0.25)";
            }}
            onMouseLeave={(e) => {
              const el = e.currentTarget as HTMLDivElement;
              el.style.borderColor = "rgba(168,85,247,0.3)";
              el.style.color = "rgba(255,255,255,0.6)";
              el.style.boxShadow = "none";
            }}
          >
            <span style={{ fontSize: "28px" }}>{collection.icon}</span>
            <span style={{ fontSize: "11px", fontWeight: 600, textAlign: "center", lineHeight: 1.4 }}>
              View All
              <br />
              {collection.movie_count} titles
            </span>
          </div>
        </Link>
      </div>
    </div>
  );
}

function MovieCard({ movie }: { movie: Movie }) {
  const [hovered, setHovered] = useState(false);
  const router = useRouter();

  return (
    <div
      style={{
        width: "160px",
        position: "relative",
        borderRadius: "10px",
        overflow: "hidden",
        cursor: "pointer",
        transition: "all 0.3s",
        transform: hovered ? "scale(1.05)" : "scale(1)",
        boxShadow: hovered ? "0 16px 36px rgba(147,51,234,0.45)" : "none",
        flexShrink: 0,
        border: "1px solid rgba(168,85,247,0.1)",
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={() => router.push(`/movies/${movie.id}`)}
    >
      <div
        style={{
          width: "160px",
          aspectRatio: "2/3",
          backgroundColor: "#150a26",
        }}
      >
        <SmartImage src={movie.poster_url} alt={movie.title} icon="🎬" fontSize="32px" />
      </div>

      {hovered && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to top, rgba(10,6,18,0.97) 40%, rgba(10,6,18,0.2) 100%)",
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-end",
            padding: "12px",
          }}
        >
          <p style={{ fontSize: "11px", fontWeight: 700, color: "#ffffff", marginBottom: "6px", lineHeight: 1.3 }}>
            {movie.title}
          </p>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <span style={{ fontSize: "10px", color: "#c084fc", fontWeight: 600 }}>
              {movie.vote_average?.toFixed(1)}/10
            </span>
            <span style={{ fontSize: "10px", color: "rgba(255,255,255,0.6)" }}>
              {movie.release_date?.split("-")[0]}
            </span>
          </div>
          <button
            onClick={(e) => {
              e.stopPropagation();
              window.open(movie.watch_url, "_blank");
            }}
            style={{
              backgroundColor: "#9333ea",
              color: "#ffffff",
              padding: "6px",
              borderRadius: "6px",
              textAlign: "center",
              fontSize: "11px",
              fontWeight: 600,
              border: "none",
              cursor: "pointer",
              width: "100%",
              boxShadow: "0 0 16px rgba(147,51,234,0.5)",
            }}
          >
            Watch Free
          </button>
        </div>
      )}
    </div>
  );
}
