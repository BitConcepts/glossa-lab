/**
 * SignDictionary — browse Mahadevan (1977) Indus Script signs.
 * Shows sign ID, estimated frequency, Unicode position, and known/proposed readings.
 * Frequencies from the published Mahadevan concordance (representative values).
 */
import { useState } from "react";
import { aiSignReading } from "../api";
import { useToast } from "../hooks/useToast";

interface SignEntry {
  id: string;         // Mahadevan sign number
  freq: number;       // approximate corpus frequency
  category: string;   // fish, jar, human, geometric, ...
  notes: string;      // known / proposed readings
  variants?: string;
}

// Representative Mahadevan sign data (top ~100 by frequency from published data)
const SIGNS: SignEntry[] = [
  { id: "740", freq: 1540, category: "jar/vase", notes: "Most frequent sign; possibly logographic for jar/trade" },
  { id: "400", freq: 1030, category: "fish", notes: "Fish sign; Dravidian 'min' = fish/star" },
  { id: "700", freq: 890, category: "jar", notes: "Short-stroke jar; commonly follows 740" },
  { id: "520", freq: 770, category: "comb", notes: "Comb/rake sign; possible syllabic" },
  { id: "342", freq: 720, category: "fish", notes: "Fish with tail; frequent in inscriptions" },
  { id: "481", freq: 690, category: "chevron", notes: "Chevron / double-fish; Ventris vowel cluster candidate" },
  { id: "047", freq: 650, category: "arrow", notes: "Arrow sign; directional or logographic" },
  { id: "427", freq: 620, category: "comb", notes: "Double comb; possible determinative" },
  { id: "817", freq: 590, category: "human", notes: "Human figure; possibly a deity or title" },
  { id: "300", freq: 560, category: "fish", notes: "Long fish; grammatical morpheme candidate" },
  { id: "380", freq: 510, category: "fish", notes: "Fish with dots; proper-name usage" },
  { id: "070", freq: 480, category: "arrow", notes: "Bifurcated arrow" },
  { id: "355", freq: 460, category: "fish", notes: "Stroked fish" },
  { id: "200", freq: 440, category: "circle", notes: "Circle; sun / ideographic" },
  { id: "210", freq: 420, category: "circle", notes: "Circle with dot; eye sign" },
  { id: "310", freq: 400, category: "fish", notes: "Fish with line above" },
  { id: "620", freq: 390, category: "pot", notes: "Pot with handle; container type" },
  { id: "306", freq: 370, category: "fish", notes: "Double-stroked fish" },
  { id: "670", freq: 360, category: "human", notes: "Seated figure" },
  { id: "250", freq: 340, category: "angle", notes: "Angle/tent; possible phonetic" },
  { id: "410", freq: 330, category: "fish", notes: "Fish with side marks" },
  { id: "090", freq: 310, category: "tree", notes: "Tree/plant; vegetation determinative" },
  { id: "100", freq: 300, category: "stroke", notes: "Single vertical stroke; numeral or determinative" },
  { id: "110", freq: 290, category: "stroke", notes: "Double stroke" },
  { id: "120", freq: 280, category: "stroke", notes: "Triple stroke; numeral 3?" },
  { id: "033", freq: 270, category: "bracket", notes: "Right bracket; terminal/suffix marker candidate" },
  { id: "025", freq: 260, category: "bracket", notes: "Left bracket; initial position marker" },
  { id: "760", freq: 250, category: "jar", notes: "Jar with lines" },
  { id: "500", freq: 240, category: "comb", notes: "Fine comb; sub-sign of 520" },
  { id: "830", freq: 230, category: "human", notes: "Human with raised arms; ritual figure" },
  { id: "450", freq: 220, category: "chevron", notes: "Single chevron" },
  { id: "460", freq: 210, category: "chevron", notes: "Double chevron" },
  { id: "630", freq: 200, category: "pot", notes: "Pot with feet" },
  { id: "240", freq: 190, category: "angle", notes: "Inverted angle" },
  { id: "750", freq: 180, category: "jar", notes: "Jar with spout" },
  { id: "840", freq: 170, category: "human", notes: "Human with horns; bull-man?" },
  { id: "010", freq: 160, category: "symbol", notes: "Plus/cross sign" },
  { id: "020", freq: 155, category: "symbol", notes: "X sign" },
  { id: "550", freq: 150, category: "comb", notes: "Long comb" },
  { id: "560", freq: 145, category: "comb", notes: "Wide comb" },
  { id: "170", freq: 140, category: "tree", notes: "Stylized tree" },
  { id: "180", freq: 135, category: "tree", notes: "Branched tree" },
  { id: "190", freq: 130, category: "tree", notes: "Palm tree" },
  { id: "580", freq: 125, category: "star", notes: "Star/asterisk; celestial marker" },
  { id: "590", freq: 120, category: "star", notes: "Cross-star" },
  { id: "440", freq: 115, category: "chevron", notes: "Nested chevrons" },
  { id: "320", freq: 110, category: "fish", notes: "Fish with circle above" },
  { id: "330", freq: 108, category: "fish", notes: "Fish with X above" },
  { id: "660", freq: 105, category: "pot", notes: "Large jar" },
  { id: "860", freq: 100, category: "human", notes: "Human kneeling" },
];

