#!/usr/bin/env python3
"""
Unit tests for the RISC-V Instruction Set Explorer.
Run:  python -m unittest tests/test_explorer.py -v
"""

import sys, json, os, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from explorer import (
    _extract_extensions,
    parse_instructions,
    norm_json_ext,
    norm_manual_ext,
    _scan_adoc,
    cross_reference,
    build_sharing_graph,
)


# ── Helpers ────────────────────────────────────────────────────────────────────

NOOP: list = []   # silent output sink


# ══════════════════════════════════════════════════════════════════════════════
# _extract_extensions
# ══════════════════════════════════════════════════════════════════════════════

class TestExtractExtensions(unittest.TestCase):

    def test_dict_with_extension_list(self):
        r = _extract_extensions({"extension": ["rv_i", "rv_zba"]})
        self.assertIn("rv_i", r); self.assertIn("rv_zba", r)

    def test_dict_with_extension_string(self):
        r = _extract_extensions({"extension": "rv_m"})
        self.assertEqual(r, ["rv_m"])

    def test_dict_with_extensions_key(self):
        r = _extract_extensions({"extensions": ["rv_f"]})
        self.assertIn("rv_f", r)

    def test_flat_list(self):
        self.assertEqual(_extract_extensions(["rv_f", "rv_d"]), ["rv_f", "rv_d"])

    def test_string_value(self):
        self.assertEqual(_extract_extensions("rv_m"), ["rv_m"])

    def test_empty_dict(self):
        self.assertEqual(_extract_extensions({}), [])

    def test_none(self):
        self.assertEqual(_extract_extensions(None), [])

    def test_lowercase_normalisation(self):
        r = _extract_extensions(["RV_ZBA", "RV_I"])
        self.assertTrue(all(e == e.lower() for e in r))

    def test_nested_list(self):
        r = _extract_extensions([["rv_i", "rv_m"]])
        self.assertIn("rv_i", r); self.assertIn("rv_m", r)


# ══════════════════════════════════════════════════════════════════════════════
# parse_instructions
# ══════════════════════════════════════════════════════════════════════════════

class TestParseInstructions(unittest.TestCase):

    def _data(self):
        return {
            "add":   {"extension": ["rv_i"]},
            "sub":   {"extension": ["rv_i"]},
            "mul":   {"extension": ["rv_m"]},
            "add.uw":{"extension": ["rv_zba", "rv64_zba"]},
            "custom":{},
        }

    def test_groups_by_extension(self):
        g, _ = parse_instructions(self._data())
        self.assertIn("rv_i", g); self.assertIn("rv_m", g)

    def test_instruction_counts(self):
        g, _ = parse_instructions(self._data())
        self.assertEqual(len(g["rv_i"]), 2)
        self.assertEqual(len(g["rv_m"]), 1)

    def test_mnemonics_uppercased(self):
        g, _ = parse_instructions(self._data())
        for mnems in g.values():
            self.assertTrue(all(m == m.upper() for m in mnems))

    def test_mnemonics_sorted(self):
        g, _ = parse_instructions(self._data())
        for mnems in g.values():
            self.assertEqual(mnems, sorted(mnems))

    def test_cross_listed_detected(self):
        _, multi = parse_instructions(self._data())
        names = {x["mnemonic"] for x in multi}
        self.assertIn("ADD.UW", names)

    def test_unknown_bucket(self):
        g, _ = parse_instructions(self._data())
        self.assertIn("_unknown", g)
        self.assertIn("CUSTOM", g["_unknown"])

    def test_empty_input(self):
        g, m = parse_instructions({})
        self.assertEqual(g, {})
        self.assertEqual(m, [])


# ══════════════════════════════════════════════════════════════════════════════
# Normalisation
# ══════════════════════════════════════════════════════════════════════════════

class TestNormalisation(unittest.TestCase):

    def test_strip_rv_prefix(self):
        self.assertEqual(norm_json_ext("rv_zba"), "zba")

    def test_strip_rv32_prefix(self):
        self.assertEqual(norm_json_ext("rv32_i"), "i")

    def test_strip_rv64_prefix(self):
        self.assertEqual(norm_json_ext("rv64_zknd"), "zknd")

    def test_already_clean(self):
        self.assertEqual(norm_json_ext("zba"), "zba")

    def test_lowercases(self):
        self.assertEqual(norm_json_ext("RV_ZBA"), "zba")

    def test_manual_lowercase(self):
        self.assertEqual(norm_manual_ext("Zba"), "zba")
        self.assertEqual(norm_manual_ext("M"), "m")


# ══════════════════════════════════════════════════════════════════════════════
# AsciiDoc scanner
# ══════════════════════════════════════════════════════════════════════════════

