/**
 * ProgramsView — the tool home (Spec 081 wireframes 01 + 16).
 *
 * Glossa Lab is the tool; a program is the unit of work inside it.
 * The app opens here: the operator is offered the programs, not a
 * global dashboard. "Program" is the existing Project entity in UI
 * language only — the data model is unchanged.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import {
  getStatus,
  importProject,
  upsertProject,
  type StatusResponse,
  type Project,
} from "../api";
import { useProject } from "../hooks/useProject";
import { useToast } from "../hooks/useToast";
import {
  Card, CardTitle, PageHead, PrimaryButton, QuietButton, RowItem, RowMeta, RowTitle,
  SmallButton, fmtClock, palette,
} from "./ui081";

function newProgramId(label: string): string {
  const slug = label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40);
  return `${slug || "program"}-${Math.random().toString(36).slice(2, 8)}`;
}

export function ProgramsView({
  darkMode, onNavigate,
}: {
  darkMode: boolean;
  onNavigate: (view: string) => void;
}) {
  const p = palette(darkMode);
  const { projects, activeProject, setActiveProject, refreshProjects, loading } = useProject();
  const [creating, setCreating] = useState(false);
  const [health, setHealth] = useState<StatusResponse | null>(null);
  const [checkedAt, setCheckedAt] = useState<Date | null>(null);

  const loadHealth = useCallback(() => {
    getStatus()
      .then((h) => { setHealth(h); setCheckedAt(new Date()); })
      .catch(() => { setHealth(null); setCheckedAt(new Date()); });
  }, []);
  useEffect(() => { loadHealth(); }, [loadHealth]);

  const openProgram = async (proj: Project) => {
    await setActiveProject(proj.id);
    onNavigate("home");
  };

  if (loading) {
    return <div style={{ color: p.muted, fontSize: 13 }}>Loading programs…</div>;
  }

  return (
    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      {projects.length === 0 ? (
        <FirstRun
          p={p} health={health} creating={creating} setCreating={setCreating}
          onCreated={async (id) => { await refreshProjects(); await setActiveProject(id); onNavigate("home"); }}
          onNavigate={onNavigate}
        />
      ) : (
        <>
          <PageHead
            p={p}
            title="Programs"
            lede={
              <>
                A program is one research effort: a question, the claims that test it, and the
                evidence behind them. Glossa Lab is the tool — programs hold the work. Open one
                to continue, or start a new one.
              </>
            }
            primary={<PrimaryButton onClick={() => setCreating(true)} testId="new-program">+ New program</PrimaryButton>}
          />

          {creating && (
            <div style={{ marginBottom: 14 }}>
              <CreateProgramCard
                p={p}
                onCancel={() => setCreating(false)}
                onCreated={async (id) => {
                  setCreating(false);
                  await refreshProjects();
                  await setActiveProject(id);
                  onNavigate("home");
                }}
              />
            </div>
          )}

          <div style={{ display: "grid", gap: 14 }}>
            {projects.map((proj) => (
              <ProgramCard
                key={proj.id}
                p={p}
                proj={proj}
                isOpen={activeProject?.id === proj.id}
                onOpen={() => void openProgram(proj)}
              />
            ))}

            {/* Service strip — the tool itself, shared by every program */}
            <Card p={p}>
              <CardTitle p={p} sub="the tool itself, shared by every program">Service</CardTitle>
              <RowItem p={p} style={{ borderBottom: "none", paddingBottom: 0 }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <RowTitle p={p}>
                    {health
                      ? `${health.app ?? "Glossa Lab"} backend · v${health.version} · ${health.host ?? "this machine"}`
                      : "Backend not answering"}
                  </RowTitle>
                  <RowMeta p={p}>
                    {health
                      ? `Data folder: ${health.data_dir || "—"} · Database ${health.db_ready ? "ready" : "not ready"} · Serving since ${health.started_at ? fmtClock(health.started_at) : "—"} · checked ${checkedAt ? fmtClock(checkedAt.toISOString()) : "—"}`
                      : "The service did not answer the identity check just now."}
                  </RowMeta>
                </div>
                <span style={{
                  display: "inline-flex", padding: "2px 8px", borderRadius: 10, fontSize: 11, fontWeight: 700,
                  background: health ? "#f0fdf4" : "#fef2f2", color: health ? "#15803d" : "#b91c1c",
                }}>
                  {health ? "Healthy" : "Offline"}
                </span>
                <SmallButton onClick={() => onNavigate("status")}>Open status</SmallButton>
              </RowItem>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}

