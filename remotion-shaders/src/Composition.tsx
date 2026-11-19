import { Composition, AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from "remotion";
import { MeshGradient, GrainGradient } from "@paper-design/shaders-react";
import { Fondos } from "./Fondos";

export const MyComposition = () => (
  <>
    <Composition id="Prueba" component={Prueba} durationInFrames={180} fps={30} width={1080} height={1920} />
    <Composition id="Fondos" component={Fondos} durationInFrames={180} fps={30} width={1080} height={1920} />
  </>
);

const words = ["Remotion", "+", "Paper", "Shaders"];

export const Prueba: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const out = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const lineW = interpolate(frame, [40, 70], [0, 520], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const sub = spring({ frame: frame - 60, fps, config: { damping: 200 } });

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a0f0a" }}>
      <MeshGradient
        colors={["#ff6b35", "#f7c59f", "#9b2226", "#2a1810"]}
        distortion={0.9} swirl={0.6} speed={0} frame={ms * 1.5}
        style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
      />
      <GrainGradient
        colors={["#00000000", "#00000055"]} colorBack="#00000000" shape="wave" intensity={0.4} noise={0.35}
        speed={0} frame={ms}
        style={{ position: "absolute", inset: 0, width: "100%", height: "100%", mixBlendMode: "multiply" }}
      />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", opacity: out, fontFamily: "Helvetica, Arial, sans-serif", color: "#fff8f0" }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
          {words.map((w, i) => {
            const s = spring({ frame: frame - i * 8, fps, config: { damping: 14, stiffness: 120 } });
            return (
              <div key={w} style={{ fontSize: w === "+" ? 110 : 170, fontWeight: 800, letterSpacing: -4, lineHeight: 1,
                transform: `translateY(${(1 - s) * 140}px) scale(${0.8 + 0.2 * s})`, opacity: s, textShadow: "0 10px 40px rgba(0,0,0,0.35)" }}>
                {w}
              </div>
            );
          })}
        </div>
        <div style={{ width: lineW, height: 8, background: "#fff8f0", borderRadius: 4, margin: "60px 0 40px" }} />
        <div style={{ fontSize: 56, fontWeight: 500, opacity: sub, transform: `translateY(${(1 - sub) * 30}px)` }}>
          Vídeo de prueba ✓
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
