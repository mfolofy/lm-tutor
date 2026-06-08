# CRITIQUE: MCP Bridge SCOPE.md

**Reviewer:** Critiquer (adversarial design review)
**Date:** 2026-06-08
**Target:** `P:\AI_Code\projects\mcp-bridge\SCOPE.md`

---

## 1. Architecture — Single Server, Single Point of Everything

> "Single server, decoupled modules — one MCP registration per agent"
> "No cross-module dependencies"

The SCOPE.md presents single-server-as-virtue: one registration, zero configuration, modules are just directories. This is a deployment convenience argument dressed up as an architectural decision.

**What happens when `modules/brushes/` has a memory leak?** Not a hypothetical — `brushes` is the heaviest module (703-line anti-pattern file + 251-line library). It holds structured knowledge in memory. If it leaks, the entire bridge goes down. Every module. Every protocol. Every agent that depends on it.

**What happens when `modules/perf/` pulls in `numpy` for big-O analysis and `numpy` conflicts with `modules/defense/`'s HTTP client version?** "No cross-module dependencies" is a statement about design intent, not about Python import chains or shared virtual environments. In a single process, every `import` is a cross-module dependency whether you planned one or not.

**Crash isolation is zero.** Module A throws an unhandled exception → the entire MCP server process dies → every agent loses every module. With 6 independent servers, one module crashing costs you one module. With the bridge, one module crashing costs you everything. The doc does not acknowledge this tradeoff, let alone mitigate it (process isolation, watchdog, graceful degradation per module).

**The single-server pattern also means a single deployment pipeline.** Want to update `modules/security/` without restarting `modules/architect/`? Can't. Rolling restart of one module requires rolling restart of the whole bridge. Zero-downtime updates are now a global problem instead of a per-module one.

---

## 2. The Central Claim — Extraordinary, Unsupported

> "Make any model — even a free tier — produce output indistinguishable from frontier quality (Opus 4.8, GPT-5)"

This sentence is the entire thesis of the project. It is also the least supported claim in the document.

**"Indistinguishable" by what measure?** By House review pass rate (success criterion 1)? That's circular — the bridge teaches what House checks, so of course outputs pass House more often. That's not "frontier quality," that's "taught to the test." A model that passes House review by mechanically applying bridge knowledge will still produce flat, unoriginal, mechanically correct outputs. Frontier models produce *surprising* correct outputs — novel solutions the reviewer didn't anticipate. The bridge cannot teach surprise.

**The ceiling problem:** Knowledge injection works up to the model's *reasoning capacity*. You can give a 8B model perfect WCAG specs and it will still fail on a novel accessibility interaction because it lacks the working memory to hold the spec *and* the context *and* generate simultaneously. The bridge can inject knowledge but it cannot inject judgment. There is a hard ceiling at "the model's executive function during generation." The doc does not identify where that ceiling is, how to measure it, or what happens when you hit it.

**The comparative baseline is missing.** "Passes House review at same rate as Opus 4.8" — what is the base rate? What does DeepSeek V4 Flash pass *without* the bridge? If the base pass rate is 15% and the bridge raises it to 25%, that's a 67% improvement but still nowhere near "indistinguishable." Without publishing the baseline, this success criterion is vapor.

---

## 3. Phase Ordering — Security at Phase 3 Is Reckless

> "Phase 3 — security — Hardest to fix after the fact"

You *know* security is the hardest to fix after the fact. You say it explicitly. And you're putting it in Phase 3. After the module loader. After brush-stroke ingestion. After the boot prompt is shipped. Security will be bolted onto whatever architecture Phase 0-2 produced, and the architecture decisions made in those phases will constrain what security can actually do.

**The bridge's own threat model is not mentioned anywhere.** Consider:

- **Prompt injection via module content:** If a module's knowledge YAML contains crafted content, it can inject instructions into the model's context window. The bridge is, by design, a content-delivery system to an LLM. It is also the perfect vector for prompt injection at scale.
- **Tool injection via malformed MCP calls:** An agent sends `bridge_security_owasp-checklist` with a payload that crashes the parser. What happens? Does the error message leak internal paths? Does the exception propagate to the model?
- **Data exfiltration via module responses:** If the bridge has access to any credentials (it shouldn't, but let's check), can a sufficiently clever prompt trick a module into echoing them?
- **Supply chain:** The bridge imports from at least 6 module directories, each potentially with their own `requirements.txt`. Every import is a supply chain risk. Who audits module dependencies?

The doc says "not a security product" in non-goals, but it *delivers security knowledge*. A bridge that teaches OWASP Top 10 but is itself vulnerable to prompt injection is not just ironic — it's dangerous. Models using it will produce *confidently secure* code that isn't.

---

## 4. Boot Prompt Naivety — This Is Not a Prompt Problem

> "You have tools. Use them. Your training data is not enough."

This boot prompt works on Claude Opus 4.8 because Opus has:

1. **Sufficient reasoning headroom** to call tools *while* maintaining generation coherence.
2. **Native tool-calling reliability** — Opus rarely hallucinates tool arguments or invents tool names.
3. **Multi-step planning** — it can call `bridge_brushes_list`, browse results, call `bridge_brushes_get`, process the response, and generate code in a single coherent pass.

