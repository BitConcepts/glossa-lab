/**
 * Shared graph auto-arrange utility.
 *
 * Implements a layered topological layout (Kahn topological sort +
 * longest-path layer assignment) used by both the Experiment Builder
 * and the Study Builder to tidy up node positions.
 */

import type { Edge, Node } from "@xyflow/react";

const SNAP  = 15;
const COL_W = 255;   // horizontal spacing between layers
const ROW_H = 150;   // vertical spacing within a layer
const OX    = 60;
const OY    = 60;

export function autoArrange<T extends Record<string, unknown>>(
  nodes: Node<T>[],
  edges: Edge[],
): Node<T>[] {
  if (nodes.length === 0) return nodes;

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

  // Group by layer
  const byLayer: Record<number, string[]> = {};
  for (const nid of topo) {
    const l = layer[nid] ?? 0;
    (byLayer[l] = byLayer[l] ?? []).push(nid);
  }

  const maxCol = Math.max(...Object.values(byLayer).map(g => g.length), 1);
  const totalH = (maxCol - 1) * ROW_H;

  const posMap: Record<string, { x: number; y: number }> = {};
  for (const [lStr, group] of Object.entries(byLayer)) {
    const l = Number(lStr);
    const colH   = (group.length - 1) * ROW_H;
    const startY = OY + (totalH - colH) / 2;
    group.forEach((nid, idx) => {
      posMap[nid] = {
        x: Math.round((OX + l * COL_W) / SNAP) * SNAP,
        y: Math.round((startY + idx * ROW_H) / SNAP) * SNAP,
      };
    });
  }

  return nodes.map(n => ({ ...n, position: posMap[n.id] ?? n.position }));
}
