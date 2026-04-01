"""CPSC (Constraint-Projected State Computing) integration module.

This module is OPTIONAL and cleanly removable. All CPSC-specific code
lives within this package. The rest of Glossa Lab detects CPSC
availability via the `CPSC_AVAILABLE` flag and falls back to standard
hill climbing if this module is absent.

IP Notice:
  The CPSC paradigm is described in US Provisional [REDACTED-PATENT-NO]
  (filed Feb 11, 2026) and is subject to the CPSC Research &
  Evaluation License. This module may be removed without affecting
  core Glossa Lab functionality.

To disable CPSC: delete the `glossa_lab/cpsc/` directory.
The decipher pipeline will automatically fall back to hill climbing.
"""

CPSC_AVAILABLE = True
CPSC_VERSION = "0.1.0"
