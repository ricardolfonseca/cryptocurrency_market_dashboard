# 📈 Cryptocurrency Market Dashboard

🚀 A **real-time cryptocurrency tracking dashboard** built with **Streamlit, CoinGecko API, and Plotly**. This project provides **live prices, historical trends, and interactive visualizations** for various cryptocurrencies.

> **Collaborators:** [ricardolfonseca](https://github.com/ricardolfonseca) & [invoany](https://github.com/invoany)

---

## **🌟 Features**
- ✅ **Live Cryptocurrency Prices** — Fetches **real-time market data** from CoinGecko.
- ✅ **Interactive Visualizations** — Uses **Plotly** for price trend analysis.
- ✅ **Multi-Currency Support** — Switch between **USD, EUR, and GBP**.
- ✅ **Compact & Readable Data Table** — Includes **crypto logos** and formatted numbers.
- ✅ **Historical Price Trends** — Select up to **365 days** of historical data.
- ✅ **Automatic Updates** — Refreshes prices **every 10 minutes**.
- ✅ **User-Friendly Interface** — Sidebar filters for easy cryptocurrency selection.

---

## **📊 Data Explanation**
This dashboard fetches data from the **CoinGecko API**, providing up-to-date cryptocurrency market details. The following information is displayed:

### **1️⃣ Live Cryptocurrency Data**
- **ID & Symbol** — Unique identifier and ticker symbol.
- **Name & Logo** — Name and official icon of the cryptocurrency.
- **Current Price** — The latest market price.
- **Market Cap** — Total market capitalization (circulating supply × price).
- **24H High & Low** — The highest and lowest price in the last 24 hours.
- **Price Change (24H)** — Absolute and percentage change in price over the last 24 hours.
- **Total Volume** — Total trading volume in the last 24 hours.

### **2️⃣ Historical Price Trends**
- **Date-Based Price Data** — Allows users to view price trends over a selected period.
- **Candlestick Time Range** — Users can select a range between **1 and 365 days**.
- **Interactive Graphs** — View price movements with zoom and hover functionality.

---

## **📥 Installation**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/ricardolfonseca/cryptocurrency_market_dashboard.git
cd cryptocurrency_market_dashboard
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Streamlit App**
```bash
streamlit run main.py
```

---

## **🖥️ How to Use the Dashboard**
1. **Select Your Currency**  
   - Choose between **USD, EUR, and GBP**.

2. **Choose a Cryptocurrency**  
   - Select from the **top 10 cryptocurrencies** (ranked by market cap).

3. **View Live Market Data**  
   - A table with **prices, market caps, and 24-hour changes** will be displayed.

4. **Analyze Historical Trends**  
   - Choose a **time range (1-365 days)** in the sidebar slider.
   - View an **interactive price trend candle chart**.

5. **Automatic Updates**  
   - The dashboard **refreshes data every 10 minutes**.

---

## **⚙️ Project Structure**
```
cryptocurrency_market_dashboard/
├── main.py                  # App entry point
├── app.py                   # Streamlit UI
├── controller/
│   ├── exchange_controller.py  # Handles API calls
├── model/
│   ├── crypto_data.py        # Fetches live & historical data
│   ├── data_treatment.py     # Logging & configuration
├── view/
│   ├── visualization.py      # Graphs & charts
├── requirements.txt          # Dependencies list
├── README.md                 # Project documentation
```

---

## **🔧 Tech Stack**
- 🐍 **Python** — Core programming language.
- 🖥 **Streamlit** — Web-based UI framework.
- 📊 **Plotly** — Data visualization library.
- 🌐 **CoinGecko API** — Fetches live & historical market data.
- 🗃 **Pandas** — Handles data processing.