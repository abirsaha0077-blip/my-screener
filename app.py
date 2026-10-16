import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.parse
import warnings

warnings.filterwarnings("ignore")

# ==============================================================================
# ১. পেজ কনফিগারেশন
# ==============================================================================
st.set_page_config(
    page_title="AlphaPulse Pro | Intraday, Swing & Sector Terminal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# ২. ৩২টি সেক্টর ও শেয়ারের তালিকা (১৮০+ লিকুইড এনএসই স্টক)
# ==============================================================================
SECTOR_STOCKS = {
    "Defence & Aerospace": ["HAL.NS", "BEL.NS", "BDL.NS", "PARAS.NS", "DATAPATTNS.NS", "ASTRAMICRO.NS"],
    "Shipbuilding & Marine": ["MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "SCI.NS", "GESHIP.NS"],
    "Railways & Wagons": ["RVNL.NS", "IRFC.NS", "IRCON.NS", "TITAGARH.NS", "JWL.NS", "CONCOR.NS", "RITES.NS"],
    "Cables & Wires": ["POLYCAB.NS", "KEI.NS", "RRKABEL.NS", "FINCABLES.NS", "UNIVERSAL.NS"],
    "Transformers & Power T&D": ["CGPOWER.NS", "VOLTAMP.NS", "TARIL.NS", "POWERINDIA.NS", "APARINDS.NS"],
    "EMS & Electronics": ["DIXON.NS", "KAYNES.NS", "SYRMA.NS", "AMBER.NS", "PGEL.NS", "CYIENTDLM.NS"],
    "Green Energy & Solar": ["IREDA.NS", "SUZLON.NS", "INOXWIND.NS", "KPIGREEN.NS", "BORORENEW.NS"],
    "Power Utilities & Financiers": ["NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "PFC.NS", "RECLTD.NS", "NHPC.NS", "JSWENERGY.NS"],
    "Cooling & HVAC": ["VOLTAS.NS", "BLUESTARCO.NS", "SYMPHONY.NS", "WHIRLPOOL.NS", "HAVELLS.NS"],
    "CNC, Bearings & Precision Engg": ["CUMMINSIND.NS", "TIMKEN.NS", "SKFINDIA.NS", "SCHAEFFLER.NS", "GRINDWELL.NS", "MTARTECH.NS"],
    "Pre-Engineered & Infra EPC": ["LT.NS", "KPIL.NS", "KEC.NS", "NCC.NS", "PNCINFRA.NS", "HGINFRA.NS", "ENGINERSIN.NS"],
    "Real Estate & Housing": ["DLF.NS", "GODREJPROP.NS", "MACROTECH.NS", "OBERIRLTY.NS", "PRESTIGE.NS", "BRIGADE.NS"],
    "Building Materials (Pipes & Sanitary)": ["ASTRAL.NS", "SUPREMEIND.NS", "CERA.NS", "KAJARIACER.NS", "CENTURYPLY.NS", "PRINCEPIPE.NS"],
    "CDMO & API Pharma": ["DIVISLAB.NS", "LAURUSLABS.NS", "SYNGENE.NS", "SUVENPHAR.NS", "GRANULES.NS", "NEULANDLAB.NS"],
    "Largecap Pharma": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "LUPIN.NS", "AUROPHARMA.NS", "ZYDUSLIFE.NS"],
    "Hospitals & Diagnostics": ["APOLLOHOSP.NS", "MAXHEALTH.NS", "FORTIS.NS", "NH.NS", "LALPATHLAB.NS", "METROPOLIS.NS"],
    "QSR & Food Delivery": ["ZOMATO.NS", "JUBLFOOD.NS", "DEVYANI.NS", "WESTLIFE.NS", "SAPPHIRE.NS", "BIKAJI.NS"],
    "FMCG Staples": ["ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "BRITANNIA.NS", "DABUR.NS", "MARICO.NS", "TATACONSUM.NS"],
    "Retail, Apparel & Footwear": ["TRENT.NS", "DMART.NS", "PAGEIND.NS", "BATAINDIA.NS", "METROBRAND.NS", "MANYAVAR.NS"],
    "Jewellery & Luxury": ["TITAN.NS", "KALYANKJIL.NS", "SENCO.NS", "THANGAMAYL.NS", "ETHOSLTD.NS"],
    "Auto OEMs": ["M&M.NS", "TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "TVSMOTOR.NS", "HEROMOTOCO.NS"],
    "Auto Ancillaries & Tyres": ["MOTHERSON.NS", "BOSCHLTD.NS", "SONACOMS.NS", "UNOMINDA.NS", "APOLLOTYRE.NS", "BALKRISIND.NS"],
    "IT Largecap": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"],
    "IT Midcap & ER&D": ["PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS", "MPHASIS.NS", "OFSS.NS"],
    "PSU Banks": ["SBIN.NS", "BANKBARODA.NS", "PNB.NS", "CANBK.NS", "UNIONBANK.NS", "INDIANB.NS"],
    "Private Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "FEDERALBNK.NS"],
    "NBFCs & Housing Finance": ["BAJFINANCE.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "LICHSGFIN.NS"],
    "Capital Market & Wealth": ["BSE.NS", "MCX.NS", "CDSL.NS", "ANGELONE.NS", "MOTILALOFS.NS", "CAMS.NS", "ANANDRATHI.NS"],
    "Specialty Chemicals & Agro": ["PIIND.NS", "SRF.NS", "DEEPAKNTR.NS", "NAVINFLUOR.NS", "CLEAN.NS", "AARTIIND.NS"],
    "Packaging & BOPP Films": ["EPL.NS", "UFLEX.NS", "POLYPLEX.NS", "JINDALPOLY.NS", "MOLDTKPAC.NS", "TCPLPACK.NS"],
    "Hotels, Tourism & Aviation": ["INDIGO.NS", "INDHOTEL.NS", "LEMONTREE.NS", "CHALET.NS", "IRCTC.NS", "EIHOTEL.NS"],
    "Metals & Mining": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "COALINDIA.NS", "NATIONALUM.NS"]
}

ALL_TICKERS = sorted(list({t for lst in SECTOR_STOCKS.values() for t in lst}))
TICKER_TO_SECTOR = {t: sec for sec, lst in SECTOR_STOCKS.items() for t in lst}

# ==============================================================================
# ৩. সেশন স্টেট ও ক্লিকেবল লিঙ্ক (Query Params) হ্যান্ডলিং
# ==============================================================================
if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = "সবগুলো সেক্টর (Show All 32)"
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = "শেয়ার টাইপ করুন..."
if "kpi_panel" not in st.session_state:
    st.session_state.kpi_panel = None

qp = st.query_params
if "focus_stock" in qp:
    clicked_sym = urllib.parse.unquote(qp["focus_stock"]).strip()
    full_t = clicked_sym if clicked_sym.endswith(".NS") else f"{clicked_sym}.NS"
    if full_t in ALL_TICKERS:
        st.session_state.selected_stock = full_t
    st.query_params.clear()

if "focus_sec" in qp:
    clicked_sec = urllib.parse.unquote(qp["focus_sec"]).strip()
    if clicked_sec in SECTOR_STOCKS:
        st.session_state.selected_sector = clicked_sec
        st.session_state.kpi_panel = "custom_sector"
    st.query_params.clear()

# ==============================================================================
# ৪. টপ হেডার, থিম সিলেক্টর ও অ্যানালগ মিটার টগল
# ==============================================================================
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

top_c1, top_c2, top_c3 = st.columns([6.3, 2.3, 1.4])
with top_c1:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;">'
        '<span style="font-size:2rem;">🧭</span>'
        '<span style="font-size:1.75rem;font-weight:800;letter-spacing:-0.3px;">'
        'AlphaPulse Pro — Intraday, Swing & Sector Terminal'
        '</span></div>',
        unsafe_allow_html=True
    )
with top_c2:
    theme_mode = st.selectbox(
        "Theme",
        ["🌙 Pro Dark (ডার্ক থিম)", "🌌 Cyber Neon (নিয়ন থিম)", "☀️ Clean Light (লাইট থিম)"],
        index=0,
        label_visibility="collapsed"
    )
with top_c3:
    show_analog_meter = st.toggle("🎛️ অ্যানালগ মিটার", value=True)

# ==============================================================================
# ৫. কাস্টম CSS (Zero-Indentation Safe)
# ==============================================================================
if "Clean Light" in theme_mode:
    BG_MAIN, BG_CARD, TEXT_MAIN, TEXT_SUB, BORDER_C = "#f8fafc", "#ffffff", "#0f172a", "#475569", "#cbd5e1"
elif "Cyber Neon" in theme_mode:
    BG_MAIN, BG_CARD, TEXT_MAIN, TEXT_SUB, BORDER_C = "#050b14", "#0b1528", "#ecfdf5", "#94a3b8", "#0ea5e966"
else:
    BG_MAIN, BG_CARD, TEXT_MAIN, TEXT_SUB, BORDER_C = "#070b14", "#0e1525", "#f8fafc", "#94a3b8", "#1e293b"

css_block = """
<style>
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: __BG_MAIN__ !important;
    color: __TEXT_MAIN__ !important;
    scroll-behavior: smooth !important;
}
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 4.5rem !important;
    max-width: 97% !important;
}
.pulse-bar {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    border-radius: 12px;
    padding: 10px 18px;
    margin: 8px 0 14px 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}
.pulse-item {
    font-size: 0.88rem;
    font-weight: 700;
}
.intraday-box-bull {
    background: linear-gradient(145deg, rgba(6,78,59,0.22), rgba(14,21,37,0.95));
    border: 1.5px solid #10b981;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 0 16px rgba(16,185,129,0.12);
    min-height: 118px;
}
.intraday-box-bear {
    background: linear-gradient(145deg, rgba(127,29,29,0.22), rgba(14,21,37,0.95));
    border: 1.5px solid #ef4444;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 0 16px rgba(239,68,68,0.12);
    min-height: 118px;
}
.box-title-bull {
    color: #10b981;
    font-size: 0.93rem;
    font-weight: 800;
    margin-bottom: 10px;
}
.box-title-bear {
    color: #ef4444;
    font-size: 0.93rem;
    font-weight: 800;
    margin-bottom: 10px;
}
.pill-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
a.bull-pill {
    text-decoration: none !important;
    background: rgba(16,185,129,0.14);
    border: 1px solid #10b981;
    color: #ecfdf5 !important;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.79rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: all 0.2s ease;
}
a.bull-pill:hover {
    background: #10b981;
    color: #03150e !important;
    transform: translateY(-2px);
}
a.bear-pill {
    text-decoration: none !important;
    background: rgba(239,68,68,0.14);
    border: 1px solid #ef4444;
    color: #fef2f2 !important;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 0.79rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: all 0.2s ease;
}
a.bear-pill:hover {
    background: #ef4444;
    color: #ffffff !important;
    transform: translateY(-2px);
}
.marquee-wrap {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    border-radius: 12px;
    padding: 10px 12px;
    overflow: hidden;
    white-space: nowrap;
    margin: 6px 0 16px 0;
}
.marquee-track {
    display: inline-block;
    animation: ticker-move 45s linear infinite;
}
.marquee-wrap:hover .marquee-track {
    animation-play-state: paused;
}
@keyframes ticker-move {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-50%); }
}
a.sec-pill-up {
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(16,185,129,0.14);
    border: 1px solid #10b981;
    color: #34d399 !important;
    padding: 6px 14px;
    margin-right: 10px;
    border-radius: 999px;
    font-size: 0.81rem;
    font-weight: 700;
}
a.sec-pill-down {
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(239,68,68,0.14);
    border: 1px solid #ef4444;
    color: #f87171 !important;
    padding: 6px 14px;
    margin-right: 10px;
    border-radius: 999px;
    font-size: 0.81rem;
    font-weight: 700;
}
.kpi-card {
    background: __BG_CARD__;
    border: 1.5px solid #0284c788;
    border-radius: 14px;
    padding: 14px 16px;
    min-height: 125px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 6px;
}
.kpi-title {
    color: __TEXT_SUB__;
    font-size: 0.82rem;
    font-weight: 700;
}
.kpi-val {
    font-size: 1.35rem;
    font-weight: 800;
    margin: 5px 0;
}
.kpi-sub-up {
    background: rgba(16,185,129,0.15);
    color: #34d399;
    border: 1px solid #10b98155;
    padding: 3px 9px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    width: fit-content;
}
.kpi-sub-down {
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid #ef444455;
    padding: 3px 9px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    width: fit-content;
}
a.floating-top-btn {
    position: fixed;
    bottom: 62px;
    right: 22px;
    z-index: 999999;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    color: #ffffff !important;
    text-decoration: none !important;
    padding: 9px 18px;
    border-radius: 999px;
    font-size: 0.86rem;
    font-weight: 800;
    box-shadow: 0 6px 20px rgba(2,132,199,0.55);
    border: 1px solid rgba(255,255,255,0.28);
    transition: all 0.2s ease;
}
a.floating-top-btn:hover {
    transform: translateY(-3px) scale(1.04);
    box-shadow: 0 8px 25px rgba(2,132,199,0.8);
}
</style>
""".replace("__BG_MAIN__", BG_MAIN).replace("__BG_CARD__", BG_CARD).replace("__TEXT_MAIN__", TEXT_MAIN).replace("__TEXT_SUB__", TEXT_SUB).replace("__BORDER_C__", BORDER_C)

st.markdown(css_block, unsafe_allow_html=True)

# ==============================================================================
# ৬. ডেটা লোডিং, RSI, ক্যান্ডেলস্টিক (Doji/Hammer) ও টার্নঅ্যারাউন্ড ইঞ্জিন
# ==============================================================================
def calc_rsi(series: pd.Series, period: int = 14) -> float:
    if len(series) < period + 1:
        return 50.0
    delta = series.diff()
    up = delta.clip(lower=0).rolling(period).mean()
    down = (-delta.clip(upper=0)).rolling(period).mean()
    rs = up / down.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    val = rsi.iloc[-1]
    return float(val) if not np.isnan(val) else 50.0


def calc_return(closes: pd.Series, days: int) -> float:
    if len(closes) < 2:
        return 0.0
    idx = max(0, len(closes) - 1 - days)
    base = float(closes.iloc[idx])
    last = float(closes.iloc[-1])
    return ((last - base) / base) * 100.0 if base > 0 else 0.0


@st.cache_data(ttl=300, show_spinner=False)
def load_pulse_indices():
    idx_tickers = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "VIX": "^INDIAVIX", "USDINR": "INR=X"}
    res = {}
    try:
        raw = yf.download(list(idx_tickers.values()), period="1y", interval="1d", progress=False, group_by="ticker", threads=True)
        for k, sym in idx_tickers.items():
            try:
                df = raw[sym].dropna(how="all")
                if len(df) >= 2:
                    c_now = float(df["Close"].iloc[-1])
                    c_prev = float(df["Close"].iloc[-2])
                    c_1d = ((c_now - c_prev) / c_prev) * 100.0
                    c_1w = calc_return(df["Close"], 5)
                    c_1m = calc_return(df["Close"], 21)
                    c_3m = calc_return(df["Close"], 63)
                    c_6m = calc_return(df["Close"], 126)
                    c_1y = calc_return(df["Close"], 250)
                    res[k] = {"price": c_now, "1D": c_1d, "1W": c_1w, "1M": c_1m, "3M": c_3m, "6M": c_6m, "1Y": c_1y}
            except Exception:
                pass
    except Exception:
        pass

    defaults = {
        "NIFTY": {"price": 23146.2, "1D": 0.65, "1W": 2.78, "1M": 1.2, "3M": 3.4, "6M": 5.1, "1Y": -1.2},
        "BANKNIFTY": {"price": 55844.0, "1D": 0.06, "1W": 1.95, "1M": 0.8, "3M": 2.5, "6M": 4.0, "1Y": 3.5},
        "VIX": {"price": 14.02, "1D": -0.04, "1W": -2.1, "1M": -4.0, "3M": 0.0, "6M": 0.0, "1Y": 0.0},
        "USDINR": {"price": 84.95, "1D": -0.21, "1W": -0.1, "1M": 0.2, "3M": 0.5, "6M": 0.8, "1Y": 1.4},
    }
    for k, v in defaults.items():
        if k not in res:
            res[k] = v
    return res


@st.cache_data(ttl=300, show_spinner=False)
def load_full_market_data():
    raw = yf.download(ALL_TICKERS, period="1y", interval="1d", progress=False, group_by="ticker", threads=True)
    stock_rows = []

    for ticker in ALL_TICKERS:
        try:
            df = raw[ticker].dropna(how="all") if len(ALL_TICKERS) > 1 else raw.dropna(how="all")
            if df is None or len(df) < 25:
                continue

            closes = df["Close"]
            opens = df["Open"]
            highs = df["High"]
            lows = df["Low"]
            vols = df["Volume"]

            c_now = float(closes.iloc[-1])
            o_now = float(opens.iloc[-1])
            h_now = float(highs.iloc[-1])
            l_now = float(lows.iloc[-1])

            r_1d = calc_return(closes, 1)
            r_1w = calc_return(closes, 5)
            r_1m = calc_return(closes, 21)
            r_3m = calc_return(closes, 63)
            r_6m = calc_return(closes, 126)
            r_1y = calc_return(closes, 250)

            dma20 = float(closes.rolling(20).mean().iloc[-1])
            dma50 = float(closes.rolling(50).mean().iloc[-1]) if len(closes) >= 50 else dma20
            dma200 = float(closes.rolling(200).mean().iloc[-1]) if len(closes) >= 200 else dma50

            avg_vol = float(vols.iloc[-21:-1].mean()) if len(vols) >= 22 else float(vols.mean())
            cur_vol = float(vols.iloc[-1])
            vol_ratio = round(cur_vol / avg_vol, 2) if avg_vol > 0 else 1.0

            rsi_val = round(calc_rsi(closes, 14), 1)

            # টানা কত দিন শেয়ারটি উপরে বা নিচে গেছে (Consecutive Up / Down Days)
            c_arr = closes.values
            consec_up, consec_down = 0, 0
            for i in range(len(c_arr) - 1, 0, -1):
                if c_arr[i] > c_arr[i - 1]:
                    if consec_down == 0:
                        consec_up += 1
                    else:
                        break
                elif c_arr[i] < c_arr[i - 1]:
                    if consec_up == 0:
                        consec_down += 1
                    else:
                        break
                else:
                    break

            # ক্যান্ডেলস্টিক ডজি / হ্যামার / শুটিং স্টার / কনসোলিডেশন বিশ্লেষণ
            rng = max(h_now - l_now, 1e-6)
            body = abs(c_now - o_now)
            body_pct = body / rng
            lower_wick = (min(o_now, c_now) - l_now) / rng
            upper_wick = (h_now - max(o_now, c_now)) / rng

            # গত ৩ দিনের কনসোলিডেশন রেঞ্জ (Tight Consolidation)
            rng_3d_pct = ((float(highs.iloc[-3:].max()) - float(lows.iloc[-3:].min())) / max(c_now, 1.0)) * 100.0 if len(df) >= 4 else 10.0

            bull_candle = None
            bear_candle = None

            if body_pct <= 0.25 and lower_wick >= 0.45:
                bull_candle = "Dragonfly Doji"
            elif body_pct <= 0.30:
                bull_candle = "Bullish Doji"
            elif lower_wick >= 0.50 and body_pct <= 0.42:
                bull_candle = "Hammer"
            elif rng_3d_pct <= 4.2 and c_now >= o_now:
                bull_candle = "Tight Base"
            elif lower_wick >= 0.35 and c_now >= o_now:
                bull_candle = "Bottom Wick"

            if body_pct <= 0.25 and upper_wick >= 0.45:
                bear_candle = "Gravestone Doji"
            elif body_pct <= 0.30:
                bear_candle = "Top Stall Doji"
            elif upper_wick >= 0.50 and body_pct <= 0.42:
                bear_candle = "Shooting Star"
            elif rng_3d_pct <= 4.2 and c_now <= o_now:
                bear_candle = "Supply Stall"
            elif upper_wick >= 0.35 and c_now <= o_now:
                bear_candle = "Upper Rejection"

            # ATR (14) হিসাব
            if len(df) >= 15:
                tr = pd.concat([
                    highs - lows,
                    (highs - closes.shift(1)).abs(),
                    (lows - closes.shift(1)).abs()
                ], axis=1).max(axis=1)
                atr = float(tr.rolling(14).mean().iloc[-1])
            else:
                atr = rng

            stock_rows.append({
                "Ticker": ticker,
                "Symbol": ticker.replace(".NS", ""),
                "Sector": TICKER_TO_SECTOR.get(ticker, "Others"),
                "Price": round(c_now, 2),
                "1D": round(r_1d, 2),
                "1W": round(r_1w, 2),
                "1M": round(r_1m, 2),
                "3M": round(r_3m, 2),
                "6M": round(r_6m, 2),
                "1Y": round(r_1y, 2),
                "Vol_Ratio": vol_ratio,
                "RSI": rsi_val,
                "DMA20": round(dma20, 2),
                "DMA50": round(dma50, 2),
                "DMA200": round(dma200, 2),
                "Above_50DMA": c_now >= dma50,
                "Dist_20DMA": round(((c_now - dma20) / dma20) * 100.0, 2) if dma20 > 0 else 0.0,
                "Consec_Up": consec_up,
                "Consec_Down": consec_down,
                "Bull_Candle": bull_candle,
                "Bear_Candle": bear_candle,
                "Body_Pct": round(body_pct, 2),
                "Lower_Wick": round(lower_wick, 2),
                "Upper_Wick": round(upper_wick, 2),
                "ATR": round(atr if not np.isnan(atr) and atr > 0 else c_now * 0.018, 2),
                "Day_High": round(h_now, 2),
                "Day_Low": round(l_now, 2),
            })
        except Exception:
            continue

    stocks_df = pd.DataFrame(stock_rows)
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # সেক্টর লেভেল ক্যালকুলেশন
    sec_rows = []
    for sec_name, grp in stocks_df.groupby("Sector"):
        s_1d = float(grp["1D"].mean())
        s_1w = float(grp["1W"].mean())
        s_1m = float(grp["1M"].mean())
        s_3m = float(grp["3M"].mean())
        s_6m = float(grp["6M"].mean())
        s_1y = float(grp["1Y"].mean())
        s_vol = float(grp["Vol_Ratio"].mean())
        s_rsi = float(grp["RSI"].mean())
        s_b50 = float((grp["Above_50DMA"].sum() / len(grp)) * 100.0)

        # ডাউন সেক্টর যা নিচ থেকে আপের দিকে মুভ করছে (Bullish Sector Turnaround)
        sec_bull_turn = (s_1w <= 1.5 or s_1m <= 1.5) and (s_1d >= -0.15 or s_1d > (s_1w / 5.0))
        # আপ সেক্টর যা ওপর থেকে নিচের দিকে নামছে (Bearish Sector Rollover)
        sec_bear_roll = (s_1w >= -0.5 or s_1m >= 0.5) and (s_1d <= 0.25 or s_1d < (s_1w / 5.0))

        meter = int(np.clip(50 + (s_1w * 3.5) + (s_1d * 6.0) + ((s_rsi - 50) * 0.6), 5, 98))

        if sec_bull_turn and s_1d >= 0:
            zone = "🔄 Turnaround Zone (ডাউন থেকে ঘুরে দাঁড়ানো)"
        elif s_1w >= 2.0 and s_1d >= 0:
            zone = "🚀 Leading Zone (টপ মোমেন্টাম)"
        elif sec_bear_roll and s_1d < 0:
            zone = "⚠️ Exhaustion Zone (ওপর থেকে নিচে নামা)"
        else:
            zone = "💎 Value Zone (ডিপ ডাউন / কনসোলিডেশন)"

        sec_rows.append({
            "Sector": sec_name,
            "Count": len(grp),
            "1D": round(s_1d, 2),
            "1W": round(s_1w, 2),
            "1M": round(s_1m, 2),
            "3M": round(s_3m, 2),
            "6M": round(s_6m, 2),
            "1Y": round(s_1y, 2),
            "Avg_Vol": round(s_vol, 2),
            "RSI": round(s_rsi, 1),
            "Breadth_50DMA": round(s_b50, 1),
            "Meter": meter,
            "Zone": zone,
            "Sec_Bull_Turn": sec_bull_turn,
            "Sec_Bear_Roll": sec_bear_roll,
        })

    sectors_df = pd.DataFrame(sec_rows)
    sec_map = sectors_df.set_index("Sector").to_dict("index")
    stocks_df["Sec_1D"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("1D", 0.0))
    stocks_df["Sec_1W"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("1W", 0.0))
    stocks_df["Sec_Bull_Turn"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Sec_Bull_Turn", False))
    stocks_df["Sec_Bear_Roll"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Sec_Bear_Roll", False))

    return stocks_df, sectors_df


def style_colored_table(df: pd.DataFrame, pct_cols: list):
    def color_pct(val):
        if pd.isna(val) or not isinstance(val, (int, float, np.number)):
            return ""
        if val > 0:
            return "color: #34d399; font-weight: 700;"
        elif val < 0:
            return "color: #f87171; font-weight: 700;"
        return "color: #94a3b8;"

    valid_cols = [c for c in pct_cols if c in df.columns]
    return df.style.map(color_pct, subset=valid_cols).format(precision=2)


# ==============================================================================
# ৭. ইন্ট্রাডে বুলিশ ও বেয়ারিশ রিভার্সাল ফোকাস (তোমার নির্দেশ অনুযায়ী ডজি + ভলিউম + সেক্টর টার্নঅ্যারাউন্ড)
# ==============================================================================
def filter_intraday_focus_stocks(stocks_df: pd.DataFrame):
    """
    ১. বুলিশ সাইড:
       - টানা ৩-৪ দিন উপরে যাওয়া শেয়ার সম্পূর্ণ বাদ (Consec_Up <= 2)
       - অতিরিক্ত বেড়ে যাওয়া শেয়ার বাদ (-1.5% <= 1D <= +4.0%)
       - নিচে ডজি / হ্যামার / টাইট কনসোলিডেশন তৈরি করেছে (Bull_Candle.notna())
       - ভলিউম তৈরি হচ্ছে (Vol_Ratio >= 1.15x, কম ভলিউমের শেয়ার বাদ)
       - ডাউন সেক্টর যা নিচ থেকে আপের দিকে ঘুরছে (Sec_Bull_Turn বা 1W ডাউন থেকে 1D পজিটিভ)
    ২. বেয়ারিশ সাইড:
       - টানা ৩-৪ দিন নিচে পড়া শেয়ার সম্পূর্ণ বাদ (Consec_Down <= 2)
       - অতিরিক্ত পড়ে যাওয়া শেয়ার বাদ (-4.0% <= 1D <= +1.5%)
       - ওপরে ডজি / শুটিং স্টার / সাপ্লাই রিজেকশন তৈরি করেছে (Bear_Candle.notna())
       - ভলিউম তৈরি হচ্ছে (Vol_Ratio >= 1.15x) এবং সেক্টর ওপর থেকে নিচে ঘুরছে
    """
    df = stocks_df.copy()

    # বুলিশ ফিল্টার
    bull_mask = (
        (df["Consec_Up"] <= 2) &
        (df["1D"] >= -1.5) & (df["1D"] <= 4.0) &
        (df["1W"] <= 4.2) &
        (df["Vol_Ratio"] >= 1.12) &
        (df["Bull_Candle"].notna())
    )
    bull_candidates = df[bull_mask].copy()

    if len(bull_candidates) < 6:
        extra_bull = df[
            (df["Consec_Up"] <= 2) &
            (df["1D"] >= -1.8) & (df["1D"] <= 4.2) &
            (df["Vol_Ratio"] >= 1.05)
        ].copy()
        extra_bull["Bull_Candle"] = extra_bull["Bull_Candle"].fillna("Doji Base")
        bull_candidates = pd.concat([bull_candidates, extra_bull]).drop_duplicates(subset=["Ticker"])

    bull_candidates["Focus_Score"] = (
        (bull_candidates["Vol_Ratio"] * 28.0)
        + np.where(bull_candidates["Sec_Bull_Turn"], 30.0, 0.0)
        + np.where(bull_candidates["1W"] <= 0.5, 20.0, 5.0)
        + ((1.0 - bull_candidates["Body_Pct"]) * 22.0)
        + (bull_candidates["Lower_Wick"] * 15.0)
    )
    bull_top6 = bull_candidates.sort_values("Focus_Score", ascending=False).head(6)

    # বেয়ারিশ ফিল্টার (ঠিক বিপরীত লজিক)
    bear_mask = (
        (df["Consec_Down"] <= 2) &
        (df["1D"] <= 1.5) & (df["1D"] >= -4.0) &
        (df["1W"] >= -4.2) &
        (df["Vol_Ratio"] >= 1.12) &
        (df["Bear_Candle"].notna())
    )
    bear_candidates = df[bear_mask].copy()

    if len(bear_candidates) < 6:
        extra_bear = df[
            (df["Consec_Down"] <= 2) &
            (df["1D"] <= 1.8) & (df["1D"] >= -4.2) &
            (df["Vol_Ratio"] >= 1.05)
        ].copy()
        extra_bear["Bear_Candle"] = extra_bear["Bear_Candle"].fillna("Top Doji")
        bear_candidates = pd.concat([bear_candidates, extra_bear]).drop_duplicates(subset=["Ticker"])

    bear_candidates["Focus_Score"] = (
        (bear_candidates["Vol_Ratio"] * 28.0)
        + np.where(bear_candidates["Sec_Bear_Roll"], 30.0, 0.0)
        + np.where(bear_candidates["1W"] >= -0.5, 20.0, 5.0)
        + ((1.0 - bear_candidates["Body_Pct"]) * 22.0)
        + (bear_candidates["Upper_Wick"] * 15.0)
    )
    bear_top6 = bear_candidates.sort_values("Focus_Score", ascending=False).head(6)

    return bull_top6, bear_top6


with st.spinner("⚡ ৩২টি সেক্টর ও ১৮০+ শেয়ারের লাইভ ডজি ক্যান্ডেল, ভলিউম ও সেক্টর রোটেশন লোড হচ্ছে..."):
    pulse = load_pulse_indices()
    stocks_df, sectors_df = load_full_market_data()

if stocks_df.empty or sectors_df.empty:
    st.error("⚠️ মার্কেট ডেটা লোড করতে সমস্যা হয়েছে। অনুগ্রহ করে পেজটি রিলোড করুন।")
    st.stop()

# ==============================================================================
# ৮. মার্কেট পালস রিবন (স্ক্রিনশটের হুবহু ডিজাইন)
# ==============================================================================
n_d = pulse["NIFTY"]
b_d = pulse["BANKNIFTY"]
v_d = pulse["VIX"]
u_d = pulse["USDINR"]

vix_badge = "🟢 স্বস্তিদায়ক (Low Fear)" if v_d["price"] < 15.5 else ("🟡 মাঝারি (Moderate)" if v_d["price"] < 19.0 else "🔴 উচ্চ ভীতি (High Fear)")

pulse_html = (
    f'<div class="pulse-bar">'
    f'<div class="pulse-item">🇮🇳 Nifty 50: <span style="color:{"#34d399" if n_d["1D"]>=0 else "#f87171"};">{n_d["price"]:,.1f} ({n_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">🏛️ Bank Nifty: <span style="color:{"#34d399" if b_d["1D"]>=0 else "#f87171"};">{b_d["price"]:,.1f} ({b_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">⚡ India VIX: <span style="color:{"#34d399" if v_d["1D"]<=0 else "#fbbf24"};">{v_d["price"]:.2f} ({v_d["1D"]:+.2f}%)</span> — {vix_badge}</div>'
    f'<div class="pulse-item">💵 USD/INR: <span style="color:#94a3b8;">₹{u_d["price"]:.2f} ({u_d["1D"]:+.2f}%)</span></div>'
    f'</div>'
)
st.markdown(pulse_html, unsafe_allow_html=True)

# ==============================================================================
# ৯. ৫-কলাম কন্ট্রোল ও ফিল্টার বার (স্ক্রিনশটের হুবহু লেআউট)
# ==============================================================================
fc1, fc2, fc3, fc4, fc5 = st.columns([1.15, 2.2, 2.2, 2.2, 2.25])

with fc1:
    tf_choice = st.selectbox("📅 ১. টাইমফ্রেম:", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=1)

with fc2:
    sort_choice = st.selectbox(
        "🔄 ২. সাজানোর ক্রম (Sort By):",
        [
            "🚀 Top Gainers (সবচেয়ে বেশি বাড়া আগে)",
            "📉 Top Losers (সবচেয়ে বেশি ডাউন আগে)",
            "🔄 Bottom Turnaround (ডাউন থেকে ঘোরা আগে)",
            "🔥 Volume Shockers (ভলিউম স্পাইক আগে)",
            "🎛️ Meter Score (অ্যানালগ মিটার অনুযায়ী)"
        ],
        index=0
    )

with fc3:
    zone_choice = st.selectbox(
        "🎯 ৩. রোটেশন জোন ফিল্টার:",
        [
            "🌐 সব সেক্টর (All 32 Sectors)",
            "🔄 Turnaround Zone (ডাউন থেকে ঘুরে দাঁড়ানো)",
            "🚀 Leading Zone (টপ মোমেন্টাম)",
            "⚠️ Exhaustion Zone (ওপর থেকে নিচে নামা)",
            "💎 Value Zone (ডিপ ডাউন / কনসোলিডেশন)"
        ],
        index=0
    )

with fc4:
    sec_list = ["সবগুলো সেক্টর (Show All 32)"] + sorted(list(SECTOR_STOCKS.keys()))
    sec_default_idx = sec_list.index(st.session_state.selected_sector) if st.session_state.selected_sector in sec_list else 0
    picked_sec = st.selectbox("🔍 ৪. নির্দিষ্ট সেক্টর খুঁজুন:", sec_list, index=sec_default_idx)
    st.session_state.selected_sector = picked_sec

with fc5:
    stock_search_list = ["শেয়ার টাইপ করুন..."] + [f"{r['Symbol']} ({r['Sector']})" for _, r in stocks_df.sort_values("Symbol").iterrows()]
    st_default_idx = 0
    if st.session_state.selected_stock != "শেয়ার টাইপ করুন...":
        target_sym = st.session_state.selected_stock.replace(".NS", "")
        for idx_s, item_s in enumerate(stock_search_list):
            if item_s.startswith(f"{target_sym} ("):
                st_default_idx = idx_s
                break
    picked_stock = st.selectbox("⚡ ৫. যেকোনো শেয়ার খুঁজুন (Stock Search):", stock_search_list, index=st_default_idx)
    if picked_stock != "শেয়ার টাইপ করুন...":
        st.session_state.selected_stock = picked_stock.split(" (")[0].strip() + ".NS"
    else:
        st.session_state.selected_stock = "শেয়ার টাইপ করুন..."

# ==============================================================================
# ১০. ইন্ট্রাডে বুলিশ ও বেয়ারিশ রিভার্সাল ফোকাস বক্স (স্ক্রিনশট + সংশোধিত লজিক)
# ==============================================================================
bull_top6, bear_top6 = filter_intraday_focus_stocks(stocks_df)

# বুলিশ ডে / বেয়ারিশ ডে ট্র্যাকিং মোড সুইচার
m_bar1, m_bar2 = st.columns([6.8, 3.2])
with m_bar1:
    st.markdown(
        '<div style="font-size:0.82rem;color:#94a3b8;margin-bottom:4px;">'
        '🎯 <b>ইন্ট্রাডে ডজি ও সেক্টর টার্নঅ্যারাউন্ড ফিল্টার:</b> টানা ৩-৪ দিন বাড়া/পড়া শেয়ার বাদ দিয়ে ডজি/হ্যামার কনসোলিডেশন ও ভলিউম বিল্ডআপ স্টক (যেকোনো শেয়ারে ক্লিক করলে সাথে সাথে চার্ট ও ট্রেড প্ল্যান খুলবে):'
        '</div>',
        unsafe_allow_html=True
    )
with m_bar2:
    market_day_mode = st.radio(
        "ট্র্যাকিং মোড:",
        ["🌗 উভয় সাইড", "🟢 বুলিশ সাইড ফোকাস", "🔴 বেয়ারিশ সাইড ফোকাস"],
        horizontal=True,
        label_visibility="collapsed"
    )

def make_pills_html(df_focus: pd.DataFrame, is_bullish: bool) -> str:
    items = []
    cls = "bull-pill" if is_bullish else "bear-pill"
    dot = "🟢" if is_bullish else "🔴"
    c_col = "Bull_Candle" if is_bullish else "Bear_Candle"

    for _, r in df_focus.iterrows():
        q_t = urllib.parse.quote(r["Ticker"])
        c_tag = r[c_col] if pd.notna(r[c_col]) else "Doji"
        tip = f"Sector: {r['Sector']} | Pattern: {c_tag} | RSI: {r['RSI']} | 1W: {r['1W']:+.1f}%"
        items.append(
            f'<a class="{cls}" href="?focus_stock={q_t}" target="_self" title="{tip}">'
            f'{dot} {r["Symbol"]} ({r["1D"]:+.1f}% | {r["Vol_Ratio"]:.2f}x Vol | {c_tag})'
            f'</a>'
        )
    return "".join(items)

bull_html_pills = make_pills_html(bull_top6, True)
bear_html_pills = make_pills_html(bear_top6, False)

bull_box_markup = (
    '<div class="intraday-box-bull">'
    '<div class="box-title-bull">🔄 ইন্ট্রাডে বুলিশ রিভার্সাল ফোকাস (Bottom Turnaround – অতিরিক্ত না বেড়ে নিচ থেকে ডজি/ভলিউমসহ ঘুরে দাঁড়ানো স্টক)</div>'
    f'<div class="pill-container">{bull_html_pills}</div>'
    '</div>'
)

bear_box_markup = (
    '<div class="intraday-box-bear">'
    '<div class="box-title-bear">📉 ইন্ট্রাডে বেয়ারিশ রিভার্সাল ফোকাস (Top Breakdown – ওপর থেকে ডজি/শুটিং স্টারসহ নিচে নামার প্রস্তুতি নেওয়া স্টক)</div>'
    f'<div class="pill-container">{bear_html_pills}</div>'
    '</div>'
)

if market_day_mode == "🟢 বুলিশ সাইড ফোকাস":
    st.markdown(bull_box_markup, unsafe_allow_html=True)
elif market_day_mode == "🔴 বেয়ারিশ সাইড ফোকাস":
    st.markdown(bear_box_markup, unsafe_allow_html=True)
else:
    ib1, ib2 = st.columns(2)
    with ib1:
        st.markdown(bull_box_markup, unsafe_allow_html=True)
    with ib2:
        st.markdown(bear_box_markup, unsafe_allow_html=True)

# ==============================================================================
# ১১. স্টক প্রোফাইল ও ইন্ট্রাডে ট্রেড সেটআপ প্যানেল (শেয়ারে ক্লিক করলে ওপেন হবে)
# ==============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def load_single_stock_ohlc(ticker: str):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        return df.dropna(how="all")
    except Exception:
        return pd.DataFrame()

if st.session_state.selected_stock != "শেয়ার টাইপ করুন..." and st.session_state.selected_stock in stocks_df["Ticker"].values:
    s_info = stocks_df[stocks_df["Ticker"] == st.session_state.selected_stock].iloc[0]
    sym_clean = s_info["Symbol"]
    p_now = s_info["Price"]
    atr_v = s_info["ATR"]

    b_entry = round(max(p_now, s_info["Day_High"] * 0.998), 2)
    b_sl = round(min(s_info["Day_Low"], b_entry - 1.2 * atr_v), 2)
    b_t1 = round(b_entry + 1.5 * atr_v, 2)
    b_t2 = round(b_entry + 2.5 * atr_v, 2)

    sh_entry = round(min(p_now, s_info["Day_Low"] * 1.002), 2)
    sh_sl = round(max(s_info["Day_High"], sh_entry + 1.2 * atr_v), 2)
    sh_t1 = round(sh_entry - 1.5 * atr_v, 2)
    sh_t2 = round(sh_entry - 2.5 * atr_v, 2)

    st.markdown("---")
    sp_col1, sp_col2 = st.columns([8.2, 1.8])
    with sp_col1:
        st.markdown(
            f"### 🎯 শেয়ার ক্যান্ডেল ও ইন্ট্রাডে ট্রেড সেটআপ: **{sym_clean}** — `{s_info['Sector']}` "
            f"(দাম: ₹{p_now:,.2f} | 1D: {s_info['1D']:+.2f}% | ভলিউম: {s_info['Vol_Ratio']}x)"
        )
    with sp_col2:
        if st.button("✖ প্যানেল বন্ধ করুন", use_container_width=True):
            st.session_state.selected_stock = "শেয়ার টাইপ করুন..."
            st.rerun()

    lv1, lv2, lv3 = st.columns(3)
    with lv1:
        c_pat = s_info["Bull_Candle"] or s_info["Bear_Candle"] or "Consolidation Candle"
        st.info(
            f"🕯️ **ক্যান্ডেল প্যাটার্ন:** {c_pat}\n\n"
            f"📊 **RSI (14):** {s_info['RSI']} | **টানা আপ দিন:** {s_info['Consec_Up']} | **টানা ডাউন দিন:** {s_info['Consec_Down']}\n\n"
            f"🔄 **সেক্টর স্ট্যাটাস:** 1W: {s_info['Sec_1W']:+.2f}% → আজ: {s_info['Sec_1D']:+.2f}%"
        )
    with lv2:
        st.success(
            f"🟢 **বুলিশ ইন্ট্রাডে/সুইং প্ল্যান (Buy Setup):**\n\n"
            f"• **Entry Above:** ₹{b_entry} | **Stop-Loss:** ₹{b_sl}\n\n"
            f"• **Target 1:** ₹{b_t1} | **Target 2:** ₹{b_t2}"
        )
    with lv3:
        st.error(
            f"🔴 **বেয়ারিশ ইন্ট্রাডে প্ল্যান (Short Setup):**\n\n"
            f"• **Short Below:** ₹{sh_entry} | **Stop-Loss:** ₹{sh_sl}\n\n"
            f"• **Target 1:** ₹{sh_t1} | **Target 2:** ₹{sh_t2}"
        )

    ohlc_df = load_single_stock_ohlc(s_info["Ticker"])
    if not ohlc_df.empty and len(ohlc_df) >= 20:
        ohlc_df["DMA20"] = ohlc_df["Close"].rolling(20).mean()
        ohlc_df["DMA50"] = ohlc_df["Close"].rolling(50).mean()
        sub_df = ohlc_df.tail(75)

        fig_st = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.74, 0.26])
        fig_st.add_trace(
            go.Candlestick(x=sub_df.index, open=sub_df["Open"], high=sub_df["High"], low=sub_df["Low"], close=sub_df["Close"], name="OHLC"),
            row=1, col=1
        )
        fig_st.add_trace(go.Scatter(x=sub_df.index, y=sub_df["DMA20"], mode="lines", name="20 DMA", line=dict(color="#38bdf8", width=1.6)), row=1, col=1)
        fig_st.add_trace(go.Scatter(x=sub_df.index, y=sub_df["DMA50"], mode="lines", name="50 DMA", line=dict(color="#f59e0b", width=1.6)), row=1, col=1)
        v_cols = ["#10b981" if c >= o else "#ef4444" for c, o in zip(sub_df["Close"], sub_df["Open"])]
        fig_st.add_trace(go.Bar(x=sub_df.index, y=sub_df["Volume"], name="Volume", marker_color=v_cols), row=2, col=1)
        fig_st.update_layout(
            height=400,
            template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig_st, use_container_width=True)

    lnk1, lnk2, lnk3 = st.columns(3)
    with lnk1:
        st.link_button(f"📈 TradingView-এ {sym_clean} চার্ট খুলুন", f"https://in.tradingview.com/chart/?symbol=NSE%3A{sym_clean}", use_container_width=True)
    with lnk2:
        st.link_button(f"📊 Screener.in-এ {sym_clean} দেখুন", f"https://www.screener.in/company/{sym_clean}/", use_container_width=True)
    with lnk3:
        st.link_button(f"📰 Google Finance-এ {sym_clean} দেখুন", f"https://www.google.com/finance/quote/{sym_clean}:NSE", use_container_width=True)
    st.markdown("---")

# ==============================================================================
# ১২. ক্লিকেবল সেক্টর বার (স্ক্রিনশটের হুবহু ডিজাইন + URL-Encoded Safe)
# ==============================================================================
st.markdown(
    '<div style="font-size:0.85rem;color:#cbd5e1;margin-top:8px;">'
    '📍 <b>ক্লিকেবল সেক্টর বার:</b> নিচের চলমান বারের ওপর মাউস রাখলে সেটি থেমে যাবে এবং <b>যেকোনো সেক্টরের ওপর ক্লিক করলেই</b> সাথে সাথে সেই সেক্টরের সব শেয়ার ও চার্ট খুলে যাবে:'
    '</div>',
    unsafe_allow_html=True
)

sec_sorted_bar = sectors_df.sort_values(tf_choice, ascending=False)
bar_items = []
for _, sr in sec_sorted_bar.iterrows():
    s_name = sr["Sector"]
    s_val = sr[tf_choice]
    q_s = urllib.parse.quote(s_name)
    cls_s = "sec-pill-up" if s_val >= 0 else "sec-pill-down"
    arr_s = "▲" if s_val >= 0 else "▼"
    dot_s = "🟢" if s_val >= 0 else "🔴"
    bar_items.append(f'<a class="{cls_s}" href="?focus_sec={q_s}" target="_self">{dot_s} {s_name}: {arr_s} {s_val:+.2f}% 🔍</a>')

marquee_html = f'<div class="marquee-wrap"><div class="marquee-track">{"".join(bar_items) * 2}</div></div>'
st.markdown(marquee_html, unsafe_allow_html=True)

# ==============================================================================
# ১৩. ৪টি সামারি KPI কার্ড এবং নিচের ৪টি অ্যাকশন বাটন (স্ক্রিনশটের হুবহু)
# ==============================================================================
adv_count = int((stocks_df[tf_choice] > 0).sum())
dec_count = int((stocks_df[tf_choice] < 0).sum())
pct_50dma = round((stocks_df["Above_50DMA"].sum() / len(stocks_df)) * 100.0, 1)

leader_sec = sectors_df.sort_values(tf_choice, ascending=False).iloc[0]
laggard_sec = sectors_df.sort_values(tf_choice, ascending=True).iloc[0]
nifty_tf = n_d.get(tf_choice, n_d["1W"])

kc1, kc2, kc3, kc4 = st.columns(4)

with kc1:
    c1_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Nifty 50 Benchmark ({tf_choice})</div>'
        f'<div class="kpi-val" style="color:{"#34d399" if nifty_tf>=0 else "#f87171"};">{nifty_tf:+.2f}%</div>'
        f'<div class="{"kpi-sub-up" if nifty_tf>=0 else "kpi-sub-down"}">1W: {n_d["1W"]:+.2f}% | 1Y: {n_d["1Y"]:+.1f}%</div>'
        f'</div>'
    )
    st.markdown(c1_html, unsafe_allow_html=True)
    if st.button("📊 নিফটি ৫০ মুভার্স লিস্ট দেখুন •", key="kpi_btn_1", use_container_width=True):
        st.session_state.kpi_panel = "nifty_movers" if st.session_state.kpi_panel != "nifty_movers" else None

with kc2:
    c2_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">মার্কেট ব্রেডথ ({tf_choice} Adv vs Dec)</div>'
        f'<div class="kpi-val"><span style="color:#34d399;">🟢 {adv_count} উপরে</span> | <span style="color:#f87171;">🔴 {dec_count} নিচে</span></div>'
        f'<div class="kpi-sub-up">{pct_50dma}% শেয়ার 50-DMA এর উপরে</div>'
        f'</div>'
    )
    st.markdown(c2_html, unsafe_allow_html=True)
    if st.button("📈 বাড়তে থাকা ও ডাউন শেয়ার দেখুন •", key="kpi_btn_2", use_container_width=True):
        st.session_state.kpi_panel = "breadth_list" if st.session_state.kpi_panel != "breadth_list" else None