function ProgramCard({
  p, proj, isOpen, onOpen,
}: {
  p: ReturnType<typeof palette>;
  proj: Project;
  isOpen: boolean;
  onOpen: () => void;
}) {
  const question = (proj.question ?? "").trim() || proj.description || "";
  const stats: { n: string; l: string }[] = [
    { n: String(proj.corpus_ids?.length ?? 0), l: "corpora linked" },
    { n: String(proj.experiment_ids?.length ?? 0), l: "experiments linked" },
    { n: String(proj.topic_ids?.length ?? 0), l: "discovery topics" },
    { n: proj.updated_at ? proj.updated_at.slice(0, 10) : "—", l: "last updated" },
  ];
  return (
    <Card p={p}>
      <div style={{ display: "flex", alignItems: "flex-start", gap: 14, flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 240 }}>
          <div style={{ fontSize: 16, fontWeight: 750, color: p.fg }}>
            {proj.label}
            {isOpen && (
              <span style={{ marginLeft: 8, fontSize: 10, fontWeight: 700, color: p.accent }}>OPEN</span>
            )}
          </div>
          {question && (
            <div style={{ fontSize: 13, color: p.muted, marginTop: 2, lineHeight: 1.45 }}>{question}</div>
          )}
        </div>
        <PrimaryButton onClick={onOpen}>Open program</PrimaryButton>
      </div>
      <div style={{ borderTop: `1px solid ${p.borderSoft}`, marginTop: 12, paddingTop: 12,
        display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: 14 }}>
        {stats.map((s) => (
          <div key={s.l}>
            <div style={{ fontSize: 26, fontWeight: 750, letterSpacing: "-0.01em", color: p.fg }}>{s.n}</div>
            <div style={{ fontSize: 12, color: p.muted, marginTop: 2 }}>{s.l}</div>
          </div>
        ))}
      </div>
      {proj.description && proj.question && (
        <RowMeta p={p} style={{ marginTop: 10 }}>{proj.description}</RowMeta>
      )}
    </Card>
  );
}

function CreateProgramCard({
  p, onCreated, onCancel,
}: {
  p: ReturnType<typeof palette>;
  onCreated: (id: string) => void;
  onCancel?: () => void;
}) {
  const { toast } = useToast();
  const [label, setLabel] = useState("");
  const [question, setQuestion] = useState("");
  const [description, setDescription] = useState("");
  const [busy, setBusy] = useState(false);

  const inp: React.CSSProperties = {
    width: "100%", padding: "8px 10px", border: `1px solid ${p.border}`, borderRadius: 7,
    fontSize: 13, background: p.inputBg, color: p.fg, outline: "none", boxSizing: "border-box",
  };

  const create = async () => {
    if (!label.trim() || !question.trim()) {
      toast("A program needs a name and the question it tests — nothing else.", "error");
      return;
    }
    setBusy(true);
    try {
      const id = newProgramId(label);
      await upsertProject(id, {
        label: label.trim(),
        question: question.trim(),
        description: description.trim(),
        prompt_context: "",
        topic_ids: [], experiment_ids: [], corpus_ids: [],
        is_active: 0,
      });
      toast(`Program “${label.trim()}” created`, "success");
      onCreated(id);
    } catch (e) {
      toast(String(e), "error");
    } finally { setBusy(false); }
  };

  return (
    <Card p={p}>
      <CardTitle p={p}>Start a program</CardTitle>
      <RowMeta p={p} style={{ marginBottom: 10 }}>
        You need two things. Everything else — data, claims, experiments — is added inside the
        program, as the work grows.
      </RowMeta>
      <div style={{ display: "grid", gap: 10 }}>
        <div>
          <div style={{ fontSize: 12, fontWeight: 700, color: p.fg, marginBottom: 3 }}>1 · A name</div>
          <input value={label} onChange={(e) => setLabel(e.target.value)} style={inp}
            placeholder="Short and plain: the effort's name, as you would say it." aria-label="Program name" />
        </div>
        <div>
          <div style={{ fontSize: 12, fontWeight: 700, color: p.fg, marginBottom: 3 }}>2 · The question it tests</div>
          <input value={question} onChange={(e) => setQuestion(e.target.value)} style={inp}
            placeholder="One sentence — it appears on the program's home and in the switcher." aria-label="Program question" />
        </div>
        <div>
          <div style={{ fontSize: 12, fontWeight: 700, color: p.fg, marginBottom: 3 }}>Description (optional)</div>
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} style={{ ...inp, minHeight: 56 }}
            placeholder="Anything else a reader of this program should know up front." aria-label="Program description" />
        </div>
      </div>
      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <PrimaryButton onClick={() => void create()} disabled={busy} testId="create-program">
          + Create program
        </PrimaryButton>
        {onCancel && <QuietButton onClick={onCancel}>Cancel</QuietButton>}
      </div>
    </Card>
  );
}

