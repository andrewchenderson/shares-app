import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Stockstream", layout="wide")
st.title("Stockstream")
st.caption(
    "Educational tool — not financial advice. Focused on: *How does the stock price compare to sector benchmarks today?*"
)

# -----------------------------
# Tickers (50 focus stocks)
# -----------------------------
asx_focus_tickers = [
    "AIA.AX", "ALL.AX", "AMC.AX", "ANZ.AX", "APA.AX", "ASX.AX", "BHP.AX", "BSL.AX", "BXB.AX",
    "CBA.AX", "COH.AX", "COL.AX", "CSL.AX", "DXS.AX", "FMG.AX", "FPH.AX", "GMG.AX", "IAG.AX",
    "JHX.AX", "MGR.AX", "MQG.AX", "NAB.AX", "NCM.AX", "NST.AX", "QBE.AX", "REA.AX", "REH.AX",
    "RHC.AX", "RIO.AX", "RMD.AX", "S32.AX", "SCG.AX", "SEK.AX", "SGP.AX", "SHL.AX", "STO.AX",
    "SUN.AX", "SYD.AX", "TAH.AX", "TCL.AX", "TLS.AX", "TPG.AX", "WBC.AX", "WES.AX", "WOW.AX",
    "WPL.AX", "WTC.AX", "XRO.AX", "ALD.AX", "MIN.AX"
]

