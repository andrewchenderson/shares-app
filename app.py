# [START OF FILE]
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="ASX Price Dashboard", layout="wide")
st.title("ASX Price Dashboard")
st.caption(
    "Educational tool — not financial advice. Focused on: *How does the stock price compare to sector benchmarks today?*"
)

# -----------------------------
# Tickers (example)
# -----------------------------
asx_300_tickers = [
    "AIA.AX", "ALL.AX", "AMC.AX", "ANZ.AX", "APA.AX", "ASX.AX", "BHP.AX", "BSL.AX", "BXB.AX",
    "CBA.AX", "COH.AX", "COL.AX", "CSL.AX", "DXS.AX", "FMG.AX", "FPH.AX", "GMG.AX", "IAG.AX",
    "JHX.AX", "MGR.AX", "MQG.AX", "NAB.AX", "NCM.AX", "NST.AX", "QBE.AX", "REA.AX", "REH.AX",
    "RHC.AX", "RIO.AX", "RMD.AX", "S32.AX", "SCG.AX", "SEK.AX", "SGP.AX", "SHL.AX", "STO.AX",
    "SUN.AX", "SYD.AX", "TAH.AX", "TCL.AX", "TLS.AX", "TPG.AX", "WBC.AX", "WES.AX", "WOW.AX",
    "WPL.AX", "WTC.AX", "XRO.AX", "ALD.AX", "MIN.AX"
]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Metric Display Settings")
metric_descriptions = {
    "PE": "Price-to-Earnings: Lower than sector benchmark is better value.",
    "PB": "Price-to-Book: Lower than sector benchmark is better value.",
    "ROE": "Return on Equity: Higher than sector benchmark indicates stronger profitability.",
    "DebtEquity": "Debt/Equity: Lower than benchmark indicates stronger balance sheet.",
    "PS": "Price-to-Sales: Lower than benchmark indicates cheaper relative to revenue.",
    "Trend": "Price vs 200-day MA: Above MA = uptrend (green), slightly below = caution (yellow), far below = red."
}
metrics_to_show = {}
for m, desc in metric_descriptions.items():
    metrics_to_show[m] = st.sidebar.checkbox(f"{m}: {desc}", value=True)

# -----------------------------
# Fixed sector benchmarks
# -----------------------------
sector_benchmarks = {
    "Financial Services": {"PE": 15, "PB": 1.5, "ROE": 10, "DebtEquity": 50, "PS": 2},
    "Basic Materials": {"PE": 20, "PB": 2, "ROE": 12, "DebtEquity": 30, "PS": 1.5},
    "Healthcare": {"PE": 25, "PB": 3, "ROE": 15, "DebtEquity": 20, "PS": 3},
    "Real Estate": {"PE": 18, "PB": 1.2, "ROE": 8, "DebtEquity": 60, "PS": 4},
    "Industrials": {"PE": 20, "PB": 2, "ROE": 12, "DebtEquity": 35, "PS": 1.5},
    "Energy": {"PE": 15, "PB": 1.5, "ROE": 10, "DebtEquity": 40, "PS": 1},
    "Consumer Defensive": {"PE": 22, "PB": 3, "ROE": 14, "DebtEquity": 30, "PS": 2},
    "Consumer Cyclical": {"PE": 25, "PB": 3, "ROE": 15, "DebtEquity": 25, "PS": 2},
    "Communication Services": {"PE": 23, "PB": 2.5, "ROE": 12, "DebtEquity": 20, "PS": 2},
    "Utilities": {"PE": 16, "PB": 1.5, "ROE": 8, "DebtEquity": 50, "PS": 1.5},
    "Technology": {"PE": 30, "PB": 4, "ROE": 18, "DebtEquity": 10, "PS": 4},
}

# -----------------------------
# Helper functions
# -----------------------------
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    try:
        tk = yf.Ticker(ticker)
        info = tk.info or {}
        hist = tk.history(period="2y")
        last_price = info.get("regularMarketPrice", np.nan)
        ma_200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else np.nan
        sector = info.get("sector", "Unknown")
        return {
            "Ticker": ticker,
            "Sector": sector,
            "Price": last_price,
            "200d MA": ma_200,
            "PE": info.get("trailingPE", np.nan),
            "PB": info.get("priceToBook", np.nan),
            "ROE": info.get("returnOnEquity", np.nan)*100 if info.get("returnOnEquity") else np.nan,
            "DebtEquity": info.get("debtToEquity", np.nan),
            "PS": info.get("priceToSalesTrailing12Months", np.nan)
        }
    except Exception as e:
        st.warning(f"Failed to fetch {ticker}: {e}")
        return None

def score_trend(row):
    if pd.notna(row["Price"]) and pd.notna(row["200d MA"]):
        if row["Price"] >= row["200d MA"]:
            return "green"
        elif row["Price"] >= 0.9 * row["200d MA"]:
            return "yellow"
        else:
            return "red"
    return "gray"

