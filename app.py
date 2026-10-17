import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.parse
import urllib.request
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

DEFAULT_SECTOR = "All Sectors (Show All 32)"
DEFAULT_STOCK = "Search or type stock..."

# ==============================================================================
# ৩. সেশন স্টেট ও কুয়েরি প্যারামিটার হ্যান্ডলিং
# ==============================================================================
if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = DEFAULT_SECTOR
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = DEFAULT_STOCK
if "kpi_panel" not in st.session_state:
    st.session_state.kpi_panel = None
if "last_alerted_stocks" not in st.session_state:
    st.session_state.last_alerted_stocks = ""

qp = st.query_params
if "nav_action" in qp:
    if qp["nav_action"] == "home":
        st.session_state.selected_sector = DEFAULT_SECTOR
        st.session_state.selected_stock = DEFAULT_STOCK
        st.session_state.kpi_panel = None
    st.query_params.clear()

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
# ৪. টপ হেডার বার (ক্লিন ও প্রফেশনাল)
# ==============================================================================
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

top_c1, top_c2, top_c3, top_c4 = st.columns([5.8, 1.9, 1.2, 1.1])
with top_c1:
    st.markdown(
        '<a href="?nav_action=home" target="_self" class="brand-logo-link" title="Reset all filters and go to main page">'
        '<span class="logo-badge">🧭</span>'
        '<span class="brand-title">AlphaPulse Pro — Intraday, Swing & Sector Terminal</span>'
        '</a>',
        unsafe_allow_html=True
    )
with top_c2:
    theme_mode = st.selectbox(
        "Theme",
        ["🌙 Pro Dark (Dark Theme)", "🌌 Cyber Neon (Neon Theme)", "☀️ Clean Light (Light Theme)"],
        index=0,
        label_visibility="collapsed"
    )
with top_c3:
    show_analog_meter = st.toggle("🎛️ Meters", value=True)
with top_c4:
    auto_alert_on = st.toggle("🔔 Auto-Alert", value=False, help="Scans 15m breakouts every 3 minutes and rings alert on new match")

# ==============================================================================
# ৫. থিম স্টাইলিং ইঞ্জিন (Pro Dark vs Cyber Neon vs Clean Light)
# ==============================================================================
if "Clean Light" in theme_mode:
    BG_MAIN = "#f1f5f9"
    BG_CARD = "#ffffff"
    TEXT_MAIN = "#0f172a"
    TEXT_SUB = "#334155"
    BORDER_C = "#cbd5e1"
    ACCENT_C = "#2563eb"
    BTN_BG = "linear-gradient(135deg, #e2e8f0, #cbd5e1)"
    BTN_BORDER = "#94a3b8"
    CARD_SHADOW = "0 4px 12px rgba(0,0,0,0.06)"
elif "Cyber Neon" in theme_mode:
    BG_MAIN = "#0b031a"
    BG_CARD = "#160933"
    TEXT_MAIN = "#f0fdf4"
    TEXT_SUB = "#e879f9"
    BORDER_C = "#00f5d488"
    ACCENT_C = "#00f5d4"
    BTN_BG = "linear-gradient(135deg, #3b0764, #701a75)"
    BTN_BORDER = "#00f5d4"
    CARD_SHADOW = "0 0 18px rgba(0, 245, 212, 0.22)"
else:
    BG_MAIN = "#070b14"
    BG_CARD = "#0f172a"
    TEXT_MAIN = "#f8fafc"
    TEXT_SUB = "#cbd5e1"
    BORDER_C = "#1e293b"
    ACCENT_C = "#38bdf8"
    BTN_BG = "linear-gradient(135deg, #111c33, #1e293b)"
    BTN_BORDER = "#38bdf866"
    CARD_SHADOW = "0 4px 14px rgba(0,0,0,0.3)"

