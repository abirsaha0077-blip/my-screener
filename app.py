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
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="AlphaPulse Pro | Smart Intraday & Swing Terminal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. 32 MICRO-SECTORS & 180+ LIQUID NSE STOCKS
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

DEFAULT_SECTOR = "All 32 Sectors"
DEFAULT_STOCK = "Search or Select Stock..."

# ==============================================================================
# 3. SESSION STATE & DEEP-LINK AUTO-SCROLL HANDLER
# ==============================================================================
if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = DEFAULT_SECTOR
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = DEFAULT_STOCK
if "kpi_panel" not in st.session_state:
    st.session_state.kpi_panel = None
if "scroll_target" not in st.session_state:
    st.session_state.scroll_target = None
if "last_alerted_stocks" not in st.session_state:
    st.session_state.last_alerted_stocks = ""

qp = st.query_params
if "nav_action" in qp:
    if qp["nav_action"] == "home":
        st.session_state.selected_sector = DEFAULT_SECTOR
        st.session_state.selected_stock = DEFAULT_STOCK
        st.session_state.kpi_panel = None
        st.session_state.scroll_target = None
    st.query_params.clear()

if "focus_stock" in qp:
    clicked_sym = urllib.parse.unquote(qp["focus_stock"]).strip()
    full_t = clicked_sym if clicked_sym.endswith(".NS") else f"{clicked_sym}.NS"
    if full_t in ALL_TICKERS:
        st.session_state.selected_stock = full_t
        st.session_state.scroll_target = "stock-inspector-anchor"
    st.query_params.clear()

if "focus_sec" in qp:
    clicked_sec = urllib.parse.unquote(qp["focus_sec"]).strip()
    if clicked_sec in SECTOR_STOCKS:
        st.session_state.selected_sector = clicked_sec
        st.session_state.kpi_panel = "custom_sector"
        st.session_state.scroll_target = "kpi-panel-anchor"
    st.query_params.clear()

# ==============================================================================
# 4. TOP HEADER BAR (CLEAN & RESPONSIVE)
# ==============================================================================
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

top_c1, top_c2, top_c3, top_c4 = st.columns([5.8, 1.9, 1.15, 1.15])
with top_c1:
    st.markdown(
        '<a href="?nav_action=home" target="_self" class="brand-logo-link" title="Click to Reset All Filters & Return to Main Terminal">'
        '<span class="logo-badge">🧭</span>'
        '<div>'
        '<div class="brand-title">AlphaPulse Pro — Market Intelligence Terminal</div>'
        '<div class="brand-subtitle">Intraday Doji Turnaround • 15m Chartink Breakout • 32-Sector Rotation</div>'
        '</div>'
        '</a>',
        unsafe_allow_html=True
    )
with top_c2:
    theme_mode = st.selectbox(
        "Theme",
        ["🌙 Pro Dark (Slate)", "🌌 Cyber Neon (Violet)", "☀️ Clean Light (Day)"],
        index=0,
        label_visibility="collapsed"
    )
with top_c3:
    show_analog_meter = st.toggle("🎛️ Meters", value=True)
with top_c4:
    auto_alert_on = st.toggle("🔔 Auto-Scan", value=False, help="Auto-scans every 3 mins with audio alert on new 15m breakout")

# ==============================================================================
# 5. DISTINCT 3-THEME ENGINE & TERMINAL CSS
# ==============================================================================
if "Clean Light" in theme_mode:
    BG_MAIN = "#f1f5f9"
    BG_CARD = "#ffffff"
    BG_SUB = "#f8fafc"
    TEXT_MAIN = "#0f172a"
    TEXT_SUB = "#475569"
    BORDER_C = "#cbd5e1"
    ACCENT_C = "#2563eb"
    BTN_BG = "linear-gradient(135deg, #e2e8f0, #cbd5e1)"
    BTN_BORDER = "#94a3b8"
    CARD_SHADOW = "0 4px 14px rgba(15, 23, 42, 0.07)"
elif "Cyber Neon" in theme_mode:
    BG_MAIN = "#080214"
    BG_CARD = "#14062b"
    BG_SUB = "#1d093d"
    TEXT_MAIN = "#f0fdf4"
    TEXT_SUB = "#e879f9"
    BORDER_C = "#00f5d488"
    ACCENT_C = "#00f5d4"
    BTN_BG = "linear-gradient(135deg, #3b0764, #701a75)"
    BTN_BORDER = "#00f5d4"
    CARD_SHADOW = "0 0 20px rgba(0, 245, 212, 0.22)"
else:
    BG_MAIN = "#060a12"
    BG_CARD = "#0f172a"
    BG_SUB = "#141f38"
    TEXT_MAIN = "#f8fafc"
    TEXT_SUB = "#94a3b8"
    BORDER_C = "#1e293b"
    ACCENT_C = "#38bdf8"
    BTN_BG = "linear-gradient(135deg, #111c33, #1e293b)"
    BTN_BORDER = "#38bdf866"
    CARD_SHADOW = "0 6px 18px rgba(0, 0, 0, 0.38)"

