# IanETrading — System Request
**Date:** 2025-10-05  
**Project Title:** IanETrading (Smart-Money-Following Automated Trading)  
**Methodology:** Unified Process (Iterative & Incremental)  
**Execution Environment:** Google Colab + GitHub Actions (with Secrets for API management)

---

## 1 · Project Overview
**Summary**  
IanETrading is an automated trading system that detects retail-driven overheated market behavior (e.g., Robinhood popularity, unusual volume spikes) and follows *Smart Money* trends by executing short or hedge trades.  
The system will be designed as a **modular (plug-in) architecture**, allowing additional trading strategies to be attached later and enabling future expansion into a **trading-as-a-service** platform.  
*(Service commercialization is an additional long-term goal, not part of the initial scope.)*

---

## 2 · Project Sponsor
| Role | Name | Contact | Responsibility |
|------|------|----------|----------------|
| Sponsor / Product Owner | Hamin Hong | (hhamin93@gmail.com / https://github.com/IanEAbba) | Defines requirements, prioritizes tasks, approves deliverables, oversees operations |

---

## 3 · Business Need
- **Supplemental Income:** Automate various stock trading strategies to generate steady side profit.  
- **Professional Value:** Build a full-stack, data-driven automation workflow using Python and GitHub Actions for real-world engineering experience.  
- **Extensibility:** Support multiple strategy plug-ins for faster iteration and diversified risk; establish clear module boundaries for future service-level growth.

---

## 4 · High-Level Business Requirements
| ID | Requirement (What) | Type | Priority |
|----|---------------------|-------|-----------|
| BR-01 | Build a data-collection pipeline for retail-popularity and sentiment metrics | Functional | High |
| BR-02 | Detect overheating and generate Smart-Money short/hedge signals | Functional | High |
| BR-03 | Execute orders through the Alpaca Paper Trading API and track positions | Functional | High |
| BR-04 | Implement a modular plug-in framework for strategy attachment / A/B testing | Non-Functional (Extensibility) | High |
| BR-05 | Provide Colab notebooks for backtesting, analytics, and visualization | Functional | Medium |
| BR-06 | Schedule automatic runs and log archival via GitHub Actions | Functional | Medium |
| BR-07 | Securely manage API keys using GitHub Secrets | Non-Functional (Security) | High |
| BR-08 | Enable future expansion toward trading services (reporting, copy-trade, etc.) | Non-Functional (Extensibility) | Medium (additional goal) |

---

## 5 · Business Value
**Quantitative Examples**
- Reduce manual monitoring / execution time by > 70 %.  
- Improve volatility-period performance once validated by backtesting.

**Qualitative**
- Gain end-to-end experience in data, automation, and deployment workflows.  
- Accumulate reusable documentation, pipelines, and automation assets for future service transition.
- take out human-related feelings / in the trading that lead to unwise dicisions(ex. panic sell)
  
---

## 6 · Feasibility Analysis
| Category | Description | Risk |
|-----------|--------------|------|
| **Technical** | Python, Colab, Alpaca Paper, and GitHub Actions are stable and well documented; plug-in design allows easy strategy expansion. | Low |
| **Economic** | Zero direct cost – free tiers of Colab / GitHub Actions / Alpaca Paper. | Low |
| **Organizational** | Solo development and operation; managed via GitHub Issues and Milestones; careful scope control required. | Medium |

**Main Risks & Mitigations**
- **Data quality or availability:** standardize adapter interface; maintain backup sources.  
- **Over-fitting:** out-of-sample (OOS) validation and walk-forward testing; favor simple parameter sets first.  
- **API latency or failures:** implement retry logic and separate order-sync job.  
- **Security:** use GitHub Secrets only; never store keys in plaintext or logs.

---

## 7 · Scope
**In Scope (v1)**
- Retail-trend data collector (min one adapter)  
- Smart-Money strategy module + short/hedge execution via Alpaca Paper  
- Plug-in architecture v1 with strategy enable/disable interface  
- Colab backtesting notebook and GitHub Actions scheduler with log archiving  

**Out of Scope (initially excluded / future consideration)**
- Live trading with real accounts or leverage products  
- Paid data feeds or high-frequency execution  
- External user services (billing, legal compliance, KYC flows)

---

## 8 · Constraints & Assumptions
| Type | Description |
|------|--------------|
| **Constraints** | Must operate entirely on free resources (Colab / Actions), not optimized for ultra-low-latency execution, must respect API rate limits. |
| **Assumptions** | Alpaca Paper API accessible and stable; at least one retail-trend data source available; daily or twice-daily scheduling is sufficient. |

---

## 9 · Success Criteria / KPIs
**Technical**
- Scheduled runs succeed ≥ 99 % per month; retry logic verified.  
- Strategy plug-ins and parameter switches function without code changes (via configuration).

**Analytical**
- OOS backtests show loss reduction or improved market-neutral metrics vs. baseline volatility.

**Documentation / Operations**
- Complete SDLC artifacts in `docs/` (requirements, diagrams, test plans).  
- Automatic log archival and reproducible Colab notebooks.

---

## 10 · High-Level Timeline (≈ 8 – 10 weeks)
| Phase | Deliverables | Duration (weeks) |
|-------|---------------|------------------|
| Planning | System Request + Feasibility Analysis | 1 |
| Analysis | Detailed Requirements, Use Cases, Activity Diagrams | 2 |
| Design | Plug-in interface, class and component diagrams | 2 |
| Implementation | Core modules, Colab notebooks, GitHub Actions scheduler | 3 – 4 |
| Testing / Validation | Unit / Integration / OOS tests + docs | 1 – 2 |

**Milestones**
- **M1:** Data adapter + base strategy + E2E paper trade success  
- **M2:** Plug-in framework and second strategy PoC  
- **M3:** Automated schedule + log archival  
- **M4:** Verified OOS performance and documentation complete

---

## 11 · Approval
| Role | Name | Date | Signature |
|------|------|------|------------|
| Project Owner | Hamin Hong | 2025-10-05 | (electronic signature) |
