import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.parse
from datetime import datetime
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
# ২. ৩২টি মাইক্রো-সেক্টর ও নির্বাচিত লিকুইড শেয়ারের তালিকা
# ==============================================================================
SECTOR_STOCKS = {
    "Defence & Aerospace": ["HAL.NS", "BEL.NS", "BDL.NS", "PARAS.NS", "DATAPATTNS.NS", "ASTRAMICRO.NS"],
    "Shipbuilding & Marine": ["MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "SCI.NS", "GESHIP.NS"],
    "Railways & Wagons": ["RVNL.NS", "IRFC.NS", "IRCON.NS", "TITAGARH.NS", "JWL.NS", "CONCOR.NS", "RITES.NS"],
    "Cables & Wires": ["POLYCAB.NS", "KEI.NS", "RRKABEL.NS", "FINCABLES.NS", "UNIVERSAL.NS"],
    "Transformers & Power T&D": ["CGPOWER.NS", "VOLTAMP.NS", "TARIL.NS", "HITACHI.NS", "GEVT&D.NS", "APARINDS.NS"],
    "EMS & Electronics": ["DIXON.NS", "KAYNES.NS", "SYRMA.NS", "AMBER.NS", "PGEL.NS", "CYIENTDLM.NS"],
    "Green Energy & Solar": ["IREDA.NS", "SUZLON.NS", "INOXWIND.NS", "KPIGREEN.NS", "WAAREEENER.NS", "BORORENEW.NS"],
    "Power Utilities & Financiers": ["NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "PFC.NS", "RECLTD.NS", "NHPC.NS", "JSWENERGY.NS"],
    "Cooling & HVAC": ["VOLTAS.NS", "BLUESTARCO.NS", "SYMPHONY.NS", "WHIRLPOOL.NS", "HAVELLS.NS"],
    "CNC, Bearings & Precision Engg": ["CUMMINSIND.NS", "TIMKEN.NS", "SKFINDIA.NS", "SCHAEFFLER.NS", "GRINDWELL.NS", "MTARTECH.NS"],
    "Pre-Engineered & Infra EPC": ["LT.NS", "KPIL.NS", "KEC.NS", "NCC.NS", "PNCINFRA.NS", "HGINFRA.NS", "ENGINERSIN.NS"],
    "Real Estate & Housing": ["DLF.NS", "GODREJPROP.NS", "MACROTECH.NS", "OBERIRLTY.NS", "PRESTIGE.NS", "BRIGADE.NS"],
    "Building Materials (Pipes & Sanitary)": ["ASTRAL.NS", "SUPREMEIND.NS", "CERA.NS", "KAJARIACER.NS", "CENTURYPLY.NS", "PRINCEPIPE.NS"],
    "CDMO & API Pharma": ["DIVISLAB.NS", "LAURUSLABS.NS", "SYNGENE.NS", "SUVENPHAR.NS", "GRANULES.NS", "NEULANDLAB.NS"],
    "Largecap Pharma": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "LUPIN.NS", "AUROPHARMA.NS", "ZYDUSLIFE.NS"],
    "Hospitals & Diagnostics": ["APOLLOHOSP.NS", "MAXHEALTH.NS", "FORTIS.NS", "NARAYANA.NS", "LALPATHLAB.NS", "METROPOLIS.NS"],
    "QSR & Food Delivery": ["ZOMATO.NS", "JUBLFOOD.NS", "DEVYANI.NS", "WESTLIFE.NS", "SAPPHIRE.NS", "BIKAJI.NS"],
    "FMCG Staples": ["ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "BRITANNIA.NS", "DABUR.NS", "MARICO.NS", "TATACONSUM.NS"],
    "Retail, Apparel & Footwear": ["TRENT.NS", "DMART.NS", "PAGEIND.NS", "BATAINDIA.NS", "METROBRAND.NS", "MANYAVAR.NS"],
    "Jewellery & Luxury": ["TITAN.NS", "KALYANKJIL.NS", "SENCO.NS", "THANGAMAYL.NS", "ETHOSLTD.NS"],
    "Auto OEMs": ["M&M.NS", "TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "TVSMOTOR.NS", "HEROMOTOCO.NS"],
    "Auto Ancillaries & Tyres": ["MOTHERSON.NS", "BOSCHLTD.NS", "SONACOMS.NS", "UNO-MINDA.NS", "APOLLOTYRE.NS", "BALKRISIND.NS"],
    "IT Largecap": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"],
    "IT Midcap & ER&D": ["PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS", "MPHASIS.NS", "OFSS.NS"],
    "PSU Banks": ["SBIN.NS", "BANKBARODA.NS", "PNB.NS", "CANBK.NS", "UNIONBANK.NS", "INDIANB.NS"],
    "Private Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "FEDERALBNK.NS"],
    "NBFCs & Housing Finance": ["BAJFINANCE.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "LICHSGFIN.NS"],
    "Capital Market & Wealth": ["BSE.NS", "MCX.NS", "CDSL.NS", "ANGELONE.NS", "MOTILALOFS.NS", "CAMS.NS", "ANANDRATHI.NS"],
    "Specialty Chemicals & Agro": ["PIIND.NS", "SRF.NS", "DEEPAKNTR.NS", "NAVINFLUOR.NS", "CLEAN.NS", "AARTIIND.NS"],
    "Packaging & BOPP Films": ["EPL.NS", "UFLEX.NS", "POLYPLEX.NS", "JINDALPOLY.NS", "MOLDTKPAC.NS", "TCPLPACK.NS"],
    "Hotels, Tourism & Aviation": ["INDIGO.NS", "INDHOTEL.NS", "LEMON.NS", "CHALET.NS", "IRCTC.NS", "EIHOTEL.NS"],
    "Metals & Mining": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "COALINDIA.NS", "NATIONALUM.NS"]
}

ALL_TICKERS = sorted(list({ticker for stocks in SECTOR_STOCKS.values() for ticker in stocks}))
TICKER_TO_SECTOR = {ticker: sec for sec, stocks in SECTOR_STOCKS.items() for ticker in stocks}

TIMEFRAME_MAP = {
    "1D": ("1D (আজকের দিন)", 1),
    "1W": ("1W (১ সপ্তাহ)", 5),
    "1M": ("1M (১ মাস)", 21),
    "3M": ("3M (৩ মাস)", 63),
    "6M": ("6M (৬ মাস)", 126),
    "1Y": ("1Y (১ বছর)", 250),
}

# ==============================================================================
# ৩. সেশন স্টেট ও কুয়েরি প্যারামিটার হ্যান্ডলিং (URL-Encoded Safe)
# ==============================================================================
if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = "সবগুলো সেক্টর (Show All 32)"
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = "শেয়ার টাইপ করুন..."
if "active_modal" not in st.session_state:
    st.session_state.active_modal = None

# URL কুয়েরি প্যারামিটার থেকে নিরাপদে স্টক বা সেক্টর সিলেকশন রিড করা
qp = st.query_params
if "focus_stock" in qp:
    raw_st = urllib.parse.unquote(qp["focus_stock"])
    full_st = raw_st if raw_st.endswith(".NS") else f"{raw_st}.NS"
    if full_st in ALL_TICKERS:
        st.session_state.selected_stock = full_st
    st.query_params.clear()

if "focus_sector" in qp:
    raw_sec = urllib.parse.unquote(qp["focus_sector"])
    if raw_sec in SECTOR_STOCKS:
        st.session_state.selected_sector = raw_sec
    st.query_params.clear()

# ==============================================================================
# ৪. টপ হেডার এবং থিম কন্ট্রোল
# ==============================================================================
st.markdown('<div id="alphapulse-top"></div>', unsafe_allow_html=True)

hdr_col1, hdr_col2, hdr_col3 = st.columns([6.2, 2.3, 1.5])
with hdr_col1:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; padding-top:2px;">
            <span style="font-size:2.1rem;">🧭</span>
            <div>
                <h1 style="margin:0; padding:0; font-size:1.75rem; font-weight:800; letter-spacing:-0.3px;">
                    AlphaPulse Pro — Intraday, Swing & Sector Terminal
                </h1>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with hdr_col2:
    theme_choice = st.selectbox(
        "থিম নির্বাচন",
        ["🌙 Pro Dark (ডার্ক থিম)", "🌌 Cyber Emerald (টার্মিনাল থিম)", "☀️ Clean Light (লাইট থিম)"],
        index=0,
        label_visibility="collapsed"
    )

with hdr_col3:
    show_analog_meter = st.toggle("🎛️ অ্যানালগ মিটার", value=True)

# ==============================================================================
# ৫. ডাইনামিক প্রফেশনাল CSS থিম ও স্টাইলিং
# ==============================================================================
if "Clean Light" in theme_choice:
    BG_MAIN = "#f4f7fb"
    BG_CARD = "#ffffff"
    BG_SUB = "#eef2f9"
    TEXT_MAIN = "#0f172a"
    TEXT_MUTED = "#475569"
    BORDER_COL = "#cbd5e1"
    ACCENT_BLUE = "#2563eb"
elif "Cyber Emerald" in theme_choice:
    BG_MAIN = "#040d0a"
    BG_CARD = "#091813"
    BG_SUB = "#0d241c"
    TEXT_MAIN = "#ecfdf5"
    TEXT_MUTED = "#94a3b8"
    BORDER_COL = "#10b98144"
    ACCENT_BLUE = "#10b981"
else:
    BG_MAIN = "#070b14"
    BG_CARD = "#0f1626"
    BG_SUB = "#162035"
    TEXT_MAIN = "#f8fafc"
    TEXT_MUTED = "#94a3b8"
    BORDER_COL = "#1e293b"
    ACCENT_BLUE = "#38bdf8"

st.markdown(
    f"""
    <style>
        html, body, [data-testid="stAppViewContainer"], .main {{
            background-color: {BG_MAIN} !important;
            color: {TEXT_MAIN} !important;
            scroll-behavior: smooth !important;
        }}
        .block-container {{
            padding-top: 1.2rem !important;
            padding-bottom: 5rem !important;
            max-width: 97% !important;
        }}
        /* সাইডবার অটো-হাইড ও ক্লিন ইউআই */
        [data-testid="stSidebar"] {{
            background-color: {BG_CARD} !important;
        }}
        /* মার্কেট পালস রিবন */
        .pulse-ribbon {{
            background: {BG_CARD};
            border: 1px solid {BORDER_COL};
            border-radius: 12px;
            padding: 10px 18px;
            margin: 8px 0 14px 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.22);
        }}
        .pulse-item {{
            font-size: 0.9rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        /* ইন্ট্রাডে বুলিশ ও বেয়ারিশ ফোকাস বক্স */
        .focus-box-bull {{
            background: linear-gradient(145deg, rgba(6, 78, 59, 0.25), rgba(15, 22, 38, 0.92));
            border: 1.5px solid #10b981;
            border-radius: 14px;
            padding: 14px 16px;
            box-shadow: 0 0 18px rgba(16, 185, 129, 0.14);
            height: 100%;
        }}
        .focus-box-bear {{
            background: linear-gradient(145deg, rgba(127, 29, 29, 0.25), rgba(15, 22, 38, 0.92));
            border: 1.5px solid #ef4444;
            border-radius: 14px;
            padding: 14px 16px;
            box-shadow: 0 0 18px rgba(239, 68, 68, 0.14);
            height: 100%;
        }}
        .focus-title-bull {{
            color: #34d399;
            font-size: 0.95rem;
            font-weight: 800;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .focus-title-bear {{
            color: #f87171;
            font-size: 0.95rem;
            font-weight: 800;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .pill-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        a.stock-pill-bull {{
            text-decoration: none !important;
            background: rgba(16, 185, 129, 0.14);
            border: 1px solid #10b981;
            color: #ecfdf5 !important;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 0.80rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}
        a.stock-pill-bull:hover {{
            background: #10b981;
            color: #04130d !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
        }}
        a.stock-pill-bear {{
            text-decoration: none !important;
            background: rgba(239, 68, 68, 0.14);
            border: 1px solid #ef4444;
            color: #fef2f2 !important;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 0.80rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}
        a.stock-pill-bear:hover {{
            background: #ef4444;
            color: #ffffff !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
        }}
        .candle-tag {{
            background: rgba(255,255,255,0.14);
            padding: 1px 6px;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 600;
        }}
        /* ক্লিকেবল সেক্টর মার্কি বার */
        .sector-marquee-box {{
            background: {BG_CARD};
            border: 1px solid {BORDER_COL};
            border-radius: 12px;
            padding: 10px 12px;
            overflow: hidden;
            white-space: nowrap;
            margin: 8px 0 16px 0;
        }}
        .sector-marquee-track {{
            display: inline-block;
            animation: marquee-scroll 48s linear infinite;
        }}
        .sector-marquee-box:hover .sector-marquee-track {{
            animation-play-state: paused;
        }}
        @keyframes marquee-scroll {{
            0% {{ transform: translateX(0%); }}
            100% {{ transform: translateX(-50%); }}
        }}
        a.sector-chip {{
            text-decoration: none !important;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            margin-right: 10px;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 700;
            transition: all 0.2s ease;
        }}
        a.sector-chip-up {{
            background: rgba(16, 185, 129, 0.13);
            border: 1px solid #10b981;
            color: #34d399 !important;
        }}
        a.sector-chip-down {{
            background: rgba(239, 68, 68, 0.13);
            border: 1px solid #ef4444;
            color: #f87171 !important;
        }}
        a.sector-chip:hover {{
            transform: scale(1.04);
            filter: brightness(1.2);
        }}
        /* ৪টি সামারি কার্ড */
        .kpi-card {{
            background: {BG_CARD};
            border: 1.5px solid {ACCENT_BLUE}55;
            border-radius: 14px;
            padding: 14px 16px;
            min-height: 128px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }}
        .kpi-label {{
            color: {TEXT_MUTED};
            font-size: 0.83rem;
            font-weight: 700;
        }}
        .kpi-main {{
            font-size: 1.38rem;
            font-weight: 800;
            margin: 6px 0;
        }}
        .kpi-badge-up {{
            display: inline-block;
            background: rgba(16, 185, 129, 0.16);
            color: #34d399;
            border: 1px solid #10b98155;
            padding: 3px 9px;
            border-radius: 8px;
            font-size: 0.76rem;
            font-weight: 700;
            width: fit-content;
        }}
        .kpi-badge-down {{
            display: inline-block;
            background: rgba(239, 68, 68, 0.16);
            color: #f87171;
            border: 1px solid #ef444455;
            padding: 3px 9px;
            border-radius: 8px;
            font-size: 0.76rem;
            font-weight: 700;
            width: fit-content;
        }}
        /* সেক্টর কার্ড */
        .sec-card {{
            background: {BG_CARD};
            border: 1px solid {BORDER_COL};
            border-radius: 14px;
            padding: 14px;
            margin-bottom: 12px;
            transition: border 0.2s ease, transform 0.2s ease;
        }}
        .sec-card:hover {{
            border-color: {ACCENT_BLUE};
            transform: translateY(-2px);
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# ৬. ডেটা ডাউনলোড ও ক্যান্ডেলস্টিক + টার্নঅ্যারাউন্ড অ্যানালাইসিস ইঞ্জিন
# ==============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def fetch_market_pulse():
    idx_map = {
        "NIFTY": "^NSEI",
        "BANKNIFTY": "^NSEBANK",
        "VIX": "^INDIAVIX",
        "USDINR": "INR=X"
    }
    out = {}
    try:
        raw = yf.download(list(idx_map.values()), period="1y", interval="1d", progress=False, group_by="ticker", threads=True)
        for name, sym in idx_map.items():
            try:
                df = raw[sym].dropna(how="all") if len(idx_map) > 1 else raw.dropna(how="all")
                if len(df) >= 2:
                    last_c = float(df["Close"].iloc[-1])
                    prev_c = float(df["Close"].iloc[-2])
                    chg_1d = ((last_c - prev_c) / prev_c) * 100.0
                    chg_1w = ((last_c - float(df["Close"].iloc[-6])) / float(df["Close"].iloc[-6])) * 100.0 if len(df) >= 6 else chg_1d
                    chg_1y = ((last_c - float(df["Close"].iloc[0])) / float(df["Close"].iloc[0])) * 100.0
                    out[name] = {"price": last_c, "chg_1d": chg_1d, "chg_1w": chg_1w, "chg_1y": chg_1y}
            except Exception:
                pass
    except Exception:
        pass

    defaults = {
        "NIFTY": {"price": 23146.2, "chg_1d": 0.65, "chg_1w": 2.78, "chg_1y": -1.2},
        "BANKNIFTY": {"price": 55844.0, "chg_1d": 0.06, "chg_1w": 1.85, "chg_1y": 4.2},
        "VIX": {"price": 14.02, "chg_1d": -0.04, "chg_1w": -3.1, "chg_1y": -5.0},
        "USDINR": {"price": 84.95, "chg_1d": -0.21, "chg_1w": -0.1, "chg_1y": 1.5}
    }
    for k, v in defaults.items():
        if k not in out:
            out[k] = v
    return out


def compute_rsi(series: pd.Series, period: int = 14) -> float:
    if len(series) < period + 1:
        return 50.0
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    val = rsi.iloc[-1]
    return float(val) if not np.isnan(val) else 50.0


def detect_candle_and_streak(df: pd.DataFrame):
    """
    ক্যান্ডেলস্টিক প্যাটার্ন (Doji, Dragonfly Doji, Hammer, Shooting Star, Gravestone Doji, Tight Base)
    এবং টানা কতদিন শেয়ারটি উপরে বা নিচে গেছে (Consecutive Up/Down Days) তা নির্ণয় করে।
    """
    closes = df["Close"].values
    opens = df["Open"].values
    highs = df["High"].values
    lows = df["Low"].values

    # টানা কত দিন উপরে বা নিচে গেছে তার হিসাব
    consec_up = 0
    consec_down = 0
    for i in range(len(closes) - 1, 0, -1):
        if closes[i] > closes[i - 1]:
            if consec_down == 0:
                consec_up += 1
            else:
                break
        elif closes[i] < closes[i - 1]:
            if consec_up == 0:
                consec_down += 1
            else:
                break
        else:
            break

    o, h, l, c = float(opens[-1]), float(highs[-1]), float(lows[-1]), float(closes[-1])
    rng = max(h - l, 1e-6)
    body = abs(c - o)
    body_pct = body / rng
    lower_wick = min(o, c) - l
    upper_wick = h - max(o, c)
    lower_pct = lower_wick / rng
    upper_pct = upper_wick / rng

    # গত ৩ দিনের কনসোলিডেশন রেঞ্জ (Tight Base) চেক
    recent_rng_pct = 99.0
    if len(closes) >= 4:
        r_high = float(np.max(highs[-3:]))
        r_low = float(np.min(lows[-3:]))
        recent_rng_pct = ((r_high - r_low) / max(r_low, 1.0)) * 100.0

    bull_pattern = None
    bear_pattern = None

    # বুলিশ ডজি / হ্যামার / কনসোলিডেশন ক্যান্ডেল ডিটেকশন
    if body_pct <= 0.25 and lower_pct >= 0.45:
        bull_pattern = "🐉 Dragonfly Doji"
    elif body_pct <= 0.28:
        bull_pattern = "🕯️ Bullish Doji"
    elif lower_pct >= 0.50 and body_pct <= 0.42:
        bull_pattern = "🔨 Hammer Reversal"
    elif recent_rng_pct <= 4.2 and c >= o:
        bull_pattern = "📦 Tight Base Doji"
    elif lower_pct >= 0.35 and c >= o:
        bull_pattern = "🔄 Bottom Rejection"

    # বেয়ারিশ ডজি / শুটিং স্টার / ডিস্ট্রিবিউশন ক্যান্ডেল ডিটেকশন
    if body_pct <= 0.25 and upper_pct >= 0.45:
        bear_pattern = "🪦 Gravestone Doji"
    elif body_pct <= 0.28:
        bear_pattern = "🕯️ Exhaustion Doji"
    elif upper_pct >= 0.50 and body_pct <= 0.42:
        bear_pattern = "🌠 Shooting Star"
    elif recent_rng_pct <= 4.2 and c <= o:
        bear_pattern = "📉 Top Stall Base"
    elif upper_pct >= 0.35 and c <= o:
        bear_pattern = "⚠️ Upper Wick Supply"

    # ATR (14) হিসাব - ইন্ট্রাডে এন্ট্রি, স্টপলস ও টার্গেটের জন্য
    if len(df) >= 15:
        tr1 = df["High"] - df["Low"]
        tr2 = (df["High"] - df["Close"].shift(1)).abs()
        tr3 = (df["Low"] - df["Close"].shift(1)).abs()
        atr = float(pd.concat([tr1, tr2, tr3], axis=1).max(axis=1).rolling(14).mean().iloc[-1])
    else:
        atr = rng

    return {
        "consec_up": consec_up,
        "consec_down": consec_down,
        "body_pct": body_pct,
        "lower_pct": lower_pct,
        "upper_pct": upper_pct,
        "bull_pattern": bull_pattern,
        "bear_pattern": bear_pattern,
        "atr": atr if not np.isnan(atr) and atr > 0 else max(c * 0.018, 1.0),
        "day_high": h,
        "day_low": l,
        "day_open": o
    }


@st.cache_data(ttl=300, show_spinner=False)
def load_all_market_data():
    raw = yf.download(ALL_TICKERS, period="1y", interval="1d", progress=False, group_by="ticker", threads=True)
    rows = []

    for ticker in ALL_TICKERS:
        try:
            df = raw[ticker].dropna(how="all") if len(ALL_TICKERS) > 1 else raw.dropna(how="all")
            if df is None or len(df) < 25:
                continue

            closes = df["Close"]
            vols = df["Volume"]
            last_c = float(closes.iloc[-1])
            prev_c = float(closes.iloc[-2])

            def pct_return(days):
                idx = max(0, len(closes) - 1 - days)
                base = float(closes.iloc[idx])
                return ((last_c - base) / base) * 100.0 if base > 0 else 0.0

            ret_1d = ((last_c - prev_c) / prev_c) * 100.0 if prev_c > 0 else 0.0
            ret_1w = pct_return(5)
            ret_1m = pct_return(21)
            ret_3m = pct_return(63)
            ret_6m = pct_return(126)
            ret_1y = pct_return(250)

            dma_20 = float(closes.rolling(20).mean().iloc[-1])
            dma_50 = float(closes.rolling(50).mean().iloc[-1]) if len(closes) >= 50 else dma_20
            dma_200 = float(closes.rolling(200).mean().iloc[-1]) if len(closes) >= 200 else dma_50

            avg_vol_20 = float(vols.iloc[-21:-1].mean()) if len(vols) >= 22 else float(vols.mean())
            curr_vol = float(vols.iloc[-1])
            vol_ratio = round(curr_vol / avg_vol_20, 2) if avg_vol_20 > 0 else 1.0

            rsi_14 = round(compute_rsi(closes, 14), 1)
            c_info = detect_candle_and_streak(df)

            dist_20dma = ((last_c - dma_20) / dma_20) * 100.0 if dma_20 > 0 else 0.0

            rows.append({
                "Ticker": ticker,
                "Symbol": ticker.replace(".NS", ""),
                "Sector": TICKER_TO_SECTOR.get(ticker, "Others"),
                "Price": round(last_c, 2),
                "1D": round(ret_1d, 2),
                "1W": round(ret_1w, 2),
                "1M": round(ret_1m, 2),
                "3M": round(ret_3m, 2),
                "6M": round(ret_6m, 2),
                "1Y": round(ret_1y, 2),
                "Vol_Ratio": vol_ratio,
                "RSI": rsi_14,
                "DMA20": round(dma_20, 2),
                "DMA50": round(dma_50, 2),
                "DMA200": round(dma_200, 2),
                "Above_50DMA": last_c >= dma_50,
                "Dist_20DMA": round(dist_20dma, 2),
                "Consec_Up": c_info["consec_up"],
                "Consec_Down": c_info["consec_down"],
                "Bull_Pattern": c_info["bull_pattern"],
                "Bear_Pattern": c_info["bear_pattern"],
                "Body_Pct": round(c_info["body_pct"], 2),
                "Lower_Wick_Pct": round(c_info["lower_pct"], 2),
                "Upper_Wick_Pct": round(c_info["upper_pct"], 2),
                "ATR": round(c_info["atr"], 2),
                "Day_High": round(c_info["day_high"], 2),
                "Day_Low": round(c_info["day_low"], 2),
            })
        except Exception:
            continue

    stocks_df = pd.DataFrame(rows)
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # ৩২টি সেক্টরের অ্যাগ্রিগেটেড পারফরম্যান্স ও টার্নঅ্যারাউন্ড জোন নির্ণয়
    sec_rows = []
    for sec_name, sec_df in stocks_df.groupby("Sector"):
        r1d = float(sec_df["1D"].mean())
        r1w = float(sec_df["1W"].mean())
        r1m = float(sec_df["1M"].mean())
        r3m = float(sec_df["3M"].mean())
        r6m = float(sec_df["6M"].mean())
        r1y = float(sec_df["1Y"].mean())
        avg_vol = float(sec_df["Vol_Ratio"].mean())
        avg_rsi = float(sec_df["RSI"].mean())
        breadth_50 = float((sec_df["Above_50DMA"].sum() / len(sec_df)) * 100.0)

        # সেক্টর টার্নঅ্যারাউন্ড লজিক:
        # বুলিশ টার্নঅ্যারাউন্ড: সেক্টরটি ১ সপ্তাহ বা ১ মাসে ডাউনে ছিল (<= 0.5%), কিন্তু আজ নিচ থেকে ঘুরছে (1D >= -0.2% বা 1D > 1W/5)
        is_bull_turnaround = (r1w <= 1.2 or r1m <= 1.5) and (r1d >= -0.15 or r1d > (r1w / 5.0))
        # বেয়ারিশ রোলওভার: সেক্টরটি আগে উপরে ছিল (1W >= 0.5% বা 1M >= 1.5%), কিন্তু আজ দুর্বল হয়ে নিচে নামছে (1D <= 0.25%)
        is_bear_rollover = (r1w >= 0.0 or r1m >= 1.0) and (r1d <= 0.35 or r1d < (r1w / 5.0))

        # রোটেশন মিটার স্কোর (0 - 100)
        meter_score = int(np.clip(50 + (r1w * 3.5) + (r1d * 6.0) + ((avg_rsi - 50) * 0.6), 5, 98))

        if is_bull_turnaround and r1d >= 0:
            zone = "🔄 Turnaround Zone (ডাউন থেকে ঘুরে দাঁড়ানো)"
        elif r1w >= 2.0 and r1d >= 0:
            zone = "🚀 Leading Zone (টপ মোমেন্টাম)"
        elif is_bear_rollover and r1d < 0:
            zone = "⚠️ Exhaustion Zone (ওপর থেকে নিচে নামা)"
        else:
            zone = "💎 Value / Oversold Zone (ডিপ ডাউন / কনসোলিডেশন)"

        sec_rows.append({
            "Sector": sec_name,
            "Stock_Count": len(sec_df),
            "1D": round(r1d, 2),
            "1W": round(r1w, 2),
            "1M": round(r1m, 2),
            "3M": round(r3m, 2),
            "6M": round(r6m, 2),
            "1Y": round(r1y, 2),
            "Avg_Vol_Ratio": round(avg_vol, 2),
            "Avg_RSI": round(avg_rsi, 1),
            "Breadth_50DMA": round(breadth_50, 1),
            "Meter": meter_score,
            "Zone": zone,
            "Bull_Turnaround": is_bull_turnaround,
            "Bear_Rollover": is_bear_rollover
        })

    sectors_df = pd.DataFrame(sec_rows)

    # সেক্টরের টার্নঅ্যারাউন্ড তথ্য প্রতিটি শেয়ারের সাথে যুক্ত করা
    sec_lookup = sectors_df.set_index("Sector")[["1D", "1W", "1M", "Zone", "Bull_Turnaround", "Bear_Rollover"]].to_dict("index")
    stocks_df["Sec_1D"] = stocks_df["Sector"].map(lambda s: sec_lookup.get(s, {}).get("1D", 0.0))
    stocks_df["Sec_1W"] = stocks_df["Sector"].map(lambda s: sec_lookup.get(s, {}).get("1W", 0.0))
    stocks_df["Sec_1M"] = stocks_df["Sector"].map(lambda s: sec_lookup.get(s, {}).get("1M", 0.0))
    stocks_df["Sec_Zone"] = stocks_df["Sector"].map(lambda s: sec_lookup.get(s, {}).get("Zone", ""))
    stocks_df["Sec_Bull_Turn"] = stocks_df["Sector"].map(lambda s: sec_lookup.get(s, {}).get("Bull_Turnaround", False))
    stocks_df["Sec_Bear_Roll"] = stocks_df["Sector"].map(lambda s: sec_lookup.get(s, {}).get("Bear_Rollover", False))

    return stocks_df, sectors_df


# ==============================================================================
# ৭. ইন্ট্রাডে বুলিশ ও বেয়ারিশ ডজি/কনসোলিডেশন ফিল্টারিং ইঞ্জিন (তোমার নির্দেশ অনুযায়ী)
# ==============================================================================
def get_intraday_reversal_focus(stocks_df: pd.DataFrame):
    """
    ১. বুলিশ সাইড:
       - টানা ৩-৪ দিন উপরে যাওয়া শেয়ার সম্পূর্ণ বাদ (Consec_Up <= 2)
       - অতিরিক্ত বেড়ে যাওয়া শেয়ার বাদ (-1.8% <= 1D <= +4.0%)
       - নিচে কনসোলিডেট করছে বা ডজি / হ্যামার / টাইট বেস তৈরি করেছে (Bull_Pattern != None)
       - ভলিউম তৈরি হচ্ছে (Vol_Ratio >= 1.10x, অগ্রাধিকার উচ্চ ভলিউমে)
       - ডাউন সেক্টর যা নিচ থেকে আপের দিকে মুভ করছে (Sec_1W বা 1W ডাউন/ফ্ল্যাট থেকে 1D পজিটিভ মোমেন্টাম)
    ২. বেয়ারিশ সাইড:
       - টানা ৩-৪ দিন নিচে পড়া শেয়ার সম্পূর্ণ বাদ (Consec_Down <= 2)
       - অতিরিক্ত পড়ে যাওয়া শেয়ার বাদ (-4.0% <= 1D <= +1.8%)
       - ওপরে গিয়ে ডজি / শুটিং স্টার / সাপ্লাই রিজেকশন তৈরি করেছে (Bear_Pattern != None)
       - ভলিউম তৈরি হচ্ছে এবং সেক্টর ওপর থেকে নিচে ঘুরছে
    """
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = stocks_df.copy()

    # বুলিশ স্কোরিং ও ফিল্টারিং
    bull_cond = (
        (df["Consec_Up"] <= 2) &                      # টানা ৩-৪ দিন বাড়া শেয়ার বাদ
        (df["1D"] >= -1.6) & (df["1D"] <= 4.0) &      # অতিরিক্ত ভাগা শেয়ার বাদ, নিচে কনসোলিডেট করা শেয়ার
        (df["1W"] <= 4.5) &                           # আগে থেকেই অতিরিক্ত র‍্যালি না করা
        (df["Bull_Pattern"].notna()) &                # ডজি / হ্যামার / টাইট বেস ক্যান্ডেল
        (df["Vol_Ratio"] >= 1.05)                     # ভলিউম তৈরি হচ্ছে
    )
    bull_df = df[bull_cond].copy()

    # যদি মার্কেট কন্ডিশনে ৬টির কম পাওয়া যায়, তবে নিকটতম ডজি/কনসোলিডেশন শেয়ার নেওয়া (তবে টানা ৩-৪ দিন বাড়া কখনোই নয়)
    if len(bull_df) < 6:
        fallback_bull = df[
            (df["Consec_Up"] <= 2) &
            (df["1D"] >= -2.0) & (df["1D"] <= 4.2) &
            (df["Vol_Ratio"] >= 0.95)
        ].copy()
        fallback_bull["Bull_Pattern"] = fallback_bull["Bull_Pattern"].fillna("🕯️ Base Consolidation")
        bull_df = pd.concat([bull_df, fallback_bull]).drop_duplicates(subset=["Ticker"])

    # বুলিশ র‍্যাঙ্কিং স্কোর: ডাউন সেক্টর আপ মুভ + ডজি ক্যান্ডেল + ভলিউম বিল্ডআপ
    bull_df["Bull_Score"] = (
        (bull_df["Vol_Ratio"] * 30.0)
        + np.where(bull_df["Sec_Bull_Turn"], 25.0, 0.0)
        + np.where(bull_df["1W"] < 0, 18.0, 5.0)
        + ((1.0 - bull_df["Body_Pct"]) * 20.0)
        + (bull_df["Lower_Wick_Pct"] * 15.0)
    )
    bull_df = bull_df.sort_values("Bull_Score", ascending=False).head(8)

    # বেয়ারিশ স্কোরিং ও ফিল্টারিং (ঠিক বিপরীত লজিক)
    bear_cond = (
        (df["Consec_Down"] <= 2) &                    # টানা ৩-৪ দিন পড়া শেয়ার বাদ
        (df["1D"] <= 1.6) & (df["1D"] >= -4.0) &      # ইতিমধ্যে ধসে যাওয়া শেয়ার বাদ
        (df["1W"] >= -4.5) &                          # ওপরে বা রেজিস্ট্যান্সের কাছে থাকা শেয়ার
        (df["Bear_Pattern"].notna()) &                # শুটিং স্টার / গ্রেভস্টোন ডজি / টপ স্টল ক্যান্ডেল
        (df["Vol_Ratio"] >= 1.05)                     # ডিস্ট্রিবিউশন ভলিউম তৈরি হচ্ছে
    )
    bear_df = df[bear_cond].copy()

    if len(bear_df) < 6:
        fallback_bear = df[
            (df["Consec_Down"] <= 2) &
            (df["1D"] <= 2.0) & (df["1D"] >= -4.2) &
            (df["Vol_Ratio"] >= 0.95)
        ].copy()
        fallback_bear["Bear_Pattern"] = fallback_bear["Bear_Pattern"].fillna("🕯️ Top Stall Doji")
        bear_df = pd.concat([bear_df, fallback_bear]).drop_duplicates(subset=["Ticker"])

    bear_df["Bear_Score"] = (
        (bear_df["Vol_Ratio"] * 30.0)
        + np.where(bear_df["Sec_Bear_Roll"], 25.0, 0.0)
        + np.where(bear_df["1W"] > 0, 18.0, 5.0)
        + ((1.0 - bear_df["Body_Pct"]) * 20.0)
        + (bear_df["Upper_Wick_Pct"] * 15.0)
    )
    bear_df = bear_df.sort_values("Bear_Score", ascending=False).head(8)

    return bull_df, bear_df


with st.spinner("⚡ ৩২টি সেক্টর, ক্যান্ডেলস্টিক ডজি প্যাটার্ন ও লাইভ ভলিউম ডেটা বিশ্লেষণ করা হচ্ছে..."):
    pulse_data = fetch_market_pulse()
    stocks_df, sectors_df = load_all_market_data()

if stocks_df.empty or sectors_df.empty:
    st.error("⚠️ লাইভ মার্কেট ডেটা লোড করতে সাময়িক সমস্যা হয়েছে। অনুগ্রহ করে পেজটি রিলোড করুন।")
    st.stop()

# ==============================================================================
# ৮. লাইভ মার্কেট পালস রিবন + অটো মার্কেট বায়াস ইন্ডিকেটর
# ==============================================================================
nifty_d = pulse_data["NIFTY"]
bnf_d = pulse_data["BANKNIFTY"]
vix_d = pulse_data["VIX"]
usd_d = pulse_data["USDINR"]

adv_1d = int((stocks_df["1D"] > 0).sum())
dec_1d = int((stocks_df["1D"] < 0).sum())

if nifty_d["chg_1d"] >= 0.25 and adv_1d >= dec_1d:
    mkt_bias_txt = "🟢 আজকের মার্কেট বায়াস: BULLISH (বুলিশ রিভার্সাল শেয়ার ট্র্যাক করুন)"
    mkt_bias_col = "#34d399"
elif nifty_d["chg_1d"] <= -0.25 and dec_1d > adv_1d:
    mkt_bias_txt = "🔴 আজকের মার্কেট বায়াস: BEARISH (বেয়ারিশ ব্রেকডাউন শেয়ার ট্র্যাক করুন)"
    mkt_bias_col = "#f87171"
else:
    mkt_bias_txt = "⚖️ আজকের মার্কেট বায়াস: SIDEWAYS / ROTATIONAL (সেক্টর দেখে বুলিশ/বেয়ারিশ ট্র্যাক করুন)"
    mkt_bias_col = "#fbbf24"

vix_status = "🟢 স্বস্তিদায়ক (Low Fear)" if vix_d["price"] < 15.5 else ("🟡 সতর্কতা (Moderate)" if vix_d["price"] < 19 else "🔴 উচ্চ ঝুঁকি (High Fear)")

st.markdown(
    f"""
    <div class="pulse-ribbon">
        <div class="pulse-item">
            <span>🇮🇳 Nifty 50:</span>
            <span style="color:{'#34d399' if nifty_d['chg_1d']>=0 else '#f87171'};">
                {nifty_d['price']:,.1f} ({nifty_d['chg_1d']:+.2f}%)
            </span>
        </div>
        <div class="pulse-item">
            <span>🏛️ Bank Nifty:</span>
            <span style="color:{'#34d399' if bnf_d['chg_1d']>=0 else '#f87171'};">
                {bnf_d['price']:,.1f} ({bnf_d['chg_1d']:+.2f}%)
            </span>
        </div>
        <div class="pulse-item">
            <span>⚡ India VIX:</span>
            <span style="color:{'#34d399' if vix_d['chg_1d']<=0 else '#fbbf24'};">
                {vix_d['price']:.2f} ({vix_d['chg_1d']:+.2f}%) — {vix_status}
            </span>
        </div>
        <div class="pulse-item">
            <span>💵 USD/INR:</span>
            <span style="color:#94a3b8;">₹{usd_d['price']:.2f} ({usd_d['chg_1d']:+.2f}%)</span>
        </div>
        <div class="pulse-item" style="color:{mkt_bias_col}; background:rgba(255,255,255,0.05); padding:4px 10px; border-radius:8px;">
            {mkt_bias_txt}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# ৯. ৫-কলাম প্রো কন্ট্রোল ও ফিল্টার বার
# ==============================================================================
f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1.2, 2.2, 2.2, 2.2, 2.2])

with f_col1:
    tf_selected = st.selectbox("📅 ১. টাইমফ্রেম:", list(TIMEFRAME_MAP.keys()), index=1)

with f_col2:
    sort_selected = st.selectbox(
        "🔄 ২. সাজানোর ক্রম (Sort By):",
        [
            "🚀 Top Gainers (সবচেয়ে বেশি বাড়া আগে)",
            "📉 Top Losers (সবচেয়ে বেশি ডাউন আগে)",
            "🔄 Bottom Turnaround (ডাউন থেকে আপ মুভ আগে)",
            "🔥 Volume Shockers (সবচেয়ে বেশি ভলিউম আগে)",
            "🎛️ Rotation Meter (মিটার স্কোর অনুযায়ী)"
        ],
        index=0
    )

with f_col3:
    zone_selected = st.selectbox(
        "🎯 ৩. রোটেশন জোন ফিল্টার:",
        [
            "🌐 সব সেক্টর (All 32 Sectors)",
            "🔄 Turnaround Zone (ডাউন থেকে ঘুরে দাঁড়ানো)",
            "🚀 Leading Zone (টপ মোমেন্টাম)",
            "⚠️ Exhaustion Zone (ওপর থেকে নিচে নামা)",
            "💎 Value / Oversold Zone (ডিপ ডাউন / কনসোলিডেশন)"
        ],
        index=0
    )

with f_col4:
    sector_options = ["সবগুলো সেক্টর (Show All 32)"] + sorted(list(SECTOR_STOCKS.keys()))
    sec_idx = sector_options.index(st.session_state.selected_sector) if st.session_state.selected_sector in sector_options else 0
    chosen_sector = st.selectbox("🔍 ৪. নির্দিষ্ট সেক্টর খুঁজুন:", sector_options, index=sec_idx)
    st.session_state.selected_sector = chosen_sector

with f_col5:
    stock_options = ["শেয়ার টাইপ করুন..."] + [f"{row['Symbol']} — ({row['Sector']})" for _, row in stocks_df.sort_values("Symbol").iterrows()]
    curr_st_idx = 0
    if st.session_state.selected_stock != "শেয়ার টাইপ করুন...":
        sym_clean = st.session_state.selected_stock.replace(".NS", "")
        for i, opt in enumerate(stock_options):
            if opt.startswith(f"{sym_clean} —"):
                curr_st_idx = i
                break
    chosen_stock_label = st.selectbox("⚡ ৫. যেকোনো শেয়ার খুঁজুন (Stock Search):", stock_options, index=curr_st_idx)
    if chosen_stock_label != "শেয়ার টাইপ করুন...":
        st.session_state.selected_stock = chosen_stock_label.split(" — ")[0].strip() + ".NS"
    else:
        st.session_state.selected_stock = "শেয়ার টাইপ করুন..."

# ==============================================================================
# ১০. ইন্ট্রাডে বুলিশ ও বেয়ারিশ রিভার্সাল ফোকাস (Doji + Consolidation + Sector Turnaround)
# ==============================================================================
st.markdown('<div id="intraday-focus-section"></div>', unsafe_allow_html=True)

bull_focus_df, bear_focus_df = get_intraday_reversal_focus(stocks_df)

mode_col1, mode_col2 = st.columns([6.5, 3.5])
with mode_col1:
    st.markdown(
        "<div style='font-size:0.86rem; color:#94a3b8; margin-bottom:4px;'>"
        "💡 <b>ইন্ট্রাডে স্মার্ট ফিল্টার লজিক:</b> টানা ৩-৪ দিন ধরে বাড়া বা পড়া শেয়ারগুলো বাদ দিয়ে, যে শেয়ারগুলো ডজি (Doji) / হ্যামার / শুটিং স্টার তৈরি করে কনসোলিডেট করছে, ভলিউম তৈরি হচ্ছে এবং সেক্টর ঘুরছে—শুধুমাত্র সেগুলোই নিচে রাখা হয়েছে (যেকোনো শেয়ারে ক্লিক করলেই ট্রেড সেটআপ ও চার্ট খুলে যাবে):"
        "</div>",
        unsafe_allow_html=True
    )
with mode_col2:
    intraday_view_mode = st.radio(
        "ইন্ট্রাডে ট্র্যাকিং মোড:",
        ["🌗 উভয় সাইড (Both)", "🟢 বুলিশ ডে মোড (Bullish)", "🔴 বেয়ারিশ ডে মোড (Bearish)"],
        horizontal=True,
        label_visibility="collapsed"
    )

def build_focus_pills_html(df_sub: pd.DataFrame, is_bull: bool) -> str:
    pills = []
    cls_name = "stock-pill-bull" if is_bull else "stock-pill-bear"
    dot_icon = "🟢" if is_bull else "🔴"
    pat_col = "Bull_Pattern" if is_bull else "Bear_Pattern"

    for _, r in df_sub.iterrows():
        sym = r["Symbol"]
        q_sym = urllib.parse.quote(r["Ticker"])
        chg_str = f"{r['1D']:+.1f}%"
        vol_str = f"{r['Vol_Ratio']:.2f}x Vol"
        pat_str = r[pat_col] if pd.notna(r[pat_col]) else "🕯️ Doji"
        sec_hint = "🔄Sec↑" if (is_bull and r["Sec_Bull_Turn"]) else ("📉Sec↓" if (not is_bull and r["Sec_Bear_Roll"]) else "")
        tooltip = (
            f"সেক্টর: {r['Sector']} (1W: {r['Sec_1W']:+.1f}%, আজ: {r['Sec_1D']:+.1f}%) | "
            f"প্যাটার্ন: {pat_str} | RSI: {r['RSI']} | টানা দিন: {r['Consec_Up'] if is_bull else r['Consec_Down']}"
        )
        pills.append(
            f'<a class="{cls_name}" href="?focus_stock={q_sym}" target="_self" title="{tooltip}">'
            f'{dot_icon} <b>{sym}</b> ({chg_str} | {vol_str}) '
            f'<span class="candle-tag">{pat_str} {sec_hint}</span>'
            f'</a>'
        )
    return "".join(pills)

bull_pills_html = build_focus_pills_html(bull_focus_df, is_bull=True)
bear_pills_html = build_focus_pills_html(bear_focus_df, is_bull=False)

if intraday_view_mode == "🟢 বুলিশ ডে মোড (Bullish)":
    st.markdown(
        f"""
        <div class="focus-box-bull">
            <div class="focus-title-bull">
                <span>🔄 ইন্ট্রাডে বুলিশ রিভার্সাল ফোকাস (Bottom Turnaround — নিচে ডজি/হ্যামার তৈরি করে ভলিউমসহ ঘুরে দাঁড়ানো স্টক)</span>
                <span style="font-size:0.78rem; color:#a7f3d0;">✅ টানা ৩-৪ দিন বাড়া শেয়ার বাদ দেওয়া হয়েছে</span>
            </div>
            <div class="pill-wrap">{bull_pills_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
elif intraday_view_mode == "🔴 বেয়ারিশ ডে মোড (Bearish)":
    st.markdown(
        f"""
        <div class="focus-box-bear">
            <div class="focus-title-bear">
                <span>📉 ইন্ট্রাডে বেয়ারিশ রিভার্সাল ফোকাস (Top Breakdown — ওপরে ডজি/শুটিং স্টার তৈরি করে নিচে নামার প্রস্তুতি নেওয়া স্টক)</span>
                <span style="font-size:0.78rem; color:#fecaca;">✅ টানা ৩-৪ দিন পড়া শেয়ার বাদ দেওয়া হয়েছে</span>
            </div>
            <div class="pill-wrap">{bear_pills_html}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    fbox1, fbox2 = st.columns(2)
    with fbox1:
        st.markdown(
            f"""
            <div class="focus-box-bull">
                <div class="focus-title-bull">
                    <span>🔄 ইন্ট্রাডে বুলিশ রিভার্সাল ফোকাস (Bottom Turnaround – অতিরিক্ত না বেড়ে নিচ থেকে ঘুরে দাঁড়ানো স্টক)</span>
                </div>
                <div class="pill-wrap">{bull_pills_html}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with fbox2:
        st.markdown(
            f"""
            <div class="focus-box-bear">
                <div class="focus-title-bear">
                    <span>📉 ইন্ট্রাডে বেয়ারিশ রিভার্সাল ফোকাস (Top Breakdown – ওপর থেকে নিচে নামার প্রস্তুতি নেওয়া স্টক)</span>
                </div>
                <div class="pill-wrap">{bear_pills_html}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==============================================================================
# ১১. সিলেক্টেড শেয়ারের লাইভ ট্রেড প্ল্যান (Entry, SL, Target) ও ক্যান্ডেলস্টিক চার্ট প্যানেল
# ==============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def get_single_stock_history(ticker: str):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        return df.dropna(how="all")
    except Exception:
        return pd.DataFrame()

if st.session_state.selected_stock != "শেয়ার টাইপ করুন..." and st.session_state.selected_stock in stocks_df["Ticker"].values:
    st_row = stocks_df[stocks_df["Ticker"] == st.session_state.selected_stock].iloc[0]
    sym_only = st_row["Symbol"]
    price_now = st_row["Price"]
    atr_val = st_row["ATR"]

    # বুলিশ ও বেয়ারিশ উভয় সেটআপ লেভেল হিসাব
    bull_entry = round(max(price_now, st_row["Day_High"] * 0.998), 2)
    bull_sl = round(min(st_row["Day_Low"], bull_entry - (1.2 * atr_val)), 2)
    bull_t1 = round(bull_entry + (1.5 * atr_val), 2)
    bull_t2 = round(bull_entry + (2.5 * atr_val), 2)

    bear_entry = round(min(price_now, st_row["Day_Low"] * 1.002), 2)
    bear_sl = round(max(st_row["Day_High"], bear_entry + (1.2 * atr_val)), 2)
    bear_t1 = round(bear_entry - (1.5 * atr_val), 2)
    bear_t2 = round(bear_entry - (2.5 * atr_val), 2)

    with st.container():
        st.markdown("---")
        insp_hdr1, insp_hdr2 = st.columns([8, 2])
        with insp_hdr1:
            st.markdown(
                f"### 🎯 লাইভ ইন্ট্রাডে ও সুইং ট্রেড ইন্সপেক্টর: **{sym_only}** "
                f"<span style='font-size:0.95rem; color:#38bdf8;'>({st_row['Sector']})</span>",
                unsafe_allow_html=True
            )
        with insp_hdr2:
            if st.button("✖️ ইন্সপেক্টর বন্ধ করুন", use_container_width=True):
                st.session_state.selected_stock = "শেয়ার টাইপ করুন..."
                st.rerun()

        ic1, ic2, ic3, ic4 = st.columns(4)
        with ic1:
            st.markdown(
                f"""
                <div class="sec-card">
                    <div style="color:#94a3b8; font-size:0.8rem;">বর্তমান দাম ও ভলিউম স্পাইক</div>
                    <div style="font-size:1.4rem; font-weight:800; margin:4px 0;">₹{price_now:,.2f} ({st_row['1D']:+.2f}%)</div>
                    <div style="font-size:0.82rem; color:#38bdf8;">📊 ভলিউম রেশিও: <b>{st_row['Vol_Ratio']}x</b> | RSI: <b>{st_row['RSI']}</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with ic2:
            pat_txt = st_row["Bull_Pattern"] or st_row["Bear_Pattern"] or "🕯️ Neutral / Range Candle"
            st.markdown(
                f"""
                <div class="sec-card">
                    <div style="color:#94a3b8; font-size:0.8rem;">ক্যান্ডেলস্টিক ও কনসোলিডেশন স্ট্যাটাস</div>
                    <div style="font-size:1.15rem; font-weight:800; margin:6px 0; color:#fbbf24;">{pat_txt}</div>
                    <div style="font-size:0.8rem;">টানা আপ দিন: <b>{st_row['Consec_Up']}</b> | টানা ডাউন দিন: <b>{st_row['Consec_Down']}</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with ic3:
            st.markdown(
                f"""
                <div class="sec-card" style="border-color:#10b98188;">
                    <div style="color:#34d399; font-size:0.82rem; font-weight:700;">🟢 বুলিশ ইন্ট্রাডে সেটআপ (Buy Setup)</div>
                    <div style="font-size:0.84rem; margin-top:4px;">
                        🔹 <b>Entry:</b> ₹{bull_entry} &nbsp;|&nbsp; 🛑 <b>SL:</b> ₹{bull_sl}<br>
                        🎯 <b>Target 1:</b> ₹{bull_t1} &nbsp;|&nbsp; 🚀 <b>Target 2:</b> ₹{bull_t2}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with ic4:
            st.markdown(
                f"""
                <div class="sec-card" style="border-color:#ef444488;">
                    <div style="color:#f87171; font-size:0.82rem; font-weight:700;">🔴 বেয়ারিশ ইন্ট্রাডে সেটআপ (Short Setup)</div>
                    <div style="font-size:0.84rem; margin-top:4px;">
                        🔹 <b>Short Below:</b> ₹{bear_entry} &nbsp;|&nbsp; 🛑 <b>SL:</b> ₹{bear_sl}<br>
                        🎯 <b>Target 1:</b> ₹{bear_t1} &nbsp;|&nbsp; 📉 <b>Target 2:</b> ₹{bear_t2}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        hist_df = get_single_stock_history(st_row["Ticker"])
        if not hist_df.empty and len(hist_df) >= 20:
            hist_df["DMA20"] = hist_df["Close"].rolling(20).mean()
            hist_df["DMA50"] = hist_df["Close"].rolling(50).mean()
            plot_df = hist_df.tail(75)

            fig = make_subplots(
                rows=2, cols=1, shared_xaxes=True,
                vertical_spacing=0.04, row_heights=[0.74, 0.26]
            )
            fig.add_trace(
                go.Candlestick(
                    x=plot_df.index, open=plot_df["Open"], high=plot_df["High"],
                    low=plot_df["Low"], close=plot_df["Close"], name="Price"
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=plot_df.index, y=plot_df["DMA20"], mode="lines", name="20 DMA", line=dict(color="#38bdf8", width=1.6)),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=plot_df.index, y=plot_df["DMA50"], mode="lines", name="50 DMA", line=dict(color="#f59e0b", width=1.6)),
                row=1, col=1
            )
            vol_colors = ["#10b981" if c >= o else "#ef4444" for c, o in zip(plot_df["Close"], plot_df["Open"])]
            fig.add_trace(
                go.Bar(x=plot_df.index, y=plot_df["Volume"], name="Volume", marker_color=vol_colors),
                row=2, col=1
            )
            fig.update_layout(
                height=420,
                template="plotly_dark" if "Clean Light" not in theme_choice else "plotly_white",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=25, b=10),
                xaxis_rangeslider_visible=False,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

        ext1, ext2, ext3 = st.columns(3)
        with ext1:
            st.link_button(f"📈 TradingView-এ {sym_only} চার্ট খুলুন", f"https://in.tradingview.com/chart/?symbol=NSE%3A{sym_only}", use_container_width=True)
        with ext2:
            st.link_button(f"📊 Screener.in-এ {sym_only} ফান্ডামেন্টাল দেখুন", f"https://www.screener.in/company/{sym_only}/", use_container_width=True)
        with ext3:
            st.link_button(f"📰 Google Finance-এ {sym_only} নিউজ দেখুন", f"https://www.google.com/finance/quote/{sym_only}:NSE", use_container_width=True)
        st.markdown("---")

# ==============================================================================
# ১২. ক্লিকেবল সেক্টর বার (URL-Encoded — `&` এরর সম্পূর্ণ ফিক্সড)
# ==============================================================================
st.markdown(
    "<div style='font-size:0.86rem; color:#cbd5e1; margin-top:8px;'>"
    "📍 <b>ক্লিকেবল সেক্টর বার:</b> নিচের চলমান বারের ওপর মাউস রাখলে সেটি থেমে যাবে এবং <b>যেকোনো সেক্টরের ওপর ক্লিক করলেই</b> সাথে সাথে সেই সেক্টরের সব শেয়ার ও চার্ট খুলে যাবে:"
    "</div>",
    unsafe_allow_html=True
)

sorted_marquee_secs = sectors_df.sort_values(tf_selected, ascending=False)
marquee_chips = []
for _, srow in sorted_marquee_secs.iterrows():
    sname = srow["Sector"]
    sval = srow[tf_selected]
    q_sec = urllib.parse.quote(sname)
    is_pos = sval >= 0
    chip_cls = "sector-chip sector-chip-up" if is_pos else "sector-chip sector-chip-down"
    arrow = "▲" if is_pos else "▼"
    dot = "🟢" if is_pos else "🔴"
    marquee_chips.append(
        f'<a class="{chip_cls}" href="?focus_sector={q_sec}" target="_self">'
        f'{dot} {sname}: {arrow} {sval:+.2f}% 🔍'
        f'</a>'
    )

marquee_inner = "".join(marquee_chips) * 2
st.markdown(
    f"""
    <div class="sector-marquee-box">
        <div class="sector-marquee-track">{marquee_inner}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# ১৩. ৪টি প্রধান সামারি KPI কার্ড এবং তাদের ওয়ার্কিং অ্যাকশন বাটন
# ==============================================================================
adv_tf = int((stocks_df[tf_selected] > 0).sum())
dec_tf = int((stocks_df[tf_selected] < 0).sum())
pct_above_50 = round((stocks_df["Above_50DMA"].sum() / len(stocks_df)) * 100.0, 1)

top_sec_row = sectors_df.sort_values(tf_selected, ascending=False).iloc[0]
bot_sec_row = sectors_df.sort_values(tf_selected, ascending=True).iloc[0]

nifty_tf_val = nifty_d["chg_1w"] if tf_selected == "1W" else nifty_d["chg_1d"]

k_col1, k_col2, k_col3, k_col4 = st.columns(4)

with k_col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Nifty 50 Benchmark ({tf_selected})</div>
            <div class="kpi-main" style="color:{'#34d399' if nifty_tf_val>=0 else '#f87171'};">
                {nifty_tf_val:+.2f}%
            </div>
            <div class="{'kpi-badge-up' if nifty_tf_val>=0 else 'kpi-badge-down'}">
                1W: {nifty_d['chg_1w']:+.2f}% | 1Y: {nifty_d['chg_1y']:+.1f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("📊 নিফটি ও মার্কেট মুভার্স লিস্ট দেখুন", key="btn_kpi_1", use_container_width=True):
        st.session_state.active_modal = "movers" if st.session_state.active_modal != "movers" else None

with k_col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">মার্কেট ব্রেডথ ({tf_selected} Adv vs Dec)</div>
            <div class="kpi-main">
                <span style="color:#34d399;">🟢 {adv_tf} উপরে</span> | <span style="color:#f87171;">🔴 {dec_tf} নিচে</span>
            </div>
            <div class="kpi-badge-up">
                {pct_above_50}% শেয়ার 50-DMA এর উপরে
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("📈 বাড়তে থাকা ও ডাউন শেয়ার দেখুন", key="btn_kpi_2", use_container_width=True):
        st.session_state.active_modal = "breadth" if st.session_state.active_modal != "breadth" else None

with k_col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">টপ লিডার সেক্টর ({tf_selected})</div>
            <div class="kpi-main">👑 {top_sec_row['Sector']}</div>
            <div class="kpi-badge-up">
                ▲ {top_sec_row[tf_selected]:+.2f}% (Meter: {top_sec_row['Meter']})
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(f"🔍 {top_sec_row['Sector']}-এর শেয়ার দেখুন", key="btn_kpi_3", use_container_width=True):
        st.session_state.selected_sector = top_sec_row["Sector"]
        st.rerun()

with k_col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">সবচেয়ে ডাউন সেক্টর ({tf_selected})</div>
            <div class="kpi-main">📉 {bot_sec_row['Sector']}</div>
            <div class="kpi-badge-down">
                ▼ {bot_sec_row[tf_selected]:+.2f}% (Turnaround Watch)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(f"🔍 {bot_sec_row['Sector']}-এর শেয়ার দেখুন", key="btn_kpi_4", use_container_width=True):
        st.session_state.selected_sector = bot_sec_row["Sector"]
        st.rerun()

# KPI বাটনের পপ-আপ / এক্সপান্ডেবল ডিটেইল ভিউ
if st.session_state.active_modal == "movers":
    with st.expander("📊 টপ ১০ গেইনার এবং টপ ১০ লুজার শেয়ার (ক্লিক করে বন্ধ করুন)", expanded=True):
        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown("#### 🚀 টপ ১০ গেইনার")
            st.dataframe(
                stocks_df.sort_values(tf_selected, ascending=False)[["Symbol", "Sector", "Price", tf_selected, "Vol_Ratio", "RSI"]].head(10),
                use_container_width=True, hide_index=True
            )
        with mc2:
            st.markdown("#### 📉 টপ ১০ লুজার")
            st.dataframe(
                stocks_df.sort_values(tf_selected, ascending=True)[["Symbol", "Sector", "Price", tf_selected, "Vol_Ratio", "RSI"]].head(10),
                use_container_width=True, hide_index=True
            )
elif st.session_state.active_modal == "breadth":
    with st.expander("📈 মার্কেট ব্রেডথ বিশ্লেষণ: 50-DMA এর উপরে ও নিচে থাকা শেয়ার", expanded=True):
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown("#### 🟢 50-DMA এর উপরে থাকা শক্তিশালী শেয়ার")
            st.dataframe(
                stocks_df[stocks_df["Above_50DMA"]].sort_values("Vol_Ratio", ascending=False)[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI"]].head(15),
                use_container_width=True, hide_index=True
            )
        with bc2:
            st.markdown("#### 🔴 50-DMA এর নিচে থাকা ওভারসোল্ড শেয়ার")
            st.dataframe(
                stocks_df[~stocks_df["Above_50DMA"]].sort_values("RSI", ascending=True)[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI"]].head(15),
                use_container_width=True, hide_index=True
            )

st.markdown('<div id="sector-matrix-section"></div>', unsafe_allow_html=True)

# ==============================================================================
# ১৪. ৪টি প্রফেশনাল টার্মিনাল ট্যাব
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🧭 ১. ৩২ সেক্টর রোটেশন ও অ্যানালগ মিটার",
    "🎯 ২. ইন্ট্রাডে ডজি ও টার্নঅ্যারাউন্ড স্ক্যানার (Bullish & Bearish)",
    "📈 ৩. সুইং ও পজিশনাল স্ক্যানার (20/50 DMA Support)",
    "📋 ৪. ৩২ সেক্টরের পূর্ণাঙ্গ তুলনামূলক ম্যাট্রিক্স"
])

# ------------------------------------------------------------------------------
# ট্যাব ১: ৩২ সেক্টর কার্ড, রোটেশন মিটার ও সেক্টর ড্রিলডাউন
# ------------------------------------------------------------------------------
with tab1:
    view_sec_df = sectors_df.copy()

    # জোন ফিল্টার প্রয়োগ
    if zone_selected != "🌐 সব সেক্টর (All 32 Sectors)":
        view_sec_df = view_sec_df[view_sec_df["Zone"] == zone_selected]

    # নির্দিষ্ট সেক্টর ফিল্টার প্রয়োগ
    if st.session_state.selected_sector != "সবগুলো সেক্টর (Show All 32)":
        view_sec_df = view_sec_df[view_sec_df["Sector"] == st.session_state.selected_sector]
        if st.button("🔄 সবগুলো সেক্টর আবার একসাথে দেখুন (Reset Sector Filter)"):
            st.session_state.selected_sector = "সবগুলো সেক্টর (Show All 32)"
            st.rerun()

    # সর্টিং প্রয়োগ
    if "Top Gainers" in sort_selected:
        view_sec_df = view_sec_df.sort_values(tf_selected, ascending=False)
    elif "Top Losers" in sort_selected:
        view_sec_df = view_sec_df.sort_values(tf_selected, ascending=True)
    elif "Bottom Turnaround" in sort_selected:
        view_sec_df = view_sec_df.sort_values(["Bull_Turnaround", "1D"], ascending=[False, False])
    elif "Volume Shockers" in sort_selected:
        view_sec_df = view_sec_df.sort_values("Avg_Vol_Ratio", ascending=False)
    else:
        view_sec_df = view_sec_df.sort_values("Meter", ascending=False)

    def render_svg_gauge(score: int) -> str:
        """হালকা ও দ্রুতগতির SVG অ্যানালগ মিটার যা পিসি কখনোই স্লো করবে না"""
        angle = -90 + (score * 1.8)
        col = "#10b981" if score >= 60 else ("#fbbf24" if score >= 40 else "#ef4444")
        return f"""
        <div style="text-align:center; margin:4px 0;">
            <svg width="120" height="68" viewBox="0 0 120 68">
                <path d="M 12 58 A 48 48 0 0 1 108 58" fill="none" stroke="#1e293b" stroke-width="10" stroke-linecap="round"/>
                <path d="M 12 58 A 48 48 0 0 1 42 16" fill="none" stroke="#ef4444" stroke-width="6" stroke-linecap="round" opacity="0.7"/>
                <path d="M 42 16 A 48 48 0 0 1 78 16" fill="none" stroke="#fbbf24" stroke-width="6" stroke-linecap="round" opacity="0.7"/>
                <path d="M 78 16 A 48 48 0 0 1 108 58" fill="none" stroke="#10b981" stroke-width="6" stroke-linecap="round" opacity="0.7"/>
                <g transform="translate(60, 58) rotate({angle})">
                    <line x1="0" y1="0" x2="0" y2="-40" stroke="{col}" stroke-width="3.2" stroke-linecap="round"/>
                    <circle cx="0" cy="0" r="4.5" fill="{col}"/>
                </g>
                <text x="60" y="54" text-anchor="middle" fill="{col}" font-size="12" font-weight="800">{score}</text>
            </svg>
        </div>
        """

    grid_cols = st.columns(3)
    for idx, (_, srow) in enumerate(view_sec_df.iterrows()):
        sec_name = srow["Sector"]
        sec_ret = srow[tf_selected]
        sec_stocks = stocks_df[stocks_df["Sector"] == sec_name].sort_values("1D", ascending=False)
        gauge_html = render_svg_gauge(int(srow["Meter"])) if show_analog_meter else ""

        stock_chips = []
        for _, st_r in sec_stocks.iterrows():
            q_t = urllib.parse.quote(st_r["Ticker"])
            s_col = "#34d399" if st_r["1D"] >= 0 else "#f87171"
            pat_icon = "🕯️" if (pd.notna(st_r["Bull_Pattern"]) or pd.notna(st_r["Bear_Pattern"])) else ""
            stock_chips.append(
                f'<a href="?focus_stock={q_t}" target="_self" '
                f'style="text-decoration:none; background:rgba(255,255,255,0.05); border:1px solid {s_col}55; '
                f'color:{s_col}; padding:3px 8px; border-radius:8px; font-size:0.75rem; font-weight:700;">'
                f'{st_r["Symbol"]} ({st_r["1D"]:+.1f}% | {st_r["Vol_Ratio"]}x) {pat_icon}</a>'
            )

        with grid_cols[idx % 3]:
            st.markdown(
                f"""
                <div class="sec-card">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div style="font-size:1.02rem; font-weight:800;">{sec_name}</div>
                            <div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">{srow['Zone']}</div>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:1.08rem; font-weight:800; color:{'#34d399' if sec_ret>=0 else '#f87171'};">
                                {sec_ret:+.2f}%
                            </span>
                            <div style="font-size:0.72rem; color:#94a3b8;">1D: {srow['1D']:+.2f}% | 1W: {srow['1W']:+.2f}%</div>
                        </div>
                    </div>
                    {gauge_html}
                    <div style="display:flex; justify-content:space-between; font-size:0.76rem; color:#94a3b8; margin:6px 0 8px 0;">
                        <span>📊 Avg Vol: <b>{srow['Avg_Vol_Ratio']}x</b></span>
                        <span>⚡ RSI: <b>{srow['Avg_RSI']}</b></span>
                        <span>📈 >50DMA: <b>{srow['Breadth_50DMA']}%</b></span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:5px; margin-top:6px;">
                        {"".join(stock_chips)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ------------------------------------------------------------------------------
# ট্যাব ২: ইন্ট্রাডে ডজি ও টার্নঅ্যারাউন্ড স্ক্যানার (পূর্ণাঙ্গ ট্রেডিং টেবিল)
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("#### 🎯 ইন্ট্রাডে ডজি, কনসোলিডেশন ও সেক্টর টার্নঅ্যারাউন্ড স্ক্যানার (Entry, SL ও Target সহ)")

    sc_col1, sc_col2 = st.columns(2)
    with sc_col1:
        st.markdown("##### 🟢 বুলিশ রিভার্সাল ও ডজি কনসোলিডেশন শেয়ার (Buy Radar)")
        bull_table = bull_focus_df[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Consec_Up", "Bull_Pattern", "ATR"]].copy()
        bull_table["Entry (₹)"] = (bull_table["Price"] * 1.001).round(2)
        bull_table["StopLoss (₹)"] = (bull_table["Price"] - 1.2 * bull_table["ATR"]).round(2)
        bull_table["Target 1 (₹)"] = (bull_table["Price"] + 1.6 * bull_table["ATR"]).round(2)
        st.dataframe(
            bull_table.drop(columns=["ATR"]),
            use_container_width=True,
            hide_index=True
        )

    with sc_col2:
        st.markdown("##### 🔴 বেয়ারিশ ব্রেকডাউন ও টপ স্টল শেয়ার (Short Radar)")
        bear_table = bear_focus_df[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Consec_Down", "Bear_Pattern", "ATR"]].copy()
        bear_table["Short Below (₹)"] = (bear_table["Price"] * 0.999).round(2)
        bear_table["StopLoss (₹)"] = (bear_table["Price"] + 1.2 * bear_table["ATR"]).round(2)
        bear_table["Target 1 (₹)"] = (bear_table["Price"] - 1.6 * bear_table["ATR"]).round(2)
        st.dataframe(
            bear_table.drop(columns=["ATR"]),
            use_container_width=True,
            hide_index=True
        )

    # ১-ক্লিকে ওয়াচলিস্ট এক্সপোর্ট
    tv_bull_list = ",".join([f"NSE:{s}" for s in bull_focus_df["Symbol"].tolist()])
    tv_bear_list = ",".join([f"NSE:{s}" for s in bear_focus_df["Symbol"].tolist()])
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            "📥 বুলিশ ফোকাস ওয়াচলিস্ট ডাউনলোড করুন (TradingView .txt)",
            data=tv_bull_list,
            file_name="alphapulse_bullish_intraday.txt",
            mime="text/plain",
            use_container_width=True
        )
    with dl2:
        st.download_button(
            "📥 বেয়ারিশ ফোকাস ওয়াচলিস্ট ডাউনলোড করুন (TradingView .txt)",
            data=tv_bear_list,
            file_name="alphapulse_bearish_intraday.txt",
            mime="text/plain",
            use_container_width=True
        )

# ------------------------------------------------------------------------------
# ট্যাব ৩: সুইং ও পজিশনাল স্ক্যানার (20-DMA Pullback & Volume Buildup)
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("#### 📈 সুইং ও পজিশনাল ট্রেডিং রাডার (20-DMA সাপোর্টের কাছে কনসোলিডেট করা ও ভলিউম বাড়তে থাকা শেয়ার)")
    swing_df = stocks_df[
        (stocks_df["Above_50DMA"]) &
        (stocks_df["Dist_20DMA"] >= -3.5) &
        (stocks_df["Dist_20DMA"] <= 4.5) &
        (stocks_df["RSI"] >= 42) &
        (stocks_df["RSI"] <= 66) &
        (stocks_df["Vol_Ratio"] >= 1.0)
    ].sort_values("Vol_Ratio", ascending=False)

    st.dataframe(
        swing_df[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "DMA20", "DMA50", "Dist_20DMA", "Bull_Pattern"]],
        use_container_width=True,
        hide_index=True
    )

# ------------------------------------------------------------------------------
# ট্যাব ৪: ৩২ সেক্টরের পূর্ণাঙ্গ তুলনামূলক ম্যাট্রিক্স
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("#### 📋 ৩২টি সেক্টরের মাল্টি-টাইমফ্রেম রোটেশন ম্যাট্রিক্স (1D থেকে 1Y)")
    st.dataframe(
        sectors_df.sort_values(tf_selected, ascending=False)[
            ["Sector", "Zone", "Meter", "1D", "1W", "1M", "3M", "6M", "1Y", "Avg_Vol_Ratio", "Avg_RSI", "Breadth_50DMA"]
        ],
        use_container_width=True,
        hide_index=True
    )

# ==============================================================================
# ১৫. ফ্লোটিং ‘ওপরে যান (Top)’ ও কুইক নেভিগেশন বার (১০০% কার্যকরী ও নন-ওভারল্যাপিং)
# ==============================================================================
components.html(
    """
    <script>
    (function() {
        const parentDoc = window.parent.document;
        const oldNav = parentDoc.getElementById("alphapulse-floating-dock");
        if (oldNav) {
            oldNav.remove();
        }

        const dock = parentDoc.createElement("div");
        dock.id = "alphapulse-floating-dock";
        dock.style.cssText = `
            position: fixed;
            bottom: 64px;
            right: 22px;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            gap: 8px;
        `;

        function createJumpBtn(label, bgGradient, targetId) {
            const btn = parentDoc.createElement("button");
            btn.innerHTML = label;
            btn.style.cssText = `
                background: ${bgGradient};
                color: #ffffff;
                border: 1px solid rgba(255,255,255,0.25);
                border-radius: 999px;
                padding: 9px 16px;
                font-size: 13px;
                font-weight: 800;
                cursor: pointer;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                font-family: sans-serif;
            `;
            btn.onmouseenter = () => { btn.style.transform = "translateY(-2px) scale(1.04)"; };
            btn.onmouseleave = () => { btn.style.transform = "translateY(0) scale(1)"; };
            btn.onclick = () => {
                if (targetId === "TOP") {
                    const anchor = parentDoc.getElementById("alphapulse-top");
                    if (anchor) anchor.scrollIntoView({ behavior: "smooth", block: "start" });
                    const containers = [
                        parentDoc.querySelector('[data-testid="stAppViewContainer"]'),
                        parentDoc.querySelector('[data-testid="stMain"]'),
                        parentDoc.querySelector('section.main'),
                        parentDoc.documentElement,
                        parentDoc.body
                    ];
                    containers.forEach(el => {
                        if (el) el.scrollTo({ top: 0, behavior: "smooth" });
                    });
                    window.parent.scrollTo({ top: 0, behavior: "smooth" });
                } else {
                    const el = parentDoc.getElementById(targetId);
                    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
                }
            };
            return btn;
        }

        const topBtn = createJumpBtn("🚀 ওপরে যান (Top)", "linear-gradient(135deg, #0284c7, #2563eb)", "TOP");
        const focusBtn = createJumpBtn("🎯 ইন্ট্রাডে ফোকাস", "linear-gradient(135deg, #059669, #10b981)", "intraday-focus-section");

        dock.appendChild(focusBtn);
        dock.appendChild(topBtn);
        parentDoc.body.appendChild(dock);
    })();
    </script>
    """,
    height=0,
    width=0
)
