## 📘 IanETrading Project Plan (Updated for Colab + GitHub Actions)

### 🧩 1️⃣ Planning 단계

#### 📄 System Request

* **Why (목표):**
  리테일 투자자의 매수 집중(예: Robinhood 인기 종목)을 탐지하여, 과열된 종목에 숏 포지션을 자동으로 생성하는 시스템.

* **Value (가치):**

  * 실제 시장 심리를 분석하는 자동화 알고리즘 설계 연습
  * GitHub Actions 및 Colab을 이용한 **클라우드 없는 자동화 인프라 실습**
  * Python 백엔드, 백테스팅, 시각화 등 풀스택 개발 프로세스 경험

* **Key Features (핵심 기능):**

  1. Robinhood 또는 유사한 공개 소스에서 인기 종목 데이터 수집
  2. 급등 신호 감지 및 숏 시그널 생성
  3. Alpaca Paper Trading API를 통한 가상 거래
  4. Colab에서 백테스트 및 시각화 수행
  5. GitHub Actions로 자동화된 시그널 검증 실행

* **Estimated Duration:**
  약 8~10주
  (기획 1주 / 분석 2주 / 설계 2주 / 구현 3주 / 테스트 1~2주)

#### 📊 Feasibility Analysis

| 구분          | 설명                                                       | 리스크 수준 |
| ----------- | -------------------------------------------------------- | ------ |
| **기술적 타당성** | Python, Colab, Alpaca API, GitHub Actions 모두 무료 및 접근 용이. | Low    |
| **경제적 타당성** | 비용 없음 (Colab + GitHub 무료, Alpaca Paper Mode 무료).         | Low    |
| **조직적 타당성** | 1인 개발 프로젝트, GitHub issue와 milestone으로 관리.                | Medium |

---

### 🧠 2️⃣ Analysis 단계

#### Functional Requirements (기능 요구사항)

| ID | 설명                                  | 우선순위   |
| -- | ----------------------------------- | ------ |
| F1 | Robinhood API/공개 데이터에서 종목 인기 데이터 수집 | High   |
| F2 | 특정 기준(예: 급등률, 거래량 등)으로 과열 종목 감지     | High   |
| F3 | 숏 신호 생성 및 Alpaca API로 주문 요청         | High   |
| F4 | Colab에서 시뮬레이션/백테스트 수행               | Medium |
| F5 | 로그 및 결과를 GitHub에 자동 커밋              | Medium |
| F6 | GitHub Actions로 매일 자동 실행            | Medium |

#### Non-Functional Requirements (비기능 요구사항)

| ID  | 설명                            | 우선순위   |
| --- | ----------------------------- | ------ |
| NF1 | GitHub Secrets로 API Key 보안 관리 | High   |
| NF2 | Colab에서 외부 API 연결이 원활해야 함     | Medium |
| NF3 | 코드 재사용성을 위한 모듈 구조 유지          | Medium |
| NF4 | 로그 및 결과의 시각적 해석 가능성           | Medium |

#### 주요 Use Case

**Use Case 1: Detect Retail Overbuy → Trigger Short Signal**

| 항목               | 내용                               |
| ---------------- | -------------------------------- |
| **Actor**        | System Scheduler (GitHub Action) |
| **Trigger**      | Colab 또는 GitHub Action이 매일 실행될 때 |
| **Precondition** | Alpaca 및 Robinhood API Key 등록 완료 |
| **Main Flow**    |                                  |

1. Robinhood 인기 데이터 수집
2. 특정 조건으로 과열 종목 탐지
3. 숏 시그널 생성
4. Alpaca Paper Account로 주문 전송
5. 거래 결과 로그를 GitHub에 커밋 |
   | **Alternative Flow** | API 응답 오류 시 로그 저장 후 재시도 |
   | **Postcondition** | 숏 주문 성공 및 결과 기록 저장 |

#### Activity Diagram (간략 예시)

```
Start
  ↓
[Fetch Robinhood Data]
  ↓
[Detect Overbuy]
  ↓
[Generate Short Signal]
  ↓
[Execute Alpaca Trade]
  ↓
[Log & Commit to GitHub]
  ↓
End
```

---

### ⚙️ 3️⃣ Design 단계

#### CRC Cards 예시 (for “ShortSignalManager”)

| **Class**            | **Responsibilities**     | **Collaborators**              |
| -------------------- | ------------------------ | ------------------------------ |
| `ShortSignalManager` | 감지된 종목에 대한 숏 시그널 생성 및 검증 | `DataFetcher`, `TradeExecutor` |
| `DataFetcher`        | Robinhood 데이터 수집         | `ShortSignalManager`           |
| `TradeExecutor`      | Alpaca API 호출            | `ShortSignalManager`           |

#### Class Diagram 초안

```
DataFetcher --> ShortSignalManager --> TradeExecutor
```

* `DataFetcher`: `fetch_robinhood_trends()`
* `ShortSignalManager`: `detect_overbuy()`, `create_signal()`
* `TradeExecutor`: `execute_short_order()`

---

### 🧪 4️⃣ Implementation & Testing

#### 구현 환경

* **Python runtime:** Google Colab
* **CI/CD:** GitHub Actions
* **Secrets 관리:** GitHub Repository → Settings → Secrets → `ALPACA_KEY`, `ALPACA_SECRET`
* **자동 실행:** `.github/workflows/daily.yml`

  ```yaml
  name: Daily Trade Bot
  on:
    schedule:
      - cron: "0 14 * * 1-5"  # 매일 오후 2시 (UTC)
  jobs:
    run-bot:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Run bot
          run: |
            python main.py
      env:
        ALPACA_KEY: ${{ secrets.ALPACA_KEY }}
        ALPACA_SECRET: ${{ secrets.ALPACA_SECRET }}
  ```
* **테스트 시나리오**

  * Mock Alpaca API를 사용한 단위 테스트
  * 샘플 데이터 기반 백테스트 결과 검증

---

### 📁 제안 GitHub 구조

```
IanETrading/
 ┣ docs/
 ┃ ┣ 01-Planning/
 ┃ ┣ 02-Analysis/
 ┃ ┣ 03-Design/
 ┃ ┗ 04-Implementation/
 ┣ src/
 ┃ ┣ data_fetcher.py
 ┃ ┣ signal_manager.py
 ┃ ┣ trade_executor.py
 ┃ ┗ main.py
 ┣ .github/
 ┃ ┗ workflows/
 ┃    ┗ daily.yml
 ┣ requirements.txt
 ┣ README.md
 ┗ .gitignore
```

---

이 포맷을 `docs/PROJECT_PLAN.md`로 저장하면 깃허브 상에서도 완벽히 읽히고,
후속 단계별 산출물(`SystemRequest.md`, `Requirements.md`, `CRC.md` 등)을 폴더별로 확장할 수 있습니다.

---
