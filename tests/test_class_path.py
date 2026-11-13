"""Tests for tutor/_class_paths.py -- external class folders via TUTOR_CLASS_PATH."""
import os

import pytest

from tutor import _class_paths
from tutor._class_paths import class_dirs, find_class_dir, iter_class_dirs
from tutor.cli.eval import infer_syllabus, list_classes
from tutor.eval.harness import grade, load_syllabus

MINIMAL = """class:
  id: {cid}
  title: "{title}"
  version: 1.0.0
  sources: ["Example"]
rules:
  - id: no-todo
    severity: fundamental
    rule: "No TODO markers."
    check_regex: |-
      TODO
"""


def _make_class(base, cid, title="External"):
    d = base / cid
    d.mkdir(parents=True)
    (d / "class.yaml").write_text(MINIMAL.format(cid=cid, title=title), encoding="utf-8")
    return d


@pytest.fixture
def ext(tmp_path, monkeypatch):
    folder = tmp_path / "pack"
    folder.mkdir()
    monkeypatch.setenv("TUTOR_CLASS_PATH", str(folder))
    return folder


def test_unset_is_builtin_only(monkeypatch):
    monkeypatch.delenv("TUTOR_CLASS_PATH", raising=False)
    assert class_dirs() == [_class_paths.BUILTIN_CLASSES_DIR]
    assert find_class_dir("brushes") == _class_paths.BUILTIN_CLASSES_DIR / "brushes"
    assert find_class_dir("no-such-class") is None
    builtin = sorted(p.parent.name for p in _class_paths.BUILTIN_CLASSES_DIR.glob("*/class.yaml"))
    assert [p.name for p in iter_class_dirs()] == builtin


def test_external_class_found_listed_and_graded(ext):
    _make_class(ext, "ext-demo", title="External Demo")
    assert find_class_dir("ext-demo") == ext / "ext-demo"
    assert "ext-demo" in [p.name for p in iter_class_dirs()]
    assert any(c["id"] == "ext-demo" and c["title"] == "External Demo" for c in list_classes())
    assert load_syllabus("ext-demo")["class"]["id"] == "ext-demo"
    result = grade("x = 1  # TODO", "ext-demo")
    assert not result.passed


def test_missing_and_blank_entries_ignored(tmp_path, monkeypatch):
    missing = tmp_path / "nope"
    monkeypatch.setenv("TUTOR_CLASS_PATH", os.pathsep.join(["", str(missing), "  "]))
    assert class_dirs() == [_class_paths.BUILTIN_CLASSES_DIR]


def test_several_folders_in_order(tmp_path, monkeypatch):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    _make_class(a, "dup", title="From A")
    _make_class(b, "dup", title="From B")
    monkeypatch.setenv("TUTOR_CLASS_PATH", os.pathsep.join([str(a), str(b)]))
    assert class_dirs() == [_class_paths.BUILTIN_CLASSES_DIR, a, b]
    assert find_class_dir("dup") == a / "dup"
    assert [p for p in iter_class_dirs() if p.name == "dup"] == [a / "dup"]


def test_builtin_wins_name_clash(ext):
    _make_class(ext, "brushes", title="Impostor")
    assert find_class_dir("brushes") == _class_paths.BUILTIN_CLASSES_DIR / "brushes"
    assert load_syllabus("brushes")["class"]["title"] != "Impostor"
    assert [c["title"] for c in list_classes() if c["id"] == "brushes"] != ["Impostor"]
    assert sum(1 for c in list_classes() if c["id"] == "brushes") == 1


def test_unknown_class_error_names_searched_folders(ext):
    result = grade("x", "no-such-class")
    assert result.error and str(ext) in result.error


def test_scaffold_into_external_dir(ext, capsys):
    from tutor.cli.new_class import scaffold

    assert scaffold("ext-new", dest_dir=ext) == 0
    assert (ext / "ext-new" / "class.yaml").is_file()
    assert (ext / "ext-new" / "SOURCES.md").is_file()
    assert find_class_dir("ext-new") == ext / "ext-new"
    # a name already on the class path is refused, even for another folder
    assert scaffold("brushes", dest_dir=ext) == 2