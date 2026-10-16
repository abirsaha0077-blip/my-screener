from urllib.parse import quote, unquote
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# ==============================================================================
# ১. পেজ সেটআপ (ফুল-স্ক্রিন ফিনান্সিয়াল টার্মিনাল মোড)
# ==============================================================================
st.set_page_config(
    page_title="AlphaPulse Pro | Intraday, Swing & Sector Terminal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# ২. ৩২টি মাইক্রো-সেক্টর, ম্যাক্রো ইনডেক্স এবং আসল NIFTY 50-এর তালিকা
# ==============================================================================
sectors = {
    "Defence & Aerospace": [
        "HAL.NS", "BEL.NS", "BDL.NS", "MAZDOCK.NS", "DATAPATTNS.NS", "PARAS.NS"
    ],
    "Shipbuilding & Marine": [
        "MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "SCI.NS", "GEESHIP.NS"
    ],
    "Railways & Wagons": [
        "RVNL.NS", "IRFC.NS", "TITAGARH.NS", "JWL.NS", "IRCON.NS", "TEXRAIL.NS", "BEML.NS"
    ],
    "Cables & Wires": [
        "POLYCAB.NS", "KEI.NS", "FINCABLES.NS", "RRKABEL.NS", "UNIVERSAL.NS"
    ],
    "Transformers & Power T&D": [
        "CGPOWER.NS", "ABB.NS", "SIEMENS.NS", "TARIL.NS", "VOLTAMP.NS"
    ],
    "EMS (Electronics Mfg)": [
        "DIXON.NS", "KAYNES.NS", "SYRMA.NS", "CYIENTDLM.NS", "AMBER.NS", "PGEL.NS"
    ],
    "Green Energy & Solar": [
        "IREDA.NS", "SUZLON.NS", "KPIGREEN.NS", "WAAREEENER.NS", "BORORENEW.NS", "INOXWIND.NS"
    ],
    "Power Utilities & Finance": [
        "PFC.NS", "RECLTD.NS", "POWERGRID.NS", "NTPC.NS", "TATAPOWER.NS", "JSWENERGY.NS"
    ],
    "Cooling, HVAC & Data Center": [
        "VOLTAS.NS", "BLUESTARCO.NS", "KIRLOSENG.NS", "TRITURBINE.NS", "ANUP.NS", "ELGIEQUIP.NS"
    ],
    "CNC, Bearings & Precision Engg": [
        "SKFINDIA.NS", "TIMKEN.NS", "SCHAEFFLER.NS", "THERMAX.NS", "CUMMINSIND.NS", "MTARTECH.NS"
    ],
    "Pre-Engineered & Infra EPC": [
        "LT.NS", "KPIL.NS", "KEC.NS", "PENNARIND.NS", "NCC.NS", "PNCINFRA.NS"
    ],
    "Real Estate & Developers": [
        "DLF.NS", "MACROTECH.NS", "PRESTIGE.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "BRIGADE.NS"
    ],
    "Building Materials (Pipes & Sanitary)": [
        "ASTRAL.NS", "SUPREMEIND.NS", "CERA.NS", "KAJARIACER.NS", "CENTURYPLY.NS", "FINPIPE.NS"
    ],
    "CDMO & API Pharma": [
        "LAURUSLABS.NS", "DIVISLAB.NS", "NEULANDLAB.NS", "SYNGENE.NS", "SUVENPHAR.NS", "PIRAMALPH.NS"
    ],
    "Largecap & US Generics Pharma": [
        "SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "LUPIN.NS", "AUROPHARMA.NS", "ZYDUSLIFE.NS"
    ],
    "Hospitals & Diagnostics": [
        "APOLLOHOSP.NS", "MAXHEALTH.NS", "LALPATHLAB.NS", "NH.NS", "METROPOLIS.NS", "FORTIS.NS"
    ],
    "QSR & Food Chains": [
        "JUBLFOOD.NS", "DEVYANI.NS", "WESTLIFE.NS", "RBA.NS", "SAPPHIRE.NS"
    ],
    "FMCG Staples": [
        "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS", "TATACONSUM.NS", "DABUR.NS", "MARICO.NS"
    ],
    "Retail, Apparel & Footwear": [
        "TRENT.NS", "DMART.NS", "METROBRAND.NS", "BATAINDIA.NS", "MANYAVAR.NS", "PAGEIND.NS"
    ],
    "Jewellery & Luxury": [
        "TITAN.NS", "KALYANKJIL.NS", "SENCO.NS", "THANGAMAYL.NS"
    ],
    "Auto OEMs & EV": [
        "M&M.NS", "TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "TVSMOTOR.NS", "OLECTRA.NS", "EICHERMOT.NS"
    ],
    "Auto Ancillaries & Tyres": [
        "MOTHERSON.NS", "SONACOMS.NS", "UNOMINDA.NS", "MRF.NS", "BALKRISIND.NS", "APOLLOTYRE.NS"
    ],
    "IT Largecap": [
        "TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"
    ],
    "IT Midcap & Niche Tech": [
        "PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS", "ZENSARTECH.NS", "AFFLE.NS"
    ],
    "PSU Banks": [
        "SBIN.NS", "PNB.NS", "BANKBARODA.NS", "CANBK.NS", "UNIONBANK.NS", "INDIANB.NS"
    ],
    "Private Banks": [
        "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "FEDERALBNK.NS"
    ],
    "NBFCs & Housing Finance": [
        "BAJFINANCE.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "LICHSGFIN.NS", "MANAPPURAM.NS"
    ],
    "Capital Market & Wealth": [
        "BSE.NS", "CDSL.NS", "MCX.NS", "ANGELONE.NS", "MOTILALOFS.NS", "CAMS.NS"
    ],
    "Specialty Chemicals & Agrochem": [
        "SRF.NS", "PIIND.NS", "NAVINFLUOR.NS", "DEEPAKNTR.NS", "AARTIIND.NS", "CLEAN.NS"
    ],
    "Packaging & BOPP Films": [
        "UFLEX.NS", "JINDALPOLY.NS", "COSMOFIRST.NS", "EPL.NS", "MOLDTKPAC.NS"
    ],
    "Hotels & Aviation": [
        "INDIGO.NS", "INDHOTEL.NS", "EIHOTEL.NS", "LEMONTREE.NS", "CHALET.NS"
    ],
    "Metals & Mining": [
        "TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "COALINDIA.NS", "VEDL.NS", "NMDC.NS"
    ],
}

NIFTY_50_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS",
    "INFY.NS", "SBIN.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS",
    "BAJFINANCE.NS", "HCLTECH.NS", "SUNPHARMA.NS", "MARUTI.NS", "M&M.NS",
    "KOTAKBANK.NS", "AXISBANK.NS", "NTPC.NS", "ULTRACEMCO.NS", "TITAN.NS",
    "TATAMOTORS.NS", "POWERGRID.NS", "ADANIENT.NS", "ADANIPORTS.NS", "HAL.NS",
    "BEL.NS", "TRENT.NS", "COALINDIA.NS", "BAJAJ-AUTO.NS", "ASIANPAINT.NS",
    "WIPRO.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "NESTLEIND.NS", "GRASIM.NS",
    "ONGC.NS", "SBILIFE.NS", "DRREDDY.NS", "CIPLA.NS", "HINDALCO.NS",
    "TECHM.NS", "EICHERMOT.NS", "SHRIRAMFIN.NS", "BPCL.NS", "BRITANNIA.NS",
    "APOLLOHOSP.NS", "TATACONSUM.NS", "INDUSINDBK.NS", "DIVISLAB.NS", "LTIM.NS"
]

benchmark = "^NSEI"
macro_tickers = ["^NSEI", "^NSEBANK", "^INDIAVIX", "USDINR=X"]
all_tickers = sorted(
    list(set(macro_tickers + NIFTY_50_TICKERS + [t for s in sectors.values() for t in s]))
)

# ==============================================================================
# ৩. টপ হেডার বার (থিম সিলেক্টর ও মিটার সুইচ)
# ==============================================================================
top_h1, top_h2, top_h3 = st.columns([2.7, 1.1, 0.8])
with top_h1:
    st.markdown("## 🧭 AlphaPulse Pro — Intraday, Swing & Sector Terminal")
with top_h2:
    theme_choice = st.selectbox(
        "🎨 থিম (Theme):",
        [
            "🌙 Pro Dark (ডার্ক থিম)",
            "☀️ Pure White (সাদা থিম)",
            "💎 Frost Blue (ব্লু থিম)",
        ],
        index=0,
        label_visibility="collapsed",
    )
with top_h3:
    show_card_meter = st.toggle("🎛️ অ্যানালগ মিটার", value=True)

# ==============================================================================
# ৪. থিম কালার ও প্রফেশনাল সিএসএস (ফ্লোটিং Back-to-Top বাটন সহ)
# ==============================================================================
if "Pure White" in theme_choice:
    bg_color = "#f4f6f9"
    card_bg = "#ffffff"
    input_bg = "#ffffff"
    text_color = "#0f172a"
    sub_text = "#475569"
    border_col = "#cbd5e1"
    chart_bg = "#ffffff"
    grid_col = "rgba(15, 23, 42, 0.08)"
    nifty_col_line = "#475569"
    accent_col = "#2563eb"
    shadow_css = "0 6px 18px rgba(15, 23, 42, 0.06)"
elif "Frost Blue" in theme_choice:
    bg_color = "#eef6ff"
    card_bg = "#ffffff"
    input_bg = "#ffffff"
    text_color = "#082f49"
    sub_text = "#334155"
    border_col = "#93c5fd"
    chart_bg = "#ffffff"
    grid_col = "rgba(8, 47, 73, 0.08)"
    nifty_col_line = "#0284c7"
    accent_col = "#0284c7"
    shadow_css = "0 6px 18px rgba(2, 132, 199, 0.08)"
else:
    bg_color = "#090d16"
    card_bg = "#111827"
    input_bg = "#1e293b"
    text_color = "#f8fafc"
    sub_text = "#94a3b8"
    border_col = "#334155"
    chart_bg = "#111827"
    grid_col = "rgba(255, 255, 255, 0.08)"
    nifty_col_line = "#facc15"
    accent_col = "#38bdf8"
    shadow_css = "0 8px 24px rgba(0, 0, 0, 0.55)"

