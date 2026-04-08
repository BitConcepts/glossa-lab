/**
 * CorpusSelector — dropdown of available corpora for corpus_id parameters.
 *
 * Used in both the Study Builder Inspector and the Experiment Builder Inspector
 * whenever a parameter is named "corpus_id". Shows all uploaded corpora from
 * the DB plus a "Default Indus corpus" option (uses icit_extracted_corpus.json
 * when corpus_id is blank).
 *
 * Architecture:
 *   Study graph  → [📚 Corpus node (corpus_id)]
 *                     ↓ corpus_id flows downstream
 *                  [🧪 Experiment node] → uses that corpus
 *
 *   Experiment graph → [CorpusReader (corpus_id)] → uses that corpus
 *
 * Setting corpus_id="" uses the default ICIT corpus as fallback.
 */

import { useEffect, useState } from "react";
import { listTexts, type TextResponse } from "../api";

interface Props {
  value: string;
  onChange: (corpusId: string) => void;
  darkMode?: boolean;
}

export function CorpusSelector({ value, onChange, darkMode = true }: Props) {
  const [corpora, setCorpora] = useState<TextResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listTexts()
      .then(setCorpora)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const iStyle: React.CSSProperties = {
    width: "100%",
    boxSizing: "border-box",
    padding: "4px 7px",
    border: `1px solid ${darkMode ? "#334155" : "#d1d5db"}`,
    borderRadius: 4,
    fontSize: 11,
    outline: "none",
    background: darkMode ? "#1e293b" : "#ffffff",
    color: darkMode ? "#e2e8f0" : "#1e293b",
    cursor: "pointer",
  };

  return (
    <select value={value ?? ""} onChange={e => onChange(e.target.value)} style={iStyle}>
      <option value="">
        {loading ? "Loading corpora…" : "Default Indus corpus (ICIT)"}
      </option>
      {corpora.map(c => (
        <option key={c.id} value={c.id}>
          {c.name}
          {c.corpus_type && c.corpus_type !== "linguistic" ? ` [${c.corpus_type}]` : ""}
          {" "}({c.content?.length?.toLocaleString?.() ?? "?"} seqs)
        </option>
      ))}
    </select>
  );
}
