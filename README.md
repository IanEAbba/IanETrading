# IanETrading 

This project is an experimental trading bot system designed to explore and implement various algorithmic trading strategies.

The goal of this project is twofold:
-  To **improve my backend, API integration, and cloud deployment skills**
-  To **build a functional, modular trading bot that can eventually run on live or paper trading accounts**

---

##  Project Goals

- Use **Alpaca Markets API** to access live market data and place trades
- Implement a **Smart Money Momentum Strategy**, with a focus on detecting institutional buying behavior
- Build in **modular trading logic**, allowing for future strategies to be plugged in
- Host and manage the bot using **AWS (EC2 or Lambda)** for 24/7 uptime
- Use **Python** as the core development language
- Optional: Expand the system with a **Java-based backend dashboard or REST API** in the future

---

## Tech Stack

- **Python 3.10+**
- [Alpaca Trade API](https://alpaca.markets/)
- **Pandas** for data manipulation
- **dotenv** for environment variable management
- **AWS EC2** for deployment (initially)
- (Optional later) **FastAPI**, **MongoDB**, or **Spring Boot**

---

## Strategy: Smart Money Momentum

The initial strategy to be implemented includes:
- Detecting **unusual volume spikes**
- Confirming price breakout **above VWAP or key resistance**
- Avoiding fakeouts by waiting for **volume confirmation**
- Executing trades with a **defined risk/reward ratio**
- Sending alerts via **Telegram bot**

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/IanETrading.git
   cd IanETrading