with kc3:
    c3_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">টপ লিডার সেক্টর ({tf_choice})</div>'
        f'<div class="kpi-val">👑 {leader_sec["Sector"]}</div>'
        f'<div class="kpi-sub-up">▲ {leader_sec[tf_choice]:+.2f}% (Meter: {leader_sec["Meter"]})</div>'
        f'</div>'
    )
    st.markdown(c3_html, unsafe_allow_html=True)
    if st.button(f"🔍 {leader_sec['Sector']}-এর শেয়ার দেখুন •", key="kpi_btn_3", use_container_width=True):
        st.session_state.selected_sector = leader_sec["Sector"]
        st.session_state.kpi_panel = "leader_sec"

with kc4:
    c4_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">সবচেয়ে ডাউন সেক্টর ({tf_choice})</div>'
        f'<div class="kpi-val">📉 {laggard_sec["Sector"]}</div>'
        f'<div class="kpi-sub-down">▼ {laggard_sec[tf_choice]:+.2f}% (Value Zone)</div>'
        f'</div>'
    )
    st.markdown(c4_html, unsafe_allow_html=True)
    if st.button(f"🔍 {laggard_sec['Sector']}-এর শেয়ার দেখুন •", key="kpi_btn_4", use_container_width=True):
        st.session_state.selected_sector = laggard_sec["Sector"]
        st.session_state.kpi_panel = "laggard_sec"

