# lm-tutor Validation

This directory contains validation protocols for independently verifying the
lm-tutor thesis — that structured rule injection measurably reduces violations
in LLM output.

## Protocols

| File | Description |
|------|-------------|
| `FABLE5_SELF_ADMITTED.md` | Fable 5 self-evaluates against class rules. First external-model validation. Run by Miguel in Claude Code. |

## Purpose

All prior benchmarks were run on DeepSeek models that could have had lm-tutor
content in training data. These validation protocols use models that were NOT
involved in class creation, eliminating training-set contamination risk.
