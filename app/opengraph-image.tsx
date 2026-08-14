import { ImageResponse } from "next/og";

export const alt = "QueryProof — Ask a question. Audit every number.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpenGraphImage() {
  return new ImageResponse(
    <div style={{ background: "#07130e", color: "#eef7f1", display: "flex", flexDirection: "column", fontFamily: "Arial, sans-serif", height: "100%", justifyContent: "space-between", padding: "64px 72px", position: "relative", width: "100%" }}>
      <div style={{ border: "1px solid rgba(140,255,203,.35)", display: "flex", height: 470, position: "absolute", right: 72, top: 82, width: 320 }} />
      <div style={{ background: "#8cffcb", display: "flex", height: 210, position: "absolute", right: 128, top: 155, width: 210 }} />
      <div style={{ color: "#07130e", display: "flex", fontFamily: "monospace", fontSize: 60, fontWeight: 800, position: "absolute", right: 181, top: 224 }}>QP</div>
      <div style={{ display: "flex", fontFamily: "monospace", fontSize: 22, justifyContent: "space-between", letterSpacing: 3, width: "100%" }}><span style={{ color: "#8cffcb" }}>QUERYPROOF</span><span style={{ marginRight: 360 }}>EVIDENCE / 2026</span></div>
      <div style={{ display: "flex", flexDirection: "column", fontSize: 72, fontWeight: 700, letterSpacing: -3, lineHeight: 1.02, maxWidth: 720 }}><span>ASK A QUESTION.</span><span style={{ color: "#8cffcb" }}>AUDIT EVERY NUMBER.</span></div>
      <div style={{ borderTop: "1px solid rgba(238,247,241,.45)", display: "flex", fontFamily: "monospace", fontSize: 20, justifyContent: "space-between", letterSpacing: 2, paddingTop: 24, width: "100%" }}><span>FASTAPI · DUCKDB · NEXT.JS</span><span style={{ color: "#8cffcb" }}>SYNTHETIC DATA</span></div>
    </div>,
    size,
  );
}
