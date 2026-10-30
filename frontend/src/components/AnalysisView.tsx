/**
 * Analysis (Spec 081 step 6, T018; Q5): one nav item, three tabs —
 * Entropy, Signs, Timeline. The three views were separate top-level
 * routes before the redesign; their route ids still resolve here
 * with the matching tab open (the shell passes initialTab).
 */
import { useState } from "react";
import { EntropyDashboard } from "./EntropyDashboard";
import { SignsView } from "./SignsView";
import { TimelineView } from "./TimelineView";
import { PageHead, palette, TabsRow } from "./ui081";

type AnalysisTab = "entropy" | "signs" | "timeline";

const TABS: { id: AnalysisTab; label: string }[] = [
  { id: "entropy", label: "Entropy" },
  { id: "signs", label: "Signs" },
  { id: "timeline", label: "Timeline" },
];

export function AnalysisView({
  darkMode,
  initialTab,
  onNavigate,
}: {
  darkMode: boolean;
  initialTab: AnalysisTab;
  onNavigate: (view: string) => void;
}) {
  const p = palette(darkMode);
  const [tab, setTab] = useState<AnalysisTab>(initialTab);

  return (
    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      <PageHead
        p={p}
        title="Analysis"
        lede="The program's instruments, in one place. Each tab is a reading of the data — a reading is evidence for a claim, never a verdict by itself."
      />
      <TabsRow p={p} tabs={TABS} active={tab} onSelect={setTab} />
      {tab === "entropy" && <EntropyDashboard />}
      {tab === "signs" && <SignsView />}
      {tab === "timeline" && <TimelineView onNavigate={onNavigate} />}
    </div>
  );
}