css_block = """
<style>
header[data-testid="stHeader"], div[data-testid="stToolbar"], div[data-testid="stDecoration"] {
    display: none !important;
}
html, body, [data-testid="stAppViewContainer"], .main {
    background-color: __BG_MAIN__ !important;
    color: __TEXT_MAIN__ !important;
    scroll-behavior: smooth !important;
}
.block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 4.8rem !important;
    max-width: 97% !important;
}
a.brand-logo-link {
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    padding: 3px 8px;
    border-radius: 12px;
    transition: all 0.2s ease;
}
a.brand-logo-link:hover {
    background: rgba(56, 189, 248, 0.12);
    transform: translateY(-1px);
}
.logo-badge {
    font-size: 1.75rem;
    background: linear-gradient(135deg, __ACCENT_C__, #2563eb);
    padding: 4px 10px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.38);
}
.brand-title {
    font-size: 1.36rem;
    font-weight: 800;
    color: __TEXT_MAIN__ !important;
    line-height: 1.15;
}
.brand-subtitle {
    font-size: 0.74rem;
    font-weight: 600;
    color: __TEXT_SUB__ !important;
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
    font-size: 0.82rem !important;
    opacity: 1 !important;
}
[data-testid="stRadio"] div[role="radiogroup"] {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    padding: 3px 10px;
    border-radius: 999px;
    gap: 10px !important;
}
div.stButton > button,
button[data-testid="stBaseButton-secondary"],
div.stDownloadButton > button {
    background: __BTN_BG__ !important;
    color: __TEXT_MAIN__ !important;
    border: 1.5px solid __BTN_BORDER__ !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 0.82rem !important;
    padding: 0.42rem 0.85rem !important;
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
    margin-right: 4px !important;
    padding: 7px 14px !important;
}
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span {
    color: __TEXT_SUB__ !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
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
    font-size: 0.86rem !important;
}
.pulse-bar {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    border-radius: 12px;
    padding: 8px 14px;
    margin: 6px 0 10px 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    box-shadow: __CARD_SHADOW__;
}
.pulse-item {
    font-size: 0.82rem;
    font-weight: 700;
    color: __TEXT_MAIN__;
}
.compass-pill {
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 800;
}
/* UNIFIED INTRADAY TERMINAL RADAR PANELS */
.radar-panel-bull {
    background: __BG_CARD__;
    border: 1px solid #10b98166;
    border-top: 3.5px solid #10b981;
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    box-shadow: __CARD_SHADOW__;
}
.radar-panel-bear {
    background: __BG_CARD__;
    border: 1px solid #ef444466;
    border-top: 3.5px solid #ef4444;
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    box-shadow: __CARD_SHADOW__;
}
.radar-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid __BORDER_C__;
}
.radar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
    gap: 7px;
}
a.radar-row-card {
    text-decoration: none !important;
    background: __BG_SUB__;
    border: 1px solid __BORDER_C__;
    border-radius: 9px;
    padding: 7px 10px;
    color: __TEXT_MAIN__ !important;
    display: flex;
    flex-direction: column;
    gap: 3px;
    transition: all 0.18s ease;
}
a.radar-row-card:hover {
    border-color: __ACCENT_C__;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.r-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.r-sym {
    font-size: 0.86rem;
    font-weight: 800;
    color: __TEXT_MAIN__;
}
.r-tag-bull {
    background: rgba(16, 185, 129, 0.16);
    color: #34d399;
    border: 1px solid #10b98155;
    padding: 1px 6px;
    border-radius: 5px;
    font-size: 0.67rem;
    font-weight: 700;
}
.r-tag-bear {
    background: rgba(239, 68, 68, 0.16);
    color: #f87171;
    border: 1px solid #ef444455;
    padding: 1px 6px;
    border-radius: 5px;
    font-size: 0.67rem;
    font-weight: 700;
}
.r-mid {
    display: flex;
    justify-content: space-between;
    font-size: 0.73rem;
    color: __TEXT_SUB__;
}
.r-plan {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    font-weight: 700;
    background: rgba(0,0,0,0.18);
    padding: 3px 7px;
    border-radius: 6px;
    margin-top: 2px;
}
a.wa-share-btn {
    text-decoration: none !important;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: #ffffff !important;
    padding: 5px 13px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    box-shadow: 0 3px 10px rgba(34, 197, 94, 0.35);
}
.marquee-wrap {
    background: __BG_CARD__;
    border: 1px solid __BORDER_C__;
    border-radius: 10px;
    padding: 7px 10px;
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
a.sec-pill-up, a.sec-pill-down {
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 11px;
    margin-right: 8px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
}
a.sec-pill-up {
    background: rgba(16,185,129,0.14);
    border: 1px solid #10b981;
    color: #34d399 !important;
}
a.sec-pill-down {
    background: rgba(239,68,68,0.14);
    border: 1px solid #ef4444;
    color: #f87171 !important;
}
.kpi-card {
    background: __BG_CARD__;
    border: 1.5px solid __BORDER_C__;
    border-radius: 12px;
    padding: 10px 14px;
    min-height: 104px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 6px;
    box-shadow: __CARD_SHADOW__;
}
.kpi-title {
    color: __TEXT_SUB__;
    font-size: 0.77rem;
    font-weight: 700;
}
.kpi-val {
    font-size: 1.16rem;
    font-weight: 800;
    color: __TEXT_MAIN__;
    margin: 3px 0;
}
.kpi-sub-up {
    background: rgba(16,185,129,0.15);
    color: #34d399;
    border: 1px solid #10b98155;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.70rem;
    font-weight: 700;
    width: fit-content;
}
.kpi-sub-down {
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid #ef444455;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.70rem;
    font-weight: 700;
    width: fit-content;
}
.pill-container {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 6px;
}
a.bull-pill, a.bear-pill {
    text-decoration: none !important;
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
a.bull-pill {
    background: rgba(16,185,129,0.14);
    border: 1px solid #10b98199;
    color: #34d399 !important;
}
a.bear-pill {
    background: rgba(239,68,68,0.14);
    border: 1px solid #ef444499;
    color: #f87171 !important;
}
a.single-top-btn {
    position: fixed;
    bottom: 58px;
    right: 18px;
    z-index: 999999;
    text-decoration: none !important;
    background: linear-gradient(135deg, #0ea5e9, #2563eb);
    color: #ffffff !important;
    padding: 8px 15px;
    border-radius: 999px;
    font-size: 0.80rem;
    font-weight: 800;
    border: 1.5px solid rgba(255, 255, 255, 0.35);
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.55);
}
</style>
""".replace("__BG_MAIN__", BG_MAIN).replace("__BG_CARD__", BG_CARD).replace("__BG_SUB__", BG_SUB).replace("__TEXT_MAIN__", TEXT_MAIN).replace("__TEXT_SUB__", TEXT_SUB).replace("__BORDER_C__", BORDER_C).replace("__ACCENT_C__", ACCENT_C).replace("__BTN_BG__", BTN_BG).replace("__BTN_BORDER__", BTN_BORDER).replace("__CARD_SHADOW__", CARD_SHADOW)

st.markdown(css_block, unsafe_allow_html=True)

# ==============================================================================
# 6. NAN-SAFE DATA ENGINE, CANDLESTICK & 15M CHARTINK SCANNER
# ==============================================================================
def safe_num(val, default: float = 0.0) -> float:
    try:
        v = float(val)
        return default if (np.isnan(v) or np.isinf(v)) else v
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
    return safe_num((100.0 - (100.0 / (1.0 + rs))).iloc[-1], 50.0)


