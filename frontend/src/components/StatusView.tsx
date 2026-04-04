import { useEffect, useState } from "react";
import {
  getHealth,
  getStatus,
  getCatalog,
  HealthResponse,
  StatusResponse,
  CatalogResponse,
} from "../api";

export function StatusView() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [status, setStatus] = useState<StatusResponse | null>(null);
  const [catalog, setCatalog] = useState<CatalogResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    try {
      const [h, s] = await Promise.all([getHealth(), getStatus()]);
      setHealth(h);
      setStatus(s);
      setError(null);
      getCatalog().then(setCatalog).catch(() => {});
    } catch (e) {
      setError(e instanceof Error ? e.message : "Connection failed");
    }
  };

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 5000);
    return () => clearInterval(id);
  }, []);

  const dot = (ok: boolean) => (
    <span
      style={{
        display: "inline-block",
        width: 10,
        height: 10,
        borderRadius: "50%",
        background: ok ? "#16a34a" : "#dc2626",
        marginRight: 6,
      }}
    />
  );

  if (error) {
    return (
      <div>
        <h2>System Status</h2>
        <p style={{ color: "#dc2626" }}>
          {dot(false)} Disconnected: {error}
        </p>
      </div>
    );
  }

  if (!health) return <p>Loading…</p>;

  const healthy = health.status === "healthy";

  return (
    <div>
      <h2>System Status</h2>
      <table style={{ borderCollapse: "collapse", minWidth: 360 }}>
        <tbody>
          <tr>
            <Td>Backend</Td>
            <Td>
              {dot(healthy)}
              {health.status}
            </Td>
          </tr>
          <tr>
            <Td>Version</Td>
            <Td>{health.version}</Td>
          </tr>
          <tr>
            <Td>Uptime</Td>
            <Td>{Math.round(health.uptime_seconds)}s</Td>
          </tr>
          {status && (
            <>
          <tr>
                <Td>Pipelines</Td>
                <Td>{status.pipeline_count ?? status.pipelines?.length ?? "—"} registered</Td>
              </tr>
              {catalog && Object.entries(catalog.counts).map(([k, v]) => (
                <tr key={k}>
                  <Td>Catalog ({k})</Td>
                  <Td>{v}</Td>
                </tr>
              ))}
              {Object.entries(status.jobs ?? status.job_counts ?? {}).map(([k, v]) => (
                <tr key={k}>
                  <Td>Jobs ({k})</Td>
                  <Td>{v}</Td>
                </tr>
              ))}
            </>
          )}
        </tbody>
      </table>

      {status?.pipelines && status.pipelines.length > 0 && (
        <>
          <h3>Registered Pipelines</h3>
          <ul style={{ columnCount: 2, paddingLeft: "1.2rem" }}>
            {status.pipelines.map((p) => (
              <li key={p} style={{ fontFamily: "monospace" }}>
                {p}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

function Td({ children }: { children: React.ReactNode }) {
  return (
    <td
      style={{
        padding: "4px 16px 4px 0",
        verticalAlign: "top",
        borderBottom: "1px solid #e5e7eb",
      }}
    >
      {children}
    </td>
  );
}
