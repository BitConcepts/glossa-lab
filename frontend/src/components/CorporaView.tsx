import { useEffect, useState } from "react";
import { createText, deleteText, updateText, listTexts, TextResponse } from "../api";

interface Props {
  /** Called when user selects a corpus for analysis */
  onSelect?: (id: string, name: string) => void;
}

export function CorporaView({ onSelect }: Props) {
  const [texts, setTexts] = useState<TextResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selected, setSelected] = useState<TextResponse | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [editName, setEditName] = useState("");
  const [editType, setEditType] = useState("");
  const [saving, setSaving] = useState(false);

  // Upload form state
  const [name, setName] = useState("");
  const [corpusType, setCorpusType] = useState("linguistic");
  const [rawContent, setRawContent] = useState("");
  const [delimiter, setDelimiter] = useState("char");
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      setTexts(await listTexts());
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load corpora");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const tokenise = (raw: string): string[] => {
    if (delimiter === "char") return raw.replace(/\s+/g, "").split("");
    if (delimiter === "word") return raw.trim().split(/\s+/);
    // line
    return raw
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);
  };

  const handleUpload = async () => {
    if (!name.trim()) {
      setUploadError("Name is required");
      return;
    }
    const content = tokenise(rawContent);
    if (content.length === 0) {
      setUploadError("Content must not be empty");
      return;
    }
    try {
      setUploading(true);
      setUploadError(null);
      await createText({ name: name.trim(), corpus_type: corpusType, content });
      setName("");
      setRawContent("");
      await load();
    } catch (e) {
      setUploadError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!selected) return;
    setSaving(true);
    try {
      await updateText(selected.id, { name: editName, corpus_type: editType });
      await load();
      setSelected(null);
      setEditMode(false);
    } catch (e) { alert(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };

  // Corpus statistics
  const getStats = (t: TextResponse) => {
    const freq: Record<string, number> = {};
    for (const s of t.content) freq[s] = (freq[s] ?? 0) + 1;
    const total = t.content.length;
    const hapax = Object.values(freq).filter((c) => c === 1).length;
    const top5 = Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, 5);
    return { total, hapax, hapaxFrac: hapax / Math.max(t.alphabet_size, 1), top5 };
  };

  return (
    <div>
      <h2>Corpora</h2>

      {/* Upload panel */}
      <details style={{ marginBottom: "1.5rem" }}>
        <summary style={{ cursor: "pointer", fontWeight: 600 }}>
          + Upload new corpus
        </summary>
        <div
          style={{
            marginTop: "0.75rem",
            padding: "1rem",
            border: "1px solid #e5e7eb",
            borderRadius: 6,
            maxWidth: 560,
          }}
        >
          <Field label="Name">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Moby Dick (English)"
              style={inputStyle}
            />
          </Field>
          <Field label="Corpus type">
            <select
              value={corpusType}
              onChange={(e) => setCorpusType(e.target.value)}
              style={inputStyle}
            >
              <option value="linguistic">linguistic</option>
              <option value="dna">dna</option>
              <option value="code">code</option>
              <option value="ancient">ancient</option>
              <option value="random">random</option>
              <option value="other">other</option>
            </select>
          </Field>
          <Field label="Tokenisation">
            <select
              value={delimiter}
              onChange={(e) => setDelimiter(e.target.value)}
              style={inputStyle}
            >
              <option value="char">Character-level</option>
              <option value="word">Word/token-level</option>
              <option value="line">Line-level</option>
            </select>
          </Field>
          <Field label="Content">
            <textarea
              value={rawContent}
              onChange={(e) => setRawContent(e.target.value)}
              rows={5}
              style={{ ...inputStyle, fontFamily: "monospace", resize: "vertical" }}
              placeholder="Paste text here…"
            />
          </Field>
          {uploadError && (
            <p style={{ color: "#dc2626", margin: "4px 0" }}>{uploadError}</p>
          )}
          <button
            onClick={handleUpload}
            disabled={uploading}
            style={btnStyle}
          >
            {uploading ? "Uploading…" : "Upload"}
          </button>
        </div>
      </details>

      {/* Corpus list */}
      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "#dc2626" }}>{error}</p>}
      {!loading && texts.length === 0 && (
        <p style={{ color: "#6b7280" }}>No corpora yet. Upload one above.</p>
      )}
      {texts.length > 0 && (
        <table style={{ borderCollapse: "collapse", width: "100%", maxWidth: 760 }}>
          <thead>
            <tr>
  {["Name", "Type", "Symbols", "Alphabet", "Created", ""].map((h) => (
                <Th key={h}>{h}</Th>
              ))}
              {onSelect && <Th>Select</Th>}
            </tr>
          </thead>
          <tbody>
            {texts.map((t) => (
              <tr key={t.id}>
                <Td>
                  <span style={{ fontWeight: 500 }}>{t.name}</span>
                  <br />
                  <span style={{ fontSize: 11, color: "#6b7280", fontFamily: "monospace" }}>
                    {t.id.slice(0, 8)}…
                  </span>
                </Td>
                <Td>{t.corpus_type}</Td>
                <Td>{t.content.length.toLocaleString()}</Td>
                <Td>{t.alphabet_size}</Td>
                <Td>{t.created_at.slice(0, 10)}</Td>
                <Td>
                  <span style={{ display: "flex", gap: 4 }}>
                    <button
                      style={{ ...btnStyle, padding: "2px 10px", fontSize: 11 }}
                      onClick={() => {
                        setSelected(t);
                        setEditMode(false);
                        setEditName(t.name);
                        setEditType(t.corpus_type);
                      }}
                    >View</button>
                    <button
                      style={{ background: "none", border: "1px solid #fca5a5", borderRadius: 4, color: "#dc2626", fontSize: 11, padding: "2px 8px", cursor: "pointer" }}
                      onClick={async () => {
                        if (!confirm(`Delete "${t.name}"?`)) return;
                        try { await deleteText(t.id); await load(); if (selected?.id === t.id) setSelected(null); } catch { alert("Delete failed"); }
                      }}
                    >Delete</button>
                  </span>
                </Td>
                {onSelect && (
                  <Td>
                    <button style={{ ...btnStyle, padding: "2px 10px", fontSize: 12 }} onClick={() => onSelect(t.id, t.name)}>Select</button>
                  </Td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Corpus detail panel */}
      {selected && (() => {
        const stats = getStats(selected);
        return (
          <div style={{ marginTop: "1.5rem", border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center",
              padding: "10px 14px", background: "#f9fafb", borderBottom: "1px solid #e5e7eb" }}>
              <strong style={{ fontSize: 14 }}>{selected.name}</strong>
              <div style={{ display: "flex", gap: 8 }}>
                {!editMode && (
                  <button onClick={() => setEditMode(true)}
                    style={{ ...btnStyle, padding: "3px 12px", fontSize: 12, background: "#7c3aed" }}>Edit</button>
                )}
                <button onClick={() => { setSelected(null); setEditMode(false); }}
                  style={{ background: "none", border: "none", cursor: "pointer", fontSize: 18, color: "#6b7280" }}>×</button>
              </div>
            </div>

            <div style={{ padding: "14px 16px" }}>
              {editMode ? (
                <div style={{ display: "flex", flexDirection: "column", gap: 10, maxWidth: 400 }}>
                  <div>
                    <label style={{ display: "block", fontWeight: 600, fontSize: 12, marginBottom: 3 }}>Name</label>
                    <input value={editName} onChange={(e) => setEditName(e.target.value)} style={inputStyle} />
                  </div>
                  <div>
                    <label style={{ display: "block", fontWeight: 600, fontSize: 12, marginBottom: 3 }}>Type</label>
                    <select value={editType} onChange={(e) => setEditType(e.target.value)} style={inputStyle}>
                      {["linguistic","ancient","dna","code","random","other"].map((t) =>
                        <option key={t}>{t}</option>)}
                    </select>
                  </div>
                  <div style={{ display: "flex", gap: 8 }}>
                    <button onClick={handleSaveEdit} disabled={saving} style={btnStyle}>
                      {saving ? "Saving…" : "Save"}
                    </button>
                    <button onClick={() => setEditMode(false)}
                      style={{ ...btnStyle, background: "#6b7280" }}>Cancel</button>
                  </div>
                </div>
              ) : (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
                  <div>
                    <h4 style={{ margin: "0 0 8px", fontSize: 13 }}>Properties</h4>
                    <table style={{ borderCollapse: "collapse", fontSize: 12 }}>
                      <tbody>
                        {[
                          ["ID", selected.id],
                          ["Type", selected.corpus_type],
                          ["Tokens", stats.total.toLocaleString()],
                          ["Alphabet size", selected.alphabet_size.toLocaleString()],
                          ["Hapax count", stats.hapax.toLocaleString()],
                          ["Hapax fraction", `${(stats.hapaxFrac * 100).toFixed(1)}%`],
                          ["Created", selected.created_at.slice(0, 10)],
                        ].map(([k, v]) => (
                          <tr key={k}>
                            <td style={{ padding: "2px 16px 2px 0", color: "#6b7280", fontWeight: 600 }}>{k}</td>
                            <td style={{ padding: "2px 0", fontFamily: "monospace" }}>{v}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div>
                    <h4 style={{ margin: "0 0 8px", fontSize: 13 }}>Top 5 tokens</h4>
                    <table style={{ borderCollapse: "collapse", fontSize: 12 }}>
                      <thead>
                        <tr>
                          <th style={{ textAlign: "left", paddingRight: 12, color: "#374151" }}>Token</th>
                          <th style={{ textAlign: "left", color: "#374151" }}>Count</th>
                        </tr>
                      </thead>
                      <tbody>
                        {stats.top5.map(([tok, cnt]) => (
                          <tr key={tok}>
                            <td style={{ paddingRight: 12, fontFamily: "monospace", fontWeight: 600 }}>{tok}</td>
                            <td>{cnt}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              <details style={{ marginTop: 12 }}>
                <summary style={{ cursor: "pointer", fontSize: 12, color: "#6b7280" }}>Content preview (first 200 tokens)</summary>
                <pre style={{ margin: "8px 0 0", padding: 10, background: "#1e293b", color: "#e2e8f0",
                  borderRadius: 4, fontSize: 10, overflowX: "auto", maxHeight: 120 }}>
                  {selected.content.slice(0, 200).join(" ")}
                  {selected.content.length > 200 ? " …" : ""}
                </pre>
              </details>

              {onSelect && (
                <button onClick={() => onSelect(selected.id, selected.name)}
                  style={{ ...btnStyle, marginTop: 12 }}>Use this corpus</button>
              )}
            </div>
          </div>
        );
      })()}
    </div>
  );
}

function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div style={{ marginBottom: "0.6rem" }}>
      <label style={{ display: "block", fontWeight: 500, marginBottom: 2, fontSize: 13 }}>
        {label}
      </label>
      {children}
    </div>
  );
}

function Th({ children }: { children: React.ReactNode }) {
  return (
    <th
      style={{
        textAlign: "left",
        padding: "4px 12px 4px 0",
        borderBottom: "2px solid #e5e7eb",
        fontSize: 13,
        color: "#374151",
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </th>
  );
}

function Td({ children }: { children: React.ReactNode }) {
  return (
    <td
      style={{
        padding: "5px 12px 5px 0",
        borderBottom: "1px solid #f3f4f6",
        fontSize: 13,
        verticalAlign: "top",
      }}
    >
      {children}
    </td>
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  padding: "5px 8px",
  border: "1px solid #d1d5db",
  borderRadius: 4,
  fontSize: 13,
  boxSizing: "border-box",
};

const btnStyle: React.CSSProperties = {
  background: "#2563eb",
  color: "#fff",
  border: "none",
  borderRadius: 4,
  padding: "6px 16px",
  fontSize: 13,
  cursor: "pointer",
};