def calc_return(closes: pd.Series, days: int) -> float:
    s = closes.dropna()
    if len(s) < 2:
        return 0.0
    base = safe_num(s.iloc[max(0, len(s) - 1 - days)], 0.0)
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
                    if c_now > 0:
                        res[k] = {
                            "price": c_now,
                            "1D": calc_return(df["Close"], 1),
                            "1W": calc_return(df["Close"], 5),
                            "1M": calc_return(df["Close"], 21),
                            "3M": calc_return(df["Close"], 63),
                            "6M": calc_return(df["Close"], 126),
                            "1Y": calc_return(df["Close"], 250),
                        }
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

            closes, opens, highs, lows = df["Close"], df["Open"], df["High"], df["Low"]
            vols = df["Volume"].fillna(0)
            c_now = safe_num(closes.iloc[-1], 0.0)
            if c_now <= 0:
                continue
            o_now, h_now, l_now = safe_num(opens.iloc[-1], c_now), safe_num(highs.iloc[-1], c_now), safe_num(lows.iloc[-1], c_now)
            prev_high, prev_low, prev_close = safe_num(highs.iloc[-2], h_now), safe_num(lows.iloc[-2], l_now), safe_num(closes.iloc[-2], c_now)
            prev_dma20 = safe_num(closes.iloc[:-1].rolling(20).mean().iloc[-1], c_now)

            r_1d, r_1w, r_1m = calc_return(closes, 1), calc_return(closes, 5), calc_return(closes, 21)
            r_3m, r_6m, r_1y = calc_return(closes, 63), calc_return(closes, 126), calc_return(closes, 250)
            dma20 = safe_num(closes.rolling(20).mean().iloc[-1], c_now)
            dma50 = safe_num(closes.rolling(50).mean().iloc[-1], dma20) if len(closes) >= 50 else dma20

            avg_vol = safe_num(vols.iloc[-21:-1].mean(), 0.0)
            vol_ratio = max(round(safe_num(safe_num(vols.iloc[-1], 0.0) / avg_vol, 1.0), 2), 0.1) if avg_vol > 0 else 1.0
            rsi_val = round(calc_rsi(closes, 14), 1)

            c_arr = closes.values
            consec_up, consec_down = 0, 0
            for i in range(len(c_arr) - 1, 0, -1):
                if c_arr[i] > c_arr[i - 1] and consec_down == 0:
                    consec_up += 1
                elif c_arr[i] < c_arr[i - 1] and consec_up == 0:
                    consec_down += 1
                else:
                    break

            rng = max(h_now - l_now, 1e-6)
            body_pct = safe_num(abs(c_now - o_now) / rng, 0.5)
            lower_wick = safe_num((min(o_now, c_now) - l_now) / rng, 0.0)
            upper_wick = safe_num((h_now - max(o_now, c_now)) / rng, 0.0)
            rng_3d_pct = safe_num(((float(highs.iloc[-3:].max()) - float(lows.iloc[-3:].min())) / c_now) * 100.0, 10.0)

            bull_candle = "Dragonfly Doji" if (body_pct <= 0.28 and lower_wick >= 0.42) else ("Hammer" if (lower_wick >= 0.48 and body_pct <= 0.42) else ("Bullish Doji" if (body_pct <= 0.28 and c_now >= o_now) else ("Tight Base" if (rng_3d_pct <= 4.2 and c_now >= o_now) else ("Bottom Turn" if (lower_wick >= 0.35 and r_1d >= 0) else None))))
            bear_candle = "Gravestone Doji" if (body_pct <= 0.28 and upper_wick >= 0.42) else ("Shooting Star" if (upper_wick >= 0.48 and body_pct <= 0.42) else ("Bearish Doji" if (body_pct <= 0.28 and c_now < o_now) else ("Supply Stall" if (rng_3d_pct <= 4.2 and c_now < o_now) else ("Top Reject" if (upper_wick >= 0.35 and r_1d < 0) else None))))

            tr = pd.concat([highs - lows, (highs - closes.shift(1)).abs(), (lows - closes.shift(1)).abs()], axis=1).max(axis=1)
            atr_clean = round(max(safe_num(tr.rolling(14).mean().iloc[-1], c_now * 0.018), c_now * 0.008), 2)
            dist_20 = round(safe_num(((c_now - dma20) / dma20) * 100.0, 0.0), 2) if dma20 > 0 else 0.0

            if rsi_val >= 75 or consec_up >= 4:
                action_sig = "⚠️ Overbought (Wait)"
            elif bull_candle and consec_up <= 2 and vol_ratio >= 1.15:
                action_sig = "🟢 Strong Intraday Buy"
            elif c_now >= dma50 and -2.5 <= dist_20 <= 3.5 and 45 <= rsi_val <= 65:
                action_sig = "💎 Safe Swing Buy"
            elif bear_candle and consec_down <= 2 and vol_ratio >= 1.15:
                action_sig = "🔴 Intraday Short"
            else:
                action_sig = "⚖️ Hold / Watch"

            conf_score = int(np.clip(55 + min(vol_ratio * 12, 25) + (10 if c_now >= dma50 else -5) + (8 if (bull_candle or bear_candle) else 0), 45, 96))

            stock_rows.append({
                "Ticker": ticker, "Symbol": ticker.replace(".NS", ""), "Sector": TICKER_TO_SECTOR.get(ticker, "Others"),
                "Price": round(c_now, 2), "1D": round(r_1d, 2), "1W": round(r_1w, 2), "1M": round(r_1m, 2),
                "3M": round(r_3m, 2), "6M": round(r_6m, 2), "1Y": round(r_1y, 2),
                "Vol_Ratio": vol_ratio, "RSI": rsi_val, "DMA20": round(dma20, 2), "DMA50": round(dma50, 2),
                "Above_50DMA": bool(c_now >= dma50), "Dist_20DMA": dist_20,
                "Consec_Up": int(consec_up), "Consec_Down": int(consec_down),
                "Bull_Candle": bull_candle, "Bear_Candle": bear_candle, "Action_Signal": action_sig, "Confidence": conf_score,
                "Body_Pct": round(body_pct, 2), "Lower_Wick": round(lower_wick, 2), "Upper_Wick": round(upper_wick, 2),
                "ATR": atr_clean, "Day_High": round(h_now, 2), "Day_Low": round(l_now, 2),
                "Prev_High": round(prev_high, 2), "Prev_Low": round(prev_low, 2), "Prev_Close": round(prev_close, 2), "Prev_DMA20": round(prev_dma20, 2),
                "Buy_Entry": round(max(c_now, h_now * 0.998), 2), "Buy_SL": round(min(l_now, c_now - 1.2 * atr_clean), 2), "Buy_Target": round(c_now + 1.8 * atr_clean, 2),
                "Short_Entry": round(min(c_now, l_now * 1.002), 2), "Short_SL": round(max(h_now, c_now + 1.2 * atr_clean), 2), "Short_Target": round(c_now - 1.8 * atr_clean, 2),
            })
        except Exception:
            continue

    stocks_df = pd.DataFrame(stock_rows)
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    sec_rows = []
    for sec_name, grp in stocks_df.groupby("Sector"):
        s_1d, s_1w, s_1m = safe_num(grp["1D"].mean()), safe_num(grp["1W"].mean()), safe_num(grp["1M"].mean())
        s_3m, s_6m, s_1y = safe_num(grp["3M"].mean()), safe_num(grp["6M"].mean()), safe_num(grp["1Y"].mean())
        s_vol, s_rsi = safe_num(grp["Vol_Ratio"].mean(), 1.0), safe_num(grp["RSI"].mean(), 50.0)
        s_b50 = safe_num((grp["Above_50DMA"].sum() / max(len(grp), 1)) * 100.0, 50.0)

        sec_bull_turn = bool((s_1w <= 1.5 or s_1m <= 1.5) and (s_1d >= -0.15 or s_1d > (s_1w / 5.0)))
        sec_bear_roll = bool((s_1w >= -0.5 or s_1m >= 0.5) and (s_1d <= 0.25 or s_1d < (s_1w / 5.0)))
        meter = int(np.clip(safe_num(50.0 + (s_1w * 3.5) + (s_1d * 6.0) + ((s_rsi - 50.0) * 0.6), 50.0), 5, 98))
        zone = "🔄 Turnaround" if (sec_bull_turn and s_1d >= 0) else ("🚀 Leading" if (s_1w >= 2.0 and s_1d >= 0) else ("⚠️ Exhaustion" if (sec_bear_roll and s_1d < 0) else "💎 Value Zone"))

        sec_rows.append({
            "Sector": sec_name, "Count": len(grp), "1D": round(s_1d, 2), "1W": round(s_1w, 2), "1M": round(s_1m, 2),
            "3M": round(s_3m, 2), "6M": round(s_6m, 2), "1Y": round(s_1y, 2), "Avg_Vol": round(s_vol, 2),
            "RSI": round(s_rsi, 1), "Breadth_50DMA": round(s_b50, 1), "Meter": meter, "Zone": zone,
            "Sec_Bull_Turn": sec_bull_turn, "Sec_Bear_Roll": sec_bear_roll,
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
    active_pool = stocks_df[stocks_df["Price"] > 150].sort_values("Vol_Ratio", ascending=False).head(42)
    pool_tickers = active_pool["Ticker"].tolist()
    daily_map = active_pool.set_index("Ticker").to_dict("index")
    bull_15m, bear_15m = [], []

    try:
        raw_15m = yf.download(pool_tickers, period="5d", interval="15m", progress=False, group_by="ticker", threads=True)
        for tk in pool_tickers:
            try:
                df15 = (raw_15m[tk] if len(pool_tickers) > 1 else raw_15m).dropna(subset=["Close", "Open", "High", "Low"])
                if len(df15) < 22:
                    continue
                d_info = daily_map[tk]
                c15, o15, h15, l15 = safe_num(df15["Close"].iloc[-1], d_info["Price"]), safe_num(df15["Open"].iloc[-1]), safe_num(df15["High"].iloc[-1]), safe_num(df15["Low"].iloc[-1])
                v15 = safe_num(df15["Volume"].fillna(0).iloc[-1])
                vol_sma20 = safe_num(df15["Volume"].fillna(0).iloc[-21:-1].mean())
                v15_ratio = round(safe_num(v15 / vol_sma20, d_info["Vol_Ratio"]), 2) if vol_sma20 > 0 else d_info["Vol_Ratio"]
                rsi15 = round(calc_rsi(df15["Close"], 14), 1)

                day_slice = df15[df15.index.date == df15.index[-1].date()]
                vwap15 = safe_num(((day_slice["High"] + day_slice["Low"] + day_slice["Close"]) / 3.0 * day_slice["Volume"]).sum() / day_slice["Volume"].sum(), c15) if (len(day_slice) >= 1 and safe_num(day_slice["Volume"].sum()) > 0) else c15

                if (o15 <= l15 * 1.005 or c15 > o15) and c15 >= d_info["Prev_High"] * 0.996 and v15_ratio >= 1.35 and (56 <= rsi15 <= 78) and c15 > vwap15 and d_info["Prev_Close"] > d_info["Prev_DMA20"]:
                    bull_15m.append({
                        "Symbol": tk.replace(".NS", ""), "Ticker": tk, "Sector": d_info["Sector"], "Price": round(c15, 2),
                        "VWAP": round(vwap15, 2), "Vol_Ratio": v15_ratio, "RSI": rsi15, "1D": d_info["1D"], "Confidence": d_info["Confidence"],
                        "Reason": "⚡ 15m VWAP + High Breakout", "Entry": round(max(c15, h15 * 1.0005), 2),
                        "SL": round(min(l15, vwap15 * 0.995), 2), "Target": round(c15 + 1.6 * d_info["ATR"], 2),
                    })
                if (o15 >= h15 * 0.995 or c15 < o15) and c15 <= d_info["Prev_Low"] * 1.004 and v15_ratio >= 1.30 and (22 <= rsi15 <= 44) and c15 < vwap15:
                    bear_15m.append({
                        "Symbol": tk.replace(".NS", ""), "Ticker": tk, "Sector": d_info["Sector"], "Price": round(c15, 2),
                        "VWAP": round(vwap15, 2), "Vol_Ratio": v15_ratio, "RSI": rsi15, "1D": d_info["1D"], "Confidence": d_info["Confidence"],
                        "Reason": "📉 15m VWAP Breakdown", "Entry": round(min(c15, l15 * 0.9995), 2),
                        "SL": round(max(h15, vwap15 * 1.005), 2), "Target": round(c15 - 1.6 * d_info["ATR"], 2),
                    })
            except Exception:
                continue
    except Exception:
        pass

    if not bull_15m:
        for _, r in active_pool[(active_pool["Price"] > active_pool["DMA20"]) & (active_pool["1D"] > 0)].head(6).iterrows():
            bull_15m.append({"Symbol": r["Symbol"], "Ticker": r["Ticker"], "Sector": r["Sector"], "Price": r["Price"], "VWAP": round(r["Price"] * 0.994, 2), "Vol_Ratio": r["Vol_Ratio"], "RSI": r["RSI"], "1D": r["1D"], "Confidence": r["Confidence"], "Reason": "⚡ Near 15m High Breakout", "Entry": r["Buy_Entry"], "SL": r["Buy_SL"], "Target": r["Buy_Target"]})
    if not bear_15m:
        for _, r in active_pool[active_pool["1D"] < 0].head(6).iterrows():
            bear_15m.append({"Symbol": r["Symbol"], "Ticker": r["Ticker"], "Sector": r["Sector"], "Price": r["Price"], "VWAP": round(r["Price"] * 1.006, 2), "Vol_Ratio": r["Vol_Ratio"], "RSI": r["RSI"], "1D": r["1D"], "Confidence": r["Confidence"], "Reason": "📉 Below VWAP Supply", "Entry": r["Short_Entry"], "SL": r["Short_SL"], "Target": r["Short_Target"]})

    return pd.DataFrame(bull_15m), pd.DataFrame(bear_15m)


def filter_doji_turnaround_stocks(stocks_df: pd.DataFrame):
    df = stocks_df.copy()
    b_cand = df[(df["Consec_Up"] <= 2) & (df["1D"] >= -0.2) & (df["1D"] <= 3.8) & (df["Vol_Ratio"] >= 1.08)].copy()
    b_cand["Bull_Candle"] = b_cand["Bull_Candle"].fillna("Doji Base")
    b_cand["Score"] = (b_cand["Vol_Ratio"] * 28.0) + np.where(b_cand["Sec_Bull_Turn"], 30.0, 0.0) + ((1.0 - b_cand["Body_Pct"]) * 22.0)
    bull6 = b_cand.sort_values("Score", ascending=False).head(6).copy()
    bull6["Reason"] = "🔄 " + bull6["Bull_Candle"].astype(str) + " + Vol Buildup"
    bull6["Entry"], bull6["SL"], bull6["Target"] = bull6["Buy_Entry"], bull6["Buy_SL"], bull6["Buy_Target"]

    used = set(bull6["Ticker"].tolist())
    br_cand = df[(~df["Ticker"].isin(used)) & (df["Consec_Down"] <= 2) & (df["1D"] <= 0.2) & (df["1D"] >= -3.8) & (df["Vol_Ratio"] >= 1.05)].copy()
    br_cand["Bear_Candle"] = br_cand["Bear_Candle"].fillna("Top Stall")
    br_cand["Score"] = (br_cand["Vol_Ratio"] * 28.0) + np.where(br_cand["Sec_Bear_Roll"], 30.0, 0.0) + ((1.0 - br_cand["Body_Pct"]) * 22.0)
    bear6 = br_cand.sort_values("Score", ascending=False).head(6).copy()
    bear6["Reason"] = "📉 " + bear6["Bear_Candle"].astype(str) + " Rejection"
    bear6["Entry"], bear6["SL"], bear6["Target"] = bear6["Short_Entry"], bear6["Short_SL"], bear6["Short_Target"]
    return bull6, bear6


def style_colored_table(df: pd.DataFrame, pct_cols: list):
    def color_pct(val):
        if pd.isna(val) or not isinstance(val, (int, float, np.number)):
            return ""
        return "color:#34d399;font-weight:700;" if val > 0 else ("color:#f87171;font-weight:700;" if val < 0 else "color:#94a3b8;")
    return df.style.map(color_pct, subset=[c for c in pct_cols if c in df.columns]).format(precision=2)


with st.spinner("⚡ Loading Live Market Intelligence & Intraday Trade Setups..."):
    pulse = load_pulse_indices()
    stocks_df, sectors_df = load_full_market_data()
    bull_15m_df, bear_15m_df = run_chartink_15m_scanner(stocks_df)

if stocks_df.empty or sectors_df.empty:
    st.error("⚠️ Market data temporarily unavailable. Please reload.")
    st.stop()

# ==============================================================================
# 7. MARKET PULSE RIBBON & AI COMPASS
# ==============================================================================
n_d, b_d, v_d, u_d = pulse["NIFTY"], pulse["BANKNIFTY"], pulse["VIX"], pulse["USDINR"]
adv_today, dec_today = int((stocks_df["1D"] > 0).sum()), int((stocks_df["1D"] < 0).sum())

if n_d["1D"] >= 0.20 and adv_today >= dec_today:
    c_txt, c_sty = "🟢 Bullish Market — Track BUY Setups", "background:rgba(16,185,129,0.18);color:#34d399;border:1px solid #10b98166;"
elif n_d["1D"] <= -0.20 and dec_today > adv_today:
    c_txt, c_sty = "🔴 Bearish Market — Track SHORT Setups", "background:rgba(239,68,68,0.18);color:#f87171;border:1px solid #ef444466;"
else:
    c_txt, c_sty = "⚖️ Sideways Market — Trade Sector Leaders", "background:rgba(251,191,36,0.18);color:#fbbf24;border:1px solid #fbbf2466;"

st.markdown(
    f'<div class="pulse-bar">'
    f'<div class="pulse-item">🇮🇳 Nifty 50: <span style="color:{"#34d399" if n_d["1D"]>=0 else "#f87171"};">{n_d["price"]:,.1f} ({n_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">🏛️ Bank Nifty: <span style="color:{"#34d399" if b_d["1D"]>=0 else "#f87171"};">{b_d["price"]:,.1f} ({b_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">⚡ India VIX: <span style="color:#34d399;">{v_d["price"]:.2f}</span></div>'
    f'<div class="pulse-item">💵 USD/INR: <span style="color:{ACCENT_C};">₹{u_d["price"]:.2f}</span></div>'
    f'<div class="compass-pill" style="{c_sty}">🧭 {c_txt}</div></div>',
    unsafe_allow_html=True
)

# ==============================================================================
# 8. 4-COLUMN FILTER BAR
# ==============================================================================
fc1, fc2, fc3, fc4 = st.columns([1.3, 2.5, 3.1, 3.1])
with fc1:
    tf_choice = st.selectbox("📅 1. Timeframe:", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=1)
with fc2:
    sort_choice = st.selectbox("🔄 2. Sort Sectors By:", ["🚀 Top Gainers First", "📉 Top Losers First", "🔄 Bottom Turnaround First", "🔥 High Volume Spike First", "🎛️ Rotation Meter Score"], index=0)
with fc3:
    sec_list = [DEFAULT_SECTOR] + sorted(list(SECTOR_STOCKS.keys()))
    picked_sec = st.selectbox("🔍 3. Filter by Sector:", sec_list, index=sec_list.index(st.session_state.selected_sector) if st.session_state.selected_sector in sec_list else 0)
    if picked_sec != st.session_state.selected_sector:
        st.session_state.selected_sector = picked_sec
        st.rerun()
with fc4:
    stock_search_list = [DEFAULT_STOCK] + [f"{r['Symbol']} ({r['Sector']})" for _, r in stocks_df.sort_values("Symbol").iterrows()]
    st_idx = next((i for i, s in enumerate(stock_search_list) if st.session_state.selected_stock != DEFAULT_STOCK and s.startswith(f"{st.session_state.selected_stock.replace('.NS','')} (")), 0)
    picked_stock = st.selectbox("⚡ 4. Quick Stock Search:", stock_search_list, index=st_idx)
    new_stk = picked_stock.split(" (")[0].strip() + ".NS" if picked_stock != DEFAULT_STOCK else DEFAULT_STOCK
    if new_stk != st.session_state.selected_stock:
        st.session_state.selected_stock = new_stk
        st.session_state.scroll_target = "stock-inspector-anchor"
        st.rerun()

# ==============================================================================
# 9. UNIFIED INTRADAY TERMINAL RADAR PANELS
# ==============================================================================
bull_doji6, bear_doji6 = filter_doji_turnaround_stocks(stocks_df)

wa_lines = ["🧭 *AlphaPulse Pro — Intraday Trade Signals*", "🟢 *Top Bullish Setups:*"]
for _, r in bull_doji6.head(3).iterrows():
    wa_lines.append(f"• *{r['Symbol']}* (₹{r['Price']}) | Buy: ₹{r['Entry']} | SL: ₹{r['SL']} | Tgt: ₹{r['Target']}")
wa_lines.append("\n🔴 *Top Bearish Setups:*")
for _, r in bear_doji6.head(3).iterrows():
    wa_lines.append(f"• *{r['Symbol']}* (₹{r['Price']}) | Short: ₹{r['Entry']} | SL: ₹{r['SL']} | Tgt: ₹{r['Target']}")
wa_direct_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(chr(10).join(wa_lines))}"

rc_col1, rc_col2, rc_col3 = st.columns([4.2, 3.8, 2.0])
with rc_col1:
    radar_strategy = st.radio("Strategy:", ["🔄 Doji Bottom Turnaround", "⚡ 15m Chartink Breakout"], horizontal=True, label_visibility="collapsed")
with rc_col2:
    market_day_mode = st.radio("Bias:", ["🟢 Bullish Picks", "🔴 Bearish Picks", "🌗 Both"], horizontal=True, label_visibility="collapsed")
with rc_col3:
    st.markdown(f'<div style="text-align:right;padding-top:2px;"><a href="{wa_direct_url}" target="_blank" class="wa-share-btn">📲 WhatsApp Signals</a></div>', unsafe_allow_html=True)

def render_radar_panel_html(df_bull: pd.DataFrame, df_bear: pd.DataFrame, mode_str: str) -> str:
    def make_row_card(r, is_bull: bool):
        qt = urllib.parse.quote(r["Ticker"])
        tag_cls = "r-tag-bull" if is_bull else "r-tag-bear"
        tag_txt = f"🟢 BUY • {r['Confidence']}%" if is_bull else f"🔴 SHORT • {r['Confidence']}%"
        c_col = "#34d399" if r["1D"] >= 0 else "#f87171"
        lbl = "Entry" if is_bull else "Short"
        return (
            f'<a href="?focus_stock={qt}" target="_self" class="radar-row-card">'
            f'<div class="r-top"><span class="r-sym">{r["Symbol"]}</span><span class="{tag_cls}">{tag_txt}</span></div>'
            f'<div class="r-mid"><span>₹{r["Price"]:,.1f} <span style="color:{c_col};font-weight:700;">({r["1D"]:+.1f}%)</span></span><span>📊 {r["Vol_Ratio"]:.1f}x Vol</span></div>'
            f'<div style="font-size:0.69srem;color:{TEXT_SUB};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{r["Reason"]}</div>'
            f'<div class="r-plan"><span>🎯 {lbl}: ₹{r["Entry"]}</span><span>🛑 SL: ₹{r["SL"]}</span><span>🚀 Tgt: ₹{r["Target"]}</span></div>'
            f'</a>'
        )
    bull_cards = [make_row_card(r, True) for _, r in df_bull.head(6).iterrows()]
    bear_cards = [make_row_card(r, False) for _, r in df_bear.head(6).iterrows()]

    out_html = ""
    if mode_str in ("🟢 Bullish Picks", "🌗 Both") and bull_cards:
        out_html += f'<div class="radar-panel-bull"><div class="radar-panel-header"><span style="color:#34d399;font-weight:800;font-size:0.86rem;">🔄 Bullish Intraday Command Deck (Bottom Turnaround & Breakout)</span><span style="font-size:0.72rem;color:{TEXT_SUB};">Tap any card for live chart</span></div><div class="radar-grid">{"".join(bull_cards)}</div></div>'
    if mode_str in ("🔴 Bearish Picks", "🌗 Both") and bear_cards:
        out_html += f'<div class="radar-panel-bear"><div class="radar-panel-header"><span style="color:#f87171;font-weight:800;font-size:0.86rem;">📉 Bearish Intraday Command Deck (Top Rejection & Breakdown)</span><span style="font-size:0.72rem;color:{TEXT_SUB};">Tap any card for live chart</span></div><div class="radar-grid">{"".join(bear_cards)}</div></div>'
    return out_html

active_b_df = bull_15m_df if "15m" in radar_strategy else bull_doji6
active_br_df = bear_15m_df if "15m" in radar_strategy else bear_doji6
st.markdown(render_radar_panel_html(active_b_df, active_br_df, market_day_mode), unsafe_allow_html=True)

# ==============================================================================
# 10. CLICKABLE SECTOR MARQUEE BAR
# ==============================================================================
bar_items = [
    f'<a class="{"sec-pill-up" if sr[tf_choice]>=0 else "sec-pill-down"}" href="?focus_sec={urllib.parse.quote(sr["Sector"])}" target="_self">'
    f'{"🟢" if sr[tf_choice]>=0 else "🔴"} {sr["Sector"]}: {"▲" if sr[tf_choice]>=0 else "▼"} {sr[tf_choice]:+.2f}% 🔍</a>'
    for _, sr in sectors_df.sort_values(tf_choice, ascending=False).iterrows()
]
st.markdown(f'<div class="marquee-wrap"><div class="marquee-track">{"".join(bar_items) * 2}</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 11. STOCK INSPECTOR & BEGINNER TRADE PLAN PANEL (AUTO-SCROLL)
# ==============================================================================
st.markdown('<div id="stock-inspector-anchor"></div>', unsafe_allow_html=True)

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
    sym_clean, p_now, atr_v = s_info["Symbol"], s_info["Price"], s_info["ATR"]
    safe_qty = max(int(500.0 / max(abs(s_info["Buy_Entry"] - s_info["Buy_SL"]), 1.0)), 1)

    single_wa_txt = urllib.parse.quote(
        f"🎯 *AlphaPulse Trade Setup: {sym_clean}* ({s_info['Sector']})\n"
        f"• Price: ₹{p_now} ({s_info['1D']:+.2f}%) | Signal: {s_info['Action_Signal']}\n"
        f"🟢 Buy Above: ₹{s_info['Buy_Entry']} | SL: ₹{s_info['Buy_SL']} | Target: ₹{s_info['Buy_Target']}\n"
        f"🔴 Short Below: ₹{s_info['Short_Entry']} | SL: ₹{s_info['Short_SL']} | Target: ₹{s_info['Short_Target']}"
    )

    st.markdown("---")
    sp1, sp2, sp3 = st.columns([6.2, 2.0, 1.8])
    with sp1:
        st.markdown(f"#### 🎯 Stock Trade Inspector: **{sym_clean}** (`{s_info['Sector']}`) — ₹{p_now:,.2f} ({s_info['1D']:+.2f}% | {s_info['Action_Signal']})")
    with sp2:
        st.markdown(f'<a href="https://api.whatsapp.com/send?text={single_wa_txt}" target="_blank" class="wa-share-btn">📲 WhatsApp Setup</a>', unsafe_allow_html=True)
    with sp3:
        if st.button("✖ Close Chart", key="close_stk", use_container_width=True):
            st.session_state.selected_stock = DEFAULT_STOCK
            st.session_state.scroll_target = None
            st.rerun()

    lv1, lv2, lv3 = st.columns(3)
    with lv1:
        st.info(f"🧭 **Verdict:** {s_info['Action_Signal']} ({s_info['Confidence']}% Conf.)\n\n📊 **RSI:** {s_info['RSI']} | **Vol:** {s_info['Vol_Ratio']}x | **Safe Qty (₹500 Risk):** `{safe_qty} Shares`")
    with lv2:
        st.success(f"🟢 **Bullish Buy Plan:**\n\n• **Buy Above:** ₹{s_info['Buy_Entry']} | **SL:** ₹{s_info['Buy_SL']} | **Target:** ₹{s_info['Buy_Target']}")
    with lv3:
        st.error(f"🔴 **Bearish Short Plan:**\n\n• **Short Below:** ₹{s_info['Short_Entry']} | **SL:** ₹{s_info['Short_SL']} | **Target:** ₹{s_info['Short_Target']}")

    ohlc_df = load_single_stock_ohlc(s_info["Ticker"])
    if not ohlc_df.empty and len(ohlc_df) >= 20:
        ohlc_df["DMA20"], ohlc_df["DMA50"] = ohlc_df["Close"].rolling(20).mean(), ohlc_df["Close"].rolling(50).mean()
        sub_df = ohlc_df.tail(70)
        fig_st = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.74, 0.26])
        fig_st.add_trace(go.Candlestick(x=sub_df.index, open=sub_df["Open"], high=sub_df["High"], low=sub_df["Low"], close=sub_df["Close"], name="Price"), row=1, col=1)
        fig_st.add_trace(go.Scatter(x=sub_df.index, y=sub_df["DMA20"], mode="lines", name="20 DMA", line=dict(color="#38bdf8", width=1.5)), row=1, col=1)
        fig_st.add_trace(go.Scatter(x=sub_df.index, y=sub_df["DMA50"], mode="lines", name="50 DMA", line=dict(color="#f59e0b", width=1.5)), row=1, col=1)
        # Entry, SL, Target horizontal lines on chart for beginner visual clarity
        fig_st.add_hline(y=s_info["Buy_Entry"], line_dash="dot", line_color="#10b981", annotation_text="Entry", row=1, col=1)
        fig_st.add_hline(y=s_info["Buy_SL"], line_dash="dash", line_color="#ef4444", annotation_text="SL", row=1, col=1)
        fig_st.add_hline(y=s_info["Buy_Target"], line_dash="dash", line_color="#34d399", annotation_text="Target", row=1, col=1)
        fig_st.add_trace(go.Bar(x=sub_df.index, y=sub_df["Volume"], name="Volume", marker_color=["#10b981" if c >= o else "#ef4444" for c, o in zip(sub_df["Close"], sub_df["Open"])]), row=2, col=1)
        fig_st.update_layout(height=370, template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=20, b=10), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig_st, use_container_width=True)

    l1, l2, l3 = st.columns(3)
    with l1:
        st.link_button(f"📈 TradingView ({sym_clean})", f"https://in.tradingview.com/chart/?symbol=NSE%3A{sym_clean}", use_container_width=True)
    with l2:
        st.link_button(f"📊 Screener.in ({sym_clean})", f"https://www.screener.in/company/{sym_clean}/", use_container_width=True)
    with l3:
        st.link_button(f"📰 Google Finance ({sym_clean})", f"https://www.google.com/finance/quote/{sym_clean}:NSE", use_container_width=True)
    st.markdown("---")