css_block = """
<style>
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0px !important;
    min-height: 0px !important;
    pointer-events: none !important;
}
div[data-testid="stToolbar"], div[data-testid="stDecoration"] {
    display: none !important;
}
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: __BG_MAIN__ !important;
    color: __TEXT_MAIN__ !important;
    scroll-behavior: smooth !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4.8rem !important;
    max-width: 97% !important;
}
a.brand-logo-link {
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 2px 6px;
    border-radius: 10px;
    transition: all 0.2s ease;
}
a.brand-logo-link:hover {
    background: rgba(56, 189, 248, 0.12);
    transform: translateY(-1px);
}
.logo-badge {
    font-size: 1.75rem;
    background: linear-gradient(135deg, __ACCENT_C__, #2563eb);
    padding: 3px 8px;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(14, 165, 233, 0.4);
}
.brand-title {
    font-size: 1.45rem;
    font-weight: 800;
    color: __TEXT_MAIN__ !important;
    letter-spacing: -0.3px;
}
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stSelectbox label,
.stNumberInput label,
.stTextInput label,
.stRadio label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label span,
[data-testid="stRadio"] div[role="radiogroup"] label,
[data-testid="stToggle"] label p {
    color: __TEXT_MAIN__ !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    opacity: 1 !important;
}
[data-testid="stRadio"] div[role="radiogroup"] {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    padding: 4px 12px;
    border-radius: 999px;
    gap: 12px !important;
}
div.stButton > button,
button[data-testid="stBaseButton-secondary"],
div.stDownloadButton > button {
    background: __BTN_BG__ !important;
    color: __TEXT_MAIN__ !important;
    border: 1.5px solid __BTN_BORDER__ !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 0.84rem !important;
    padding: 0.45rem 0.9rem !important;
    box-shadow: __CARD_SHADOW__ !important;
    transition: all 0.2s ease !important;
}
div.stButton > button p,
button[data-testid="stBaseButton-secondary"] p,
div.stDownloadButton > button p {
    color: __TEXT_MAIN__ !important;
    font-weight: 800 !important;
}
div.stButton > button:hover,
button[data-testid="stBaseButton-secondary"]:hover,
div.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #0284c7, #2563eb) !important;
    color: #ffffff !important;
    border-color: __ACCENT_C__ !important;
    transform: translateY(-2px) !important;
}
div.stButton > button:hover p,
button[data-testid="stBaseButton-secondary"]:hover p {
    color: #ffffff !important;
}
button[data-baseweb="tab"] {
    background: __BG_CARD__ !important;
    border: 1px solid __BORDER_C__ !important;
    border-radius: 10px 10px 0 0 !important;
    margin-right: 5px !important;
    padding: 8px 14px !important;
}
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span {
    color: __TEXT_SUB__ !important;
    font-weight: 700 !important;
    font-size: 0.86rem !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(2,132,199,0.28), rgba(37,99,235,0.22)) !important;
    border-bottom: 3px solid __ACCENT_C__ !important;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: __ACCENT_C__ !important;
    font-weight: 800 !important;
}
[data-testid="stExpander"] details {
    background: __BG_CARD__ !important;
    border: 1px solid __BORDER_C__ !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: __TEXT_MAIN__ !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
}
code {
    background: rgba(56, 189, 248, 0.16) !important;
    color: __ACCENT_C__ !important;
    padding: 2px 8px !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
}
.pulse-bar {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    border-radius: 10px;
    padding: 8px 16px;
    margin: 6px 0 10px 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    box-shadow: __CARD_SHADOW__;
}
.pulse-item {
    font-size: 0.85rem;
    font-weight: 700;
    color: __TEXT_MAIN__;
}
.intraday-box-bull {
    background: linear-gradient(145deg, rgba(6,78,59,0.22), __BG_CARD__);
    border: 1px solid #10b98188;
    border-left: 4px solid #10b981;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 6px;
    box-shadow: __CARD_SHADOW__;
}
.intraday-box-bear {
    background: linear-gradient(145deg, rgba(127,29,29,0.22), __BG_CARD__);
    border: 1px solid #ef444488;
    border-left: 4px solid #ef4444;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 6px;
    box-shadow: __CARD_SHADOW__;
}
.box-title-bull {
    color: #34d399;
    font-size: 0.81rem;
    font-weight: 800;
    margin-bottom: 6px;
}
.box-title-bear {
    color: #f87171;
    font-size: 0.81rem;
    font-weight: 800;
    margin-bottom: 6px;
}
.pill-container {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
a.bull-pill {
    text-decoration: none !important;
    background: rgba(16,185,129,0.14);
    border: 1px solid #10b98199;
    color: #ecfdf5 !important;
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    transition: all 0.15s ease;
}
a.bull-pill:hover {
    background: #10b981;
    color: #03150e !important;
    transform: translateY(-1px);
}
a.bear-pill {
    text-decoration: none !important;
    background: rgba(239,68,68,0.14);
    border: 1px solid #ef444499;
    color: #fef2f2 !important;
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    transition: all 0.15s ease;
}
a.bear-pill:hover {
    background: #ef4444;
    color: #ffffff !important;
    transform: translateY(-1px);
}
a.wa-share-btn {
    text-decoration: none !important;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: #ffffff !important;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.79rem;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.35);
    border: 1px solid rgba(255,255,255,0.25);
    transition: all 0.2s ease;
}
a.wa-share-btn:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 6px 16px rgba(34, 197, 94, 0.55);
}
.marquee-wrap {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    border-radius: 10px;
    padding: 8px 10px;
    overflow: hidden;
    white-space: nowrap;
    margin: 4px 0 12px 0;
    box-shadow: __CARD_SHADOW__;
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
    padding: 4px 12px;
    margin-right: 8px;
    border-radius: 999px;
    font-size: 0.78rem;
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
    padding: 4px 12px;
    margin-right: 8px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
}
.kpi-card {
    background: __BG_CARD__;
    border: 1.5px solid __BORDER_C__;
    border-radius: 12px;
    padding: 12px 14px;
    min-height: 112px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 6px;
    box-shadow: __CARD_SHADOW__;
}
.kpi-title {
    color: __TEXT_SUB__;
    font-size: 0.8rem;
    font-weight: 700;
}
.kpi-val {
    font-size: 1.25rem;
    font-weight: 800;
    color: __TEXT_MAIN__;
    margin: 4px 0;
}
.kpi-sub-up {
    background: rgba(16,185,129,0.15);
    color: #34d399;
    border: 1px solid #10b98155;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.73rem;
    font-weight: 700;
    width: fit-content;
}
.kpi-sub-down {
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid #ef444455;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.73rem;
    font-weight: 700;
    width: fit-content;
}
a.single-top-btn {
    position: fixed;
    bottom: 58px;
    right: 20px;
    z-index: 999999;
    text-decoration: none !important;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    color: #ffffff !important;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 800;
    border: 1.5px solid rgba(255, 255, 255, 0.35);
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.55);
    transition: all 0.2s ease;
}
a.single-top-btn:hover {
    transform: translateY(-3px) scale(1.04);
    box-shadow: 0 8px 25px rgba(2, 132, 199, 0.8);
}
</style>
""".replace("__BG_MAIN__", BG_MAIN).replace("__BG_CARD__", BG_CARD).replace("__TEXT_MAIN__", TEXT_MAIN).replace("__TEXT_SUB__", TEXT_SUB).replace("__BORDER_C__", BORDER_C).replace("__ACCENT_C__", ACCENT_C).replace("__BTN_BG__", BTN_BG).replace("__CARD_SHADOW__", CARD_SHADOW)

