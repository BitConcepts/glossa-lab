/**
 * Pure-SVG line chart for block entropy curves.
 * Renders H_n (normalized) vs n for one or more corpora.
 */

interface EntropyEntry {
  n: number;
  normalized: number;
}

interface Series {
  label: string;
  entries: EntropyEntry[];
  color: string;
}

interface Props {
  series: Series[];
  width?: number;
  height?: number;
}

const MARGIN = { top: 20, right: 20, bottom: 40, left: 50 };
const COLORS = [
  "#2563eb", "#16a34a", "#dc2626", "#d97706", "#7c3aed",
  "#db2777", "#0891b2", "#65a30d",
];

export function EntropyChart({ series, width = 540, height = 300 }: Props) {
  if (!series || series.length === 0) return null;

  const innerW = width - MARGIN.left - MARGIN.right;
  const innerH = height - MARGIN.top - MARGIN.bottom;

  // Determine x domain from max n
  const maxN = Math.max(...series.flatMap((s) => s.entries.map((e) => e.n)));
  const minN = 1;

  // y domain 0 .. 1 (normalized entropy)
  const xScale = (n: number) =>
    ((n - minN) / Math.max(maxN - minN, 1)) * innerW;
  const yScale = (v: number) => innerH - v * innerH;

  const yTicks = [0, 0.25, 0.5, 0.75, 1.0];
  const xTicks = Array.from({ length: maxN }, (_, i) => i + 1);

  return (
    <svg width={width} height={height} style={{ overflow: "visible" }}>
      <g transform={`translate(${MARGIN.left},${MARGIN.top})`}>
        {/* Grid lines */}
        {yTicks.map((t) => (
          <line
            key={t}
            x1={0}
            x2={innerW}
            y1={yScale(t)}
            y2={yScale(t)}
            stroke="#e5e7eb"
            strokeWidth={1}
          />
        ))}

        {/* Y axis */}
        <line x1={0} x2={0} y1={0} y2={innerH} stroke="#6b7280" strokeWidth={1} />
        {yTicks.map((t) => (
          <g key={t} transform={`translate(0,${yScale(t)})`}>
            <line x1={-4} x2={0} stroke="#6b7280" />
            <text x={-8} dy="0.35em" textAnchor="end" fontSize={11} fill="#6b7280">
              {t.toFixed(2)}
            </text>
          </g>
        ))}
        <text
          transform={`rotate(-90) translate(${-innerH / 2},${-36})`}
          textAnchor="middle"
          fontSize={12}
          fill="#374151"
        >
          H_n / ln(L)
        </text>

        {/* X axis */}
        <line x1={0} x2={innerW} y1={innerH} y2={innerH} stroke="#6b7280" strokeWidth={1} />
        {xTicks.map((n) => (
          <g key={n} transform={`translate(${xScale(n)},${innerH})`}>
            <line y1={0} y2={4} stroke="#6b7280" />
            <text dy="1.2em" textAnchor="middle" fontSize={11} fill="#6b7280">
              {n}
            </text>
          </g>
        ))}
        <text
          x={innerW / 2}
          y={innerH + 32}
          textAnchor="middle"
          fontSize={12}
          fill="#374151"
        >
          Block size N
        </text>

        {/* Series lines */}
        {series.map((s, si) => {
          const color = s.color || COLORS[si % COLORS.length];
          const sorted = [...s.entries].sort((a, b) => a.n - b.n);
          const d = sorted
            .map((e, i) => {
              const x = xScale(e.n);
              const y = yScale(Math.min(1, Math.max(0, e.normalized)));
              return `${i === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`;
            })
            .join(" ");
          return (
            <g key={si}>
              <path d={d} fill="none" stroke={color} strokeWidth={2} />
              {sorted.map((e) => (
                <circle
                  key={e.n}
                  cx={xScale(e.n)}
                  cy={yScale(Math.min(1, Math.max(0, e.normalized)))}
                  r={3}
                  fill={color}
                />
              ))}
            </g>
          );
        })}
      </g>

      {/* Legend */}
      <g transform={`translate(${MARGIN.left + innerW - 10},${MARGIN.top})`}>
        {series.map((s, si) => {
          const color = s.color || COLORS[si % COLORS.length];
          return (
            <g key={si} transform={`translate(0,${si * 18})`}>
              <line x1={-30} x2={-10} y1={6} y2={6} stroke={color} strokeWidth={2} />
              <circle cx={-20} cy={6} r={3} fill={color} />
              <text fontSize={11} fill="#374151" dominantBaseline="middle" dy={6}>
                {s.label}
              </text>
            </g>
          );
        })}
      </g>
    </svg>
  );
}