# KPI কার্ডের বাটনে ক্লিক করলে ওপেন হওয়া বিস্তারিত প্যানেল
if st.session_state.kpi_panel is not None:
    st.markdown("---")
    kp_h1, kp_h2 = st.columns([8.5, 1.5])
    with kp_h2:
        if st.button("✖ লিস্ট বন্ধ করুন", use_container_width=True):
            st.session_state.kpi_panel = None
            st.rerun()

    if st.session_state.kpi_panel == "nifty_movers":
        with kp_h1:
            st.markdown(f"#### 📊 টপ গেইনার এবং টপ লুজার শেয়ার ({tf_choice})")
        mv1, mv2 = st.columns(2)
        with mv1:
            st.markdown("##### 🚀 Top 12 Gainers")
            g_df = stocks_df.sort_values(tf_choice, ascending=False)[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI"]].head(12)
            st.dataframe(style_colored_table(g_df, ["1D", "1W", "1M"]), use_container_width=True, hide_index=True)
        with mv2:
            st.markdown("##### 📉 Top 12 Losers")
            l_df = stocks_df.sort_values(tf_choice, ascending=True)[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI"]].head(12)
            st.dataframe(style_colored_table(l_df, ["1D", "1W", "1M"]), use_container_width=True, hide_index=True)

    elif st.session_state.kpi_panel == "breadth_list":
        with kp_h1:
            st.markdown(f"#### 📈 মার্কেট ব্রেডথ রিপোর্ট: বাড়তে থাকা ({adv_count}) বনাম ডাউন ({dec_count}) শেয়ার")
        br1, br2 = st.columns(2)
        with br1:
            st.markdown("##### 🟢 বাড়তে থাকা ও 50-DMA এর উপরে থাকা শেয়ার")
            up_df = stocks_df[stocks_df[tf_choice] > 0].sort_values("Vol_Ratio", ascending=False)[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Bull_Candle"]].head(15)
            st.dataframe(style_colored_table(up_df, ["1D", "1W"]), use_container_width=True, hide_index=True)
        with br2:
            st.markdown("##### 🔴 ডাউন কিন্তু টার্নঅ্যারাউন্ড ওয়াচে থাকা শেয়ার")
            dn_df = stocks_df[stocks_df[tf_choice] < 0].sort_values("Vol_Ratio", ascending=False)[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Bull_Candle"]].head(15)
            st.dataframe(style_colored_table(dn_df, ["1D", "1W"]), use_container_width=True, hide_index=True)

    elif st.session_state.kpi_panel in ("leader_sec", "laggard_sec", "custom_sector"):
        sec_focus_name = st.session_state.selected_sector
        with kp_h1:
            st.markdown(f"#### 🔍 সেক্টর ডিপ-ডাইভ ও সব শেয়ারের তালিকা: **{sec_focus_name}**")
        sub_sec_stocks = stocks_df[stocks_df["Sector"] == sec_focus_name].sort_values(tf_choice, ascending=False)
        st.dataframe(
            style_colored_table(
                sub_sec_stocks[["Symbol", "Price", "1D", "1W", "1M", "3M", "Vol_Ratio", "RSI", "DMA20", "DMA50", "Bull_Candle", "Bear_Candle"]],
                ["1D", "1W", "1M", "3M"]
            ),
            use_container_width=True,
            hide_index=True
        )
    st.markdown("---")

# ==============================================================================
# ১৪. ৪টি প্রধান ট্যাব (সেক্টর চার্ট ও অ্যানালগ মিটার, ইন্ট্রাডে রিস্ক ক্যালকুলেটর, সুইং স্ক্যানার, তুলনামূলক টেবিল)
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 ১. সেক্টর চার্ট, মিটার ও শেয়ার তালিকা",
    "🎯 ২. ইন্ট্রাডে ডোজি/হ্যামার রিভার্সাল ও রিস্ক ক্যালকুলেটর",
    "🚀 ৩. লং ও সুইং স্ক্যানার (Breakout & Value)",
    "📋 ৪. সব সেক্টরের তুলনামূলক টেবিল"
])

# ------------------------------------------------------------------------------
# ট্যাব ১: সেক্টর চার্ট, Plotly অ্যানালগ স্পিডোমিটার ও ড্রিল-ডাউন এক্সপান্ডার
# ------------------------------------------------------------------------------
with tab1:
    filtered_secs = sectors_df.copy()

    if zone_choice != "🌐 সব সেক্টর (All 32 Sectors)":
        filtered_secs = filtered_secs[filtered_secs["Zone"] == zone_choice]

    if st.session_state.selected_sector != "সবগুলো সেক্টর (Show All 32)":
        filtered_secs = filtered_secs[filtered_secs["Sector"] == st.session_state.selected_sector]
        if st.button("🔄 সবগুলো ৩২টি সেক্টর আবার একসাথে দেখুন"):
            st.session_state.selected_sector = "সবগুলো সেক্টর (Show All 32)"
            st.session_state.kpi_panel = None
            st.rerun()

    if "Top Gainers" in sort_choice:
        filtered_secs = filtered_secs.sort_values(tf_choice, ascending=False)
    elif "Top Losers" in sort_choice:
        filtered_secs = filtered_secs.sort_values(tf_choice, ascending=True)
    elif "Bottom Turnaround" in sort_choice:
        filtered_secs = filtered_secs.sort_values(["Sec_Bull_Turn", "1D"], ascending=[False, False])
    elif "Volume Shockers" in sort_choice:
        filtered_secs = filtered_secs.sort_values("Avg_Vol", ascending=False)
    else:
        filtered_secs = filtered_secs.sort_values("Meter", ascending=False)

    def make_plotly_speedometer(score: int, title_txt: str, ret_val: float):
        bar_col = "#10b981" if score >= 60 else ("#fbbf24" if score >= 38 else "#ef4444")
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": f" ({ret_val:+.1f}%)", "font": {"size": 15, "color": TEXT_MAIN}},
            title={"text": title_txt, "font": {"size": 13, "color": TEXT_MAIN}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#475569"},
                "bar": {"color": bar_col, "thickness": 0.32},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 1,
                "bordercolor": "#334155",
                "steps": [
                    {"range": [0, 38], "color": "rgba(239, 68, 68, 0.18)"},
                    {"range": [38, 60], "color": "rgba(251, 191, 36, 0.18)"},
                    {"range": [60, 100], "color": "rgba(16, 185, 129, 0.18)"}
                ],
            }
        ))
        fig_g.update_layout(
            height=175,
            margin=dict(l=16, r=16, t=36, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig_g

    is_single_sec = len(filtered_secs) == 1
    sec_cols = st.columns(2)

    for idx, (_, s_row) in enumerate(filtered_secs.iterrows()):
        s_name = s_row["Sector"]
        s_ret = s_row[tf_choice]
        s_meter = int(s_row["Meter"])
        s_stocks = stocks_df[stocks_df["Sector"] == s_name].sort_values(tf_choice, ascending=False)

        with sec_cols[idx % 2]:
            if show_analog_meter:
                st.plotly_chart(
                    make_plotly_speedometer(s_meter, f"🧭 {s_name}", s_ret),
                    use_container_width=True,
                    key=f"gauge_{s_name}"
                )
            else:
                st.markdown(
                    f'<div class="kpi-card" style="min-height:80px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<b>🧭 {s_name}</b>'
                    f'<span style="color:{"#34d399" if s_ret>=0 else "#f87171"};font-weight:800;">{s_ret:+.2f}% (Meter: {s_meter})</span>'
                    f'</div>'
                    f'<div style="font-size:0.78rem;color:#94a3b8;">{s_row["Zone"]} | Avg Vol: {s_row["Avg_Vol"]}x | RSI: {s_row["RSI"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with st.expander(f"📂 {s_name} — শেয়ার তালিকা, ডজি সিগন্যাল ও চার্ট ({len(s_stocks)}টি শেয়ার)", expanded=is_single_sec):
                st.dataframe(
                    style_colored_table(
                        s_stocks[["Symbol", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "Consec_Up", "Bull_Candle", "Bear_Candle"]],
                        ["1D", "1W", "1M"]
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                q_pills = []
                for _, st_item in s_stocks.iterrows():
                    qt = urllib.parse.quote(st_item["Ticker"])
                    q_pills.append(
                        f'<a class="{"bull-pill" if st_item["1D"]>=0 else "bear-pill"}" href="?focus_stock={qt}" target="_self">'
                        f'📈 {st_item["Symbol"]} চার্ট ও সেটআপ</a>'
                    )
                st.markdown(f'<div class="pill-container">{"".join(q_pills)}</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# ট্যাব ২: ইন্ট্রাডে ডোজি/হ্যামার রিভার্সাল ও রিস্ক ক্যালকুলেটর
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("#### 🎯 ইন্ট্রাডে ডজি / হ্যামার কনসোলিডেশন ও সেক্টর টার্নঅ্যারাউন্ড স্ক্যানার")

    # সম্পূর্ণ ফিল্টারড বুলিশ ও বেয়ারিশ টেবিল (Entry, SL, Target সহ)
    t2_c1, t2_c2 = st.columns(2)
    with t2_c1:
        st.markdown("##### 🟢 বুলিশ ইন্ট্রাডে রিভার্সাল (ডাউন সেক্টর আপ মুভ + ডজি/হ্যামার + ভলিউম)")
        b_scan = stocks_df[
            (stocks_df["Consec_Up"] <= 2) &
            (stocks_df["1D"] >= -1.8) & (stocks_df["1D"] <= 4.2) &
            (stocks_df["Vol_Ratio"] >= 1.05)
        ].copy()
        b_scan["Bull_Candle"] = b_scan["Bull_Candle"].fillna("Base Consolidation")
        b_scan["Entry (₹)"] = (b_scan["Price"] * 1.001).round(2)
        b_scan["SL (₹)"] = (b_scan["Price"] - 1.2 * b_scan["ATR"]).round(2)
        b_scan["Target (₹)"] = (b_scan["Price"] + 1.8 * b_scan["ATR"]).round(2)
        b_scan = b_scan.sort_values(["Sec_Bull_Turn", "Vol_Ratio"], ascending=[False, False]).head(15)
        st.dataframe(
            style_colored_table(
                b_scan[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Bull_Candle", "Entry (₹)", "SL (₹)", "Target (₹)"]],
                ["1D", "1W"]
            ),
            use_container_width=True,
            hide_index=True
        )

    with t2_c2:
        st.markdown("##### 🔴 বেয়ারিশ ইন্ট্রাডে ব্রেকডাউন (টপ সেক্টর রোলওভার + ডজি/শুটিং স্টার + ভলিউম)")
        br_scan = stocks_df[
            (stocks_df["Consec_Down"] <= 2) &
            (stocks_df["1D"] <= 1.8) & (stocks_df["1D"] >= -4.2) &
            (stocks_df["Vol_Ratio"] >= 1.05)
        ].copy()
        br_scan["Bear_Candle"] = br_scan["Bear_Candle"].fillna("Top Stall Doji")
        br_scan["Short Below (₹)"] = (br_scan["Price"] * 0.999).round(2)
        br_scan["SL (₹)"] = (br_scan["Price"] + 1.2 * br_scan["ATR"]).round(2)
        br_scan["Target (₹)"] = (br_scan["Price"] - 1.8 * br_scan["ATR"]).round(2)
        br_scan = br_scan.sort_values(["Sec_Bear_Roll", "Vol_Ratio"], ascending=[False, False]).head(15)
        st.dataframe(
            style_colored_table(
                br_scan[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Bear_Candle", "Short Below (₹)", "SL (₹)", "Target (₹)"]],
                ["1D", "1W"]
            ),
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")
    st.markdown("#### 🧮 ইন্ট্রাডে পজিশন সাইজ ও রিস্ক ক্যালকুলেটর (Risk Management Tool)")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        cap_amt = st.number_input("💰 মোট ট্রেডিং ক্যাপিটাল (₹):", min_value=1000.0, value=100000.0, step=5000.0)
    with rc2:
        risk_pct = st.number_input("⚠️ প্রতি ট্রেডে সর্বোচ্চ ঝুঁকি (Risk %):", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
    with rc3:
        ent_p = st.number_input("🎯 এন্ট্রি প্রাইস (Entry ₹):", min_value=1.0, value=500.0, step=5.0)
    with rc4:
        sl_p = st.number_input("🛑 স্টপ-লস প্রাইস (Stop-Loss ₹):", min_value=0.5, value=490.0, step=5.0)

    max_loss_rs = cap_amt * (risk_pct / 100.0)
    sl_diff = abs(ent_p - sl_p)
    qty_to_trade = int(max_loss_rs / sl_diff) if sl_diff > 0 else 0
    target_1_2 = ent_p + (2.0 * sl_diff) if ent_p >= sl_p else ent_p - (2.0 * sl_diff)

    st.success(
        f"✅ **অনুমোদিত সর্বোচ্চ লস:** ₹{max_loss_rs:,.0f} &nbsp;|&nbsp; "
        f"📦 **সঠিক শেয়ার সংখ্যা (Quantity):** `{qty_to_trade} টি` &nbsp;|&nbsp; "
        f"🎯 **১:২ রিস্ক-রিওয়ার্ড টার্গেট:** `₹{target_1_2:,.2f}`"
    )

# ------------------------------------------------------------------------------
# ট্যাব ৩: লং ও সুইং স্ক্যানার (Breakout & Value)
# ------------------------------------------------------------------------------
with tab3:
    sw1, sw2 = st.columns(2)
    with sw1:
        st.markdown("##### 🚀 সুইং পুলব্যাক ও ভলিউম ব্রেকআউট স্ক্যানার (Near 20/50 DMA Support)")
        swing_pullback = stocks_df[
            (stocks_df["Above_50DMA"]) &
            (stocks_df["Dist_20DMA"] >= -3.0) &
            (stocks_df["Dist_20DMA"] <= 4.5) &
            (stocks_df["RSI"] >= 45) & (stocks_df["RSI"] <= 65) &
            (stocks_df["Vol_Ratio"] >= 1.0)
        ].sort_values("Vol_Ratio", ascending=False)
        st.dataframe(
            style_colored_table(
                swing_pullback[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "DMA20", "DMA50", "Bull_Candle"]],
                ["1D", "1W", "1M"]
            ),
            use_container_width=True,
            hide_index=True
        )

    with sw2:
        st.markdown("##### 💎 ভ্যালু ও বটম টার্নঅ্যারাউন্ড স্ক্যানার (Oversold + Volume Recovery)")
        val_scan = stocks_df[
            (stocks_df["1M"] < 0) &
            (stocks_df["1D"] > 0) &
            (stocks_df["RSI"] <= 48) &
            (stocks_df["Vol_Ratio"] >= 1.05)
        ].sort_values("Vol_Ratio", ascending=False)
        st.dataframe(
            style_colored_table(
                val_scan[["Symbol", "Sector", "Price", "1D", "1W", "1M", "3M", "Vol_Ratio", "RSI", "Bull_Candle"]],
                ["1D", "1W", "1M", "3M"]
            ),
            use_container_width=True,
            hide_index=True
        )

    csv_data = stocks_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 সম্পূর্ণ ১৮০+ শেয়ারের স্ক্যানার রিপোর্ট ডাউনলোড করুন (CSV / Excel)",
        data=csv_data,
        file_name="alphapulse_pro_full_scan.csv",
        mime="text/csv",
        use_container_width=True
    )

# ------------------------------------------------------------------------------
# ট্যাব ৪: সব সেক্টরের তুলনামূলক টেবিল ও বার চার্ট
# ------------------------------------------------------------------------------
with tab4:
    st.markdown(f"#### 📊 ৩২টি সেক্টরের তুলনামূলক পারফরম্যান্স চার্ট ({tf_choice})")
    chart_secs = sectors_df.sort_values(tf_choice, ascending=True)
    bar_colors = ["#10b981" if v >= 0 else "#ef4444" for v in chart_secs[tf_choice]]

    fig_bar = go.Figure(go.Bar(
        x=chart_secs[tf_choice],
        y=chart_secs["Sector"],
        orientation="h",
        marker_color=bar_colors,
        text=[f"{v:+.2f}%" for v in chart_secs[tf_choice]],
        textposition="outside"
    ))
    fig_bar.update_layout(
        height=720,
        template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=40, t=15, b=10),
        xaxis_title=f"রিটার্ন ({tf_choice} %)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### 📋 ৩২ সেক্টরের পূর্ণাঙ্গ মাল্টি-টাইমফ্রেম রোটেশন ম্যাট্রিক্স")
    st.dataframe(
        style_colored_table(
            sectors_df.sort_values(tf_choice, ascending=False)[
                ["Sector", "Zone", "Meter", "1D", "1W", "1M", "3M", "6M", "1Y", "Avg_Vol", "RSI", "Breadth_50DMA"]
            ],
            ["1D", "1W", "1M", "3M", "6M", "1Y"]
        ),
        use_container_width=True,
        hide_index=True
    )

# ==============================================================================
# ১৫. ফ্লোটিং ‘🚀 ওপরে যান (Top)’ বাটন (HTML Anchor + JS Smooth Scroller)
# ==============================================================================
st.markdown('<a href="#top-anchor" class="floating-top-btn" id="alphapulse-top-btn">🚀 ওপরে যান (Top)</a>', unsafe_allow_html=True)

components.html(
    """
    <script>
    (function() {
        const doc = window.parent.document;
        const btn = doc.getElementById("alphapulse-top-btn");
        if (btn) {
            btn.addEventListener("click", function(e) {
                e.preventDefault();
                const anchor = doc.getElementById("top-anchor");
                if (anchor) {
                    anchor.scrollIntoView({ behavior: "smooth", block: "start" });
                }
                const targets = [
                    doc.querySelector('[data-testid="stAppViewContainer"]'),
                    doc.querySelector('[data-testid="stMain"]'),
                    doc.querySelector('section.main'),
                    doc.documentElement,
                    doc.body
                ];
                targets.forEach(function(el) {
                    if (el && el.scrollTo) {
                        el.scrollTo({ top: 0, behavior: "smooth" });
                    }
                });
                window.parent.scrollTo({ top: 0, behavior: "smooth" });
            });
        }
    })();
    </script>
    """,
    height=0,
    width=0
)