An 8B model does not have these capabilities. The boot prompt is telling the model to do something it may literally be incapable of:

- **Tool-calling reliability degrades sharply with model size.** DeepSeek V4 Flash hallucinates tool names at a higher rate than Opus. Gemma 4 8B's function-calling is experimental. Telling a model to "use your tools" doesn't make its tool-calling more reliable — it just adds pressure to *attempt* tool calls, increasing the chance of hallucinated invocations.
- **Dual-processing tax:** A small model cannot simultaneously maintain "I am generating a React component" and "I should check the accessibility module" in its limited working memory. The cognitive load of tool orchestration steals context from generation quality. The result may be *worse* than letting the model just generate — it now divides its limited capacity between two tasks.
- **Refusal rates:** Free models are heavily guardrailed. Many refuse tool calls that involve "validation," "auditing," or "security scanning" because those keywords trigger refusal classifiers. The bridge will teach a model to attempt a tool call that the model's own safety layer then blocks.

The doc acknowledges model-specific variants (line 151) but treats this as a prompt templating problem. It is not. It is a model capability ceiling. No amount of prompt engineering will give an 8B model the executive function of a 400B model.

---

## 5. Scope Creep — The Bridge Will Eat Everything

The document quietly undergoes three expansions:

1. **Phase 0-1:** Knowledge modules. A content server. Clean scope.
2. **Phase 2:** Boot prompt injection. Now it's a behavior modification system.
3. **Phase 8:** Protocol engine. Execution Protocol (UEP). House review gate. Research swarm. Twin validation. Now it's an *orchestrator*.

Phase 8 turns the bridge into something that competes with every other Ghost Stack component:

- **It becomes a second Forge** when it runs the Execution Protocol (spawn sub-agents, manage multi-step flows).
- **It becomes a second Fleet Manager** when it orchestrates research swarms and validation sidecars.
- **It becomes a session state store** when the handoff protocol writes continuation documents.

What's the boundary? The doc says "I lean describing for Phase 0-7, running for Phase 8" — but Phase 8 is in scope. The bridge *will* become an orchestrator. The document does not define what prevents it from consuming the entire Ghost Stack.

Compare to the non-goals: "Not a replacement for House." But Phase 8 integrates House review gating. If the bridge calls House review and House calls the bridge, you have a circular dependency that will be resolved by merging them into a single monolith.

The doc needs a **terminus** — a concrete statement of what the bridge will *never* do. "We won't run inference" is a terminus. "We won't manage model state" is not, because Phase 8 manages execution state, which is model-adjacent state.

---

## 6. Competitive Reality — The Maintenance Tax Is Unstated

> "Ghost Stack's curated corpus + operational discipline beats 'more rules'"

Six modules, each representing a domain of knowledge that changes over time:

| Module | Knowledge Domain | Update Frequency |
|--------|-----------------|-----------------|
| `brushes` | WCAG / UI/UX | Every WCAG release (yearly) + framework shifts |
| `architect` | Architecture patterns | Ongoing — microservices, serverless, edge evolve |
| `defense` | Error handling | Stable-ish, but new failure modes appear |
| `perf` | Performance patterns | Every new browser engine, every new framework |
| `test` | Testing methodology | Annual-ish |
| `security` | OWASP Top 10 | Every OWASP refresh + zero-days |

**WCAG 3.0 is in draft and will fundamentally restructure accessibility guidelines.** The bridge's `brushes` module will need a rewrite. Who does it? On what timeline?

**OWASP Top 10 changes every 2-4 years, and zero-days are weekly.** If the security module teaches a pattern for SQL injection prevention and a new bypass technique is published, every model using the bridge will continue generating the *old* correct pattern — which is now wrong — until someone updates the module.

**Stale knowledge is worse than no knowledge.** A model that knows it should call the bridge for security guidance but receives outdated guidance will produce *confidently vulnerable* code. The model's own uncertainty is stripped away by the authoritative-sounding module content.

The doc mentions none of this. No maintenance budget. No update cadence. No staleness detection. No mechanism for flagging or retiring outdated modules.

---

## 7. Paint Stroke Extraction — The Integration Cost Is Swept Under the Rug

> "Option B: make bridge the canonical home and brush-stroke a historical artifact"

brush-stroke (at `projects/brush-stroke/`) has:

- Its own Python package structure (`brush_stroke/`)
- Its own schemas (`brush_stroke/schemas.py` — 81 lines of Pydantic models)
- Its own test suite (`tests/` — 5 test files)
- Its own MCP server (`brush_stroke/mcp_server.py` — 79 lines)
- Its own anti-pattern database (703 lines in `anti_patterns.py`)
- Its own adapter system for multiple frameworks (React, Vue, vanilla)
- Its own markdown brush format

The doc presents migration as "extract into `modules/brushes/`" (line 139-142). This is not extraction — it is **repackaging** at minimum and **rewriting** at worst.

