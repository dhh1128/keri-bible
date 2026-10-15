"""Unit tests for the corpus tooling. Run with `python3 -m unittest discover -s tests`."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "refresh"))

import detect  # noqa: E402
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

    def test_curly_and_straight_apostrophes_match(self):
        self.assertEqual(freshness.norm("the middle doesn\u2019t matter"), freshness.norm("the middle doesn't matter"))

    def test_editorial_insertion_is_removed_from_needle(self):
        needle, _ = freshness.quoted_needles('"the Issuer [sic] anchors the credential in a registry"')[0]
        self.assertNotIn("sic", needle)


def tiny_pdf(text: str) -> bytes:
    """A one-page PDF showing `text` in Helvetica, built by hand so the test needs no PDF library."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
            b"/Resources << /Font << /F1 5 0 R >> >> >>",
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    return bytes(out)


class ConvertedFormats(unittest.TestCase):
    """freshness reads PDFs and SubRip captions as text, so quotes from papers and talks resolve."""

    SRT = ("\ufeff1\r\n00:00:01,000 --> 00:00:03,500\r\nthe witness pool is a\r\n\r\n"
           "2\n00:00:03,600 --> 00:00:05,000\n<i>service the controller</i>\nchooses for itself\n\n"
           "3\n00:00:05,100 --> 00:00:06,000\n2026\n")

    def test_srt_drops_cue_furniture_and_joins_cues(self):
        self.assertEqual(freshness.srt_text(self.SRT),
                         "the witness pool is a service the controller chooses for itself 2026")

    def test_quote_spanning_two_cues_matches(self):
        corpus = freshness.norm(freshness.converted_text("talk.srt", self.SRT.encode()))
        needle, _ = freshness.quoted_needles('"the witness pool is a service the controller chooses"')[0]
        self.assertIn(needle, corpus)

    def test_pdf_dispatches_to_pdf_extractor(self):
        from unittest import mock
        with mock.patch.object(freshness, "pdf_text", return_value="stub text") as stub:
            self.assertEqual(freshness.converted_text("paper.PDF", b"%PDF-stub-for-dispatch"), "stub text")
        stub.assert_called_once()

    def test_unknown_converted_format_raises(self):
        with self.assertRaises(ValueError):
            freshness.converted_text("x.docx", b"")

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext (poppler-utils) not installed")
    def test_pdf_text_extracted(self):
        text = freshness.pdf_text(tiny_pdf("Duplicity is detectable by any validator"))
        self.assertIn("Duplicity is detectable by any validator", text)

    def test_pdf_ligatures_spelled_out_and_line_hyphens_rejoined(self):
        from unittest import mock
        out = mock.Mock(returncode=0, stdout="more \ufb02exibility, contractually pro-\n  tected and self-\ndealing".encode())
        with mock.patch.object(freshness.subprocess, "run", return_value=out):
            corpus = freshness.norm(freshness.pdf_text(b"%PDF-stub"))
        for quote in ("more flexibility", "contractually protected", "self-dealing", "selfdealing"):
            self.assertIn(freshness.norm(quote), corpus)

    def test_non_ascii_path_is_read_from_the_ref_not_the_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            git = ["git", "-C", str(d), "-c", "user.name=t", "-c", "user.email=t@t"]
            subprocess.run(["git", "init", "-q", "-b", "main", str(d)], check=True)
            (d / "subtitles").mkdir()
            talk = d / "subtitles" / "Sam Smith \uff5c The Future of KERI.srt"
            talk.write_text(self.SRT)
            subprocess.run(git + ["add", "."], check=True)
            subprocess.run(git + ["commit", "-q", "-m", "x"], check=True)
            talk.write_text("1\n00:00:01,000 --> 00:00:02,000\nonly in the working copy\n")
            text = freshness.read_ref(d, "main", ["subtitles"])
        self.assertIn("service the controller chooses for itself", text)
        self.assertNotIn("only in the working copy", text)

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext (poppler-utils) not installed")
    def test_pdf_and_srt_read_from_a_git_ref(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            git = ["git", "-C", str(d), "-c", "user.name=t", "-c", "user.email=t@t"]
            subprocess.run(["git", "init", "-q", "-b", "main", str(d)], check=True)
            (d / "papers").mkdir()
            (d / "papers/a.pdf").write_bytes(tiny_pdf("Pre-rotation commits to the next key"))
            (d / "papers/talk.srt").write_text(self.SRT)
            (d / "papers/skip.bin").write_bytes(b"not read")
            subprocess.run(git + ["add", "."], check=True)
            subprocess.run(git + ["commit", "-q", "-m", "x"], check=True)
            text = freshness.read_ref(d, "main", ["papers"])
        self.assertIn("Pre-rotation commits to the next key", text)
        self.assertIn("service the controller chooses for itself", text)
        self.assertNotIn("not read", text)


class GhIssues(unittest.TestCase):
    """detect.issues_since lists issues and PRs and marks the threads a primary author is in."""

    LINES = "\n".join([
        '{"number": 12, "title": "a bug", "url": "https://x/12", "updated": "2026-10-14T01:00:00Z", "created": "2026-10-01T00:00:00Z", "author": "alice", "pr": false, "comments": 3}',
        '{"number": 13, "title": "a fix", "url": "https://x/13", "updated": "2026-10-14T02:00:00Z", "created": "2026-10-02T00:00:00Z", "author": "SmithSamuelM", "pr": true, "comments": 0}',
        '{"number": 14, "title": "quiet", "url": "https://x/14", "updated": "2026-10-14T03:00:00Z", "created": "2026-10-03T00:00:00Z", "author": "bob", "pr": false, "comments": 1}',
        ""])

    def test_items_and_primary_flag(self):
        from unittest import mock
        with mock.patch.object(detect, "run", return_value=self.LINES) as run, \
             mock.patch.object(detect, "gh_json", return_value=[{"number": 12}]) as search:
            hits = detect.issues_since("o/r", "2026-10-14", {"SmithSamuelM"})
        self.assertIn("since=2026-10-14T00:00:00Z", " ".join(run.call_args[0][0]))
        self.assertIn("--involves", search.call_args[0][0])
        self.assertEqual([h["number"] for h in hits], [12, 13, 14])
        self.assertEqual({h["number"]: h["primary"] for h in hits}, {12: True, 13: True, 14: False})
        self.assertTrue(hits[1]["pr"])
        self.assertEqual(hits[0]["updated"], "2026-10-14")

    def test_non_json_output_is_an_error(self):
        from unittest import mock
        with mock.patch.object(detect, "run", return_value='{"message": "Not Found"\n'):
            with self.assertRaises(detect.SourceError):
                detect.issues_since("o/r", "2026-10-14", set())


class PageHash(unittest.TestCase):
    """detect.page_hash: a match pattern watches what a script holds, and fails loud when lost."""

    PAGE = ('<html><head><script>var versionArr = [[\'C63A-20_{v}.html\',\'Current Version\']];\n'
            'var versionDefault="C63A-20_{v}";</script></head><body>{banner} Chapter 20</body></html>')
    MATCH = r'var versionArr = \[.*?\];|var versionDefault="[^"]*"'

    def h(self, body, match=None):
        from unittest import mock
        with mock.patch.object(detect, "fetch_page", return_value=body):
            return detect.page_hash("https://example.test/", match)

    def test_visible_text_hash_misses_a_script_only_change(self):
        a = self.PAGE.format(v="2026", banner="")
        b = self.PAGE.format(v="2027", banner="")
        self.assertEqual(self.h(a), self.h(b))

    def test_match_sees_the_version_change_and_ignores_the_banner(self):
        a = self.PAGE.format(v="2026", banner="")
        self.assertNotEqual(self.h(a, self.MATCH), self.h(self.PAGE.format(v="2027", banner=""), self.MATCH))
        self.assertEqual(self.h(a, self.MATCH), self.h(self.PAGE.format(v="2026", banner="Playback down today"), self.MATCH))

    def test_match_that_finds_nothing_is_an_error(self):
        with self.assertRaises(detect.SourceError):
            self.h("<html>redesigned</html>", self.MATCH)


class IssueState(unittest.TestCase):
    def items(self, updated):
        return [{"repo": "o/r", "number": 12, "updated_at": updated, "primary": True}]

    def test_unchanged_thread_is_not_changed_on_the_next_run(self):
        first = self.items("2026-10-14T01:00:00Z")
        seen = detect.mark_changed(first, {})
        self.assertTrue(first[0]["changed"])
        again = self.items("2026-10-14T01:00:00Z")
        detect.mark_changed(again, seen)
        self.assertFalse(again[0]["changed"])

    def test_new_comment_makes_it_changed_again(self):
        seen = detect.mark_changed(self.items("2026-10-14T01:00:00Z"), {})
        later = self.items("2026-11-02T09:00:00Z")
        detect.mark_changed(later, seen)
        self.assertTrue(later[0]["changed"])


class ReportItems(unittest.TestCase):
    def test_primary_item_past_the_cap_is_still_shown(self):
        items = [{"number": i, "primary": False} for i in range(45)] + [{"number": 99, "primary": True}]
        shown = detect.shown_items(items)
        self.assertEqual(shown[0]["number"], 99)
        self.assertEqual(shown[-1], 6)              # 45 others, 39 shown beside the one primary
        self.assertEqual(len([x for x in shown if isinstance(x, dict)]), 40)

    def test_every_primary_shown_even_beyond_the_cap(self):
        items = [{"number": i, "primary": True} for i in range(50)] + [{"number": 100, "primary": False}]
        shown = detect.shown_items(items)
        self.assertEqual(len([x for x in shown if isinstance(x, dict) and x["primary"]]), 50)
        self.assertEqual(shown[-1], 1)

    def test_rendered_report_lists_a_late_primary_thread(self):
        items = [{"number": i, "title": "t", "url": f"u{i}", "author": "a", "updated": "2026-10-14", "primary": False} for i in range(40)]
        items.append({"number": 777, "title": "ruling", "url": "u777", "author": "a", "updated": "2026-10-14", "primary": True})
        r = {"generated": "2026-10-15T00:00:00", "check": ["monthly"], "previous_run": None, "errors": [],
             "sources": [{"id": "x", "kind": "gh-issues", "material": True, "feeds": [], "chapters": [], "items": items}],
             "freshness": {"status": "error", "detail": ""}}
        self.assertIn("#777", detect.render(r))


class Checks(unittest.TestCase):
    """detect.selected_checks: monthly always, quarterly in the quarter months, --check overrides."""

    def pick(self, month, check=None):
        from datetime import datetime
        from types import SimpleNamespace
        return detect.selected_checks(SimpleNamespace(check=check), datetime(2026, month, 1))

    def test_default_by_month(self):
        self.assertEqual(self.pick(2), {"monthly"})
        self.assertEqual(self.pick(10), {"monthly", "quarterly"})

    def test_override_and_rejects_unknown(self):
        self.assertEqual(self.pick(2, "quarterly"), {"quarterly"})
        with self.assertRaises(SystemExit):
            self.pick(2, "hot")


class Manifest(unittest.TestCase):
    """Every source in refresh/sources.yaml is a kind detect.py handles, with the keys it reads."""

    def test_every_source_is_readable_by_detect(self):
        import yaml
        m = yaml.safe_load((ROOT / "refresh" / "sources.yaml").read_text())
        ids = [s["id"] for s in m["sources"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate source ids")
        need = {"git": {"path", "remote", "branches"}, "gh-repo": {"repo", "branches"},
                "gh-discussions": {"repo", "since"}, "gh-prs": {"repo", "since"},
                "gh-issues": {"since"}, "web": {"urls"}}
        for s in m["sources"]:
            self.assertIn(s["kind"], need, s["id"])
            self.assertIn(s.get("check"), detect.CHECKS, s["id"])
            self.assertEqual(need[s["kind"]] - set(s), set(), s["id"])
            if s["kind"] == "gh-issues":
                self.assertTrue(s.get("repo") or s.get("repos"), s["id"])


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

    def test_early_sources_heading_does_not_end_the_body(self):
        for early in ("##  Sources {#early}", "~~~\n## Sources {#q}\n~~~", "<!--\n## Sources {#q}\n-->", "```\n```python\n## Sources {#q}\n```"):
            long = self.CHAPTER.replace("## Sources", early + "\n\n" + ("word " * 7600) + "\n\n## Sources")
            self.assertTrue(any("length" in p for p in self.published(long)), early)

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
