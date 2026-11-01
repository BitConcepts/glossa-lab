/**
 * AnchorSetsView — the Data surface's anchor-sets tab (Spec 081
 * step 6): the editor promoted out of CorporaView to a peer of the
 * corpora list, per tasks.md T018.
 *
 * These are USER-DEFINED sets only (D1): sets a person creates here
 * for their own comparisons. They are not the program's recorded
 * anchor evidence and are never presented as it.
 */
import { useEffect, useState } from "react";
import {
  createAnchorSet,
  deleteAnchorSet,
  listAnchorSets,
  type AnchorPair,
  type AnchorSet,
} from "../api";
import { useToast } from "../hooks/useToast";

const inputStyle: React.CSSProperties = { width: "100%", padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, boxSizing: "border-box", display: "block" };
const labelStyle: React.CSSProperties = { display: "block", fontWeight: 600, fontSize: 12, color: "#374151", marginBottom: 3 };
const btnSmall: React.CSSProperties = { padding: "3px 10px", border: "1px solid #e5e7eb", borderRadius: 4, cursor: "pointer", fontSize: 11, background: "#f9fafb", color: "#374151" };
const btnMini: React.CSSProperties = { padding: "2px 7px", border: "1px solid #e5e7eb", borderRadius: 4, cursor: "pointer", fontSize: 10, background: "#f9fafb", color: "#374151" };

export function AnchorSetsView() {
  return (
    <div>
      <div style={{ fontSize: 12, color: "#6b7280", marginBottom: 10, maxWidth: "68ch" }}>
        User-defined sets only — sets created here for comparison work. The program's
        recorded anchor evidence lives with the program's data, not in this editor.
      </div>
      <AnchorSetEditor />
    </div>
  );
}

// ── Anchor Set Editor ───────────────────────────────────────────────────────────────

function AnchorSetEditor() {
  const { toast } = useToast();
  const [sets, setSets] = useState<AnchorSet[]>([]);
  const [loading, setLoading] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [newName, setNewName] = useState("");
  const [newLang, setNewLang] = useState("");
  const [pairInput, setPairInput] = useState(""); // cipher<TAB>target per line

  const load = async () => {
    setLoading(true);
    try { setSets(await listAnchorSets()); }
    catch (e) { toast(e instanceof Error ? e.message : "Failed to load", "error"); }
    finally { setLoading(false); }
  };

  const parsePairs = (raw: string): AnchorPair[] =>
    raw.split("\n").map(l => l.trim()).filter(Boolean).map(l => {
      const [cipher, target, confidence, ...noteParts] = l.split(/\s+|\t/);
      return { cipher: cipher ?? "", target: target ?? "",
        confidence: (confidence ?? "high") as "high" | "medium" | "low",
        note: noteParts.join(" ") };
    }).filter(p => p.cipher && p.target);

  const handleCreate = async () => {
    if (!newName.trim()) { toast("Name required", "warning"); return; }
    try {
      const s = await createAnchorSet({ name: newName.trim(), language: newLang.trim(),
        pairs: parsePairs(pairInput) });
      setSets(prev => [s, ...prev]);
      setShowNew(false); setNewName(""); setNewLang(""); setPairInput("");
      toast("Anchor set created", "success");
    } catch (e) { toast(e instanceof Error ? e.message : "Create failed", "error"); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm("Delete this anchor set?")) return;
    try { await deleteAnchorSet(id); setSets(prev => prev.filter(s => s.id !== id)); }
    catch (e) { toast(e instanceof Error ? e.message : "Delete failed", "error"); }
  };

  useEffect(() => { void load(); }, []);

  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <div style={{ fontWeight: 600, fontSize: 13, padding: "8px 0", color: "#7c3aed" }}>
        ⚓ Anchor Sets ({sets.length})
      </div>
      <div style={{ marginTop: 10, padding: "1rem", border: "1px solid #ede9fe", borderRadius: 8, background: "#faf5ff" }}>
        <div style={{ display: "flex", gap: 8, marginBottom: 10 }}>
          <button onClick={() => setShowNew(s => !s)} style={{ ...btnSmall, background: "#7c3aed", color: "#fff", border: "none" }}>+ New Set</button>
          <button onClick={() => void load()} style={btnSmall}>⟳ Refresh</button>
        </div>
        {showNew && (
          <div style={{ padding: 12, border: "1px solid #a78bfa", borderRadius: 6, marginBottom: 12, background: "#fff" }}>
            <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
              <div style={{ flex: 2 }}>
                <label style={labelStyle}>Set Name</label>
                <input value={newName} onChange={e => setNewName(e.target.value)}
                  placeholder="e.g. Fuls Ugaritic Anchors" style={inputStyle} />
              </div>
              <div style={{ flex: 1 }}>
                <label style={labelStyle}>Language (optional)</label>
                <input value={newLang} onChange={e => setNewLang(e.target.value)}
                  placeholder="e.g. Ugaritic" style={inputStyle} />
              </div>
            </div>
            <div style={{ marginBottom: 8 }}>
              <label style={labelStyle}>Anchor Pairs (one per line: cipher target confidence note)</label>
              <textarea value={pairInput} onChange={e => setPairInput(e.target.value)}
                rows={5} style={{ ...inputStyle, fontFamily: "monospace", fontSize: 11, resize: "vertical" }}
                placeholder={"004 T high Fuls verified\n066 m high Fuls verified\n208 n high Fuls verified"} />
              <div style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>Format: cipher_sign target confidence(high/medium/low) note</div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={() => void handleCreate()} style={{ ...btnSmall, background: "#7c3aed", color: "#fff", border: "none" }}>Create</button>
              <button onClick={() => setShowNew(false)} style={btnSmall}>Cancel</button>
            </div>
          </div>
        )}
        {loading && <p style={{ fontSize: 13, color: "#6b7280" }}>Loading…</p>}
        {sets.length === 0 && !loading && <p style={{ fontSize: 13, color: "#6b7280" }}>No anchor sets yet. Create one above.</p>}
        {sets.map(s => (
          <div key={s.id} style={{ border: "1px solid #ede9fe", borderRadius: 6, padding: "8px 12px",
            marginBottom: 6, background: "#fff" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <div style={{ flex: 1 }}>
                <span style={{ fontWeight: 600, fontSize: 12 }}>{s.name}</span>
                {s.language && <span style={{ fontSize: 11, color: "#7c3aed", marginLeft: 6 }}>{s.language}</span>}
                <span style={{ fontSize: 11, color: "#9ca3af", marginLeft: 6 }}>{s.pairs.length} pairs</span>
              </div>
              <button onClick={() => handleDelete(s.id)}
                style={{ ...btnMini, color: "#dc2626", borderColor: "#fca5a5" }}>Delete</button>
            </div>
            {s.pairs.length > 0 && (
              <div style={{ marginTop: 4, display: "flex", gap: 4, flexWrap: "wrap" }}>
                {s.pairs.slice(0, 8).map((p, i) => (
                  <span key={i} style={{ fontSize: 10, padding: "1px 5px", borderRadius: 4,
                    background: p.confidence === "high" ? "#d1fae5" : p.confidence === "medium" ? "#fef3c7" : "#fee2e2",
                    color: "#374151" }}>
                    {p.cipher}→{p.target}
                  </span>
                ))}
                {s.pairs.length > 8 && <span style={{ fontSize: 10, color: "#9ca3af" }}>+{s.pairs.length - 8} more</span>}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
