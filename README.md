# Qubic Price Tracker Bot 🚀

A high-performance, asynchronous Telegram bot designed to provide real-time statistics for the **Qubic (QUBIC)** ecosystem. Built with `python-telegram-bot` and `aiohttp`.

---

## 🛠 Features

* **Instant Responses:** Data is served from a local cache—no waiting for API calls.
* **Detailed Metrics:** Tracks Price (9 decimals), Market Cap, Active Addresses, and Burned $QUB$.
* **Automated Background Refresh:** The bot fetches new data independently of user requests.
* **Safe Concurrency:** Uses `asyncio.Lock` to prevent "Cache Stampedes."
* **Production Logging:** Rotating logs to monitor performance and API health.

---

## 🏗 System Architecture

The bot uses a **Background Worker** pattern to ensure the user never experiences lag:

1.  **Background Loop:** Every 30 seconds, a task wakes up and fetches data from the Qubic RPC.
2.  **Global Cache:** Data is formatted and stored in memory with a timestamp.
3.  **User Request:** When a user triggers `/dmprice`, the bot pulls the pre-formatted text from memory instantly.



---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/drdtrn/qubot.git](https://github.com/drdtrn/qubot.git)
cd qubot
```
### 2. Install Dependencies
```Bash
pip install -r requirements.txt
```
### 3. Configure Environment Variables
Create a .env file in the root directory:

### Code snippet

BOT_TOKEN=your_telegram_bot_token_here

LOG_PATH=./bot.log
🚀 Usage
Start the bot by running:

```Bash
python bot.py
```
## Commands:

/dmprice - Displays the current Qubic price, market cap, and burned supply.

## 🛡 Security & Best Practices
### Secrets Management: Uses python-dotenv to keep your API keys out of the source code.

### Asynchronous Design: Non-blocking code ensures the bot stays responsive.

### Error Handling: Includes try-except blocks for API failures to ensure the bot remains online.

## 📄 Requirements
```
Python 3.10+

python-telegram-bot

aiohttp

python-dotenv
```
