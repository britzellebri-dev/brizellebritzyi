import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { Warp, Swirl, Dithering } from "@paper-design/shaders-react";

const full = { position: "absolute" as const, inset: 0, width: "100%", height: "100%" };

const Label: React.FC<{ title: string; sub: string; color: string }> = ({ title, sub, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 13, stiffness: 140 } });
  const sub2 = spring({ frame: frame - 8, fps, config: { damping: 200 } });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", fontFamily: "Helvetica, Arial, sans-serif", color }}>
      <div style={{ fontSize: 190, fontWeight: 900, letterSpacing: -6, transform: `scale(${0.7 + 0.3 * s})`, opacity: s, textShadow: "0 12px 50px rgba(0,0,0,.35)" }}>{title}</div>
      <div style={{ fontSize: 48, fontWeight: 600, marginTop: 10, opacity: sub2, transform: `translateY(${(1 - sub2) * 30}px)` }}>{sub}</div>
    </AbsoluteFill>
  );
};

// each scene drives its shader from the frame, never the clock (deterministic render)
const Scene: React.FC<{ children: (ms: number) => React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const punch = interpolate(frame, [0, 10], [1.12, 1], { extrapolateRight: "clamp" });
  return <AbsoluteFill style={{ transform: `scale(${punch})` }}>{children((frame / fps) * 1000)}</AbsoluteFill>;
};

export const Fondos: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#111" }}>
    <Sequence durationInFrames={60}>
      <Scene>{(ms) => (<>
        <Warp style={full} speed={0} frame={ms * 2} colors={["#7a0c0c", "#d7392b", "#f28c28", "#ffd166"]} shape="stripes" proportion={0.45} softness={1} distortion={0.25} swirl={0.8} swirlIterations={10} shapeScale={0.1} />
        <Label title="Salsa" sub="Warp · Paper Shaders" color="#fff6e8" />
      </>)}</Scene>
    </Sequence>
    <Sequence from={60} durationInFrames={60}>
      <Scene>{(ms) => (<>
        <Swirl style={full} speed={0} frame={ms * 2} colorBack="#1f3d12" colors={["#a6d608", "#f6e05e", "#4c9a2a"]} bandCount={4} twist={0.3} center={0.2} proportion={0.5} softness={0.4} noise={0.2} noiseFrequency={0.4} />
        <Label title="Cítrico" sub="Swirl · Paper Shaders" color="#fffbe6" />
      </>)}</Scene>
    </Sequence>
    <Sequence from={120} durationInFrames={60}>
      <Scene>{(ms) => (<>
        <Dithering style={full} speed={0} frame={ms * 2} colorBack="#2a1a12" colorFront="#f4b860" shape="sphere" type="4x4" size={3} />
        <Label title="Retro" sub="Dithering · Paper Shaders" color="#fff6e8" />
      </>)}</Scene>
    </Sequence>
  </AbsoluteFill>
);
