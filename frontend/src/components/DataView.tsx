/**
 * Data (Spec 081 step 6, T018): the program's data surface — corpora
 * and anchor sets as peer tabs. The anchor-set editor was promoted
 * out of the corpora view, where it sat as an afterthought at the
 * bottom of the page; here it is a named peer (and labelled
 * user-defined sets only, per D1).
 */
import { useState } from "react";
import { AnchorSetsView } from "./AnchorSetsView";
import { CorporaView } from "./CorporaView";
import { PageHead, palette, TabsRow } from "./ui081";

type DataTab = "corpora" | "anchors";

const TABS: { id: DataTab; label: string }[] = [
  { id: "corpora", label: "Corpora" },
  { id: "anchors", label: "Anchor sets" },
];

export function DataView({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const [tab, setTab] = useState<DataTab>("corpora");

  return (
    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      <PageHead
        p={p}
        title="Data"
        lede="The texts and sets the program's work runs on. What is registered here is what the analysis and the loop can see — nothing else is quietly in scope."
      />
      <TabsRow p={p} tabs={TABS} active={tab} onSelect={setTab} />
      {tab === "corpora" && <CorporaView />}
      {tab === "anchors" && <AnchorSetsView />}
    </div>
  );
}
