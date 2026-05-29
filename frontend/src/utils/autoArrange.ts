/**
 * Shared graph auto-arrange utility.
 *
 * Implements a layered topological layout (Kahn topological sort +
 * longest-path layer assignment) used by both the Experiment Builder
 * and the Study Builder to tidy up node positions.
 *
 * Supports a nodeHeightFn option so callers can supply per-node heights
 * based on their port counts, preventing vertical overlap on tall nodes.
 */

import type { Edge, Node } from "@xyflow/react";

const SNAP    = 15;
/** Horizontal gap between left edge of one column and left edge of the next.
 *  Must be > max node width (280px) + desired breathing room. */
const COL_GAP = 360;
/** Vertical gap between the bottom of one node and the top of the next
 *  within the same column (used when nodeHeightFn is provided). */
const ROW_GAP = 48;
/** Fallback row height when no nodeHeightFn is supplied (legacy path). */
const ROW_H_FALLBACK = 180;
const OX      = 60;
const OY      = 60;

export interface AutoArrangeOptions<T> {
  /** Return the rendered pixel height for a node given its data.
   *  When omitted, falls back to a fixed row height. */
  nodeHeightFn?: (data: T) => number;
}

export function autoArrange<T extends Record<string, unknown>>(
  nodes: Node<T>[],
  edges: Edge[],
  options?: AutoArrangeOptions<T>,
): Node<T>[] {
  if (nodes.length === 0) return nodes;

  const heightOf = options?.nodeHeightFn
    ? (n: Node<T>) => Math.max(60, options.nodeHeightFn!(n.data))
    : () => ROW_H_FALLBACK;

  const children: Record<string, string[]> = {};
  const parents:  Record<string, string[]> = {};
  for (const n of nodes) { children[n.id] = []; parents[n.id] = []; }
  for (const e of edges) {
    if (e.source in children && e.target in parents) {
      if (!children[e.source].includes(e.target)) children[e.source].push(e.target);
      if (!parents[e.target].includes(e.source))  parents[e.target].push(e.source);
    }
  }

  // Kahn topological sort
  const inDeg: Record<string, number> = {};
  for (const n of nodes) inDeg[n.id] = parents[n.id].length;
  const queue   = nodes.filter(n => inDeg[n.id] === 0).map(n => n.id);
  const visited = new Set(queue);
  const topo: string[] = [];
  let qi = 0;
  while (qi < queue.length) {
    const nid = queue[qi++];
    topo.push(nid);
    for (const c of children[nid]) {
      inDeg[c]--;
      if (inDeg[c] === 0 && !visited.has(c)) { visited.add(c); queue.push(c); }
    }
  }
  for (const n of nodes) if (!visited.has(n.id)) topo.push(n.id); // cycles

  // Longest-path layer assignment
  const layer: Record<string, number> = {};
  for (const nid of topo) {
    layer[nid] = 0;
    for (const par of parents[nid])
      if (par in layer) layer[nid] = Math.max(layer[nid], layer[par] + 1);
  }

  // Group by layer; build index for height lookup
  const byLayer: Record<number, string[]> = {};
  for (const nid of topo) {
    const l = layer[nid] ?? 0;
    (byLayer[l] = byLayer[l] ?? []).push(nid);
  }
  const nodeById = Object.fromEntries(nodes.map(n => [n.id, n]));

  // Compute column total heights (sum of node heights + gaps)
  const colTotalH = (group: string[]) =>
    group.reduce((acc, nid) => acc + heightOf(nodeById[nid]), 0)
    + Math.max(0, group.length - 1) * ROW_GAP;

  const maxTotalH = Math.max(...Object.values(byLayer).map(colTotalH), 0);

  const posMap: Record<string, { x: number; y: number }> = {};
  for (const [lStr, group] of Object.entries(byLayer)) {
    const l      = Number(lStr);
    const thisH  = colTotalH(group);
    // Centre this column relative to the tallest column
    let curY = OY + (maxTotalH - thisH) / 2;
    group.forEach((nid) => {
      posMap[nid] = {
        x: Math.round((OX + l * COL_GAP) / SNAP) * SNAP,
        y: Math.round(curY / SNAP) * SNAP,
      };
      curY += heightOf(nodeById[nid]) + ROW_GAP;
    });
  }

  return nodes.map(n => ({ ...n, position: posMap[n.id] ?? n.position }));
}
