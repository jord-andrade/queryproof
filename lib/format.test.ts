import { describe, expect, it } from "vitest";
import { formatMetric, scaleMetric, shortHash } from "./format";

describe("formatMetric", () => {
  it("formats analytical units without hiding precision", () => {
    expect(formatMetric(72.36, "percent")).toBe("72.4%");
    expect(formatMetric(31.25, "minutes")).toBe("31.3 min");
    expect(formatMetric(4.126, "score")).toBe("4.13");
    expect(formatMetric(1234, "count")).toBe("1,234");
  });
});

describe("chart helpers", () => {
  it("keeps visible bars within safe bounds", () => {
    expect(scaleMetric(0, 0)).toBe(0);
    expect(scaleMetric(1, 100)).toBe(4);
    expect(scaleMetric(200, 100)).toBe(100);
  });

  it("shortens evidence hashes while preserving both ends", () => {
    expect(shortHash("1234567890abcdef")).toBe("12345678…abcdef");
  });
});
