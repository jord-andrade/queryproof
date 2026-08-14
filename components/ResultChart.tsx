import { formatMetric, scaleMetric } from "@/lib/format";
import type { ChartPoint, Unit } from "@/lib/types";

type ResultChartProps = {
  points: ChartPoint[];
  title: string;
  unit: Unit;
};

export function ResultChart({ points, title, unit }: ResultChartProps) {
  const maximum = Math.max(...points.map((point) => point.value), 0);

  return (
    <section className="chart-card" aria-labelledby="chart-title">
      <div className="panel-heading">
        <div>
          <span className="panel-index">02</span>
          <h3 id="chart-title">{title}</h3>
        </div>
        <span>{points.length} rows</span>
      </div>
      <ol className="bar-chart">
        {points.map((point) => (
          <li key={point.label}>
            <div className="bar-meta">
              <span>{point.label}</span>
              <strong>{formatMetric(point.value, unit)}</strong>
            </div>
            <div className="bar-track" aria-hidden="true">
              <span style={{ width: `${scaleMetric(point.value, maximum)}%` }} />
            </div>
            {point.secondary !== null ? (
              <small>
                {unit === "count"
                  ? `${point.secondary.toFixed(1)}% of rows`
                  : `${Math.round(point.secondary)} observations`}
              </small>
            ) : null}
          </li>
        ))}
      </ol>
    </section>
  );
}
