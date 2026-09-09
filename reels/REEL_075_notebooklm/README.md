# 📓 The NotebookLM Briefing System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![AI_SNIPP](https://img.shields.io/badge/Curated%20by-AI__SNIPP-cyan.svg)](https://instagram.com/ai_snipp)
[![Tool](https://img.shields.io/badge/Tool-NotebookLM-1a73e8.svg)](https://notebooklm.google.com)

The exact way to turn a pile of research — docs, PDFs, YouTube talks, your own
notes — into a **spoken briefing you can trust**, using Google's free
**NotebookLM**.

> **Featured on AI_SNIPP Reel #075:** *"Google quietly built a free tool that
> reads your research back to you like a podcast — barely anyone uses it."*

The thing that makes NotebookLM different from ChatGPT/Claude/Gemini for research:
**it only answers from the sources you give it, and every sentence links back to
the exact line it came from.** It is a closed-book model over *your* library, not
an open-book model guessing from the internet.

---

## 📑 Contents

1. [When to reach for this](#-when-to-reach-for-this)
2. [The 4-step workflow](#-the-4-step-workflow)
3. [The grounding prompts](#-the-grounding-prompts)
4. [Source hygiene (why your answers get worse)](#-source-hygiene)
5. [`source_manifest.py` — track what you fed it](#-source_manifestpy)
6. [Limits & gotchas](#-limits--gotchas)
7. [FAQ](#-faq)

---

## 🎯 When to reach for this

| Situation | Why NotebookLM beats a normal chatbot |
|---|---|
| 15 tabs of docs open, need the gist | Audio Overview = a 6–12 min two-host briefing on *your* set, listen once at 1.5× |
| "Did the paper actually say that?" | Every claim is a tappable citation → the exact sentence in the source |
| Comparing 5 vendors / 5 approaches | Ask "where do these disagree?" and it quotes both sides |
| Onboarding to a new codebase or domain | Drop the README + design docs + a call transcript, then interrogate it |
| You don't trust AI summaries | Grounded mode: it says "the sources don't cover this" instead of inventing |

Not for: live/breaking info (it only knows your sources), or anything you
haven't actually collected yet.

---

## 🧭 The 4-step workflow

### 1. Add sources one at a time

`+ Add source` → paste a link, upload a PDF, drop a Google Doc, or paste a
**YouTube URL** (it transcribes it). Free tier: **up to 50 sources per notebook**,
~500k words each.

Good sources: primary docs, official specs, papers, transcripts of talks, your
own written notes. Bad sources: SEO listicles, a page that's mostly navigation,
three articles that all rewrite the same press release (see
[Source hygiene](#-source-hygiene)).

### 2. Generate the Audio Overview

Studio panel → **Audio Overview → Generate**. ~90 seconds later you get a
two-host "deep dive" conversation about your sources. Use it as a **map**, not
the final word — note which sources the hosts lean on, then go read those.

> Customize it: before generating, click **Customize** and tell it the audience
> and focus, e.g. *"Assume I'm an engineer. Skip the intro. Focus on the
> trade-offs and the numbers."*

### 3. Interrogate it in chat — grounded

Ask questions in the chat box. Force it to stay grounded with the prompts in
[`grounding_prompts.md`](./grounding_prompts.md). The one to always start with:

```
Answer only from the sources. If the sources don't cover something, say so
explicitly. Do not use outside knowledge.
```

### 4. Verify every claim via its citation

Each sentence in an answer has a small **citation chip** (`¹ ² ³`). **Tap it** —
the source panel opens and scrolls to the exact highlighted line. If a claim has
no citation, treat it as unverified. This 5-second habit is the whole point of
using NotebookLM instead of a normal chatbot.

---

## 💬 The grounding prompts

Full pack in [`grounding_prompts.md`](./grounding_prompts.md). The three that do
most of the work:

```
1.  Summarise each source in 2 lines: its main claim + its strongest evidence.

2.  Where do these sources disagree or contradict each other? Quote both sides
    with citations.

3.  List the 5 most important questions these sources still leave unanswered.
```

---

## 🧹 Source hygiene

NotebookLM's answers are only as good as the library. The failure mode is
**dilution**: 5 pages that all summarise the same announcement make the model
over-weight that announcement and speak with false confidence.

Rules of thumb:

- **One canonical source per fact.** Prefer the primary (the spec, the paper,
  the filing) over coverage of it.
- **Drop near-duplicates.** If two sources share a domain and a topic, keep the
  better one.
- **Name your sources well.** NotebookLM shows source titles everywhere; a
  notebook of `Untitled document (3)` is unusable at 30 sources.
- **Prune before you hit 50.** The cap is per-notebook; a focused 12-source
  notebook out-answers a bloated 50-source one.

`source_manifest.py` (below) helps you see the library at a glance and flags
likely duplicates.

---

## 🐍 `source_manifest.py`

A zero-dependency (Python 3.9+ stdlib only) helper. Point it at a folder of files
you're about to upload and/or a `urls.txt`, and it prints a clean, numbered,
de-duplicated manifest — plus warnings for same-domain duplicates and probable
low-value pages.

```bash
python source_manifest.py --dir ./research --urls urls.txt
python source_manifest.py --dir ./research --urls urls.txt --check   # warnings only
```

Example output:

```
NOTEBOOKLM SOURCE MANIFEST  —  17 sources
------------------------------------------------------------
 01  [pdf ]  attention-is-all-you-need.pdf
 02  [pdf ]  flash-attention-2.pdf
 03  [url ]  https://developer.nvidia.com/...       (nvidia.com)
 04  [url ]  https://developer.nvidia.com/blog/...  (nvidia.com)   ⚠ same domain as #03
 ...
⚠  3 warnings — review before uploading (see --check)
Sources: 12 files, 5 urls   ·   NotebookLM free tier cap: 50
```

Use the numbered list as a checklist inside NotebookLM so you always know what's
loaded.

---

## ⚠️ Limits & gotchas

| Limit | Detail |
|---|---|
| Sources per notebook | 50 (free) / 300 (Plus) |
| It only knows your sources | No live web, no "what happened today" |
| Audio Overview language/length | Improving, but not fully controllable — treat as a first pass |
| Long PDFs | Split a 400-page PDF into chapters; retrieval is sharper on focused sources |
| Citations point to *a* line | Occasionally the neighbouring line — still 100× faster than re-finding it yourself |
| Privacy | Google states personal notebooks aren't used to train models; still don't upload secrets |

---

## ❓ FAQ

**Is it actually free?** Yes — core features (sources, Audio Overview, chat,
citations) are on the free tier. NotebookLM Plus raises the limits.

**Can I use it on my phone?** Yes, there's an app; the Audio Overview is the
killer mobile feature — generate on desktop, listen on the commute.

**Does it hallucinate?** Far less than an open-book chatbot, because it's
retrieval-grounded — but a weak/contradictory source set can still produce a
confident-sounding wrong answer. That's what the citation-tap habit and
`grounding_prompts.md` are for.

**How is this different from Perplexity?** Perplexity searches the web for you.
NotebookLM does the opposite — it locks to the library *you* curated and never
leaves it.

---

*Curated by [@ai_snipp](https://instagram.com/ai_snipp) · MIT licensed · Reel #075*