function FirstRun({
  p, health, creating, setCreating, onCreated, onNavigate,
}: {
  p: ReturnType<typeof palette>;
  health: StatusResponse | null;
  creating: boolean;
  setCreating: (v: boolean) => void;
  onCreated: (id: string) => void;
  onNavigate: (view: string) => void;
}) {
  const { toast } = useToast();
  const { refreshProjects } = useProject();
  const fileRef = useRef<HTMLInputElement>(null);

  const handleImport = async (file: File) => {
    try {
      const bundle = JSON.parse(await file.text()) as Record<string, unknown>;
      const proj = await importProject(bundle);
      toast(`Imported program “${proj.label}”`, "success");
      await refreshProjects();
      onCreated(proj.id);
    } catch (e) {
      toast(`Import failed: ${String(e)}`, "error");
    }
  };

  return (
    <div>
      <PageHead
        p={p}
        title="Glossa Lab is ready. The work starts with a program."
        lede={
          <>
            Glossa Lab is a workbench for evidence-tested research. A <b>program</b> is one
            research effort inside it: a question, the claims that test it — each registered
            with the evidence that could prove it wrong — and the record of what people have
            settled. No program exists yet on this machine.
          </>
        }
      />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 14, alignItems: "start" }}>
        {creating ? (
          <CreateProgramCard p={p} onCreated={onCreated} />
        ) : (
          <Card p={p}>
            <CardTitle p={p}>Start a program</CardTitle>
            <RowMeta p={p} style={{ marginBottom: 10 }}>
              You need two things. Everything else — data, claims, experiments — is added
              inside the program, as the work grows.
            </RowMeta>
            <RowItem p={p}>
              <div>
                <RowTitle p={p}>1 · A name</RowTitle>
                <RowMeta p={p}>Short and plain: the effort's name, as you would say it.</RowMeta>
              </div>
            </RowItem>
            <RowItem p={p} style={{ borderBottom: "none" }}>
              <div>
                <RowTitle p={p}>2 · The question it tests</RowTitle>
                <RowMeta p={p}>
                  One sentence. It appears on the program's home and in the switcher, so it
                  should say what would count as an answer.
                </RowMeta>
              </div>
            </RowItem>
            <div style={{ marginTop: 12 }}>
              <PrimaryButton onClick={() => setCreating(true)} testId="create-first-program">
                + Create your first program
              </PrimaryButton>
            </div>
          </Card>
        )}

        <Card p={p}>
          <CardTitle p={p}>Or bring existing work</CardTitle>
          <RowMeta p={p} style={{ marginBottom: 10 }}>
            A project export from the current version imports as a program: its topics,
            corpora, experiments, and records keep their names and dates.
          </RowMeta>
          <QuietButton onClick={() => fileRef.current?.click()}>Import an existing project…</QuietButton>
          <input ref={fileRef} type="file" accept=".json,application/json" style={{ display: "none" }}
            onChange={(e) => { const f = e.target.files?.[0]; if (f) void handleImport(f); e.target.value = ""; }} />
          <div style={{ borderTop: `1px solid ${p.borderSoft}`, marginTop: 12, paddingTop: 12 }}>
            <RowMeta p={p}>
              The service underneath is already verified:{" "}
              <b style={{ color: p.fg }}>
                {health ? `${health.app ?? "Glossa Lab"} v${health.version}` : "backend not answering"}
              </b>{" "}
              on this machine{health?.data_dir ? `, data folder ${health.data_dir}` : ""}, checked
              just now. Details live under{" "}
              <a href="#" onClick={(e) => { e.preventDefault(); onNavigate("status"); }} style={{ color: p.accent }}>
                Status
              </a>{" "}
              — you do not need them to begin.
            </RowMeta>
          </div>
        </Card>
      </div>
    </div>
  );
}
