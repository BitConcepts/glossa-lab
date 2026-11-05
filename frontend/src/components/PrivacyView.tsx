/**
 * PrivacyView — the Privacy and Data-Handling Statement screen
 * (Spec 084, T011; inventory gap A4).
 *
 * The statement text is NOT in this file. It is served by the
 * backend (GET /api/v1/privacy) from the single approved copy
 * (backend/glossa_lab/privacy_statement.py), which CI diffs
 * against the Spec 084 fixture — the single source of truth.
 * This view only fetches and renders it. Editing the words here
 * is impossible by construction; the text changes only through a
 * recorded owner-approval act (FR-084-08).
 *
 * Utility route ("privacy", not in the nav), reached from the
 * command palette — the same pattern as AI Tools (Spec 081 Q6).
 */
import { useEffect, useState, type ReactNode } from "react";
import { getPrivacyStatement } from "../api";

// ── Minimal renderer for the statement's markdown ─────────────────
// The approved text uses only: # / ## / ### headings, hard-wrapped
// paragraphs, "- " bullets with indented continuations, one
// blockquote, and **bold** / *italic* / `code` inline marks.

function inline(text: string, keyBase: string): ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g);
  return parts.map((part, i) => {
    const key = `${keyBase}-${i}`;
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={key}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith("*") && part.endsWith("*") && part.length > 2) {
      return <em key={key}>{part.slice(1, -1)}</em>;
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return <code key={key}>{part.slice(1, -1)}</code>;
    }
    return <span key={key}>{part}</span>;
  });
}

type Block =
  | { kind: "h1" | "h2" | "h3" | "p"; text: string }
  | { kind: "ul"; items: string[] }
  | { kind: "quote"; text: string };

function parseBlocks(text: string): Block[] {
  const blocks: Block[] = [];
  let para: string[] = [];
  let items: string[] | null = null;
  let quote: string[] = [];

  const flushPara = () => {
    if (para.length) blocks.push({ kind: "p", text: para.join(" ") });
    para = [];
  };
  const flushItems = () => {
    if (items) blocks.push({ kind: "ul", items });
    items = null;
  };
  const flushQuote = () => {
    if (quote.length) blocks.push({ kind: "quote", text: quote.join(" ") });
    quote = [];
  };
  const flushAll = () => {
    flushPara();
    flushItems();
    flushQuote();
  };

  for (const raw of text.split("\n")) {
    const line = raw.trimEnd();
    if (!line.trim()) {
      flushAll();
    } else if (line.startsWith("### ")) {
      flushAll();
      blocks.push({ kind: "h3", text: line.slice(4) });
    } else if (line.startsWith("## ")) {
      flushAll();
      blocks.push({ kind: "h2", text: line.slice(3) });
    } else if (line.startsWith("# ")) {
      flushAll();
      blocks.push({ kind: "h1", text: line.slice(2) });
    } else if (line.startsWith("- ")) {
      flushPara();
      flushQuote();
      if (!items) items = [];
      items.push(line.slice(2));
    } else if (line.startsWith("> ")) {
      flushPara();
      flushItems();
      quote.push(line.slice(2));
    } else if (line.startsWith("  ") && items && items.length) {
      items[items.length - 1] += " " + line.trim();
    } else if (quote.length) {
      quote.push(line.trim());
    } else if (items) {
      flushItems();
      para.push(line.trim());
    } else {
      para.push(line.trim());
    }
  }
  flushAll();
  return blocks;
}

export function PrivacyView() {
  const [text, setText] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let live = true;
    getPrivacyStatement()
      .then((r) => {
        if (live) setText(r.text);
      })
      .catch((e) => {
        if (live) setError(e instanceof Error ? e.message : String(e));
      });
    return () => {
      live = false;
    };
  }, []);

  if (error) {
    return (
      <div style={{ maxWidth: 860, margin: "0 auto", width: "100%" }}>
        <h2>Privacy and data handling</h2>
        <p>The statement could not be loaded: {error}</p>
      </div>
    );
  }
  if (text === null) {
    return (
      <div style={{ maxWidth: 860, margin: "0 auto", width: "100%" }}>
        <p>Loading the privacy statement…</p>
      </div>
    );
  }

  const blocks = parseBlocks(text);
  return (
    <div style={{ maxWidth: 860, margin: "0 auto", width: "100%", lineHeight: 1.55 }}>
      {blocks.map((b, i) => {
        const key = `b-${i}`;
        switch (b.kind) {
          case "h1":
            return <h1 key={key} style={{ fontSize: 26 }}>{inline(b.text, key)}</h1>;
          case "h2":
            return <h2 key={key} style={{ fontSize: 20, marginTop: 28 }}>{inline(b.text, key)}</h2>;
          case "h3":
            return <h3 key={key} style={{ fontSize: 16, marginTop: 22 }}>{inline(b.text, key)}</h3>;
          case "ul":
            return (
              <ul key={key} style={{ paddingLeft: 22 }}>
                {b.items.map((item, j) => (
                  <li key={`${key}-${j}`} style={{ marginBottom: 6 }}>{inline(item, `${key}-${j}`)}</li>
                ))}
              </ul>
            );
          case "quote":
            return (
              <blockquote
                key={key}
                style={{ borderLeft: "3px solid #888", margin: "12px 0", paddingLeft: 14, fontStyle: "italic" }}
              >
                {inline(b.text, key)}
              </blockquote>
            );
          default:
            return <p key={key}>{inline(b.text, key)}</p>;
        }
      })}
    </div>
  );
}
