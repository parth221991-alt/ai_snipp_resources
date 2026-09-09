# NotebookLM Grounding Prompts

Copy-paste prompts for the NotebookLM **chat** box. They force it to stay inside
your sources, surface disagreement, and expose gaps — the things a normal
chatbot glosses over.

Order of use: **0 → 1 → (2,3,4 as needed) → 5 before you rely on anything.**

---

## 0. Lock it to the sources (always start here)

```
Answer only from the sources I've added. If the sources don't cover something,
say "not in the sources" — do not use outside knowledge and do not guess.
Every claim must carry a citation.
```

## 1. Map the library

```
Summarise each source in exactly 2 lines: (a) its single main claim, (b) its
strongest piece of supporting evidence. List them as a numbered table with the
source title.
```

## 2. Find the disagreements

```
Where do these sources disagree, contradict, or hedge against each other?
For each conflict: quote both sides verbatim with citations, then tell me which
source is more credible on that specific point and why.
```

## 3. Expose the gaps

```
List the 5 most important questions these sources leave unanswered. For each,
say which source came closest and what exactly is missing.
```

## 4. Pressure-test a specific claim

```
I want to rely on this claim: "<paste claim>".
Show me every sentence in the sources that supports it, every sentence that
weakens or complicates it, and the exact conditions under which it holds.
```

## 5. Build the briefing

```
Write a one-page briefing for someone who has 3 minutes: the 5 things that
matter, each as a headline + one sentence + citation. Then a "what I'd still
verify" list. No hype, no filler.
```

---

## For specific source types

**Research papers / technical docs**
```
For each paper: state the exact setup (dataset, model, hardware, N), the headline
result WITH its error bars or caveats, and one limitation the authors admit to.
Flag any result that's only shown in an appendix or a figure, not the main text.
```

**Meeting / call / interview transcripts**
```
Extract every decision made, every open action item with an owner, and every
point where participants disagreed. Quote the exact line for each. Ignore
smalltalk.
```

**Competitor / vendor material**
```
Separate verifiable facts (specs, prices, dates) from marketing claims
("fastest", "best", "seamless"). For each marketing claim, note whether anything
in the sources actually substantiates it.
```

**Legal / regulatory / policy documents**
```
List every obligation ("must", "shall", "required to") with its citation and
who it applies to. Then list the exceptions and carve-outs. Do not paraphrase
the obligations — quote them.
```

---

## The Audio Overview customization prompt

Paste this into **Customize** before generating the Audio Overview:

```
Audience: a working engineer / analyst who already knows the basics. Skip the
introduction and definitions. Focus the whole conversation on: the trade-offs,
the numbers, where the sources disagree, and what's still unknown. Be concrete —
name the sources when you cite them.
```

---

*Reel #075 · [@ai_snipp](https://instagram.com/ai_snipp) · MIT licensed*
