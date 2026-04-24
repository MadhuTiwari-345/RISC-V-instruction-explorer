#!/usr/bin/env python3
"""
RISC-V Instruction Set Explorer
================================
Mentorship Coding Challenge — All Three Tiers

Usage:
    python explorer.py --all
    python explorer.py --tier1
    python explorer.py --tier2
    python explorer.py --tier3
    python explorer.py --all --output results.txt
"""

import json, re, sys, os, argparse, subprocess, tempfile, shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# ── Constants ──────────────────────────────────────────────────────────────────

INSTR_DICT_URL = (
    "https://raw.githubusercontent.com/rpsene/"
    "riscv-extensions-landscape/main/instr_dict.json"
)
MANUAL_REPO_URL = "https://github.com/riscv/riscv-isa-manual"

# Stop-words that appear capitalised in AsciiDoc but are NOT extension names
ADOC_STOP_WORDS: Set[str] = {
    "The","This","These","That","Those","A","An","In","Is","It","If","As","At",
    "Be","By","Do","For","From","Has","Have","He","Her","His","How","I","My",
    "No","Not","Of","On","Or","Our","Out","So","To","Up","Was","We","Will",
    "With","You","All","Are","But","Can","Its","New","One","See","Set","Use",
    "When","Which","Who","Why","Your","NOTE","WARNING","TIP","CAUTION",
    "IMPORTANT","ISA","ABI","CPU","ALU","CSR","PC","SP","GPR","FPR","RISC",
    "MISA","HART","XLEN","FLEN","VLEN","ELEN","MXLEN","Table","Figure",
    "Section","Chapter","Appendix","Example","Register","Registers",
    "Instruction","Instructions","Extension","Extensions","Privilege",
    "Unprivileged","Volume","Version","Number","Name","Value","Type","Mode",
    "True","False","None","List","File","Description","RV32","RV64","RV128",
    "WARL","WLRL","SBI","ELF","MEM","BIT","RISC-V",
}


# ── Shared utilities ───────────────────────────────────────────────────────────

def norm_json_ext(tag: str) -> str:
    """Strip rv_, rv32_, rv64_ … prefixes; lowercase.
    e.g.  rv_zba -> zba,  rv32_i -> i,  rv64_zknd -> zknd
    """
    return re.sub(r"^rv\d*_", "", tag.lower())


def norm_manual_ext(token: str) -> str:
    """Lowercase a manual-side token for comparison."""
    return token.lower()


def load_json(source: str) -> dict:
    """Load JSON from a URL or local path."""
    import urllib.request
    if source.startswith("http://") or source.startswith("https://"):
        with urllib.request.urlopen(source, timeout=20) as r:
            return json.loads(r.read().decode())
    with open(source, encoding="utf-8") as f:
        return json.load(f)


def _extract_extensions(entry) -> List[str]:
    """
    Robustly extract extension tags from one instruction entry.

    Handles every shape observed in the wild:
      { "extension": ["rv_i", ...], ... }
      { "extension": "rv_i" }
      ["rv_i", ...]
      "rv_i"
      {}   -> []
    """
    if isinstance(entry, dict):
        raw = entry.get("extension", entry.get("extensions", []))
    elif isinstance(entry, list):
        raw = entry
    elif isinstance(entry, str):
        raw = [entry]
    else:
        return []

    if not isinstance(raw, list):
        raw = [raw]

    result: List[str] = []
    def _flat(x):
        if isinstance(x, list):
            for item in x: _flat(item)
        elif x:
            result.append(str(x).lower().strip())
    _flat(raw)
    return result


def _out(lines: List[str], msg: str):
    print(msg)
    lines.append(msg)


# ══════════════════════════════════════════════════════════════════════════════
# TIER 1 — Instruction Set Parsing
# ══════════════════════════════════════════════════════════════════════════════

def parse_instructions(data: dict) -> Tuple[Dict[str, List[str]], List[dict]]:
    """
    Group instructions by extension tag.

    Returns
    -------
    grouped   : { ext_tag: [MNEMONIC, ...] }  (mnemonics sorted)
    multi_ext : [{ mnemonic, exts }, ...]       (cross-listed instructions)
    """
    grouped: Dict[str, List[str]] = defaultdict(list)
    multi_ext = []

    for mnemonic, entry in data.items():
        M = mnemonic.upper()
        exts = _extract_extensions(entry)

        if not exts:
            grouped["_unknown"].append(M)
            continue

        for ext in exts:
            grouped[ext].append(M)

        if len(exts) > 1:
            multi_ext.append({"mnemonic": M, "exts": exts})

    # Sort for determinism
    for arr in grouped.values():
        arr.sort()
    sorted_grouped = dict(sorted(grouped.items()))
    multi_ext.sort(key=lambda x: x["mnemonic"])

    return sorted_grouped, multi_ext