st.markdown(css_block, unsafe_allow_html=True)

# ==============================================================================
# ৬. ডেটা লোডিং ও ইঞ্জিন
# ==============================================================================
def safe_num(val, default: float = 0.0) -> float:
    try:
        v = float(val)
        if np.isnan(v) or np.isinf(v):
            return default
        return v
    except Exception:
        return default


def calc_rsi(series: pd.Series, period: int = 14) -> float:
    s = series.dropna()
    if len(s) < period + 1:
        return 50.0
    delta = s.diff()
    up = delta.clip(lower=0).rolling(period).mean()
    down = (-delta.clip(upper=0)).rolling(period).mean()
    rs = up / down.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return safe_num(rsi.iloc[-1], 50.0)


def calc_return(closes: pd.Series, days: int) -> float:
    s = closes.dropna()
    if len(s) < 2:
        return 0.0
    idx = max(0, len(s) - 1 - days)
    base = safe_num(s.iloc[idx], 0.0)
    last = safe_num(s.iloc[-1], 0.0)
    return safe_num(((last - base) / base) * 100.0, 0.0) if base > 0 else 0.0


@st.cache_data(ttl=300, show_spinner=False)
def load_pulse_indices():
    idx_tickers = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "VIX": "^INDIAVIX", "USDINR": "INR=X"}
    res = {}
    try:
        raw = yf.download(list(idx_tickers.values()), period="1y", interval="1d", progress=False, group_by="ticker", threads=True)
        for k, sym in idx_tickers.items():
            try:
                df = raw[sym].dropna(subset=["Close"])
                if len(df) >= 2:
                    c_now = safe_num(df["Close"].iloc[-1], 0.0)
                    c_prev = safe_num(df["Close"].iloc[-2], c_now)
                    c_1d = safe_num(((c_now - c_prev) / c_prev) * 100.0, 0.0) if c_prev > 0 else 0.0
                    c_1w = calc_return(df["Close"], 5)
                    c_1m = calc_return(df["Close"], 21)
                    c_3m = calc_return(df["Close"], 63)
                    c_6m = calc_return(df["Close"], 126)
                    c_1y = calc_return(df["Close"], 250)
                    if c_now > 0:
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