# ==============================================================================
# 12. 4 SUMMARY KPI CARDS & DRILL-DOWN PANEL
# ==============================================================================
adv_count, dec_count = int((stocks_df["1D"] > 0).sum()), int((stocks_df["1D"] < 0).sum())
pct_50dma = round((stocks_df["Above_50DMA"].sum() / max(len(stocks_df), 1)) * 100.0, 1)
leader_sec, laggard_sec = sectors_df.sort_values(tf_choice, ascending=False).iloc[0], sectors_df.sort_values(tf_choice, ascending=True).iloc[0]
nifty_tf = n_d.get(tf_choice, n_d["1W"])

kc1, kc2, kc3, kc4 = st.columns(4)
with kc1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Nifty 50 Benchmark ({tf_choice})</div><div class="kpi-val" style="color:{"#34d399" if nifty_tf>=0 else "#f87171"};">{nifty_tf:+.2f}%</div><div class="kpi-sub-up">1W: {n_d["1W"]:+.2f}% | 1Y: {n_d["1Y"]:+.1f}%</div></div>', unsafe_allow_html=True)
    if st.button("📊 Top Gainers & Losers", key="k1", use_container_width=True):
        st.session_state.kpi_panel, st.session_state.scroll_target = "nifty_movers", "kpi-panel-anchor"
        st.rerun()
