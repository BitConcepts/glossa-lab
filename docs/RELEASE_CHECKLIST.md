# Release Checklist — Deposits (Zenodo and equivalents)

Mandatory for every external deposit/release that carries repo
files. Written after the v4.2.0 anchors divergence (see
`reports/release_integrity_audit_v420.md`): that deposit shipped a
stale, CRLF, out-of-tree copy of `INDUS_FINAL_ANCHORS.json` whose
content had not been the repo state for four months. Every step
below exists to make that failure impossible to repeat silently.

## 1. Freeze the source

- [ ] Name the exact source commit (full SHA) the deposit is built
      from. Record it in the release record.
- [ ] Stage from a **clean checkout** of that commit (`git status`
      empty). Never stage from a long-lived working tree.
- [ ] Line endings: the repo mandates LF (`.gitattributes`:
      `*.json text eol=lf`, likewise `.md`/`.py`). A staged file
      with CRLF endings is a stop condition, not a cosmetic issue —
      it changes the hash and proves the copy did not come from a
      clean git checkout.

## 2. Write the manifest

- [ ] One manifest per release (JSON; YAML accepted), listing
      **every** file to be deposited. Each entry names either its
      repo `source` path or an explicit `external_source` note
      explaining why no repo source exists:

      ```json
      {"files": [
        {"deposit_name": "INDUS_FINAL_ANCHORS.json",
         "source": "backend/reports/INDUS_FINAL_ANCHORS.json"},
        {"deposit_name": "RELEASE_VALIDATION.json",
         "source": "outputs/RELEASE_VALIDATION.json"},
        {"deposit_name": "pierson_2026_indus_preprint_v3.pdf",
         "external_source": "Built PDF; source .tex in glossa-corpus/indus/"}
      ]}
      ```

- [ ] No file is deposited that is not in the manifest.

## 3. Run the hash gate — MANDATORY, blocking

- [ ] Run, from the repo root, against the staging directory:

      ```bash
      python backend/scripts/release_gate.py \
          --manifest <release_manifest.json> \
          --staging-dir <staging_dir> \
          --repo-root . \
          --json-out <staging_dir>/release_gate_output.json
      ```

- [ ] **Exit code must be 0.** Any `MISMATCH`, `MISSING-STAGED`, or
      `MISSING-SOURCE` stops the release. Do not "fix" a mismatch by
      editing the staged copy or the manifest after the fact —
      re-stage from the named commit and re-run.
- [ ] `EXTERNAL` entries are expected only where the manifest says
      so; their staged hashes are printed for the release record.

## 4. Record the gate output (RELEASE_VALIDATION practice)

Following the existing `RELEASE_VALIDATION.json` practice — a
release is only as real as its recorded validation — the gate
output is part of the release record, not console ephemera:

- [ ] Paste the gate's full per-file table (file, status, staged
      sha256, source sha256) into the release's validation record:
      for a Zenodo deposit, into the `RELEASE_VALIDATION.json`
      update or the accompanying release notes for that version;
      in all cases also into the repo ledger entry for the release.
- [ ] Record, alongside it: the source commit SHA (§1), the deposit
      DOI / record ID once created, and the gate's verdict line.
- [ ] After depositing, re-pull the deposited record's file list
      and checksums from the provider API and confirm each
      deposited file's hash equals the gate's staged hash for that
      file. Record that confirmation too. (Zenodo stores MD5;
      compare MD5 there and sha256 from the gate — both must agree
      with the staged files.)

## 5. Close out

- [ ] Ledger entry (append-only, with AI disclosure) covering:
      source commit, manifest, gate verdict + table, DOI/record ID,
      post-deposit checksum confirmation.
- [ ] No anchor file, deposit, or external record is modified
      outside this checklist. Corrections to a published deposit
      are a new version, never a silent edit.