css_template = """
<style>
header[data-testid="stHeader"] {
    display: none !important;
}
section[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
.stApp {
    background-color: __BG_COLOR__ !important;
    color: __TEXT_COLOR__ !important;
}
.block-container {
    padding-top: 0.9rem !important;
    padding-bottom: 2rem !important;
    padding-left: 1.6rem !important;
    padding-right: 1.6rem !important;
    max-width: 100% !important;
}
h1, h2, h3, h4, h5, h6, label {
    color: __TEXT_COLOR__ !important;
}
div[data-baseweb="select"] > div {
    background-color: __INPUT_BG__ !important;
    color: __TEXT_COLOR__ !important;
    border: 1.5px solid __BORDER_COL__ !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within {
    border-color: __ACCENT_COL__ !important;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.28) !important;
}
div[data-baseweb="select"] span {
    color: __TEXT_COLOR__ !important;
}
div[data-baseweb="popover"] ul {
    background-color: __CARD_BG__ !important;
    border: 1px solid __BORDER_COL__ !important;
}
div[data-baseweb="popover"] li {
    color: __TEXT_COLOR__ !important;
    cursor: pointer !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: __ACCENT_COL__ !important;
    height: 3px !important;
}
div[data-baseweb="tab-border"] {
    background-color: __BORDER_COL__ !important;
}
button[data-baseweb="tab"] {
    background-color: __CARD_BG__ !important;
    color: __TEXT_COLOR__ !important;
    border: 1px solid __BORDER_COL__ !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 10px 16px !important;
    margin-right: 6px !important;
    font-weight: 700 !important;
    font-size: 13.5px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
button[data-baseweb="tab"] p,
button[data-baseweb="tab"] span {
    color: __TEXT_COLOR__ !important;
    font-weight: 700 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: rgba(56, 189, 248, 0.14) !important;
    border-color: __ACCENT_COL__ !important;
    border-bottom: 3px solid __ACCENT_COL__ !important;
    color: __ACCENT_COL__ !important;
}
button[data-baseweb="tab"][aria-selected="true"] p,
button[data-baseweb="tab"][aria-selected="true"] span {
    color: __ACCENT_COL__ !important;
}
div.stButton > button {
    width: 100%;
    background-color: __INPUT_BG__ !important;
    color: __ACCENT_COL__ !important;
    border: 1px solid __BORDER_COL__ !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 7px 12px !important;
    cursor: pointer !important;
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    border-color: __ACCENT_COL__ !important;
    background-color: rgba(56, 189, 248, 0.16) !important;
    transform: translateY(-1px);
}
div[data-testid="stExpander"] details {
    background-color: __CARD_BG__ !important;
    border: 1px solid __BORDER_COL__ !important;
    border-radius: 12px !important;
    padding: 4px 10px !important;
}
div[data-testid="stExpander"] summary {
    cursor: pointer !important;
}
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary p {
    color: __TEXT_COLOR__ !important;
    font-weight: 700 !important;
    font-size: 14px !important;
}
div[data-testid="stExpander"] summary:hover span,
div[data-testid="stExpander"] summary:hover p {
    color: __ACCENT_COL__ !important;
}
div[data-testid="stMetric"] {
    background-color: __CARD_BG__ !important;
    border: 1px solid __BORDER_COL__ !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    box-shadow: __SHADOW_CSS__ !important;
}
div[data-testid="stMetricLabel"] p {
    color: __SUB_TEXT__ !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricValue"] div {
    color: __TEXT_COLOR__ !important;
    font-weight: 800 !important;
}
.pro-card {
    background-color: __CARD_BG__;
    border: 1px solid __BORDER_COL__;
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 10px;
    box-shadow: __SHADOW_CSS__;
    transition: all 0.2s ease;
}
.pro-card:hover {
    border-color: __ACCENT_COL__;
}
.focus-drawer {
    background-color: __CARD_BG__;
    border: 2px solid __ACCENT_COL__;
    border-radius: 16px;
    padding: 18px 22px;
    margin: 10px 0 18px 0;
    box-shadow: 0 10px 30px rgba(56, 189, 248, 0.18);
}
.intraday-bull-box {
    background: linear-gradient(135deg, rgba(0, 230, 118, 0.08) 0%, __CARD_BG__ 100%);
    border: 1px solid rgba(0, 230, 118, 0.4);
    border-left: 5px solid #00e676;
    border-radius: 14px;
    padding: 12px 15px;
    margin-bottom: 12px;
    box-shadow: __SHADOW_CSS__;
}
.intraday-bear-box {
    background: linear-gradient(135deg, rgba(255, 82, 82, 0.08) 0%, __CARD_BG__ 100%);
    border: 1px solid rgba(255, 82, 82, 0.4);
    border-left: 5px solid #ff5252;
    border-radius: 14px;
    padding: 12px 15px;
    margin-bottom: 12px;
    box-shadow: __SHADOW_CSS__;
}
.focus-pill-bull {
    display: inline-block;
    margin: 4px 6px 4px 0;
    padding: 5px 11px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 700;
    background: rgba(0, 230, 118, 0.15);
    border: 1px solid rgba(0, 230, 118, 0.45);
    color: #00e676 !important;
    text-decoration: none !important;
}
.focus-pill-bull:hover {
    background: rgba(0, 230, 118, 0.28);
}
.focus-pill-bear {
    display: inline-block;
    margin: 4px 6px 4px 0;
    padding: 5px 11px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 700;
    background: rgba(255, 82, 82, 0.15);
    border: 1px solid rgba(255, 82, 82, 0.45);
    color: #ff5252 !important;
    text-decoration: none !important;
}
.focus-pill-bear:hover {
    background: rgba(255, 82, 82, 0.28);
}
.macro-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    background-color: __CARD_BG__;
    border: 1px solid __BORDER_COL__;
    border-radius: 12px;
    padding: 8px 16px;
    margin-bottom: 12px;
    box-shadow: __SHADOW_CSS__;
}
.macro-item {
    font-size: 13px;
    font-weight: 700;
    color: __TEXT_COLOR__;
}
.kpi-card {
    background-color: __CARD_BG__;
    border: 1px solid __BORDER_COL__;
    border-top: 4px solid __ACCENT_COL__;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: __SHADOW_CSS__;
    margin-bottom: 6px;
    min-height: 112px;
}
.kpi-title {
    font-size: 13px;
    font-weight: 700;
    color: __SUB_TEXT__ !important;
    margin-bottom: 4px;
}
.kpi-main {
    font-size: 18px;
    font-weight: 800;
    color: __TEXT_COLOR__ !important;
    line-height: 1.3;
    margin-bottom: 6px;
}
.kpi-sub-pos {
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    color: #00e676 !important;
    background: rgba(0, 230, 118, 0.14);
    padding: 2px 9px;
    border-radius: 99px;
}
.kpi-sub-neg {
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    color: #ff5252 !important;
    background: rgba(255, 82, 82, 0.14);
    padding: 2px 9px;
    border-radius: 99px;
}
.badge-green {
    background: rgba(0, 230, 118, 0.16);
    color: #00e676 !important;
    border: 1px solid rgba(0, 230, 118, 0.45);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 14px;
}
.badge-red {
    background: rgba(255, 82, 82, 0.16);
    color: #ff5252 !important;
    border: 1px solid rgba(255, 82, 82, 0.45);
    padding: 4px 12px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 14px;
}
.stage-banner {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 700;
    margin: 6px 0;
    background: rgba(56, 189, 248, 0.12);
    color: __TEXT_COLOR__ !important;
    border-left: 4px solid __ACCENT_COL__;
}
.action-btn {
    display: inline-block;
    padding: 4px 10px;
    margin: 3px 4px 3px 0;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none !important;
    border: 1px solid __BORDER_COL__;
    background: __INPUT_BG__;
    color: __TEXT_COLOR__ !important;
}
.action-btn:hover {
    border-color: __ACCENT_COL__;
    background: rgba(56, 189, 248, 0.18);
}
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: __CARD_BG__;
    border: 1px solid __BORDER_COL__;
    border-radius: 12px;
    padding: 10px 14px;
    margin: 6px 0 12px 0;
    white-space: nowrap;
    box-shadow: __SHADOW_CSS__;
}
.ticker-move {
    display: inline-block;
    animation: ticker 185s linear infinite;
}
.ticker-wrap:hover .ticker-move {
    animation-play-state: paused;
}
a.ticker-chip-up {
    display: inline-block;
    margin-right: 16px;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 13.5px;
    font-weight: 800;
    background: rgba(0, 230, 118, 0.14);
    border: 1px solid rgba(0, 230, 118, 0.45);
    color: #00e676 !important;
    text-decoration: none !important;
    cursor: pointer !important;
    transition: all 0.18s ease;
}
a.ticker-chip-up:hover {
    background: rgba(0, 230, 118, 0.28);
    transform: scale(1.05);
}
a.ticker-chip-down {
    display: inline-block;
    margin-right: 16px;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 13.5px;
    font-weight: 800;
    background: rgba(255, 82, 82, 0.14);
    border: 1px solid rgba(255, 82, 82, 0.45);
    color: #ff5252 !important;
    text-decoration: none !important;
    cursor: pointer !important;
    transition: all 0.18s ease;
}
a.ticker-chip-down:hover {
    background: rgba(255, 82, 82, 0.28);
    transform: scale(1.05);
}
/* ফ্লোটিং Back to Top বাটন */
.back-to-top {
    position: fixed;
    bottom: 25px;
    right: 25px;
    background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
    color: #ffffff !important;
    padding: 10px 16px;
    border-radius: 99px;
    font-weight: 800;
    font-size: 13.5px;
    text-decoration: none !important;
    box-shadow: 0 4px 20px rgba(56, 189, 248, 0.5);
    z-index: 99999;
    transition: transform 0.2s ease;
}
.back-to-top:hover {
    transform: scale(1.08);
}
@keyframes ticker {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-50%); }
}
</style>
"""

final_css = (
    css_template.replace("__BG_COLOR__", bg_color)
    .replace("__CARD_BG__", card_bg)
    .replace("__INPUT_BG__", input_bg)
    .replace("__TEXT_COLOR__", text_color)
    .replace("__SUB_TEXT__", sub_text)
    .replace("__BORDER_COL__", border_col)
    .replace("__ACCENT_COL__", accent_col)
    .replace("__SHADOW_CSS__", shadow_css)
)
st.markdown(final_css, unsafe_allow_html=True)

# ફ্লোটিং ব্যাক-টু-টপ বাটন রেন্ডার করা
st.markdown('<a class="back-to-top" href="#" target="_self">🚀 ওপরে যান (Top)</a>', unsafe_allow_html=True)

