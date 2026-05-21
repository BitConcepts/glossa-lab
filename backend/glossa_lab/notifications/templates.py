"""HTML + plaintext templates for the three notification kinds.

Each ``format_*`` function returns ``(subject, body_text, body_html)`` so the
caller can hand the tuple straight to :meth:`Notifier.send`. We keep the
HTML deliberately tiny (table layout, inline styles) so it renders the same
in Gmail's webmail, Apple Mail, and Outlook desktop without an extra dep.
"""

from __future__ import annotations

import html
from collections import Counter
from datetime import datetime, timezone
from typing import Any


def _now_human() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _escape(s: str) -> str:
    return html.escape(s or "", quote=True)


# ── Discovery digest ─────────────────────────────────────────────────────────


def format_discovery_digest(items: list[dict[str, Any]]) -> tuple[str, str, str]:
    """Compose a digest email summarising new discovery items.

    *items* must be the raw ``DiscoveryItem.to_dict()`` shape (or compatible).
    """
    n = len(items)
    by_topic = Counter()
    by_kind = Counter()
    for it in items:
        for t in (it.get("topic") or "").split(","):
            t = t.strip()
            if t:
                by_topic[t] += 1
        kind = (it.get("kind") or "other").strip() or "other"
        by_kind[kind] += 1

    subject = f"[Glossa Lab] {n} new discovery item{'s' if n != 1 else ''}"

    # Plain text
    lines: list[str] = [
        f"Glossa Lab discovery digest — {_now_human()}",
        f"{n} new item{'s' if n != 1 else ''}.",
        "",
        "By topic:",
    ]
    for topic, c in sorted(by_topic.items(), key=lambda kv: -kv[1]):
        lines.append(f"  - {topic}: {c}")
    lines.append("")
    lines.append("By kind:")
    for kind, c in sorted(by_kind.items(), key=lambda kv: -kv[1]):
        lines.append(f"  - {kind}: {c}")
    lines.append("")
    lines.append("Top items (highest confidence first):")
    sorted_items = sorted(items, key=lambda i: -float(i.get("confidence") or 0.0))
    for it in sorted_items[:25]:
        title = (it.get("title") or "(untitled)").strip()
        url = (it.get("url") or "").strip()
        kind = (it.get("kind") or "other").strip() or "other"
        conf = float(it.get("confidence") or 0.0)
        summary = (it.get("summary") or "").strip()
        lines.append(f"  • [{kind} · {int(conf * 100)}%] {title}")
        if url:
            lines.append(f"    {url}")
        if summary:
            lines.append(f"    {summary[:280]}")
        lines.append("")
    body_text = "\n".join(lines)

    # HTML
    rows: list[str] = []
    for it in sorted_items[:25]:
        title = _escape((it.get("title") or "(untitled)").strip())
        url = (it.get("url") or "").strip()
        kind = _escape(it.get("kind") or "other")
        conf = float(it.get("confidence") or 0.0)
        summary = _escape((it.get("summary") or "").strip()[:280])
        topic = _escape(it.get("topic") or "")
        title_a = (
            f'<a href="{_escape(url)}" style="color:#1d4ed8;text-decoration:none">{title}</a>'
            if url else title
        )
        rows.append(
            f'<tr><td style="padding:8px 12px;border-bottom:1px solid #e5e7eb">'
            f'<div style="font-weight:600;font-size:14px">{title_a}</div>'
            f'<div style="margin-top:2px;font-size:11px;color:#6b7280">'
            f'{kind} · {int(conf * 100)}% · {topic}</div>'
            f'<div style="margin-top:4px;font-size:12px;color:#374151">{summary}</div>'
            f'</td></tr>'
        )
    topic_chips = " ".join(
        f'<span style="display:inline-block;padding:2px 8px;border-radius:9px;'
        f'background:#f1f5f9;color:#475569;font-size:11px;border:1px solid #cbd5e1;'
        f'margin-right:4px">{_escape(t)} · {c}</span>'
        for t, c in sorted(by_topic.items(), key=lambda kv: -kv[1])
    )
    body_html = f"""\
<!doctype html>
<html><body style="font-family:system-ui,sans-serif;background:#f8fafc;margin:0;padding:0">
<table role="presentation" width="100%" style="background:#f8fafc;padding:24px 12px">
<tr><td align="center">
  <table role="presentation" width="640" style="background:#fff;border-radius:10px;
         border:1px solid #e5e7eb;border-collapse:collapse">
    <tr><td style="padding:18px 18px 4px">
      <div style="font-size:20px;font-weight:700;color:#111827">🔭 Glossa Lab discovery</div>
      <div style="font-size:12px;color:#6b7280;margin-top:4px">{_escape(_now_human())}</div>
    </td></tr>
    <tr><td style="padding:6px 18px 14px">
      <div style="font-size:14px;color:#374151">
        <strong>{n}</strong> new item{'s' if n != 1 else ''} classified.
      </div>
      <div style="margin-top:10px">{topic_chips}</div>
    </td></tr>
    {"".join(rows)}
    <tr><td style="padding:14px 18px;background:#f8fafc;border-top:1px solid #e5e7eb;
            color:#9ca3af;font-size:11px">
      Manage recipients in Settings → Notifications.
    </td></tr>
  </table>
</td></tr>
</table>
</body></html>
"""
    return subject, body_text, body_html