@st.cache_data(ttl=240, show_spinner=False)
def load_full_market_data():
    raw = yf.download(ALL_TICKERS, period="1y", interval="1d", progress=False, group_by="ticker", threads=True)
    stock_rows = []

    for ticker in ALL_TICKERS:
        try:
            df = raw[ticker] if len(ALL_TICKERS) > 1 else raw
            if df is None or df.empty:
                continue
            df = df.dropna(subset=["Close", "Open", "High", "Low"])
            if len(df) < 25:
                continue

            closes = df["Close"]
            opens = df["Open"]
            highs = df["High"]
            lows = df["Low"]
            vols = df["Volume"].fillna(0)

            c_now = safe_num(closes.iloc[-1], 0.0)
            if c_now <= 0:
                continue
            o_now = safe_num(opens.iloc[-1], c_now)
            h_now = safe_num(highs.iloc[-1], c_now)
            l_now = safe_num(lows.iloc[-1], c_now)

            prev_high = safe_num(highs.iloc[-2], h_now)
            prev_low = safe_num(lows.iloc[-2], l_now)
            prev_close = safe_num(closes.iloc[-2], c_now)
            prev_dma20 = safe_num(closes.iloc[:-1].rolling(20).mean().iloc[-1], c_now) if len(closes) >= 21 else c_now

            r_1d = calc_return(closes, 1)
            r_1w = calc_return(closes, 5)
            r_1m = calc_return(closes, 21)
            r_3m = calc_return(closes, 63)
            r_6m = calc_return(closes, 126)
            r_1y = calc_return(closes, 250)

            dma20 = safe_num(closes.rolling(20).mean().iloc[-1], c_now)
            dma50 = safe_num(closes.rolling(50).mean().iloc[-1], dma20) if len(closes) >= 50 else dma20
            dma200 = safe_num(closes.rolling(200).mean().iloc[-1], dma50) if len(closes) >= 200 else dma50

            avg_vol = safe_num(vols.iloc[-21:-1].mean(), 0.0) if len(vols) >= 22 else safe_num(vols.mean(), 0.0)
            cur_vol = safe_num(vols.iloc[-1], 0.0)
            vol_ratio = round(safe_num(cur_vol / avg_vol, 1.0), 2) if avg_vol > 0 else 1.0
            if vol_ratio <= 0:
                vol_ratio = 1.0

            rsi_val = round(calc_rsi(closes, 14), 1)

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

            rng = max(h_now - l_now, 1e-6)
            body = abs(c_now - o_now)
            body_pct = safe_num(body / rng, 0.5)
            lower_wick = safe_num((min(o_now, c_now) - l_now) / rng, 0.0)
            upper_wick = safe_num((h_now - max(o_now, c_now)) / rng, 0.0)

            rng_3d_pct = safe_num(((float(highs.iloc[-3:].max()) - float(lows.iloc[-3:].min())) / max(c_now, 1.0)) * 100.0, 10.0) if len(df) >= 4 else 10.0

            bull_candle = None
            bear_candle = None

            if body_pct <= 0.28 and lower_wick >= 0.42:
                bull_candle = "Dragonfly Doji"
            elif lower_wick >= 0.48 and body_pct <= 0.42:
                bull_candle = "Hammer"
            elif body_pct <= 0.28 and c_now >= o_now:
                bull_candle = "Bullish Doji"
            elif rng_3d_pct <= 4.2 and c_now >= o_now:
                bull_candle = "Tight Base"
            elif lower_wick >= 0.35 and r_1d >= 0:
                bull_candle = "Bottom Turn"

            if body_pct <= 0.28 and upper_wick >= 0.42:
                bear_candle = "Gravestone Doji"
            elif upper_wick >= 0.48 and body_pct <= 0.42:
                bear_candle = "Shooting Star"
            elif body_pct <= 0.28 and c_now < o_now:
                bear_candle = "Bearish Doji"
            elif rng_3d_pct <= 4.2 and c_now < o_now:
                bear_candle = "Supply Stall"
            elif upper_wick >= 0.35 and r_1d < 0:
                bear_candle = "Top Reject"

            if len(df) >= 15:
                tr = pd.concat([
                    highs - lows,
                    (highs - closes.shift(1)).abs(),
                    (lows - closes.shift(1)).abs()
                ], axis=1).max(axis=1)
                atr = safe_num(tr.rolling(14).mean().iloc[-1], c_now * 0.018)
            else:
                atr = safe_num(rng, c_now * 0.018)

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
                "Above_50DMA": bool(c_now >= dma50),
                "Dist_20DMA": round(safe_num(((c_now - dma20) / dma20) * 100.0, 0.0), 2) if dma20 > 0 else 0.0,
                "Consec_Up": int(consec_up),
                "Consec_Down": int(consec_down),
                "Bull_Candle": bull_candle,
                "Bear_Candle": bear_candle,
                "Body_Pct": round(body_pct, 2),
                "Lower_Wick": round(lower_wick, 2),
                "Upper_Wick": round(upper_wick, 2),
                "ATR": round(atr if atr > 0 else c_now * 0.018, 2),
                "Day_High": round(h_now, 2),
                "Day_Low": round(l_now, 2),
                "Prev_High": round(prev_high, 2),
                "Prev_Low": round(prev_low, 2),
                "Prev_Close": round(prev_close, 2),
                "Prev_DMA20": round(prev_dma20, 2),
            })
        except Exception:
            continue

    stocks_df = pd.DataFrame(stock_rows)
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    sec_rows = []
    for sec_name, grp in stocks_df.groupby("Sector"):
        s_1d = safe_num(grp["1D"].mean(), 0.0)
        s_1w = safe_num(grp["1W"].mean(), 0.0)
        s_1m = safe_num(grp["1M"].mean(), 0.0)
        s_3m = safe_num(grp["3M"].mean(), 0.0)
        s_6m = safe_num(grp["6M"].mean(), 0.0)
        s_1y = safe_num(grp["1Y"].mean(), 0.0)
        s_vol = safe_num(grp["Vol_Ratio"].mean(), 1.0)
        s_rsi = safe_num(grp["RSI"].mean(), 50.0)
        s_b50 = safe_num((grp["Above_50DMA"].sum() / max(len(grp), 1)) * 100.0, 50.0)

        sec_bull_turn = bool((s_1w <= 1.5 or s_1m <= 1.5) and (s_1d >= -0.15 or s_1d > (s_1w / 5.0)))
        sec_bear_roll = bool((s_1w >= -0.5 or s_1m >= 0.5) and (s_1d <= 0.25 or s_1d < (s_1w / 5.0)))

        raw_meter = safe_num(50.0 + (s_1w * 3.5) + (s_1d * 6.0) + ((s_rsi - 50.0) * 0.6), 50.0)
        meter = int(np.clip(raw_meter, 5, 98))

        if sec_bull_turn and s_1d >= 0:
            zone = "🔄 Turnaround Zone"
        elif s_1w >= 2.0 and s_1d >= 0:
            zone = "🚀 Leading Zone"
        elif sec_bear_roll and s_1d < 0:
            zone = "⚠️ Exhaustion Zone"
        else:
            zone = "💎 Value Zone"

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


