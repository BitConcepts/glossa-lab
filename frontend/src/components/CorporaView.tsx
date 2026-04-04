import { useEffect, useState } from "react";
import { createText, deleteText, listTexts, TextResponse } from "../api";

interface Props {
  /** Called when user selects a corpus for analysis */
  onSelect?: (id: string, name: string) => void;
}

export function CorporaView({ onSelect }: Props) {
  const [texts, setTexts] = useState<TextResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Upload form state
  const [name, setName] = useState("");
  const [corpusType, setCorpusType] = useState("linguistic");
  const [rawContent, setRawContent] = useState("");
  const [delimiter, setDelimiter] = useState("char"); // "char" | "word" | "line"
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
                  <button
                    style={{ background: "none", border: "1px solid #fca5a5", borderRadius: 4, color: "#dc2626", fontSize: 11, padding: "2px 8px", cursor: "pointer" }}
                    onClick={async () => {
                      if (!confirm(`Delete "${t.name}"?`)) return;
                      try { await deleteText(t.id); await load(); } catch { alert("Delete failed"); }
                    }}
                  >Delete</button>
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