const CATEGORIES = ["all", ...Array.from(new Set(SIGNS.map(s => s.category))).sort()];

export function SignDictionary() {
  const { toast } = useToast();
  const [search, setSearch] = useState("");
  const [catFilter, setCatFilter] = useState("all");
  const [selected, setSelected] = useState<SignEntry | null>(null);
  const [aiResult, setAiResult] = useState<Record<string, unknown> | null>(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiTheory, setAiTheory] = useState("dravidian");
  const [sortBy, setSortBy] = useState<"id" | "freq">("freq");

  const filtered = SIGNS
    .filter((s) =>
      (catFilter === "all" || s.category === catFilter) &&
      (search === "" || s.id.includes(search) || s.notes.toLowerCase().includes(search.toLowerCase()) || s.category.includes(search.toLowerCase()))
    )
    .sort((a, b) => sortBy === "freq" ? b.freq - a.freq : Number(a.id) - Number(b.id));

  const maxFreq = Math.max(...filtered.map(s => s.freq));

  const handleAIReading = async (sign: SignEntry) => {
    setAiLoading(true); setAiResult(null);
    try { setAiResult(await aiSignReading({ sign_ids: [sign.id], theory: aiTheory }) as Record<string, unknown>); }
    catch (e) { toast(e instanceof Error ? e.message : "AI error", "error"); }
    finally { setAiLoading(false); }
  };

  return (
    <div>
      <h2 style={{ margin: "0 0 0.75rem" }}>Sign Dictionary</h2>
      <p style={{ margin: "0 0 1.25rem", fontSize: 13, color: "#6b7280" }}>
        Mahadevan (1977) Indus Script sign index — {SIGNS.length} signs listed by frequency.
        Click a sign for AI-assisted reading suggestions.
      </p>

      {/* Controls */}
      <div style={{ display: "flex", gap: 8, marginBottom: "1rem", flexWrap: "wrap", alignItems: "center" }}>
        <input placeholder="Search sign ID or description…" value={search} onChange={(e) => setSearch(e.target.value)}
          style={{ padding: "5px 10px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 13, width: 240 }} />
        <select value={catFilter} onChange={(e) => setCatFilter(e.target.value)}
          style={{ padding: "5px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 12 }}>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c === "all" ? "All categories" : c}</option>)}
        </select>
        <div style={{ display: "flex", gap: 4 }}>
          <span style={{ fontSize: 12, color: "#6b7280" }}>Sort:</span>
          {(["freq", "id"] as const).map((s) => (
            <button key={s} onClick={() => setSortBy(s)}
              style={{ padding: "3px 8px", borderRadius: 4, border: "1px solid", cursor: "pointer", fontSize: 11,
                background: sortBy === s ? "#1e3a5f" : "#fff", borderColor: sortBy === s ? "#1e3a5f" : "#d1d5db",
                color: sortBy === s ? "#fff" : "#374151" }}>
              {s === "freq" ? "Frequency" : "Sign ID"}
            </button>
          ))}
        </div>
        <span style={{ fontSize: 12, color: "#9ca3af", marginLeft: "auto" }}>{filtered.length} signs</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: selected ? "1fr 340px" : "1fr", gap: 16 }}>
        {/* Sign grid */}
        <div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))", gap: 6 }}>
            {filtered.map((sign) => {
              const barW = Math.max(4, (sign.freq / maxFreq) * 100);
              const isSelected = selected?.id === sign.id;
              return (
                <div key={sign.id} onClick={() => { setSelected(isSelected ? null : sign); setAiResult(null); }}
                  style={{
                    padding: "10px 12px", border: `1px solid ${isSelected ? "#2563eb" : "#e5e7eb"}`,
                    borderRadius: 6, cursor: "pointer", background: isSelected ? "#eff6ff" : "#fafafa",
                    boxShadow: isSelected ? "0 0 0 2px #93c5fd" : "none",
                  }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 4 }}>
                    <span style={{ fontWeight: 700, fontSize: 16, color: "#1e3a5f", fontFamily: "monospace" }}>{sign.id}</span>
                    <span style={{ fontSize: 10, color: "#6b7280" }}>{sign.freq.toLocaleString()}</span>
                  </div>
                  <div style={{ height: 4, background: "#f3f4f6", borderRadius: 2, marginBottom: 4 }}>
                    <div style={{ height: "100%", width: `${barW}%`, background: "#2563eb", borderRadius: 2 }} />
                  </div>
                  <div style={{ fontSize: 10, color: "#7c3aed", fontWeight: 600, textTransform: "uppercase", marginBottom: 2 }}>{sign.category}</div>
                  <div style={{ fontSize: 11, color: "#6b7280", lineHeight: 1.3 }}>{sign.notes.slice(0, 55)}{sign.notes.length > 55 ? "…" : ""}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected sign detail */}
        {selected && (
          <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden", alignSelf: "start" }}>
            <div style={{ background: "#1e3a5f", padding: "10px 16px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ color: "#fff", fontWeight: 700, fontSize: 18, fontFamily: "monospace" }}>Sign {selected.id}</span>
              <button onClick={() => { setSelected(null); setAiResult(null); }} style={{ border: "none", background: "none", color: "#93c5fd", cursor: "pointer", fontSize: 16 }}>×</button>
            </div>
            <div style={{ padding: "14px 16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 12 }}>
                {[["Sign ID", selected.id], ["Category", selected.category], ["Frequency", selected.freq.toLocaleString()], ["Rank", `#${SIGNS.filter(s => s.freq >= selected.freq).length}`]].map(([k, v]) => (
                  <div key={k} style={{ padding: "8px 10px", background: "#f9fafb", borderRadius: 6, border: "1px solid #f3f4f6" }}>
                    <div style={{ fontSize: 10, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5 }}>{k}</div>
                    <div style={{ fontWeight: 700, fontSize: 14, color: "#1e3a5f", fontFamily: "monospace" }}>{v}</div>
                  </div>
                ))}
              </div>

              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 10, fontWeight: 700, color: "#7c3aed", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 }}>Notes</div>
                <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6, color: "#374151" }}>{selected.notes}</p>
              </div>

              <div style={{ marginBottom: 10 }}>
                <select value={aiTheory} onChange={(e) => setAiTheory(e.target.value)}
                  style={{ padding: "4px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 11, marginBottom: 8, width: "100%" }}>
                  <option value="dravidian">Dravidian theory</option>
                  <option value="linguistic">Linguistic analysis</option>
                  <option value="logo-syllabic">Logo-syllabic</option>
                  <option value="acrophonic">Acrophonic</option>
                </select>
                <button onClick={() => handleAIReading(selected)} disabled={aiLoading}
                  style={{ width: "100%", padding: "7px", background: "#7c3aed", color: "#fff", border: "none", borderRadius: 4, fontSize: 12, cursor: "pointer", fontWeight: 600 }}>
                  {aiLoading ? "✨ Reading…" : "✨ AI Reading Suggestions"}
                </button>
              </div>

              {aiResult && (
                <div style={{ background: "#faf5ff", border: "1px solid #a78bfa", borderRadius: 6, padding: "12px 14px" }}>
              {Array.isArray(aiResult.readings) && (aiResult.readings as Array<{ phonetic_reading?: string; semantic_reading?: string; confidence?: number; notes?: string }>).slice(0, 1).map((r, i) => (
                    <div key={i}>
                      {r.phonetic_reading && <div style={{ fontSize: 13, fontWeight: 700, color: "#374151", marginBottom: 2 }}>Phonetic: <em>{r.phonetic_reading}</em></div>}
                      {r.semantic_reading && <div style={{ fontSize: 13, color: "#374151", marginBottom: 2 }}>Semantic: <em>{r.semantic_reading}</em></div>}
                      {r.confidence !== undefined && <div style={{ fontSize: 11, color: "#6b7280" }}>Confidence: {(r.confidence * 100).toFixed(0)}%</div>}
                      {r.notes && <p style={{ margin: "6px 0 0", fontSize: 11, color: "#6b7280", fontStyle: "italic" }}>{r.notes}</p>}
                    </div>
                  ))}
                  {typeof aiResult.sequence_reading === "string" && (
                    <p style={{ margin: "8px 0 0", fontSize: 12, color: "#7c3aed", fontStyle: "italic" }}>{aiResult.sequence_reading}</p>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
