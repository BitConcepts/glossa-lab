"""Leg C hardening (C-02): GlossaShell sandbox confinement tests.

Before the fix, ``GlossaShell._resolve`` returned absolute paths and
``../`` traversals unchecked, so builtins (cat/rm/cp/mv/…) could reach
anything the backend process could reach; only ``cd`` enforced the
sandbox. These tests pin the confinement: reads/writes outside the
sandbox root are refused, in-sandbox access still works.
"""
from __future__ import annotations

from glossa_lab.glossa_shell import GlossaShell


def _shell(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "inside.txt").write_text("inside-marker\n", encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text("outside-marker\n", encoding="utf-8")
    return GlossaShell(cwd=root, sandbox_root=root), root, outside


def test_cat_absolute_path_outside_sandbox_is_refused(tmp_path):
    shell, _root, outside = _shell(tmp_path)
    out = list(shell.run(f"cat {outside}"))
    assert not any("outside-marker" in line for line in out)
    assert any("escapes sandbox" in line for line in out)


def test_cat_traversal_outside_sandbox_is_refused(tmp_path):
    shell, _root, _outside = _shell(tmp_path)
    out = list(shell.run("cat ../outside.txt"))
    assert not any("outside-marker" in line for line in out)
    assert any("escapes sandbox" in line for line in out)


def test_cat_inside_sandbox_still_works(tmp_path):
    shell, _root, _outside = _shell(tmp_path)
    out = list(shell.run("cat inside.txt"))
    assert any("inside-marker" in line for line in out)


def test_rm_traversal_outside_sandbox_does_not_delete(tmp_path):
    shell, _root, outside = _shell(tmp_path)
    list(shell.run("rm ../outside.txt"))
    assert outside.exists()