def run_tier1(source: str, out_lines: List[str]) -> Tuple[Optional[dict], Optional[list]]:
    """Execute Tier 1 and print results."""
    sep = "─" * 62

    _out(out_lines, f"\n{sep}")
    _out(out_lines, "  TIER 1 — Instruction Set Parsing")
    _out(out_lines, sep)
    _out(out_lines, f"  Source: {source}")

    try:
        _out(out_lines, "  Fetching instr_dict.json …")
        data = load_json(source)
        _out(out_lines, f"  Loaded {len(data)} instruction entries.")
    except Exception as exc:
        _out(out_lines, f"  ERROR: {exc}")
        return None, None

    grouped, multi_ext = parse_instructions(data)

    # ── Summary table ──────────────────────────────────────────────
    _out(out_lines, "")
    col_w = max((len(k) for k in grouped), default=12)
    hdr = f"  {'EXTENSION TAG':<{col_w}}  |  COUNT  |  EXAMPLE MNEMONIC"
    _out(out_lines, hdr)
    _out(out_lines, "  " + "─" * (len(hdr) - 2))

    for ext, mnems in grouped.items():
        ex = mnems[0] if mnems else "—"
        _out(out_lines, f"  {ext:<{col_w}}  |  {len(mnems):>5}  |  e.g. {ex}")

    total = sum(len(v) for v in grouped.values())
    _out(out_lines, "  " + "─" * (len(hdr) - 2))
    _out(out_lines, f"  {'TOTAL':<{col_w}}  |  {total:>5}  |")

    # ── Cross-listed instructions ──────────────────────────────────
    _out(out_lines, f"\n  Instructions belonging to multiple extensions ({len(multi_ext)}):")
    if multi_ext:
        _out(out_lines, "  " + "─" * 52)
        for item in multi_ext:
            tags = ", ".join(item["exts"])
            _out(out_lines, f"  {item['mnemonic']:<20}  →  {tags}")
    else:
        _out(out_lines, "  None found.")

    _out(out_lines, f"\n  Extensions: {len(grouped)}  |  Total entries: {total}  |  Cross-listed: {len(multi_ext)}")
    return grouped, multi_ext


# ══════════════════════════════════════════════════════════════════════════════
# TIER 2 — Cross-Reference with ISA Manual
# ══════════════════════════════════════════════════════════════════════════════

def _scan_adoc(text: str) -> Set[str]:
    """Extract candidate extension names from one AsciiDoc file."""
    found: Set[str] = set()
    for m in re.finditer(r"\b([A-Z][a-zA-Z0-9]{0,35})\b", text):
        tok = m.group(1)
        if tok not in ADOC_STOP_WORDS:
            found.add(tok.lower())
    return found