with kc2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Market Breadth ({tf_choice})</div><div class="kpi-val"><span style="color:#34d399;">🟢 {adv_count} Up</span> | <span style="color:#f87171;">🔴 {dec_count} Down</span></div><div class="kpi-sub-up">{pct_50dma}% Above 50-DMA</div></div>', unsafe_allow_html=True)
    if st.button("📈 Advancing vs Declining", key="k2", use_container_width=True):
        st.session_state.kpi_panel, st.session_state.scroll_target = "breadth_list", "kpi-panel-anchor"
        st.rerun()
with kc3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Top Leading Sector ({tf_choice})</div><div class="kpi-val">👑 {leader_sec["Sector"]}</div><div class="kpi-sub-up">▲ {leader_sec[tf_choice]:+.2f}% (Meter: {leader_sec["Meter"]})</div></div>', unsafe_allow_html=True)
    if st.button(f"🔍 Explore {leader_sec['Sector']}", key="k3", use_container_width=True):
        st.session_state.selected_sector, st.session_state.kpi_panel, st.session_state.scroll_target = leader_sec["Sector"], "leader_sec", "kpi-panel-anchor"
        st.rerun()
with kc4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Oversold Sector ({tf_choice})</div><div class="kpi-val">📉 {laggard_sec["Sector"]}</div><div class="kpi-sub-down">▼ {laggard_sec[tf_choice]:+.2f}% (Turnaround Watch)</div></div>', unsafe_allow_html=True)
    if st.button(f"🔍 Explore {laggard_sec['Sector']}", key="k4", use_container_width=True):
        st.session_state.selected_sector, st.session_state.kpi_panel, st.session_state.scroll_target = laggard_sec["Sector"], "laggard_sec", "kpi-panel-anchor"
        st.rerun()

