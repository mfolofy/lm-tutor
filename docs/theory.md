# Why It Works — The Biology of Machine Learning

> lm-tutor is built on the conviction that **learning is learning**, whether the
> substrate is biological or silicon. Every design decision maps to a principle
> from neuroscience, cognitive psychology, or evolutionary biology — not because
> that's poetic, but because those sciences have been studying how systems learn
> for centuries. We're just catching up.

## 1. Attention as Salience — The Reticular Activating System

A model's attention mechanism [Vaswani et al. 2017] and the brain's reticular
activating system [Moruzzi & Magoun 1949] solve the same problem: **signal from
noise**. The RAS filters sensory input so the brain only processes what's
salient — you don't consciously hear the refrigerator hum until it stops. A
transformer's attention heads do the same: they compute which tokens matter.

The `[RULE]` landmark format works *because* the attention mechanism already
exists. We're not teaching the model to pay attention — we're telling it *what
to attend to*. A `[RULE]` prefix is a salience signal in the attention
landscape, exactly as a flashing hazard light captures the RAS's attention
before conscious processing begins. Token-efficient injection (~120 tokens per
10 rules vs ~500 tokens for prose [Min et al. 2022]) isn't a performance hack
— it's cognitive load management [Sweller 1988].

## 2. Hebbian Learning — "Neurons that fire together, wire together"

Donald Hebb's 1949 postulate [Hebb 1949]: if two neurons fire simultaneously,
the connection between them strengthens. Every `tutor learn` session is a
Hebbian intervention. The rule token and the correct output token fire in
sequence, repeatedly, until the attention pathway between them is the path of
least resistance.

Initially, the model's broken pattern has higher probability (it was trained on
more broken examples). Each `[RULE] → correct generation` cycle strengthens that
specific neural pathway in the attention distribution [McClelland & Rumelhart
1986]. After enough cycles, the correct pattern fires first — not because the
old one was deleted, but because the new one has more synaptic weight. This is
Hebb's rule operating at the attention level: cells that fire together wire
together, and tokens that attend together link together.

## 3. Error-Driven Learning — The Brain's Loss Function

The Rescorla-Wagner model of classical conditioning [Rescorla & Wagner 1972]
states that learning only happens when reality violates expectation. If the
brain predicts an outcome and gets it right, no learning occurs. If it gets it
wrong, the prediction weights adjust. This is the foundation of reinforcement
learning [Sutton & Barto 2018] and, by extension, the loss functions that train
every modern LLM.

The `tutor eval` harness is the prediction error signal. The model generates
output expecting it to be correct. The harness scores it: **violations found**.
That mismatch is a prediction error — the model's output distribution didn't
match the rule distribution. `tutor fix` closes the loop: the model sees exactly
where the violation was, compares it to the PASS example, and adjusts the next
generation. This is the dopaminergic reward prediction error signal [Schultz,
Dayan & Montague 1997], implemented in software as the diff between the
generated output and the expected output.

The `tutor profile` command tracks which rules produce the most prediction
errors per model. This traces a **learning curve** [Ebbinghaus 1885] — same as
tracking how many times a student misses a spelling word before it sticks.
Models that show decreasing violation rates over successive `tutor eval` runs
are undergoing associative learning [Pearce & Bouton 2001].

## 4. The Zone of Proximal Development — Track Assignment

Vygotsky's Zone of Proximal Development [Vygotsky 1978]: learning is most
effective when the material is just beyond what the student can do alone but
within reach with scaffolding. Too easy → boredom, no learning (the model
already passes at 95%). Too hard → frustration, no learning (the model can't
parse the rules at all).

The track system (remedial → standard → honors) is ZPD applied to language
models:

- **Remedial**: fundamentals + Booster scaffolding. `[RULE]` checklists plus
  the sandbox (scratchpad, verification, few-shot, lookahead). The model can't
  do it alone — but with the tools, it can. This is Wood, Bruner & Ross's
  "scaffolding" [Wood et al. 1976].
