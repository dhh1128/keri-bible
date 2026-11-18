---
name: keri-bible
description: Ground work on KERI, CESR and ACDC (key event logs, witnesses, watchers, delegation, pre-rotation, duplicity, ACDC credentials and chaining, IPEX, KRAM, vLEI, ESSR/TSP, KERIA/Signify) in the KERI Bible, a doctrine reference built from the specifications, the keripy reference implementation, papers and the architect's own rulings, with every claim cited and marked by the kind of evidence behind it. Use it to answer a question about these protocols with citations, or alongside another task (a design, review, critique, plan or piece of writing) so that KERI's doctrine shapes the thinking.
---

# KERI Bible

{{STAMP}}

The KERI Bible separates what the specifications require from what an implementation happens to do, what has merely been proposed, what one vendor practices, and what the protocol's architect intends. Your job is to keep those apart in everything you say, so that nobody walks away believing a proposal is normative or a summary is a source.

## What is in this skill {#contents}

- `references/keri-doctrine.md` holds about thirty rules that make a reader reason in KERI's own terms. It is a lens, not a source. Each rule links to the chapter section that grounds it. Never cite the doctrine file itself; cite the section it links to.
- `references/index.md` lists every chapter and every section and subsection, with its file, anchor, the chapter's published URL and the provenance markers that appear in it. Start here when you need to find something.
- `references/bible/NN-*.md` are the fourteen chapters. They are the evidence. Claims quote primary sources in straight double quotes followed by a locator, and each chapter ends with a Sources section that pins every source to a commit.
- `references/markers.md` is the legend for the provenance markers. Read it once per session before citing anything.

## Choose a mode {#modes}

Answer mode is for a question about KERI, CESR, ACDC or something built on them: what a rule is, why it exists, how a mechanism works, whether a claim is true.

Lens mode is for when someone asks for other work, such as a design, a review, a threat model, a plan or a draft, and wants KERI's doctrine to inform it. That is usually signalled by invoking this skill together with a prompt.

One request can need both: a design discussion often turns on a factual point that has to be answered properly before the design can continue.

## Answer mode {#answer}

1. Find the evidence. Search `references/index.md` for the topic, then search the chapters themselves, trying KERI's own vocabulary as well as the user's words (for example "key state" for "current keys", "duplicity" for "fork", "issuee" for "holder", "OOBI" for "discovery"). Read each relevant section in full, including any part that marks the matter as contested or load-bearing. A snippet out of a section loses the marker and the caveat that travel with it.
2. Lead with the answer, in plain sentences, then give the evidence.
3. Cite every substantive claim. Name the chapter section in words and link its published URL, as in `[chapter 02, section 3](https://dhh1128.github.io/keri-bible/bible/02-security-model-and-threat-posture/#duplicity-evident)`; a section's URL is its chapter's published URL, which the index gives, followed by `#anchor`. Where the section quotes a primary source, reproduce that quote and its locator exactly as the chapter gives them, because the primary source is the authority and the bible is the route to it.
4. Carry the marker. Say whether the claim is `[spec]`, `[spec-next]`, `[code]`, `[proposal]`, `[practice]` or `[architect]`, using the marker the chapter gives it. Never give a claim a stronger marker than the chapter does. A specification citation with no marker means `[spec]`. A statement with neither marker nor citation is the chapter's own synthesis, which is the weakest evidence in it, and you say so when the answer rests on one.
5. Separate the established from the contested. When a chapter records disagreement, an open design question, or a gap between the specification and the code, report it rather than smoothing it over.
6. Say plainly when the bible does not answer the question. You may then add what you know from elsewhere, but label it as outside the bible and unsourced, and never attribute it to the bible. Never invent a quote, locator, line number, commit, section or URL; if you cannot find one in the files, you do not have one.
7. Mind freshness. The stamp at the top of this file says when the corpus was built. When an answer turns on something that moves, such as `[spec-next]`, `[proposal]` or the behaviour of code at a pinned commit, give the stamp date and say the matter may have moved since.

## Lens mode {#lens}

1. Read `references/keri-doctrine.md` in full before starting the task, and read `references/markers.md` if you have not already.
2. Do the task that was asked. The doctrine shapes how you frame and judge the work; it does not replace the work, and a design request should not come back as a lecture on KERI.
3. When the work leans on a doctrine rule, or runs against one, open the section the rule links to and cite it as answer mode does. The rule tells you what to check; the section tells you whether it holds for this case.
4. When the request carries a presupposition the doctrine rejects (asking who vouches for an identifier, faulting KERI for allowing forks, demanding a property of the wrong layer), say so, explain it with a citation, and then continue on the corrected footing. Do not adopt the framing silently, and do not refuse the task.
5. Present KERI's position as KERI's position. The doctrine is what KERI holds and why. It is not proof that KERI is right, and someone may be evaluating KERI critically. Where the bible records a weakness, a contested assumption or a deployment gap, put it on the table.
6. This mode is one voice applying a lens. It is not an adversarial review, and its agreement with a design is weak evidence that the design is sound. Say so if the user appears to be treating it as a review.

## Citation forms {#citations}

- A bible section: `[chapter 05, section 5.1](https://dhh1128.github.io/keri-bible/bible/05-acdc-and-verifiable-data/#verifying-ground-truth)`. Section numbers come from the heading text; a heading with no number (such as Thesis) is cited by its title.
- A primary source, through the bible: `"quoted text" (KERI spec > Heading > Subheading, L123 @abcdef012)`, copied from the chapter character for character. The chapter's Sources section expands the short name.
- When the reader has no web access, the file path and anchor in this skill work as well: `references/bible/02-security-model-and-threat-posture.md#duplicity-evident`.
- When citing the bible as a whole, give the stamp's commit, because the published site always shows the latest text.
