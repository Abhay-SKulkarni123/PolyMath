"use client";
import { useState } from "react";

// Drop-in replacement for <img> that auto-falls-back to a styled gradient card
// if the URL 404s or is empty. Solves "missing cover" issues for BOTH
// movie posters (wrong/stale TMDB paths) and book covers (missing DB image field)
// without needing to hand-verify every single URL.
interface SmartImageProps {
    src: string | null | undefined;
    alt: string;
    icon?: string;
    fontSize?: string;
}

export default function SmartImage({ src, alt, icon = "🎬", fontSize = "32px" }: SmartImageProps) {
    const [failed, setFailed] = useState(false);

    if (!src || failed) {
        return (
            <div style={{
                width: "100%",
                height: "100%",
                background: "linear-gradient(135deg, #1a0a2e 0%, #2d1657 50%, #1a0a2e 100%)",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: "8px",
                padding: "12px",
                boxSizing: "border-box",
                textAlign: "center"
            }}>
                <span style={{ fontSize }}>{icon}</span>
                <p style={{
                    fontSize: "10px",
                    color: "rgba(255,255,255,0.6)",
                    lineHeight: 1.3,
                    margin: 0
                }}>
                    {alt}
                </p>
            </div>
        );
    }

    return (
        <img
            src={src}
            alt={alt}
            loading="lazy"
            onError={() => setFailed(true)}
            style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
        />
    );
}