# -----------------------------
# ASX200 tickers (for benchmarks)
# -----------------------------
# TODO: replace this placeholder with your full ASX200 list
asx200_tickers = [
    "360.AX", "3PL.AX", "4DX.AX", "5EA.AX", "A2M.AX", "ABB.AX", "ABC.AX", "ABP.AX", "ABY.AX", "AD8.AX"
"ADH.AX", "ADT.AX", "AGL.AX", "AGY.AX", "AHX.AX", "AIA.AX", "AIZ.AX", "ALD.AX", "ALG.AX", "ALL.AX"
"ALQ.AX", "ALU.AX", "AMA.AX", "AMC.AX", "AMP.AX", "ANN.AX", "ANZ.AX", "APE.AX", "APM.AX", "APT.AX"
"APX.AX", "ARB.AX", "ARG.AX", "ARU.AX", "ASB.AX", "ASX.AX", "AUB.AX", "AUI.AX", "AUR.AX", "AUS.AX"
"AVH.AX", "AVZ.AX", "AWC.AX", "AX1.AX", "AXE.AX", "AZJ.AX", "BAP.AX", "BBOZ.AX", "BEN.AX", "BGA.AX"
"BGL.AX", "BHP.AX", "BKL.AX", "BKW.AX", "BLD.AX", "BLX.AX", "BPT.AX", "BRG.AX", "BRN.AX", "BSL.AX"
"BUB.AX", "BVS.AX", "BWP.AX", "BXB.AX", "C29.AX", "C6C.AX", "CBA.AX", "CCL.AX", "CCP.AX", "CCX.AX"
"CDP.AX", "CGC.AX", "CGF.AX", "CHC.AX", "CHN.AX", "CIA.AX", "CIM.AX", "CKF.AX", "CLW.AX", "CMW.AX"
"CNI.AX", "COH.AX", "COL.AX", "CPU.AX", "CQR.AX", "CRN.AX", "CSL.AX", "CSR.AX", "CTD.AX", "CUV.AX"
"CWN.AX", "CWY.AX", "CXL.AX", "DBI.AX", "DCN.AX", "DDR.AX", "DEG.AX", "DHG.AX", "DMP.AX", "DOW.AX"
"DRR.AX", "DTL.AX", "DUB.AX", "DYL.AX", "EBO.AX", "ECX.AX", "EDV.AX", "ELD.AX", "EML.AX", "EMR.AX"
"EOS.AX", "ERA.AX", "EVN.AX", "EVT.AX", "FBU.AX", "FCL.AX", "FEX.AX", "FLT.AX", "FMG.AX", "FPH.AX"
"FWD.AX", "GDF.AX", "GMA.AX", "GNC.AX", "GOZ.AX", "GQG.AX", "GRR.AX", "GUD.AX", "GWA.AX", "HLS.AX"
"HMC.AX", "HSN.AX", "HT1.AX", "HVN.AX", "HZN.AX", "IAU.AX", "IEL.AX", "IFL.AX", "IGO.AX", "ILU.AX"
"IMU.AX", "INA.AX", "ING.AX", "IPH.AX", "IPL.AX", "IRE.AX", "IVC.AX", "IVZ.AX", "JBH.AX", "JHX.AX"
"JLG.AX", "JRV.AX", "KGN.AX", "KLS.AX", "KMD.AX", "KPG.AX", "LFS.AX", "LFG.AX", "LGL.AX", "LLC.AX"
"LNK.AX", "LOV.AX", "LTR.AX", "LYC.AX", "MAH.AX", "MAQ.AX", "MCY.AX", "MEZ.AX", "MFG.AX", "MGR.AX"
"MIN.AX", "MMS.AX", "MP1.AX", "MPL.AX", "MQG.AX", "MSB.AX", "MSL.AX", "MTS.AX", "MYR.AX", "NAB.AX"
"NAN.AX", "NCK.AX", "NEC.AX", "NEU.AX", "NHF.AX", "NIC.AX", "NHC.AX", "NMT.AX", "NST.AX", "NUF.AX"
"NWH.AX", "NWL.AX", "NXT.AX", "OBL.AX", "OML.AX", "OPT.AX", "ORA.AX", "ORE.AX", "ORI.AX", "OSH.AX"
"OZL.AX", "PDN.AX", "PEA.AX", "PEP.AX", "PGH.AX", "PLS.AX", "PME.AX", "PMV.AX", "PNI.AX", "PNV.AX"
"PPK.AX", "PRN.AX", "PRU.AX", "PSI.AX", "PTM.AX", "QAN.AX", "QBE.AX", "QUB.AX", "RBL.AX", "REA.AX"
"RED.AX", "REG.AX", "REH.AX", "RFF.AX", "RHC.AX", "RIO.AX", "RMD.AX", "RMS.AX", "RRL.AX", "RSG.AX"
"RWC.AX", "S32.AX", "SBM.AX", "SCP.AX", "SCU.AX", "SDG.AX", "SEK.AX", "SFR.AX", "SGF.AX", "SGM.AX"
"SGP.AX", "SHL.AX", "SIQ.AX", "SIV.AX", "SKC.AX", "SKI.AX", "SLR.AX", "SM1.AX", "SMR.AX", "SOL.AX"
"SPK.AX", "SPT.AX", "SQR.AX", "SRG.AX", "SRX.AX", "SSM.AX", "STO.AX", "STX.AX", "SUL.AX", "SUN.AX"
"SVW.AX", "SWM.AX", "SYA.AX", "SYD.AX", "SYR.AX", "TAH.AX", "TCL.AX", "TGR.AX", "TLS.AX", "TLX.AX"
"TNE.AX", "TPG.AX", "TPW.AX", "TUA.AX", "TWE.AX", "TYR.AX", "UBI.AX", "UMG.AX", "UNI.AX", "URW.AX"
"VGL.AX", "VHT.AX", "VMS.AX", "VOC.AX", "VRC.AX", "VRL.AX", "VUK.AX", "WAF.AX", "WAM.AX", "WBC.AX"
"WEB.AX", "WES.AX", "WHC.AX", "WOR.AX", "WOW.AX", "WPL.AX", "WPR.AX", "WTC.AX", "XRO.AX", "YAL.AX"
"ZIM.AX", "ZNO.AX",
]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Metric Display Settings")
metric_descriptions = {
    "PE": "Price-to-Earnings: Dollar cost of share for every dollar profit company made",
    "PB": "Share dollar cost for every dollar company has in assets - how asset rich is the stock",
    "ROE": "Return for every shareholder dollar invested",
    "Debt/Equity": "Lower than benchmark indicates stronger asset position",
    "PS": "Price to sales - Dollar cost of share for every dollar of revenue.",
    "Trend": "Is today's share price above or below its 200 day average? No - potential dying stock. Yes - strong stock."
}
metrics_to_show = {}
for m, desc in metric_descriptions.items():
    metrics_to_show[m] = st.sidebar.checkbox(f"{m}: {desc}", value=True)

# -----------------------------
# Dynamic benchmark pool selection
# -----------------------------
st.sidebar.header("Benchmarking Pool")
benchmark_pool_size = st.sidebar.selectbox(
    "Select benchmarking pool size:",
    options=[100, 150, 200],
    index=2,  # default 100
)

