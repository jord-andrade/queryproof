import { ImageResponse } from "next/og";

export const size = { width: 64, height: 64 };
export const contentType = "image/png";

export default function Icon() {
  return new ImageResponse(
    <div style={{ alignItems: "center", background: "#8cffcb", color: "#07130e", display: "flex", fontFamily: "monospace", fontSize: 24, fontWeight: 700, height: "100%", justifyContent: "center", width: "100%" }}>QP</div>,
    size,
  );
}