# ==============================================================================
# ৫. ডেটা ইঞ্জিন (Close, High, Low, Open, Volume)
# ==============================================================================
@st.cache_data(ttl=3600)
def load_full_market_data():
    raw = yf.download(all_tickers, period="5y", interval="1d", auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        lvl0 = raw.columns.levels[0]
        close_df = raw["Close"].ffill() if "Close" in lvl0 else pd.DataFrame()
        high_df = raw["High"].ffill() if "High" in lvl0 else close_df.copy()
        low_df = raw["Low"].ffill() if "Low" in lvl0 else close_df.copy()
        open_df = raw["Open"].ffill() if "Open" in lvl0 else close_df.copy()
        vol_df = raw["Volume"].fillna(0) if "Volume" in lvl0 else pd.DataFrame()
    else:
        close_df = raw.ffill()
        high_df = close_df.copy()
        low_df = close_df.copy()
        open_df = close_df.copy()
        vol_df = pd.DataFrame(index=close_df.index)
    return close_df, high_df, low_df, open_df, vol_df

with st.spinner("মার্কেট ডেটা, প্রাইস অ্যাকশন ও ইন্ট্রাডে টার্নঅ্যারাউন্ড রাডার প্রস্তুত হচ্ছে..."):
    full_df, full_high_df, full_low_df, full_open_df, full_vol_df = load_full_market_data()

tf_days_map = {
    "1D": 2, "1W": 6, "1M": 22, "3M": 64, "6M": 126, "1Y": 252, "3Y": 756, "5Y": len(full_df)
}

def calc_return(series, days):
    s = series.dropna()
    if len(s) < 2:
        return 0.0
    sub = s.tail(min(days, len(s)))
    if len(sub) < 2 or sub.iloc[0] == 0:
        return 0.0
    return round(((sub.iloc[-1] / sub.iloc[0]) - 1) * 100, 2)

def calc_rsi(series, period=14):
    s = series.dropna()
    if len(s) < period + 2:
        return 50.0
    delta = s.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    last_g = float(gain.iloc[-1]) if not pd.isna(gain.iloc[-1]) else 0.0
    last_l = float(loss.iloc[-1]) if not pd.isna(loss.iloc[-1]) else 0.0
    if last_l == 0:
        return 100.0 if last_g > 0 else 50.0
    rs = last_g / last_l
    return round(100.0 - (100.0 / (1.0 + rs)), 1)

def calc_rvol(t_sym):
    if full_vol_df is None or t_sym not in full_vol_df.columns:
        return 1.0, "📊 1.0x (Normal)"
    v = full_vol_df[t_sym].replace(0, np.nan).dropna()
    if len(v) < 21:
        return 1.0, "📊 1.0x (Normal)"
    curr_v = float(v.iloc[-1])
    avg_v = float(v.iloc[-21:-1].mean())
    if avg_v <= 0:
        return 1.0, "📊 1.0x (Normal)"
    ratio = round(curr_v / avg_v, 2)
    if ratio >= 2.0:
        return ratio, f"🔥 {ratio}x (Huge Vol)"
    elif ratio >= 1.35:
        return ratio, f"⚡ {ratio}x (High Vol)"
    elif ratio <= 0.55:
        return ratio, f"💤 {ratio}x (Low Vol)"
    return ratio, f"📊 {ratio}x (Normal)"

def style_colored_table(df_in, primary_col):
    if df_in is None or df_in.empty:
        return df_in

    clean_df = df_in.loc[:, ~df_in.columns.duplicated()].copy().reset_index(drop=True)
    pct_candidates = ["1D %", "1W %", "1M %", "3M %", "6M %", "1Y %", "5Y %", "From 52W High %", "Day Range Pos %"]
    pct_cols = [c for c in pct_candidates if c in clean_df.columns]

    price_candidates = ["CMP (₹)", "Buy Above (₹)", "Sell Below (₹)", "Stop Loss (₹)", "Target 1 (₹)", "Target 2 (₹)"]
    price_cols = [c for c in price_candidates if c in clean_df.columns]

    fmt = {}
    for pc in price_cols:
        fmt[pc] = "₹{:.2f}"
    if "RSI (14)" in clean_df.columns:
        fmt["RSI (14)"] = "{:.1f}"
    if "Meter Score" in clean_df.columns:
        fmt["Meter Score"] = "{:.0f}/100"
    if "Now Meter (0-100)" in clean_df.columns:
        fmt["Now Meter (0-100)"] = "{:.1f}"
    if "Prev Meter" in clean_df.columns:
        fmt["Prev Meter"] = "{:.1f}"
    if "Shift (Δ)" in clean_df.columns:
        fmt["Shift (Δ)"] = "{:+.1f}"
    if "Avg RSI" in clean_df.columns:
        fmt["Avg RSI"] = "{:.1f}"
    for c in pct_cols:
        if c == "Day Range Pos %":
            fmt[c] = "{:.0f}%"
        else:
            fmt[c] = "{:+.2f}%"

    def row_tint(row):
        val = row.get(primary_col, 0.0)
        if not isinstance(val, (int, float, np.number)) or pd.isna(val):
            return [""] * len(row)
        if val >= 0:
            return ["background-color: rgba(0, 230, 118, 0.12);"] * len(row)
        return ["background-color: rgba(255, 82, 82, 0.12);"] * len(row)

    def cell_tint(val):
        if not isinstance(val, (int, float, np.number)) or pd.isna(val):
            return ""
        if val > 0:
            return "background-color: rgba(0, 230, 118, 0.24); color: #00e676; font-weight: 700;"
        elif val < 0:
            return "background-color: rgba(255, 82, 82, 0.24); color: #ff5252; font-weight: 700;"
        return ""

    tint_subset = [c for c in pct_cols if c != "Day Range Pos %"]
    try:
        styler = clean_df.style.apply(row_tint, axis=1)
        if tint_subset:
            if hasattr(styler, "map"):
                styler = styler.map(cell_tint, subset=tint_subset)
            else:
                styler = styler.applymap(cell_tint, subset=tint_subset)
        return styler.format(fmt)
    except Exception:
        return clean_df

def make_analog_gauge(score, prev_score, title_txt, height_px=215):
    if score >= 60:
        bar_col = "#00e676"
    elif score >= 48:
        bar_col = "#84cc16"
    elif score >= 38:
        bar_col = "#f59e0b"
    else:
        bar_col = "#ff5252"

    fig_g = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=score,
            delta={
                "reference": prev_score,
                "increasing": {"color": "#00e676"},
                "decreasing": {"color": "#ff5252"},
                "valueformat": ".1f",
            },
            title={"text": title_txt, "font": {"size": 12, "color": text_color}},
            number={"font": {"size": 23, "color": text_color}, "valueformat": ".0f"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": sub_text},
                "bar": {"color": bar_col, "thickness": 0.32},
                "bgcolor": chart_bg,
                "borderwidth": 1,
                "bordercolor": border_col,
                "steps": [
                    {"range": [0, 38], "color": "rgba(255, 82, 82, 0.22)"},
                    {"range": [38, 48], "color": "rgba(245, 158, 11, 0.22)"},
                    {"range": [48, 60], "color": "rgba(132, 204, 22, 0.22)"},
                    {"range": [60, 100], "color": "rgba(0, 230, 118, 0.28)"},
                ],
                "threshold": {
                    "line": {"color": text_color, "width": 4},
                    "thickness": 0.82,
                    "value": score,
                },
            },
        )
    )
    fig_g.update_layout(
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font={"color": text_color},
        height=height_px,
        margin=dict(t=32, b=8, l=18, r=18),
    )
    return fig_g

# ==============================================================================
# ৬. ম্যাক্রো মার্কেট পালস রিবন
# ==============================================================================
def get_macro_stat(sym):
    if sym not in full_df.columns or len(full_df[sym].dropna()) < 3:
        return 0.0, 0.0
    s = full_df[sym].dropna()
    return round(float(s.iloc[-1]), 2), calc_return(s, 2)

n50_lvl, n50_1d = get_macro_stat("^NSEI")
bnk_lvl, bnk_1d = get_macro_stat("^NSEBANK")
vix_lvl, vix_1d = get_macro_stat("^INDIAVIX")
usd_lvl, usd_1d = get_macro_stat("USDINR=X")

vix_mood = "🟢 স্বস্তিদায়ক (Low Fear)" if vix_lvl < 15 else ("🟡 সতর্কতা (Moderate)" if vix_lvl < 20 else "🔴 উচ্চ ঝুঁকি (High Fear)")
n50_col_str = "#00e676" if n50_1d >= 0 else "#ff5252"
bnk_col_str = "#00e676" if bnk_1d >= 0 else "#ff5252"
vix_col_str = "#ff5252" if vix_1d > 0 else "#00e676"

