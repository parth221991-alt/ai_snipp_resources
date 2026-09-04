# 🏛️ SEBI AI Compliance Framework & Audit Toolkit (2026 FinTech Edition)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![AI_SNIPP](https://img.shields.io/badge/Curated%20by-AI__SNIPP-cyan.svg)](https://instagram.com/ai_snipp)
[![Compliance: SEBI AI/ML Ready](https://img.shields.io/badge/Compliance-SEBI%20AI%2FML%20Ready-emerald.svg)](#)

The definitive technical compliance blueprint, audit checklist, and automated code scanner for Indian FinTech founders, algorithmic traders, quantitative developers, and AI engineers building financial tools in India.

> **Featured on AI_SNIPP Reel #068:** *"SEBI Just Issued New AI Guidelines in India — Here is how to keep your financial AI tools 100% compliant."*

---

## 📌 Executive Overview

The Securities and Exchange Board of India (**SEBI**) has intensified regulatory oversight over Artificial Intelligence (AI) and Machine Learning (ML) tools operating within the Indian capital markets.

Whether you run an algorithmic trading system, an automated research newsletter, a robo-advisor, or a custom GPT for stock analysis, **black-box automation without registered human accountability is no longer permitted**.

This repository provides:
1. The **4 Non-Negotiable Regulatory Pillars**.
2. The **8-Point SEBI AI Compliance Checklist** (`SEBI-AI-01` to `SEBI-AI-08`).
3. An **Automated Codebase Compliance Scanner** (`sebi_compliance_checker.py`).
4. A standard **Model Disclosure & Algorithmic Inventory Template** (`model_disclosure_template.json`).
5. Copy-pasteable **Statutory Risk Disclaimers** conforming to SEBI regulations.

---

## ⚖️ The 4 Non-Negotiable Regulatory Pillars

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     THE 4 SEBI REGULATORY PILLARS                       │
├──────────────────────────┬──────────────────────────────────────────────┤
│ 1. Algorithmic           │ Full disclosure of models, parameters, and   │
│    Accountability        │ underlying architecture. No "black-box"      │
│                          │ defense is legally admissible.               │
├──────────────────────────┼──────────────────────────────────────────────┤
│ 2. Human-in-the-Loop     │ 100% legal liability rests on the registered │
│    (HITL) Gate           │ entity/advisor. Autonomous unsolicited trade │
│                          │ dispatch to retail users is strictly barred. │
├──────────────────────────┼──────────────────────────────────────────────┤
│ 3. Data Privacy &        │ Zero leakage of Indian investor PII into     │
│    Sovereignty           │ public LLM training sets. DPDP Act and SEBI  │
│                          │ cybersecurity framework compliance.          │
├──────────────────────────┼──────────────────────────────────────────────┤
│ 4. Prohibition of        │ Zero guarantees of returns, claims of 100%   │
│    Deceptive Marketing   │ accuracy, or un-vetted broker API loops.     │
│                          │ Prominent statutory disclaimers mandatory.   │
└──────────────────────────┴──────────────────────────────────────────────┘
```

---

## 📋 The 8-Point SEBI AI Compliance Checklist

| Code | Audit Check | Regulatory Standard | Required Implementation |
|---|---|---|---|
| **SEBI-AI-01** | **Model Inventory & Registry** | All AI/ML models in production must be formally documented with versioning, architecture, and deployment date. | Maintain `model_disclosure.json` in your repository root with active model IDs, training cutoff dates, and model weights origin. |
| **SEBI-AI-02** | **Strict Human-in-the-Loop Gate** | Registered intermediaries (Research Analysts / Investment Advisers) remain personally responsible for any AI-generated research or recommendation. | Code-level gate (`require_approval == True`) that prevents auto-publishing research or auto-routing orders without an authenticated operator sign-off. |
| **SEBI-AI-03** | **Indian PII Sanitization** | Investor identity data (PAN, Aadhaar, Demat numbers, phone numbers) must NEVER be sent to public third-party LLM APIs. | Client-side Regex + NER scrubbing before forwarding any context to OpenAI, Anthropic, or external providers. |
| **SEBI-AI-04** | **Immutable Audit Trail** | Regulators may audit algorithmic decisions retrospectively during inspection. | Append-only hash-chained logs storing prompt inputs, model completion outputs, timestamps, and the approving compliance officer ID. |
| **SEBI-AI-05** | **Statutory Risk Disclaimers** | Every screen, PDF report, or bot message conveying market research must display standard risk warnings. | Prominent inclusion of: *"Investments in securities market are subject to market risks. Read all related documents carefully before investing."* |
| **SEBI-AI-06** | **Deterministic Guardrails** | Unbounded generative outputs ("hallucinations") in financial recommendations must be programmatically blocked. | Use structured output libraries (Pydantic / Instructor) with strict validation schemas. Free-form text generation without bounded limits is non-compliant. |
| **SEBI-AI-07** | **Emergency Kill Switch** | Algorithmic execution systems must possess an automated circuit-breaker for aberrant market conditions or API anomalies. | Real-time drawdown halts, max-slippage gates, and one-click manual liquidation controls across broker sessions. |
| **SEBI-AI-08** | **No Guaranteed Return Claims** | Prohibiting any language implying risk-free profits, guaranteed daily returns, or infallible win rates. | Automated marketing scanner blocking terms like *"Guaranteed 5% daily"*, *"100% Win Rate"*, or *"Zero Risk"*. |

---

## 🏗️ Compliant Architecture Blueprint

Here is the reference architecture for building a SEBI-compliant FinTech AI pipeline:

```
                  ┌─────────────────────────────────────┐
                  │          Investor / User UI         │
                  └──────────────────┬──────────────────┘
                                     │ Query / Request
                                     ▼
                  ┌─────────────────────────────────────┐
                  │       PII & Secret Sanitizer        │
                  │   (Regex Scrub: PAN, Aadhaar, PII)  │
                  └──────────────────┬──────────────────┘
                                     │ Clean Context Only
                                     ▼
                  ┌─────────────────────────────────────┐
                  │       AI Inference Engine           │
                  │ (Local vLLM / Enterprise Zero-Log)  │
                  └──────────────────┬──────────────────┘
                                     │ Raw Output
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      Deterministic Guardrail Gate   │
                  │ (Pydantic Schema + Risk Multipliers)│
                  └──────────────────┬──────────────────┘
                                     │ Structured Signal
                                     ▼
                  ┌─────────────────────────────────────┐
                  │  👑 MANDATORY HUMAN-IN-THE-LOOP     │
                  │   (Licensed RA/RIA Sign-off Portal) │
                  └──────────────────┬──────────────────┘
                                     │ Approved & Signed
                                     ▼
       ┌─────────────────────────────┴─────────────────────────────┐
       │                                                           │
       ▼                                                           ▼
┌───────────────────────────┐                         ┌───────────────────────────┐
│     User Notification     │                         │   Immutable Audit Log     │
│  (+ Statutory Disclaimer) │                         │ (Hash-Chained S3 / JSONL) │
└───────────────────────────┘                         └───────────────────────────┘
```

---

## 🚀 Quick Start: Running the Automated Compliance Checker

We have included an automated scanner `sebi_compliance_checker.py` that verifies your codebase against the key SEBI tenets.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Audit on Your Codebase
```bash
python sebi_compliance_checker.py --target .
```

### 3. Sample Terminal Audit Output
```text
=======================================================
🏛️  SEBI FINANCIAL AI COMPLIANCE CHECKER — 2026 EDITION
Target Directory: D:\FinTech_Project
=======================================================

-------------------------------------------------------
OVERALL SEBI COMPLIANCE SCORE: 100% (PASSED_COMPLIANT)
-------------------------------------------------------

[PASS] SEBI-AI-01: Model Inventory & Algorithmic Disclosure (25/25 pts)
       • Model disclosure registered: Found valid model_disclosure.json
[PASS] SEBI-AI-02: PII Protection & Hardcoded Secret Sanitation (20/20 pts)
       • Zero hardcoded broker credentials or real Indian PANs detected in source code.
[PASS] SEBI-AI-03: Human-in-the-Loop (HITL) Gate & Advisor Liability (20/20 pts)
       • Human approval gate verified in execution logic / documentation.
[PASS] SEBI-AI-04: Mandatory Statutory Risk Disclaimers (20/20 pts)
       • Statutory risk disclaimers verified across project interfaces.
[PASS] SEBI-AI-05: Immutable Decision & Prompt Audit Logging (15/15 pts)
       • Structured event and prompt audit logging detected.

📄 Saved full audit report to: D:\FinTech_Project\sebi_audit_report.json
```

---

## 📑 Model Inventory Template (`model_disclosure_template.json`)

To satisfy SEBI algorithmic inspections, maintain a standard `model_disclosure.json` in your repository. Copy our pre-built template:

```bash
cp model_disclosure_template.json model_disclosure.json
```

Key fields required:
- `registration_type`: `RESEARCH_ANALYST` or `INVESTMENT_ADVISER`
- `sebi_registration_number`: Intermediary license ID
- `model_id` & `underlying_architecture`: Specification of the ML model
- `input_features`: Market data feeds ingested
- `human_in_the_loop`: Explicit definition of the approval gate
- `risk_boundaries`: Max drawdown limits and circuit-breaker triggers

---

## ⚖️ Standard Statutory Risk Disclaimer Templates

### For UI Footers & Telegram / WhatsApp Bots:
> *"Investments in securities market are subject to market risks. Read all the related documents carefully before investing. Registration granted by SEBI and certification from NISM in no way guarantee performance of the intermediary or provide any assurance of returns to investors."*

### For Algorithmic Research Outputs & PDFs:
> *"Disclaimer: All content and algorithmic signals provided herein are generated for market research and analytical purposes only. Past performance is no guarantee of future returns. The intermediary shall not be liable for any direct or indirect trading losses resulting from automated market data or analysis."*

---

## 📄 License & Attribution

Distributed under the **MIT License**. Free for FinTech startups, research desks, and independent developers.

*Curated with precision by [@ai_snipp](https://instagram.com/ai_snipp). Follow for daily production AI engineering blueprints.*
