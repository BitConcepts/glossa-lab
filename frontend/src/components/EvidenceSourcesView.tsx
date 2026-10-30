/**
 * Evidence & sources (Spec 081 step 6, FR-012): the consolidation of
 * the program's source material — the Library (registered papers and
 * hypothesis models), Citations, Correspondence, and Notebooks
 * (Q10: notebooks are the fourth tab of this surface).
 *
 * This is the register's doorway: sources enter the program's work
 * here, by registration and extraction — claims themselves are read
 * on the Claims surface, and nothing on this surface states a
 * verdict. The legacy citations / correspondence / notebooks routes
 * land on their tabs (the shell stashes the requested tab).
 */
import { useState } from "react";
import { CitationManager } from "./CitationManager";
import { CorrespondenceView } from "./CorrespondenceView";
import { EvidenceLibrary } from "./EvidenceLibrary";
import { ResearchNotebook } from "./ResearchNotebook";
import { PageHead, palette, TabsRow } from "./ui081";

type EvidenceTab = "library" | "citations" | "correspondence" | "notebooks";

const TABS: { id: EvidenceTab; label: string }[] = [
  { id: "library", label: "📚 Library" },
  { id: "citations", label: "Citations" },
  { id: "correspondence", label: "Correspondence" },
  { id: "notebooks", label: "Notebooks" },
];

function initialTab(): EvidenceTab {
  try {
    const hint = sessionStorage.getItem("glossa_evidence_tab");
    if (hint === "citations" || hint === "correspondence" || hint === "notebooks") {
      sessionStorage.removeItem("glossa_evidence_tab");
      return hint;
    }
  } catch { /* */ }
  return "library";
}

export function EvidenceSourcesView({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const [tab, setTab] = useState<EvidenceTab>(initialTab);

  return (
    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      <PageHead
        p={p}
        title="Evidence & sources"
        lede="Everything the program reads, in one place. Registering a source here is what makes it available to extraction and the research loop — no source off this list is quietly used."
      />
      <TabsRow p={p} tabs={TABS} active={tab} onSelect={setTab} />
      <div style={{ marginTop: 16 }}>
        {tab === "library" && <EvidenceLibrary darkMode={darkMode} />}
        {tab === "citations" && <CitationManager />}
        {tab === "correspondence" && <CorrespondenceView />}
        {tab === "notebooks" && <ResearchNotebook />}
      </div>
    </div>
  );
}