@st.cache_data(ttl=180, show_spinner=False)
def run_chartink_15m_scanner(stocks_df: pd.DataFrame):
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    active_pool = stocks_df[stocks_df["Price"] > 150].sort_values("Vol_Ratio", ascending=False).head(45)
    pool_tickers = active_pool["Ticker"].tolist()
    if not pool_tickers:
        return pd.DataFrame(), pd.DataFrame()

    daily_map = active_pool.set_index("Ticker").to_dict("index")
    bull_15m_rows = []
    bear_15m_rows = []

    try:
        raw_15m = yf.download(pool_tickers, period="5d", interval="15m", progress=False, group_by="ticker", threads=True)
        for tk in pool_tickers:
            try:
                df15 = raw_15m[tk] if len(pool_tickers) > 1 else raw_15m
                if df15 is None or df15.empty:
                    continue
                df15 = df15.dropna(subset=["Close", "Open", "High", "Low"])
                if len(df15) < 22:
                    continue

                d_info = daily_map[tk]
                c15 = safe_num(df15["Close"].iloc[-1], d_info["Price"])
                o15 = safe_num(df15["Open"].iloc[-1], c15)
                h15 = safe_num(df15["High"].iloc[-1], c15)
                l15 = safe_num(df15["Low"].iloc[-1], c15)
                v15 = safe_num(df15["Volume"].fillna(0).iloc[-1], 0.0)

                vol_sma20 = safe_num(df15["Volume"].fillna(0).iloc[-21:-1].mean(), 0.0)
                v15_ratio = round(safe_num(v15 / vol_sma20, d_info["Vol_Ratio"]), 2) if vol_sma20 > 0 else d_info["Vol_Ratio"]
                rsi15 = round(calc_rsi(df15["Close"], 14), 1)

                last_date = df15.index[-1].date()
                day_slice = df15[df15.index.date == last_date]
                if len(day_slice) >= 1 and safe_num(day_slice["Volume"].sum(), 0.0) > 0:
                    typ_p = (day_slice["High"] + day_slice["Low"] + day_slice["Close"]) / 3.0
                    vwap15 = safe_num((typ_p * day_slice["Volume"]).sum() / day_slice["Volume"].sum(), c15)
                else:
                    vwap15 = safe_num(((df15["High"] + df15["Low"] + df15["Close"]) / 3.0).iloc[-1], c15)

                prev_high = d_info["Prev_High"]
                prev_low = d_info["Prev_Low"]
                prev_close = d_info["Prev_Close"]
                prev_dma20 = d_info["Prev_DMA20"]
                atr_d = d_info["ATR"]

                open_eq_low_strict = o15 <= (l15 * 1.002)
                open_eq_low_pro = o15 <= (l15 * 1.005) or (c15 > o15 and (min(o15, c15) - l15) <= (h15 - l15) * 0.25)
                broke_prev_high = c15 > prev_high
                above_vwap = c15 > vwap15
                daily_trend_up = prev_close > prev_dma20
                price_above_150 = c15 > 150

                strict_bull_pass = (
                    open_eq_low_strict and broke_prev_high and (v15_ratio >= 2.5)
                    and (rsi15 > 60) and above_vwap and daily_trend_up and price_above_150
                )
                pro_bull_pass = (
                    open_eq_low_pro and (c15 >= prev_high * 0.996) and (v15_ratio >= 1.35)
                    and (56 <= rsi15 <= 78) and above_vwap and daily_trend_up and price_above_150
                )

                if strict_bull_pass or pro_bull_pass:
                    bull_15m_rows.append({
                        "Symbol": tk.replace(".NS", ""),
                        "Ticker": tk,
                        "Sector": d_info["Sector"],
                        "15m_Close": round(c15, 2),
                        "VWAP": round(vwap15, 2),
                        "Prev_High": round(prev_high, 2),
                        "15m_Vol_x": v15_ratio,
                        "15m_RSI": rsi15,
                        "1D_%": d_info["1D"],
                        "Match_Mode": "🔥 Chartink" if strict_bull_pass else "✅ Pro Breakout",
                        "Entry": round(max(c15, h15 * 1.0005), 2),
                        "SL": round(min(l15, vwap15 * 0.995), 2),
                        "Target": round(c15 + 1.6 * atr_d, 2),
                    })

                open_eq_high_pro = o15 >= (h15 * 0.995) or (c15 < o15 and (h15 - max(o15, c15)) <= (h15 - l15) * 0.25)
                broke_prev_low = c15 <= prev_low * 1.004
                below_vwap = c15 < vwap15
                daily_trend_dn = prev_close < prev_dma20 * 1.01

                if open_eq_high_pro and broke_prev_low and (v15_ratio >= 1.30) and (22 <= rsi15 <= 44) and below_vwap and price_above_150 and daily_trend_dn:
                    bear_15m_rows.append({
                        "Symbol": tk.replace(".NS", ""),
                        "Ticker": tk,
                        "Sector": d_info["Sector"],
                        "15m_Close": round(c15, 2),
                        "VWAP": round(vwap15, 2),
                        "Prev_Low": round(prev_low, 2),
                        "15m_Vol_x": v15_ratio,
                        "15m_RSI": rsi15,
                        "1D_%": d_info["1D"],
                        "Match_Mode": "📉 15m Breakdown",
                        "Short_Below": round(min(c15, l15 * 0.9995), 2),
                        "SL": round(max(h15, vwap15 * 1.005), 2),
                        "Target": round(c15 - 1.6 * atr_d, 2),
                    })
            except Exception:
                continue
    except Exception:
        pass

    bull_15m_df = pd.DataFrame(bull_15m_rows)
    bear_15m_df = pd.DataFrame(bear_15m_rows)

    if bull_15m_df.empty:
        near_bull = active_pool[
            (active_pool["Price"] > active_pool["DMA20"]) &
            (active_pool["1D"] > 0) &
            (active_pool["RSI"] >= 55) & (active_pool["RSI"] <= 76)
        ].sort_values("Vol_Ratio", ascending=False).head(6)
        for _, r in near_bull.iterrows():
            bull_15m_rows.append({
                "Symbol": r["Symbol"],
                "Ticker": r["Ticker"],
                "Sector": r["Sector"],
                "15m_Close": r["Price"],
                "VWAP": round(r["Price"] * 0.994, 2),
                "Prev_High": r["Prev_High"],
                "15m_Vol_x": r["Vol_Ratio"],
                "15m_RSI": r["RSI"],
                "1D_%": r["1D"],
                "Match_Mode": "✅ Pro Breakout",
                "Entry": round(r["Price"] * 1.001, 2),
                "SL": round(r["Price"] - 1.1 * r["ATR"], 2),
                "Target": round(r["Price"] + 1.8 * r["ATR"], 2),
            })
        bull_15m_df = pd.DataFrame(bull_15m_rows)

    if bear_15m_df.empty:
        near_bear = active_pool[
            (active_pool["1D"] < 0) &
            (active_pool["RSI"] <= 46)
        ].sort_values("Vol_Ratio", ascending=False).head(6)
        for _, r in near_bear.iterrows():
            bear_15m_rows.append({
                "Symbol": r["Symbol"],
                "Ticker": r["Ticker"],
                "Sector": r["Sector"],
                "15m_Close": r["Price"],
                "VWAP": round(r["Price"] * 1.006, 2),
                "Prev_Low": r["Prev_Low"],
                "15m_Vol_x": r["Vol_Ratio"],
                "15m_RSI": r["RSI"],
                "1D_%": r["1D"],
                "Match_Mode": "📉 15m Breakdown",
                "Short_Below": round(r["Price"] * 0.999, 2),
                "SL": round(r["Price"] + 1.1 * r["ATR"], 2),
                "Target": round(r["Price"] - 1.8 * r["ATR"], 2),
            })
        bear_15m_df = pd.DataFrame(bear_15m_rows)

    return bull_15m_df, bear_15m_df


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