- **Standard**: the full curriculum, less scaffolding. Classes are harder (code
  review, audit, architecture) but no Booster is needed.
- **Honors**: the same full curriculum, skip-eligible. Models that consistently
  score >90% on evaluation can skip mastered classes — the model has
  "internalized" the skill [Vygotsky 1978, p. 57].

The Booster activation threshold (working memory score < 0.65) is a ZPD
heuristic: models with less working memory capacity [Miller 1956] get more
scaffolding. This mirrors the educational practice of giving shorter,
more structured assignments to students with lower digit-span scores.

## 5. Myelination — The Correction Loop

When a human learns a skill — playing piano, writing code, reading — repeated
practice builds myelin sheaths around the relevant neural pathways [Fields
2008]. Signal velocity increases from ~1 m/s (unmyelinated) to ~100 m/s
(myelinated). The skill doesn't just get *more accurate* — it gets *faster and
less effortful*. This is the transition from "controlled processing" to
"automatic processing" [Shiffrin & Schneider 1977].

The `tutor fix` loop (eval → fix → re-eval until pass) is myelination for
attention weights. Each cycle reduces the "cognitive load" [Sweller 1988] of
generating the correct pattern. The first attempt requires the full `[RULE]`
prefix in context. By the tenth successful generation in sequence, the model
generates the correct output as the default — the attention pathway is
"myelinated," and the generation moves from conscious effort to automaticity.

The `--auto` flag (iterative fix until pass) is the pedagogical equivalent of
"drill until the pattern is automatic" — the same principle behind multiplication
tables and scales practice.

## 6. Working Memory and the 7 ± 2 Limit

Miller's Law [Miller 1956]: human working memory can hold 7 ± 2 items before
capacity is exceeded. A small model's context window isn't about storage —
it's about **working memory** [Baddeley & Hitch 1974]. An 8K context model can
hold approximately 8 small rules before the earlier ones decay from the
attention window.

Three direct consequences:

- **Instruction placement matters**: the primacy effect [Atkinson & Shiffrin
  1968] means the first items in the context window get the strongest encoding.
  In LLMs this is "Lost in the Middle" [Liu et al. 2023] — tokens at the start
  and end of long contexts receive disproportionately more attention weight.
  lm-tutor's `[RULE]` landmarks go FIRST, before the generation task.
- **Token efficiency**: `[RULE]` format compresses ~500 tokens of prose into
  ~120 tokens of working memory-efficient format. This is cognitive load theory
  [Sweller 1988] applied to prompt engineering: reduce extraneous load to
  maximize germane load (the actual learning).
- **External working memory**: the Booster scratchpad sandbox is the equivalent
  of writing a phone number on your hand. The model offloads intermediate
  reasoning steps so they don't crowd the context. This matches Baddeley's
  episodic buffer [Baddeley 2000] — a temporary storage system that integrates
  information across domains.

The working memory score (`f(context_window, param_count, tool_reliability)`)
is directly analogous to a digit span test in a cognitive assessment [Wechsler
1939]. Models that score low get the Booster.

## 7. Dual-Process Theory — System 1 and System 2

Kahneman's Thinking, Fast and Slow [Kahneman 2011]: System 1 is fast,
automatic, pattern-matching. System 2 is slow, deliberate, analytical. A small
model generating code defaults to System 1 — it pattern-matches from training
data without reasoning about correctness. This is why small models produce
confident but wrong output: they don't know what they don't know [Dunning &
Kruger 1999].

Chain-of-thought prompting [Wei et al. 2022] is a System 2 intervention:
forcing the model to verbalize intermediate reasoning steps before generating
the final answer activates the deliberation circuit. The `tutor booster` tools
(scratchpad verification, downstream lookahead) are System 2 prosthetics —
they give the model structured processes that mimic analytical reasoning, the
same way a decision tree helps a human override gut instinct.

The `prompt-design` class teaches the model when to use System 1 (low
temperature, known patterns) and when to invoke System 2 (novel problems, high
stakes). This is the AI equivalent of learning to "stop and think" before
responding — a metacognitive skill [Flavell 1979].

