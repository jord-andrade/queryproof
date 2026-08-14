import { AnalysisWorkspace } from "@/components/AnalysisWorkspace";

const principles = [
  ["01", "Allowlisted execution", "Questions map to six reviewed SQL queries. User text never becomes executable code."],
  ["02", "Synthetic by construction", "A seeded generator produces the complete public dataset without names, emails or customer records."],
  ["03", "Evidence in the response", "Every answer includes SQL, source hash, row counts, chart values and a trace of completed steps."],
  ["04", "Failure stays visible", "Unsupported questions stop before execution instead of receiving a plausible invented answer."],
];

export default function Home() {
  return (
    <main>
      <header className="site-header">
        <a className="brand" href="#top" aria-label="QueryProof home">
          <span>QP</span> QueryProof
        </a>
        <nav aria-label="Primary navigation">
          <a href="#demo">Demo</a>
          <a href="#method">Method</a>
          <a href="https://github.com/jord-andrade/queryproof">Source ↗</a>
        </nav>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow"><span /> Traceable analytics · synthetic data</p>
          <h1>Ask a question.<br /><em>Audit every number.</em></h1>
          <p className="hero-summary">
            QueryProof turns a natural-language question into an approved SQL query,
            runs it against a reproducible dataset and returns the evidence beside the answer.
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="#demo">Open the demo <span>↓</span></a>
            <a className="secondary-action" href="/api/docs">Inspect the API <span>↗</span></a>
          </div>
        </div>
        <div className="hero-system" aria-label="Evidence workflow">
          <div className="system-header"><span>RUN / 001</span><span>DETERMINISTIC</span></div>
          <div className="system-question">Which queue receives the most tickets?</div>
          <ol>
            <li><span>01</span><p>intent</p><strong>ticket_volume_by_queue</strong><b>✓</b></li>
            <li><span>02</span><p>source</p><strong>synthetic · 960 rows</strong><b>✓</b></li>
            <li><span>03</span><p>runtime</p><strong>DuckDB · read only</strong><b>✓</b></li>
            <li><span>04</span><p>evidence</p><strong>SQL + hash + rows</strong><b>✓</b></li>
          </ol>
          <div className="system-result"><span>ANSWER STATUS</span><strong>SUPPORTED</strong></div>
        </div>
      </section>

      <div className="proof-strip" aria-label="System properties">
        <span>NO USER SQL</span><i />
        <span>SEED 42</span><i />
        <span>24 EVALUATION CASES</span><i />
        <span>ZERO PRIVATE RECORDS</span>
      </div>

      <section className="demo-section" id="demo">
        <div className="section-heading">
          <p>01 / Interactive demonstration</p>
          <h2>One answer. The whole path.</h2>
          <span>Every output can be checked without trusting a hidden chain of thought.</span>
        </div>
        <AnalysisWorkspace />
      </section>

      <section className="method-section" id="method">
        <div className="section-heading light">
          <p>02 / Trust model</p>
          <h2>Constrained on purpose.</h2>
          <span>The public demo optimizes for reproducibility, cost control and honest failure.</span>
        </div>
        <div className="principles-grid">
          {principles.map(([number, title, description]) => (
            <article key={number}>
              <span>{number}</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>

      <footer>
        <a className="brand" href="#top"><span>QP</span> QueryProof</a>
        <p>Built by <a href="https://jord-andrade.dev">Jordan Andrade ↗</a></p>
        <p>FastAPI · DuckDB · Next.js</p>
      </footer>
    </main>
  );
}