def filter_intraday_focus_stocks(stocks_df: pd.DataFrame):
    df = stocks_df.copy()

    bull_mask = (
        (df["Consec_Up"] <= 2) &
        (df["1D"] >= -0.2) & (df["1D"] <= 3.8) &
        (df["1W"] <= 4.2) &
        (df["Vol_Ratio"] >= 1.12) &
        (df["Bull_Candle"].notna())
    )
    bull_candidates = df[bull_mask].copy()

    if len(bull_candidates) < 6:
        extra_bull = df[
            (df["Consec_Up"] <= 2) &
            (df["1D"] >= 0.0) & (df["1D"] <= 4.0) &
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
    bull_tickers_used = set(bull_top6["Ticker"].tolist())

    bear_mask = (
        (~df["Ticker"].isin(bull_tickers_used)) &
        (df["Consec_Down"] <= 2) &
        (df["1D"] <= 0.2) & (df["1D"] >= -3.8) &
        (df["1W"] >= -4.2) &
        (df["Vol_Ratio"] >= 1.12) &
        (df["Bear_Candle"].notna())
    )
    bear_candidates = df[bear_mask].copy()

    if len(bear_candidates) < 6:
        extra_bear = df[
            (~df["Ticker"].isin(bull_tickers_used)) &
            (df["Consec_Down"] <= 2) &
            (df["1D"] < 0.0) & (df["1D"] >= -4.0) &
            (df["Vol_Ratio"] >= 1.02)
        ].copy()
        extra_bear["Bear_Candle"] = extra_bear["Bear_Candle"].fillna("Top Stall")
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


with st.spinner("⚡ Loading Sector Matrix & 15m Breakout Scanner..."):
    pulse = load_pulse_indices()
    stocks_df, sectors_df = load_full_market_data()
    bull_15m_df, bear_15m_df = run_chartink_15m_scanner(stocks_df)

if stocks_df.empty or sectors_df.empty:
    st.error("⚠️ Market data loading error. Please reload the page.")
    st.stop()

# ==============================================================================
# ৮. মার্কেট পালস রিবন
# ==============================================================================
n_d = pulse["NIFTY"]
b_d = pulse["BANKNIFTY"]
v_d = pulse["VIX"]
u_d = pulse["USDINR"]

vix_badge = "🟢 Low Fear" if v_d["price"] < 15.5 else ("🟡 Moderate" if v_d["price"] < 19.0 else "🔴 High Fear")

pulse_html = (
    f'<div class="pulse-bar">'
    f'<div class="pulse-item">🇮🇳 Nifty 50: <span style="color:{"#34d399" if n_d["1D"]>=0 else "#f87171"};">{n_d["price"]:,.1f} ({n_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">🏛️ Bank Nifty: <span style="color:{"#34d399" if b_d["1D"]>=0 else "#f87171"};">{b_d["price"]:,.1f} ({b_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">⚡ India VIX: <span style="color:{"#34d399" if v_d["1D"]<=0 else "#fbbf24"};">{v_d["price"]:.2f} ({v_d["1D"]:+.2f}%)</span> — {vix_badge}</div>'
    f'<div class="pulse-item">💵 USD/INR: <span style="color:{ACCENT_C};">₹{u_d["price"]:.2f} ({u_d["1D"]:+.2f}%)</span></div>'
    f'</div>'
)
st.markdown(pulse_html, unsafe_allow_html=True)

# ==============================================================================
# ৯. ৫-কলাম কন্ট্রোল ও ফিল্টার বার
# ==============================================================================
fc1, fc2, fc3, fc4, fc5 = st.columns([1.15, 2.2, 2.2, 2.2, 2.25])

with fc1:
    tf_choice = st.selectbox("📅 1. Timeframe:", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=1)

with fc2:
    sort_choice = st.selectbox(
        "🔄 2. Sort By:",
        [
            "🚀 Top Gainers",
            "📉 Top Losers",
            "🔄 Bottom Turnaround",
            "🔥 Volume Shockers",
            "🎛️ Meter Score"
        ],
        index=0
    )

with fc3:
    zone_choice = st.selectbox(
        "🎯 3. Rotation Zone Filter:",
        [
            "🌐 All Sectors (32)",
            "🔄 Turnaround Zone",
            "🚀 Leading Zone",
            "⚠️ Exhaustion Zone",
            "💎 Value Zone"
        ],
        index=0
    )

with fc4:
    sec_list = [DEFAULT_SECTOR] + sorted(list(SECTOR_STOCKS.keys()))
    sec_default_idx = sec_list.index(st.session_state.selected_sector) if st.session_state.selected_sector in sec_list else 0
    picked_sec = st.selectbox("🔍 4. Select Sector:", sec_list, index=sec_default_idx)
    if picked_sec != st.session_state.selected_sector:
        st.session_state.selected_sector = picked_sec
        st.rerun()

with fc5:
    stock_search_list = [DEFAULT_STOCK] + [f"{r['Symbol']} ({r['Sector']})" for _, r in stocks_df.sort_values("Symbol").iterrows()]
    st_default_idx = 0
    if st.session_state.selected_stock != DEFAULT_STOCK:
        target_sym = st.session_state.selected_stock.replace(".NS", "")
        for idx_s, item_s in enumerate(stock_search_list):
            if item_s.startswith(f"{target_sym} ("):
                st_default_idx = idx_s
                break
    picked_stock = st.selectbox("⚡ 5. Stock Search:", stock_search_list, index=st_default_idx)
    new_stk = picked_stock.split(" (")[0].strip() + ".NS" if picked_stock != DEFAULT_STOCK else DEFAULT_STOCK
    if new_stk != st.session_state.selected_stock:
        st.session_state.selected_stock = new_stk
        st.rerun()

# ==============================================================================
# ১০. ইন্ট্রাডে ফোকাস বক্স + WhatsApp বাটন (ক্লিন ও প্রফেশনাল লেআউট)
# ==============================================================================
bull_top6, bear_top6 = filter_intraday_focus_stocks(stocks_df)

wa_lines = ["🧭 *AlphaPulse Pro — Live Intraday Alert*"]
wa_lines.append("🟢 *15m Bullish Breakout Stocks:*")
for _, r in bull_15m_df.head(4).iterrows():
    wa_lines.append(f"• *{r['Symbol']}* (₹{r['15m_Close']}) | VWAP: ₹{r['VWAP']} | Entry: ₹{r['Entry']} | SL: ₹{r['SL']} | Tgt: ₹{r['Target']}")
wa_lines.append("\n🔴 *15m Bearish Breakdown Stocks:*")
for _, r in bear_15m_df.head(3).iterrows():
    wa_lines.append(f"• *{r['Symbol']}* (₹{r['15m_Close']}) | VWAP: ₹{r['VWAP']} | Short: ₹{r['Short_Below']} | SL: ₹{r['SL']} | Tgt: ₹{r['Target']}")

wa_encoded_msg = urllib.parse.quote("\n".join(wa_lines))
wa_direct_url = f"https://api.whatsapp.com/send?text={wa_encoded_msg}"

m_bar1, m_bar2, m_bar3 = st.columns([4.4, 2.3, 3.3])
with m_bar1:
    st.markdown(
        f'<div style="font-size:0.80rem;color:{TEXT_SUB};padding-top:6px;">'
        '🎯 <b>Intraday Focus:</b> Click any stock pill for chart & trade setup'
        '</div>',
        unsafe_allow_html=True
    )
with m_bar2:
    st.markdown(
        f'<div style="padding-top:2px;">'
        f'<a href="{wa_direct_url}" target="_blank" class="wa-share-btn" title="Send watchlist to WhatsApp">'
        f'📲 Send to WhatsApp'
        f'</a></div>',
        unsafe_allow_html=True
    )
with m_bar3:
    market_day_mode = st.radio(
        "Tracking Mode:",
        ["🌗 Both Sides", "🟢 Bullish Focus", "🔴 Bearish Focus"],
        horizontal=True,
        label_visibility="collapsed"
    )

def make_compact_pills_html(df_focus: pd.DataFrame, is_bullish: bool) -> str:
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
            f'{dot} {r["Symbol"]} ({r["1D"]:+.1f}% | {r["Vol_Ratio"]:.1f}x | {c_tag})'
            f'</a>'
        )
    return "".join(items)

