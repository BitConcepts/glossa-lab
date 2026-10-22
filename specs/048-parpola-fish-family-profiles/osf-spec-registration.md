# Spec 048 — OSF Contract Registration

> ## FILED — PENDING APPROVAL — 2026-10-21
>
> Filed at the freeze under DD-048-14 (campaign
> decision E-1), following the Specs 036–039
> pattern.
> Registration: **https://osf.io/f5ej9/**
> Draft registration id: `6ad8938bdfd575a9d40da976`
> Filed at: 2026-10-21T10:27:45Z (draft created
> immediately before, same session)
> Node: nrb9u (Predictions & Registrations)
> Schema: OSF Preregistration
> (697b72f611a8e98484c6139b)
> Subjects: the programme's five standing subjects
> (Computational Linguistics; Social and Behavioral
> Sciences; Anthropology; Linguistics;
> Archaeological Anthropology)
>
> State at filing, verified by API read-back:
> `reviews_state` initial,
> `pending_registration_approval` true, not yet
> public; all 29 schema responses present,
> including the freeze digest in the study-design
> answer. Approval proceeds via the token link in
> OSF's admin-notification email — the parent's
> approval click, which this freeze does not
> perform and whose mail it does not handle.
> Execution (Phase-408) does not begin while the
> registration stands pending: it awaits that
> approval act and a separate execution order
> (freeze.md §5). This record is completed by
> append once the approval is API-verified
> (accepted + public + DOI).
>
> The registration carries the frozen contract:
> freeze digest
> `56beec70957ac64e5f17e3bb889e66c9becfe7a7a55b49bc59e5a232c642a846`,
> execution Phase-408, the Asset F pin-timing
> ruling (contract anchor: Spec 044's freeze
> digest
> `6851f943d196fa389e48b67cb5161b90daa1180d8a3e1cf3f020fcf25691d9c8`;
> pin source: Spec 044's step-0 outcome record;
> gate 0.1 asserting the byte-digest at execution
> step 0, with ASSET F NOT AVAILABLE and ASSET F
> DIGEST MISMATCH as its closures), the strict
> corpus reading (Spec 033 §4 V3 /
> Mahadevan-lineage corpus, gate-0.3 pin with
> T2.4 reproduction), the join via
> `mahadevan_number` with the UNMAPPED
> disposition, the frozen criteria (member bar
> 20%, family lines 70% / 30%, floor 30, the
> integral Holdat second arm), the control-set
> rules fixed at the freeze, the nine-class
> outcome set, and the Roif hold stated as what
> it is: the registration files the frozen
> *contract* — a design text — and no result;
> the campaign's R-7 hold on this spec's results
> stands, and this filing clears nothing under
> it.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*

## Filing failure + re-filing — REGISTRATION OF RECORD: eqpab (2026-10-21)

This section supersedes the "FILED — PENDING
APPROVAL" header above as the registration of
record. **eqpab is now the registration to
approve**; f5ej9 is not, and cannot be.

### The f5ej9 failure

The original registration **f5ej9** (draft
`6ad8938bdfd575a9d40da976`, filed
2026-10-21T10:27:45Z) failed at filing on
OSF's side. OSF sent a "Problem Registering"
email (Gmail id `1a15e00c54e3ee96`, held
unarchived until the replacement is approved)
citing "errors copying files to the
registration". An API GET on
`registrations/f5ej9` returns it no longer
available (410/404). It never reached the
approval stage and cannot be approved. The
failure was discovered by the parent's
approval run.

Spec 048's freeze itself is merged and
unaffected: the freeze digest
`56beec70957ac64e5f17e3bb889e66c9becfe7a7a55b49bc59e5a232c642a846`
stands, unchanged.

### The re-filing: eqpab

Re-filed 2026-10-21 by the campaign
coordinator with the identical frozen
contract payload. The original responses file
(`~/workspace/campaign-freeze-work/spec048/osf/responses.json`,
all 29 schema responses) was reused verbatim
— the PATCH read-back showed 29 responses,
zero field diffs; same title, description,
node nrb9u, schema OSF Preregistration
(697b72f611a8e98484c6139b), and the same five
standing subjects.

- **New registration: https://osf.io/eqpab/**
- New draft registration id:
  `6ad8a237217927597e1bf66a`
- Register POST returned 201.
- State at filing, from the POST response:
  `reviews_state` initial,
  `pending_registration_approval` true, not
  public.

Approval is the parent's act and is pending.
Execution (Phase-408) still awaits that
approval. The re-filing staging is kept at
`~/workspace/campaign-freeze-work/spec048/osf-refile/`
(`refile.py`, `draft.json`, `subjects.json`,
`register.json`).

### A note on verification

GET read-backs of registrations via the CLI
route currently return 404 for all
registrations in this environment, including
long-public ones. The filing's verification
of record is therefore the create / patch /
register responses themselves (201 / 200 /
201, with the read-back comparisons above)
— the same class of evidence the original
filing used.

---

*Filing-failure + re-filing record appended
2026-10-21 by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson,
per constitution §VI. Append-only: nothing
above this section was edited.*

---

## Approval completed — eqpab APPROVED + PUBLIC (2026-10-21)

This section completes this record. The
registration of record **eqpab**
(https://osf.io/eqpab/) is **approved and
public**, per the parent's second approval
pass of 2026-10-21.

- **Registration:** https://osf.io/eqpab/
- **DOI:** 10.17605/OSF.IO/EQPAB
- **State on completion:** approved +
  public, with the DOI above, verified by
  the parent's API verification in that
  approval pass. The parent's mail archiving
  for this registration runs as their
  completion leg of the same pass.
- **The failed f5ej9's mail:** the OSF mail
  for the failed registration f5ej9 stays in
  the inbox, per the standing rule — mail for
  a failed registration is not archived.
- **Execution:** approval alone does not
  execute. Execution (Phase-408) still
  requires its Wave 3 execution turn under
  the campaign.

---

*Approval-completion record appended
2026-10-21 by an AI agent (Muse Spark, via
Muse) at the direction of Tristen Pierson,
per constitution §VI. Append-only: nothing
above this section was edited.*
