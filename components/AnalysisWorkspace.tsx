"use client";

import { FormEvent, useState } from "react";
import { shortHash } from "@/lib/format";
import type { AnalysisResult } from "@/lib/types";
import { ResultChart } from "./ResultChart";

const examples = [
  "Which queue receives the most tickets?",
  "How has CSAT changed week over week?",
  "What is first-contact resolution by queue?",
  "Which category has the highest escalation rate?",
  "Which queue takes the longest to resolve?",
  "How are contacts split by channel?",
];

export function AnalysisWorkspace() {
  const [question, setQuestion] = useState(examples[0]);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [error, setError] = useState("");

  async function runAnalysis(event?: FormEvent) {
    event?.preventDefault();
    if (question.trim().length < 6) return;

    setStatus("loading");
    setError("");
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question: question.trim() }),
      });
      if (!response.ok) throw new Error(`Analysis returned ${response.status}`);
      setResult((await response.json()) as AnalysisResult);
      setStatus("idle");
    } catch {
      setError("The analysis service is unavailable. Try again in a moment.");
      setStatus("error");
    }
  }

  function chooseExample(example: string) {
    setQuestion(example);
    setResult(null);
    setStatus("idle");
    setError("");
  }

  return (
    <section className="workspace" aria-labelledby="workspace-title">
      <div className="workspace-input">
        <div className="workspace-label">
          <span>Interactive proof</span>
          <span className="live-pill"><i /> deterministic</span>
        </div>
        <h2 id="workspace-title">Ask the dataset.</h2>
        <p>
          The demo maps your question to one approved analytical intent. It never
          executes user-authored SQL.
        </p>

        <form onSubmit={runAnalysis}>
          <label htmlFor="question">Question</label>
          <textarea
            id="question"
            maxLength={300}
            onChange={(event) => setQuestion(event.target.value)}
            rows={4}
            value={question}
          />
          <div className="input-footer">
            <span>{question.length}/300</span>
            <button disabled={status === "loading" || question.trim().length < 6} type="submit">
              {status === "loading" ? "Running…" : "Run analysis"}
              <b aria-hidden="true">↗</b>
            </button>
          </div>
        </form>

        <div className="examples" aria-label="Example questions">
          <span>Try an evaluated question</span>
          {examples.map((example) => (
            <button key={example} onClick={() => chooseExample(example)} type="button">
              {example}
            </button>
          ))}
        </div>
      </div>

      <div className="workspace-output" aria-live="polite">
        {status === "loading" ? (
          <div className="empty-state loading-state">
            <span className="loader" />
            <h3>Executing the evidence path</h3>
            <p>Classify → query → verify → explain</p>
          </div>
        ) : null}
        {status === "error" ? (
          <div className="empty-state error-state">
            <span>Service error</span>
            <h3>{error}</h3>
          </div>
        ) : null}
        {status === "idle" && !result ? (
          <div className="empty-state">
            <div className="empty-diagram" aria-hidden="true">
              <span>?</span><i /><b>SQL</b><i /><strong>✓</strong>
            </div>
            <h3>No hidden reasoning.</h3>
            <p>Run an analysis to inspect the answer, query, source and execution trail.</p>
          </div>
        ) : null}
        {status === "idle" && result ? (
          <div className="result-stack">
            <section className={`answer-card ${result.supported ? "" : "unsupported"}`}>
              <div className="panel-heading">
                <div>
                  <span className="panel-index">01</span>
                  <h3>{result.supported ? "Measured answer" : "Guardrail triggered"}</h3>
                </div>
                <span>{result.evidence.query_id}</span>
              </div>
              <p className="answer">{result.answer}</p>
              <p className="explanation">{result.explanation}</p>
            </section>

            {result.chart.length ? (
              <ResultChart points={result.chart} title={result.chart_title} unit={result.unit} />
            ) : null}

            <section className="sql-card">
              <div className="panel-heading">
                <div>
                  <span className="panel-index">03</span>
                  <h3>Executed SQL</h3>
                </div>
                <span>read only</span>
              </div>
              <pre><code>{result.sql}</code></pre>
            </section>

            <section className="evidence-card">
              <div className="panel-heading">
                <div>
                  <span className="panel-index">04</span>
                  <h3>Evidence packet</h3>
                </div>
                <span>reproducible</span>
              </div>
              <dl>
                <div><dt>Source</dt><dd>{result.evidence.source}</dd></div>
                <div><dt>Dataset hash</dt><dd>{shortHash(result.evidence.dataset_sha256)}</dd></div>
                <div><dt>Rows scanned</dt><dd>{result.evidence.rows_scanned}</dd></div>
                <div><dt>Rows returned</dt><dd>{result.evidence.rows_returned}</dd></div>
              </dl>
              <ol className="trace-list">
                {result.trace.map((step, index) => (
                  <li className={step.status} key={step.label}>
                    <span>{String(index + 1).padStart(2, "0")}</span>
                    <div><strong>{step.label}</strong><p>{step.detail}</p></div>
                  </li>
                ))}
              </ol>
            </section>
          </div>
        ) : null}
      </div>
    </section>
  );
}
