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
  jobs: Record<string, number>;
  job_counts: Record<string, number>;
  pipelines: string[];
  pipeline_count: number;
  catalog_counts: Record<string, number>;
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

export const updateText = (id: string, body: Partial<TextCreate>): Promise<TextResponse> =>
  request("PUT", `/texts/${id}`, body);

export const deleteText = (id: string): Promise<TextResponse> =>
  request("DELETE", `/texts/${id}`);

// ── Jobs ──────────────────────────────────────────────────────────────

export const listJobs = (): Promise<JobResponse[]> =>
  request("GET", "/jobs");

export const getJob = (id: string): Promise<JobResponse> =>
  request("GET", `/jobs/${id}`);

export const createJob = (body: JobCreate): Promise<JobResponse> =>
  request("POST", "/jobs", body);

export const cancelJob = (id: string): Promise<JobResponse> =>
  request("DELETE", `/jobs/${id}`);

export const clearJobs = (): Promise<{ cleared: number }> =>
  request("DELETE", "/jobs");

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

export interface StudyNode {
  id: string;
  type: "experiment" | "pipeline" | "note";
  ref_id: string;  // experiment id or pipeline id
  label: string;
  params: Record<string, unknown>;
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

export interface StudyRunResult {
  study_id: string;
  node_count: number;
  completed: number;
  skipped: number;
  errors: number;
  results: Record<string, {
    status: "complete" | "skipped" | "error";
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    result?: Record<string, any>;
    reason?: string;
  }>;
}

export const runStudy = (id: string): Promise<StudyRunResult> =>
  request("POST", `/studies/${id}/run`);

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
  source_file: string;
  custom: boolean;
}

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

// ── Presets ───────────────────────────────────────────────────────────

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

export const aiChat = (body: {
  messages: ChatMessage[];
  context_type?: string | null;
  context_id?: string | null;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
}): Promise<Record<string, any>> =>
  request("POST", "/ai/chat", body);

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

// Note: do NOT encodeURIComponent here — EventSource sends the URL as-is and
// FastAPI's path param decoder handles the colon in model names like "mistral:7b"
export const getOllamaPullUrl = (modelName: string): string =>
  `/api/v1/ollama/pull/${modelName}`;

// ── Terminal + Logs ─────────────────────────────────────────────────

export const getLogStreamUrl = (): string => `/api/v1/terminal/log/stream`;

export const getLog = (lines = 200): Promise<{ lines: string[]; total_lines?: number; exists: boolean }> =>
  request("GET", `/terminal/log?lines=${lines}`);

export const runTerminalCommand = (command: string, cwd?: string): Promise<Response> =>
  fetch(`${BASE}/terminal/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command, cwd, use_venv: true }),
  });

// listJobs and cancelJob are defined in the Jobs section above