def _get_manual_exts(repo_url: str, out_lines: List[str]) -> Set[str]:
    """Clone (or reuse) the ISA manual repo and scan its AsciiDoc files."""
    git = shutil.which("git")
    if not git:
        _out(out_lines, "  WARNING: git not found — using seed extension list only.")
        return set()

    cache = Path(tempfile.gettempdir()) / "riscv_isa_manual_cache"

    if (cache / ".git").exists():
        _out(out_lines, f"  Reusing cached clone at {cache}")
        subprocess.run([git, "pull", "--quiet"], cwd=cache,
                       capture_output=True, check=False)
    else:
        _out(out_lines, f"  Cloning {repo_url} …")
        result = subprocess.run(
            [git, "clone", "--depth=1", "--quiet", repo_url, str(cache)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            _out(out_lines, f"  ERROR cloning: {result.stderr.strip()}")
            return set()
        _out(out_lines, "  Clone complete.")

    src_dir = cache / "src"
    if not src_dir.exists():
        src_dir = cache

    adoc_files = list(src_dir.rglob("*.adoc"))
    _out(out_lines, f"  Found {len(adoc_files)} AsciiDoc files.")

    tokens: Set[str] = set()
    for path in adoc_files:
        try:
            tokens |= _scan_adoc(path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass

    _out(out_lines, f"  Extracted {len(tokens)} unique candidate tokens.")
    return tokens


def cross_reference(
    grouped: dict,
    manual_tokens: Set[str],
    out_lines: List[str],
) -> Tuple[Set[str], Set[str], Set[str]]:
    """Compare normalised extension sets; return (matched, json_only, manual_only)."""
    json_norm: Dict[str, str] = {norm_json_ext(k): k for k in grouped}

    matched    = {n for n in json_norm if n in manual_tokens}
    json_only  = {n for n in json_norm if n not in manual_tokens}
    manual_only = {t for t in manual_tokens if t not in json_norm}

    # ── Print results ──────────────────────────────────────────────
    _out(out_lines, f"\n  Count summary: {len(matched)} matched, "
         f"{len(json_only)} in JSON only, {len(manual_only)} in manual only")

    _out(out_lines, f"\n  Matched in both ({len(matched)}):")
    for n in sorted(matched):
        _out(out_lines, f"    {json_norm[n]:<25}  ↔  {n}")

    if json_only:
        _out(out_lines, f"\n  In JSON but NOT in manual ({len(json_only)}):")
        for n in sorted(json_only):
            _out(out_lines, f"    {json_norm[n]}")

    if manual_only:
        preview = sorted(manual_only)[:40]
        _out(out_lines, f"\n  In manual but NOT in JSON ({len(manual_only)}, first 40):")
        for n in preview:
            _out(out_lines, f"    {n}")
        if len(manual_only) > 40:
            _out(out_lines, f"    … and {len(manual_only) - 40} more")

    return matched, json_only, manual_only


def run_tier2(grouped: dict, repo_url: str, out_lines: List[str]):
    """Execute Tier 2 and print results."""
    sep = "─" * 62
    _out(out_lines, f"\n{sep}")
    _out(out_lines, "  TIER 2 — Cross-Reference with ISA Manual")
    _out(out_lines, sep)

    manual_tokens = _get_manual_exts(repo_url, out_lines)
    cross_reference(grouped, manual_tokens, out_lines)


# ══════════════════════════════════════════════════════════════════════════════
# TIER 3 — Graph (text-based)
# ══════════════════════════════════════════════════════════════════════════════

def build_sharing_graph(grouped: dict):
    """Build adjacency map: ext → {neighbour_ext: [shared_mnemonics]}."""
    mnem_to_exts: Dict[str, Set[str]] = defaultdict(set)
    for ext, mnems in grouped.items():
        for m in mnems:
            mnem_to_exts[m].add(ext)

    adj: Dict[str, Dict[str, List[str]]] = {e: {} for e in grouped}

    for mnem, exts in mnem_to_exts.items():
        exts_l = sorted(exts)
        for i in range(len(exts_l)):
            for j in range(i + 1, len(exts_l)):
                a, b = exts_l[i], exts_l[j]
                adj[a].setdefault(b, []).append(mnem)
                adj[b].setdefault(a, []).append(mnem)

    return adj


def run_tier3_graph(grouped: dict, out_lines: List[str]):
    """Print text-based extension sharing graph."""
    sep = "─" * 62
    _out(out_lines, f"\n{sep}")
    _out(out_lines, "  TIER 3 — Extension Sharing Graph")
    _out(out_lines, sep)

    adj = build_sharing_graph(grouped)
    edges_seen = set()
    edges = []
    for a, neighbours in adj.items():
        for b, mnems in neighbours.items():
            key = tuple(sorted([a, b]))
            if key not in edges_seen:
                edges_seen.add(key)
                edges.append((a, b, mnems))

    edges.sort(key=lambda e: -len(e[2]))

    _out(out_lines, f"  Nodes: {len(adj)}  |  Edges: {len(edges)}")
    _out(out_lines, "")
    _out(out_lines, "  Extension Sharing Edges (sorted by shared count):")
    _out(out_lines, "  " + "─" * 56)
    for a, b, mnems in edges:
        shared = ", ".join(sorted(mnems))
        _out(out_lines, f"  {a:<20}  ──[{len(mnems)}]──  {b}")
        _out(out_lines, f"    shared: {shared}")

    isolated = [e for e, nb in adj.items() if not nb]
    if isolated:
        _out(out_lines, f"\n  Isolated nodes (no shared instructions): {len(isolated)}")
        _out(out_lines, "  " + ", ".join(sorted(isolated)))


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="RISC-V Instruction Set Explorer — Mentorship Challenge",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--all",   action="store_true")
    parser.add_argument("--tier1", action="store_true")
    parser.add_argument("--tier2", action="store_true")
    parser.add_argument("--tier3", action="store_true")
    parser.add_argument("--json-url", default=INSTR_DICT_URL,
                        help="URL or local path to instr_dict.json")
    parser.add_argument("--manual-repo", default=MANUAL_REPO_URL)
    parser.add_argument("--output", default=None,
                        help="Save combined output to this file")
    args = parser.parse_args()

    if not any([args.all, args.tier1, args.tier2, args.tier3]):
        parser.print_help(); sys.exit(1)

    t1 = args.all or args.tier1
    t2 = args.all or args.tier2
    t3 = args.all or args.tier3

    out_lines: List[str] = []
    _out(out_lines, "=" * 62)
    _out(out_lines, "  RISC-V Instruction Set Explorer")
    _out(out_lines, "=" * 62)

    grouped = None
    if t1 or t2 or t3:
        grouped, multi_ext = run_tier1(args.json_url, out_lines)

    if t2 and grouped:
        run_tier2(grouped, args.manual_repo, out_lines)

    if t3 and grouped:
        run_tier3_graph(grouped, out_lines)

    _out(out_lines, "\n" + "=" * 62)

    if args.output:
        Path(args.output).write_text("\n".join(out_lines), encoding="utf-8")
        print(f"\n[Saved to {args.output}]")


if __name__ == "__main__":
    main()
