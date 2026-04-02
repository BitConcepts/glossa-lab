# Verification

## Conflict And Consistency Handling

If an agent detects:

* a requirement without a test
* a test without a requirement
* architecture that violates requirements
* ledger inconsistencies
* documentation that contradicts implementation

The agent SHALL:

1. Report the issue explicitly
2. Reference exact document locations (file, line, requirement ID)
3. NOT propose fixes unless explicitly requested
4. Record the inconsistency in the current session's ledger entry under "Risks"

---

## Verification Minimum

Must record:

* what changed
* what was tested
* what passed/failed
* what is unknown

---

