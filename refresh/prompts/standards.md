# The standards a refresh must hold

Read this before editing anything under `raw/`, `bible/`, or `keri-doctrine.md`. It is the contract that makes this corpus worth citing; a refresh that adds current information while loosening it has made the bible worse, not fresher. When a rule here conflicts with an instinct to be helpful, the rule wins.

## 1. Every claim carries a quote, and every quote carries a pin

A claim enters the corpus only with a **verbatim quote of 25 words or fewer** from a primary source, plus `file §heading` and a line-number hint, at a **named commit**. The quoted text is the citation of record; the line number is a hint that will drift and is expected to. If you cannot produce the quote, you do not have the claim — write down the gap instead, in the note's open-questions section.

Primary means the source itself. A diff is not the source. A commit message is not the source. Another note's summary is not the source, and neither is a previous session's output. Open the file at the commit and read the passage the quote comes from, including enough around it to know the quote is not reversed by its next sentence. This corpus has already been burned twice by relaying someone else's summary as though it were the source.

## 2. Provenance classes are load-bearing and never upgraded for convenience

The provenance markers (`[N]`, `[N1.1]`, `[K]`, `[P]`, `[V]`, `[SAM-DIRECT]`) are defined in `docs/house-style.md`, and their order is a real ordering.

A claim may only be marked at the tier its citation actually supports. Moving `[N1.1]` → `[N]` requires the text in the standardizing branch at a named commit, not an expectation that it will land. Moving `[P]` → `[K]` requires the code, not a merged PR title.

Spoken and first-hand report needs care. Edited auto-captions of conference talks (`raw/14`) preserve near-wording, never exact speech. They may be quoted, but only as the captions read, with a caption locator giving speaker, talk and time (`docs/house-style.md`, Citations), and only as evidence of status, intent and framing, never of a design detail. A first-hand account of a call (`raw/16`, section 0) preserves neither wording nor detail: it is usable for status and intent only and is never quoted. Do not launder either into a stronger citation by finding similar words in a written source.

## 3. Append and correct; never silently rewrite

When a source now contradicts something the corpus says, the old claim does not vanish. Mark it superseded, dated, with what replaced it and why. `raw/16 §8` item 3 is the model: the question struck through, the resolution underneath, and the general lesson drawn out ("a dead discussion thread is not evidence of a dead idea"). The record of having believed something, and of what changed, is part of what a reader is buying.

The same applies to an open question that closes, a residual that resolves, and a shibboleth that stops being one.

## 4. Hedged register, conditional guarantees

State KERI's claims as KERI states them, then state the boundary. Every security property is relative to its assumptions; name them. Do not let a confident sentence carry a shaky one along with it. Where the corpus is candid that an outsider critique survives reframing — immature observer tooling, thin formal literature, no eIDAS-equivalent standing — that candor is doctrine and stays.

Distinguish an author's assessment from a surveyed result. When Sam writes "AFAIK, only KERI/ACDC provides such protection", that is his assessment and the corpus repeats it as one.

## 5. Chapters keep their shape

Form is governed by `docs/house-style.md`: the chapter skeleton (thesis, status where the material is pre-normative, numbered sections, Sources), logical markup with no bold or italics, permanent heading anchors, the locator forms, and no hard wrapping. A refresh updates the pins in each chapter's Sources section; it does not drop them.

## 6. What a refresh may not do unattended

- **No new `bible/` chapter.** A new chapter is a structural decision about what the bible is. Propose it in the PR body, with what it would cover and which sources it would rest on. A new `raw/` note for a newly discovered topic is fine — that is mining, not restructuring.
- **No retargeting the manifest.** `branches`, `chapters` and `tier` in `refresh/sources.yaml` are reviewed fields. Propose changes in the PR body; do not apply them.
- **No advancing `last_mined` for a source you did not re-read.** `last_scanned` advances every run. `last_mined` advances only where a note was actually re-read against that commit. Under-claim rather than over-claim: the pin is a promise about what was read.
- **No writing to a WebOfTrust or trustoverip conversation.** Nothing in this procedure files an issue, comments on a discussion, or opens a PR anywhere but `dhh1128/keri-bible`. If a refresh turns up something that ought to be raised upstream, write it in the PR body and let Daniel raise it himself.

## 7. Fail loud, and cut what you cannot verify

A quote that cannot be found in its source at its pinned commit is **cut**, not reworded into something that can be. Record the cut in the PR body with what it used to support. A claim whose support was cut either finds a new citation or is marked as unsupported and struck.

A source that cannot be read is an error, reported as one. A quiet month and a broken config look identical from the outside, and only one of them is good news. Never let the second masquerade as the first.
