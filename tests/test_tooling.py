"""Unit tests for the corpus tooling. Run with `python3 -m unittest discover -s tests`."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "refresh"))

import freshness  # noqa: E402
import lint_corpus  # noqa: E402



class QuotePairing(unittest.TestCase):
    """freshness.quoted_needles must pair quote marks the way a reader would."""

    def needles(self, text):
        return [frag for _, frag in freshness.quoted_needles(text)]

    def test_short_quote_does_not_shift_pairing(self):
        # Before 2026-10-14 the pattern skipped the short quote while pairing, so the long
        # quotation was paired with the prose gap after it and never checked.
        text = 'A "term" and then a long stretch of ordinary prose, "a real quotation that is long enough to check" (src > H, L5).'
        self.assertEqual(self.needles(text), ["a real quotation that is long enough to check"])

    def test_locator_between_quotes_is_not_a_quote(self):
        text = '"the first quotation is long enough to count" (KERI spec > A, L1) and "the second quotation is long enough too" (KERI spec > B, L2).'
        self.assertEqual(len(self.needles(text)), 2)
        self.assertTrue(all("KERI spec" not in n for n in self.needles(text)))

    def test_pairing_is_per_line(self):
        text = 'an odd mark " on one line\n"a quotation that is long enough to count" on the next'
        self.assertEqual(self.needles(text), ["a quotation that is long enough to count"])

    def test_elided_quote_matches_longest_fragment(self):
        text = '"short bit... the longer fragment of the elided quotation"'
        self.assertEqual(self.needles(text), ["the longer fragment of the elided quotation"])

    def test_unicode_ellipsis_splits_like_three_dots(self):
        self.assertEqual(self.needles('"short bit… the longer fragment of the elided quotation"'), ["the longer fragment of the elided quotation"])

    def test_editorial_insertion_is_removed_from_needle(self):
        needle, _ = freshness.quoted_needles('"the Issuer [sic] anchors the credential in a registry"')[0]
        self.assertNotIn("sic", needle)


class Lint(unittest.TestCase):
    def published(self, text, path="bible/01-x.md"):
        return lint_corpus.check_published(path, text, {path: lint_corpus.anchors_of(text)})

    CHAPTER = "# 01 — Title {#t}\n\n## Thesis {#thesis}\n\nText.\n\n## 1. One {#one}\n\nText.\n\n## Sources {#sources}\n\n- A — b.\n"

    def test_clean_chapter_passes(self):
        self.assertEqual(self.published(self.CHAPTER), [])

    def test_bold_flagged_but_not_inside_quote_or_code(self):
        self.assertTrue(self.published(self.CHAPTER + "\nSome **bold** text.\n"))
        self.assertEqual(self.published(self.CHAPTER + '\nA "quoted **bold** span" and `**code**`.\n'), [])

    def test_dunder_in_locator_is_not_bold(self):
        self.assertEqual(self.published(self.CHAPTER + "\n(keripy core/eventing.py, Kevery.__init__, L1 @abcdef012)\n"), [])

    def test_italics_flagged(self):
        self.assertTrue(self.published(self.CHAPTER + "\nAn *emphasized* word.\n"))

    def test_section_sign_flagged_outside_quotes(self):
        self.assertTrue(self.published(self.CHAPTER + "\nSee §3.\n"))
        self.assertEqual(self.published(self.CHAPTER + '\nIt says "see §3 of the spec".\n'), [])

    def test_missing_and_duplicate_anchor(self):
        self.assertTrue(self.published(self.CHAPTER + "\n## 2. Two\n"))
        self.assertTrue(self.published(self.CHAPTER.replace("{#one}", "{#thesis}")))

    def test_ampersand_in_heading(self):
        self.assertTrue(self.published(self.CHAPTER.replace("1. One", "1. One & two")))

    def test_skipped_level(self):
        self.assertTrue(self.published(self.CHAPTER + "\n#### Deep {#deep}\n"))

    def test_skeleton(self):
        self.assertTrue(self.published(self.CHAPTER.replace("## Thesis {#thesis}", "## 0. Intro {#intro}")))

    def test_broken_link(self):
        self.assertTrue(self.published(self.CHAPTER + "\nSee [section 9](#nine).\n"))
        self.assertEqual(self.published(self.CHAPTER + "\nSee [section 1](#one).\n"), [])

    def test_chapter_over_length_limit(self):
        long = self.CHAPTER.replace("## Sources", ("word " * 7600) + "\n\n## Sources")
        self.assertTrue(any("length" in p for p in self.published(long)))

    def test_fenced_sources_heading_does_not_end_the_body(self):
        long = self.CHAPTER.replace("## Sources", "```\n## Sources (quoted example)\n```\n\n" + ("word " * 7600) + "\n\n## Sources")
        self.assertTrue(any("length" in p for p in self.published(long)))

    def test_hard_wrap(self):
        self.assertTrue(lint_corpus.check_wrap("x.md", "A paragraph that\ncontinues here.\n"))
        self.assertEqual(lint_corpus.check_wrap("x.md", "- item\n- item\n\n| a |\n| b |\n\n```\ncode\ncode\n```\n"), [])


class Build(unittest.TestCase):
    def test_prefixes_anchors_and_rewrites_links(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "bible").mkdir()
            (d / "docs").mkdir()
            (d / "docs/house-style.md").write_text("# S\n\n## Provenance markers {#markers}\n\nLegend text. This section is the legend that `build-bible.py` and the site generate from.\n\n## Next {#next}\n")
            (d / "bible/01-a.md").write_text("# 01 — A {#a}\n\n## Thesis {#thesis}\n\nSee [x](#thesis) and [y](02-b.md#thesis).\n")
            (d / "bible/02-b.md").write_text("# 02 — B {#b}\n\n## Thesis {#thesis}\n\nB.\n")
            out = subprocess.run([sys.executable, str(ROOT / "build-bible.py")], cwd=d, capture_output=True, text=True, check=True).stdout
        self.assertIn("{#01-thesis}", out)
        self.assertIn("{#02-thesis}", out)
        self.assertIn("[x](#01-thesis)", out)
        self.assertIn("[y](#02-thesis)", out)
        self.assertIn("Legend text.", out)
        self.assertNotIn("generate from", out)


class SiteNav(unittest.TestCase):
    def test_every_chapter_is_in_the_site_nav(self):
        import tomllib
        cfg = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
        listed = set()
        for entry in cfg["project"]["nav"]:
            for value in entry.values():
                if isinstance(value, list):
                    listed.update(v for v in value if isinstance(v, str))
        chapters = {f"bible/{p.name}" for p in (ROOT / "bible").glob("*.md")}
        self.assertEqual(chapters - listed, set(), "chapters missing from zensical.toml's nav")


if __name__ == "__main__":
    unittest.main()