## 8. Neuroplasticity — The Core Thesis

The brain never stops rewiring. The old belief (fixed brain after childhood
[Hubel & Wiesel 1970, critical periods]) has been replaced by the understanding
that neuroplasticity persists throughout life [Merzenich et al. 1984, Kleim &
Jones 2008]. Every experience modifies synaptic weights.

The lm-tutor thesis: **models are equally plastic.** Their weights are frozen
(at inference time), but the *attention distribution* is always fluid. What the
model attends to changes with every input token [Vaswani et al. 2017, Figure 2].
This is lm-tutor's leverage: we can't change the weights (can't fine-tune), but
we don't need to. We change what the model attends to at generation time — and
attention is the only thing that determines output.

**Training determines capability; attention determines performance.** lm-tutor
optimizes the latter, leaving the former untouched. It works because attention
plasticity never stops [Bavelier et al. 2010].

This is distinct from fine-tuning, which is the equivalent of surgery. lm-tutor
is education — structured, repeated, corrective feedback delivered through the
existing attention mechanism. It works because the mechanism was already there.

## 9. Metacognition — The Profile Loop

Flavell's metacognition [Flavell 1979]: knowing what you know and what you
don't know. The most effective human learners self-monitor — they check their
understanding, identify gaps, and seek targeted remediation [Schraw &
Dennison 1994]. This is the difference between a novice who practices randomly
and an expert who practices deliberately [Ericsson et al. 1993].

The `tutor profile --model <id>` command gives the model its metacognitive
dashboard: per-class pass rates, weakest rules, next-class suggestions. The
model can see: "I pass code-review at 90% but I'm at 40% on audit — I should
retake audit before advancing." This is metacognition externalized into data.

The evaluation history (`~/.tutor/evals/<model>.jsonl`) is the model's learning
journal — a longitudinal record of what it knows and doesn't know, calibrated
against objective standards rather than self-assessment (which is unreliable
even for humans [Dunning & Kruger 1999]).

## 10. Chunking — FAIL/PASS as Paired Associates

The brain processes information in chunks [Miller 1956, Gobet et al. 2001]:
7 ± 2 items, but those items can be complex if chunked into a single unit. A
phone number is 10 digits, but we chunk it as 3-3-4 (three units). Chess
masters don't see 32 pieces — they see 4-5 strategic chunks [Chase & Simon
1973]. Expertise is largely the ability to chunk domain-specific patterns
[Ericsson & Kintsch 1995].

