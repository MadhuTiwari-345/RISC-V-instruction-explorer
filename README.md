
## 🚀 Project Banner

<p align="center">
  <img src="https://github.com/user-attachments/assets/3a3415aa-fc5f-4e29-83a8-a42021269292" width="900"/>
</p>


# 🚀 RISC-V Instruction Set Explorer

<p align="center">
  <i>A zero-setup RISC-V analysis tool that parses, validates, and visualizes ISA structure—revealing hidden relationships across extensions.</i>
</p>


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/HTML5-5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-Browser-yellow?style=for-the-badge&logo=javascript"/>
  <img src="https://img.shields.io/badge/Tests-38%20Passing-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge"/>
</p>

---

## 🖼️ Preview 

<p align="center">
  <img src="https://github.com/user-attachments/assets/91418903-8974-44e1-98d9-cf7c2c3e3d68" width="48%"/>
  <img src="https://github.com/user-attachments/assets/686b0ffe-c10a-40a6-aff6-9748900ef14d" width="48%"/>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7411705b-df15-4880-a45f-e7a5b0984f88" width="48%"/>
  <img src="https://github.com/user-attachments/assets/00987db2-cafd-4a9e-a87e-448e21e44362" width="48%"/>
</p>

---

## 🎯 Overview

A **complete 3-tier implementation** that transforms raw RISC-V instruction data into:

- 🔍 Structured extension groups  
- 🔗 ISA cross-references  
- 🧪 Verified outputs via unit tests  
- 📊 Interactive graph visualizations  

---

## ✨ Why This Stands Out

- ⚡ **Zero-setup browser execution (offline)**
- 🧠 **Smart normalization across inconsistent naming**
- 🔬 **Cross-validation with official ISA manual**
- 📈 **Graph-based insight into extension relationships**
- 🧪 **Test-backed correctness (38 tests)**

---

## 🧰 Implementations

| File | Language | Network |
|------|----------|--------|
| `riscv-explorer.html` | JavaScript | ❌ Offline |
| `src/explorer.py` | Python | ✅ Required |

---

## ⚡ Quick Start

### 🌐 Browser (Recommended)

