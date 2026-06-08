"""lm-tutor — The School for LLMs.

Structured AI education for any model: enrollment -> curriculum track ->
classes -> graduation. Phase 0 ships the skeleton plus a Layer 1 (rules
engine) eval harness.

The package is import-light by design: the top level pulls in nothing beyond
the standard library so that ``python -m tutor --help`` and ``tutor eval`` are
fast and have no side effects. Subcommands import their own dependencies
lazily.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
