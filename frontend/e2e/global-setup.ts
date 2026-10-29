/**
 * Playwright global setup (Spec 081).
 *
 * The redesigned shell shows program-space navigation only while a
 * program is open, and lands on the open program's home. The CI
 * backend starts with an empty data dir, so seed one active program
 * before the suite runs; specs then exercise the program space.
 * The no-program tool home is verified separately (it needs an empty
 * backend by definition).
 *
 * Backend mode only (PLAYWRIGHT_USE_BACKEND=1, as in CI).
 */
const BACKEND = process.env.PLAYWRIGHT_BACKEND_URL || "http://127.0.0.1:8001";

export default async function globalSetup(): Promise<void> {
  if (!process.env.PLAYWRIGHT_USE_BACKEND) return;

  for (let i = 0; i < 30; i++) {
    try {
      const r = await fetch(`${BACKEND}/api/v1/health`);
      if (r.ok) break;
    } catch {
      /* backend not up yet */
    }
    await new Promise((r) => setTimeout(r, 1000));
  }

  const listResp = await fetch(`${BACKEND}/api/v1/projects`);
  if (!listResp.ok) return;
  const projects = (await listResp.json()) as Array<{ id: string; is_active?: boolean }>;
  if (projects.some((p) => p.is_active)) return;

  let id = projects[0]?.id;
  if (!id) {
    id = "e2e-program";
    await fetch(`${BACKEND}/api/v1/projects/${id}`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        label: "E2E Program",
        description: "Seeded by the Playwright global setup.",
        question: "Does the redesigned shell hold together end to end?",
        prompt_context: "",
        topic_ids: [],
        experiment_ids: [],
        corpus_ids: [],
      }),
    });
  }
  await fetch(`${BACKEND}/api/v1/projects/${id}/activate`, { method: "POST" });
}