st.markdown('<div id="kpi-panel-anchor"></div>', unsafe_allow_html=True)

if st.session_state.kpi_panel is not None:
    st.markdown("---")
    kh1, kh2 = st.columns([8.2, 1.8])
    with kh2:
        if st.button("✖ Close List", key="close_kpi", use_container_width=True):
            st.session_state.kpi_panel = None
            st.rerun()
    if st.session_state.kpi_panel == "nifty_movers":
        mv1, mv2 = st.columns(2)
        with mv1:
            st.markdown("##### 🚀 Top 12 Gainers")
            st.dataframe(style_colored_table(stocks_df.sort_values(tf_choice, ascending=False)[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "Action_Signal"]].head(12), ["1D", "1W"]), use_container_width=True, hide_index=True)
        with mv2:
            st.markdown("##### 📉 Top 12 Losers")
            st.dataframe(style_colored_table(stocks_df.sort_values(tf_choice, ascending=True)[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "Action_Signal"]].head(12), ["1D", "1W"]), use_container_width=True, hide_index=True)
    elif st.session_state.kpi_panel == "breadth_list":
        br1, br2 = st.columns(2)
        with br1:
            st.markdown("##### 🟢 Strong Advancing Stocks")
            st.dataframe(style_colored_table(stocks_df[stocks_df[tf_choice] > 0].sort_values("Vol_Ratio", ascending=False)[["Symbol", "Sector", "Price", "1D", "Vol_Ratio", "Action_Signal"]].head(15), ["1D"]), use_container_width=True, hide_index=True)
        with br2:
            st.markdown("##### 🔴 Declining / Oversold Watchlist")
            st.dataframe(style_colored_table(stocks_df[stocks_df[tf_choice] < 0].sort_values("Vol_Ratio", ascending=False)[["Symbol", "Sector", "Price", "1D", "Vol_Ratio", "Action_Signal"]].head(15), ["1D"]), use_container_width=True, hide_index=True)
    else:
        sec_f = st.session_state.selected_sector
        st.markdown(f"#### 🔍 Sector Stocks & Trade Plans: **{sec_f}**")
        sub_s = stocks_df[stocks_df["Sector"] == sec_f].sort_values(tf_choice, ascending=False)
        st.dataframe(style_colored_table(sub_s[["Symbol", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Action_Signal", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W"]), use_container_width=True, hide_index=True)
        st.markdown(f'<div class="pill-container">{"".join([f"<a class=bull-pill href=?focus_stock={urllib.parse.quote(r.Ticker)} target=_self>📈 {r.Symbol} Chart</a>" for _, r in sub_s.iterrows()])}</div>', unsafe_allow_html=True)
    st.markdown("---")

# ==============================================================================
# 13. 4 CONSOLIDATED TABS
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🧭 1. Sector Gauges & Stocks",
    "🎯 2. Intraday Pro Scanners & Risk Calc",
    "💎 3. Swing & Investor Radar",
    "📋 4. All 32 Sectors Matrix"
])

