"use client";
// Reusable ambient background: drifting purple gradient orbs + floating particles.
// Pure CSS animation, no JS loop, so it's cheap and never blocks interaction.
// pointerEvents: "none" ensures it NEVER intercepts clicks - solves the "must not overlap content" requirement.
export default function MagicBackground() {
    return (
        <div
            aria-hidden="true"
            style={{
                position: "fixed",
                inset: 0,
                zIndex: 0,
                overflow: "hidden",
                pointerEvents: "none"
            }}
        >
            <style>{`
        @keyframes drift1 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(60px, 40px) scale(1.15); }
        }
        @keyframes drift2 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(-50px, 60px) scale(1.1); }
        }
        @keyframes drift3 {
          0%, 100% { transform: translate(0, 0) scale(1); }
          50% { transform: translate(40px, -50px) scale(1.2); }
        }
        @keyframes twinkle {
          0%, 100% { opacity: 0.15; }
          50% { opacity: 0.7; }
        }
        .magic-orb-1 { animation: drift1 22s ease-in-out infinite; }
        .magic-orb-2 { animation: drift2 28s ease-in-out infinite; }
        .magic-orb-3 { animation: drift3 25s ease-in-out infinite; }
        .magic-particle { animation: twinkle 4s ease-in-out infinite; }
      `}</style>

            {/* Drifting gradient orbs */}
            <div className="magic-orb-1" style={{
                position: "absolute",
                top: "5%",
                left: "10%",
                width: "500px",
                height: "500px",
                borderRadius: "50%",
                background: "radial-gradient(circle, rgba(147,51,234,0.18) 0%, transparent 70%)",
                filter: "blur(40px)"
            }} />
            <div className="magic-orb-2" style={{
                position: "absolute",
                top: "40%",
                right: "5%",
                width: "450px",
                height: "450px",
                borderRadius: "50%",
                background: "radial-gradient(circle, rgba(99,30,180,0.16) 0%, transparent 70%)",
                filter: "blur(40px)"
            }} />
            <div className="magic-orb-3" style={{
                position: "absolute",
                bottom: "5%",
                left: "30%",
                width: "400px",
                height: "400px",
                borderRadius: "50%",
                background: "radial-gradient(circle, rgba(168,85,247,0.14) 0%, transparent 70%)",
                filter: "blur(40px)"
            }} />

            {/* Floating particles */}
            {Array.from({ length: 24 }).map((_, i) => {
                const left = (i * 37) % 100;
                const top = (i * 53) % 100;
                const size = 2 + (i % 3);
                const delay = (i % 8) * 0.5;
                return (
                    <div
                        key={i}
                        className="magic-particle"
                        style={{
                            position: "absolute",
                            left: `${left}%`,
                            top: `${top}%`,
                            width: `${size}px`,
                            height: `${size}px`,
                            borderRadius: "50%",
                            backgroundColor: "#c084fc",
                            boxShadow: "0 0 6px rgba(192,132,252,0.8)",
                            animationDelay: `${delay}s`
                        }}
                    />
                );
            })}
        </div>
    );
}