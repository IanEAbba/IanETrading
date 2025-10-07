# IanETrading — Requirements Definition

## 1. Purpose
Define the functional scope of IanETrading (Smart Money tracking, modular strategy system, paper trading).

## 2. Functional Requirements
| ID | Requirement | Priority |
|----|--------------|----------|
| F1 | Collect retail sentiment data (e.g., Robinhood API) | High |
| F2 | Identify divergence between retail and institutional signals | High |
| F3 | Generate short/hedge trade signals | High |
| F4 | Execute trades via Alpaca Paper API | High |
| F5 | Log trade results and performance data | Medium |
| F6 | Run automatically on schedule (GitHub Actions) | Medium |
| F7 | Add modular plug-in support for new strategies | High |

## 3. Non-Functional Requirements
| ID | Requirement | Priority |
|----|--------------|----------|
| NF1 | Secure API key storage via GitHub Secrets | High |
| NF2 | Maintain modular, testable code structure | Medium |
| NF3 | Scalable for new data sources | Medium |
| NF4 | Readable Colab notebooks for visualization | Medium |

## 4. Main Use Case
**Name:** Detect Retail Overbuy → Trigger Short Signal  
**Actor:** Scheduler (GitHub Action)  
**Trigger:** Scheduled run  
**Main Flow:**
1. Fetch retail sentiment data  
2. Analyze for overbought conditions  
3. Generate short signals  
4. Execute orders through Alpaca Paper  
5. Log results to GitHub repo  

**Alternative Flow:**  
API error → retry and log failure  

## 5. Activity Diagram
!(images/Flowchart.png "flowchart")