# IanETrading Project Plan

## 1. Requirements Specification

### Functional Requirements
- [x] Connect to Alpaca API to fetch real-time market data
- [x] Detect momentum-based entry signals using price and volume
- [ ] Send alert or place trade when conditions are met
- [ ] Use .env for API key and configuration management
- [ ] Deploy to AWS to run continuously

### Non-Functional Requirements
- [x] Implement using Python
- [ ] Persistent behavior on restart (optional)
- [ ] Version control using Git
- [ ] Avoid committing secrets or sensitive files

---

## 2. Design

### System Architecture
```
[Alpaca API]
     |
[alpaca_client.py] <- handles market data and order execution
     |
[strategy.py] <- defines and evaluates trade logic
     |
[notifier.py] <- sends alerts (e.g. Telegram, console)
     |
[trader.py] <- executes trades based on signal
     |
[run.py] <- main entrypoint to schedule and run bot
```

### Configuration
- Environment variables loaded through `.env`
- Centralized in `config.py`

### Modular Structure
- Strategy logic kept in `strategy.py`
- Scalable: future strategies can be added easily
- Trade history stored in `data/trade_log.csv`

---

## 3. Testing

### Testing Scope
- [ ] Test entry signal logic in `strategy.py`
- [ ] Validate order flow and API response handling
- [ ] Ensure environment config is loaded correctly
- [ ] Telegram alert sending (manual test OK)

### Tools
- Manual testing in dev
- Optional: use `pytest`
- Simulate market data using sample CSVs for backtest

---

## 4. Maintenance & Deployment

- Deploy on EC2 or use Docker container
- Use `.env.dev` vs `.env.prod` to separate environments
- Consider GitHub Actions for CI/CD
- Logs stored in CloudWatch or local `data/` folder

---

## Milestones (Tentative)
| Week | Goals |
|------|-------|
| Week 1 | Planning, API connection, project scaffolding |
| Week 2 | Strategy implementation, alert system |
| Week 3 | Auto order execution, backtesting logic |
| Week 4 | AWS deployment, testing, final review |

---

## Next Actions (TO-DO)
- [ ] Await API key approval
- [ ] Create `alpaca_client.py` with market/order functions
- [ ] Define and test strategy logic in `strategy.py`
- [ ] Integrate everything in `run.py`

