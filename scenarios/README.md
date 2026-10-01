# Scenarios

End-to-end worked walkthroughs that stitch the doctrine in `bible/` to the keripy reference implementation's worked-example tests, following one concrete transaction from issuance through presentation.

These are a third genre, deliberately kept out of both neighbours. A `bible/` chapter states what is true about KERI for an adversarial reviewer, and is folded into `keri-bible.md` and loaded by the review panel as doctrine. A `field/` note records a dated measurement of someone's running infrastructure. A file here is neither: it is an *operational narrative* — "here is how these pieces compose to accomplish one real task" — grounded in named spec sections, `bible/` chapters, and specific keripy tests. It is kept outside `bible/` so `build-bible.py` does not concatenate it and the review panel does not load it as settled doctrine, because a scenario may lean on code that is still on a branch rather than in `upstream/main`.

Read the dated provenance header before trusting any claim. Each file pins the keripy commit/branch and the `bible/` basis it was synthesized from, and marks which parts are *built* in the reference implementation versus *modeled at the data-structure level* versus *pre-normative and unbuilt*.

- [`utah-sedi-age-residency.md`](utah-sedi-age-residency.md) — how a Utah citizen uses a SEDI identity credential plus a SEDI age credential to prove "legal Utah resident, over 18" under contractually-protected disclosure, assuming Utah's planned bulk issuance with pre-created registries.
