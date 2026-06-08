"""Model registry: curated capability profiles + manual overrides.

``models.json`` holds curated capability profiles. ``overrides.json`` holds
manual corrections that always win over auto-synced data. The loader merges
them and resolves aliases.
"""

import json
from pathlib import Path

_REGISTRY_DIR = Path(__file__).parent
_MODELS_PATH = _REGISTRY_DIR / "models.json"
_OVERRIDES_PATH = _REGISTRY_DIR / "overrides.json"


def _deep_merge(base: dict, over: dict) -> dict:
    """Recursively merge ``over`` onto a copy of ``base``."""
    out = dict(base)
    for key, val in over.items():
        if key in out and isinstance(out[key], dict) and isinstance(val, dict):
            out[key] = _deep_merge(out[key], val)
        else:
            out[key] = val
    return out


def load_registry() -> dict:
    """Load the merged registry (models.json deep-merged with overrides.json).

    Keys beginning with ``_`` in overrides.json are ignored (schema/docs).
    """
    models = json.loads(_MODELS_PATH.read_text(encoding="utf-8"))
    if _OVERRIDES_PATH.exists():
        overrides = json.loads(_OVERRIDES_PATH.read_text(encoding="utf-8"))
        for model_id, patch in overrides.items():
            if model_id.startswith("_"):
                continue
            if model_id in models:
                models[model_id] = _deep_merge(models[model_id], patch)
            else:
                models[model_id] = patch
    return models


def resolve_model(model_id: str, registry: dict | None = None) -> tuple[str, dict] | None:
    """Resolve a model id (canonical key or alias) to (canonical_id, entry).

    Returns ``None`` if the model is not registered.
    """
    reg = registry if registry is not None else load_registry()
    if model_id in reg:
        return model_id, reg[model_id]
    for canonical, entry in reg.items():
        if canonical.startswith("_"):
            continue
        if model_id in entry.get("aliases", []):
            return canonical, entry
    return None
