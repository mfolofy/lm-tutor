"""Where classes live: the built-in folder plus optional external folders.

Classes ship in ``tutor/classes``. To keep a private class pack outside the
repo, point ``TUTOR_CLASS_PATH`` at one or more folders (separated by
``os.pathsep``: ``;`` on Windows, ``:`` elsewhere). Each folder holds
``<class-id>/class.yaml`` directories, exactly like the built-in folder.

The built-in folder always comes first, so an external class can never shadow a
shipped class of the same name. Blank entries and folders that do not exist are
ignored. With the variable unset, behaviour is exactly the built-in folder.
"""

import os
from pathlib import Path

CLASS_PATH_ENV = "TUTOR_CLASS_PATH"
BUILTIN_CLASSES_DIR = Path(__file__).parent / "classes"


def class_dirs() -> list[Path]:
    """Built-in class folder first, then each existing ``TUTOR_CLASS_PATH`` folder."""
    dirs = [BUILTIN_CLASSES_DIR]
    for raw in os.environ.get(CLASS_PATH_ENV, "").split(os.pathsep):
        raw = raw.strip()
        if not raw:
            continue
        p = Path(raw).expanduser()
        if p.is_dir() and p not in dirs:
            dirs.append(p)
    return dirs


def find_class_dir(name: str) -> Path | None:
    """Folder of the class ``name`` (first folder holding ``<name>/class.yaml``), or None."""
    for base in class_dirs():
        if (base / name / "class.yaml").is_file():
            return base / name
    return None


def iter_class_dirs() -> list[Path]:
    """Every class folder (each holding a ``class.yaml``), sorted by id.

    A name found in more than one folder is listed once, from the first folder.
    """
    seen: dict[str, Path] = {}
    for base in class_dirs():
        for path in sorted(base.glob("*/class.yaml")):
            seen.setdefault(path.parent.name, path.parent)
    return [seen[k] for k in sorted(seen)]