Each `[RULE]` in `class.yaml` carries a **paired FAIL/PASS example**. This is
paired-associate learning [McGeoch & Irion 1952, Atkinson & Shiffrin 1968].
The model doesn't learn the rule in isolation — it learns the rule +
counterexample as a single cognitive chunk. This is why FAIL/PASS pairs
[Min et al. 2022] are more effective than instructions alone: they define the
decision boundary. The model doesn't just know "add alt text" — it knows `<img
src="x.png">` is wrong and `<img src="x.png" alt="...">` is right. The boundary
between the two IS the chunk.

## 11. Associative Learning — Context-Dependent Memory

Memory is context-dependent [Tulving 1972, Godden & Baddeley 1975]: what you
learn in one context is recalled best in that context. Scuba divers who learned
a word list underwater recalled it best underwater; the list learned on land
was recalled best on land.

The `tutor learn` command embeds rules into the generation context. The model
learns the rule AND the context in which it applies. When the model enters a
code generation task, the `[RULE]` landmarks reactivate the same context,
triggering recall. This is encoding specificity [Tulving & Thomson 1973]: the
retrieval cue (the generation task) matches the encoding context (the class
injection), maximizing recall accuracy.

---

## References

Atkinson & Shiffrin 1968. "Human Memory: A Proposed System." *Psychology of
Learning and Motivation* 2.

Baddeley & Hitch 1974. "Working Memory." *Psychology of Learning and
Motivation* 8.

Baddeley 2000. "The Episodic Buffer." *Trends in Cognitive Sciences* 4(11).

Bavelier et al. 2010. "Removing Brakes on Adult Brain Plasticity." *Trends in
Cognitive Sciences* 14(3).

Chase & Simon 1973. "Perception in Chess." *Cognitive Psychology* 4(1).

Dunning & Kruger 1999. "Unskilled and Unaware of It." *Journal of Personality
and Social Psychology* 77(6).

Ebbinghaus 1885. *Über das Gedächtnis*.

Ericsson et al. 1993. "The Role of Deliberate Practice." *Psychological
Review* 100(3).

Ericsson & Kintsch 1995. "Long-Term Working Memory." *Psychological Review*
102(2).

Fields 2008. "White Matter in Learning, Cognition and Psychiatric Disorders."
*Trends in Neurosciences* 31(7).

Flavell 1979. "Metacognition and Cognitive Monitoring." *American
Psychologist* 34(10).

Gobet et al. 2001. "Chunking Mechanisms in Human Learning." *Trends in
Cognitive Sciences* 5(6).

Godden & Baddeley 1975. "Context-Dependent Memory in Two Natural
Environments." *British Journal of Psychology* 66(3).

Hebb 1949. *The Organization of Behavior*. Wiley.

Hubel & Wiesel 1970. "The Period of Susceptibility to Physiological Effects
of Unilateral Eye Closure." *Journal of Physiology* 206(2).

Kahneman 2011. *Thinking, Fast and Slow*. Farrar, Straus and Giroux.

Kleim & Jones 2008. "Principles of Experience-Dependent Neural Plasticity."
*Journal of Speech, Language, and Hearing Research* 51(1).

Liu et al. 2023. "Lost in the Middle: How Language Models Use Long Contexts."
arXiv 2307.03172.

McClelland & Rumelhart 1986. *Parallel Distributed Processing*. MIT Press.

McGeoch & Irion 1952. *The Psychology of Human Learning*. Longmans.

Merzenich et al. 1984. "Somatosensory Cortical Map Changes Following Digit
Amputation." *Journal of Comparative Neurology* 224(4).

Miller 1956. "The Magical Number Seven, Plus or Minus Two." *Psychological
Review* 63(2).

Min et al. 2022. "Rethinking the Role of Demonstrations." arXiv 2202.12837.

Moruzzi & Magoun 1949. "Brain Stem Reticular Formation and Activation of the
EEG." *Electroencephalography and Clinical Neurophysiology* 1(4).

Pearce & Bouton 2001. "Theories of Associative Learning." *Annual Review of
Psychology* 52.

Rescorla & Wagner 1972. "A Theory of Pavlovian Conditioning." In *Classical
Conditioning II*.

Schraw & Dennison 1994. "Assessing Metacognitive Awareness." *Contemporary
Educational Psychology* 19(4).

Schultz, Dayan & Montague 1997. "A Neural Substrate of Prediction and
Reward." *Science* 275(5306).

Shiffrin & Schneider 1977. "Controlled and Automatic Human Information
Processing." *Psychological Review* 84(2).

Sutton & Barto 2018. *Reinforcement Learning: An Introduction*. 2nd Ed. MIT
Press.

Sweller 1988. "Cognitive Load During Problem Solving." *Cognitive Science*
12(2).

Tulving 1972. "Episodic and Semantic Memory." In *Organization of Memory*,
pp. 381-403.

Tulving & Thomson 1973. "Encoding Specificity and Retrieval Processes."
*Psychological Review* 80(5).

Vaswani et al. 2017. "Attention Is All You Need." NeurIPS 2017.

Vygotsky 1978. *Mind in Society*. Harvard University Press.

Wei et al. 2022. "Chain-of-Thought Prompting Elicits Reasoning." arXiv
2201.11903.

Wood, Bruner & Ross 1976. "The Role of Tutoring in Problem Solving."
*Journal of Child Psychology and Psychiatry* 17(2).