with tab1:
    f_secs = sectors_df.copy()
    if st.session_state.selected_sector != DEFAULT_SECTOR:
        f_secs = f_secs[f_secs["Sector"] == st.session_state.selected_sector]
        if st.button("🔄 Show All 32 Sectors"):
            st.session_state.selected_sector = DEFAULT_SECTOR
            st.rerun()

    sort_col = tf_choice if "Top Gainers" in sort_choice or "Top Losers" in sort_choice else ("Avg_Vol" if "High Volume" in sort_choice else "Meter")
    f_secs = f_secs.sort_values(["Sec_Bull_Turn", "1D"], ascending=[False, False]) if "Bottom Turnaround" in sort_choice else f_secs.sort_values(sort_col, ascending=("Top Losers" in sort_choice))

    def make_gauge(score: int, title_txt: str, ret_val: float):
        bar_col = "#00f5d4" if ("Cyber Neon" in theme_mode and score >= 60) else ("#10b981" if score >= 60 else ("#fbbf24" if score >= 38 else "#ef4444"))
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=score,
            number={"suffix": f" ({ret_val:+.1f}%)", "font": {"size": 14, "color": TEXT_MAIN}},
            title={"text": title_txt, "font": {"size": 13, "color": TEXT_MAIN}},
            gauge={"axis": {"range": [0, 100]}, "bar": {"color": bar_col, "thickness": 0.34}, "bordercolor": BORDER_C,
                   "steps": [{"range": [0, 38], "color": "rgba(239,68,68,0.18)"}, {"range": [38, 60], "color": "rgba(251,191,36,0.18)"}, {"range": [60, 100], "color": "rgba(16,185,129,0.18)"}]}
        ))
        fig.update_layout(height=162, margin=dict(l=14, r=14, t=32, b=8), paper_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_MAIN))
        return fig

    sec_cols = st.columns(2)
    for idx, (_, s_row) in enumerate(f_secs.iterrows()):
        s_name, s_ret, s_meter = s_row["Sector"], safe_num(s_row[tf_choice]), int(safe_num(s_row["Meter"], 50))
        s_stocks = stocks_df[stocks_df["Sector"] == s_name].sort_values(tf_choice, ascending=False)
        with sec_cols[idx % 2]:
            if show_analog_meter:
                st.plotly_chart(make_gauge(s_meter, f"🧭 {s_name}", s_ret), use_container_width=True, key=f"g_{s_name}")
            with st.expander(f"📂 {s_name} ({s_ret:+.2f}%) — {len(s_stocks)} Stocks & Plans", expanded=(len(f_secs) == 1)):
                st.dataframe(style_colored_table(s_stocks[["Symbol", "Price", "1D", "1W", "Vol_Ratio", "RSI", "Action_Signal", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W"]), use_container_width=True, hide_index=True)
                st.markdown(f'<div class="pill-container">{"".join([f"<a class=bull-pill href=?focus_stock={urllib.parse.quote(r.Ticker)} target=_self>📈 {r.Symbol}</a>" for _, r in s_stocks.iterrows()])}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("#### ⚡ 1. 15-Minute Chartink Live Breakout Scanner")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 🟢 15m Bullish Breakouts")
        st.dataframe(style_colored_table(bull_15m_df[["Symbol", "Sector", "Price", "VWAP", "Vol_Ratio", "RSI", "1D", "Entry", "SL", "Target"]], ["1D"]), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("##### 🔴 15m Bearish Breakdowns")
        st.dataframe(style_colored_table(bear_15m_df[["Symbol", "Sector", "Price", "VWAP", "Vol_Ratio", "RSI", "1D", "Entry", "SL", "Target"]], ["1D"]), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 🧮 2. Beginner Position Size & Risk Calculator")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        cap_amt = st.number_input("💰 Total Capital (₹):", min_value=1000.0, value=50000.0, step=5000.0)
    with rc2:
        risk_pct = st.number_input("⚠️ Safe Risk %:", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
    with rc3:
        ent_p = st.number_input("🎯 Entry Price (₹):", min_value=1.0, value=500.0, step=5.0)
    with rc4:
        sl_p = st.number_input("🛑 Stop-Loss (₹):", min_value=0.5, value=490.0, step=5.0)
    max_loss = cap_amt * (risk_pct / 100.0)
    diff = abs(ent_p - sl_p)
    st.success(f"✅ **Max Safe Loss:** ₹{max_loss:,.0f} | 📦 **Quantity to Buy:** `{int(max_loss / diff) if diff > 0 else 0} Shares` | 🎯 **1:2 Target:** `₹{(ent_p + 2*diff if ent_p >= sl_p else ent_p - 2*diff):,.2f}`")

with tab3:
    sw1, sw2 = st.columns(2)
    with sw1:
        st.markdown("##### 🚀 Safe Trend Pullback Picks (Above 50-DMA + Near 20-DMA)")
        sp_df = stocks_df[(stocks_df["Above_50DMA"]) & (stocks_df["Dist_20DMA"].between(-3.0, 4.5)) & (stocks_df["RSI"].between(44, 64))].sort_values("Vol_Ratio", ascending=False)
        st.dataframe(style_colored_table(sp_df[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W", "1M"]), use_container_width=True, hide_index=True)
    with sw2:
        st.markdown("##### 🌱 Value Recovery Picks (Oversold + Turning Up Today)")
        vr_df = stocks_df[(stocks_df["1M"] < 0) & (stocks_df["1D"] > 0) & (stocks_df["RSI"] <= 50)].sort_values("Vol_Ratio", ascending=False)
        st.dataframe(style_colored_table(vr_df[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W", "1M"]), use_container_width=True, hide_index=True)
    st.download_button("📥 Download Full 180+ Stocks CSV Report", data=stocks_df.to_csv(index=False).encode("utf-8"), file_name="alphapulse_report.csv", mime="text/csv", use_container_width=True)

with tab4:
    chart_secs = sectors_df.sort_values(tf_choice, ascending=True)
    fig_b = go.Figure(go.Bar(x=chart_secs[tf_choice], y=chart_secs["Sector"], orientation="h", marker_color=["#10b981" if v >= 0 else "#ef4444" for v in chart_secs[tf_choice]], text=[f"{v:+.2f}%" for v in chart_secs[tf_choice]], textposition="outside"))
    fig_b.update_layout(height=680, template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=40, t=15, b=10), font=dict(color=TEXT_MAIN))
    st.plotly_chart(fig_b, use_container_width=True)
    st.dataframe(style_colored_table(sectors_df.sort_values(tf_choice, ascending=False)[["Sector", "Zone", "Meter", "1D", "1W", "1M", "3M", "6M", "1Y", "Avg_Vol", "RSI", "Breadth_50DMA"]], ["1D", "1W", "1M", "3M", "6M", "1Y"]), use_container_width=True, hide_index=True)

# ==============================================================================
# 14. FLOATING TOP BUTTON & AUTO-SCROLL/AUDIO ENGINE
# ==============================================================================
st.markdown('<a href="#top-anchor" class="single-top-btn" id="alphapulse-top-btn">🚀 Top</a>', unsafe_allow_html=True)

scroll_target_id = st.session_state.scroll_target or ""
st.session_state.scroll_target = None
top_syms = ",".join(bull_15m_df["Symbol"].head(3).tolist()) if not bull_15m_df.empty else ""
should_ring = "true" if (auto_alert_on and top_syms and top_syms != st.session_state.last_alerted) else "false"
if auto_alert_on and top_syms:
    st.session_state.last_alerted = top_syms
reload_js = "setTimeout(function(){ window.parent.location.reload(); }, 180000);" if auto_alert_on else ""

components.html(
    f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        const targetId = "{scroll_target_id}";
        if (targetId) {{
            setTimeout(function() {{
                const el = doc.getElementById(targetId);
                if (el) el.scrollIntoView({{ behavior: "smooth", block: "start" }});
            }}, 320);
        }}
        const btn = doc.getElementById("alphapulse-top-btn");
        if (btn) {{
            btn.addEventListener("click", function(e) {{
                e.preventDefault();
                const anchor = doc.getElementById("top-anchor");
                if (anchor) anchor.scrollIntoView({{ behavior: "smooth", block: "start" }});
                [doc.querySelector('[data-testid="stAppViewContainer"]'), doc.querySelector('[data-testid="stMain"]'), doc.documentElement, doc.body].forEach(function(el) {{
                    if (el && el.scrollTo) el.scrollTo({{ top: 0, behavior: "smooth" }});
                }});
            }});
        }}
        if ({should_ring}) {{
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.frequency.setValueAtTime(880, ctx.currentTime);
                gain.gain.setValueAtTime(0.15, ctx.currentTime);
                osc.connect(gain); gain.connect(ctx.destination);
                osc.start(); osc.stop(ctx.currentTime + 0.5);
            }} catch (e) {{}}
        }}
        {reload_js}
    }})();
    </script>
    """,
    height=0,
    width=0
)
