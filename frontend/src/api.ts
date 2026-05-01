/**
 * Typed API client for Glossa Lab backend.
 * All functions return typed results or throw on HTTP error.
 */

const BASE = "/api/v1";

async function request<T>(
  method: string,
  path: string,
  body?: unknown,
  signal?: AbortSignal,
): Promise<T> {
  const opts: RequestInit = {
    method,
    headers: { "Content-Type": "application/json" },
    signal,
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
  jobs: Record<string, number>;
  job_counts: Record<string, number>;
  pipelines: string[];
  pipeline_count: number;
  catalog_counts: Record<string, number>;
  ollama_installed?: boolean;
  ollama_running?: boolean;
}

export interface CatalogPipeline {
  id: string;
  label: string;
  group: string;
  description: string;
  inputs: string;
  outputs: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  default_params: Record<string, any>;
  needs_lm: boolean;
  registered: boolean;
  module: string;
}

export interface ModelDetail {
  id: string;
  description: string;
  use_for: string;
}

export interface CatalogProvider {
  id: string;
  label: string;
  api_key_setting: string;
  supports_live_model_discovery: boolean;
  recommended_models: string[];
  model_details: ModelDetail[];
  ocr_preferred_models: string[];
}

export interface CatalogReport {
  id: string;
  name: string;
  kind: string;
  relative_path: string;
  size_bytes: number;
  updated_at: string;
  experiment_id: string;  // set when this report is produced by a known experiment
}

export interface CatalogExperiment {
  id: string;
  name: string;
  category: string;
  description: string;
  command: string;
  results_file?: string;
  requires_key?: string;
  estimated_time: string;
}

export interface CatalogResponse {
  counts: Record<string, number>;
  pipelines: CatalogPipeline[];
  experiments: CatalogExperiment[];
  reports: CatalogReport[];
  providers: CatalogProvider[];
}

export interface TextCreate {
  name: string;
  corpus_type?: string;
  content: string[];
  metadata?: Record<string, unknown>;
  reading_direction?: string;
}

export interface TextResponse {
  id: string;
  name: string;
  corpus_type: string;
  content: string[];
  alphabet_size: number;
  symbol_set: string[];
  metadata: Record<string, unknown>;
  reading_direction: string;
  created_at: string;
}

export interface DetectDirectionResult {
  text_id: string;
  word_source: string;
  entropy_pos0: number | null;
  entropy_posN1: number | null;
  gini_pos0: number | null;
  gini_posN1: number | null;
  inferred_direction: "ltr" | "rtl" | "unknown";
  confidence: "high" | "medium" | "low";
  n_words: number;
  interpretation: string;
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

// ── Experiment Graph types ───────────────────────────────────────────

export interface AtomicPort {
  name: string;
  type: string;       // "sequences" | "freq_map" | "profiles" | "clusters" | "number" | "text" | "json" | "any"
  required?: boolean;
}

export interface AtomicNodeDef {
  id: string;
  name: string;
  category: string;
  description: string;
  inputs: AtomicPort[];
  outputs: AtomicPort[];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  params_schema: Record<string, any>;
}

export interface GraphExperiment {
  id?: string;
  name: string;
  description: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  nodes: Record<string, any>[];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  edges: Record<string, any>[];
}

export interface GraphExperimentMeta {
  id: string;
  name: string;
  description: string;
  node_count: number;
  edge_count: number;
}

// Port type → hex colour (mirrors backend PORT_COLORS)
export const PORT_COLORS: Record<string, string> = {
  sequences: "#059669",
  freq_map:  "#2563eb",
  profiles:  "#7c3aed",
  clusters:  "#d97706",
  number:    "#dc2626",
  text:      "#0d9488",
  json:      "#4f46e5",
  any:       "#64748b",
};

export const getAtomicNodeCatalog = (): Promise<AtomicNodeDef[]> =>
  request("GET", "/experiment-graphs/catalog");

export const listGraphExperiments = (): Promise<GraphExperimentMeta[]> =>
  request("GET", "/experiment-graphs");

export const getGraphExperiment = (id: string): Promise<GraphExperiment> =>
  request("GET", `/experiment-graphs/${id}`);

export const createGraphExperiment = (body: GraphExperiment): Promise<GraphExperiment> =>
  request("POST", "/experiment-graphs", body);

export const updateGraphExperiment = (id: string, body: GraphExperiment): Promise<GraphExperiment> =>
  request("PUT", `/experiment-graphs/${id}`, body);

export const deleteGraphExperiment = (id: string): Promise<{ deleted: boolean }> =>
  request("DELETE", `/experiment-graphs/${id}`);

export const runGraphExperiment = (
  id: string,
  kwargs: Record<string, unknown> = {},
  notify = false,
// eslint-disable-next-line @typescript-eslint/no-explicit-any
): Promise<{ status: string; result: Record<string, any> }> =>
  request("POST", `/experiment-graphs/${id}/run`, { kwargs, notify });

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

export const updateText = (id: string, body: Partial<TextCreate>): Promise<TextResponse> =>
  request("PUT", `/texts/${id}`, body);

export const deleteText = (id: string): Promise<TextResponse> =>
  request("DELETE", `/texts/${id}`);

export const detectCorpusDirection = (
  id: string,
  words?: string[][],
  updateField = true,
): Promise<DetectDirectionResult> =>
  request("POST", `/texts/${id}/detect-direction`, {
    words: words ?? null,
    update_field: updateField,
  });

// ── Jobs ──────────────────────────────────────────────────────────────

export const listJobs = (): Promise<JobResponse[]> =>
  request("GET", "/jobs");

export const getJob = (id: string): Promise<JobResponse> =>
  request("GET", `/jobs/${id}`);

export const createJob = (body: JobCreate): Promise<JobResponse> =>
  request("POST", "/jobs", body);

export const cancelJob = (id: string): Promise<JobResponse> =>
  request("DELETE", `/jobs/${id}`);

export const clearJobs = (finishedOnly = false): Promise<{ cleared: number }> =>
  request("DELETE", finishedOnly ? "/jobs?finished_only=true" : "/jobs");

// ── Results ───────────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getJobResults = (jobId: string): Promise<Record<string, any>> =>
  request("GET", `/jobs/${jobId}/results`);

// ── Settings ──────────────────────────────────────────────────────────

export interface KeyStatus {
  set: boolean;
  source: "env" | "stored" | null;
  masked: string;
}

export interface SettingsResponse {
  keys: Record<string, KeyStatus>;
  data_dir: string;
}

// Keys that are stored client-side in localStorage (never sent as plaintext to server display)
const LS_KEY = "glossa_lab_api_keys";

export function getLocalKeys(): Record<string, string> {
  try { return JSON.parse(localStorage.getItem(LS_KEY) ?? "{}"); }
  catch { return {}; }
}

export function setLocalKey(name: string, value: string): void {
  const existing = getLocalKeys();
  if (value) existing[name] = value;
  else delete existing[name];
  localStorage.setItem(LS_KEY, JSON.stringify(existing));
}

export function clearLocalKey(name: string): void {
  setLocalKey(name, "");
}

export function isLocalKeySet(name: string): boolean {
  return Boolean(getLocalKeys()[name]);
}

// Also persists to backend for terminal scripts (ocr_mahadevan.py, etc.)
export const getSettings = (): Promise<SettingsResponse> =>
  request("GET", "/settings");

export interface VerifyKeyResult {
  valid: boolean;
  provider: string;
  message: string;
}

export const verifyKey = (
  keyName: string,
  keyValue?: string
): Promise<VerifyKeyResult> =>
  request("POST", "/settings/verify-key", { key_name: keyName, key_value: keyValue ?? null });

export const updateSettings = (
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  body: Record<string, any>
): Promise<{ updated: string[]; updated_providers: string[]; message: string }> =>
  request("PUT", "/settings", body);

// ── Catalog ───────────────────────────────────────────────────────────

export const getCatalog = (): Promise<CatalogResponse> =>
  request("GET", "/catalog");

export const getPipelineCatalog = (): Promise<CatalogPipeline[]> =>
  request("GET", "/catalog/pipelines");

export const getProviderCatalog = (): Promise<CatalogProvider[]> =>
  request("GET", "/catalog/providers");

export const getReportCatalog = (): Promise<CatalogReport[]> =>
  request("GET", "/catalog/reports");

// ── Reports ───────────────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getReport = (name: string): Promise<Record<string, any>> =>
  request("GET", `/reports/${name}`);

export const listReports = (): Promise<CatalogReport[]> =>
  request("GET", "/reports");

export const deleteReport = (name: string): Promise<{ deleted: boolean; relative_path: string }> =>
  request("DELETE", `/reports/${name}`);

export const getReportDownloadUrl = (name: string): string =>
  `/api/v1/reports/${name}/download`;

export interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  requires: string[];
  ready: boolean;  // true if all required input JSONs exist
}

export interface GenerateReportResult {
  started: boolean;
  job_id: string | null;
  template_id: string;
  template_name: string;
  message: string;
}

export const listReportTemplates = (): Promise<ReportTemplate[]> =>
  request("GET", "/reports/templates");

export const generateReport = (template_id: string): Promise<GenerateReportResult> =>
  request("POST", "/reports/generate", { template_id });

export const openReportFolder = (name: string): Promise<{ opened: boolean; folder: string }> =>
  request("POST", `/reports/${name}/open-folder`);

// ── Pipelines (CRUD additions) ───────────────────────────────────────────

export const duplicatePipeline = (
  id: string,
  newId?: string
// eslint-disable-next-line @typescript-eslint/no-explicit-any
): Promise<Record<string, any>> =>
  request("POST", `/pipelines/${id}/duplicate`, { new_id: newId });

export const deletePipeline = (
  id: string
): Promise<{ deleted: boolean; file: string }> =>
  request("DELETE", `/pipelines/${id}`);

export const importPipeline = (
  sourcePath: string
// eslint-disable-next-line @typescript-eslint/no-explicit-any
): Promise<Record<string, any>> =>
  request("POST", "/pipelines/import", { source_path: sourcePath });

// ── Studies ─────────────────────────────────────────────────────────────────

export type StudyNodeType =
  | "experiment" | "pipeline" | "corpus"
  | "rag_query" | "ai_analysis" | "compare"
  | "note" | "report" | "hypothesis";

export interface StudyNode {
  id: string;
  type: StudyNodeType;
  ref_id: string;       // experiment / pipeline id; empty for corpus/note/rag/ai/report/hypothesis
  label: string;
  params: Record<string, unknown>;
  note_text?: string;   // text content for note nodes
  color?: string;       // optional custom hex color override
  position: { x: number; y: number };
}

export interface StudyEdge {
  id: string;
  source: string;
  target: string;
}

export interface StudyGraph {
  nodes: StudyNode[];
  edges: StudyEdge[];
}

export interface StudyResponse {
  id: string;
  name: string;
  description: string;
  graph: StudyGraph;
  created_at: string;
  updated_at: string;
}

export const listStudies = (): Promise<StudyResponse[]> =>
  request("GET", "/studies");

export const getStudy = (id: string): Promise<StudyResponse> =>
  request("GET", `/studies/${id}`);

export const createStudy = (body: {
  name: string;
  description?: string;
  graph?: StudyGraph;
}): Promise<StudyResponse> =>
  request("POST", "/studies", body);

export const updateStudy = (
  id: string,
  body: { name?: string; description?: string; graph?: StudyGraph }
): Promise<StudyResponse> =>
  request("PUT", `/studies/${id}`, body);

export const deleteStudy = (id: string): Promise<{ deleted: boolean }> =>
  request("DELETE", `/studies/${id}`);

export type NodeRunStatus = "idle" | "running" | "complete" | "error" | "skipped" | "annotation" | "corpus" | "pending";

export interface StudyRunResult {
  study_id: string;
  node_count: number;
  completed: number;
  skipped: number;
  annotations: number;
  errors: number;
  job_id?: string | null;
  results: Record<string, {
    status: NodeRunStatus;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    result?: Record<string, any>;
    reason?: string;
    job_id?: string;
  }>;
}

/** SSE events emitted during a streaming study run. */
export interface StudyRunEvent {
  event: "started" | "node_start" | "node_end" | "run_complete" | "run_error";
  // started
  study_id?: string;
  study_name?: string;
  node_count?: number;
  job_id?: string | null;
  // node_start / node_end
  nid?: string;
  label?: string;
  type?: string;
  idx?: number;
  total?: number;
  status?: NodeRunStatus;
  reason?: string;
  // run_complete
  completed?: number;
  skipped?: number;
  annotations?: number;
  errors?: number;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  results?: Record<string, any>;
  // run_error
  message?: string;
}

/** SSE events emitted during a streaming experiment graph run. */
export interface ExpRunEvent {
  event: "started" | "node_start" | "node_end" | "run_complete" | "run_error";
  exp_id?: string;
  exp_name?: string;
  node_count?: number;
  nid?: string;
  label?: string;
  type?: string;
  idx?: number;
  total?: number;
  status?: "complete" | "error";
  error?: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  result?: Record<string, any>;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  node_results?: Record<string, any>;
  message?: string;
}

/** Shared SSE line reader — parses a fetch ReadableStream into typed events. */
async function* _sseStream<T>(response: Response, signal?: AbortSignal): AsyncGenerator<T> {
  if (!response.ok) {
    const text = await response.text().catch(() => response.statusText);
    throw new Error(`HTTP ${response.status}: ${text}`);
  }
  const reader = response.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      if (signal?.aborted) break;
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";
      for (const line of lines) {
        if (line.startsWith("data: ") && line.length > 6) {
          try { yield JSON.parse(line.slice(6)) as T; } catch { /* skip malformed */ }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

export async function* runStudyStream(
  studyId: string,
  signal?: AbortSignal,
  notify = false,
): AsyncGenerator<StudyRunEvent> {
  const res = await fetch(`${BASE}/studies/${studyId}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ notify }),
    signal,
  });
  yield* _sseStream<StudyRunEvent>(res, signal);
}

export async function* runGraphExperimentStream(
  expId: string,
  kwargs: Record<string, unknown> = {},
  signal?: AbortSignal,
  notify = false,
): AsyncGenerator<ExpRunEvent> {
  const res = await fetch(`${BASE}/experiment-graphs/${expId}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kwargs, notify }),
    signal,
  });
  yield* _sseStream<ExpRunEvent>(res, signal);
}

// ── Experiments (live CRUD) ───────────────────────────────────────────

export interface ExperimentMeta {
  id: string;
  name: string;
  category: string;
  description: string;
  estimated_time: string;
  requires_key: string | null;
  command: string;
  results_file: string | null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  report_schema: Record<string, any> | null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  params_schema: Record<string, any> | null;
  source_file: string;
  custom: boolean;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getNodeSchema = (nodeType: string, refId: string): Promise<Record<string, any>> =>
  request("GET", `/node-registry/${nodeType}/${refId}`);

export const listExperiments = (): Promise<ExperimentMeta[]> =>
  request("GET", "/experiments");

export const runExperiment = (
  id: string,
  kwargs: Record<string, unknown> = {}
// eslint-disable-next-line @typescript-eslint/no-explicit-any
): Promise<Record<string, any>> =>
  request("POST", `/experiments/${id}/run`, { kwargs });

export const deleteExperiment = (
  id: string
): Promise<{ deleted: boolean; file: string }> =>
  request("DELETE", `/experiments/${id}`);

export const duplicateExperiment = (
  id: string,
  newId?: string,
  newName?: string
// eslint-disable-next-line @typescript-eslint/no-explicit-any
): Promise<Record<string, any>> =>
  request("POST", `/experiments/${id}/duplicate`, {
    new_id: newId,
    new_name: newName,
  });

export const generateExperiment = (body: {
  prompt: string;
  name: string;
  category?: string;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
}): Promise<Record<string, any>> =>
  request("POST", "/experiments/generate", body);

export const reloadExperiments = (): Promise<{ reloaded: boolean; count: number }> =>
  request("POST", "/experiments/reload");

// ── AI summarization ──────────────────────────────────────────────────

export interface SuggestedAction {
  label: string;
  action: "create_study" | "generate_experiment" | string;
  hint: string;
}

export interface AISummaryResult {
  abstract: string;
  hypothesis: string | null;
  highlights: string[];
  insights: string;
  next_steps: string[];
  suggested_actions: SuggestedAction[];
  // experiment-level extras
  experiment_id?: string;
  // study-level extras
  study_id?: string;
  node_count?: number;
  // shared
  name?: string;
  category?: string;
  description?: string;
}

export const summarizeExperiment = (id: string): Promise<AISummaryResult> =>
  request("POST", `/experiments/${id}/summarize`);

export const summarizeStudy = (id: string): Promise<AISummaryResult> =>
  request("POST", `/studies/${id}/summarize`);

export const generateStudy = (body: {
  prompt: string;
  name: string;
}): Promise<StudyResponse> =>
  request("POST", "/studies/generate", body);

// ── RAG ──────────────────────────────────────────────────────────────────────

export interface RagChunk {
  text: string;
  source: string;
  source_type: string;
  score: number;
}

export const getRagStatus = (): Promise<{ index_size: number; index_age_seconds: number; ready: boolean }> =>
  request("GET", "/rag/status");

export const rebuildRagIndex = (): Promise<{ indexed_chunks: number; ready: boolean }> =>
  request("POST", "/rag/index");

export const queryRag = (query: string, topK = 5): Promise<{ query: string; results: RagChunk[]; total: number }> =>
  request("POST", "/rag/query", { query, top_k: topK });

// ── Presets

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const listPipelinePresets = (): Promise<Record<string, any>[]> =>
  request("GET", "/presets/pipelines");

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const createPipelinePreset = (body: Record<string, any>): Promise<Record<string, any>> =>
  request("POST", "/presets/pipelines", body);

export const duplicatePipelinePreset = (id: string) =>
  request("POST", `/presets/pipelines/${id}/duplicate`);

export const deletePipelinePreset = (id: string) =>
  request("DELETE", `/presets/pipelines/${id}`);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const listExperimentPresets = (): Promise<Record<string, any>[]> =>
  request("GET", "/presets/experiments");

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const createExperimentPreset = (body: Record<string, any>): Promise<Record<string, any>> =>
  request("POST", "/presets/experiments", body);

export const duplicateExperimentPreset = (id: string) =>
  request("POST", `/presets/experiments/${id}/duplicate`);

export const deleteExperimentPreset = (id: string) =>
  request("DELETE", `/presets/experiments/${id}`);

// ── Corpus Analysis ──────────────────────────────────────────────────

export interface EntropyResult {
  h1: number;
  h2_joint: number;
  conditional_h: number;
  h2_h1_ratio: number | null;
  type_token_ratio: number;
  zipf_correlation: number;
  token_count: number;
  type_count: number;
  hapax_count: number;
  zipf_table: Array<{ rank: number; token: string; freq: number; log_rank: number; log_freq: number }>;
}

export interface NgramEntry { ngram: string; count: number; tokens: string[]; }
export interface ConcordanceHit { position: number; left: string[]; match: string; right: string[]; }
export interface ConcordanceResult { query: string; hits: ConcordanceHit[]; total: number; }

export const getCorpusEntropy = (id: string): Promise<EntropyResult> =>
  request("GET", `/texts/${id}/entropy`);

export const getCorpusNgrams = (id: string, n = 2, limit = 50): Promise<NgramEntry[]> =>
  request("GET", `/texts/${id}/ngrams?n=${n}&limit=${limit}`);

export const getCorpusConcordance = (id: string, q: string, w = 5): Promise<ConcordanceResult> =>
  request("GET", `/texts/${id}/concordance?q=${encodeURIComponent(q)}&w=${w}`);

export const getCorpusExportUrl = (id: string, fmt: "txt" | "csv" | "json"): string =>
  `/api/v1/texts/${id}/export?fmt=${fmt}`;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const analyzeCorpus = (id: string): Promise<Record<string, any>> =>
  request("POST", `/texts/${id}/analyze`);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const detectCorpusAnomalies = (id: string): Promise<Record<string, any>> =>
  request("POST", `/texts/${id}/anomalies`);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const critiqueCorpus = (id: string): Promise<Record<string, any>> =>
  request("POST", `/texts/${id}/critique`);

// ── Research: Hypotheses ────────────────────────────────────────────

export interface Hypothesis {
  id: string;
  title: string;
  statement: string;
  status: "active" | "confirmed" | "refuted" | "paused" | string;
  evidence: string[];
  study_ids: string[];
  exp_ids: string[];
  created_at: string;
  updated_at: string;
}

export const listHypotheses = (): Promise<Hypothesis[]> =>
  request("GET", "/hypotheses");

export const createHypothesis = (body: { title: string; statement?: string; status?: string }): Promise<Hypothesis> =>
  request("POST", "/hypotheses", body);

export const updateHypothesis = (id: string, body: Partial<Hypothesis>): Promise<Hypothesis> =>
  request("PUT", `/hypotheses/${id}`, body);

export const deleteHypothesis = (id: string): Promise<Hypothesis> =>
  request("DELETE", `/hypotheses/${id}`);

// ── Research: Notebooks ─────────────────────────────────────────────

export interface Notebook {
  id: string;
  title: string;
  content: string;
  study_id: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export const listNotebooks = (): Promise<Notebook[]> =>
  request("GET", "/notebooks");

export const createNotebook = (body: { title: string; content?: string; study_id?: string; tags?: string[] }): Promise<Notebook> =>
  request("POST", "/notebooks", body);

export const updateNotebook = (id: string, body: Partial<Notebook>): Promise<Notebook> =>
  request("PUT", `/notebooks/${id}`, body);

export const deleteNotebook = (id: string): Promise<Notebook> =>
  request("DELETE", `/notebooks/${id}`);

// ── Research: Citations ─────────────────────────────────────────────

export interface Citation {
  id: string;
  key: string;
  title: string;
  authors: string;
  year: string;
  venue: string;
  doi: string;
  url: string;
  bibtex: string;
  exp_ids: string[];
  study_ids: string[];
  notes: string;
  created_at: string;
}

export const listCitations = (): Promise<Citation[]> =>
  request("GET", "/citations");

export const createCitation = (body: Omit<Citation, "id" | "exp_ids" | "study_ids" | "created_at">): Promise<Citation> =>
  request("POST", "/citations", body);

export const updateCitation = (id: string, body: Partial<Citation>): Promise<Citation> =>
  request("PUT", `/citations/${id}`, body);

export const deleteCitation = (id: string): Promise<Citation> =>
  request("DELETE", `/citations/${id}`);

// ── AI Tools ─────────────────────────────────────────────────────

export interface ChatMessage { role: string; content: string; }

export interface AIAction {
  type: string;        // run_experiment | run_pipeline | change_setting | generate_report |
                       // create_hypothesis | create_notebook | open_view | clear_jobs
  params: Record<string, unknown>;
  label: string;       // short human-readable label
  description: string; // longer explanation shown in the approval card
  requires_approval?: boolean; // if falsy, auto-execute without showing card
}

export interface AIChatResponse {
  role: string;
  content: string;
  actions?: AIAction[];
  context_type?: string | null;
  context_id?: string | null;
}

export const aiChat = (
  body: {
    messages: ChatMessage[];
    context_type?: string | null;
    context_id?: string | null;
    provider?: string | null;
    model?: string | null;
  },
  signal?: AbortSignal,
): Promise<AIChatResponse> =>
  request("POST", "/ai/chat", body, signal);

export const executeAiAction = (body: {
  type: string;
  params: Record<string, unknown>;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
}): Promise<Record<string, any>> =>
  request("POST", "/ai/execute-action", body);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const aiDecipher = (body: { sign_sequence: string[]; theory?: string; corpus_id?: string }): Promise<Record<string, any>> =>
  request("POST", "/ai/decipher", body);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const aiDraftSection = (body: { experiment_id: string; section_type?: string; result_json?: Record<string, any> }): Promise<Record<string, any>> =>
  request("POST", "/ai/draft-section", body);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const aiGenerateHypotheses = (body: { study_id?: string; context?: string }): Promise<Record<string, any>> =>
  request("POST", "/ai/hypotheses/generate", body);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const aiExperimentChain = (body: { hypothesis: string; available_experiment_ids?: string[] }): Promise<Record<string, any>> =>
  request("POST", "/ai/experiment-chain", body);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const aiSynthesize = (body: { study_ids: string[]; question?: string }): Promise<Record<string, any>> =>
  request("POST", "/ai/synthesize", body);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const aiSignReading = (body: { sign_ids: string[]; theory?: string; context?: string }): Promise<Record<string, any>> =>
  request("POST", "/ai/sign-reading", body);

export interface ResearchContextSummary {
  n_assigned_signs: number;
  token_coverage_pct: number;
  next_steps: string[];
  context_chars: number;
}

export interface ResearchContextResponse {
  context: string;
  summary: ResearchContextSummary;
}

export const getResearchContext = (): Promise<ResearchContextResponse> =>
  request("GET", "/ai/research-context");

export const aiReportSynthesis = (body: {
  report_contents: Array<{ name: string; filename: string; data: unknown }>;
  study_ids?: string[];
  title?: string;
}): Promise<{ title: string; markdown: string; n_reports: number; study_ids: string[] }> =>
  request("POST", "/ai/report-synthesis", body);

// ── System Metrics ───────────────────────────────────────────────

export interface GpuInfo {
  name: string;
  memory_total_mb: number;
  memory_used_mb: number;
  memory_free_mb: number;
  utilization_pct: number;
  memory_utilization_pct: number;
  temperature_c: number | null;
}

export interface SystemMetrics {
  timestamp: number;
  cpu: {
    percent: number;
    count_logical: number;
    count_physical: number;
    freq_mhz: number | null;
    freq_max_mhz: number | null;
    per_core_pct: number[];
    peak_pct: number;
  };
  ram: {
    total_gb: number;
    used_gb: number;
    available_gb: number;
    percent: number;
    peak_pct: number;
    swap_total_gb: number;
    swap_used_gb: number;
  };
  gpu: GpuInfo[];
  gpu_peaks: { utilization_pct: number; memory_utilization_pct: number };
  disk: {
    total_gb: number;
    used_gb: number;
    free_gb: number;
    percent: number;
    read_mbps: number;
    write_mbps: number;
    peak_read_mbps: number;
    peak_write_mbps: number;
  };
  network: {
    send_mbps: number;
    recv_mbps: number;
    peak_send_mbps: number;
    peak_recv_mbps: number;
    total_sent_gb: number;
    total_recv_gb: number;
  };
  peaks: Record<string, number>;
}

export const getSystemMetrics = (): Promise<SystemMetrics> =>
  request("GET", "/system/metrics");

export const getSystemGpu = (): Promise<GpuInfo[]> =>
  request("GET", "/system/gpu");

export const clearPeaks = (): Promise<{ cleared: boolean; peaks: Record<string, number> }> =>
  request("POST", "/system/peaks/clear");

export const getSystemMetricsStreamUrl = (): string => `/api/v1/system/metrics/stream`;

// ── Ollama ─────────────────────────────────────────────────────────

export interface OllamaInstalledModel {
  name: string;
  size_gb: number;
  modified_at: string;
  digest: string;
  family: string;
  display: string;
  glossa_score: number | null;
  tags: string[];
}

export interface OllamaLibraryEntry {
  name: string;
  display: string;
  family: string;
  size_gb: number;
  min_vram_gb: number;
  param_b: number;
  desc: string;
  quality: string;
  glossa_score: number;
  tags: string[];
  installed: boolean;
}

export interface OllamaCtxTier {
  min_vram_gb: number;
  max_vram_gb: number;
  label: string;
  ctx: number;
  note: string;
}

export interface OllamaRecommendation {
  gpu_name: string;
  vram_gb: number;
  tier: string;
  tier_description: string;
  recommended: OllamaLibraryEntry;
  all_fitting: string[];
  recommended_ctx_length: number;
  ctx_tier_label: string;
  ctx_tier_note: string;
  ctx_tiers: OllamaCtxTier[];
  glossa_note: string;
}

export interface OllamaContextConfig {
  session_ctx_length: number;
  tiers: OllamaCtxTier[];
  all_options: number[];
}

export const getOllamaStatus = (): Promise<{ running: boolean; base_url: string; message: string }> =>
  request("GET", "/ollama/status");

export const listOllamaInstalled = (): Promise<{ running: boolean; models: OllamaInstalledModel[]; count?: number }> =>
  request("GET", "/ollama/installed");

export const getOllamaLibrary = (): Promise<{ running: boolean; models: OllamaLibraryEntry[]; installed_names: string[] }> =>
  request("GET", "/ollama/library");

export const getOllamaRecommendation = (): Promise<OllamaRecommendation> =>
  request("GET", "/ollama/recommend");

export const deleteOllamaModel = (name: string): Promise<{ deleted: boolean; model: string }> =>
  request("DELETE", `/ollama/models/${encodeURIComponent(name)}`);

export const getOllamaContextConfig = (): Promise<OllamaContextConfig> =>
  request("GET", "/ollama/context-config");

export const setOllamaContextLength = (ctx_length: number): Promise<{ session_ctx_length: number; updated: boolean }> =>
  request("POST", "/ollama/context-config", { ctx_length });

// localStorage key for persisting context length between sessions
const CTX_LS_KEY = "glossa_ollama_ctx";
export const getLocalCtxLength = (): number =>
  parseInt(localStorage.getItem(CTX_LS_KEY) ?? "4096", 10) || 4096;
export const setLocalCtxLength = (n: number): void =>
  { localStorage.setItem(CTX_LS_KEY, String(n)); };

// ── H16: User-Definable Report Templates (DB-backed) ─────────────────────

export interface ReportTemplateSection {
  title:        string;
  data_source:  string;  // experiment ID or "upstream"
  data_key:     string;
  chart_type:   "table" | "bar" | "line" | "text";
  include_table: boolean;
  description:  string;
}

export interface UserReportTemplate {
  id:          string;
  name:        string;
  description: string;
  category:    string;
  sections:    ReportTemplateSection[];
  created_at:  string;
  updated_at:  string;
}

export const listUserReportTemplates = (): Promise<UserReportTemplate[]> =>
  request("GET", "/report-templates");

export const getUserReportTemplate = (id: string): Promise<UserReportTemplate> =>
  request("GET", `/report-templates/${id}`);

export const createUserReportTemplate = (body: {
  name: string;
  description?: string;
  category?: string;
  sections?: ReportTemplateSection[];
}): Promise<UserReportTemplate> =>
  request("POST", "/report-templates", body);

export const updateUserReportTemplate = (
  id: string,
  body: Partial<Pick<UserReportTemplate, "name" | "description" | "category" | "sections">>
): Promise<UserReportTemplate> =>
  request("PUT", `/report-templates/${id}`, body);

export const deleteUserReportTemplate = (id: string): Promise<{ deleted: boolean }> =>
  request("DELETE", `/report-templates/${id}`);

// ── H16: Anchor Sets ───────────────────────────────────────────────────

export interface AnchorPair {
  cipher:     string;
  target:     string;
  confidence: "high" | "medium" | "low";
  note:       string;
}

export interface AnchorSet {
  id:          string;
  name:        string;
  description: string;
  corpus_id:   string | null;
  language:    string;
  pairs:       AnchorPair[];
  created_at:  string;
  updated_at:  string;
}

export const listAnchorSets = (corpusId?: string): Promise<AnchorSet[]> =>
  request("GET", corpusId ? `/anchor-sets?corpus_id=${encodeURIComponent(corpusId)}` : "/anchor-sets");

export const getAnchorSet = (id: string): Promise<AnchorSet> =>
  request("GET", `/anchor-sets/${id}`);

export const createAnchorSet = (body: {
  name: string;
  description?: string;
  corpus_id?: string | null;
  language?: string;
  pairs?: AnchorPair[];
}): Promise<AnchorSet> =>
  request("POST", "/anchor-sets", body);

export const updateAnchorSet = (
  id: string,
  body: Partial<Pick<AnchorSet, "name" | "description" | "corpus_id" | "language" | "pairs">>
): Promise<AnchorSet> =>
  request("PUT", `/anchor-sets/${id}`, body);

export const deleteAnchorSet = (id: string): Promise<{ deleted: boolean }> =>
  request("DELETE", `/anchor-sets/${id}`);

// ── H16: World Language Corpus Catalogue ─────────────────────────────

export interface CorpusCatalogueEntry {
  id:                string;
  name:              string;
  language:          string;
  language_family:   string;
  script_type:       string;
  period:            string;
  tokens_approx:     number;
  source_url:        string;
  license:           string;
  description:       string;
  local_module:      string;  // non-empty = can import in one click
  is_undeciphered:   boolean | number;
  reading_direction: string;  // ltr | rtl | bidi | unknown
  already_imported?: boolean;  // enriched by API
}

export interface CatalogueImportResult {
  imported:   boolean;
  corpus_id?: string;
  name:       string;
  tokens?:    number;
  reason?:    string;  // "already_exists" if duplicate
}

export const listCorpusCatalogue = (params?: {
  script_type?: string;
  undeciphered?: boolean;
}): Promise<CorpusCatalogueEntry[]> => {
  const qs = new URLSearchParams();
  if (params?.script_type)  qs.set("script_type", params.script_type);
  if (params?.undeciphered !== undefined) qs.set("undeciphered", String(params.undeciphered));
  const q = qs.toString();
  return request("GET", `/corpus-catalogue${q ? `?${q}` : ""}`);
};

export const importCorpusCatalogueEntry = (id: string): Promise<CatalogueImportResult> =>
  request("POST", `/corpus-catalogue/${id}/import`);

// Note: do NOT encodeURIComponent here — EventSource sends the URL as-is and
// FastAPI's path param decoder handles the colon in model names like "mistral:7b"
export const getOllamaPullUrl = (modelName: string): string =>
  `/api/v1/ollama/pull/${modelName}`;

// ── Python Environment ─────────────────────────────────────────────

export interface EnvStatus {
  venv_exists: boolean;
  venv_path: string;
  python_path: string | null;
  python_version: string | null;
  pkg_count: number;
  backend_dir: string;
}

export interface EnvPackage {
  name: string;
  version: string;
}

export const getEnvStatus = (): Promise<EnvStatus> =>
  request("GET", "/env/status");

export const getEnvPackages = (): Promise<{ packages: EnvPackage[]; count: number; venv_exists: boolean }> =>
  request("GET", "/env/packages");

// SSE streams — return the URL; caller opens EventSource
export const getEnvSetupUrl  = (): string => `/api/v1/env/setup`;
export const getEnvRebuildUrl = (): string => `/api/v1/env/rebuild`;
export const getEnvUpgradeUrl = (): string => `/api/v1/env/upgrade`;

// POST wrappers that return a raw Response (SSE body)
export const runEnvSetup   = (): Promise<Response> => fetch(`${BASE}/env/setup`,   { method: "POST" });
export const runEnvRebuild = (): Promise<Response> => fetch(`${BASE}/env/rebuild`, { method: "POST" });
export const runEnvUpgrade = (): Promise<Response> => fetch(`${BASE}/env/upgrade`, { method: "POST" });

// ── Terminal + Logs ─────────────────────────────────────────────────

export const getLogStreamUrl = (): string => `/api/v1/terminal/log/stream`;

export const getLog = (lines = 200): Promise<{ lines: string[]; total_lines?: number; exists: boolean }> =>
  request("GET", `/terminal/log?lines=${lines}`);

export const purgeLog = (): Promise<{ cleared: number; file: string }> =>
  request("POST", "/terminal/log/purge");

export const runTerminalCommand = (command: string, cwd?: string): Promise<Response> =>
  fetch(`${BASE}/terminal/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command, cwd, use_venv: true }),
  });

// listJobs and cancelJob are defined in the Jobs section above

// ── Collaboration Messages ────────────────────────────────────────────────

export interface CollabMessage {
  id: string;
  study_id: string;
  author: string;
  message: string;
  pinned: number;   // 0 | 1
  created_at: string;
}

export const listCollabMessages = (studyId: string): Promise<CollabMessage[]> =>
  request("GET", `/studies/${studyId}/messages`);

export const createCollabMessage = (
  studyId: string,
  body: { author?: string; message: string }
): Promise<CollabMessage> =>
  request("POST", `/studies/${studyId}/messages`, body);

export const updateCollabMessage = (
  studyId: string,
  msgId: string,
  body: { pinned?: number; message?: string; author?: string }
): Promise<CollabMessage> =>
  request("PATCH", `/studies/${studyId}/messages/${msgId}`, body);

export const deleteCollabMessage = (
  studyId: string,
  msgId: string,
): Promise<{ deleted: boolean; id: string }> =>
  request("DELETE", `/studies/${studyId}/messages/${msgId}`);

// ── CAS Models (CPSC) ────────────────────────────────────────────────

export interface CASModel {
  id: string;
  name: string;
  description: string;
  yaml_text: string;
  engine_hint: string;    // auto | iterative | cellular
  is_builtin: number;     // 0 = user, 1 = built-in (protected)
  created_at: string;
  updated_at: string;
}

export interface CASModelCreate {
  name: string;
  description?: string;
  yaml_text: string;
  engine_hint?: string;
}

export interface CASModelUpdate {
  name?: string;
  description?: string;
  yaml_text?: string;
  engine_hint?: string;
}

export interface CASValidateResult {
  valid: boolean;
  error: string | null;
  model_id: string;
  n_variables: number;
  n_constraints: number;
  dof_vars: string[];
  dry_run_success?: boolean;
  dry_run_violation?: number;
}

export const listCASModels = (builtinOnly = false): Promise<CASModel[]> =>
  request("GET", `/cas-models${builtinOnly ? "?builtin_only=true" : ""}`);

export const getCASModel = (id: string): Promise<CASModel> =>
  request("GET", `/cas-models/${id}`);

export const createCASModel = (body: CASModelCreate): Promise<CASModel> =>
  request("POST", "/cas-models", body);

export const updateCASModel = (id: string, body: CASModelUpdate): Promise<CASModel> =>
  request("PUT", `/cas-models/${id}`, body);

export const deleteCASModel = (id: string): Promise<{ deleted: boolean; id: string }> =>
  request("DELETE", `/cas-models/${id}`);

export const validateCASModel = (id: string): Promise<CASValidateResult> =>
  request("POST", `/cas-models/${id}/validate`);

// ── AG2 Research Agent ────────────────────────────────────────────

export interface AG2Status {
  available: boolean;
  model: string | null;
  mode: "llm_enabled" | "tool_only";
  tools: string[];
  note?: string;
  error?: string;
}

export interface AG2Event {
  type: "agent_start" | "tool_call" | "tool_result" | "message" | "error" | "done";
  agent: string;
  content: string;
}

export interface AG2Tool {
  name: string;
  description: string;
}

export const getAG2Status = (): Promise<AG2Status> =>
  request("GET", "/ag2/status");

export const getAG2Tools = (): Promise<AG2Tool[]> =>
  request("GET", "/ag2/tools");

export async function* streamAG2Chat(
  message: string,
  history: { role: string; content: string }[] = [],
  contextType = "",
  contextId = "",
  signal?: AbortSignal,
): AsyncGenerator<AG2Event> {
  const res = await fetch(`${BASE}/ag2/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history, context_type: contextType, context_id: contextId }),
    signal,
  });
  if (!res.ok) throw new Error(`AG2 HTTP ${res.status}`);
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  try {
    while (true) {
      if (signal?.aborted) break;
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";
      for (const line of lines) {
        if (line.startsWith("data: ") && line.length > 6) {
          try { yield JSON.parse(line.slice(6)) as AG2Event; } catch { /* skip */ }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

// ── Discovery (continuous-discovery engine) ───────────────────────────────

export interface DiscoveryLink {
  kind: string;          // sign | dedr | site | provider | ...
  target_id: string;
  scheme?: string;       // generic | mahadevan | parpola | fuls (for sign links)
  label?: string;
}

export interface DiscoveryItem {
  id: string;
  title: string;
  url: string;
  source: string;
  topic: string;         // CSV of topic ids
  published_at: string;
  fetched_at: string;
  lang: string;
  raw_json: Record<string, unknown>;
  summary: string;
  kind: string;          // hypothesis | finding | study | tablet | review | tooling | other
  confidence: number;
  links: DiscoveryLink[];
  status: "new" | "reviewed" | "saved" | "dismissed" | string;
  notes: string;
}

export interface DiscoveryTopic {
  id: string;
  label: string;
  description: string;
  keywords: string[];
  exclusions: string[];
  languages: string[];
}

export interface DiscoverySource {
  source: string;
  requires: string[];
  configured: boolean;
  disabled_reason: string;
}

export interface DiscoveryListResponse {
  items: DiscoveryItem[];
  limit: number;
  offset: number;
}

export interface DiscoveryJobAck {
  job_id: string;
  status: string;
  message: string;
}

export interface DiscoveryListParams {
  topic?: string;
  kind?: string;
  status?: string;
  since?: string;
  limit?: number;
  offset?: number;
}

function _qs(params: Record<string, unknown>): string {
  const usp = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === null || v === "") continue;
    usp.set(k, String(v));
  }
  const s = usp.toString();
  return s ? `?${s}` : "";
}

export const listDiscoveryItems = (
  params: DiscoveryListParams = {},
): Promise<DiscoveryListResponse> =>
  request("GET", `/discovery/items${_qs(params as Record<string, unknown>)}`);

export const getDiscoveryItem = (id: string): Promise<DiscoveryItem> =>
  request("GET", `/discovery/items/${encodeURIComponent(id)}`);

export const updateDiscoveryStatus = (
  id: string,
  status: string,
  notes?: string,
): Promise<DiscoveryItem> =>
  request("POST", `/discovery/items/${encodeURIComponent(id)}/status`, { status, notes });

export const listDiscoveryTopics = (): Promise<{ topics: DiscoveryTopic[] }> =>
  request("GET", "/discovery/topics");

export const listDiscoverySources = (): Promise<{ sources: DiscoverySource[] }> =>
  request("GET", "/discovery/sources");

export const getDiscoveryStats = (
  group: "status" | "kind" | "topic" | "source" = "status",
): Promise<{ group: string; counts: Record<string, number> }> =>
  request("GET", `/discovery/stats?group=${group}`);

export const startDiscoveryFetch = (body: {
  topics?: string[]; sources?: string[]; since_iso?: string;
}): Promise<DiscoveryJobAck> =>
  request("POST", "/discovery/fetch", body);

export const startDiscoveryMine = (body: {
  topic?: string; limit?: number;
}): Promise<DiscoveryJobAck> =>
  request("POST", "/discovery/mine", body);

// ── Notifications (email recipients + send log) ────────────────────────

export interface NotificationRecipient {
  id: string;
  email: string;
  label: string;
  active: number; // 0 | 1
  created_at: string;
  updated_at: string;
}

export interface NotificationLogEntry {
  id: string;
  recipient: string;
  subject: string;
  kind: string;
  sent_at: string;
  item_count: number;
  status: string; // sent | failed | skipped
  error: string;
}

export interface NotifierStatus {
  configured: boolean;
  transport: "graph" | "smtp" | "none";
  host: string;
  port: number;
  from: string;
  use_tls: boolean;
  username_set: boolean;
  password_set: boolean;
  graph_configured: boolean;
  graph_client_id_set: boolean;
  graph_tenant: string;
  recipients_total: number;
  recipients_active: number;
}

export interface GraphDeviceFlowStart {
  session_id: string;
  user_code: string;
  verification_uri: string;
  expires_in: number;
  interval: number;
  message: string;
}

export interface GraphDeviceFlowPoll {
  status: "pending" | "success" | "failed" | "expired";
  error?: string;
}

export interface DiscoverySchedulerStatus {
  running: boolean;
  enabled: boolean;
  interval_seconds: number;
  newly_started?: boolean;
  stopped?: boolean;
}

export interface NotificationTestResult {
  subject: string;
  results: { recipient: string; status: string; error: string }[];
  sent: number;
  failed: number;
}

export const listNotificationRecipients = (
): Promise<{ recipients: NotificationRecipient[]; count: number }> =>
  request("GET", "/notifications/recipients");

export const createNotificationRecipient = (
  body: { email: string; label?: string; active?: boolean },
): Promise<NotificationRecipient> =>
  request("POST", "/notifications/recipients", body);

export const updateNotificationRecipient = (
  rid: string,
  body: Partial<{ email: string; label: string; active: boolean }>,
): Promise<NotificationRecipient> =>
  request("PATCH", `/notifications/recipients/${encodeURIComponent(rid)}`, body);

export const deleteNotificationRecipient = (
  rid: string,
): Promise<{ deleted: boolean; id: string }> =>
  request("DELETE", `/notifications/recipients/${encodeURIComponent(rid)}`);

export const getNotifierStatus = (): Promise<NotifierStatus> =>
  request("GET", "/notifications/status");

export const listNotificationLog = (
  limit = 100,
): Promise<{ entries: NotificationLogEntry[]; limit: number }> =>
  request("GET", `/notifications/log?limit=${limit}`);

export const sendTestNotification = (): Promise<NotificationTestResult> =>
  request("POST", "/notifications/test");

// ── Microsoft Graph (Outlook 365) device-code OAuth ───────────────────

export const startGraphDeviceFlow = (): Promise<GraphDeviceFlowStart> =>
  request("POST", "/notifications/graph/start");

export const pollGraphDeviceFlow = (
  session_id: string,
): Promise<GraphDeviceFlowPoll> =>
  request("POST", "/notifications/graph/poll", { session_id });

export const disconnectGraph = (): Promise<{ disconnected: boolean }> =>
  request("POST", "/notifications/graph/disconnect");

// ── Discovery scheduler runtime control ──────────────────────────

export const getDiscoverySchedulerStatus = (
): Promise<DiscoverySchedulerStatus> =>
  request("GET", "/discovery/scheduler/status");

export const startDiscoveryScheduler = (
): Promise<DiscoverySchedulerStatus> =>
  request("POST", "/discovery/scheduler/start");

export const stopDiscoveryScheduler = (
): Promise<DiscoverySchedulerStatus> =>
  request("POST", "/discovery/scheduler/stop");
