export type Unit = "count" | "percent" | "minutes" | "score";

export type ChartPoint = {
  label: string;
  value: number;
  secondary: number | null;
};

export type TraceStep = {
  label: string;
  detail: string;
  status: "complete" | "blocked";
};

export type AnalysisResult = {
  supported: boolean;
  intent: string;
  answer: string;
  explanation: string;
  chart_title: string;
  unit: Unit;
  chart: ChartPoint[];
  sql: string;
  evidence: {
    source: string;
    dataset_sha256: string;
    rows_scanned: number;
    rows_returned: number;
    query_id: string;
  };
  trace: TraceStep[];
};
