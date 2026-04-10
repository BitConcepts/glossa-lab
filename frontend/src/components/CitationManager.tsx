/**
 * CitationManager — store and manage research citations.
 * Supports manual entry and BibTeX paste/import.
 * Link citations to experiments and studies.
 */
import { useEffect, useState } from "react";
import {
  createCitation, deleteCitation, listCitations, updateCitation,
  type Citation,
} from "../api";
import { useToast } from "../hooks/useToast";

/** Parse a single BibTeX entry into fields */
function parseBibTeX(raw: string): Partial<Citation> {
  const key = (raw.match(/@\w+\{([^,]+),/) ?? [])[1]?.trim() ?? "";
  const get = (field: string) => {
    const m = raw.match(new RegExp(`\\b${field}\\s*=\\s*[{"]([^}"]+)[}"]`, "i"));
    return m ? m[1].trim() : "";
  };
  return {
    key,
    title: get("title"),
    authors: get("author"),
    year: get("year"),
    venue: get("journal") || get("booktitle") || get("publisher"),
    doi: get("doi"),
    url: get("url"),
    bibtex: raw.trim(),
  };
}

function CitationCard({ cit, onUpdated, onDeleted }: {
  cit: Citation; onUpdated: (c: Citation) => void; onDeleted: (id: string) => void;
}) {
  const { toast } = useToast();
  const [expanded, setExpanded] = useState(false);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ ...cit });
  const [saving, setSaving] = useState(false);

  const save = async () => {
    setSaving(true);
    try {
      const updated = await updateCitation(cit.id, {
        title: form.title, authors: form.authors, year: form.year,
        venue: form.venue, doi: form.doi, url: form.url, notes: form.notes, bibtex: form.bibtex,
      });
      onUpdated(updated); setEditing(false); toast("Saved", "success");
    } catch { toast("Save failed", "error"); }
    finally { setSaving(false); }
  };

  const [bibtexCopied, setBibtexCopied] = useState(false);
  const copyBibTeX = () => {
    if (!cit.bibtex) { toast("No BibTeX stored", "warning"); return; }
    navigator.clipboard.writeText(cit.bibtex).then(() => {
      setBibtexCopied(true);
      setTimeout(() => setBibtexCopied(false), 1400);
    });
  };

  return (
    <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden", marginBottom: 8 }}>
      <div style={{ display: "flex", gap: 10, padding: "10px 14px", background: "#fafafa", cursor: "pointer", alignItems: "center" }}
        onClick={() => setExpanded(x => !x)}>
        <span style={{ fontSize: 11, padding: "1px 6px", borderRadius: 6, background: "#f3f4f6", color: "#6b7280", fontWeight: 700, fontFamily: "monospace" }}>{cit.year}</span>
        <span style={{ flex: 1, fontWeight: 600, fontSize: 13, color: "#111827" }}>{cit.title || cit.key}</span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{cit.authors.split(",")[0]?.trim().split(" ").pop() ?? ""}{cit.authors.includes(",") ? " et al." : ""}</span>
        {cit.venue && <span style={{ fontSize: 11, color: "#9ca3af", maxWidth: 150, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{cit.venue}</span>}
        <span style={{ fontSize: 11, color: "#6b7280", fontFamily: "monospace" }}>[{cit.key}]</span>
        <button onClick={(e) => { e.stopPropagation(); copyBibTeX(); }} title="Copy BibTeX"
          style={{ border: "1px solid #e5e7eb", background: bibtexCopied ? "#dcfce7" : "none",
            color: bibtexCopied ? "#16a34a" : undefined,
            borderRadius: 4, fontSize: 10, padding: "1px 7px", cursor: "pointer", transition: "background 0.2s" }}>
            {bibtexCopied ? "✓" : "BibTeX"}</button>
        <button onClick={(e) => { e.stopPropagation(); if (!confirm("Delete?")) return; deleteCitation(cit.id).then(() => onDeleted(cit.id)).catch(() => toast("Delete failed", "error")); }}
          style={{ border: "1px solid #fca5a5", background: "none", color: "#dc2626", borderRadius: 4, fontSize: 10, padding: "1px 7px", cursor: "pointer" }}>🗑</button>
        <span style={{ fontSize: 14, color: "#9ca3af" }}>{expanded ? "▲" : "▼"}</span>
      </div>

      {expanded && (
        <div style={{ padding: "14px 16px" }} onClick={(e) => e.stopPropagation()}>
          {editing ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 8, maxWidth: 600 }}>
              {(["title", "authors", "year", "venue", "doi", "url"] as Array<"title"|"authors"|"year"|"venue"|"doi"|"url">).map((field) => (
                <div key={field}>
                  <label style={lbl}>{field.charAt(0).toUpperCase() + field.slice(1)}</label>
                  <input value={form[field]} onChange={(e) => setForm(f => ({ ...f, [field]: e.target.value }))} style={inp} />
                </div>
              ))}
              <div>
                <label style={lbl}>Notes</label>
                <textarea value={form.notes} onChange={(e) => setForm(f => ({ ...f, notes: e.target.value }))} rows={3} style={{ ...inp, resize: "vertical", fontFamily: "inherit" }} />
              </div>
              <div>
                <label style={lbl}>BibTeX</label>
                <textarea value={form.bibtex} onChange={(e) => setForm(f => ({ ...f, bibtex: e.target.value }))} rows={6} style={{ ...inp, resize: "vertical", fontFamily: "monospace", fontSize: 11 }} />
              </div>
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={save} disabled={saving} style={btnPrimary}>{saving ? "Saving…" : "Save"}</button>
                <button onClick={() => setEditing(false)} style={btnSecondary}>Cancel</button>
              </div>
            </div>
          ) : (
            <div>
              {cit.title && <p style={{ margin: "0 0 6px", fontSize: 14, fontWeight: 600, color: "#111827" }}>{cit.title}</p>}
              {cit.authors && <p style={{ margin: "0 0 4px", fontSize: 13, color: "#374151" }}>{cit.authors}</p>}
              <p style={{ margin: "0 0 4px", fontSize: 12, color: "#6b7280" }}>
                {[cit.venue, cit.year].filter(Boolean).join(", ")}
                {cit.doi && <> · <a href={`https://doi.org/${cit.doi}`} target="_blank" rel="noopener noreferrer" style={{ color: "#2563eb" }}>DOI</a></>}
                {cit.url && !cit.doi && <> · <a href={cit.url} target="_blank" rel="noopener noreferrer" style={{ color: "#2563eb" }}>Link</a></>}
              </p>
              {cit.notes && <p style={{ margin: "8px 0 0", fontSize: 12, color: "#6b7280", lineHeight: 1.5, borderLeft: "2px solid #e5e7eb", paddingLeft: 8 }}>{cit.notes}</p>}
              <button onClick={() => setEditing(true)} style={{ ...btnSecondary, marginTop: 10, fontSize: 11, padding: "3px 10px" }}>✎ Edit</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function CitationManager() {
  const { toast } = useToast();
  const [citations, setCitations] = useState<Citation[]>([]);
  const [loading, setLoading] = useState(true);
  const [bibtexInput, setBibtexInput] = useState("");
  const [manualForm, setManualForm] = useState({ key: "", title: "", authors: "", year: "", venue: "", doi: "", url: "", notes: "" });
  const [mode, setMode] = useState<"bibtex" | "manual">("bibtex");
  const [search, setSearch] = useState("");

  useEffect(() => {
    listCitations().then(setCitations).catch(() => toast("Failed to load", "error")).finally(() => setLoading(false));
  }, []);

  const importBibTeX = async () => {
    const parsed = parseBibTeX(bibtexInput);
    if (!parsed.key) { toast("Could not parse BibTeX key", "warning"); return; }
    try {
      const c = await createCitation({
        key: parsed.key!, title: parsed.title ?? "", authors: parsed.authors ?? "",
        year: parsed.year ?? "", venue: parsed.venue ?? "", doi: parsed.doi ?? "",
        url: parsed.url ?? "", bibtex: parsed.bibtex ?? "", notes: "",
      });
      setCitations((prev) => [c, ...prev]); setBibtexInput(""); toast("Citation imported", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Import failed", "error"); }
  };

  const addManual = async () => {
    if (!manualForm.key.trim()) { toast("Citation key is required", "warning"); return; }
    try {
      const c = await createCitation({ ...manualForm, bibtex: "" });
      setCitations((prev) => [c, ...prev]);
      setManualForm({ key: "", title: "", authors: "", year: "", venue: "", doi: "", url: "", notes: "" });
      toast("Citation added", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Failed", "error"); }
  };

  const visible = search
    ? citations.filter((c) => [c.key, c.title, c.authors, c.venue].join(" ").toLowerCase().includes(search.toLowerCase()))
    : citations;

  return (
    <div>
      <h2 style={{ margin: "0 0 0.75rem" }}>Citation Manager</h2>
      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        Store and manage references. Import from BibTeX or add manually.
      </p>

      {/* Add citation */}
      <details style={{ marginBottom: "1.5rem" }}>
        <summary style={{ cursor: "pointer", fontWeight: 600, fontSize: 13, padding: "8px 0" }}>+ Add citation</summary>
        <div style={{ marginTop: 10, padding: "1rem", border: "1px solid #e5e7eb", borderRadius: 8, maxWidth: 600 }}>
          <div style={{ display: "flex", gap: 6, marginBottom: 12 }}>
            <button onClick={() => setMode("bibtex")} style={{ ...btnSmall, background: mode === "bibtex" ? "#1e3a5f" : "#f3f4f6", color: mode === "bibtex" ? "#fff" : "#374151" }}>BibTeX</button>
            <button onClick={() => setMode("manual")} style={{ ...btnSmall, background: mode === "manual" ? "#1e3a5f" : "#f3f4f6", color: mode === "manual" ? "#fff" : "#374151" }}>Manual</button>
          </div>

          {mode === "bibtex" ? (
            <div>
              <label style={lbl}>Paste BibTeX entry</label>
              <textarea value={bibtexInput} onChange={(e) => setBibtexInput(e.target.value)} rows={8}
                style={{ ...inp, fontFamily: "monospace", fontSize: 11, resize: "vertical" }}
                placeholder={"@article{mahadevan1977,\n  author = {Mahadevan, Iravatham},\n  title = {The Indus Script},\n  year = {1977},\n  journal = {...}\n}"} />
              <button onClick={importBibTeX} disabled={!bibtexInput.trim()} style={btnPrimary}>Import BibTeX</button>
            </div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {[["Key *", "key"], ["Title", "title"], ["Authors", "authors"], ["Year", "year"], ["Venue", "venue"], ["DOI", "doi"], ["URL", "url"]].map(([label, field]) => (
                <div key={field}>
                  <label style={lbl}>{label}</label>
                  <input value={(manualForm as Record<string, string>)[field]} onChange={(e) => setManualForm(f => ({ ...f, [field]: e.target.value }))} style={inp} />
                </div>
              ))}
              <button onClick={addManual} style={btnPrimary}>Add Citation</button>
            </div>
          )}
        </div>
      </details>

      {/* Search */}
      <div style={{ marginBottom: "1rem" }}>
        <input placeholder="Search citations…" value={search} onChange={(e) => setSearch(e.target.value)}
          style={{ ...inp, width: "100%", maxWidth: 360 }} />
      </div>

      <div style={{ fontSize: 12, color: "#9ca3af", marginBottom: 8 }}>{visible.length} citations</div>

      {loading && <p style={{ color: "#6b7280", fontSize: 13 }}>Loading…</p>}
      {!loading && visible.length === 0 && <p style={{ color: "#6b7280", fontSize: 13 }}>No citations yet. Import or add one above.</p>}
      {visible.map((c) => (
        <CitationCard key={c.id} cit={c}
          onUpdated={(u) => setCitations((prev) => prev.map((x) => x.id === u.id ? u : x))}
          onDeleted={(id) => setCitations((prev) => prev.filter((x) => x.id !== id))} />
      ))}
    </div>
  );
}

const lbl: React.CSSProperties = { display: "block", fontWeight: 600, fontSize: 12, color: "#374151", marginBottom: 3 };
const inp: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const btnPrimary: React.CSSProperties = { background: "#2563eb", color: "#fff", border: "none", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer", fontWeight: 600 };
const btnSecondary: React.CSSProperties = { background: "#fff", color: "#374151", border: "1px solid #d1d5db", borderRadius: 4, padding: "6px 14px", fontSize: 12, cursor: "pointer" };
const btnSmall: React.CSSProperties = { padding: "3px 10px", border: "1px solid #e5e7eb", borderRadius: 4, cursor: "pointer", fontSize: 11, background: "#f9fafb", color: "#374151" };