# ── Study / experiment completion ───────────────────────────────────────────


def _completion_subject(kind: str, name: str, status: str) -> str:
    icon = "✅" if status == "completed" else "❌" if status in ("failed", "error") else "ℹ️"
    return f"[Glossa Lab] {icon} {kind} {status}: {name}"


def _format_completion(
    *, kind: str, name: str, run_id: str, status: str,
    summary: dict[str, Any] | None = None,
    duration_s: float | None = None,
) -> tuple[str, str, str]:
    """Shared HTML+text body for study and experiment completion emails."""
    summary = summary or {}
    subject = _completion_subject(kind, name, status)
    color = "#16a34a" if status == "completed" else "#dc2626" if status in ("failed", "error") else "#2563eb"
    bullets: list[str] = []
    for k, v in summary.items():
        if isinstance(v, (str, int, float, bool)):
            bullets.append(f"  - {k}: {v}")
    text = "\n".join([
        f"{kind} run {status}",
        f"Name: {name}",
        f"Run ID: {run_id}",
        f"Duration: {duration_s:.1f}s" if duration_s is not None else "",
        f"Time: {_now_human()}",
        "",
        "Summary:",
        *bullets,
    ]).rstrip()

    bullet_html = "".join(
        f'<tr><td style="padding:2px 0;color:#6b7280">{_escape(str(k))}</td>'
        f'<td style="padding:2px 0 2px 12px;color:#111827;font-family:monospace">{_escape(str(v))}</td></tr>'
        for k, v in summary.items() if isinstance(v, (str, int, float, bool))
    )
    body_html = f"""\
<!doctype html>
<html><body style="font-family:system-ui,sans-serif;background:#f8fafc;margin:0;padding:0">
<table role="presentation" width="100%" style="background:#f8fafc;padding:24px 12px">
<tr><td align="center">
  <table role="presentation" width="560" style="background:#fff;border-radius:10px;
         border:1px solid #e5e7eb;border-collapse:collapse">
    <tr><td style="padding:18px;border-left:4px solid {color}">
      <div style="font-size:18px;font-weight:700;color:#111827">{_escape(kind)} {_escape(status)}</div>
      <div style="font-size:14px;color:#374151;margin-top:4px">{_escape(name)}</div>
      <div style="font-size:11px;color:#9ca3af;margin-top:2px">
        Run {_escape(run_id)} · {_escape(_now_human())}
        {(' · ' + f'{duration_s:.1f}s') if duration_s is not None else ''}
      </div>
    </td></tr>
    <tr><td style="padding:14px 18px">
      <table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;font-size:12px">
        {bullet_html}
      </table>
    </td></tr>
    <tr><td style="padding:12px 18px;background:#f8fafc;border-top:1px solid #e5e7eb;
            color:#9ca3af;font-size:11px">
      Sent because <em>Notify on completion</em> was enabled for this run.
    </td></tr>
  </table>
</td></tr>
</table>
</body></html>
"""
    return subject, text, body_html


def format_study_complete(
    *, name: str, study_id: str, status: str,
    summary: dict[str, Any] | None = None, duration_s: float | None = None,
) -> tuple[str, str, str]:
    return _format_completion(
        kind="Study", name=name, run_id=study_id, status=status,
        summary=summary, duration_s=duration_s,
    )


def format_experiment_complete(
    *, name: str, exp_id: str, status: str,
    summary: dict[str, Any] | None = None, duration_s: float | None = None,
) -> tuple[str, str, str]:
    return _format_completion(
        kind="Experiment", name=name, run_id=exp_id, status=status,
        summary=summary, duration_s=duration_s,
    )


# ── Test email ───────────────────────────────────────────────────────────────


def format_test() -> tuple[str, str, str]:
    """A simple deliverability check fired by the Settings ‘Send test’ button."""
    subject = "[Glossa Lab] Test email — notification subsystem is alive"
    body_text = (
        "This is a Glossa Lab notification test email.\n\n"
        f"Sent at {_now_human()}.\n\n"
        "If you received this, your SMTP credentials and recipient list "
        "are working. You can now enable notifications on discovery, study, "
        "and experiment runs."
    )
    body_html = f"""\
<!doctype html>
<html><body style="font-family:system-ui,sans-serif;background:#f8fafc;margin:0;padding:24px">
<table role="presentation" width="100%" align="center" style="max-width:520px;background:#fff;
       border:1px solid #e5e7eb;border-radius:10px;border-collapse:collapse">
  <tr><td style="padding:18px;border-left:4px solid #16a34a">
    <div style="font-size:18px;font-weight:700;color:#111827">✓ SMTP works</div>
    <div style="font-size:13px;color:#374151;margin-top:6px">
      Glossa Lab can deliver email to this address.
    </div>
    <div style="font-size:11px;color:#9ca3af;margin-top:4px">{_escape(_now_human())}</div>
  </td></tr>
</table>
</body></html>
"""
    return subject, body_text, body_html


# Keep the helpers re-exported via __init__.py
__all__ = [
    "format_discovery_digest",
    "format_study_complete",
    "format_experiment_complete",
    "format_test",
]
