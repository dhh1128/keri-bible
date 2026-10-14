# House style

Status: adopted 2026-10-14. Changes to this file are proposed and argued in their own commit, never folded into a content change.

This file says how the corpus is written. `refresh/prompts/standards.md` says what may be claimed and on what evidence, and it stays the citation contract; where its §5 talks about form, this file replaces it. CI checks every rule below that a script can check, and each rule says whether it is checked.

The primary reader is a model loading the bible as context for an adversarial review. The second reader is a person on the published site, who arrives from a search or a citation and reads one section. Both need the same things: structure carried by markup a machine can see, and citations that resolve.

## Markup

### Logical markup only

Structure is carried by headings, lists, tables, block quotes and code spans. Bold and italics are not used. A paragraph that opens with a bold phrase is a heading that has not been written yet, and it becomes one. Emphasis inside a sentence is removed, and if the sentence then reads flat, the sentence is rewritten so the weight falls at its end. Checked: CI rejects `**` and `*`/`_` emphasis outside code spans.

Titles of papers, talks and specifications are written plain, and linked where a URL exists. They are not put in quotation marks, because quotation marks mean a quotation here (see Citations).

### Headings

One H1 per chapter: `# NN — Title`, where NN is the two-digit chapter number. H2 is a numbered section, `## N. Title`. H3 is a numbered subsection, `### N.M Title`. An unnumbered heading, used for the units that were bold-led paragraphs (a shibboleth's correction, a named finding), sits one level below its parent: H3 under a section with no numbered subsections, H4 under a numbered subsection. No level is skipped. Checked.

Heading text contains no ampersand; write "and". An ampersand is mangled differently by different slug generators, table-of-contents builders and HTML escapers, so it breaks links in ways that vary by tool. This retitles chapters 04, 05, 06 and 08. Checked.

Every heading carries an explicit, permanent anchor in attribute-list syntax: `## 5. Edges, chaining, and the operator families {#edges}`. The anchor is a short lowercase slug of letters, digits and hyphens, chosen once and never changed, even when the section is renumbered or retitled. Numbers are for reading and anchors are for citing, and keeping them apart is what lets either change without breaking the other. Anchors are unique within a chapter, and a section's full identity is its chapter plus its anchor: on the site, `/05-acdc-and-verifiable-data/#edges`. `build-bible.py` prefixes each anchor with its chapter number in the assembled `keri-bible.md` (`#05-edges`) and rewrites cross-references to match, so the single file stays unambiguous. Checked: every heading has an anchor, anchors are unique within their chapter, and an anchor that existed at the last release may not disappear (it may move, and the old one is kept as an alias).

### Chapter skeleton

In order: the H1; `## Thesis {#thesis}`; `## Status {#status}`, only where the chapter covers pre-normative material; the numbered body sections, starting at 1; `## Sources {#sources}`. Every chapter has all of them except Status. Checked.

Chapters carry no marker key and no "how to read" section. The marker legend below is generated once into the assembled `keri-bible.md` (by `build-bible.py`) and onto a legend page of the published site that every page links to, so a reader or model arriving at one chapter cold still has it. A caveat about one source goes in that source's Sources entry; a caveat about how far the whole chapter is from normative goes in Status.

### Paragraphs and punctuation

One line per paragraph, never hard-wrapped, in every markdown file in the repo. Checked.

Em dash with a space each side ( — ), never `--`. US spelling. Dates are ISO, `2026-10-14`. Commits are written as the first nine hex digits in a code span. Checked, except spelling.

The section sign (§) is not used in anything the corpus writes, because it cannot be typed on most keyboards. Locators and cross-references use the forms below instead. It survives only inside a quotation whose source uses it.

## Provenance markers

A marker says what kind of source a claim rests on, and the order is real: a later marker is never upgraded to an earlier one without new evidence at a named commit. A marker is written plain, with no bold and no code span. This section is the legend that `build-bible.py` and the site generate from.

- `[N]`, normative. The text is in the line of a specification that the community is actively standardizing, its `main` branch.
- `[N1.1]`, forward branch. The text is in a specification's `v1.1` branch and not in `main`. It is new thinking that is likely, not certain, to become normative, and it binds nobody today.
- `[K]`, implemented. An implementation (keripy unless named otherwise) behaves this way at a named commit. Code is evidence about code, not about what the specification requires.
- `[P]`, proposed. A design stated in a discussion, issue, pull request, whitepaper or code on an unmerged branch, and in no specification. However confident its author, it binds nobody.
- `[V]`, vendor or deployment practice. What one organization's product, service, schema set or deployment does. Evidence of how the doctrine survives contact with practice; never evidence of what KERI is. This absorbs the corpus's current unmarked "deployment evidence" and "applied schema corpus" classes.
- `[SAM-DIRECT]`, Sam Smith in his own voice outside a specification: keri.one, his conference talks, and personal communications. It carries his intent, which is often exactly what a reviewer needs, and it is not normative.

Unmarked text has one meaning everywhere. A specification citation with no marker is to that specification's standardizing line, and so means `[N]`. A claim with neither a marker nor a citation is the chapter's own synthesis, the weakest kind of evidence in it.

`[K-fork]` is retired. It marked code that exists only on an unmerged personal fork (in practice, Daniel's post-quantum branch of signify-ts, `raw/10` section 11). Code nobody else runs is a proposal made in code, so it is cited as `[P]`, with the fork, branch and commit in the locator.

## Citations

### Citing a source from the bible

The quotation is the citation of record, as `standards.md` §1 requires, and it sits in straight double quotes. It is followed, in parentheses, by a locator in one fixed form:

`"quoted text" (source > Heading > Subheading, L123 @abcdef012)`

where `source` is the short name defined in the chapter's Sources section (`KERI spec`, `ACDC spec`, `wtbo.md`, `keripy vdr/verifying.py`), and the `>` path names the heading the quote sits under, as deep as needed to be unambiguous. The line number is a hint and may drift; the heading and the quote may not. Code has no headings, so a code locator is `(keripy vdr/verifying.py, Verifier.verifyChain, L455 @80f77b73b)`, naming the function or class.

Conference captions may be quoted. They are cited as the captions read, not as what was said, so the locator says so and gives the time: `"quoted caption text" (KERIConf26 caption, Sam Smith, The Digital Identity Tradespace, 12:34)`. A caption quote is never cited as evidence of a design detail, only of intent and framing, and it is checked against the caption files like any other quote. This amends `standards.md` §2, which currently forbids quoting captions at all.

### Text-fragment links

Where the source is published as HTML, the locator also links to it with a text fragment, which makes a browser scroll to the quoted words and highlight them. A fragment is not a fuzzy match, so rather than dropping words, cite a range: the fragment form `#:~:text=start,end` matches from the first occurrence of `start` to the next occurrence of `end`, so a long quotation is linked by its first few words and its last few. Example: `https://trustoverip.github.io/kswg-acdc-specification/#:~:text=the%20more%20general%20goal,exploitation%20of%20data`. Commas, hyphens and ampersands inside the text must be percent-encoded, because they are fragment syntax.

Two limits. A fragment only resolves against rendered HTML, so it supplements the commit-pinned locator and never replaces it. And a fragment that no longer matches fails silently, scrolling nowhere, so a scheduled CI job checks every fragment against the live page the way `freshness.py` checks quotes. How tolerant matching is of case, whitespace and punctuation differences has not been tested here; the site prototype will settle it before the conversion starts writing fragments.

### Citing within the bible

A cross-reference is a link to the target heading's anchor, whose text names the chapter and section in words: `[chapter 05, section 5.1](05-acdc-and-verifiable-data.md#verifying-ground-truth)`. Not "the presentation chapter", not a bare file path. Checked: every link resolves.

### Citing the bible from outside

Each section is citable by its anchor URL on the published site, and by a commit-pinned GitHub URL for anyone who needs the exact text. The site footer of every page shows the commit it was built from. A suggested citation form goes on the site's front page.

## Sources sections

Today two chapters have one (01 and 08), and both are bulleted lists in an ad hoc form. ACM and similar styles do not fit: they assume published works with venues and years, and most of this corpus's sources are repositories read at a commit. Every chapter's Sources section is instead a bulleted list, one entry per short name the chapter uses, in this form:

`- KERI spec — Key Event Receipt Infrastructure (KERI) specification, Trust Over IP. trustoverip/kswg-keri-specification, spec/spec-body.md, main @fbdd4a615 (2026-08-28). Mined in raw/01.`

That is: the short name, an em dash, the title and author or body, the location (repository and path, or URL), the pin with its date, and the raw note it was mined in. A source read at two pins gets both, each saying which claims it supports. Entries are sorted by short name. This is the only place pins live.

## What this would change

Measured on 2026-10-14: about 1,600 bold spans across the ten chapters, of which about 760 open a paragraph and would become H4 headings; about 730 italic spans; no explicit anchors anywhere; at least four different citation-locator forms; section signs throughout; ampersands in four chapter titles; Sources sections in two chapters of ten; and lettered subsections (`§3a`, `§5a`) in chapters 04 and 08, which `keri-review-panel/personas/cesr-wire-serialization-engineer.md` cites by number and would need updating with them. It also removes the ten "How to read this chapter" sections, moving their caveats into Sources and Status. `standards.md` §2 and §5 change to match.