**Scenario A: bridge adapts to brush-stroke's conventions.** The bridge's module loader must understand brush-stroke's brush format, its adapter schema, its markdown conventions. Now the bridge has module-specific knowledge — the "no cross-module dependencies" claim is false. The bridge has a hard dependency on brush-stroke's data model.

**Scenario B: brush-stroke adapts to bridge conventions.** brush-stroke must abandon its established schemas, its existing adapter system, its standalone-ability. The 81-line `schemas.py` must be replaced with the bridge's module format. The 5 test files must be rewritten. The markdown brushes must be reformatted. brush-stroke can no longer be used standalone (or if it can, maintaining two formats doubles the maintenance burden).

**The doc's assessment** — "maintaining two repos for one codebase is busywork" — is true only if the migration is clean. The doc does not assess how clean the migration actually is. If it's 80% compatible, Option B is reasonable. If it's 20% compatible, Option B is a destructive rewrite. The doc doesn't know because it hasn't done the compatibility analysis.

---

## 8. Missing Entirely — Telemetry and the Measurement Loop

> Success criterion: "passes House review at the same rate as Opus 4.8"

How do you know which modules the model actually called? How do you know which it skipped? How do you know if the model called a module but ignored its output? How do you know if the boot prompt is working, partially working, or being ignored entirely?

**There is zero instrumentation in the scope document.** Not a mention of logging. Not a mention of usage metrics. Not a mention of A/B testing.

**The black box problem:** A model that ignores the bridge entirely produces the same observable output (final code) as a model that faithfully calls every module. You cannot distinguish "bridge working as designed" from "bridge completely unused" without per-request module invocation telemetry.

**What a telemetry-first design would include:**
- Per-request module call log: which modules were invoked, in what order, with what arguments
- Module response acceptance rate: did the generated code reflect the module's guidance?
- Boot prompt adherence: did the model call *any* module? Did it call modules before generating or after?
- Module latency: which modules are slow? Which are fast? Where is the performance bottleneck?
- Module error rate: which modules fail? Do they fail silently (the model gets empty responses)?

Without this, the bridge is a hope-based system. You hope it works. You cannot prove it does.

---

## 9. The Naming Question Is a Distraction — But It Reveals Something

> "Naming — 'MCP Bridge' is descriptive but boring. Candidates: merge, conduit, equalizer, delta."

This section takes up real estate in a document that does not discuss telemetry, threat model, or maintenance. That's where your head is — on the name — instead of on the hard problems.

But the naming question reveals a deeper issue: **identity uncertainty.** What *is* this thing?

- A knowledge server? (Phases 0-1)
- A behavior modifier? (Phase 2)
- A quality gate? (Phase 3-7)
- An orchestrator? (Phase 8)

The naming anxiety comes from not knowing what the project will become. "MCP Bridge" is vague because the scope is vague. A sharp project has a name that snaps into focus. "Paint Stroke" tells you exactly what it does — it paints strokes of knowledge onto generation. This project doesn't have that clarity yet, and the name hopscotch is a symptom.

---

## 10. The Real Threat — This Solves a 2026 Problem

> "What's our moat? Ghost Stack's curated corpus + operational discipline"

The moat is a moat made of sand.

**Claude Code is already an MCP host.** Every Claude Code session connects to MCP servers natively. The model already knows how to call tools. The gap the bridge fills — "models don't know to ask for help" — is already closing.

**Models are getting framework-specific knowledge built into training.** GPT-5's training data includes curated coding standards. Opus 4.8 already knows WCAG. The training-data-poisoning problem the doc identifies (95.9% broken pages) is real, but the answer is *better training data*, not *runtime knowledge injection*. And frontier labs are investing billions in better training data.

**In 12-18 months, the bridge's content will be either:**
1. **Built into the model** — making the bridge redundant (the model already knows what the bridge teaches)
2. **Stale** — if the model has been updated and the bridge hasn't, the bridge is now teaching deprecated patterns
3. **A crutch** — models that rely on the bridge never develop the judgment to generate correctly without it, meaning agent outputs *degrade* when the bridge is unavailable

The doc's competitive positioning section (open question 5) acknowledges this indirectly but hand-waves it: "Ghost Stack's curated corpus + operational discipline beats 'more rules.'" It beats rules today. It won't beat native model knowledge in 2027.

---

## THE BIGGEST PROBLEM

**The bridge has no feedback loop.**

The entire thesis is: "Inject curated knowledge at generation time to raise output quality." But there is no mechanism to measure whether the injection works, which modules drive quality improvements, which modules are ignored, or whether the bridge is making things worse. The success criterion ("passes House review at same rate as Opus") is an outcome metric measured *after* generation — it cannot distinguish between "the bridge taught the model well" and "the model already knew this and the bridge was irrelevant."

Without telemetry, the bridge is a religion, not an engineering system. You will believe it works because you want it to work. When modules go stale, you won't notice until outputs degrade — and by then, you won't know which module caused the degradation because you have no per-module usage data.

**Ship telemetry before the boot prompt. Ship measurement before security. Ship observability before everything else.** Otherwise the bridge will be an unobservable, unprovable, unmaintainable black box that everyone assumes is working and no one can verify.
