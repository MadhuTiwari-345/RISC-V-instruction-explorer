
# 🚀 RISC-V Instruction Set Explorer

<p align="center">
  <b>Deep Dive into RISC-V ISA — Parsing • Validation • Visualization</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/JavaScript-Browser-yellow?style=for-the-badge&logo=javascript"/>
  <img src="https://img.shields.io/badge/Tests-38%20Passing-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge"/>
</p>

---

## 🎯 Overview

A **complete 3-tier implementation** that transforms raw RISC-V instruction data into:

- 🔍 Structured extension groups  
- 🔗 ISA cross-references  
- 🧪 Verified outputs via unit tests  
- 📊 Interactive graph visualizations  

---

## 🖼️ Preview 

<p align="center">
  <img src="<img width="883" height="574" alt="{92C3A3A7-C3BD-40ED-B32C-FF3BF5D4D118}" src="https://github.com/user-attachments/assets/91418903-8974-44e1-98d9-cf7c2c3e3d68" />
" width="800"/>
</p>

<p align="center">
  <img src="<img width="854" height="574" alt="{9FB51AED-B59C-4FE9-9061-672C2C2ABC51}" src="https://github.com/user-attachments/assets/686b0ffe-c10a-40a6-aff6-9748900ef14d" />
" width="800"/>
</p>

<p align="center">
  <img src="<img width="854" height="575" alt="{85F0B19A-D647-4CC3-B334-E69460745ABB}" src="https://github.com/user-attachments/assets/7411705b-df15-4880-a45f-e7a5b0984f88" />
" width="800"/>
</p>

<p align="center">
  <img src="<img width="810" height="480" alt="graph" src="https://github.com/user-attachments/assets/00987db2-cafd-4a9e-a87e-448e21e44362" />
" width="800"/>
</p>
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

👉 Click **▶ RUN ALL TIERS**

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

## 🧠 Visualization

* Node size → instruction count
* Edge weight → shared instructions
* Color → extension family
* Hover → instruction details

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

## 🏁 Final Thoughts

This project focuses on:

✔ Accuracy
✔ Scalability
✔ Clarity of insights

while staying lightweight and easy to run.

---