```bash
start riscv-explorer.html
````

👉 👉 Click **▶ RUN ALL TIERS** to execute all three tiers instantly
---

### 🐍 Python CLI

```bash
python src/explorer.py --all
```

Run specific tiers:

```bash
python src/explorer.py --tier1
python src/explorer.py --tier2
python src/explorer.py --tier3
```

Run tests:

```bash
python -m unittest tests/test_explorer.py -v
```

---

## 📊 Core Features

### 🧩 Tier 1 — Instruction Parsing

* Parses 245+ instructions
* Groups by extension
* Detects overlaps

### 🔗 Tier 2 — Cross-Reference

* Matches against ISA manual
* Normalizes naming differences
* Identifies mismatches

### 📈 Tier 3 — Graph Analysis

* Extension relationships
* Shared instruction mapping
* Interactive visualization

---

## 📊 Sample Output 

### 🧩 Tier 1 — Instruction Parsing

- ✅ **245 instructions processed**
- 📦 **262 total extension mappings**
- 🔁 **17 multi-extension overlaps detected**

**Top Extensions:**

rv_i   → 40 instructions  
rv_d   → 28 instructions  
rv_c   → 26 instructions  
rv_f   → 26 instructions  

**Multi-Extension Examples:**

ADD.UW   → rv_zba, rv64_zba  
AES64DS  → rv64_zknd, rv64_zkne  
ANDN     → rv_zbb, rv_zbkb  

---

### 🔗 Tier 2 — ISA Cross-Reference

- 📄 **42 ISA files scanned**
- 🔍 **847 candidate tokens extracted**

**Results:**
- ✅ Matched: **23**
- ❌ JSON-only: **0**
- ⚠️ Manual-only: **63** (expected noise)

**Example Matches:**

rv_a   ↔ a  
rv_c   ↔ c  
rv_zba ↔ zba  

---

### 📈 Tier 3 — Graph Analysis

**Top Relationships (by shared instructions):**

rv_zbb  ──[5]── rv_zbkb  
rv_zbc  ──[2]── rv_zbkc  
rv_zba  ──[1]── rv64_zba  

---

## 🧠 Visualization Output

The browser version renders a **live interactive graph**:

- 🔵 Node size → instruction count  
- 🔗 Edge weight → shared instructions  
- 🎨 Color → extension family  
- 🖱 Hover → full instruction list  

---

## 🧠 Key Insights

### 🔹 1. Core ISA dominates instruction distribution

The base integer extension (`rv_i`) contains the highest number of instructions (~40), confirming its role as the foundational layer of the RISC-V architecture.

👉 Insight:
Most other extensions build on top of this core, reinforcing a **modular ISA design philosophy**.

---

### 🔹 2. Significant overlap between specialized extensions

Multiple instructions belong to more than one extension (e.g., `ANDN`, `CLMUL`, `AES64DS`).

👉 Insight:
RISC-V extensions are **not strictly isolated**—they share functionality, especially in:

* Bit manipulation (`rv_zb*`)
* Cryptography (`rv_zk*`)

This suggests **intentional reuse and composability**, not duplication.

---

### 🔹 3. Strong clustering in bit-manipulation extensions

Extensions like:

* `rv_zbb`
* `rv_zbkb`
* `rv_zbc`

show the highest number of shared instructions.

👉 Insight:
Bit-manipulation extensions form a **tightly coupled cluster**, indicating:

* High internal cohesion
* Designed to be used together

---

### 🔹 4. Clean JSON coverage vs ISA manual mismatch

* ✅ JSON-only extensions: **0**
* ⚠️ Manual-only tokens: **63**

👉 Insight:
The instruction dictionary is **complete and consistent**, while the ISA manual introduces:

* Extra tokens (e.g., section names, abbreviations)
* Expected parsing noise

This validates the **reliability of structured JSON over raw documentation parsing**.

---

### 🔹 5. Graph structure reveals extension relationships

The force-directed graph highlights:

* Dense clusters (bitmanip group)
* Sparse links (specialized extensions like `rv_zba` ↔ `rv64_zba`)

👉 Insight:
RISC-V follows a **hybrid structure**:

* Dense clusters → general-purpose extensions
* Sparse edges → niche or architecture-specific features

---

### 🔹 6. Design favors scalability over rigidity

Normalization required:

* Removing prefixes (`rv32_`, `rv64_`)
* Case harmonization

👉 Insight:
RISC-V naming conventions are **flexible but inconsistent**, reinforcing the need for:

* Programmatic normalization
* Rule-based parsing instead of hardcoding

---

## 🎯 Final Takeaway

RISC-V’s design emphasizes:

* 🧩 **Modularity** — extensions build on a strong base
* 🔗 **Interoperability** — shared instructions across domains
* 📈 **Scalability** — easy to extend without breaking structure

This project transforms raw instruction data into **actionable architectural insights about the RISC-V ecosystem**.

---

## 📁 Project Structure

```
RISC-V-instruction-explorer/
├── README.md
├── riscv-explorer.html
├── src/
├── tests/
├── output/
```

---

## ⚙️ Key Design Decisions

### 🔹 Normalization Strategy

* Regex-based (`^rv\d*_`)
* Lowercase transformation
* No hardcoding → future-proof

---

### 🔹 Offline Browser Mode

* Embedded dataset
* No CORS issues
* Instant execution

---

### 🔹 Efficient Graph Model

* Adjacency dictionary
* Fast lookups
* Easy visualization

---

## 📌 Assumptions

* Flexible JSON schema supported
* Missing extensions → `_unknown`
* Manual parsing may include noise (expected)

---

## 📌 Key Result

- ✔ 0 missing extensions in JSON dataset  
- ✔ 23 validated ISA matches  
- ✔ 17 cross-extension overlaps identified  

👉 Confirms both **data completeness** and **structural interconnectivity**

---

## 🧾 Conclusion

This project demonstrates that **RISC-V’s instruction set is not merely a collection of isolated extensions, but a deeply interconnected and modular architecture**.

Through systematic parsing, normalization, and cross-referencing, several structural characteristics emerge:

* The **base ISA (`rv_i`) acts as a stable foundation**, with higher-level extensions layering functionality rather than redefining it
* **Extension boundaries are intentionally porous**, enabling instruction reuse across domains such as bit manipulation and cryptography
* The observed **clustered graph topology** reflects design intent—dense regions correspond to general-purpose capability groups, while sparse connections highlight specialized features

From a data perspective, the contrast between structured JSON and unstructured ISA documentation reinforces a key observation:

> **machine-readable specifications enable far more reliable analysis than textual standards alone**

The necessity of normalization further indicates that **RISC-V prioritizes extensibility over strict naming uniformity**, a trade-off that favors long-term scalability at the cost of tooling complexity.

---

### 🎯 Broader Implication

The findings suggest that RISC-V is best understood not as a fixed ISA, but as an **evolving ecosystem of interoperable instruction subsets**.

This has direct implications for:

* **Compiler design** → optimization across overlapping extensions
* **Hardware implementation** → selective inclusion of tightly coupled instruction groups
* **Tooling & analysis** → need for abstraction layers over raw specification formats

---

### 🔍 Final Perspective

By combining parsing, validation, and visualization, this work transforms static instruction data into a **dynamic representation of architectural intent**.

> Ultimately, this project highlights how even low-level ISA data, when properly structured and analyzed, can reveal **higher-order design principles** underlying modern computing architectures.

---

