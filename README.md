# 📈 Cryptocurrency Market Dashboard

🚀 A **real-time cryptocurrency tracking dashboard** built with **Streamlit, CoinGecko API, and Plotly**. This project provides **live prices, historical trends, an AI chatbot**, and **interactive visualizations** for top cryptocurrencies.

🌐 **Live Demo:** [cryptocurrency-market-dashboard.streamlit.app](https://cryptocurrency-market-dashboard.streamlit.app/)

👥 **Collaborators:** [ricardolfonseca](https://github.com/ricardolfonseca) & [invoany](https://github.com/invoany)

---

## 🌟 **Features**

- ✅ **Live Cryptocurrency Prices** – Real-time data from CoinGecko (top 10 by market cap).  
- ✅ **Multi-Currency Support** – Switch between **USD** and **EUR**.  
- ✅ **Interactive Candlestick Charts** – Historical trends from 1 to 365 days, powered by Plotly.  
- ✅ **Compact & Readable Data Table** – Clean display with logos, thousands separators, and currency symbols.  
- ✅ **AI Chatbot (Gemini)** – Ask questions about cryptocurrencies; the bot uses current market data for context and politely refuses conversions to other currencies.  
- ✅ **1-Minute Caching** – Reduces API calls while keeping data fresh.  
- ✅ **MVC Architecture** – Well-organized code with separate `model`, `view`, and `controller` layers.  
- ✅ **Responsive Layout** – Works on desktop and mobile.

---

## 📊 **Data Explanation**

The dashboard fetches data from the [CoinGecko API](https://www.coingecko.com/en/api). The following information is displayed:

### **Live Table**
- **Rank** – Market cap rank.
- **Name & Logo** – Cryptocurrency name and official icon.
- **Symbol** – Ticker symbol.
- **Current Price** – Latest market price in selected currency (with thousands separators).
- **Market Cap** – Total market capitalization (circulating supply × price).
- **Total Volume** – 24-hour trading volume.
- **Circulating Supply** – Number of coins in circulation.
- **All-Time High (ATH)** – Highest price ever recorded, with date and percentage change from ATH.

### **Candlestick Chart**
- Visualizes **open, high, low, close** prices over a selected period.
- Green candles indicate price increase; red candles indicate decrease.
- Includes a moving average line for trend clarity.

### **AI Chatbot**
- Built with Google **Gemini 2.0 Flash**.
- Understands natural language questions about cryptocurrencies.
- Uses the live market data from the dashboard as context.
- **Does not perform currency conversions** – instead suggests changing the currency in the sidebar.

---

## 📥 **Installation**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ricardolfonseca/cryptocurrency_market_dashboard.git
cd cryptocurrency_market_dashboard
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up API Keys (for Chatbot)
The chatbot uses Google Gemini. Obtain a free API key from aistudio.google.com.  
Create a file `.streamlit/secrets.toml` in the project root and add:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

⚠️ Do not commit this file – it’s already in `.gitignore`.

### 4️⃣ Run the App
```bash
streamlit run app.py
```

---

## 🖥️ How to Use

### Sidebar Controls
- Select Currency – Choose USD or EUR.  
- Pick a Cryptocurrency – Select from the top 10 coins.  
- Choose Time Range – Set the number of days for the candlestick chart (1–365).

### Main Dashboard
- The live price table updates every minute and shows a timestamp of the last refresh.  
- The candlestick chart provides historical analysis – hover to see exact values.  
- Click the 💬 Chat button in the top-right corner to open the chatbot popover.  
- Ask questions like “What is Bitcoin’s price?” or “Compare Ethereum and Solana”.  
- The bot will answer based on the current market data and its general knowledge.  
- If you ask for a price in a currency not selected, it will politely suggest changing the currency in the sidebar.

---

## ⚙️ Project Structure

```text
cryptocurrency_market_dashboard/
├── app.py                         # Main Streamlit application (view)
├── controller/
│   └── controller.py              # Lightweight controller (orchestrates model and view)
├── model/
│   ├── crypto_data_provider.py    # CoinGecko API calls (class)
│   ├── gemini_chat.py             # Gemini chatbot logic (class)
│   └── formatter.py               # MarketDataFormatter utility (price/number formatting)
├── view/
│   └── view.py                    # Plotly charts and formatting helpers
├── .streamlit/
│   └── secrets.toml               # API keys (ignored by Git)
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── .gitignore                     # Git ignore rules
```

---

## 🔧 Tech Stack

- 🐍 Python 3.11 – Core language.  
- 🖥 Streamlit – Rapid UI development.  
- 📊 Plotly – Interactive charts.  
- 🌐 CoinGecko API – Real-time and historical crypto data.  
- 🤖 Google Gemini API – AI-powered chatbot.  
- 🗃 Pandas – Data manipulation.  
- 🧹 Requests & urllib3 – API calls with retry logic.

---

## 📝 Recent Improvements

This project evolved through several refactors to achieve a clean MVC structure and enhance user experience:

- MVC Architecture – Split monolithic code into model, view, and controller layers.  
- Classes in Model – CryptoDataProvider (CoinGecko), GeminiChat, and MarketDataFormatter encapsulate logic.  
- 1-Minute Caching – Live data is cached for 60 seconds to reduce API load.  
- AI Chatbot – Integrated Gemini with context from live market data; handles currency conversion politely.  
- Thousand Separators – Numbers in the table now show commas (e.g., $68,732.00) for readability.  
- Currency Symbols – Dynamic display of $ or € based on selection.  
- Popover Chat UI – Chat opens in a compact popover, keeping the dashboard clean.  
- Timestamp on Data – Shows when the data was last refreshed.  
- Bug Fixes – Resolved duplicate set_page_config, currency-detection issues, and formatting glitches.

---

## 🙌 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. For major changes, please discuss first.

---

## 📄 License

MIT