# SHT — Self-Surprise Conformal Framework for LLM Hallucination Analysis

> 📄 **Public preview.** This repository accompanies a paper currently being submitted to NLPCC 2026 (Springer LNCS). The full implementation, manifests, decision logs, and experimental artifacts are maintained in a private repository pending peer review.
>
> If you are a researcher, recruiter, or hiring manager who would like deeper access (full code, reproducibility manifests, internal decision logs) **prior** to public release, please reach out — see [Contact](#contact).

[![Status](https://img.shields.io/badge/status-submission%20ready-brightgreen.svg)](#status)
[![Paper](https://img.shields.io/badge/paper-NLPCC%202026%20(submission)-b31b1b.svg)](#)
[![Preview](https://img.shields.io/badge/repo-public%20preview-orange.svg)](#)

---

## 🔍 What this project is

Existing LLM hallucination detectors are largely **batch-mode** — they require completing a generation, sampling multiple alternatives, or running post-hoc retrieval before a decision is made. **SHT** is a sequential, *anytime-valid* framework: it issues a decision as early as sample-efficient evidence allows, with rigorous statistical false-alarm guarantees that hold **at any stopping time**.

The framework cleanly separates three layers of guarantees, each with its own assumption set and its own evaluation methodology — a structural choice that, to the authors' knowledge, has not been made explicit in prior LLM hallucination work.

<p align="center">
  <img src="figures/method_overview_lite.png" width="780" alt="SHT three-layer architecture (overview)"/>
</p>

| Layer | Role | Guarantee type |
|---|---|---|
| Layer 1 — Token | Anytime-valid monitor on the realised sampling distribution | Provable (Ville-derived martingale; Theorem 13) |
| Layer 2 — Claim/Trace | Per-category split-conformal calibration | Provable (finite-sample; Theorem 14) |
| Layer 3 — Empirical | Bridging the token-level signal to claim-level labels | Empirical (AUROC + per-prompt miscoverage) |

This separation matters because it lets us be **honest about what is, and isn't, mathematically proven**. Existing methods often conflate "alarm fires" with "hallucination detected"; we make the gap explicit and quantify it as a joint characterization of (anytime-valid status × calibration-target choice).

## 🎯 Why anytime-valid matters

Most LLM hallucination work uses tests that are valid **only at a pre-specified sample size** — running them at multiple time points without correction inflates Type-I error. SHT instead uses [e-processes](https://arxiv.org/abs/2410.23614) and [test martingales](https://www.sciencedirect.com/science/article/pii/S0167715211002148), which permit **continuous monitoring**: the analyst can peek at the test statistic after every token without sacrificing the false-alarm guarantee. This matches the autoregressive nature of LLM generation in a way that batch-mode methods cannot.

## 🛠️ Technical stack

- **Theoretical machinery**: e-processes, test martingales, Ville's inequality, split conformal prediction, proper scoring rules (centered Brier), Bregman divergences
- **Score function**: centered Brier residual $s_t = \|q_t\|_2^2 - q_t(X_t) \in [-1, 1]$, mean-zero under the sampling identity
- **Implementation**: Python · PyTorch · HuggingFace Transformers · NumPy · PyArrow · scipy / sklearn
- **Target model**: Qwen2.5-7B-Instruct (deterministic custom decoding loop)
- **Comparison baselines**: NLL surprisal aggregators (mean / max / std), q_t entropy aggregators, CUSUM

## 📊 Status

| Component | Status |
|---|---|
| Layer 1 framework & theory (Theorem 13) | ✅ Complete |
| Layer 2 framework & theory (Theorem 14, trace-level per-category) | ✅ Complete |
| Token-level generation pipeline (Qwen2.5-7B, 25 prompts × 5 seeds) | ✅ Complete (125 traces) |
| Multi-LLM atomic-claim annotation | ✅ Complete (1026 claims, 3 annotators, 667 unanimous) |
| Phase D primary run (Stage 4 batch) | ✅ Complete (Gate 1 evaluated) |
| Sensitivity run (C1/C2 majority merge) | ✅ Complete (Stage 5) |
| Path B streaming infrastructure | ✅ Complete (Stage 6, 8 modules + driver) |
| Gate 3 peeking-FAR three-arm experiment | ✅ Complete (Stage 8) |
| Stage 9 paper finalization | ✅ Complete (post-Stage-10 sign-off) |
| NLPCC 2026 submission | 🚧 In preparation |

The paper is post-Stage-10 sign-off (2026-05-21) and ready for NLPCC submission upload.

## 🔒 Why this repo is a preview

The paper is under submission preparation; the full implementation includes calibration artifacts and decision logs that we preserve in a private repository to maintain submission priority and to protect the dataset construction methodology. This is standard practice for in-progress research.

**What's in this preview:**
- Paper LaTeX source (`paper/SHT_v8_paper.tex`)
- Bibliography (`paper/references.bib`)
- High-level architectural overview (this README)
- Empirical status snapshot

**What's in the full (private) repo:**
- Complete source code for Phase D (Layer 3 AUROC) and Path B (streaming three-arm peeking-FAR)
- Theorem proofs (Theorems 13/14 and Lemma 7) with full algebra
- Frozen experiment manifests with SHA256 anchors (pre-registration discipline)
- Annotated claim corpus and per-token feature parquet
- 15+ decision logs from 10 stages + 14 rounds of internal hostile-review
- v2 candidate redesign notes

## 🚦 Roadmap

```
Now (2026-05) ──┐
                ├── NLPCC 2026 submission upload
                │
                ├── Review period (June–August 2026, NLPCC schedule)
                │     ↳ This preview repo remains
                │
                ├── Decision
                │     ↳ If accepted: full code + camera-ready
                │     ↳ If rejected: incorporate reviewer feedback, retarget
                │
                └── v2 redesign work (parallel): Channel-U-dominant benchmark,
                    score function dual-design for Channel O, larger sample budget
```

## 📧 Contact

**Jie Yuan** (袁捷)
Kean University · Department of Mathematical Sciences
📩 [yuanjie@kean.edu](mailto:yuanjie@kean.edu)

If you would like access to the private full repository for **collaboration, recruiting, or referee review** purposes, please email with a brief note about your role and intended use.

---

<sub>*This README intentionally omits some technical details (proof internals, dataset construction specifics, internal decision logs) that constitute the contribution of the in-review paper. They will be released here in full once the paper is public.*</sub>