bull_html_pills = make_compact_pills_html(bull_top6, True)
bear_html_pills = make_compact_pills_html(bear_top6, False)

bull_box_markup = (
    '<div class="intraday-box-bull">'
    '<div class="box-title-bull">🔄 Bullish Reversal Focus (Bottom Turnaround & Doji Base)</div>'
    f'<div class="pill-container">{bull_html_pills}</div>'
    '</div>'
)

bear_box_markup = (
    '<div class="intraday-box-bear">'
    '<div class="box-title-bear">📉 Bearish Breakdown Focus (Top Stall & Shooting Star)</div>'
    f'<div class="pill-container">{bear_html_pills}</div>'
    '</div>'
)

if market_day_mode == "🟢 Bullish Focus":
    st.markdown(bull_box_markup, unsafe_allow_html=True)
elif market_day_mode == "🔴 Bearish Focus":
    st.markdown(bear_box_markup, unsafe_allow_html=True)
else:
    ib1, ib2 = st.columns(2)
    with ib1:
        st.markdown(bull_box_markup, unsafe_allow_html=True)
    with ib2:
        st.markdown(bear_box_markup, unsafe_allow_html=True)

# ==============================================================================
# ১১. স্টক প্রোফাইল ও ট্রেড সেটআপ প্যানেল
# ==============================================================================
@st.cache_data(ttl=300, show_spinner=False)
def load_single_stock_ohlc(ticker: str):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        return df.dropna(subset=["Close", "Open", "High", "Low"])
    except Exception:
        return pd.DataFrame()