def traffic_light(val, benchmark, reverse=False):
    """Return a pastel-style background color based on comparison to benchmark."""
    if pd.isna(val) or pd.isna(benchmark):
        return ""
    try:
        val = float(val)
        benchmark = float(benchmark)
        if reverse:  # lower is better
            if val <= benchmark*0.8:
                return "background-color: rgba(0, 200, 0, 0.2)"  # soft green
            elif val <= benchmark:
                return "background-color: rgba(255, 255, 150, 0.2)"  # soft yellow
            else:
                return "background-color: rgba(255, 100, 100, 0.2)"  # soft red
        else:  # higher is better
            if val >= benchmark*1.2:
                return "background-color: rgba(0, 200, 0, 0.2)"  # soft green
            elif val >= benchmark:
                return "background-color: rgba(255, 255, 150, 0.2)"  # soft yellow
            else:
                return "background-color: rgba(255, 100, 100, 0.2)"  # soft red
    except:
        return ""

# -----------------------------
# Fetch all stocks
# -----------------------------
st.info("Fetching stock data... This may take a minute.")
stocks = []
progress_bar = st.progress(0)
for i, ticker in enumerate(asx_300_tickers):
    data = fetch_stock_data(ticker)
    if data:
        stocks.append(data)
    progress_bar.progress((i+1)/len(asx_300_tickers))

df = pd.DataFrame(stocks)

# -----------------------------
# Trend column
# -----------------------------
df["Trend"] = df.apply(score_trend, axis=1)

# -----------------------------
# Value column: count green metrics
# -----------------------------
def count_green(row):
    sector = row["Sector"]
    bench = sector_benchmarks.get(sector, {})
    greens = 0
    if pd.notna(row["PE"]) and row["PE"] <= bench.get("PE", np.nan)*0.8:
        greens += 1
    if pd.notna(row["PB"]) and row["PB"] <= bench.get("PB", np.nan)*0.8:
        greens += 1
    if pd.notna(row["ROE"]) and row["ROE"] >= bench.get("ROE", np.nan)*1.2:
        greens += 1
    if pd.notna(row["DebtEquity"]) and row["DebtEquity"] <= bench.get("DebtEquity", np.nan)*0.8:
        greens += 1
    if pd.notna(row["PS"]) and row["PS"] <= bench.get("PS", np.nan)*0.8:
        greens += 1
    if row["Trend"]=="green":
        greens += 1
    return greens

df["Value"] = df.apply(count_green, axis=1)

# -----------------------------
# Overview Table
# -----------------------------
overview_cols = ["Ticker","Sector","Price","PE","PB","ROE","DebtEquity","PS","Trend","Value"]
overview_df = df[overview_cols]

def style_overview(row):
    sector = row["Sector"]
    bench = sector_benchmarks.get(sector, {})

    style_list = []

    # Ticker, Sector, Price - no color
    style_list.extend(["", "", ""])

    # PE
    style_list.append(traffic_light(row["PE"], bench.get("PE", np.nan), reverse=True) if metrics_to_show["PE"] else "")

    # PB
    style_list.append(traffic_light(row["PB"], bench.get("PB", np.nan), reverse=True) if metrics_to_show["PB"] else "")

    # ROE
    style_list.append(traffic_light(row["ROE"], bench.get("ROE", np.nan)) if metrics_to_show["ROE"] else "")

    # DebtEquity
    style_list.append(traffic_light(row["DebtEquity"], bench.get("DebtEquity", np.nan), reverse=True) if metrics_to_show["DebtEquity"] else "")

    # PS
    style_list.append(traffic_light(row["PS"], bench.get("PS", np.nan), reverse=True) if metrics_to_show["PS"] else "")

    # Trend
    if metrics_to_show["Trend"]:
        style_list.append(
            "background-color: rgba(0, 200, 0, 0.2)" if row["Trend"]=="green" else
            "background-color: rgba(255, 255, 150, 0.2)" if row["Trend"]=="yellow" else
            "background-color: rgba(255, 100, 100, 0.2)" if row["Trend"]=="red" else ""
        )
    else:
        style_list.append("")

    # Value - no color
    style_list.append("")

    return style_list

st.dataframe(overview_df.style.apply(lambda r: style_overview(r), axis=1))

# -----------------------------
# Rationale Box
# -----------------------------
st.markdown("""
**Rationale:**
- **P/E, P/B, P/S:** Compare to sector benchmarks. Lower than benchmark = green, near = yellow, higher = red.
- **ROE:** Higher than benchmark = green, near = yellow, below = red.
- **Debt/Equity:** Lower than benchmark = green, near = yellow, higher = red.
- **Trend:** Price vs 200-day MA: Above MA = green, slightly below = yellow, far below = red.
- **Value:** Counts number of "green" metrics (best value and trend).
""")
# [END OF FILE]
