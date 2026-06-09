"""Audit all classes for teaching-only rules that could have checkers."""
import yaml
from pathlib import Path

classes_dir = Path("tutor/classes")
for class_dir in sorted(classes_dir.iterdir()):
    if not class_dir.is_dir():
        continue
    yaml_path = class_dir / "class.yaml"
    if not yaml_path.exists():
        continue
    cls = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    rules = cls.get("rules", []) or []
    total = len(rules)
    with_check = sum(1 for r in rules if r.get("check_selector") or r.get("check_regex"))
    teaching = total - with_check
    print(f"{class_dir.name:30s} {total:3d} rules ({with_check:2d} checkable, {teaching:2d} teaching)")
    if teaching > 0:
        for r in rules:
            if not r.get("check_selector") and not r.get("check_regex"):
                rid = r.get("id", "?")
                sev = r.get("severity", "?")
                print(f"    - {rid:35s} severity={sev}")
