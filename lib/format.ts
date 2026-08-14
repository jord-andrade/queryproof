import type { Unit } from "./types";

export function formatMetric(value: number, unit: Unit): string {
  if (unit === "percent") return `${value.toFixed(1)}%`;
  if (unit === "minutes") return `${value.toFixed(1)} min`;
  if (unit === "score") return value.toFixed(2);
  return Math.round(value).toLocaleString("en-US");
}

export function scaleMetric(value: number, maximum: number): number {
  if (maximum <= 0) return 0;
  return Math.max(4, Math.min(100, (value / maximum) * 100));
}

export function shortHash(value: string): string {
  return value ? `${value.slice(0, 8)}…${value.slice(-6)}` : "unavailable";
}