st.markdown(
    f"""
    <div class="macro-strip">
        <div class="macro-item">🇮🇳 <b>Nifty 50:</b> {n50_lvl:,.1f} <span style="color:{n50_col_str};">({n50_1d:+.2f}%)</span></div>
        <div class="macro-item">🏦 <b>Bank Nifty:</b> {bnk_lvl:,.1f} <span style="color:{bnk_col_str};">({bnk_1d:+.2f}%)</span></div>
        <div class="macro-item">⚡ <b>India VIX:</b> {vix_lvl:.2f} <span style="color:{vix_col_str};">({vix_1d:+.2f}%)</span> — {vix_mood}</div>
        <div class="macro-item">💵 <b>USD/INR:</b> ₹{usd_lvl:.2f} <span style="color:{sub_text};">({usd_1d:+.2f}%)</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# ৭. ৫টি মূল কন্ট্রোল মেনু
# ==============================================================================
if "ctrl_sec_jump" not in st.session_state:
    st.session_state["ctrl_sec_jump"] = "সবগুলো সেক্টর (Show All 32)"

def reset_single_sector_lock():
    st.session_state["ctrl_sec_jump"] = "সবগুলো সেক্টর (Show All 32)"
    try:
        if "focus_sec" in st.query_params:
            del st.query_params["focus_sec"]
    except Exception:
        pass

all_unique_stock_names = sorted(list(set([t.replace(".NS", "") for s in sectors.values() for t in s])))

c1, c2, c3, c4, c5 = st.columns([0.9, 1.35, 1.35, 1.25, 1.25])
with c1:
    tf_option = st.selectbox(
        "📅 ১. টাইমফ্রেম:",
        ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"],
        index=1,
        key="ctrl_tf",
    )
with c2:
    sort_option = st.selectbox(
        "🔃 ২. সাজানোর ক্রম (Sort By):",
        [
            "🚀 Top Gainers (সবচেয়ে বেশি বাড়া আগে)",
            "📉 Top Losers (সবচেয়ে বেশি ডাউন আগে)",
            "🔄 Red ➔ Green (নিচ থেকে ঘুরছে আগে)",
            "⚠️ Green ➔ Red (উপর থেকে নামছে আগে)",
            "🧭 Meter: High to Low (সর্বোচ্চ মিটার আগে)",
            "🧭 Meter: Low to High (সর্বনিম্ন মিটার আগে)",
        ],
        key="ctrl_sort",
        on_change=reset_single_sector_lock,
    )
with c3:
    zone_filter_choice = st.selectbox(
        "🎯 ৩. রোটেশন জোন ফিল্টার:",
        [
            "🌐 সব সেক্টর (All 32 Sectors)",
            "🚀 Strong Green (আপট্রেন্ড লিডার)",
            "🔄 Red ➔ Green (টার্নঅ্যারাউন্ড জোন)",
            "🟡 Yellow Zone (ওয়াচলিস্ট জোন)",
            "⚠️ Green ➔ Red (কুলিং অফ জোন)",
            "🔴 Red Zone (ডিপ ভ্যালু / ডাউন)",
        ],
        key="ctrl_zone",
        on_change=reset_single_sector_lock,
    )
with c4:
    quick_sec_jump = st.selectbox(
        "🔍 ৪. নির্দিষ্ট সেক্টর খুঁজুন:",
        ["সবগুলো সেক্টর (Show All 32)"] + sorted(list(sectors.keys())),
        key="ctrl_sec_jump",
    )
with c5:
    instant_stock_search = st.selectbox(
        "⚡ ৫. যেকোনো শেয়ার খুঁজুন (Stock Search):",
        ["শেয়ার টাইপ করুন..."] + all_unique_stock_names,
        key="ctrl_stk_search",
    )

ret_key = f"{tf_option} %"

# ==============================================================================
# ৮. সেক্টর ও স্টকের সম্পূর্ণ ক্যালকুলেশন (নিচ থেকে ঘুরে দাঁড়ানো Turnaround Reversal লজিকসহ)
# ==============================================================================
nifty_col = full_df[benchmark] if benchmark in full_df.columns else pd.Series(dtype=float)
nifty_multi_ret = {tf: calc_return(nifty_col, d) for tf, d in tf_days_map.items()}
nifty_curr_val = nifty_multi_ret[tf_option]

sector_master = []
all_stocks_master = {}

ticker_to_sector = {}
for s_nm, t_list in sectors.items():
    for t_sym in t_list:
        if t_sym not in ticker_to_sector:
            ticker_to_sector[t_sym] = s_nm

def compute_stock_row(t, s_name_label):
    s_price = full_df[t].dropna()
    curr_p = round(float(s_price.iloc[-1]), 2)
    high_52w = float(s_price.tail(252).max())
    low_52w = float(s_price.tail(252).min())
    dd_52w = round(((curr_p / high_52w) - 1) * 100, 2) if high_52w > 0 else 0.0

    day_high = float(full_high_df[t].dropna().iloc[-1]) if t in full_high_df.columns and len(full_high_df[t].dropna()) > 0 else curr_p
    day_low = float(full_low_df[t].dropna().iloc[-1]) if t in full_low_df.columns and len(full_low_df[t].dropna()) > 0 else curr_p
    day_open = float(full_open_df[t].dropna().iloc[-1]) if t in full_open_df.columns and len(full_open_df[t].dropna()) > 0 else curr_p

    day_range = max(day_high - day_low, 0.01)
    clv_pct = round(float(np.clip(((curr_p - day_low) / day_range) * 100.0, 0.0, 100.0)), 1)

    if t in full_high_df.columns and t in full_low_df.columns:
        recent_ranges = (full_high_df[t].tail(14) - full_low_df[t].tail(14)).dropna()
        atr_val = float(recent_ranges.mean()) if len(recent_ranges) > 0 else curr_p * 0.02
    else:
        atr_val = curr_p * 0.02
    atr_val = max(atr_val, curr_p * 0.012)

    buy_above = round(max(day_high, curr_p) * 1.001, 2)
    bull_sl = round(buy_above - (atr_val * 0.65), 2)
    bull_t1 = round(buy_above + (atr_val * 0.85), 2)
    bull_t2 = round(buy_above + (atr_val * 1.65), 2)

    sell_below = round(min(day_low, curr_p) * 0.999, 2)
    bear_sl = round(sell_below + (atr_val * 0.65), 2)
    bear_t1 = round(sell_below - (atr_val * 0.85), 2)
    bear_t2 = round(sell_below - (atr_val * 1.65), 2)

    sma50_val = float(s_price.tail(50).mean()) if len(s_price) >= 50 else curr_p
    sma200_val = float(s_price.tail(200).mean()) if len(s_price) >= 200 else curr_p
    above_50dma = curr_p >= sma50_val
    above_200dma = curr_p >= sma200_val

    rsi_14 = calc_rsi(s_price, 14)
    rvol_num, rvol_label = calc_rvol(t)

    r_map = {
        "1D %": calc_return(s_price, 2),
        "1W %": calc_return(s_price, 6),
        "1M %": calc_return(s_price, 22),
        "3M %": calc_return(s_price, 64),
        "6M %": calc_return(s_price, 126),
        "1Y %": calc_return(s_price, 252),
        "5Y %": calc_return(s_price, len(full_df)),
    }

    r_1d = r_map["1D %"]
    r_1w = r_map["1W %"]
    r_sel = r_map[ret_key]
    st_score = float(np.clip(50 + (r_sel * 2.0) + (r_1w * 1.2) + ((rsi_14 - 50) * 0.3), 2, 98))
    st_prev = float(np.clip(50 + (r_map["3M %"] * 0.9) + (r_map["1Y %"] * 0.3), 2, 98))

    # ইন্ট্রাডে টার্নঅ্যারাউন্ড ও রিভার্সাল ফোকাস লজিক (যা অলরেডি ৩-৪ দিন বেড়ে যাওয়া স্টক ফিল্টার করে বাদ দেবে এবং নিচ থেকে ঘুরে দাঁড়ানো স্টক খুঁজবে)
    # বুলিশ টার্নঅ্যারাউন্ড: গত ১ সপ্তাহ মাইনাস বা ফ্ল্যাট ছিল, কিন্তু আজ ভলিউম নিয়ে পজিটিভ হয়েছে এবং ডে-হাইয়ের কাছে ক্লোজ হয়েছে
    turnaround_bull_score = round(
        (rvol_num * 5.0) + ((clv_pct - 50.0) * 0.25) + (r_1d * 2.5) + (2.0 if r_1w < 2.0 else -2.0), 2
    )
    # বেয়ারিশ টার্নঅ্যারাউন্ড: গত ১ সপ্তাহ পজিটিভ ছিল, কিন্তু আজ ভলিউম নিয়ে ব্রেকডাউন করেছে এবং ডে-লোর কাছে ক্লোজ হয়েছে
    turnaround_bear_score = round(
        (rvol_num * 5.0) + ((50.0 - clv_pct) * 0.25) + ((-r_1d) * 2.5) + (2.0 if r_1w > -2.0 else -2.0), 2
    )

    if r_1d >= 1.0 and r_1w <= 3.0 and rvol_num >= 1.25 and clv_pct >= 65:
        intraday_catalyst = f"🔄 নিচ থেকে রিভার্সাল (Turnaround Reversal | Vol {rvol_num}x)"
    elif r_1d >= 2.0 and rvol_num >= 1.4:
        intraday_catalyst = f"🔥 হেভি ভলিউম ব্রেকআউট ({rvol_num}x Vol)"
    elif r_1d <= -1.0 and r_1w >= -3.0 and rvol_num >= 1.25 and clv_pct <= 35:
        intraday_catalyst = f"📉 উপর থেকে রিভার্সাল সেল (Bearish Reversal | Vol {rvol_num}x)"
    else:
        intraday_catalyst = f"📊 নরমাল ইন্ট্রাডে রেঞ্জ (CLV: {clv_pct:.0f}% | Vol {rvol_num}x)"

    if above_50dma and r_sel > 2.0 and rvol_num >= 1.25:
        action_sig = "🔥 ভলিউম ব্রেকআউট (Vol Breakout)"
    elif dd_52w < -12 and r_1d > 0.5:
        action_sig = "🔄 নিচ থেকে ঘুরছে (Turnaround)"
    elif dd_52w < -25 or rsi_14 < 35:
        action_sig = "💎 ওভারসোল্ড / ভ্যালু (Deep Value)"
    elif above_50dma:
        action_sig = "🟢 পজিটিভ ট্রেন্ড (Positive)"
    else:
        action_sig = "⚠️ দুর্বল / ডাউন (Weak Trend)"

    return {
        "Ticker": t,
        "Stock": t.replace(".NS", ""),
        "Sector": s_name_label,
        "Signal (সিগন্যাল)": action_sig,
        "Intraday Catalyst": intraday_catalyst,
        "CMP (₹)": curr_p,
        "Day High": round(day_high, 2),
        "Day Low": round(day_low, 2),
        "Day Open": round(day_open, 2),
        "Day Range Pos %": clv_pct,
        "Buy Above (₹)": buy_above,
        "Sell Below (₹)": sell_below,
        "Bull SL (₹)": bull_sl,
        "Bull T1 (₹)": bull_t1,
        "Bull T2 (₹)": bull_t2,
        "Bear SL (₹)": bear_sl,
        "Bear T1 (₹)": bear_t1,
        "Bear T2 (₹)": bear_t2,
        "Turnaround_Bull_Score": turnaround_bull_score,
        "Turnaround_Bear_Score": turnaround_bear_score,
        "RSI (14)": rsi_14,
        "Volume Action": rvol_label,
        "RVOL_Num": rvol_num,
        "Meter Score": round(st_score, 1),
        "Prev Meter": round(st_prev, 1),
        **r_map,
        "From 52W High %": dd_52w,
        "52W High": round(high_52w, 2),
        "52W Low": round(low_52w, 2),
        "50 DMA Trend": "🟢 Above 50DMA" if above_50dma else "🔴 Below 50DMA",
        "200 DMA Trend": "🟢 Above 200DMA" if above_200dma else "🔴 Below 200DMA",
        "Above_50": above_50dma,
        "Is_Nifty50": t in NIFTY_50_TICKERS,
    }

for s_name, tickers in sectors.items():
    valid = [t for t in tickers if t in full_df.columns and len(full_df[t].dropna()) > 5]
    if not valid:
        continue

    st_rows = []
    for t in valid:
        row_dict = compute_stock_row(t, s_name)
        st_rows.append(row_dict)
        all_stocks_master[t] = row_dict

    st_df = pd.DataFrame(st_rows)
    sec_rets = {tf: round(float(st_df[f"{tf} %"].mean()), 2) for tf in ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"]}
    avg_dd_52w = round(float(st_df["From 52W High %"].mean()), 2)
    avg_rsi = round(float(st_df["RSI (14)"].mean()), 1)

    sel_ret = sec_rets[tf_option]
    alpha_sel = sel_ret - nifty_curr_val
    breadth_sel = float((st_df[ret_key] >= 0).mean()) * 100

    curr_meter = float(np.clip(50 + (alpha_sel * 2.2) + (sel_ret * 1.1) + ((breadth_sel - 50) * 0.25), 3, 98))
    prev_meter = float(np.clip(50 + ((sec_rets["3M"] - nifty_multi_ret["3M"]) * 1.2) + ((sec_rets["1Y"] - nifty_multi_ret["1Y"]) * 0.4), 3, 98))
    meter_diff = round(curr_meter - prev_meter, 1)

    turnaround_score = round((sec_rets["1W"] * 1.8 + sec_rets["1M"] * 1.2) - (sec_rets["3M"] * 0.6) + abs(min(0, avg_dd_52w)) * 0.3, 2)
    cooling_score = round((sec_rets["1Y"] * 0.4 + sec_rets["3M"] * 0.8) - (sec_rets["1W"] * 1.8 + sec_rets["1M"] * 1.2), 2)

    is_turnaround = (avg_dd_52w < -8.0 or sec_rets["3M"] < 0 or prev_meter < 48) and (sec_rets["1W"] > 0 or sec_rets["1M"] > 0 or sel_ret > 0)
    is_cooling = (sec_rets["1Y"] > 8.0 or sec_rets["3M"] > 4.0 or prev_meter >= 52) and (sec_rets["1W"] < 0 or sec_rets["1M"] < 0 or sel_ret < nifty_curr_val)
    is_strong_green = (sel_ret >= nifty_curr_val and sel_ret > 0) or curr_meter >= 58
    is_red_zone = sel_ret < 0 or curr_meter < 42
    is_yellow = (38 <= curr_meter <= 62) or (-3.0 <= sel_ret <= 4.0)

    if is_turnaround and meter_diff > 0:
        stage_label = "🔄 Red ➔ Green Turnaround"
        meter_status = "🔴 রেড জোন থেকে ঘুরে 🟢 গ্রিন জোনে উঠছে (Bullish Turnaround)"
    elif is_strong_green:
        stage_label = "🚀 Strong Green Leader"
        meter_status = "🟢 ফুল গ্রিন জোন — মার্কেটকে লিড দিচ্ছে (Strong Leader)"
    elif is_cooling and meter_diff < 0:
        stage_label = "⚠️ Green ➔ Red Cooling"
        meter_status = "🟢 গ্রিন থেকে কমে 🟡 নিচে নামছে (Cooling Off)"
    elif is_red_zone:
        stage_label = "🔴 Red Zone / Deep Value"
        meter_status = "🔴 রেড জোন — এখন ডাউন বা ভ্যালু জোনে আছে (Beaten Down)"
    else:
        stage_label = "🟡 Yellow Watchlist Zone"
        meter_status = "🟡 ইয়েলো জোন — ব্রেকআউটের অপেক্ষায় (Watchlist)"

    sector_master.append({
        "Sector": s_name,
        "Stage": stage_label,
        "Meter_Status": meter_status,
        "Curr_Meter": round(curr_meter, 1),
        "Prev_Meter": round(prev_meter, 1),
        "Meter_Diff": meter_diff,
        "Avg RSI": avg_rsi,
        "Turnaround_Score": turnaround_score,
        "Cooling_Score": cooling_score,
        "Is_Turnaround": is_turnaround,
        "Is_Cooling": is_cooling,
        "Is_Strong_Green": is_strong_green,
        "Is_Yellow": is_yellow,
        "Is_Red_Zone": is_red_zone,
        "valid_tickers": valid,
        "stocks_df": st_df,
        **{f"{k} %": v for k, v in sec_rets.items()},
    })

nifty50_rows = []
for t in NIFTY_50_TICKERS:
    if t in all_stocks_master:
        nifty50_rows.append(all_stocks_master[t])
    elif t in full_df.columns and len(full_df[t].dropna()) > 5:
        r_d = compute_stock_row(t, ticker_to_sector.get(t, "Nifty 50 Core"))
        nifty50_rows.append(r_d)
nifty50_df_global = pd.DataFrame(nifty50_rows)
all_st_df_global = pd.DataFrame(list(all_stocks_master.values()))

# ==============================================================================
# ৯. ইনস্ট্যান্ট স্টক সার্চ প্যানেল
# ==============================================================================
if not instant_stock_search.startswith("শেয়ার"):
    st_sym_lookup = instant_stock_search + ".NS"
    if st_sym_lookup in all_stocks_master:
        st_obj = all_stocks_master[st_sym_lookup]
        stk_nm_clean = st_obj["Stock"]
        st.markdown('<div class="focus-drawer">', unsafe_allow_html=True)
        sh_c1, sh_c2 = st.columns([4.5, 1.5])
        with sh_c1:
            st.markdown(
                f"### ⚡ কুইক স্টক প্রোফাইল: **{stk_nm_clean}** ({st_obj['Sector']}) — `{st_obj['Signal (সিগন্যাল)']}`"
            )
            st.caption(f"🎯 ইন্ট্রাডে ক্যাটালিস্ট: **{st_obj['Intraday Catalyst']}**")
        with sh_c2:
            st.markdown(
                f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{stk_nm_clean}" target="_blank">📈 TradingView</a> '
                f'<a class="action-btn" href="https://www.screener.in/company/{stk_nm_clean}/" target="_blank">📊 Screener</a> '
                f'<a class="action-btn" href="https://www.google.com/search?q={stk_nm_clean}+share+news+india&tbm=nws" target="_blank">📰 News</a>',
                unsafe_allow_html=True,
            )
        qm1, qm2, qm3, qm4, qm5, qm6 = st.columns(6)
        qm1.metric("বর্তমান দাম (CMP)", f"₹{st_obj['CMP (₹)']}")
        qm2.metric("1D / ইন্ট্রাডে মুভ", f"{st_obj['1D %']:+.2f}%", f"Day Pos: {st_obj['Day Range Pos %']:.0f}%")
        qm3.metric("Buy Above (বুলিশ)", f"₹{st_obj['Buy Above (₹)']}", f"T1: ₹{st_obj['Bull T1 (₹)']}")
        qm4.metric("Sell Below (বেয়ারিশ)", f"₹{st_obj['Sell Below (₹)']}", f"T1: ₹{st_obj['Bear T1 (₹)']}")
        qm5.metric("RSI (14)", f"{st_obj['RSI (14)']}")
        qm6.metric("Volume Action", st_obj["Volume Action"])
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# ১০. নতুন ইন্ট্রাডে ফোকাস বার (যাতে অলরেডি ৪-৫ দিন বেড়ে যাওয়া স্টক বাদ দিয়ে নিচ থেকে ঘুরে দাঁড়ানো স্টক আসে)
# ==============================================================================
# বুলিশ টার্নঅ্যারাউন্ড ফিল্টার (যে স্টকগুলো গত ৩-৪ দিন অতিরিক্ত বা ধারাবাহিক বাড়েনি, কিন্তু আজ ভলিউম নিয়ে নিচ থেকে ঘুরছে)
bull_turnaround_pool = all_st_df_global[
    (all_st_df_global["1D %"] > 0.2) & (all_st_df_global["1W %"] < 6.0) & (all_st_df_global["Day Range Pos %"] >= 65)
].sort_values(by="Turnaround_Bull_Score", ascending=False)
if len(bull_turnaround_pool) < 6:
    bull_turnaround_pool = all_st_df_global.sort_values(by="Turnaround_Bull_Score", ascending=False)
top_6_bull_intraday = bull_turnaround_pool.head(6).reset_index(drop=True)

# বেয়ারিশ টার্নঅ্যারাউন্ড ফিল্টার
bear_turnaround_pool = all_st_df_global[
    (all_st_df_global["1D %"] < -0.2) & (all_st_df_global["1W %"] > -6.0) & (all_st_df_global["Day Range Pos %"] <= 35)
].sort_values(by="Turnaround_Bear_Score", ascending=False)
if len(bear_turnaround_pool) < 6:
    bear_turnaround_pool = all_st_df_global.sort_values(by="Turnaround_Bear_Score", ascending=False)
top_6_bear_intraday = bear_turnaround_pool.head(6).reset_index(drop=True)

ib_col1, ib_col2 = st.columns(2)
with ib_col1:
    bull_pills_html = ""
    for _, brow in top_6_bull_intraday.iterrows():
        b_stk = brow["Stock"]
        b_ret = brow["1D %"]
        b_rvol = brow["RVOL_Num"]
        b_lvl = brow["Buy Above (₹)"]
        bull_pills_html += (
            f'<a class="focus-pill-bull" href="https://in.tradingview.com/chart/?symbol=NSE:{b_stk}" target="_blank" '
            f'title="Buy Above: ₹{b_lvl} | Vol: {b_rvol}x | ক্লিক করে চার্ট খুলুন">'
            f'🟢 {b_stk} ({b_ret:+.1f}% | {b_rvol}x Vol)</a>'
        )
    st.markdown(
        f"""
        <div class="intraday-bull-box">
            <div style="font-size:13.5px; font-weight:800; color:#00e676; margin-bottom:4px;">
                🔄 ইন্ট্রাডে বুলিশ রিভার্সাল ফোকাস (Bottom Turnaround — অতিরিক্ত না বেড়ে নিচ থেকে ঘুরে দাঁড়ানো স্টক)
            </div>
            <div>{bull_pills_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with ib_col2:
    bear_pills_html = ""
    for _, srow in top_6_bear_intraday.iterrows():
        s_stk = srow["Stock"]
        s_ret = srow["1D %"]
        s_rvol = srow["RVOL_Num"]
        s_lvl = srow["Sell Below (₹)"]
        bear_pills_html += (
            f'<a class="focus-pill-bear" href="https://in.tradingview.com/chart/?symbol=NSE:{s_stk}" target="_blank" '
            f'title="Sell Below: ₹{s_lvl} | Vol: {s_rvol}x | ক্লিক করে চার্ট খুলুন">'
            f'🔴 {s_stk} ({s_ret:+.1f}% | {s_rvol}x Vol)</a>'
        )
    st.markdown(
        f"""
        <div class="intraday-bear-box">
            <div style="font-size:13.5px; font-weight:800; color:#ff5252; margin-bottom:4px;">
                📉 ইন্ট্রাডে বেয়ারিশ রিভার্সাল ফোকাস (Top Breakdown — ওপর থেকে নিচে নামার প্রস্তুতি নেওয়া স্টক)
            </div>
            <div>{bear_pills_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# ১১. ১০০% ক্লিকেবল স্ক্রলিং সেক্টর বার (ব্যাকস্ল্যাশ মুক্ত ও সম্পূর্ণ নিরাপদ)
# ==============================================================================
pos_secs = sorted([s for s in sector_master if s[ret_key] >= 0], key=lambda x: x[ret_key], reverse=True)
neg_secs = sorted([s for s in sector_master if s[ret_key] < 0], key=lambda x: x[ret_key], reverse=False)

mixed_ticker_secs = []
max_len = max(len(pos_secs), len(neg_secs))
for i in range(max_len):
    if i < len(pos_secs):
        mixed_ticker_secs.append(pos_secs[i])
    if i < len(neg_secs):
        mixed_ticker_secs.append(neg_secs[i])

ticker_items = []
for s in mixed_ticker_secs:
    r_val = s[ret_key]
    sec_name_clean = s["Sector"]
    sec_encoded = quote(sec_name_clean)
    if r_val >= 0:
        chip_html = (
            f'<a class="ticker-chip-up" href="?focus_sec={sec_encoded}" target="_self" '
            f'title="ক্লিক করে {sec_name_clean}-এর সব শেয়ার ও চার্ট দেখুন">'
            f'🟢 {sec_name_clean}: ▲ {r_val:+.2f}% 🔍</a>'
        )
        ticker_items.append(chip_html)
    else:
        chip_html = (
            f'<a class="ticker-chip-down" href="?focus_sec={sec_encoded}" target="_self" '
            f'title="ক্লিক করে {sec_name_clean}-এর সব শেয়ার ও চার্ট দেখুন">'
            f'🔴 {sec_name_clean}: ▼ {r_val:+.2f}% 🔍</a>'
        )
        ticker_items.append(chip_html)

st.caption("💡 **ক্লিকেবল সেক্টর বার:** নিচের চলমান বারের ওপর মাউস রাখলে সেটি থেমে যাবে এবং **যেকোনো সেক্টরের ওপর ক্লিক করলেই** সাথে সাথে সেই সেক্টরের সব শেয়ার ও চার্ট খুলে যাবে:")
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-move">{"".join(ticker_items * 2)}</div></div>',
    unsafe_allow_html=True,
)

# টিকার বারে ক্লিক করলে তার ডিটেইলস প্যানেল
clicked_sec_raw = None
try:
    q_val = st.query_params.get("focus_sec", None)
    if isinstance(q_val, list):
        clicked_sec_raw = unquote(q_val[0]) if q_val else None
    elif q_val:
        clicked_sec_raw = unquote(q_val)
except Exception:
    clicked_sec_raw = None

if clicked_sec_raw:
    clicked_sec_obj = next((s for s in sector_master if s["Sector"] == clicked_sec_raw), None)
    if clicked_sec_obj is not None:
        st.markdown('<div class="focus-drawer">', unsafe_allow_html=True)
        dr_c1, dr_c2 = st.columns([4.8, 1.2])
        with dr_c1:
            s_r_now = clicked_sec_obj[ret_key]
            st.markdown(
                f"### 🎯 নির্বাচিত সেক্টর ডিপ-ডাইভ: **{clicked_sec_obj['Sector']}** "
                f"({tf_option}: `{s_r_now:+.2f}%` | মিটার স্কোর: `{clicked_sec_obj['Curr_Meter']}/100` | গড় RSI: `{clicked_sec_obj['Avg RSI']}`)"
            )
            st.markdown(f"**রোটেশন স্ট্যাটাস:** {clicked_sec_obj['Meter_Status']}")
        with dr_c2:
            if st.button("✖ এই সেক্টর ভিউ বন্ধ করুন", key="btn_close_ticker_sec"):
                try:
                    st.query_params.clear()
                except Exception:
                    pass
                st.rerun()

        c_st_df = clicked_sec_obj["stocks_df"].sort_values(by=ret_key, ascending=False).reset_index(drop=True)
        c_up = int((c_st_df[ret_key] >= 0).sum())
        c_dn = len(c_st_df) - c_up
        st.markdown(
            f"📊 **সেক্টর ব্রেডথ ({tf_option}):** মোট **{len(c_st_df)}টি শেয়ারের** মধ্যে "
            f"<span style='color:#00e676; font-weight:800;'>🟢 {c_up}টি শেয়ার উপরে মুভ করছে</span> এবং "
            f"<span style='color:#ff5252; font-weight:800;'>🔴 {c_dn}টি শেয়ার ডাউন আছে</span>।",
            unsafe_allow_html=True,
        )

        sub_tk = full_df.tail(tf_days_map[tf_option]).copy()
        norm_tk = pd.DataFrame(
            {c: (sub_tk[c] / sub_tk[c].dropna().iloc[0]) * 100 for c in clicked_sec_obj["valid_tickers"] if len(sub_tk[c].dropna()) > 0},
            index=sub_tk.index,
        )

        tk_col1, tk_col2 = st.columns([1, 2.1])
        with tk_col1:
            fig_tk_g = make_analog_gauge(
                clicked_sec_obj["Curr_Meter"],
                clicked_sec_obj["Prev_Meter"],
                f"Prev: {clicked_sec_obj['Prev_Meter']} ➔ Now: {clicked_sec_obj['Curr_Meter']}",
                height_px=270,
            )
            st.plotly_chart(fig_tk_g, use_container_width=True, theme=None, key="ticker_clicked_gauge")
        with tk_col2:
            fig_tk_lines = go.Figure()
            for t_c in norm_tk.columns:
                sn = t_c.replace(".NS", "")
                sr = all_stocks_master[t_c][ret_key]
                fig_tk_lines.add_trace(
                    go.Scatter(x=norm_tk.index, y=norm_tk[t_c], name=f"{sn} ({sr:+.1f}%)", mode="lines", line=dict(width=2.3))
                )
            fig_tk_lines.update_layout(
                title=f"{clicked_sec_obj['Sector']} — কোন শেয়ারগুলো মুভ করছে তার লাইভ তুলনামূলক চার্ট ({tf_option})",
                paper_bgcolor=chart_bg,
                plot_bgcolor=chart_bg,
                font=dict(color=text_color, size=11),
                height=270,
                hovermode="x unified",
                margin=dict(t=35, b=12, l=10, r=10),
                xaxis=dict(gridcolor=grid_col),
                yaxis=dict(gridcolor=grid_col, title="Base 100"),
            )
            st.plotly_chart(fig_tk_lines, use_container_width=True, theme=None, key="ticker_clicked_chart")

        tk_disp_cols = [
            "Stock", "Signal (সিগন্যাল)", "CMP (₹)", "RSI (14)", "Volume Action",
            "Meter Score", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %", "50 DMA Trend"
        ]
        st.dataframe(
            style_colored_table(c_st_df[tk_disp_cols], ret_key),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("##### 🔗 সরাসরি চার্ট (TradingView), ফান্ডামেন্টাল (Screener) ও লাইভ নিউজ খুলুন:")
        tk_btns = ""
        for _, r in c_st_df.iterrows():
            stk_c = r["Stock"]
            tk_btns += (
                f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{stk_c}" target="_blank">📈 {stk_c} (TV)</a>'
                f'<a class="action-btn" href="https://www.screener.in/company/{stk_c}/" target="_blank">📊 Screener</a>'
                f'<a class="action-btn" href="https://www.google.com/search?q={stk_c}+share+news+india&tbm=nws" target="_blank">📰 News</a> &nbsp;'
            )
        st.markdown(tk_btns, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# ১২. ক্লিকেবল ৪টি মেইন KPI কার্ড
# ==============================================================================
adv_count = int((all_st_df_global[ret_key] >= 0).sum())
dec_count = len(all_st_df_global) - adv_count
pct_above_50 = round(float(all_st_df_global["Above_50"].mean()) * 100, 1)
best_sec_now = max(sector_master, key=lambda x: x[ret_key])
worst_sec_now = min(sector_master, key=lambda x: x[ret_key])

if "active_kpi_panel" not in st.session_state:
    st.session_state["active_kpi_panel"] = None

def toggle_kpi(panel_name):
    if st.session_state["active_kpi_panel"] == panel_name:
        st.session_state["active_kpi_panel"] = None
    else:
        st.session_state["active_kpi_panel"] = panel_name

k1, k2, k3, k4 = st.columns(4)

with k1:
    sub_cls = "kpi-sub-pos" if nifty_multi_ret["1W"] >= 0 else "kpi-sub-neg"
    main_col = "#00e676" if nifty_curr_val >= 0 else "#ff5252"
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Nifty 50 Benchmark ({tf_option})</div>
            <div class="kpi-main" style="color:{main_col} !important;">{nifty_curr_val:+.2f}%</div>
            <span class="{sub_cls}">1W: {nifty_multi_ret['1W']:+.2f}% | 1Y: {nifty_multi_ret['1Y']:+.1f}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("📊 নিফটি ৫০ মুভার্স লিস্ট দেখুন ▾", key="btn_kpi_nifty"):
        toggle_kpi("nifty")

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">মার্কেট ব্রেডথ ({tf_option} Adv vs Dec)</div>
            <div class="kpi-main"><span style="color:#00e676 !important;">🟢 {adv_count} উপরে</span> | <span style="color:#ff5252 !important;">🔴 {dec_count} নিচে</span></div>
            <span class="kpi-sub-pos">{pct_above_50}% শেয়ার 50-DMA এর উপরে</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("📋 বাড়তে থাকা ও ডাউন শেয়ার দেখুন ▾", key="btn_kpi_breadth"):
        toggle_kpi("breadth")

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">টপ লিডার সেক্টর ({tf_option})</div>
            <div class="kpi-main" style="color:#00e676 !important;">👑 {best_sec_now['Sector']}</div>
            <span class="kpi-sub-pos">▲ {best_sec_now[ret_key]:+.2f}% (Meter: {best_sec_now['Curr_Meter']:.0f})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"🔍 {best_sec_now['Sector']}-এর শেয়ার দেখুন ▾", key="btn_kpi_leader"):
        toggle_kpi("leader")

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">সবচেয়ে ডাউন সেক্টর ({tf_option})</div>
            <div class="kpi-main" style="color:#ff5252 !important;">📉 {worst_sec_now['Sector']}</div>
            <span class="kpi-sub-neg">▼ {worst_sec_now[ret_key]:+.2f}% (Value Zone)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"🔍 {worst_sec_now['Sector']}-এর শেয়ার দেখুন ▾", key="btn_kpi_laggard"):
        toggle_kpi("laggard")

active_p = st.session_state["active_kpi_panel"]
if active_p is not None:
    st.markdown('<div class="focus-drawer">', unsafe_allow_html=True)
    top_bar_c1, top_bar_c2 = st.columns([5, 1])
    with top_bar_c2:
        if st.button("✖ লিস্ট বন্ধ করুন", key="close_kpi_panel"):
            st.session_state["active_kpi_panel"] = None
            st.rerun()

    disp_cols_kpi = [
        "Stock", "Sector", "Signal (সিগন্যাল)", "CMP (₹)", "RSI (14)", "Volume Action",
        "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %"
    ]

    if active_p == "nifty":
        n50_up = int((nifty50_df_global[ret_key] >= 0).sum())
        n50_dn = len(nifty50_df_global) - n50_up
        with top_bar_c1:
            st.markdown(
                f"### 📊 আসল Nifty 50 শেয়ার মুভার্স লিস্ট ({tf_option}: {nifty_curr_val:+.2f}% | 🟢 {n50_up}টি প্লাসে, 🔴 {n50_dn}টি মাইনাসে)"
            )
        nc1, nc2 = st.columns(2)
        with nc1:
            st.markdown(f"#### 🟢 নিফটি ৫০ টপ গেইনার্স ({tf_option})")
            top_pull = nifty50_df_global.sort_values(by=ret_key, ascending=False).head(25).reset_index(drop=True)
            st.dataframe(style_colored_table(top_pull[disp_cols_kpi], ret_key), use_container_width=True, height=380, hide_index=True)
        with nc2:
            st.markdown(f"#### 🔴 নিফটি ৫০ টপ লুজার্স ({tf_option})")
            top_drag = nifty50_df_global.sort_values(by=ret_key, ascending=True).head(25).reset_index(drop=True)
            st.dataframe(style_colored_table(top_drag[disp_cols_kpi], ret_key), use_container_width=True, height=380, hide_index=True)

    elif active_p == "breadth":
        with top_bar_c1:
            st.markdown(f"### 📋 মার্কেট ব্রেডথ রিপোর্ট: 🟢 {adv_count}টি শেয়ার উপরে | 🔴 {dec_count}টি শেয়ার নিচে ({tf_option})")
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown(f"#### 🟢 বাড়তে থাকা শেয়ারসমূহ ({adv_count}টি)")
            adv_df = all_st_df_global[all_st_df_global[ret_key] >= 0].sort_values(by=ret_key, ascending=False).reset_index(drop=True)
            st.dataframe(style_colored_table(adv_df[disp_cols_kpi], ret_key), use_container_width=True, height=380, hide_index=True)
        with bc2:
            st.markdown(f"#### 🔴 ডাউন বা মাইনাসে থাকা শেয়ারসমূহ ({dec_count}টি)")
            dec_df = all_st_df_global[all_st_df_global[ret_key] < 0].sort_values(by=ret_key, ascending=True).reset_index(drop=True)
            st.dataframe(style_colored_table(dec_df[disp_cols_kpi], ret_key), use_container_width=True, height=380, hide_index=True)

    elif active_p in ["leader", "laggard"]:
        target_sec = best_sec_now if active_p == "leader" else worst_sec_now
        sec_title_prefix = "👑 টপ লিডার সেক্টর" if active_p == "leader" else "📉 সবচেয়ে ডাউন সেক্টর"
        with top_bar_c1:
            st.markdown(
                f"### {sec_title_prefix}: **{target_sec['Sector']}** ({tf_option} রিটার্ন: {target_sec[ret_key]:+.2f}%)"
            )

        t_df = target_sec["stocks_df"].sort_values(by=ret_key, ascending=False).reset_index(drop=True)
        lc1, lc2 = st.columns([1.25, 1.75])
        with lc1:
            sub_k = full_df.tail(tf_days_map[tf_option]).copy()
            norm_k = pd.DataFrame(
                {c: (sub_k[c] / sub_k[c].dropna().iloc[0]) * 100 for c in target_sec["valid_tickers"] if len(sub_k[c].dropna()) > 0},
                index=sub_k.index,
            )
            fig_k = go.Figure()
            for t_c in norm_k.columns:
                sn = t_c.replace(".NS", "")
                sr = all_stocks_master[t_c][ret_key]
                fig_k.add_trace(go.Scatter(x=norm_k.index, y=norm_k[t_c], name=f"{sn} ({sr:+.1f}%)", mode="lines", line=dict(width=2.2)))
            fig_k.update_layout(
                title=f"{target_sec['Sector']} - শেয়ারগুলোর তুলনামূলক চার্ট ({tf_option})",
                paper_bgcolor=chart_bg,
                plot_bgcolor=chart_bg,
                font=dict(color=text_color, size=11),
                height=310,
                hovermode="x unified",
                margin=dict(t=35, b=15, l=10, r=10),
                xaxis=dict(gridcolor=grid_col),
                yaxis=dict(gridcolor=grid_col, title="Base 100"),
            )
            st.plotly_chart(fig_k, use_container_width=True, theme=None, key=f"kpi_chart_{active_p}_{tf_option}")
        with lc2:
            cols_sec_show = ["Stock", "Signal (সিগন্যাল)", "CMP (₹)", "RSI (14)", "Volume Action", "1D %", "1W %", "1M %", "1Y %", "From 52W High %"]
            st.dataframe(style_colored_table(t_df[cols_sec_show], ret_key), use_container_width=True, height=310, hide_index=True)
            btn_links = ""
            for _, r in t_df.iterrows():
                stk_c = r["Stock"]
                btn_links += (
                    f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{stk_c}" target="_blank">📈 {stk_c} (TV)</a>'
                    f'<a class="action-btn" href="https://www.screener.in/company/{stk_c}/" target="_blank">📊 Screener</a>'
                    f'<a class="action-btn" href="https://www.google.com/search?q={stk_c}+share+news+india&tbm=nws" target="_blank">📰 News</a> &nbsp;'
                )
            st.markdown(btn_links, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# ১৩. গ্লোবাল ফিল্টারিং ও সর্টিং লজিক
# ==============================================================================
if not quick_sec_jump.startswith("সবগুলো"):
    filtered_sectors = [s for s in sector_master if s["Sector"] == quick_sec_jump]
else:
    if "Strong Green" in zone_filter_choice:
        filtered_sectors = [s for s in sector_master if s["Is_Strong_Green"]]
    elif "Red ➔ Green" in zone_filter_choice:
        filtered_sectors = [s for s in sector_master if s["Is_Turnaround"]]
        if not filtered_sectors:
            filtered_sectors = sorted(sector_master, key=lambda x: x["Turnaround_Score"], reverse=True)[:10]
    elif "Yellow" in zone_filter_choice:
        filtered_sectors = [s for s in sector_master if s["Is_Yellow"]]
    elif "Green ➔ Red" in zone_filter_choice:
        filtered_sectors = [s for s in sector_master if s["Is_Cooling"]]
        if not filtered_sectors:
            filtered_sectors = sorted(sector_master, key=lambda x: x["Cooling_Score"], reverse=True)[:10]
    elif "Red Zone" in zone_filter_choice:
        filtered_sectors = [s for s in sector_master if s["Is_Red_Zone"]]
    else:
        filtered_sectors = list(sector_master)

if "Top Gainers" in sort_option:
    filtered_sectors = sorted(filtered_sectors, key=lambda x: x[ret_key], reverse=True)
elif "Top Losers" in sort_option:
    filtered_sectors = sorted(filtered_sectors, key=lambda x: x[ret_key], reverse=False)
elif "Red ➔ Green" in sort_option:
    filtered_sectors = sorted(filtered_sectors, key=lambda x: (x["Is_Turnaround"], x["Turnaround_Score"], x["Meter_Diff"]), reverse=True)
elif "Green ➔ Red" in sort_option:
    filtered_sectors = sorted(filtered_sectors, key=lambda x: (x["Is_Cooling"], x["Cooling_Score"], -x["Meter_Diff"]), reverse=True)
elif "Meter: High to Low" in sort_option:
    filtered_sectors = sorted(filtered_sectors, key=lambda x: x["Curr_Meter"], reverse=True)
elif "Meter: Low to High" in sort_option:
    filtered_sectors = sorted(filtered_sectors, key=lambda x: x["Curr_Meter"], reverse=False)

# ==============================================================================
# ১৪. ৫টি প্রো ট্যাব
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧭 ১. সেক্টর চার্ট, মিটার ও শেয়ার তালিকা",
    "⚡ ২. ইন্ট্রাডে ও সুইং রাডার (Next-Day Bullish/Bearish)",
    "🔥 ৩. লং ও শর্ট-টার্ম স্ক্যানার (Volume, RSI & Value)",
    "📊 ৪. সব সেক্টরের তুলনামূলক টেবিল",
    "📈 ৫. শেয়ারের নিজস্ব চার্ট ও মুভিং অ্যাভারেজ",
])

# ==============================================================================
# TAB 1: সেক্টর গ্রিড + অ্যানালগ মিটার + সব শেয়ারের চার্ট ও সবুজ/লাল টেবিল
# ==============================================================================
with tab1:
    days_sel = tf_days_map[tf_option]
    nifty_curr_ret = nifty_multi_ret[tf_option]

    sub_df = full_df.tail(days_sel).copy()
    norm_sub = pd.DataFrame(index=sub_df.index)
    for col in sub_df.columns:
        s = sub_df[col].dropna()
        if len(s) > 0 and s.iloc[0] != 0:
            norm_sub[col] = (sub_df[col] / s.iloc[0]) * 100

    nifty_norm_line = norm_sub[benchmark] if benchmark in norm_sub.columns else None

    if len(filtered_sectors) == 1:
        cols = [st.container()]
    else:
        cols = st.columns(2)

    for idx, sec in enumerate(filtered_sectors):
        target_col = cols[0] if len(filtered_sectors) == 1 else cols[idx % 2]
        with target_col:
            s_name = sec["Sector"]
            s_ret = sec[ret_key]
            alpha_val = round(s_ret - nifty_curr_ret, 2)
            outperform = s_ret >= nifty_curr_ret
            st_df = sec["stocks_df"].sort_values(by=ret_key, ascending=False).reset_index(drop=True)

            up_cnt = int((st_df[ret_key] >= 0).sum())
            dn_cnt = len(st_df) - up_cnt
            badge_cls = "badge-green" if s_ret >= 0 else "badge-red"
            arrow_sym = "▲" if s_ret >= 0 else "▼"

            st.markdown(
                f"""
                <div class="pro-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:19px; font-weight:800; color:{text_color};">#{idx+1} {s_name}</span>
                        <span class="{badge_cls}">{arrow_sym} {s_ret:+.2f}% ({tf_option})</span>
                    </div>
                    <div class="stage-banner">{sec['Meter_Status']}</div>
                    <div style="font-size:13px; color:{sub_text}; margin-top:4px;">
                        <b>Alpha vs Nifty:</b> {alpha_val:+.2f}% &nbsp;|&nbsp;
                        <span style="color:#00e676; font-weight:700;">🟢 উপরে: {up_cnt}টি</span> &nbsp;|&nbsp;
                        <span style="color:#ff5252; font-weight:700;">🔴 নিচে: {dn_cnt}টি</span> &nbsp;|&nbsp;
                        <b>Avg RSI:</b> {sec['Avg RSI']} &nbsp;|&nbsp;
                        🧭 <b>Meter:</b> {sec['Curr_Meter']}/100
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            valid_cols = [t for t in sec["valid_tickers"] if t in norm_sub.columns]
            sec_line = norm_sub[valid_cols].mean(axis=1)
            unique_key_suffix = f"{s_name}_{tf_option}_{idx}"

            if show_card_meter:
                ch_col, mt_col = st.columns([1.65, 1])
            else:
                ch_col = st.container()

            with ch_col:
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=norm_sub.index,
                        y=sec_line,
                        name=f"{s_name} ({s_ret:+.1f}%)",
                        line=dict(color="#00e676" if outperform else "#ff5252", width=2.8),
                    )
                )
                if nifty_norm_line is not None:
                    fig.add_trace(
                        go.Scatter(
                            x=norm_sub.index,
                            y=nifty_norm_line,
                            name=f"Nifty 50 ({nifty_curr_ret:+.1f}%)",
                            line=dict(color=nifty_col_line, width=1.8, dash="dot"),
                        )
                    )
                fig.update_layout(
                    paper_bgcolor=chart_bg,
                    plot_bgcolor=chart_bg,
                    font=dict(color=text_color),
                    height=225,
                    hovermode="x unified",
                    margin=dict(t=22, b=12, l=10, r=10),
                    legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11, color=text_color)),
                    xaxis=dict(gridcolor=grid_col),
                    yaxis=dict(gridcolor=grid_col, title="Base 100"),
                )
                st.plotly_chart(fig, use_container_width=True, theme=None, key=f"sec_ch_{unique_key_suffix}")

            if show_card_meter:
                with mt_col:
                    fig_gauge = make_analog_gauge(
                        sec["Curr_Meter"],
                        sec["Prev_Meter"],
                        "Rotation Meter",
                        height_px=225,
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True, theme=None, key=f"sec_g_{unique_key_suffix}")

            top_st = st_df.iloc[0]
            bot_st = st_df.iloc[-1]
            st.markdown(
                f"🟢 **টপ গেইনার:** `{top_st['Stock']} ({top_st[ret_key]:+.1f}%)` &nbsp;|&nbsp; "
                f"🔴 **সবচেয়ে ডাউন:** `{bot_st['Stock']} ({bot_st[ret_key]:+.1f}%)`"
            )

            is_expanded_default = len(filtered_sectors) == 1
            with st.expander(
                f"🔍 {s_name} ওপেন করুন — সব শেয়ারের সিগন্যাল, RSI, ভলিউম ও চার্ট ({len(st_df)}টি শেয়ার)",
                expanded=is_expanded_default,
            ):
                ex_c1, ex_c2 = st.columns([1, 2])
                with ex_c1:
                    big_gauge = make_analog_gauge(
                        sec["Curr_Meter"],
                        sec["Prev_Meter"],
                        f"Prev: {sec['Prev_Meter']} ➔ Now: {sec['Curr_Meter']}",
                        height_px=250,
                    )
                    st.plotly_chart(big_gauge, use_container_width=True, theme=None, key=f"big_g_{unique_key_suffix}")

                with ex_c2:
                    fig_st = go.Figure()
                    for t in valid_cols:
                        st_name = t.replace(".NS", "")
                        st_r = all_stocks_master[t][ret_key]
                        fig_st.add_trace(
                            go.Scatter(
                                x=norm_sub.index,
                                y=norm_sub[t],
                                name=f"{st_name} ({st_r:+.1f}%)",
                                mode="lines",
                                line=dict(width=2),
                            )
                        )
                    fig_st.update_layout(
                        title=f"{s_name} - কোন শেয়ার উপরে ও কোন শেয়ার নিচে ({tf_option})",
                        paper_bgcolor=chart_bg,
                        plot_bgcolor=chart_bg,
                        font=dict(color=text_color, size=11),
                        height=250,
                        hovermode="x unified",
                        margin=dict(t=35, b=12, l=10, r=10),
                        xaxis=dict(gridcolor=grid_col),
                        yaxis=dict(gridcolor=grid_col, title="Base 100"),
                    )
                    st.plotly_chart(fig_st, use_container_width=True, theme=None, key=f"st_cmp_{unique_key_suffix}")

                disp_cols = [
                    "Stock", "Signal (সিগন্যাল)", "CMP (₹)", "RSI (14)", "Volume Action",
                    "Meter Score", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %"
                ]
                st.dataframe(
                    style_colored_table(st_df[disp_cols], ret_key),
                    use_container_width=True,
                    hide_index=True,
                )

                st.markdown("##### 🔗 এক ক্লিকে চার্ট (TradingView), ফান্ডামেন্টাল (Screener) ও নিউজ খুলুন:")
                btn_html = ""
                for _, r in st_df.iterrows():
                    stk_c = r["Stock"]
                    btn_html += (
                        f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{stk_c}" target="_blank">📈 {stk_c} (TV)</a>'
                        f'<a class="action-btn" href="https://www.screener.in/company/{stk_c}/" target="_blank">📊 Screener</a>'
                        f'<a class="action-btn" href="https://www.google.com/search?q={stk_c}+share+news+india&tbm=nws" target="_blank">📰 News</a> &nbsp;'
                    )
                st.markdown(btn_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: ইন্ট্রাডে ও সুইং রাডার (Next-Day Bullish/Bearish Action Plan + News)
# ==============================================================================
with tab2:
    st.subheader("⚡ আগামীকালের ইন্ট্রাডে ও সুইং ট্রেডিং ফোকাস রাডার (Volume + Price Action + News)")
    st.markdown(
        "**কীভাবে ব্যবহার করবেন:**\n"
        "- 🟢 **মার্কেট যদি বুলিশ (উপরে) থাকে:** বামপাশের **বুলিশ ফোকাস তালিকা** থেকে যে শেয়ারগুলো আজকের দিনের হাই (`Buy Above`)-এর ওপরে ট্রেড করবে, সেগুলোতে Buy/Long ইন্ট্রাডে বা সুইং ট্রেড নেওয়া যাবে।\n"
        "- 🔴 **মার্কেট যদি বেয়ারিশ (নিচে) থাকে:** ডানপাশের **বেয়ারিশ ফোকাস তালিকা** থেকে যে শেয়ারগুলো আজকের দিনের লো (`Sell Below`)-এর নিচে নামবে, সেগুলোতে Short/Sell ইন্ট্রাডে ট্রেড নেওয়া যাবে।"
    )

    in_c1, in_c2 = st.columns(2)

    with in_c1:
        st.markdown("#### 🚀 ১. বুলিশ ইন্ট্রাডে ও সুইং ফোকাস (Top 10 Bullish Setups)")
        st.caption("নিচ থেকে ঘুরে দাঁড়ানো (Turnaround Reversal) + হেভি ভলিউম স্টক:")
        top_10_bull = top_6_bull_intraday.head(10).reset_index(drop=True).copy()
        top_10_bull_disp = top_10_bull[[
            "Stock", "Sector", "CMP (₹)", "1D %", "Volume Action", "Day Range Pos %",
            "Buy Above (₹)", "Bull SL (₹)", "Bull T1 (₹)", "Bull T2 (₹)", "Intraday Catalyst"
        ]].rename(columns={
            "Bull SL (₹)": "Stop Loss (₹)",
            "Bull T1 (₹)": "Target 1 (₹)",
            "Bull T2 (₹)": "Target 2 (₹)",
        })
        st.dataframe(
            style_colored_table(top_10_bull_disp, "1D %"),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("##### 🔗 বুলিশ ফোকাস শেয়ারগুলোর লাইভ চার্ট ও ব্রেকিং নিউজ চেক করুন:")
        bull_links_str = ""
        for _, r in top_10_bull.head(6).iterrows():
            st_c = r["Stock"]
            bull_links_str += (
                f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{st_c}" target="_blank">📈 {st_c} Chart</a>'
                f'<a class="action-btn" href="https://www.google.com/search?q={st_c}+share+news+india&tbm=nws" target="_blank">📰 {st_c} News</a> &nbsp;'
            )
        st.markdown(bull_links_str, unsafe_allow_html=True)

    with in_c2:
        st.markdown("#### 📉 ২. বেয়ারিশ ইন্ট্রাডে ফোকাস (Top 10 Bearish Breakdown Setups)")
        st.caption("ওপর থেকে নিচে নামার প্রস্তুতি নেওয়া (Top Reversal) দুর্বল শেয়ার:")
        top_10_bear = top_6_bear_intraday.head(10).reset_index(drop=True).copy()
        top_10_bear_disp = top_10_bear[[
            "Stock", "Sector", "CMP (₹)", "1D %", "Volume Action", "Day Range Pos %",
            "Sell Below (₹)", "Bear SL (₹)", "Bear T1 (₹)", "Bear T2 (₹)", "Intraday Catalyst"
        ]].rename(columns={
            "Bear SL (₹)": "Stop Loss (₹)",
            "Bear T1 (₹)": "Target 1 (₹)",
            "Bear T2 (₹)": "Target 2 (₹)",
        })
        st.dataframe(
            style_colored_table(top_10_bear_disp, "1D %"),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("##### 🔗 বেয়ারিশ ফোকাস শেয়ারগুলোর লাইভ চার্ট ও ব্রেকিং নিউজ চেক করুন:")
        bear_links_str = ""
        for _, r in top_10_bear.head(6).iterrows():
            st_c = r["Stock"]
            bear_links_str += (
                f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{st_c}" target="_blank">📉 {st_c} Chart</a>'
                f'<a class="action-btn" href="https://www.google.com/search?q={st_c}+share+news+india&tbm=nws" target="_blank">📰 {st_c} News</a> &nbsp;'
            )
        st.markdown(bear_links_str, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🌊 ৩. সুইং ট্রেডিং স্পেশাল: ভলিউম ও প্রাইস শক স্ক্যানার (Unusual Volume + Big Move)")
    st.caption("যে শেয়ারগুলোতে আজ সাধারণ সময়ের চেয়ে দেড় গুণ বা দ্বিগুণের বেশি ভলিউম হয়েছে:")
    swing_shock_df = (
        all_st_df_global[all_st_df_global["RVOL_Num"] >= 1.3]
        .sort_values(by="RVOL_Num", ascending=False)
        .head(15)
        .reset_index(drop=True)
    )
    if swing_shock_df.empty:
        swing_shock_df = all_st_df_global.sort_values(by="RVOL_Num", ascending=False).head(12).reset_index(drop=True)

    swing_cols = [
        "Stock", "Sector", "Signal (সিগন্যাল)", "CMP (₹)", "1D %", "1W %",
        "Volume Action", "Day Range Pos %", "RSI (14)", "Intraday Catalyst"
    ]
    st.dataframe(
        style_colored_table(swing_shock_df[swing_cols], "1D %"),
        use_container_width=True,
        hide_index=True,
    )

# ==============================================================================
# TAB 3: লং ও শর্ট-টার্ম স্ক্যানার
# ==============================================================================
with tab3:
    st.subheader("🔥 লং-টার্ম ও পজিশনাল শেয়ার স্ক্যানার (Breakout, Turnaround & Deep Value)")
    cols_scanner = []
    for c_item in ["Stock", "Sector", "Signal (সিগন্যাল)", "CMP (₹)", "RSI (14)", "Volume Action", ret_key, "1W %", "From 52W High %"]:
        if c_item not in cols_scanner:
            cols_scanner.append(c_item)

    sc_col1, sc_col2 = st.columns(2)
    with sc_col1:
        st.markdown(f"#### 🔥 ১. ইনস্টিটিউশনাল ভলিউম ব্রেকআউট (High Volume Buying - {tf_option})")
        vol_brk_df = (
            all_st_df_global[all_st_df_global["1D %"] > 0]
            .sort_values(by=["RVOL_Num", ret_key], ascending=[False, False])
            .head(15)
            .reset_index(drop=True)
        )
        st.dataframe(style_colored_table(vol_brk_df[cols_scanner], ret_key), use_container_width=True, hide_index=True)

    with sc_col2:
        st.markdown(f"#### 🚀 ২. পজিশনাল মোমেন্টাম লিডার (Top Breakouts - {tf_option})")
        brk_df = (
            all_st_df_global[all_st_df_global["Above_50"]]
            .sort_values(by=ret_key, ascending=False)
            .head(15)
            .reset_index(drop=True)
        )
        st.dataframe(style_colored_table(brk_df[cols_scanner], ret_key), use_container_width=True, hide_index=True)

    st.markdown("---")
    sc_col3, sc_col4 = st.columns(2)
    with sc_col3:
        st.markdown("#### 🔄 ৩. নিচ থেকে ঘুরে দাঁড়ানো শেয়ার (Turnaround Gems)")
        turn_df = (
            all_st_df_global[(all_st_df_global["From 52W High %"] < -10) & (all_st_df_global["1W %"] > 0)]
            .sort_values(by="1W %", ascending=False)
            .head(15)
            .reset_index(drop=True)
        )
        st.dataframe(style_colored_table(turn_df[cols_scanner], "1W %"), use_container_width=True, hide_index=True)

    with sc_col4:
        st.markdown("#### 💎 ৪. লং-টার্ম ভ্যালু ও লো-RSI শেয়ার (Oversold / Deep Value)")
        val_df = all_st_df_global.sort_values(by="From 52W High %", ascending=True).head(15).reset_index(drop=True)
        st.dataframe(style_colored_table(val_df[cols_scanner], "From 52W High %"), use_container_width=True, hide_index=True)

    csv_bytes = all_st_df_global.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 সব শেয়ারের সম্পূর্ণ ডেটা (Intraday Levels, RSI ও Volume সহ) Excel/CSV ডাউনলোড করুন",
        data=csv_bytes,
        file_name="AlphaPulse_Full_Screener.csv",
        mime="text/csv",
    )

# ==============================================================================
# TAB 4: সব সেক্টরের তুলনামূলক টেবিল ও বার চার্ট
# ==============================================================================
with tab4:
    st.subheader(f"📊 ৩২টি সেক্টরের এক নজরে র‍্যাঙ্কিং ও তুলনামূলক টেবিল ({tf_option})")

    bar_secs = sorted(sector_master, key=lambda x: x[ret_key], reverse=True)
    bar_names = [s["Sector"] for s in bar_secs]
    bar_vals = [s[ret_key] for s in bar_secs]
    bar_cols = ["#00e676" if v >= 0 else "#ff5252" for v in bar_vals]

    fig_bar = go.Figure(
        go.Bar(
            x=bar_names,
            y=bar_vals,
            marker_color=bar_cols,
            text=[f"{v:+.1f}%" for v in bar_vals],
            textposition="outside",
        )
    )
    fig_bar.update_layout(
        title=f"সব সেক্টরের আপসাইড (সবুজ) বনাম ডাউনসাইড (লাল) তুলনা ({tf_option})",
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font=dict(color=text_color, size=11),
        height=360,
        margin=dict(t=40, b=80, l=15, r=15),
        xaxis=dict(tickangle=-35, gridcolor=grid_col),
        yaxis=dict(gridcolor=grid_col, title=f"Return ({tf_option}) %"),
    )
    st.plotly_chart(fig_bar, use_container_width=True, theme=None, key=f"bar_rank_{tf_option}")

    mat_df = pd.DataFrame(filtered_sectors)[
        ["Sector", "Stage", "Curr_Meter", "Prev_Meter", "Meter_Diff", "Avg RSI", "1D %", "1W %", "1M %", "3M %", "6M %", "1Y %", "5Y %"]
    ].rename(
        columns={
            "Curr_Meter": "Now Meter (0-100)",
            "Prev_Meter": "Prev Meter",
            "Meter_Diff": "Shift (Δ)",
        }
    ).reset_index(drop=True)

    st.dataframe(
        style_colored_table(mat_df, ret_key),
        use_container_width=True,
        height=640,
        hide_index=True,
    )

# ==============================================================================
# TAB 5: যেকোনো শেয়ারের নিজস্ব চার্ট, RSI, ভলিউম এবং স্টকের অ্যানালগ মিটার
# ==============================================================================
with tab5:
    st.subheader("📈 সিঙ্গেল স্টক চার্ট, RSI, ভলিউম এবং মুভিং অ্যাভারেজ (DMA)")

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        chosen_sec = st.selectbox("১. সেক্টর বেছে নিন:", list(sectors.keys()), key="t4_sec")
    with sc2:
        sec_tickers = [t.replace(".NS", "") for t in sectors[chosen_sec] if t in full_df.columns]
        chosen_stock = st.selectbox("২. শেয়ার বেছে নিন:", sec_tickers, key="t4_stk")
    with sc3:
        chart_tf = st.selectbox("৩. চার্টের সময়কাল:", ["3M", "6M", "1Y", "3Y", "5Y"], index=2, key="t4_tf")

    if chosen_stock:
        t_sym = chosen_stock + ".NS"
        s_info = all_stocks_master.get(t_sym, {})

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("বর্তমান দাম (CMP)", f"₹{s_info.get('CMP (₹)', 0)}")
        m2.metric("RSI (14)", f"{s_info.get('RSI (14)', 50)}")
        m3.metric("Volume Action", s_info.get("Volume Action", ""))
        m4.metric("1M Return", f"{s_info.get('1M %', 0):+.2f}%")
        m5.metric("52W High থেকে দূরত্ব", f"{s_info.get('From 52W High %', 0):+.2f}%")
        m6.metric("সিগন্যাল", s_info.get("Signal (সিগন্যাল)", ""))

        st.markdown(
            f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{chosen_stock}" target="_blank">📈 TradingView-তে {chosen_stock}-এর পূর্ণাঙ্গ চার্ট খুলুন</a> '
            f'<a class="action-btn" href="https://www.screener.in/company/{chosen_stock}/" target="_blank">📊 Screener.in-এ {chosen_stock}-এর ফান্ডামেন্টাল দেখুন</a> '
            f'<a class="action-btn" href="https://www.google.com/search?q={chosen_stock}+share+news+india&tbm=nws" target="_blank">📰 {chosen_stock}-এর ব্রেকিং নিউজ দেখুন</a>',
            unsafe_allow_html=True,
        )

        s_full = full_df[t_sym].dropna()
        sma20 = s_full.rolling(20).mean()
        sma50 = s_full.rolling(50).mean()
        sma200 = s_full.rolling(200).mean()

        d_cnt = tf_days_map[chart_tf]
        s_sub = s_full.tail(d_cnt)

        ind_c1, ind_c2 = st.columns([2.35, 1])
        with ind_c1:
            fig_ind = go.Figure()
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=s_sub, name=f"{chosen_stock} Price", line=dict(color=accent_col, width=2.8))
            )
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=sma20.tail(d_cnt), name="20 DMA", line=dict(color="#f59e0b", width=1.5, dash="dot"))
            )
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=sma50.tail(d_cnt), name="50 DMA", line=dict(color="#00e676", width=1.8))
            )
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=sma200.tail(d_cnt), name="200 DMA", line=dict(color="#ff5252", width=2.0))
            )
            fig_ind.update_layout(
                title=f"{chosen_stock} ({chosen_sec}) - প্রাইস ও মুভিং অ্যাভারেজ চার্ট ({chart_tf})",
                paper_bgcolor=chart_bg,
                plot_bgcolor=chart_bg,
                font=dict(color=text_color),
                height=400,
                hovermode="x unified",
                margin=dict(t=45, b=20, l=15, r=15),
                xaxis=dict(gridcolor=grid_col),
                yaxis=dict(gridcolor=grid_col, title="Price (₹)"),
                legend=dict(orientation="h", y=1.08, x=0, font=dict(color=text_color)),
            )
            st.plotly_chart(fig_ind, use_container_width=True, theme=None, key=f"ind_stock_chart_{chosen_stock}_{chart_tf}")

        with ind_c2:
            fig_st_gauge = make_analog_gauge(
                s_info.get("Meter Score", 50.0),
                s_info.get("Prev Meter", 50.0),
                f"{chosen_stock} মোমেন্টাম মিটার",
                height_px=360,
            )
            st.plotly_chart(fig_st_gauge, use_container_width=True, theme=None, key=f"ind_stock_gauge_{chosen_stock}_{chart_tf}")
