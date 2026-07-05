"""tutor.cert — constrained-decoding certificates for the Layer-1 rules engine.

See tutor/cert/SCOPE.md (repo root docs/ entry) for the exact guarantee and
its limits. In one line: a certificate proves that a compiled Outlines
constraint regex is provably equivalent to the COMPLEMENT of a specific
class.yaml ``check_regex`` (structural invariance of the grader's own check),
NOT semantic safety, and applies only to a logits-controlled local decoding
path — API-model submissions remain detect-only forever.
"""
