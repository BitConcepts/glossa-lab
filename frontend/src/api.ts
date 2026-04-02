/**
 * Typed API client for Glossa Lab backend.
 * All functions return typed results or throw on HTTP error.
 */

const BASE = "/api/v1";

async function request<T>(
  method: string,
  path: string,
  body?: unknown
): Promise<T> {
  const opts: RequestInit = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`${method} ${path} → HTTP ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// ── Types ─────────────────────────────────────────────────────────────

export interface HealthResponse {
  status: "healthy" | "degraded" | "down";
  version: string;
  uptime_seconds: number;
}

export interface StatusResponse {
  status: string;
  job_counts: Record<string, number>;
  pipelines: string[];
}

export interface TextCreate {
  name: string;
  corpus_type?: string;
  content: string[];
  metadata?: Record<string, unknown>;
}

export interface TextResponse {
  id: string;
  name: string;
  corpus_type: string;
  content: string[];
  alphabet_size: number;
  symbol_set: string[];
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface JobCreate {
  name: string;
  pipeline: string;
  params?: Record<string, unknown>;
}

export interface JobResponse {
  id: string;
  name: string;
  pipeline: string;
  status: "pending" | "running" | "completed" | "failed" | string;
  params: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

// ── Health & Status ───────────────────────────────────────────────────

export const getHealth = (): Promise<HealthResponse> =>
  request("GET", "/health");

export const getStatus = (): Promise<StatusResponse> =>
  request("GET", "/status");

// ── Texts ─────────────────────────────────────────────────────────────

export const listTexts = (): Promise<TextResponse[]> =>
  request("GET", "/texts");

export const getText = (id: string): Promise<TextResponse> =>
  request("GET", `/texts/${id}`);

export const createText = (body: TextCreate): Promise<TextResponse> =>
  request("POST", "/texts", body);

// ── Jobs ──────────────────────────────────────────────────────────────

export const listJobs = (): Promise<JobResponse[]> =>
  request("GET", "/jobs");

export const getJob = (id: string): Promise<JobResponse> =>
  request("GET", `/jobs/${id}`);

export const createJob = (body: JobCreate): Promise<JobResponse> =>
  request("POST", "/jobs", body);

export const cancelJob = (id: string): Promise<JobResponse> =>
  request("DELETE", `/jobs/${id}`);

// ── Results ───────────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getJobResults = (jobId: string): Promise<Record<string, any>> =>
  request("GET", `/jobs/${jobId}/results`);
