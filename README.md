# RISC-V Instruction Set Explorer

> RISC-V Mentorship Coding Challenge — All Three Tiers

A complete solution that parses the RISC-V instruction dictionary, cross-references it against the official ISA manual, runs a full unit-test suite, and renders an interactive force-directed extension-sharing graph.

Two implementations are provided:

| File | Language | Requires network? |
|------|----------|-------------------|
| `riscv-explorer.html` | JavaScript (browser) | No — data embedded |
| `src/explorer.py` | Python 3.8+ | Yes (Tier 1 & 2 fetch from GitHub) |

---

## Quick Start — Browser (recommended for submission demo)

```bash
# Just open the file — no server, no install, no network needed
open riscv-explorer.html          # macOS
xdg-open riscv-explorer.html      # Linux
start riscv-explorer.html         # Windows
```

Click **▶ RUN ALL TIERS** and all three tiers execute instantly.

---

## Quick Start — Python CLI

### Requirements

- Python 3.8+
- `git` (for Tier 2 — clones the ISA manual repo)
- No third-party packages required

### Run all tiers

```bash
python src/explorer.py --all
```

### Run individual tiers

```bash
python src/explorer.py --tier1
python src/explorer.py --tier2
python src/explorer.py --tier3
```

### Save output to file

```bash
python src/explorer.py --all --output output/results.txt
```

### Use a local instr_dict.json

```bash
python src/explorer.py --all --json-url /path/to/instr_dict.json
```

### Run unit tests

```bash
python -m unittest tests/test_explorer.py -v
```

---

## Sample Output

### Tier 1

```
──────────────────────────────────────────────────────────────
  TIER 1 — Instruction Set Parsing
──────────────────────────────────────────────────────────────
  Source: https://raw.githubusercontent.com/...
  Loaded 245 instruction entries.

  EXTENSION TAG         |  COUNT  |  EXAMPLE MNEMONIC
  ──────────────────────────────────────────────────
  rv_a                  |     11  |  e.g. AMOADD.W
  rv_c                  |     26  |  e.g. C.ADD
  rv_d                  |     28  |  e.g. FADD.D
  rv_f                  |     26  |  e.g. FADD.S
  rv_i                  |     40  |  e.g. ADD
  rv_m                  |      8  |  e.g. DIV
  rv_zba                |      4  |  e.g. SH1ADD
  ...
  TOTAL                 |    262  |

  Instructions belonging to multiple extensions (17):
  ────────────────────────────────────────────────────
  ADD.UW                →  rv_zba, rv64_zba
  AES64DS               →  rv64_zknd, rv64_zkne
  ANDN                  →  rv_zbb, rv_zbkb
  CLMUL                 →  rv_zbc, rv_zbkc
  MUL                   →  rv_m, rv_zmmul
  ...
```

### Tier 2

```
──────────────────────────────────────────────────────────────
  TIER 2 — Cross-Reference with ISA Manual
──────────────────────────────────────────────────────────────
  Cloning riscv-isa-manual …
  Found 42 AsciiDoc files.
  Extracted 847 unique candidate tokens.

  Count summary: 23 matched, 0 in JSON only, 63 in manual only

  Matched in both (23):
    rv_a                       ↔  a
    rv_c                       ↔  c
    rv_zba                     ↔  zba
    ...

  In manual but NOT in JSON (63, first 40):
    e  g  h  n  q  smstateen  svinval  svnapot  ...
```

### Tier 3 — Graph (text)

```
  Extension Sharing Edges (sorted by shared count):
  ────────────────────────────────────────────────
  rv_zbb                ──[5]──  rv_zbkb
    shared: ANDN, ORN, ROL, ROR, XNOR
  rv_zbc                ──[2]──  rv_zbkc
    shared: CLMUL, CLMULH
  rv_zba                ──[1]──  rv64_zba
    shared: ADD.UW
  ...
```

The browser version renders a live **force-directed canvas graph** where:
- Node size = instruction count
- Edge weight = number of shared instructions
- Colour = extension family (base/FP/bitmanip/crypto/vector)
- Hover = tooltip with instruction list

---

## Project Structure

```
riscv-submission/
├── riscv-explorer.html     # Self-contained browser app (all 3 tiers)
├── src/
│   └── explorer.py         # Python CLI (all 3 tiers)
├── tests/
│   └── test_explorer.py    # 38 unit tests
├── output/
│   └── sample_output.txt   # Sample run output
└── README.md
```

---

## Design Decisions

### Extension name normalisation (Tier 2)
The two sources use different naming conventions:

| Source | Example | Normalised |
|--------|---------|------------|
| `instr_dict.json` | `rv_zba`, `rv32_zknd` | strip `rv\d*_` → `zba`, `zknd` |
| ISA manual AsciiDoc | `Zba`, `M`, `Zicsr` | lowercase → `zba`, `m`, `zicsr` |

A single regex `^rv\d*_` handles all observed JSON prefix variants. Both sides are then lowercased for comparison. No hard-coded mapping table — the rule-based approach handles new extensions automatically.

### AsciiDoc scanning strategy
The scanner uses a broad capitalised-token regex (`\b[A-Z][a-zA-Z0-9]{0,35}\b`) and filters against a curated stop-word list. This means **"manual only"** will always contain false positives (section titles, abbreviations like `WARL`). The meaningful metrics are **matched** and **JSON only** — both are clean.

### No network in the browser version
Browser sandboxes block cross-origin `fetch()` to GitHub. Rather than fight CORS proxies, the HTML file embeds 245 real instructions as a JS literal — instant load, works offline, zero errors.

### Cached git clone (Python Tier 2)
`git clone --depth=1` on first run; `git pull` on repeat runs. Stored in the system temp directory so the working directory stays clean and re-runs take under a second.

### Graph representation
Adjacency dict `{ ext → { neighbour → [shared_mnemonics] } }` gives O(1) lookup and trivial serialisation. The browser renders a Fruchterman-Reingold force simulation on `<canvas>`.

---

## Assumptions

1. `instr_dict.json` values may be a dict, list, or string — the parser handles all three.
2. Entries with no extension tag go into a `_unknown` bucket rather than being silently dropped.
3. The ISA manual `src/` directory contains the authoritative AsciiDoc sources. If absent, the whole repo root is scanned.
4. "Manual only" tokens include English words that slip through the stop-word filter — this is expected and documented.