class TestScanAdoc(unittest.TestCase):

    def test_finds_extension_names(self):
        text = "The Zba extension defines SH1ADD. See also Zicsr and M."
        f = _scan_adoc(text)
        self.assertIn("zba", f); self.assertIn("zicsr", f); self.assertIn("m", f)

    def test_filters_stop_words(self):
        text = "The ISA Extensions manual describes Instructions."
        f = _scan_adoc(text)
        self.assertNotIn("the", f)
        self.assertNotIn("extensions", f)
        self.assertNotIn("instructions", f)

    def test_independent_calls(self):
        a = _scan_adoc("Zba Zbb")
        b = _scan_adoc("Zbc Zbd")
        self.assertIn("zba", a); self.assertIn("zbc", b)

    def test_empty_text(self):
        self.assertEqual(_scan_adoc(""), set())


# ══════════════════════════════════════════════════════════════════════════════
# Cross-reference
# ══════════════════════════════════════════════════════════════════════════════

class TestCrossReference(unittest.TestCase):

    def test_matched(self):
        grouped = {"rv_zba": ["SH1ADD"], "rv_i": ["ADD"]}
        manual  = {"zba", "i", "f"}
        m, jo, mo = cross_reference(grouped, manual, NOOP)
        self.assertIn("zba", m); self.assertIn("i", m)

    def test_json_only(self):
        grouped = {"rv_ztso": ["FENCE.TSO"]}
        manual  = {"zba"}
        _, jo, _ = cross_reference(grouped, manual, NOOP)
        self.assertIn("ztso", jo)

    def test_manual_only(self):
        grouped = {"rv_zba": ["SH1ADD"]}
        manual  = {"zba", "smstateen"}
        _, _, mo = cross_reference(grouped, manual, NOOP)
        self.assertIn("smstateen", mo)

    def test_empty(self):
        m, jo, mo = cross_reference({}, set(), NOOP)
        self.assertEqual(len(m), 0)
        self.assertEqual(len(jo), 0)
        self.assertEqual(len(mo), 0)


# ══════════════════════════════════════════════════════════════════════════════
# Graph
# ══════════════════════════════════════════════════════════════════════════════

class TestBuildSharingGraph(unittest.TestCase):

    def _grouped(self):
        return {
            "rv_i":  ["ADD", "SUB"],
            "rv_m":  ["MUL", "ADD"],   # ADD shared
            "rv_f":  ["FADD"],          # isolated
        }

    def test_shared_edge_exists(self):
        adj = build_sharing_graph(self._grouped())
        self.assertIn("rv_m", adj["rv_i"])

    def test_symmetric(self):
        adj = build_sharing_graph(self._grouped())
        self.assertIn("rv_i", adj["rv_m"])

    def test_isolated_no_neighbours(self):
        adj = build_sharing_graph(self._grouped())
        self.assertEqual(adj["rv_f"], {})

    def test_edge_label(self):
        adj = build_sharing_graph(self._grouped())
        self.assertIn("ADD", adj["rv_i"]["rv_m"])

    def test_no_self_loops(self):
        adj = build_sharing_graph(self._grouped())
        for ext, nb in adj.items():
            self.assertNotIn(ext, nb)

    def test_empty(self):
        adj = build_sharing_graph({})
        self.assertEqual(adj, {})


# ══════════════════════════════════════════════════════════════════════════════
# Integration
# ══════════════════════════════════════════════════════════════════════════════

class TestEndToEnd(unittest.TestCase):

    SAMPLE = {
        "add":    {"extension": ["rv_i"]},
        "sub":    {"extension": ["rv_i"]},
        "mul":    {"extension": ["rv_m"]},
        "mulh":   {"extension": ["rv_m", "rv_zmmul"]},
        "sh1add": {"extension": ["rv_zba"]},
    }

    def test_tier1_pipeline(self):
        grouped, multi = parse_instructions(self.SAMPLE)
        self.assertEqual(len(grouped["rv_i"]), 2)
        self.assertEqual(grouped["rv_m"], ["MUL", "MULH"])
        self.assertEqual(len(multi), 1)
        self.assertEqual(multi[0]["mnemonic"], "MULH")

    def test_tier1_to_graph_consistency(self):
        grouped, multi = parse_instructions(self.SAMPLE)
        adj = build_sharing_graph(grouped)
        # mulh is in both rv_m and rv_zmmul → edge must exist
        self.assertIn("rv_zmmul", adj["rv_m"])
        # multi_ext matches graph edge
        for item in multi:
            exts = item["exts"]
            for i in range(len(exts)):
                for j in range(i + 1, len(exts)):
                    a, b = exts[i], exts[j]
                    self.assertIn(b, adj.get(a, {}),
                                  f"Expected edge {a}--{b}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