# -----------------------------
# Fallback fixed sector benchmarks
# -----------------------------
fallback_sector_benchmarks = {
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
# Helpers
# -----------------------------
def normalize_ticker(ticker: str) -> str:
    ticker = str(ticker).upper()
    return ticker if ticker.endswith('.AX') else ticker + '.AX'

@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    """Fetch metrics for a ticker using yfinance. Returns dict or None on failure."""
    try:
        full_t = normalize_ticker(ticker)
        tk = yf.Ticker(full_t)
        info = tk.info or {}
        hist = tk.history(period="2y")

        last_price = info.get("regularMarketPrice", np.nan)
        ma_200 = hist['Close'].rolling(200).mean().iloc[-1] if len(hist) >= 200 else np.nan
        sector = info.get("sector", "Unknown")

        return {
            "Ticker": full_t,
            "Sector": sector,
            "Price": last_price,
            "200d MA": ma_200,
            "PE": info.get("trailingPE", np.nan),
            "PB": info.get("priceToBook", np.nan),
            "ROE": (info.get("returnOnEquity", np.nan) * 100) if info.get("returnOnEquity") is not None else np.nan,
            "DebtEquity": info.get("debtToEquity", np.nan),
            "PS": info.get("priceToSalesTrailing12Months", np.nan)
        }
    except Exception as e:
        st.warning(f"Failed to fetch {ticker}: {e}")
        return None

@st.cache_data(ttl=3600)
def compute_dynamic_benchmarks(tickers):
    """Compute sector-level benchmarks (median) from a list of tickers."""
    stocks = []
    progress = st.progress(0)
    for i, t in enumerate(tickers):
        data = fetch_stock_data(t)
        if data:
            stocks.append(data)
        progress.progress((i + 1) / len(tickers))

    if not stocks:
        return {}

    df = pd.DataFrame(stocks)

    # ensure numeric types
    for col in ["PE", "PB", "ROE", "DebtEquity", "PS"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # groupby sector and take median
    sector_benchmarks = df.groupby("Sector")[["PE", "PB", "ROE", "DebtEquity", "PS"]].median().to_dict(orient="index")
    return sector_benchmarks

def score_trend(row):
    if pd.notna(row.get("Price")) and pd.notna(row.get("200d MA")):
        if row["Price"] >= row["200d MA"]:
            return "green"
        elif row["Price"] >= 0.9 * row["200d MA"]:
            return "yellow"
        else:
            return "red"
    return "gray"

def traffic_light(val, benchmark, reverse=False):
    """Return pastel-style CSS string based on comparison to benchmark."""
    if pd.isna(val) or pd.isna(benchmark):
        return ""
    try:
        val = float(val)
        benchmark = float(benchmark)
        if reverse:  # lower is better
            if val <= benchmark * 0.8:
                return "background-color: rgba(0, 200, 0, 0.2)"
            elif val <= benchmark:
                return "background-color: rgba(255, 255, 150, 0.2)"
            else:
                return "background-color: rgba(255, 100, 100, 0.2)"
        else:  # higher is better
            if val >= benchmark * 1.2:
                return "background-color: rgba(0, 200, 0, 0.2)"
            elif val >= benchmark:
                return "background-color: rgba(255, 255, 150, 0.2)"
            else:
                return "background-color: rgba(255, 100, 100, 0.2)"
    except Exception:
        return ""

# -----------------------------
# Helper: fetch market cap for a ticker
# -----------------------------
@st.cache_data(ttl=3600)
def fetch_market_cap(ticker):
    try:
        tk = yf.Ticker(normalize_ticker(ticker))
        info = tk.info or {}
        return info.get("marketCap", np.nan)
    except:
        return np.nan

# -----------------------------
# Filter ASX200 by top market cap
# -----------------------------
@st.cache_data(ttl=3600)
def get_top_n_by_marketcap(tickers, n):
    """Return the top N tickers sorted by market cap."""
    caps = []
    progress = st.progress(0)
    for i, t in enumerate(tickers):
        mc = fetch_market_cap(t)
        if not pd.isna(mc):
            caps.append({"Ticker": t, "MarketCap": mc})
        progress.progress((i + 1) / len(tickers))
    df_caps = pd.DataFrame(caps)
    df_caps_sorted = df_caps.sort_values("MarketCap", ascending=False).head(n)
    return df_caps_sorted["Ticker"].tolist()

# -----------------------------
# Compute dynamic benchmarks using top N by market cap
# -----------------------------
st.info(f"Computing dynamic sector benchmarks from top {benchmark_pool_size} ASX200 stocks by market cap... (may take a while)")
top_n_tickers = get_top_n_by_marketcap(asx200_tickers, benchmark_pool_size)
sector_benchmarks = compute_dynamic_benchmarks(top_n_tickers)


# -----------------------------
# Fetch focus stocks
# -----------------------------
st.info("Fetching focus stock data... This may take a minute.")
stocks = []
progress_bar = st.progress(0)
for i, ticker in enumerate(asx_focus_tickers):
    data = fetch_stock_data(ticker)
    if data:
        stocks.append(data)
    progress_bar.progress((i + 1) / len(asx_focus_tickers))

# -----------------------------
# Data preparation
# -----------------------------
df = pd.DataFrame(stocks) if stocks else pd.DataFrame(
    columns=["Ticker","Sector","Price","200d MA","PE","PB","ROE","DebtEquity","PS"]
)

# Ensure numeric
for col in ["PE", "PB", "ROE", "DebtEquity", "PS"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Trend
df["Trend"] = df.apply(score_trend, axis=1) if not df.empty else []

# Helper to get benchmark value with fallback
def get_bench_value(sector, metric):
    v = np.nan
    if sector in sector_benchmarks:
        v = sector_benchmarks.get(sector, {}).get(metric, np.nan)
    if pd.isna(v):
        v = fallback_sector_benchmarks.get(sector, {}).get(metric, np.nan)
    return v

# Value score
def count_green(row):
    sector = row.get("Sector", "Unknown")
    greens = 0
    if pd.notna(row.get("PE")) and row.get("PE") <= get_bench_value(sector, "PE") * 0.8:
        greens += 1
    if pd.notna(row.get("PB")) and row.get("PB") <= get_bench_value(sector, "PB") * 0.8:
        greens += 1
    if pd.notna(row.get("ROE")) and row.get("ROE") >= get_bench_value(sector, "ROE") * 1.2:
        greens += 1
    if pd.notna(row.get("DebtEquity")) and row.get("DebtEquity") <= get_bench_value(sector, "DebtEquity") * 0.8:
        greens += 1
    if pd.notna(row.get("PS")) and row.get("PS") <= get_bench_value(sector, "PS") * 0.8:
        greens += 1
    if row.get("Trend") == "green":
        greens += 1
    return greens

df["Value"] = df.apply(count_green, axis=1) if not df.empty else []

# -----------------------------
# Overview display
# -----------------------------
overview_cols = ["Ticker","Sector","Price","PE","PB","ROE","DebtEquity","PS","Trend","Value"]
overview_df = df[overview_cols].copy()

def style_overview(row):
    sector = row.get("Sector", "Unknown")
    style_list = ["", "", ""]  # Ticker, Sector, Price
    style_list.append(traffic_light(row.get("PE", np.nan), get_bench_value(sector, "PE"), reverse=True) if metrics_to_show.get("PE", True) else "")
    style_list.append(traffic_light(row.get("PB", np.nan), get_bench_value(sector, "PB"), reverse=True) if metrics_to_show.get("PB", True) else "")
    style_list.append(traffic_light(row.get("ROE", np.nan), get_bench_value(sector, "ROE"), reverse=False) if metrics_to_show.get("ROE", True) else "")
    style_list.append(traffic_light(row.get("DebtEquity", np.nan), get_bench_value(sector, "DebtEquity"), reverse=True) if metrics_to_show.get("DebtEquity", True) else "")
    style_list.append(traffic_light(row.get("PS", np.nan), get_bench_value(sector, "PS"), reverse=True) if metrics_to_show.get("PS", True) else "")
    if metrics_to_show.get("Trend", True):
        style_list.append(
            "background-color: rgba(0, 200, 0, 0.2)" if row.get("Trend") == "green" else
            "background-color: rgba(255, 255, 150, 0.2)" if row.get("Trend") == "yellow" else
            "background-color: rgba(255, 100, 100, 0.2)" if row.get("Trend") == "red" else ""
        )
    else:
        style_list.append("")
    style_list.append("")  # Value
    return style_list

if not overview_df.empty:
    st.dataframe(overview_df.style.apply(lambda r: style_overview(r), axis=1))
else:
    st.info("No data to display. Check ticker list or internet connection to yfinance.")

# Optional: show computed sector benchmarks
with st.expander("Show computed sector benchmarks (median from ASX200)"):
    if sector_benchmarks:
        bench_df = pd.DataFrame(sector_benchmarks).T
        st.dataframe(bench_df)
    else:
        st.write("No dynamic benchmarks computed. The app will use fallback benchmarks where available.")

# -----------------------------
# Rationale
# -----------------------------
st.markdown("""
**Rationale:**
- **P/E, P/B, P/S:** Compare to dynamic sector benchmarks (from ASX200). Lower = green, near = yellow, higher = red.
- **ROE:** Higher than benchmark = green, near = yellow, below = red.
- **Debt/Equity:** Lower than benchmark = green, near = yellow, higher = red.
- **Trend:** Price vs 200-day MA: Above MA = green, slightly below = yellow, far below = red.
- **Value:** Counts number of "green" metrics (best value and trend).
""")
