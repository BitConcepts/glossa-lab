/**
 * Renders job results with type-specific visualizations:
 * - block_entropy  → EntropyChart + table
 * - decipher       → mapping table
 * - hypothesis     → comparison table
 * - logosyllabic   → sign classification table + candidate words
 * - char_freq      → frequency table
 * - default        → raw JSON
 */

import { EntropyChart } from "./EntropyChart";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AnyResult = Record<string, any>;

interface Props {
  result: AnyResult;
  jobName: string;
}

export function ResultsView({ result, jobName }: Props) {
  return (
    <div>
      <h3 style={{ marginBottom: "0.75rem" }}>{jobName}</h3>
      {renderResult(result)}
    </div>
  );
}

function renderResult(r: AnyResult) {
  if (r.block_entropies) return <BlockEntropyResult r={r} />;
  if (r.proposed_mapping) return <DecipherResult r={r} />;
  if (r.results && Array.isArray(r.results) && r.results[0]?.hypothesis)
    return <HypothesisResult r={r} />;
  if (r.sign_classification) return <LogosyllabicResult r={r} />;
  if (r.char_frequencies || r.frequencies) return <FreqResult r={r} />;
  return <JsonResult r={r} />;
}

// ── Block entropy ────────────────────────────────────────────────────

function BlockEntropyResult({ r }: { r: AnyResult }) {
  const entries: { n: number; normalized: number }[] = r.block_entropies || [];
  const series = [
    {
      label: r.text_name ?? "corpus",
      entries,
      color: "#2563eb",
    },
  ];

  return (
    <div>
      <p style={{ fontSize: 13, color: "#6b7280", marginTop: 0 }}>
        Corpus: <strong>{r.text_name}</strong> · {r.symbol_count} symbols ·
        alphabet {r.alphabet_size} · estimator:{" "}
        <code>{r.estimator ?? "mle"}</code>
      </p>
      <EntropyChart series={series} />
      <table style={tableStyle}>
        <thead>
          <tr>
            {["N", "H_N (nats)", "H_N / ln(L)"].map((h) => (
              <Th key={h}>{h}</Th>
            ))}
          </tr>
        </thead>
        <tbody>
          {entries.map((e) => (
            <tr key={e.n}>
              <Td>{e.n}</Td>
              <Td>{(r.block_entropies[e.n - 1]?.raw_nats ?? "—").toFixed?.(4) ?? "—"}</Td>
              <Td>{e.normalized.toFixed(4)}</Td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ── Decipher ─────────────────────────────────────────────────────────

function DecipherResult({ r }: { r: AnyResult }) {
  const mapping: Record<string, string> = r.proposed_mapping || {};
  const entries = Object.entries(mapping).slice(0, 60);

  return (
    <div>
      <p style={{ fontSize: 13, color: "#6b7280", marginTop: 0 }}>
        Score: <strong>{r.score}</strong> · Kandles confidence:{" "}
        <strong>{(r.kandles_confidence ?? 0).toFixed(3)}</strong> · Cipher
        alphabet: {r.cipher_alphabet_size}
      </p>
      <h4>Proposed Mapping</h4>
      <table style={tableStyle}>
        <thead>
          <tr>
            <Th>Cipher sign</Th>
            <Th>Proposed reading</Th>
          </tr>
        </thead>
        <tbody>
          {entries.map(([cipher, reading]) => (
            <tr key={cipher}>
              <Td>
                <code>{cipher}</code>
              </Td>
              <Td>
                <code>{reading}</code>
              </Td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ── Hypothesis ───────────────────────────────────────────────────────

function HypothesisResult({ r }: { r: AnyResult }) {
  const results: AnyResult[] = r.results || [];

  return (
    <div>
      <table style={tableStyle}>
        <thead>
          <tr>
            {["Hypothesis", "Total score", "Word matches", "Consistency", "Kandles"].map((h) => (
              <Th key={h}>{h}</Th>
            ))}
          </tr>
        </thead>
        <tbody>
          {results.map((res) => (
            <tr key={res.hypothesis}>
              <Td>
                <strong>{res.hypothesis}</strong>
              </Td>
              <Td>{res.total_score}</Td>
              <Td>{res.scores?.word_matches ?? "—"}</Td>
              <Td>{res.scores?.consistency?.toFixed(3) ?? "—"}</Td>
              <Td>{res.scores?.kandles?.toFixed(3) ?? "—"}</Td>
            </tr>
          ))}
        </tbody>
      </table>
      {results[0]?.suggestions && (
        <div style={{ marginTop: "0.75rem" }}>
          <strong>Suggestions:</strong>
          <ul style={{ marginTop: 4 }}>
            {results[0].suggestions.map((s: string, i: number) => (
              <li key={i} style={{ fontSize: 13 }}>
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// ── Logosyllabic ─────────────────────────────────────────────────────

function LogosyllabicResult({ r }: { r: AnyResult }) {
  const summary = r.summary || {};
  const classification: Record<string, AnyResult> = r.sign_classification || {};
  const words: AnyResult[] = (r.candidate_words || []).slice(0, 20);

  return (
    <div>
      <p style={{ fontSize: 13, color: "#6b7280", marginTop: 0 }}>
        Target: <strong>{r.target_language}</strong> · {r.sign_count} signs ·{" "}
        {r.unique_signs} unique · {r.inscription_count} inscriptions
      </p>
      <p style={{ fontSize: 13 }}>
        Logograms: <strong>{summary.logograms}</strong> · Syllabograms:{" "}
        <strong>{summary.syllabograms}</strong> · Determinatives:{" "}
        <strong>{summary.determinatives}</strong>
      </p>

      <h4>Sign Classification (top 30)</h4>
      <table style={tableStyle}>
        <thead>
          <tr>
            {["Sign", "Type", "Freq", "Boundary bias", "Evidence"].map((h) => (
              <Th key={h}>{h}</Th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Object.entries(classification)
            .sort((a, b) => b[1].frequency - a[1].frequency)
            .slice(0, 30)
            .map(([sign, info]) => (
              <tr key={sign}>
                <Td>
                  <code>{sign}</code>
                </Td>
                <Td>
                  <span
                    style={{
                      color:
                        info.type === "logogram"
                          ? "#7c3aed"
                          : info.type === "determinative"
                          ? "#d97706"
                          : "#2563eb",
                    }}
                  >
                    {info.type}
                  </span>
                </Td>
                <Td>{info.frequency}</Td>
                <Td>{info.boundary_bias.toFixed(2)}</Td>
                <Td style={{ fontSize: 12 }}>{info.evidence}</Td>
              </tr>
            ))}
        </tbody>
      </table>

      {words.length > 0 && (
        <>
          <h4>Candidate Word Readings</h4>
          <table style={tableStyle}>
            <thead>
              <tr>
                {["Signs", "Reading", "Confidence", "Vocab match"].map((h) => (
                  <Th key={h}>{h}</Th>
                ))}
              </tr>
            </thead>
            <tbody>
              {words.map((w, i) => (
                <tr key={i}>
                  <Td>
                    <code>{w.signs.join("-")}</code>
                  </Td>
                  <Td>
                    <strong>{w.combined_reading}</strong>
                  </Td>
                  <Td>{w.avg_confidence.toFixed(2)}</Td>
                  <Td>
                    {w.vocabulary_match ? (
                      <span style={{ color: "#16a34a" }}>
                        ✓ {w.meaning}
                      </span>
                    ) : (
                      <span style={{ color: "#9ca3af" }}>—</span>
                    )}
                  </Td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}

// ── Char frequency ────────────────────────────────────────────────────

function FreqResult({ r }: { r: AnyResult }) {
  const freqs: Record<string, number> = r.char_frequencies ?? r.frequencies ?? {};
  const sorted = Object.entries(freqs).sort((a, b) => b[1] - a[1]);

  return (
    <div>
      <table style={tableStyle}>
        <thead>
          <tr>
            <Th>Symbol</Th>
            <Th>Count</Th>
            <Th>Frequency</Th>
          </tr>
        </thead>
        <tbody>
          {sorted.slice(0, 40).map(([sym, cnt]) => {
            const total = sorted.reduce((s, [, c]) => s + c, 0);
            return (
              <tr key={sym}>
                <Td>
                  <code>{sym}</code>
                </Td>
                <Td>{cnt}</Td>
                <Td>{((cnt / total) * 100).toFixed(2)}%</Td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// ── Fallback: raw JSON ────────────────────────────────────────────────

function JsonResult({ r }: { r: AnyResult }) {
  return (
    <pre
      style={{
        background: "#f9fafb",
        border: "1px solid #e5e7eb",
        borderRadius: 4,
        padding: "0.75rem",
        fontSize: 12,
        overflowX: "auto",
        maxHeight: 400,
      }}
    >
      {JSON.stringify(r, null, 2)}
    </pre>
  );
}

// ── Shared table helpers ──────────────────────────────────────────────

const tableStyle: React.CSSProperties = {
  borderCollapse: "collapse",
  width: "100%",
  maxWidth: 760,
  marginTop: "0.5rem",
};

function Th({ children }: { children: React.ReactNode }) {
  return (
    <th
      style={{
        textAlign: "left",
        padding: "4px 12px 4px 0",
        borderBottom: "2px solid #e5e7eb",
        fontSize: 12,
        color: "#374151",
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </th>
  );
}

function Td({
  children,
  style,
}: {
  children: React.ReactNode;
  style?: React.CSSProperties;
}) {
  return (
    <td
      style={{
        padding: "4px 12px 4px 0",
        borderBottom: "1px solid #f3f4f6",
        fontSize: 12,
        verticalAlign: "top",
        ...style,
      }}
    >
      {children}
    </td>
  );
}
