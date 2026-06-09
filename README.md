# lm-tutor — The School for LLMs

> **Phase 1** — 11 classes, 185 rules, 494 tests. MIT licensed.
> _Structured AI education for any model. No fine-tuning required._

Most code on the web is broken. Models trained on it learn to reproduce that
brokenness — not because they can't do better, but because the broken pattern
is the one they saw most often. (96% of homepages fail WCAG accessibility. A
model trained on that will default to broken unless you tell it otherwise.)

lm-tutor treats this as an **attention problem, not a capability gap.** The
model already knows how to write good code — it just needs a reminder at the
right moment. Structured, token-efficient rule injection shifts what the model
attends to at generation time. That's the whole trick.

**Benchmarked:** DeepSeek V4 Flash generating HTML — 15.8 violations raw, 6.0
after a single `tutor learn` injection. **62% fewer violations.** Python
output (which was already clean): zero effect, as expected. The impact is
proportional to how broken the training data was for that domain.

[Full methodology and data →](docs/benchmark-methodology.md)

---

## Quickstart

```bash
git clone https://github.com/mfolofy/lm-tutor.git
cd lm-tutor
pip install -e .
echo "<div>" | tutor eval
```

One command, zero setup. The syllabus is auto-detected from content.

```bash
# Find your track
tutor enroll --model deepseek-chat
# Take a class
tutor learn --model deepseek-chat --class brushes
# Grade some output
echo "<html><img src='a.png'>" | tutor eval
```

---

## The Classes

| Class | Rules | Standard |
|-------|-------|----------|
| **brushes** — Web accessibility | 34 (10 check) | WCAG 2.2, ARIA, HTML |
| **defense** — Security | 19 (8 check) | OWASP Top 10, ASVS, CWE |
| **audit** — Compliance evidence | 19 (8 check) | SOC2, HIPAA, CMMC, NIST 800-53 |
| **security** — Secure coding | 20 (6 check) | NIST SP 800-53 Rev 5 |
| **architect** — System design | 21 (4 check) | Fowler, SoD, CP/CPS, cloud patterns |
| **code-review** — Review standards | 18 (2 check) | ITIL v4, House |
| **prompt-design** — Prompt engineering | 16 (5 check) | COT, Constitutional AI |
| **perf** — Performance | 18 (4 check) | Web Vitals, Lighthouse |
| **test** — Testing | 18 (4 check) | xUnit Patterns, FIRST, TDD |
| **python-best-practices** — Python | 16 (6 check) | PEP 8, PEP 257, PEP 484 |
| **api-design** — REST/GraphQL/gRPC | 18 (6 check) | Fielding, Google AIP, OpenAPI |

**185 rules total** — 41 with deterministic checkers, 144 teaching-only.

---

## How It Works

**Track assignment** — `tutor enroll` looks up your model and assigns a track
based on capability. Small models get remedial (fundamentals + Booster tools).
Powerful models get honors (full curriculum, skip-eligible).

**Classes** — Each class is a YAML file with `[RULE]` checklists + FAIL/PASS
examples. The format is optimized for working memory (~120 tokens for 10 rules,
vs ~500 tokens for prose). Models attend to `[RULE]` landmarks automatically.

**Grading** — `tutor eval` scores output against the same `class.yaml` it
taught from. No drift between what's taught and what's tested.

**Eval history** — Every grade is saved per model. `tutor profile` shows
per-class pass rates, weakest rules, and next-class suggestions.

---

## The CLI

| Command | What it does |
|---------|--------------|
| `tutor enroll --model <id>` | Get your track |
| `tutor learn --model <id> --class <name>` | Take a class |
| `tutor eval [--class <name>]` | Grade stdin |
| `tutor fix [--class <name>]` | Eval → fix loop |
| `tutor curriculum --model <id>` | Show your track |
| `tutor profile --model <id>` | Your eval history |
| `tutor booster <sub>` | Scratchpad, verify, few-shot |
| `tutor mcp` | MCP server mode |

---

## Why It Works

The full theory is at **[docs/theory.md](docs/theory.md)** — 11 sections
connecting every design decision to neuroscience, cognitive psychology, and
evolutionary biology. Short version:

- **`[RULE]` landmarks work like your RAS** — they make the right patterns
  salient in the attention landscape, the same way a hazard light catches your
  peripheral vision before you consciously see it.
- **Every `tutor learn` cycle is Hebbian** — neurons that fire together wire
  together. Each rule+output cycle strengthens the correct attention pathway.
- **The fix loop is myelination** — repeated practice makes the correct pattern
  faster and more automatic, the same way scales practice makes a pianist faster.
- **Track assignment is Vygotsky's ZPD** — give each model exactly the
  scaffolding it needs, not more and not less.

---

## References

- **Standards catalog:** [REFERENCES.md](REFERENCES.md) — every cited standard,
  paper, and control across all 11 classes.
- **Theory:** [docs/theory.md](docs/theory.md) — neurobiological foundations
  with 30+ citations.
- **Benchmark data:** [docs/benchmark-methodology.md](docs/benchmark-methodology.md)
  — methodology and results across 2 models and 3 conditions.

---

## Contributing

Adding a class is three files: one `class.yaml`, one `SOURCES.md`, one test.
See [CONTRIBUTING.md](CONTRIBUTING.md). No "because I think so" rules —
cite your sources.