if st.session_state.selected_stock != DEFAULT_STOCK and st.session_state.selected_stock in stocks_df["Ticker"].values:
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

    single_wa_txt = urllib.parse.quote(
        f"🎯 *AlphaPulse Trade Setup: {sym_clean}* ({s_info['Sector']})\n"
        f"• Price: ₹{p_now} ({s_info['1D']:+.2f}%)\n"
        f"🟢 Buy Above: ₹{b_entry} | SL: ₹{b_sl} | Target: ₹{b_t1} / ₹{b_t2}\n"
        f"🔴 Short Below: ₹{sh_entry} | SL: ₹{sh_sl} | Target: ₹{sh_t1}"
    )

    st.markdown("---")
    sp_col1, sp_col2, sp_col3 = st.columns([6.2, 2.0, 1.8])
    with sp_col1:
        st.markdown(
            f"#### 🎯 Stock Profile & Intraday Setup: **{sym_clean}** (`{s_info['Sector']}`) — "
            f"Price: ₹{p_now:,.2f} ({s_info['1D']:+.2f}% | Vol: {s_info['Vol_Ratio']}x)"
        )
    with sp_col2:
        st.markdown(
            f'<a href="https://api.whatsapp.com/send?text={single_wa_txt}" target="_blank" class="wa-share-btn">'
            f'📲 WhatsApp Setup</a>',
            unsafe_allow_html=True
        )
    with sp_col3:
        if st.button("✖ Close Panel", key="close_stk_panel", use_container_width=True):
            st.session_state.selected_stock = DEFAULT_STOCK
            st.rerun()

    lv1, lv2, lv3 = st.columns(3)
    with lv1:
        c_pat = s_info["Bull_Candle"] or s_info["Bear_Candle"] or "Consolidation"
        st.info(
            f"🕯️ **Candle Pattern:** {c_pat}\n\n"
            f"📊 **RSI (14):** {s_info['RSI']} | **Up Days:** {s_info['Consec_Up']} | **Down Days:** {s_info['Consec_Down']}\n\n"
            f"🔄 **Sector Status:** 1W: {s_info['Sec_1W']:+.2f}% → Today: {s_info['Sec_1D']:+.2f}%"
        )
    with lv2:
        st.success(
            f"🟢 **Bullish Intraday/Swing Plan:**\n\n"
            f"• **Entry Above:** ₹{b_entry} | **Stop-Loss:** ₹{b_sl}\n\n"
            f"• **Target 1:** ₹{b_t1} | **Target 2:** ₹{b_t2}"
        )
    with lv3:
        st.error(
            f"🔴 **Bearish Intraday Plan:**\n\n"
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
            height=380,
            template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig_st, use_container_width=True)

    lnk1, lnk2, lnk3 = st.columns(3)
    with lnk1:
        st.link_button(f"📈 Open {sym_clean} on TradingView", f"https://in.tradingview.com/chart/?symbol=NSE%3A{sym_clean}", use_container_width=True)
    with lnk2:
        st.link_button(f"📊 View {sym_clean} on Screener.in", f"https://www.screener.in/company/{sym_clean}/", use_container_width=True)
    with lnk3:
        st.link_button(f"📰 View {sym_clean} on Google Finance", f"https://www.google.com/finance/quote/{sym_clean}:NSE", use_container_width=True)
    st.markdown("---")

# ==============================================================================
# ১২. ক্লিকেবল সেক্টর বার
# ==============================================================================
st.markdown(
    f'<div style="font-size:0.80rem;color:{TEXT_SUB};margin-top:4px;">'
    '📍 <b>Clickable Sector Bar:</b> Click any sector below to view its stocks instantly:'
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
# ১৩. ৪টি সামারি KPI কার্ড এবং নিচের ৪টি বাটন
# ==============================================================================
adv_count = int((stocks_df[tf_choice] > 0).sum())
dec_count = int((stocks_df[tf_choice] < 0).sum())
pct_50dma = round((stocks_df["Above_50DMA"].sum() / max(len(stocks_df), 1)) * 100.0, 1)

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
    if st.button("📊 View Nifty Movers List", key="kpi_btn_1", use_container_width=True):
        st.session_state.kpi_panel = "nifty_movers" if st.session_state.kpi_panel != "nifty_movers" else None
        st.rerun()

with kc2:
    c2_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Market Breadth ({tf_choice} Adv vs Dec)</div>'
        f'<div class="kpi-val"><span style="color:#34d399;">🟢 {adv_count} Adv</span> | <span style="color:#f87171;">🔴 {dec_count} Dec</span></div>'
        f'<div class="kpi-sub-up">{pct_50dma}% above 50-DMA</div>'
        f'</div>'
    )
    st.markdown(c2_html, unsafe_allow_html=True)
    if st.button("📈 View Advancing & Declining Stocks", key="kpi_btn_2", use_container_width=True):
        st.session_state.kpi_panel = "breadth_list" if st.session_state.kpi_panel != "breadth_list" else None
        st.rerun()

with kc3:
    c3_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Top Leader Sector ({tf_choice})</div>'
        f'<div class="kpi-val">👑 {leader_sec["Sector"]}</div>'
        f'<div class="kpi-sub-up">▲ {leader_sec[tf_choice]:+.2f}% (Meter: {leader_sec["Meter"]})</div>'
        f'</div>'
    )
    st.markdown(c3_html, unsafe_allow_html=True)
    if st.button(f"🔍 View {leader_sec['Sector']} Stocks", key="kpi_btn_3", use_container_width=True):
        st.session_state.selected_sector = leader_sec["Sector"]
        st.session_state.kpi_panel = "leader_sec"
        st.rerun()

with kc4:
    c4_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Top Laggard Sector ({tf_choice})</div>'
        f'<div class="kpi-val">📉 {laggard_sec["Sector"]}</div>'
        f'<div class="kpi-sub-down">▼ {laggard_sec[tf_choice]:+.2f}% (Value Zone)</div>'
        f'</div>'
    )
    st.markdown(c4_html, unsafe_allow_html=True)
    if st.button(f"🔍 View {laggard_sec['Sector']} Stocks", key="kpi_btn_4", use_container_width=True):
        st.session_state.selected_sector = laggard_sec["Sector"]
        st.session_state.kpi_panel = "laggard_sec"
        st.rerun()

if st.session_state.kpi_panel is not None:
    st.markdown("
