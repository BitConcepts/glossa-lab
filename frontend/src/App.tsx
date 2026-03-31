import { useEffect, useState } from "react";

interface HealthStatus {
  status: "healthy" | "degraded" | "down";
  version: string;
  uptime_seconds: number;
}

export function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await fetch("/api/v1/health");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data: HealthStatus = await res.json();
        setHealth(data);
        setError(null);
      } catch (err) {
        setHealth(null);
        setError(err instanceof Error ? err.message : "Connection failed");
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>Glossa Lab</h1>
      <p>
        Agentic research lab for decoding, translating, and modeling languages
        and scripts.
      </p>

      <h2>Backend Status</h2>
      {error ? (
        <p style={{ color: "#dc2626" }}>
          <strong>Disconnected:</strong> {error}
        </p>
      ) : health ? (
        <ul>
          <li>
            <strong>Status:</strong> {health.status}
          </li>
          <li>
            <strong>Version:</strong> {health.version}
          </li>
          <li>
            <strong>Uptime:</strong> {Math.round(health.uptime_seconds)}s
          </li>
        </ul>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
