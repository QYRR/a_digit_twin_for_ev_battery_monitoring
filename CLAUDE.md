# CLAUDE.md — A Digital Twin for EV Battery Monitoring

## Project Overview

Master's thesis (Laurea Magistrale) in Computer Engineering at Politecnico di Torino.

**Title:** A Digital Twin for EV Battery Monitoring
**Candidate:** Chao Song
**Supervisors:** Prof. Sara Vinco, Prof. Massimo Poncino

### Research Topic
Edge-based machine learning for real-time SoC (State of Charge) and SoH (State of Health) estimation in EV batteries. The thesis proposes:
1. A lightweight ML model deployed on an MCU for on-board inference
2. An OTA update system to periodically refresh the model as the battery degrades

### Key Technical Domains
- Battery management systems (BMS), SoC/SoH estimation
- Machine learning (neural networks, regression)
- Edge computing / embedded systems (MCU deployment)
- Digital twin concepts

---

## LaTeX Build System

**Engine:** pdflatex (see thesis.tex line 2: `% !TEX TS-program = pdflatex`)
**Document class:** `toptesi` (Politecnico di Torino official thesis class)
**Bibliography:** biblatex + biber, source: `bibliography.bib`

### How to Compile

```bash
pdflatex thesis.tex
biber thesis
pdflatex thesis.tex
pdflatex thesis.tex
```

Or with latexmk (recommended for auto-reruns):
```bash
latexmk -pdf thesis.tex
```

### File Structure

```
thesis.tex              ← Main document. Do NOT reorder \input statements
common/
  thesis_info.tex       ← Candidate name, title, supervisors, date
  packages.tex          ← \usepackage declarations
  package_config.tex    ← Package settings
  new_commands.tex      ← Custom LaTeX macros
  config.tex            ← General config
  font_config.tex       ← Font settings
  toptesi_config.tex    ← toptesi class configuration
  frontpage.tex         ← Custom title page
  post_summary_config.tex ← Config applied after frontmatter
content/
  chapters.tex          ← Lists all chapter \input statements in order
  summary.tex           ← Italian summary (sommario)
  abstract.tex          ← Abstract (optional)
  acknowledgements.tex  ← Ringraziamenti
  appendix.tex          ← Appendix content
  chapters/
    introduction.tex    ← Ch1: Introduction (motivation, problem, aims, outline)
    background.tex      ← Ch2: Background / literature review
    methodology.tex     ← Ch3: Methodology (ML model, OTA system)
    experiment.tex      ← Ch4: Experiments and results
    conclusion.tex      ← Ch5: Conclusion
    chapter0.tex        ← DEMO/TEMPLATE — not a real chapter, keep for reference
images/                 ← All figures (PNG, SVG, EPS)
bibliography.bib        ← BibTeX references
glossaries.tex          ← Acronyms and glossary entries
```

---

## Agent Workflow (Two-Agent Pipeline)

This project uses two specialized agents that work in series:

1. **Writer Agent** — Writes chapter content in LaTeX
2. **Humanizer Agent** — Reduces AI-detection rate by rewriting prose naturally

### Workflow: Chapter by Chapter

```
Writer Agent → writes chapter_N.tex (draft)
     ↓
Humanizer Agent → rewrites prose only, preserves LaTeX/equations/citations
     ↓
Writer Agent → reviews humanized output for technical accuracy
```

### Critical Rules for BOTH Agents

**DO NOT change:**
- `thesis.tex` (main structure)
- Any file in `common/` (unless explicitly asked)
- `content/chapters.tex` (chapter list)
- LaTeX commands, labels, `\ref`, `\cite`, `\autocite`
- Equations, tables, figures, algorithms
- Bibliography keys and citation format

**DO change:**
- Prose/paragraph text within `content/chapters/*.tex`
- Chapter structure (sections, subsections) — if it improves flow

### Writing Guidelines

- **Language:** English (British spelling acceptable)
- **Tone:** Academic but not overly formal. Clear, direct, precise.
- **Citation style:** `\autocite{key}` for standard citations
- **Figures:** Always include `\label{fig:...}` and descriptive `\caption{}` with source attribution via `\autocite{}`
- **Equations:** Numbered with `\label{eq:...}`, explain all variables
- **Cross-references:** Use `\autoref{label}` or `\ref{label}`
- **Notes to self:** Use LaTeX `\begin{comment}...\end{comment}` blocks (not visible in PDF)

---

## Current State

- Introduction (Ch1): ~80% complete, Contributions section empty
- Background (Ch2): Empty template
- Methodology (Ch3): Empty template
- Experiment (Ch4): Empty template
- Conclusion (Ch5): Empty template
- chapter0.tex: LaTeX format example/demo — NOT for editing
