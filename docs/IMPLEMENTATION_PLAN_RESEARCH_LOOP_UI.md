# Implementation Plan: Native Research Loop UI + Dashboard Fixes

## Status: ALL PHASES (1-7) IMPLEMENTED

---

## 1. Dashboard Metrics Fix

### Current State
- **"Experiments" count** shows only saved JSON graph experiments from `experiments/graphs/*.json` — NOT the 15 registered `AtomicNodeDef` nodes
- **"Studies" count** shows database-stored studies, which is correct but may be 0 if no studies have been created through the UI
- Our 15 registered Indus decipherment nodes are available as atomic building blocks in the Experiment Builder palette but don't inflate the dashboard counter

### Fix Options

**Option A: Count atomic nodes separately**
Add a new dashboard tile "Atomic Nodes" that shows the count of registered `AtomicNodeDef` entries. This keeps the existing "Experiments" count accurate (saved graphs) while surfacing the atomic node count.

**Option B: Include atomic nodes in experiments count**
Modify `_graph_experiment_ids()` in `dashboard.py` to also count `ATOMIC_NODES` from the registry. This would show a higher number but conflates two different things.

**Recommendation: Option A** — Add a separate counter. The two concepts (saved graph experiments vs registered atomic nodes) are genuinely different.

### Implementation
```python
# In dashboard.py, add:
def _atomic_node_count() -> int:
    from glossa_lab.experiment_graph import ATOMIC_NODES
    return len(ATOMIC_NODES)
```
```tsx
// In DashboardView.tsx, add tile:
<CounterTile label="Atomic nodes" value={data.n_atomic_nodes} emoji="⚛️"
  sub="registered" onClick={() => navigate("experiments")} />
```

---

## 2. Integrated Research Loop as Native UI Feature

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Research Loop Panel                        │
│                                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  MINE   │→ │ ANALYZE │→ │REGISTER │→ │ EXECUTE │→ ...   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                               │
│  [▶ Start Loop]  [⏸ Pause]  [■ Stop]  Cycles: [15 ▾]       │
│                                                               │
│  ┌─ Cycle Progress ──────────────────────────────────────┐  │
│  │ C1 ████████████ rare_sign_context → site_formula  ✓   │  │
│  │ C2 ████████████ compound_morph → motif_title      ✓   │  │
│  │ C3 ████████░░░░ seal_owner → suffix_chain         ⏳  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  Papers mined: 972    Insights: 35    Experiments: 15        │
└─────────────────────────────────────────────────────────────┘
```

### Backend Changes

1. **New API endpoint**: `POST /api/v1/research-loop/start`
   - Parameters: `max_cycles`, `gap_topics` (list), `experiment_templates` (list)
   - Returns: SSE stream with cycle-by-cycle progress updates
   - Internally calls the same functions as `integrated_research_loop.py`

2. **New API endpoint**: `GET /api/v1/research-loop/status`
   - Returns current loop state (running/paused/stopped, cycle count, results)

3. **New API endpoint**: `POST /api/v1/research-loop/stop`
   - Graceful stop at end of current cycle

4. **Pipeline class**: `glossa_lab/pipelines/research_loop.py`
   - Move core logic from `backend/scripts/integrated_research_loop.py`
   - Add persistent state (papers_seen, history) via database
   - Add SSE event emission for real-time progress

### Frontend Changes

1. **New component**: `ResearchLoopPanel.tsx`
   - Cycle-by-cycle progress display
   - Start/pause/stop controls
   - Gap topic and experiment template selectors
   - Cumulative metrics (papers, insights, experiments)
   - Auto-scrolling experiment verdict log

2. **Dashboard integration**: Add to `DashboardView.tsx` below DeciphermentPanel
   - Show last loop run summary
   - Quick-start button for new loop

3. **Experiment Builder integration**: Add "Research Loop" as a meta-node
   - Can be wired into larger experiment graphs
   - Output ports: papers_count, insights_count, experiment_results

### Should It Work With Auto-Decipher Loop?

**Yes, but as complementary tools, not merged.**

The two loops serve different purposes:

| Feature | Auto-Decipher Loop | Integrated Research Loop |
|---------|-------------------|------------------------|
| **Goal** | Push convergence channels from weak→strong | Mine literature + run diverse experiments |
| **Input** | Current convergence state | Current research gaps |
| **Experiments** | 10 focused channel tests | 15 diverse corpus analyses |
| **Mining** | Channel-specific queries | Gap-specific queries |
| **Termination** | All channels strong (early stop) | Max cycles or plateau |

**Integration point**: The Research Loop should feed the Auto-Decipher Loop:
1. Research Loop mines new evidence → extracts insights
2. If an insight suggests a convergence channel test → trigger Auto-Decipher
3. Auto-Decipher upgrades a channel → Research Loop skips that gap next cycle

### Implementation Path

1. **Phase 1** ✅ (backend): Pipeline class at `pipelines/research_loop.py` + API endpoints at `api/research_loop.py`
2. **Phase 2** ✅ (API): SSE streaming, status, stop, results endpoints registered in `main.py`
3. **Phase 3** ✅ (dashboard): Atomic node counter + `ResearchLoopPanel.tsx` in `DashboardView.tsx`
4. **Phase 4** ✅ (frontend): `ResearchLoopPanel.tsx` with Start/Stop, SSE streaming, metrics row
5. **Phase 5** ✅ (Experiment Builder): `ResearchLoopRunner` registered as atomic node in `experiment_graph.py`
6. **Phase 6** ✅ (intelligence): `INSIGHT_TO_EXPERIMENTS` mapping; `_select_experiment()` picks experiments based on mined insight types with round-robin fallback
7. **Phase 7** ✅ (persistence): Schema V21 `research_loop_state` table; `save_research_loop_state()`/`load_research_loop_state()` in `database.py`; `ResearchLoop` auto-loads/saves via `db` parameter

---

## 3. Files Reference

| File | Purpose |
|------|---------|
| `backend/scripts/integrated_research_loop.py` | Current standalone script |
| `backend/scripts/auto_decipher_loop.py` | Convergence-focused loop |
| `backend/glossa_lab/experiment_graph_phase322_362.py` | 15 registered graph nodes |
| `docs/INTEGRATED_RESEARCH_LOOP.md` | Feature specification |
| `docs/IMPLEMENTATION_PLAN_RESEARCH_LOOP_UI.md` | This file |
