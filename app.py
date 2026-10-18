import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone, timedelta
import urllib.parse
import warnings

warnings.filterwarnings("ignore")

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="AlphaPulse Pro | Sector Turnaround & Intraday Terminal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. 42 COMPREHENSIVE SECTORS COVERING 420+ NIFTY 500 STOCKS (INCLUDING CEMENT)
# ==============================================================================
SECTOR_STOCKS = {
    "Cement & Clinker": ["ULTRACEMCO.NS", "AMBUJACEM.NS", "SHREECEM.NS", "DALBHARAT.NS", "ACC.NS", "JKCEMENT.NS", "RAMCOCEM.NS", "BIRLACORPN.NS", "INDIACEM.NS", "NUVOCO.NS", "JKTYRE.NS", "HEIDELBERG.NS"],
    "Defence & Aerospace": ["HAL.NS", "BEL.NS", "BDL.NS", "PARAS.NS", "DATAPATTNS.NS", "ASTRAMICRO.NS", "MIDHANI.NS", "ZENTEC.NS", "BEML.NS", "SOLARINDS.NS"],
    "Shipbuilding & Marine": ["MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "SCI.NS", "GESHIP.NS", "SEAMECLTD.NS", "DREDGECORP.NS"],
    "Railways & Wagons": ["RVNL.NS", "IRFC.NS", "IRCON.NS", "TITAGARH.NS", "JWL.NS", "CONCOR.NS", "RITES.NS", "RAILTEL.NS", "TEXRAIL.NS", "RAMKRISHNA.NS"],
    "Cables & Wires": ["POLYCAB.NS", "KEI.NS", "RRKABEL.NS", "FINCABLES.NS", "UNIVERSAL.NS", "STERLITE.NS", "PARAMOUNT.NS"],
    "Transformers & Power T&D": ["CGPOWER.NS", "VOLTAMP.NS", "TARIL.NS", "POWERINDIA.NS", "APARINDS.NS", "BHEL.NS", "SIEMENS.NS", "ABB.NS", "SCHNEIDER.NS", "TRITURBINE.NS"],
    "EMS & Electronics": ["DIXON.NS", "KAYNES.NS", "SYRMA.NS", "AMBER.NS", "PGEL.NS", "CYIENTDLM.NS", "AVALON.NS", "IKIO.NS", "HONAUT.NS"],
    "Green Energy & Solar": ["IREDA.NS", "SUZLON.NS", "INOXWIND.NS", "KPIGREEN.NS", "BORORENEW.NS", "SWLECT.NS", "SJVN.NS", "NHPC.NS", "ADANIGREEN.NS"],
    "Power Utilities & Financiers": ["NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "PFC.NS", "RECLTD.NS", "JSWENERGY.NS", "TORNTPOWER.NS", "CESC.NS", "ADANIPOWER.NS", "NLCINDIA.NS"],
    "Oil, Gas & City Gas": ["RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS", "HPCL.NS", "GAIL.NS", "OIL.NS", "PETRONET.NS", "IGL.NS", "MGL.NS", "GUJGASLTD.NS", "CHENNPETRO.NS"],
    "Metals, Steel & Mining": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "COALINDIA.NS", "NATIONALUM.NS", "SAIL.NS", "JINDALSTEL.NS", "HINDZINC.NS", "APLAPOLLO.NS", "WELCORP.NS"],
    "Auto OEMs (2W, 4W & CV)": ["M&M.NS", "TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "TVSMOTOR.NS", "HEROMOTOCO.NS", "ASHOKLEY.NS", "ESCORTS.NS", "FORCEMOT.NS"],
    "Auto Ancillaries & Tyres": ["MOTHERSON.NS", "BOSCHLTD.NS", "SONACOMS.NS", "UNOMINDA.NS", "APOLLOTYRE.NS", "BALKRISIND.NS", "MRF.NS", "CEATLTD.NS", "ENDURANCE.NS", "EXIDEIND.NS", "ARE&M.NS", "BHARATFORG.NS"],
    "PSU Banks": ["SBIN.NS", "BANKBARODA.NS", "PNB.NS", "CANBK.NS", "UNIONBANK.NS", "INDIANB.NS", "BANKINDIA.NS", "MAHABANK.NS", "IOB.NS", "UCOBANK.NS", "CENTRALBK.NS"],
    "Private Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "FEDERALBNK.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "RBLBANK.NS", "KARURVYSYA.NS", "AUBANK.NS", "CUB.NS"],
    "NBFCs & Housing Finance": ["BAJFINANCE.NS", "BAJAJFINSV.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "LICHSGFIN.NS", "PNBHOUSING.NS", "LTF.NS", "M&MFIN.NS", "POONAWALLA.NS", "CANFINHOME.NS"],
    "Insurance (Life & General)": ["LICI.NS", "SBILIFE.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", "ICICIGI.NS", "STARHEALTH.NS", "NIACL.NS", "GICRE.NS", "MFSL.NS"],
    "Capital Market, Exchanges & AMC": ["BSE.NS", "MCX.NS", "CDSL.NS", "ANGELONE.NS", "MOTILALOFS.NS", "CAMS.NS", "ANANDRATHI.NS", "HDFCAMC.NS", "NAM-INDIA.NS", "UTIAMC.NS", "KFINTECH.NS", "ISEC.NS"],
    "IT Largecap": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"],
    "IT Midcap, AI & ER&D": ["PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS", "MPHASIS.NS", "OFSS.NS", "LTTS.NS", "CYIENT.NS", "ZENSARTECH.NS", "BSOFT.NS", "SONATSOFTW.NS", "MASTEK.NS"],
    "Largecap Pharma": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "LUPIN.NS", "AUROPHARMA.NS", "ZYDUSLIFE.NS", "TORNTPHARM.NS", "ALKEM.NS", "GLENMARK.NS", "BIOCON.NS", "MANKIND.NS"],
    "CDMO, API & Specialty Pharma": ["DIVISLAB.NS", "LAURUSLABS.NS", "SYNGENE.NS", "SUVENPHAR.NS", "GRANULES.NS", "NEULANDLAB.NS", "PIRAMALPHR.NS", "JBCHEPHARM.NS", "NATCOPHARM.NS", "IPCALAB.NS", "GLAND.NS"],
    "Hospitals & Diagnostics": ["APOLLOHOSP.NS", "MAXHEALTH.NS", "FORTIS.NS", "NH.NS", "LALPATHLAB.NS", "METROPOLIS.NS", "MEDANTA.NS", "KIMS.NS", "ASTERDM.NS", "RAINBOW.NS", "VIJAYA.NS"],
    "Specialty Chemicals": ["PIIND.NS", "SRF.NS", "DEEPAKNTR.NS", "NAVINFLUOR.NS", "CLEAN.NS", "AARTIIND.NS", "ATUL.NS", "VINATIORGA.NS", "FLUOROCHEM.NS", "ALKYLAMINE.NS", "TATACHEM.NS", "FINEORG.NS"],
    "Fertilizers & Agrochemicals": ["COROMANDEL.NS", "CHAMBLFERT.NS", "GNFC.NS", "FACT.NS", "RCF.NS", "GSFC.NS", "DEEPAKFERT.NS", "PARADEEP.NS", "UPL.NS", "SUMICHEM.NS", "RALLIS.NS", "BAYERCROP.NS"],
    "Real Estate & Developers": ["DLF.NS", "GODREJPROP.NS", "MACROTECH.NS", "OBERIRLTY.NS", "PRESTIGE.NS", "BRIGADE.NS", "PHOENIXLTD.NS", "SOBHA.NS", "SUNTECK.NS", "MAHLIFE.NS", "ANANTRAJ.NS"],
    "Infra, EPC & Construction": ["LT.NS", "KPIL.NS", "KEC.NS", "NCC.NS", "PNCINFRA.NS", "HGINFRA.NS", "ENGINERSIN.NS", "NBCC.NS", "IRB.NS", "GRINFRA.NS", "KNRCON.NS", "AHLUCONT.NS"],
    "Building Materials (Pipes & Tiles)": ["ASTRAL.NS", "SUPREMEIND.NS", "CERA.NS", "KAJARIACER.NS", "FINPIPE.NS", "PRINCEPIPE.NS", "APOLLOPIPE.NS", "SOMANYCERA.NS"],
    "Paints, Adhesives & Woodpanel": ["ASIANPAINT.NS", "BERGEPAINT.NS", "KANSAINER.NS", "PIDILITIND.NS", "AKZOINDIA.NS", "INDIGOPNTS.NS", "CENTURYPLY.NS", "GREENPANEL.NS", "GREENPLY.NS"],
    "Cooling, HVAC & Consumer Durables": ["VOLTAS.NS", "BLUESTARCO.NS", "SYMPHONY.NS", "WHIRLPOOL.NS", "HAVELLS.NS", "CROMPTON.NS", "VGUARD.NS", "ORIENTELEC.NS", "BAJAJELEC.NS"],
    "CNC, Bearings & Industrial Engg": ["CUMMINSIND.NS", "TIMKEN.NS", "SKFINDIA.NS", "SCHAEFFLER.NS", "GRINDWELL.NS", "MTARTECH.NS", "THERMAX.NS", "CARBORUNIV.NS", "ELGIEQUIP.NS", "AIAENG.NS"],
    "FMCG & Staples": ["ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "BRITANNIA.NS", "DABUR.NS", "MARICO.NS", "TATACONSUM.NS", "GODREJCP.NS", "COLPAL.NS", "VBL.NS", "EMAMILTD.NS", "JYOTHYLAB.NS"],
    "QSR, Food & Beverages": ["ZOMATO.NS", "JUBLFOOD.NS", "DEVYANI.NS", "WESTLIFE.NS", "SAPPHIRE.NS", "BIKAJI.NS", "RADICO.NS", "UNITDSPR.NS", "UBL.NS", "PATANJALI.NS"],
    "Retail, Supermarkets & Footwear": ["TRENT.NS", "DMART.NS", "BATAINDIA.NS", "METROBRAND.NS", "MANYAVAR.NS", "ABFRL.NS", "RELAXO.NS", "CAMPUS.NS", "NYKAA.NS", "SHOPERSTOP.NS"],
    "Textiles, Yarn & Apparel": ["PAGEIND.NS", "KPRMILL.NS", "TRIDENT.NS", "WELSPUNLIV.NS", "VTL.NS", "RAYMOND.NS", "ARVIND.NS", "GOKEX.NS", "SWANENERGY.NS", "ALOKINDS.NS"],
    "Jewellery & Luxury": ["TITAN.NS", "KALYANKJIL.NS", "SENCO.NS", "THANGAMAYL.NS", "ETHOSLTD.NS", "RAJESHEXPO.NS", "VAIBHAVGBL.NS"],
    "Telecom, Towers & Broadband": ["BHARTIARTL.NS", "INDUSTOWER.NS", "IDEA.NS", "TATACOMM.NS", "TEJASNET.NS", "HFCL.NS", "ITI.NS", "STLTECH.NS", "ROUTE.NS"],
    "Logistics, Ports & Supply Chain": ["ADANIPORTS.NS", "DELHIVERY.NS", "BLUEDART.NS", "JSWINFRA.NS", "TCIEXP.NS", "ALLCARGO.NS", "VRL.NS", "AEGISLOG.NS", "GPPL.NS", "GATEWAY.NS"],
    "Hotels, Tourism & Aviation": ["INDIGO.NS", "INDHOTEL.NS", "LEMONTREE.NS", "CHALET.NS", "IRCTC.NS", "EIHOTEL.NS", "EASEMYTRIP.NS", "BLS.NS", "THOMASCOOK.NS"],
    "Sugar, Ethanol & Paper": ["BALRAMCHIN.NS", "TRIVENI.NS", "EIDPARRY.NS", "RENUKA.NS", "PRAJIND.NS", "JKPAPER.NS", "WESTCOAST.NS", "ANDHRAPAP.NS"],
    "Packaging & BOPP Films": ["EPL.NS", "UFLEX.NS", "POLYPLEX.NS", "JINDALPOLY.NS", "MOLDTKPAC.NS", "TCPLPACK.NS", "HUHTAMAKI.NS", "AGI.NS"],
    "Media, Multiplex & Gaming": ["SUNTV.NS", "PVRINOX.NS", "ZEEL.NS", "NAZARA.NS", "DELTACORP.NS", "NETWORK18.NS", "SAREGAMA.NS", "TIPSINDLTD.NS"]
}

ALL_TICKERS = sorted(list({t for lst in SECTOR_STOCKS.values() for t in lst}))
TICKER_TO_SECTOR = {t: sec for sec, lst in SECTOR_STOCKS.items() for t in lst}
DEFAULT_SECTOR = f"All {len(SECTOR_STOCKS)} Sectors ({len(ALL_TICKERS)} Stocks)"
DEFAULT_STOCK = "Search or Select Stock..."

# ==============================================================================
# 3. SESSION STATE & URL QUERY PARAMETER HANDLER
# ==============================================================================
for k, v in [
    ("selected_sector", DEFAULT_SECTOR),
    ("selected_stock", DEFAULT_STOCK),
    ("kpi_panel", None),
    ("scroll_target", None),
    ("last_alerted", ""),
    ("show_ai_helper", False),
    ("show_nse_heatmap", False)
]:
    if k not in st.session_state:
        st.session_state[k] = v

qp = st.query_params
if "nav_action" in qp:
    st.session_state.selected_sector = DEFAULT_SECTOR
    st.session_state.selected_stock = DEFAULT_STOCK
    st.session_state.kpi_panel = None
    st.session_state.scroll_target = None
    st.session_state.show_nse_heatmap = False
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
# 4. TOP HEADER BAR WITH AI HELP, HEATMAP TOGGLE & REFRESH
# ==============================================================================
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
is_mkt_open = (ist_now.weekday() < 5) and (
    (ist_now.hour == 9 and ist_now.minute >= 15)
    or (10 <= ist_now.hour <= 14)
    or (ist_now.hour == 15 and ist_now.minute <= 30)
)
mkt_status_html = (
    f'<span style="color:#10b981;font-weight:800;">🟢 LIVE MARKET ({ist_now.strftime("%I:%M %p IST")})</span>'
    if is_mkt_open else
    f'<span style="color:#f59e0b;font-weight:700;">🕒 MARKET CLOSED ({ist_now.strftime("%a %I:%M %p IST")})</span>'
)

top_c1, top_c2, top_c3, top_c4, top_c5, top_c6 = st.columns([4.6, 1.6, 1.15, 0.9, 0.9, 0.85])
with top_c1:
    st.markdown(
        f'<a href="?nav_action=home" target="_self" class="brand-logo-link" title="Click to Reset All Filters & Return to Home">'
        f'<span class="clean-compass-icon">🧭</span>'
        f'<div><div class="brand-title-glow">AlphaPulse Pro — Nifty 500 Turnaround Terminal</div>'
        f'<div class="brand-subtitle">{len(SECTOR_STOCKS)} Sectors • {len(ALL_TICKERS)}+ Stocks • {mkt_status_html}</div></div></a>',
        unsafe_allow_html=True
    )
with top_c2:
    theme_mode = st.selectbox("Theme", ["🌙 Pro Dark (Slate)", "🌌 Cyber Neon (Violet)", "☀️ Clean Light (Day)"], index=0, label_visibility="collapsed")
with top_c3:
    if st.button("🤖 AI Help", use_container_width=True, help="Open Live AI Trading Assistant & Gemini Chat"):
        st.session_state.show_ai_helper = not st.session_state.show_ai_helper
with top_c4:
    show_analog_meter = st.toggle("🎛️ Meters", value=True)
with top_c5:
    auto_alert_on = st.toggle("🔔 Auto", value=False, help="Auto-scans every 3 mins during live market hours")
with top_c6:
    if st.button("🔄", use_container_width=True, help="Refresh Live Market Data"):
        st.cache_data.clear()
        st.rerun()

# ==============================================================================
# 5. THEME ENGINE & ICON-SAFE RESPONSIVE CSS (FIXES _arrow_right OVERLAP BUG)
# ==============================================================================
if "Clean Light" in theme_mode:
    BG_MAIN, BG_CARD, BG_SUB, TEXT_MAIN, TEXT_SUB, BORDER_C, ACCENT_C = "#f4f6fb", "#ffffff", "#eef2f8", "#0f172a", "#475569", "#cbd5e1", "#d97706"
    BTN_BG, BTN_BORDER, CARD_SHADOW = "linear-gradient(135deg,#ffffff,#e2e8f0)", "#94a3b8", "0 4px 14px rgba(15,23,42,0.06)"
elif "Cyber Neon" in theme_mode:
    BG_MAIN, BG_CARD, BG_SUB, TEXT_MAIN, TEXT_SUB, BORDER_C, ACCENT_C = "#080214", "#14062b", "#1d093d", "#f8fafc", "#e879f9", "#00f5d488", "#00f5d4"
    BTN_BG, BTN_BORDER, CARD_SHADOW = "linear-gradient(135deg,#3b0764,#701a75)", "#00f5d4", "0 0 20px rgba(0,245,212,0.20)"
else:
    BG_MAIN, BG_CARD, BG_SUB, TEXT_MAIN, TEXT_SUB, BORDER_C, ACCENT_C = "#060a12", "#0f172a", "#141f38", "#f8fafc", "#94a3b8", "#1e293b", "#f59e0b"
    BTN_BG, BTN_BORDER, CARD_SHADOW = "linear-gradient(135deg,#111c33,#1e293b)", "#38bdf866", "0 6px 18px rgba(0,0,0,0.38)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

header[data-testid="stHeader"], div[data-testid="stToolbar"], div[data-testid="stDecoration"] {{ display:none !important; }}

/* APPLY MODERN FONT WITHOUT BREAKING STREAMLIT MATERIAL ICONS (_arrow_right FIX) */
html, body, [data-testid="stAppViewContainer"], .main, p, label, button, input, .stMarkdown {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}}
[data-testid="stIconMaterial"], .material-icons, .material-symbols-rounded {{
    font-family: 'Material Symbols Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: 1.15rem !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-smoothing: antialiased !important;
}}

html, body, [data-testid="stAppViewContainer"], .main {{
    background-color:{BG_MAIN} !important;
    color:{TEXT_MAIN} !important;
    scroll-behavior:smooth !important;
}}
.block-container {{ padding-top:1.1rem !important; padding-bottom:4.8rem !important; max-width:97% !important; }}

a.brand-logo-link {{
    text-decoration:none !important;
    display:inline-flex;
    align-items:center;
    gap:10px;
    padding:2px 4px;
    transition:transform 0.2s ease;
}}
a.brand-logo-link:hover {{ transform:translateY(-1px); }}
.clean-compass-icon {{
    font-size:2.2rem;
    line-height:1;
    background:transparent !important;
    border:none !important;
    padding:0 !important;
    filter:drop-shadow(0 2px 6px rgba(245,158,11,0.35));
}}
.brand-title-glow {{
    font-size:1.35rem;
    font-weight:800;
    letter-spacing:-0.4px;
    line-height:1.18;
    background:linear-gradient(90deg, #f59e0b 0%, #ef4444 48%, #10b981 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}}
.brand-subtitle {{ font-size:0.73rem; font-weight:600; color:{TEXT_SUB} !important; }}

[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, .stSelectbox label, .stNumberInput label, .stRadio label, [data-testid="stRadio"] label span, [data-testid="stToggle"] label p, [data-testid="stCheckbox"] label p {{
    color:{TEXT_MAIN} !important; font-weight:700 !important; font-size:0.81rem !important; opacity:1 !important;
}}
[data-testid="stRadio"] div[role="radiogroup"] {{ background:{BG_CARD}; border:1px solid {BORDER_C}; padding:3px 10px; border-radius:999px; gap:10px !important; }}

div.stButton > button, button[data-testid="stBaseButton-secondary"], div.stDownloadButton > button,
div.stLinkButton > a, a[data-testid="stBaseLinkButton-secondary"] {{
    background:{BTN_BG} !important;
    color:{TEXT_MAIN} !important;
    border:1.5px solid {BTN_BORDER} !important;
    border-radius:10px !important;
    font-weight:800 !important;
    font-size:0.80rem !important;
    padding:0.42rem 0.85rem !important;
    box-shadow:{CARD_SHADOW} !important;
    text-decoration:none !important;
    transition:all 0.2s ease !important;
}}
div.stButton > button p, div.stDownloadButton > button p, div.stLinkButton > a p, a[data-testid="stBaseLinkButton-secondary"] p, a[data-testid="stBaseLinkButton-secondary"] span {{
    color:{TEXT_MAIN} !important; font-weight:800 !important;
}}
div.stButton > button:hover, div.stDownloadButton > button:hover, div.stLinkButton > a:hover, a[data-testid="stBaseLinkButton-secondary"]:hover {{
    background:linear-gradient(135deg,#f59e0b,#ea580c) !important;
    color:#ffffff !important;
    border-color:#f59e0b !important;
    transform:translateY(-2px) !important;
}}
div.stButton > button:hover p, div.stLinkButton > a:hover p, a[data-testid="stBaseLinkButton-secondary"]:hover p, a[data-testid="stBaseLinkButton-secondary"]:hover span {{
    color:#ffffff !important;
}}

/* HIGH-CONTRAST TABS & CLEAN EXPANDERS WITH PROPER SPACING */
button[data-baseweb="tab"] {{
    background:{BG_CARD} !important;
    border:1.5px solid {BORDER_C} !important;
    border-radius:10px 10px 0 0 !important;
    margin-right:6px !important;
    padding:8px 16px !important;
}}
button[data-baseweb="tab"] p {{
    color:{TEXT_MAIN} !important;
    font-weight:700 !important;
    font-size:0.84rem !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    background:linear-gradient(135deg,rgba(245,158,11,0.22),rgba(16,185,129,0.18)) !important;
    border-color:#f59e0b !important;
    border-bottom:3px solid #f59e0b !important;
}}
button[data-baseweb="tab"][aria-selected="true"] p {{
    color:#f59e0b !important;
    font-weight:800 !important;
}}
[data-testid="stExpander"] details {{
    background:{BG_CARD} !important;
    border:1px solid {BORDER_C} !important;
    border-radius:10px !important;
    box-shadow:{CARD_SHADOW};
    margin-top:2px !important;
}}
[data-testid="stExpander"] summary {{
    padding:9px 14px !important;
    display:flex !important;
    align-items:center !important;
    gap:8px !important;
}}
[data-testid="stExpander"] summary p {{
    color:{TEXT_MAIN} !important;
    font-weight:700 !important;
    font-size:0.82rem !important;
    margin:0 !important;
}}

.aligned-sec-hdr {{
    font-size:0.88rem;
    font-weight:800;
    color:{TEXT_MAIN};
    background:{BG_CARD};
    border:1px solid {BORDER_C};
    border-left:4px solid #f59e0b;
    padding:8px 12px;
    border-radius:8px;
    margin-bottom:8px;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}}

/* NSE-STYLE LIVE HEATMAP TILES (MATCHING NSE HEATMAP SCREENSHOT) */
.nse-heatmap-container {{
    background:{BG_CARD};
    border:1.5px solid {BORDER_C};
    border-radius:14px;
    padding:14px 16px;
    margin:8px 0 14px 0;
    box-shadow:{CARD_SHADOW};
}}
.nse-legend-bar {{
    display:flex;
    gap:5px;
    align-items:center;
    flex-wrap:wrap;
}}
.nse-leg-pill {{
    padding:2px 9px;
    border-radius:999px;
    font-size:0.68rem;
    font-weight:800;
    color:#ffffff;
}}
.nse-heatmap-grid {{
    display:grid;
    grid-template-columns:repeat(auto-fill, minmax(175px, 1fr));
    gap:8px;
    margin-top:10px;
}}
a.nse-tile {{
    text-decoration:none !important;
    color:#ffffff !important;
    padding:10px 12px;
    border-radius:8px;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    height:74px;
    box-shadow:0 3px 8px rgba(0,0,0,0.22);
    transition:transform 0.16s ease, filter 0.16s ease;
    border:1px solid rgba(255,255,255,0.15);
}}
a.nse-tile:hover {{
    transform:translateY(-2px) scale(1.02);
    filter:brightness(1.12);
}}
.nse-tile-name {{
    font-size:0.74rem;
    font-weight:800;
    text-transform:uppercase;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}}
.nse-tile-bot {{
    display:flex;
    justify-content:space-between;
    align-items:baseline;
    font-family:'JetBrains Mono',monospace !important;
}}

/* PULSE BAR & TURNAROUND HERO DECK */
.pulse-bar {{ background:{BG_CARD}; border:1px solid {BORDER_C}; border-radius:12px; padding:8px 14px; margin:6px 0 10px 0; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:8px; box-shadow:{CARD_SHADOW}; }}
.pulse-item {{ font-size:0.81rem; font-weight:700; color:{TEXT_MAIN}; font-family:'JetBrains Mono',monospace !important; }}
.compass-pill {{ padding:3px 10px; border-radius:999px; font-size:0.74rem; font-weight:800; }}
.turnaround-hero-box {{ background:{BG_CARD}; border:1.5px solid {BORDER_C}; border-left:5px solid #10b981; border-radius:12px; padding:10px 14px; margin:4px 0 10px 0; box-shadow:{CARD_SHADOW}; }}
.turnaround-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:8px; margin-top:8px; }}
a.turn-sec-card {{ text-decoration:none !important; background:{BG_SUB}; border:1px solid #10b98155; border-radius:10px; padding:8px 11px; color:{TEXT_MAIN} !important; display:flex; flex-direction:column; justify-content:space-between; height:84px; transition:all 0.18s ease; }}
a.turn-sec-card:hover {{ border-color:#f59e0b; transform:translateY(-2px); box-shadow:0 4px 12px rgba(16,185,129,0.22); }}
.t-sec-name {{ font-weight:800; font-size:0.81rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:145px; }}

/* NEXT-DAY WATCHLIST CARDS */
.radar-panel-bull {{ background:{BG_CARD}; border:1px solid #10b98166; border-top:3.5px solid #10b981; border-radius:12px; padding:10px 12px; margin-bottom:8px; }}
.radar-panel-bear {{ background:{BG_CARD}; border:1px solid #ef444466; border-top:3.5px solid #ef4444; border-radius:12px; padding:10px 12px; margin-bottom:8px; }}
.radar-panel-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid {BORDER_C}; }}
.radar-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(235px,1fr)); gap:7px; }}
a.radar-row-card {{ text-decoration:none !important; background:{BG_SUB}; border:1px solid {BORDER_C}; border-radius:9px; padding:8px 10px; color:{TEXT_MAIN} !important; display:flex; flex-direction:column; justify-content:space-between; min-height:96px; transition:all 0.18s ease; }}
a.radar-row-card:hover {{ border-color:#f59e0b; transform:translateY(-2px); }}
.r-top {{ display:flex; justify-content:space-between; align-items:center; }}
.r-sym {{ font-size:0.84rem; font-weight:800; color:{TEXT_MAIN}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:155px; }}
.r-tag-bull {{ background:rgba(16,185,129,0.16); color:#10b981; border:1px solid #10b98155; padding:1px 6px; border-radius:5px; font-size:0.66rem; font-weight:800; }}
.r-tag-bear {{ background:rgba(239,68,68,0.16); color:#ef4444; border:1px solid #ef444455; padding:1px 6px; border-radius:5px; font-size:0.66rem; font-weight:800; }}
.r-mid {{ display:flex; justify-content:space-between; font-size:0.73rem; color:{TEXT_SUB}; }}
.r-reason-box {{ font-size:0.70rem; color:{TEXT_MAIN}; background:rgba(245,158,11,0.10); border-left:2.5px solid #f59e0b; padding:3px 7px; border-radius:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.r-plan {{ display:flex; justify-content:space-between; font-size:0.70rem; font-weight:700; background:rgba(0,0,0,0.16); padding:3px 7px; border-radius:6px; font-family:'JetBrains Mono',monospace !important; }}
a.wa-share-btn {{ text-decoration:none !important; background:linear-gradient(135deg,#16a34a,#22c55e); color:#fff !important; padding:5px 13px; border-radius:999px; font-size:0.75rem; font-weight:800; display:inline-flex; align-items:center; gap:5px; }}

/* MARQUEE & KPI CARDS */
.marquee-wrap {{ background:{BG_CARD}; border:1px solid {BORDER_C}; border-radius:10px; padding:7px 10px; overflow:hidden; white-space:nowrap; margin:6px 0 12px 0; box-shadow:{CARD_SHADOW}; }}
.marquee-track {{ display:inline-block; animation:ticker-move 55s linear infinite; }}
.marquee-wrap:hover .marquee-track {{ animation-play-state:paused; }}
@keyframes ticker-move {{ 0% {{ transform:translateX(0%); }} 100% {{ transform:translateX(-50%); }} }}
a.sec-pill-up, a.sec-pill-down {{ text-decoration:none !important; display:inline-flex; align-items:center; gap:5px; padding:3px 11px; margin-right:8px; border-radius:999px; font-size:0.74rem; font-weight:700; }}
a.sec-pill-up {{ background:rgba(16,185,129,0.14); border:1px solid #10b981; color:#10b981 !important; }}
a.sec-pill-down {{ background:rgba(239,68,68,0.14); border:1px solid #ef4444; color:#ef4444 !important; }}
.kpi-card {{ background:{BG_CARD}; border:1.5px solid {BORDER_C}; border-radius:12px; padding:10px 14px; height:102px; display:flex; flex-direction:column; justify-content:space-between; margin-bottom:6px; box-shadow:{CARD_SHADOW}; }}
.kpi-title {{ color:{TEXT_SUB}; font-size:0.75rem; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.kpi-val {{ font-size:1.08rem; font-weight:800; color:{TEXT_MAIN}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.kpi-sub-up {{ background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b98155; padding:2px 8px; border-radius:6px; font-size:0.69rem; font-weight:700; width:fit-content; }}
.kpi-sub-down {{ background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid #ef444455; padding:2px 8px; border-radius:6px; font-size:0.69rem; font-weight:700; width:fit-content; }}
.pill-container {{ display:flex; flex-wrap:wrap; gap:5px; margin-top:6px; }}
a.bull-pill, a.bear-pill {{ text-decoration:none !important; padding:3px 8px; border-radius:999px; font-size:0.71rem; font-weight:700; display:inline-flex; align-items:center; gap:4px; }}
a.bull-pill {{ background:rgba(16,185,129,0.14); border:1px solid #10b98199; color:#10b981 !important; }}
a.bear-pill {{ background:rgba(239,68,68,0.14); border:1px solid #ef444499; color:#ef4444 !important; }}

/* FLOATING RIGHT DOCK (AI HELP + TOP BUTTON) */
.floating-right-dock {{
    position:fixed;
    bottom:58px;
    right:18px;
    z-index:999999;
    display:flex;
    flex-direction:column;
    gap:7px;
    align-items:flex-end;
}}
a.floating-ai-btn {{
    text-decoration:none !important;
    background:linear-gradient(135deg,#7c3aed,#2563eb);
    color:#ffffff !important;
    padding:7px 14px;
    border-radius:999px;
    font-size:0.78rem;
    font-weight:800;
    border:1.5px solid rgba(255,255,255,0.35);
    box-shadow:0 6px 18px rgba(124,58,237,0.5);
}}
a.single-top-btn {{
    text-decoration:none !important;
    background:linear-gradient(135deg,#f59e0b,#ea580c);
    color:#fff !important;
    padding:7px 15px;
    border-radius:999px;
    font-size:0.79rem;
    font-weight:800;
    border:1.5px solid rgba(255,255,255,0.35);
    box-shadow:0 6px 20px rgba(245,158,11,0.5);
}}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. NAN-SAFE DATA ENGINE (42 SECTORS & 420+ NIFTY 500 STOCKS)
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

def make_stock_pills(df_sub: pd.DataFrame) -> str:
    pills = []
    for _, r in df_sub.iterrows():
        qt = urllib.parse.quote(str(r["Ticker"]))
        cls = "bull-pill" if safe_num(r.get("1D", 0.0)) >= 0 else "bear-pill"
        icon = "🟢" if safe_num(r.get("1D", 0.0)) >= 0 else "🔴"
        pills.append(f'<a class="{cls}" href="?focus_stock={qt}" target="_self">{icon} {r["Symbol"]}</a>')
    return f'<div class="pill-container">{"".join(pills)}</div>'

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

@st.cache_data(ttl=300, show_spinner=False)
def load_full_market_data():
    raw = yf.download(ALL_TICKERS, period="1y", interval="1d", progress=False, group_by="ticker", threads=True)
    stock_rows = []
    for ticker in ALL_TICKERS:
        try:
            df = raw[ticker] if len(ALL_TICKERS) > 1 else raw
            if df is None or df.empty:
                continue
            df = df.dropna(subset=["Close", "Open", "High", "Low"])
            if len(df) < 22:
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
                action_sig = "⚠️ Overbought"
            elif bull_candle and consec_up <= 2 and vol_ratio >= 1.15:
                action_sig = "🟢 Turnaround Buy"
            elif c_now >= dma50 and -2.5 <= dist_20 <= 3.5 and 45 <= rsi_val <= 65:
                action_sig = "💎 Swing Buy"
            elif bear_candle and consec_down <= 2 and vol_ratio >= 1.15:
                action_sig = "🔴 Top Short"
            else:
                action_sig = "⚖️ Watch"

            conf_score = int(np.clip(55 + min(vol_ratio * 12, 25) + (10 if c_now >= dma50 else -5) + (8 if (bull_candle or bear_candle) else 0), 45, 96))

            stock_rows.append({
                "Ticker": ticker, "Symbol": ticker.replace(".NS", ""), "Sector": TICKER_TO_SECTOR.get(ticker, "Others"),
                "Price": round(c_now, 2), "1D": round(r_1d, 2), "1W": round(r_1w, 2), "1M": round(r_1m, 2),
                "3M": round(r_3m, 2), "6M": round(r_6m, 2), "1Y": round(r_1y, 2),
                "Vol_Ratio": vol_ratio, "RSI": rsi_val, "DMA20": round(dma20, 2), "DMA50": round(dma50, 2),
                "Above_20DMA": bool(c_now >= dma20), "Above_50DMA": bool(c_now >= dma50), "Dist_20DMA": dist_20,
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
        s_b20 = safe_num((grp["Above_20DMA"].sum() / max(len(grp), 1)) * 100.0, 50.0)
        s_b50 = safe_num((grp["Above_50DMA"].sum() / max(len(grp), 1)) * 100.0, 50.0)
        avg_price = safe_num(grp["Price"].mean(), 1000.0)

        was_correcting = (s_1m <= 2.2) or (s_3m <= 3.5) or (s_1w <= 1.5)
        reversing_up = (s_1d >= -0.05) and ((s_1d > (s_1w / 5.0)) or (s_1w > (s_1m / 4.0)))
        sec_bull_turn = bool(was_correcting and reversing_up)
        sec_bear_roll = bool((s_1m >= 1.5 or s_1w >= 1.0) and (s_1d <= 0.15) and (s_1d < (s_1w / 5.0)))

        turn_score = round(
            (35.0 if sec_bull_turn else 0.0)
            + (max(0.0, 3.0 - s_1m) * 3.2 if reversing_up else 0.0)
            + (s_1d * 10.0)
            + (s_vol * 18.0)
            + (s_b20 * 0.2),
            1
        )

        meter = int(np.clip(safe_num(50.0 + (s_1w * 3.5) + (s_1d * 6.0) + ((s_rsi - 50.0) * 0.6), 50.0), 5, 98))
        zone = "🔄 Turnaround" if (sec_bull_turn and s_1d >= 0) else (
            "🚀 Leading" if (s_1w >= 2.0 and s_1d >= 0) else (
                "⚠️ Exhaustion" if (sec_bear_roll and s_1d < 0) else "💎 Value Watch"
            )
        )
        top_pick_sym = grp.sort_values(["Vol_Ratio", "1D"], ascending=[False, False]).iloc[0]["Symbol"]

        sec_rows.append({
            "Sector": sec_name, "Count": len(grp), "Top_Pick": top_pick_sym, "Avg_Price": round(avg_price, 1),
            "1D": round(s_1d, 2), "1W": round(s_1w, 2), "1M": round(s_1m, 2),
            "3M": round(s_3m, 2), "6M": round(s_6m, 2), "1Y": round(s_1y, 2),
            "Avg_Vol": round(s_vol, 2), "RSI": round(s_rsi, 1),
            "Breadth_20DMA": round(s_b20, 1), "Breadth_50DMA": round(s_b50, 1),
            "Meter": meter, "Turnaround_Score": turn_score, "Zone": zone,
            "Sec_Bull_Turn": sec_bull_turn, "Sec_Bear_Roll": sec_bear_roll,
        })

    sectors_df = pd.DataFrame(sec_rows)
    sec_map = sectors_df.set_index("Sector").to_dict("index")
    stocks_df["Sec_1D"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("1D", 0.0))
    stocks_df["Sec_1W"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("1W", 0.0))
    stocks_df["Sec_1M"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("1M", 0.0))
    stocks_df["Sec_Bull_Turn"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Sec_Bull_Turn", False))
    stocks_df["Sec_Bear_Roll"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Sec_Bear_Roll", False))
    return stocks_df, sectors_df

@st.cache_data(ttl=180, show_spinner=False)
def run_chartink_15m_scanner(stocks_df: pd.DataFrame):
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()
    active_pool = stocks_df[stocks_df["Price"] > 150].sort_values("Vol_Ratio", ascending=False).head(40)
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
                        "Reason": "⚡ 15m Open≈Low + Above VWAP & Prev High", "Entry": round(max(c15, h15 * 1.0005), 2),
                        "SL": round(min(l15, vwap15 * 0.995), 2), "Target": round(c15 + 1.6 * d_info["ATR"], 2),
                    })
                if (o15 >= h15 * 0.995 or c15 < o15) and c15 <= d_info["Prev_Low"] * 1.004 and v15_ratio >= 1.30 and (22 <= rsi15 <= 44) and c15 < vwap15:
                    bear_15m.append({
                        "Symbol": tk.replace(".NS", ""), "Ticker": tk, "Sector": d_info["Sector"], "Price": round(c15, 2),
                        "VWAP": round(vwap15, 2), "Vol_Ratio": v15_ratio, "RSI": rsi15, "1D": d_info["1D"], "Confidence": d_info["Confidence"],
                        "Reason": "📉 15m Open≈High + Below VWAP & Prev Low", "Entry": round(min(c15, l15 * 0.9995), 2),
                        "SL": round(max(h15, vwap15 * 1.005), 2), "Target": round(c15 - 1.6 * d_info["ATR"], 2),
                    })
            except Exception:
                continue
    except Exception:
        pass

    if not bull_15m:
        for _, r in active_pool[(active_pool["Price"] > active_pool["DMA20"]) & (active_pool["1D"] > 0)].head(6).iterrows():
            bull_15m.append({"Symbol": r["Symbol"], "Ticker": r["Ticker"], "Sector": r["Sector"], "Price": r["Price"], "VWAP": round(r["Price"] * 0.994, 2), "Vol_Ratio": r["Vol_Ratio"], "RSI": r["RSI"], "1D": r["1D"], "Confidence": r["Confidence"], "Reason": "⚡ Near Prev High Breakout + Above 20-DMA", "Entry": r["Buy_Entry"], "SL": r["Buy_SL"], "Target": r["Buy_Target"]})
    if not bear_15m:
        for _, r in active_pool[active_pool["1D"] < 0].head(6).iterrows():
            bear_15m.append({"Symbol": r["Symbol"], "Ticker": r["Ticker"], "Sector": r["Sector"], "Price": r["Price"], "VWAP": round(r["Price"] * 1.006, 2), "Vol_Ratio": r["Vol_Ratio"], "RSI": r["RSI"], "1D": r["1D"], "Confidence": r["Confidence"], "Reason": "📉 Below Intraday VWAP + Supply Pressure", "Entry": r["Short_Entry"], "SL": r["Short_SL"], "Target": r["Short_Target"]})

    return pd.DataFrame(bull_15m), pd.DataFrame(bear_15m)

def filter_next_day_intraday_stocks(stocks_df: pd.DataFrame):
    df = stocks_df.copy()
    b_cand = df[(df["Consec_Up"] <= 2) & (df["1D"] >= -0.3) & (df["1D"] <= 3.8) & (df["Vol_Ratio"] >= 1.10)].copy()
    b_cand["Bull_Candle"] = b_cand["Bull_Candle"].fillna("Tight Base")
    b_cand["Score"] = (b_cand["Vol_Ratio"] * 28.0) + np.where(b_cand["Sec_Bull_Turn"], 35.0, 0.0) + ((1.0 - b_cand["Body_Pct"]) * 22.0)
    bull8 = b_cand.sort_values("Score", ascending=False).head(8).copy()
    bull8["Reason"] = bull8["Bull_Candle"].astype(str) + " • Vol " + bull8["Vol_Ratio"].astype(str) + "x • Sec 1M " + bull8["Sec_1M"].astype(str) + "%→Up"
    bull8["Entry"], bull8["SL"], bull8["Target"] = bull8["Buy_Entry"], bull8["Buy_SL"], bull8["Buy_Target"]

    used = set(bull8["Ticker"].tolist())
    br_cand = df[(~df["Ticker"].isin(used)) & (df["Consec_Down"] <= 2) & (df["1D"] <= 0.3) & (df["1D"] >= -3.8) & (df["Vol_Ratio"] >= 1.08)].copy()
    br_cand["Bear_Candle"] = br_cand["Bear_Candle"].fillna("Supply Stall")
    br_cand["Score"] = (br_cand["Vol_Ratio"] * 28.0) + np.where(br_cand["Sec_Bear_Roll"], 35.0, 0.0) + ((1.0 - br_cand["Body_Pct"]) * 22.0)
    bear8 = br_cand.sort_values("Score", ascending=False).head(8).copy()
    bear8["Reason"] = bear8["Bear_Candle"].astype(str) + " • Vol " + bear8["Vol_Ratio"].astype(str) + "x • Top Rejection"
    bear8["Entry"], bear8["SL"], bear8["Target"] = bear8["Short_Entry"], bear8["Short_SL"], bear8["Short_Target"]
    return bull8, bear8

def style_colored_table(df: pd.DataFrame, pct_cols: list):
    def color_pct(val):
        if pd.isna(val) or not isinstance(val, (int, float, np.number)):
            return ""
        return "color:#10b981;font-weight:700;" if val > 0 else ("color:#ef4444;font-weight:700;" if val < 0 else "color:#94a3b8;")
    return df.style.map(color_pct, subset=[c for c in pct_cols if c in df.columns]).format(precision=2)

with st.spinner(f"⚡ Scanning {len(ALL_TICKERS)}+ Nifty 500 Stocks across {len(SECTOR_STOCKS)} Sectors..."):
    pulse = load_pulse_indices()
    stocks_df, sectors_df = load_full_market_data()

if stocks_df.empty or sectors_df.empty:
    st.error("⚠️ Market data temporarily unavailable. Please click Refresh.")
    st.stop()

# ==============================================================================
# 7. MARKET PULSE RIBBON & AI COMPASS
# ==============================================================================
n_d, b_d, v_d, u_d = pulse["NIFTY"], pulse["BANKNIFTY"], pulse["VIX"], pulse["USDINR"]
adv_today, dec_today = int((stocks_df["1D"] > 0).sum()), int((stocks_df["1D"] < 0).sum())

if n_d["1D"] >= 0.20 and adv_today >= dec_today:
    c_txt, c_sty = "🟢 Bullish Bias — Track Turnaround BUY Setups", "background:rgba(16,185,129,0.16);color:#10b981;border:1px solid #10b98155;"
elif n_d["1D"] <= -0.20 and dec_today > adv_today:
    c_txt, c_sty = "🔴 Bearish Bias — Track Top SHORT Setups", "background:rgba(239,68,68,0.16);color:#ef4444;border:1px solid #ef444455;"
else:
    c_txt, c_sty = "⚖️ Rotational Market — Focus on Turnaround Sectors", "background:rgba(245,158,11,0.16);color:#f59e0b;border:1px solid #f59e0b55;"

st.markdown(
    f'<div class="pulse-bar">'
    f'<div class="pulse-item">🇮🇳 Nifty 50: <span style="color:{"#10b981" if n_d["1D"]>=0 else "#ef4444"};">{n_d["price"]:,.1f} ({n_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">🏛️ Bank Nifty: <span style="color:{"#10b981" if b_d["1D"]>=0 else "#ef4444"};">{b_d["price"]:,.1f} ({b_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">⚡ India VIX: <span style="color:#10b981;">{v_d["price"]:.2f} ({v_d["1D"]:+.2f}%)</span></div>'
    f'<div class="pulse-item">💵 USD/INR: <span style="color:#f59e0b;">₹{u_d["price"]:.2f}</span></div>'
    f'<div class="compass-pill" style="{c_sty}">🧭 {c_txt}</div></div>',
    unsafe_allow_html=True
)

# ==============================================================================
# 8. 5-COLUMN FILTER & ACTION BAR (WITH NSE HEATMAP & AI HELP BUTTONS)
# ==============================================================================
fc1, fc2, fc3, fc4, fc5 = st.columns([1.1, 2.3, 2.5, 2.4, 1.7])
with fc1:
    tf_choice = st.selectbox("📅 1. Timeframe:", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=0)
with fc2:
    sort_choice = st.selectbox(
        "🔄 2. Sort Sectors By:",
        [
            "🔄 Bottom Turnaround First",
            "🚀 Top Gainers First",
            "📉 Top Losers First",
            "🔥 High Volume First",
            "🎛️ Meter Score"
        ],
        index=0
    )
with fc3:
    sec_list = [DEFAULT_SECTOR] + sorted(list(SECTOR_STOCKS.keys()))
    picked_sec = st.selectbox("🔍 3. Select Sector (42 Sectors):", sec_list, index=sec_list.index(st.session_state.selected_sector) if st.session_state.selected_sector in sec_list else 0)
    if picked_sec != st.session_state.selected_sector:
        st.session_state.selected_sector = picked_sec
        st.rerun()
with fc4:
    stock_search_list = [DEFAULT_STOCK] + [f"{r['Symbol']} ({r['Sector']})" for _, r in stocks_df.sort_values("Symbol").iterrows()]
    st_idx = next((i for i, s in enumerate(stock_search_list) if st.session_state.selected_stock != DEFAULT_STOCK and s.startswith(f"{st.session_state.selected_stock.replace('.NS','')} (")), 0)
    picked_stock = st.selectbox("⚡ 4. Search Any Stock:", stock_search_list, index=st_idx)
    new_stk = picked_stock.split(" (")[0].strip() + ".NS" if picked_stock != DEFAULT_STOCK else DEFAULT_STOCK
    if new_stk != st.session_state.selected_stock:
        st.session_state.selected_stock = new_stk
        st.session_state.scroll_target = "stock-inspector-anchor"
        st.rerun()
with fc5:
    st.markdown("<div style='padding-top:23px;'></div>", unsafe_allow_html=True)
    if st.button("🗺️ NSE Heatmap & Verdict", use_container_width=True, help="Open NSE Sector Heatmap Grid & Bullish/Bearish Sector Recommendations"):
        st.session_state.show_nse_heatmap = not st.session_state.show_nse_heatmap

# ==============================================================================
# 8.1 INTERACTIVE AI HELP ASSISTANT PANEL (LIVE PROMPT + GEMINI LINK)
# ==============================================================================
turnaround_secs = sectors_df.sort_values(["Sec_Bull_Turn", "Turnaround_Score"], ascending=[False, False]).head(8)
bull_next8, bear_next8 = filter_next_day_intraday_stocks(stocks_df)

if st.session_state.show_ai_helper:
    top_turn_names = ", ".join([f"{r['Sector']} ({r['1D']:+.1f}%)" for _, r in turnaround_secs.head(4).iterrows()])
    top_bull_syms = ", ".join([f"{r['Symbol']} (₹{r['Price']}, Buy>{r['Entry']}, SL {r['SL']})" for _, r in bull_next8.head(4).iterrows()])
    top_bear_syms = ", ".join([f"{r['Symbol']} (₹{r['Price']}, Short<{r['Entry']}, SL {r['SL']})" for _, r in bear_next8.head(3).iterrows()])
    sel_stk_txt = ""
    if st.session_state.selected_stock != DEFAULT_STOCK and st.session_state.selected_stock in stocks_df["Ticker"].values:
        sr = stocks_df[stocks_df["Ticker"] == st.session_state.selected_stock].iloc[0]
        sel_stk_txt = f"\nSelected Stock Focus: {sr['Symbol']} ({sr['Sector']}) at ₹{sr['Price']} (1D: {sr['1D']:+.2f}%, RSI: {sr['RSI']}, Vol: {sr['Vol_Ratio']}x, Buy>{sr['Buy_Entry']}, SL:{sr['Buy_SL']}, Tgt:{sr['Buy_Target']})."

    live_ai_prompt = (
        f"বন্ধু, আজকের লাইভ মার্কেট ডেটা দেখো:\n"
        f"• Nifty 50: {n_d['price']:,.1f} ({n_d['1D']:+.2f}%), Bank Nifty: {b_d['price']:,.1f} ({b_d['1D']:+.2f}%), India VIX: {v_d['price']:.2f}\n"
        f"• Top Turnaround Sectors: {top_turn_names}\n"
        f"• Top Bullish Intraday Picks: {top_bull_syms}\n"
        f"• Top Bearish Intraday Picks: {top_bear_syms}{sel_stk_txt}\n"
        f"এই ডেটা অনুযায়ী এখন লাইভ মার্কেটে কোন সেক্টর ও কোন শেয়ারটিতে ট্রেড নেওয়া সবচেয়ে নিরাপদ হবে আমাকে গাইড করো।"
    )
    with st.container():
        st.markdown('<div class="aligned-sec-hdr">🤖 AI Live Market Assistant — Copy Live Market Summary & Chat with Gemini</div>', unsafe_allow_html=True)
        ai_c1, ai_c2, ai_c3 = st.columns([6.5, 2.0, 1.5])
        with ai_c1:
            st.code(live_ai_prompt, language="markdown")
        with ai_c2:
            st.link_button("💬 Open Gemini AI Chat", "https://gemini.google.com/app", use_container_width=True)
            st.caption("উপরের বক্সের ডানদিকের Copy আইকনে ক্লিক করে মেসেজটি কপি করে Gemini চ্যাটে পেস্ট করো।")
        with ai_c3:
            if st.button("✖ Close AI Help", use_container_width=True):
                st.session_state.show_ai_helper = False
                st.rerun()

# ==============================================================================
# 8.2 NSE SECTORAL HEATMAP & BULLISH / BEARISH SECTOR RECOMMENDATION PANEL
# ==============================================================================
if st.session_state.show_nse_heatmap:
    bull_secs_df = sectors_df[(sectors_df[tf_choice] > 0.25) & (sectors_df["RSI"] >= 50)].sort_values(tf_choice, ascending=False)
    turn_secs_df = sectors_df[sectors_df["Sec_Bull_Turn"]].sort_values("Turnaround_Score", ascending=False)
    bear_secs_df = sectors_df[sectors_df[tf_choice] < -0.15].sort_values(tf_choice, ascending=True)

    def get_nse_tile_color(val: float) -> str:
        if val >= 3.0:
            return "#047857"   # Dark Green (+3% to +5%)
        elif val >= 1.0:
            return "#10b981"   # Medium Green (+1% to +3%)
        elif val >= 0.0:
            return "#34d399"   # Light Green (0% to +1%)
        elif val >= -1.0:
            return "#f87171"   # Light Pink/Red (0% to -1%)
        elif val >= -3.0:
            return "#ef4444"   # Medium Red (-1% to -3%)
        else:
            return "#b91c1c"   # Dark Red (<-3%)

    heatmap_tiles = []
    for _, srow in sectors_df.sort_values(tf_choice, ascending=False).iterrows():
        v_pct = safe_num(srow[tf_choice], 0.0)
        bg_c = get_nse_tile_color(v_pct)
        q_sec = urllib.parse.quote(srow["Sector"])
        verdict_tag = "🟢 BULL" if v_pct > 0.3 else ("🔄 TURN" if srow["Sec_Bull_Turn"] else ("🔴 BEAR" if v_pct < -0.2 else "⚖️ FLAT"))
        heatmap_tiles.append(
            f'<a href="?focus_sec={q_sec}" target="_self" class="nse-tile" style="background:{bg_c};" title="Click to inspect {srow["Sector"]} stocks | Top Pick: {srow["Top_Pick"]}">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<span class="nse-tile-name">{srow["Sector"]}</span>'
            f'<span style="font-size:0.62rem;background:rgba(0,0,0,0.28);padding:1px 5px;border-radius:4px;font-weight:800;">{verdict_tag}</span>'
            f'</div>'
            f'<div class="nse-tile-bot">'
            f'<span style="font-size:0.74rem;opacity:0.92;">⭐ {srow["Top_Pick"]}</span>'
            f'<span style="font-size:0.86rem;font-weight:800;">{v_pct:+.2f}%</span>'
            f'</div></a>'
        )

    hm_top1, hm_top2, hm_top3 = st.columns([6.2, 2.3, 1.5])
    with hm_top1:
        st.markdown(f"#### 🗺️ NSE Sectoral Indices Heatmap & AI Sector Verdict ({tf_choice})")
    with hm_top2:
        st.link_button("🌐 Official NSE India Heatmap", "https://www.nseindia.com/market-data/live-market-indices/heatmap", use_container_width=True)
    with hm_top3:
        if st.button("✖ Close Heatmap", use_container_width=True):
            st.session_state.show_nse_heatmap = False
            st.rerun()

    rec1, rec2, rec3 = st.columns(3)
    with rec1:
        bull_names = ", ".join([f"**{r['Sector']}** ({r[tf_choice]:+.1f}%)" for _, r in bull_secs_df.head(5).iterrows()]) or "None right now"
        st.success(f"🟢 **BULLISH SECTORS (Buy / Breakout Focus):**\n\n{bull_names}")
    with rec2:
        turn_names = ", ".join([f"**{r['Sector']}** (Score {r['Turnaround_Score']})" for _, r in turn_secs_df.head(5).iterrows()]) or "None right now"
        st.info(f"🔄 **BOTTOM TURNAROUND (Accumulate / Reversal):**\n\n{turn_names}")
    with rec3:
        bear_names = ", ".join([f"**{r['Sector']}** ({r[tf_choice]:+.1f}%)" for _, r in bear_secs_df.head(5).iterrows()]) or "None right now"
        st.error(f"🔴 **BEARISH SECTORS (Avoid Buying / Short Focus):**\n\n{bear_names}")

    st.markdown(
        f'<div class="nse-heatmap-container">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">'
        f'<span style="font-size:0.82rem;font-weight:800;color:{TEXT_MAIN};">📊 All {len(SECTOR_STOCKS)} Sectors Live Heatmap Grid (Click Any Tile to Open Sector Stocks)</span>'
        f'<div class="nse-legend-bar">'
        f'<span class="nse-leg-pill" style="background:#047857;">+3% to +5%</span>'
        f'<span class="nse-leg-pill" style="background:#10b981;">+1% to +3%</span>'
        f'<span class="nse-leg-pill" style="background:#34d399;">0% to +1%</span>'
        f'<span class="nse-leg-pill" style="background:#f87171;">0% to -1%</span>'
        f'<span class="nse-leg-pill" style="background:#ef4444;">-1% to -3%</span>'
        f'<span class="nse-leg-pill" style="background:#b91c1c;">&lt; -3%</span>'
        f'</div></div>'
        f'<div class="nse-heatmap-grid">{"".join(heatmap_tiles)}</div></div>',
        unsafe_allow_html=True
    )

# ==============================================================================
# 9. PRIORITY 1 (HERO FOCUS): SECTOR TURNAROUND RADAR
# ==============================================================================
turn_cards = []
for _, ts in turnaround_secs.iterrows():
    q_s = urllib.parse.quote(ts["Sector"])
    turn_cards.append(
        f'<a href="?focus_sec={q_s}" target="_self" class="turn-sec-card" title="{ts["Sector"]} — Click to view all stocks">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span class="t-sec-name">🔄 {ts["Sector"]}</span>'
        f'<span style="background:rgba(16,185,129,0.16);color:#10b981;padding:1px 6px;border-radius:5px;font-size:0.67rem;font-weight:800;">Score {ts["Turnaround_Score"]}</span>'
        f'</div>'
        f'<div style="font-size:0.72rem;color:{TEXT_SUB};font-family:\'JetBrains Mono\',monospace !important;">'
        f'1M:<b style="color:{"#10b981" if ts["1M"]>=0 else "#ef4444"};">{ts["1M"]:+.1f}%</b> ➔ '
        f'1W:<b style="color:{"#10b981" if ts["1W"]>=0 else "#ef4444"};">{ts["1W"]:+.1f}%</b> ➔ '
        f'1D:<b style="color:{"#10b981" if ts["1D"]>=0 else "#ef4444"};">{ts["1D"]:+.1f}%</b>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;font-size:0.70rem;color:#f59e0b;font-weight:700;">'
        f'<span>Vol: {ts["Avg_Vol"]}x | >20DMA: {ts["Breadth_20DMA"]}%</span>'
        f'<span>⭐ {ts["Top_Pick"]}</span>'
        f'</div></a>'
    )

st.markdown(
    f'<div class="turnaround-hero-box">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">'
    f'<span style="font-size:0.88rem;font-weight:800;color:#10b981;">🧭 PRIORITY 1 — Sector Turnaround Radar (Bottoming Out Sectors Reversing Up with Volume)</span>'
    f'<span style="font-size:0.72rem;color:{TEXT_SUB};">Click any sector card to inspect its stocks</span>'
    f'</div>'
    f'<div class="turnaround-grid">{"".join(turn_cards)}</div></div>',
    unsafe_allow_html=True
)

# ==============================================================================
# 10. PRIORITY 2 (HIDDEN BY DEFAULT): NEXT-DAY INTRADAY WATCHLIST + REASONS
# ==============================================================================
wa_lines = ["🧭 *AlphaPulse Pro — Next-Day Intraday Watchlist*", "🟢 *Bullish Turnaround Stocks:*"]
for _, r in bull_next8.head(4).iterrows():
    wa_lines.append(f"• *{r['Symbol']}* (₹{r['Price']}) | Buy: ₹{r['Entry']} | SL: ₹{r['SL']} | Tgt: ₹{r['Target']} [{r['Bull_Candle']}]")
wa_lines.append("\n🔴 *Bearish Rejection Stocks:*")
for _, r in bear_next8.head(4).iterrows():
    wa_lines.append(f"• *{r['Symbol']}* (₹{r['Price']}) | Short: ₹{r['Entry']} | SL: ₹{r['SL']} | Tgt: ₹{r['Target']} [{r['Bear_Candle']}]")
wa_direct_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(chr(10).join(wa_lines))}"

with st.expander("🎯 PRIORITY 2 — Next-Day Intraday Watchlist (Bullish Turnaround & Bearish Rejection + Reasons) — Click to Expand", expanded=False):
    nd_c1, nd_c2 = st.columns([7.2, 2.8])
    with nd_c1:
        nd_bias = st.radio("View:", ["🌗 Both Bullish & Bearish", "🟢 Bullish Only", "🔴 Bearish Only"], horizontal=True, label_visibility="collapsed")
    with nd_c2:
        st.markdown(f'<div style="text-align:right;"><a href="{wa_direct_url}" target="_blank" class="wa-share-btn">📲 Send to WhatsApp</a></div>', unsafe_allow_html=True)

    def build_nextday_box(df_sub: pd.DataFrame, is_bull: bool) -> str:
        cards = []
        for _, r in df_sub.iterrows():
            qt = urllib.parse.quote(str(r["Ticker"]))
            tag_cls = "r-tag-bull" if is_bull else "r-tag-bear"
            tag_txt = f"🟢 BUY • {r['Confidence']}%" if is_bull else f"🔴 SHORT • {r['Confidence']}%"
            c_col = "#10b981" if r["1D"] >= 0 else "#ef4444"
            lbl = "Buy" if is_bull else "Short"
            cards.append(
                f'<a href="?focus_stock={qt}" target="_self" class="radar-row-card" title="{r["Symbol"]} ({r["Sector"]}) — {r["Reason"]}">'
                f'<div class="r-top"><span class="r-sym">{r["Symbol"]} <span style="font-size:0.70rem;color:{TEXT_SUB};font-weight:600;">({r["Sector"]})</span></span><span class="{tag_cls}">{tag_txt}</span></div>'
                f'<div class="r-mid"><span>₹{r["Price"]:,.1f} <span style="color:{c_col};font-weight:700;">({r["1D"]:+.1f}%)</span></span><span>RSI: {r["RSI"]} | Vol: {r["Vol_Ratio"]:.1f}x</span></div>'
                f'<div class="r-reason-box">💡 {r["Reason"]}</div>'
                f'<div class="r-plan"><span style="color:#f59e0b;">🎯 {lbl}: ₹{r["Entry"]}</span><span style="color:#ef4444;">🛑 SL: ₹{r["SL"]}</span><span style="color:#10b981;">🚀 Tgt: ₹{r["Target"]}</span></div>'
                f'</a>'
            )
        p_cls = "radar-panel-bull" if is_bull else "radar-panel-bear"
        h_col = "#10b981" if is_bull else "#ef4444"
        h_txt = "🟢 Bullish Next-Day Picks (Doji/Hammer + Turnaround)" if is_bull else "🔴 Bearish Next-Day Picks (Top Rejection + Supply)"
        return f'<div class="{p_cls}"><div class="radar-panel-header"><span style="color:{h_col};font-weight:800;font-size:0.82rem;">{h_txt}</span></div><div class="radar-grid">{"".join(cards)}</div></div>'

    if nd_bias == "🟢 Bullish Only":
        st.markdown(build_nextday_box(bull_next8, True), unsafe_allow_html=True)
    elif nd_bias == "🔴 Bearish Only":
        st.markdown(build_nextday_box(bear_next8, False), unsafe_allow_html=True)
    else:
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.markdown(build_nextday_box(bull_next8.head(6), True), unsafe_allow_html=True)
        with b_col2:
            st.markdown(build_nextday_box(bear_next8.head(6), False), unsafe_allow_html=True)

# ==============================================================================
# 11. CLICKABLE 42-SECTOR MARQUEE BAR
# ==============================================================================
bar_items = [
    f'<a class="{"sec-pill-up" if sr[tf_choice]>=0 else "sec-pill-down"}" href="?focus_sec={urllib.parse.quote(sr["Sector"])}" target="_self">'
    f'{"🟢" if sr[tf_choice]>=0 else "🔴"} {sr["Sector"]}: {"▲" if sr[tf_choice]>=0 else "▼"} {sr[tf_choice]:+.2f}% 🔍</a>'
    for _, sr in sectors_df.sort_values("Turnaround_Score" if "Bottom Turnaround" in sort_choice else tf_choice, ascending=False).iterrows()
]
st.markdown(f'<div class="marquee-wrap"><div class="marquee-track">{"".join(bar_items) * 2}</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 12. STOCK INSPECTOR, 5-POINT CHECKLIST & SMART CHART
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
    is_bear_setup = ("Short" in s_info["Action_Signal"]) or (s_info["1D"] < -0.3 and pd.notna(s_info["Bear_Candle"]))
    safe_qty = max(int(500.0 / max(abs(s_info["Buy_Entry"] - s_info["Buy_SL"]), 1.0)), 1)

    chk_trend, chk_vol, chk_rsi, chk_sec, chk_streak = s_info["Above_50DMA"], s_info["Vol_Ratio"] >= 1.15, (42.0 <= s_info["RSI"] <= 72.0), (s_info["Sec_1D"] >= -0.15), (s_info["Consec_Up"] <= 2)
    passed_cnt = sum([chk_trend, chk_vol, chk_rsi, chk_sec, chk_streak])

    single_wa_txt = urllib.parse.quote(
        f"🎯 *AlphaPulse Setup: {sym_clean}* ({s_info['Sector']})\n"
        f"• Price: ₹{p_now} ({s_info['1D']:+.2f}%) | Safety: {passed_cnt}/5\n"
        f"🟢 Buy: ₹{s_info['Buy_Entry']} | SL: ₹{s_info['Buy_SL']} | Tgt: ₹{s_info['Buy_Target']}\n"
        f"🔴 Short: ₹{s_info['Short_Entry']} | SL: ₹{s_info['Short_SL']} | Tgt: ₹{s_info['Short_Target']}"
    )

    st.markdown("---")
    sp1, sp2, sp3 = st.columns([6.2, 2.0, 1.8])
    with sp1:
        st.markdown(f"#### 🎯 Stock Inspector: **{sym_clean}** (`{s_info['Sector']}`) — ₹{p_now:,.2f} ({s_info['1D']:+.2f}% | {s_info['Action_Signal']})")
    with sp2:
        st.markdown(f'<a href="https://api.whatsapp.com/send?text={single_wa_txt}" target="_blank" class="wa-share-btn">📲 WhatsApp Setup</a>', unsafe_allow_html=True)
    with sp3:
        if st.button("✖ Close Chart", key="close_stk", use_container_width=True):
            st.session_state.selected_stock = DEFAULT_STOCK
            st.session_state.scroll_target = None
            st.rerun()

    lv1, lv2, lv3 = st.columns(3)
    with lv1:
        st.info(
            f"🛡️ **Safety Checklist ({passed_cnt}/5 Passed):**\n\n"
            f"{'✅' if chk_trend else '⚠️'} >50-DMA | {'✅' if chk_vol else '⚠️'} Vol ({s_info['Vol_Ratio']}x) | "
            f"{'✅' if chk_rsi else '⚠️'} RSI ({s_info['RSI']}) | {'✅' if chk_streak else '⚠️'} Fresh Base\n\n"
            f"📦 **Safe Qty (₹500 Risk):** `{safe_qty} Shares`"
        )
    with lv2:
        st.success(f"🟢 **Bullish Buy Plan:**\n\n• **Buy Above:** ₹{s_info['Buy_Entry']} | **SL:** ₹{s_info['Buy_SL']}\n\n• **Target 1:** ₹{round(s_info['Buy_Entry'] + 1.2*atr_v, 2)} | **Target 2:** ₹{s_info['Buy_Target']}")
    with lv3:
        st.error(f"🔴 **Bearish Short Plan:**\n\n• **Short Below:** ₹{s_info['Short_Entry']} | **SL:** ₹{s_info['Short_SL']}\n\n• **Target 1:** ₹{round(s_info['Short_Entry'] - 1.2*atr_v, 2)} | **Target 2:** ₹{s_info['Short_Target']}")

    ohlc_df = load_single_stock_ohlc(s_info["Ticker"])
    if not ohlc_df.empty and len(ohlc_df) >= 20:
        ohlc_df["DMA20"], ohlc_df["DMA50"] = ohlc_df["Close"].rolling(20).mean(), ohlc_df["Close"].rolling(50).mean()
        sub_df = ohlc_df.tail(70)
        fig_st = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.74, 0.26])
        fig_st.add_trace(go.Candlestick(x=sub_df.index, open=sub_df["Open"], high=sub_df["High"], low=sub_df["Low"], close=sub_df["Close"], name="Price"), row=1, col=1)
        fig_st.add_trace(go.Scatter(x=sub_df.index, y=sub_df["DMA20"], mode="lines", name="20 DMA", line=dict(color="#38bdf8", width=1.5)), row=1, col=1)
        fig_st.add_trace(go.Scatter(x=sub_df.index, y=sub_df["DMA50"], mode="lines", name="50 DMA", line=dict(color="#f59e0b", width=1.5)), row=1, col=1)

        if is_bear_setup:
            fig_st.add_hline(y=s_info["Short_Entry"], line_dash="dot", line_color="#f59e0b", annotation_text=f"Short: ₹{s_info['Short_Entry']}", row=1, col=1)
            fig_st.add_hline(y=s_info["Short_SL"], line_dash="dash", line_color="#ef4444", annotation_text=f"SL: ₹{s_info['Short_SL']}", row=1, col=1)
            fig_st.add_hline(y=s_info["Short_Target"], line_dash="dash", line_color="#10b981", annotation_text=f"Target: ₹{s_info['Short_Target']}", row=1, col=1)
        else:
            fig_st.add_hline(y=s_info["Buy_Entry"], line_dash="dot", line_color="#38bdf8", annotation_text=f"Buy: ₹{s_info['Buy_Entry']}", row=1, col=1)
            fig_st.add_hline(y=s_info["Buy_SL"], line_dash="dash", line_color="#ef4444", annotation_text=f"SL: ₹{s_info['Buy_SL']}", row=1, col=1)
            fig_st.add_hline(y=s_info["Buy_Target"], line_dash="dash", line_color="#10b981", annotation_text=f"Target: ₹{s_info['Buy_Target']}", row=1, col=1)

        fig_st.add_trace(go.Bar(x=sub_df.index, y=sub_df["Volume"], name="Volume", marker_color=["#10b981" if c >= o else "#ef4444" for c, o in zip(sub_df["Close"], sub_df["Open"])]), row=2, col=1)
        fig_st.update_layout(height=360, template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=20, b=10), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig_st, use_container_width=True)

    l1, l2, l3, l4 = st.columns(4)
    with l1:
        st.link_button(f"📈 TradingView ({sym_clean})", f"https://in.tradingview.com/chart/?symbol=NSE%3A{sym_clean}", use_container_width=True)
    with l2:
        st.link_button(f"📊 Screener.in ({sym_clean})", f"https://www.screener.in/company/{sym_clean}/", use_container_width=True)
    with l3:
        st.link_button(f"📰 Google Finance ({sym_clean})", f"https://www.google.com/finance/quote/{sym_clean}:NSE", use_container_width=True)
    with l4:
        st.link_button(f"🤖 Ask Gemini About {sym_clean}", "https://gemini.google.com/app", use_container_width=True)
    st.markdown("---")

# ==============================================================================
# 13. 4 SUMMARY KPI CARDS & DRILL-DOWN PANEL
# ==============================================================================
adv_count, dec_count = int((stocks_df[tf_choice] > 0).sum()), int((stocks_df[tf_choice] < 0).sum())
pct_50dma = round((stocks_df["Above_50DMA"].sum() / max(len(stocks_df), 1)) * 100.0, 1)
top_turn_sec = turnaround_secs.iloc[0]
leader_sec = sectors_df.sort_values(tf_choice, ascending=False).iloc[0]
nifty_tf = n_d.get(tf_choice, n_d["1W"])

kc1, kc2, kc3, kc4 = st.columns(4)
with kc1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Nifty 50 Benchmark ({tf_choice})</div><div class="kpi-val" style="color:{"#10b981" if nifty_tf>=0 else "#ef4444"};">{nifty_tf:+.2f}%</div><div class="kpi-sub-up">1W: {n_d["1W"]:+.2f}% | 1Y: {n_d["1Y"]:+.1f}%</div></div>', unsafe_allow_html=True)
    if st.button("📊 Top Gainers & Losers", key="k1", use_container_width=True):
        st.session_state.kpi_panel = None if st.session_state.kpi_panel == "nifty_movers" else "nifty_movers"
        st.session_state.scroll_target = "kpi-panel-anchor"
        st.rerun()
with kc2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Nifty 500 Breadth ({tf_choice})</div><div class="kpi-val"><span style="color:#10b981;">🟢 {adv_count} Up</span> | <span style="color:#ef4444;">🔴 {dec_count} Down</span></div><div class="kpi-sub-up">{pct_50dma}% Above 50-DMA</div></div>', unsafe_allow_html=True)
    if st.button("📈 Advancing vs Declining", key="k2", use_container_width=True):
        st.session_state.kpi_panel = None if st.session_state.kpi_panel == "breadth_list" else "breadth_list"
        st.session_state.scroll_target = "kpi-panel-anchor"
        st.rerun()
with kc3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">#1 Turnaround Sector</div><div class="kpi-val">🔄 {top_turn_sec["Sector"]}</div><div class="kpi-sub-up">Score: {top_turn_sec["Turnaround_Score"]} | 1D: {top_turn_sec["1D"]:+.2f}%</div></div>', unsafe_allow_html=True)
    if st.button("🔍 Inspect Turnaround Leader", key="k3", use_container_width=True):
        st.session_state.selected_sector, st.session_state.kpi_panel, st.session_state.scroll_target = top_turn_sec["Sector"], "turn_sec", "kpi-panel-anchor"
        st.rerun()
with kc4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Top Momentum Sector ({tf_choice})</div><div class="kpi-val">👑 {leader_sec["Sector"]}</div><div class="kpi-sub-up">▲ {leader_sec[tf_choice]:+.2f}% (Meter: {leader_sec["Meter"]})</div></div>', unsafe_allow_html=True)
    if st.button("🔍 Inspect Momentum Leader", key="k4", use_container_width=True):
        st.session_state.selected_sector, st.session_state.kpi_panel, st.session_state.scroll_target = leader_sec["Sector"], "leader_sec", "kpi-panel-anchor"
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
            st.markdown(f'<div class="aligned-sec-hdr">🚀 Top 15 Gainers ({tf_choice})</div>', unsafe_allow_html=True)
            g15 = stocks_df.sort_values(tf_choice, ascending=False).head(15)
            st.dataframe(style_colored_table(g15[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "Action_Signal"]], ["1D", "1W"]), use_container_width=True, hide_index=True)
            st.markdown(make_stock_pills(g15), unsafe_allow_html=True)
        with mv2:
            st.markdown(f'<div class="aligned-sec-hdr">📉 Top 15 Losers ({tf_choice})</div>', unsafe_allow_html=True)
            l15 = stocks_df.sort_values(tf_choice, ascending=True).head(15)
            st.dataframe(style_colored_table(l15[["Symbol", "Sector", "Price", "1D", "1W", "Vol_Ratio", "Action_Signal"]], ["1D", "1W"]), use_container_width=True, hide_index=True)
            st.markdown(make_stock_pills(l15), unsafe_allow_html=True)
    elif st.session_state.kpi_panel == "breadth_list":
        br1, br2 = st.columns(2)
        with br1:
            st.markdown('<div class="aligned-sec-hdr">🟢 Strong Advancing Stocks</div>', unsafe_allow_html=True)
            up15 = stocks_df[stocks_df[tf_choice] > 0].sort_values("Vol_Ratio", ascending=False).head(15)
            st.dataframe(style_colored_table(up15[["Symbol", "Sector", "Price", "1D", "Vol_Ratio", "Action_Signal"]], ["1D"]), use_container_width=True, hide_index=True)
            st.markdown(make_stock_pills(up15), unsafe_allow_html=True)
        with br2:
            st.markdown('<div class="aligned-sec-hdr">🔴 Declining / Oversold Watchlist</div>', unsafe_allow_html=True)
            dn15 = stocks_df[stocks_df[tf_choice] < 0].sort_values("Vol_Ratio", ascending=False).head(15)
            st.dataframe(style_colored_table(dn15[["Symbol", "Sector", "Price", "1D", "Vol_Ratio", "Action_Signal"]], ["1D"]), use_container_width=True, hide_index=True)
            st.markdown(make_stock_pills(dn15), unsafe_allow_html=True)
    else:
        sec_f = st.session_state.selected_sector
        st.markdown(f'<div class="aligned-sec-hdr">🔍 Sector Stocks & Trade Plans: {sec_f}</div>', unsafe_allow_html=True)
        sub_s = stocks_df[stocks_df["Sector"] == sec_f].sort_values(tf_choice, ascending=False)
        st.dataframe(style_colored_table(sub_s[["Symbol", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "Action_Signal", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W", "1M"]), use_container_width=True, hide_index=True)
        st.markdown(make_stock_pills(sub_s), unsafe_allow_html=True)
    st.markdown("---")

# ==============================================================================
# 14. 4 CONSOLIDATED TABS (CLEAN GAUGES & ZERO OVERLAP EXPANDERS)
# ==============================================================================
live_tab_badge = "🟢 LIVE" if is_mkt_open else "⏸️ Standby"
tab1, tab2, tab3, tab4 = st.tabs([
    f"🔄 1. {len(SECTOR_STOCKS)} Sector Turnaround & Gauges",
    f"⚡ 2. Live Intraday Stock Finder ({live_tab_badge})",
    "💎 3. Swing & Positional Radar",
    f"📋 4. All {len(SECTOR_STOCKS)} Sectors Matrix"
])

with tab1:
    f_secs = sectors_df.copy()
    if st.session_state.selected_sector != DEFAULT_SECTOR:
        f_secs = f_secs[f_secs["Sector"] == st.session_state.selected_sector]
        if st.button(f"🔄 Show All {len(SECTOR_STOCKS)} Sectors"):
            st.session_state.selected_sector = DEFAULT_SECTOR
            st.rerun()

    if "Bottom Turnaround" in sort_choice:
        f_secs = f_secs.sort_values(["Sec_Bull_Turn", "Turnaround_Score"], ascending=[False, False]).reset_index(drop=True)
    elif "Top Gainers" in sort_choice:
        f_secs = f_secs.sort_values(tf_choice, ascending=False).reset_index(drop=True)
    elif "Top Losers" in sort_choice:
        f_secs = f_secs.sort_values(tf_choice, ascending=True).reset_index(drop=True)
    elif "High Volume" in sort_choice:
        f_secs = f_secs.sort_values("Avg_Vol", ascending=False).reset_index(drop=True)
    else:
        f_secs = f_secs.sort_values("Meter", ascending=False).reset_index(drop=True)

    def make_gauge(score: int, title_txt: str, ret_val: float):
        bar_col = "#00f5d4" if ("Cyber Neon" in theme_mode and score >= 60) else ("#10b981" if score >= 60 else ("#f59e0b" if score >= 38 else "#ef4444"))
        short_title = title_txt if len(title_txt) <= 32 else title_txt[:30] + ".."
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=score,
            number={"suffix": f" ({ret_val:+.1f}%)", "font": {"size": 14, "color": TEXT_MAIN}},
            title={"text": short_title, "font": {"size": 13, "color": TEXT_MAIN}},
            gauge={"axis": {"range": [0, 100], "tickwidth": 1}, "bar": {"color": bar_col, "thickness": 0.34}, "bordercolor": BORDER_C,
                   "steps": [{"range": [0, 38], "color": "rgba(239,68,68,0.16)"}, {"range": [38, 60], "color": "rgba(245,158,11,0.16)"}, {"range": [60, 100], "color": "rgba(16,185,129,0.16)"}]}
        ))
        fig.update_layout(height=172, margin=dict(l=16, r=16, t=44, b=10), paper_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_MAIN))
        return fig

    for row_start in range(0, len(f_secs), 2):
        row_cols = st.columns(2)
        for offset in range(2):
            idx = row_start + offset
            if idx >= len(f_secs):
                break
            s_row = f_secs.iloc[idx]
            s_name, s_ret, s_meter = s_row["Sector"], safe_num(s_row[tf_choice]), int(safe_num(s_row["Meter"], 50))
            s_stocks = stocks_df[stocks_df["Sector"] == s_name].sort_values(tf_choice, ascending=False)
            with row_cols[offset]:
                if show_analog_meter:
                    st.plotly_chart(make_gauge(s_meter, f"🧭 {s_name}", s_ret), use_container_width=True, key=f"g_{s_name}")
                short_exp_lbl = f"📂 {s_name} ({s_ret:+.1f}% • {s_row['Zone']} • Score {s_row['Turnaround_Score']})"
                with st.expander(short_exp_lbl, expanded=(len(f_secs) == 1)):
                    st.dataframe(style_colored_table(s_stocks[["Symbol", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "Action_Signal", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W", "1M"]), use_container_width=True, hide_index=True)
                    st.markdown(make_stock_pills(s_stocks), unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="aligned-sec-hdr">⚡ PRIORITY 3 — Live 15-Minute Intraday Stock Finder (Chartink Conditions)</div>', unsafe_allow_html=True)
    force_test_scan = False
    if not is_mkt_open:
        st.warning(
            f"⏸️ **Live Intraday Stock Finder is on Standby (Market Closed — {ist_now.strftime('%A %I:%M %p IST')}).** "
            "Automatically activates during live market hours (Mon–Fri, 9:15 AM – 3:30 PM IST)."
        )
        force_test_scan = st.checkbox("🔓 Preview Last Session's 15-Minute Scan Results", value=False)

    if is_mkt_open or force_test_scan:
        with st.spinner("⚡ Scanning 15m Candles, VWAP & Volume Spikes..."):
            bull_15m_df, bear_15m_df = run_chartink_15m_scanner(stocks_df)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="aligned-sec-hdr">🟢 15m Bullish Breakouts (Above VWAP & Prev High)</div>', unsafe_allow_html=True)
            st.dataframe(style_colored_table(bull_15m_df[["Symbol", "Sector", "Price", "VWAP", "Vol_Ratio", "RSI", "1D", "Entry", "SL", "Target"]], ["1D"]), use_container_width=True, hide_index=True)
            st.markdown(make_stock_pills(bull_15m_df), unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="aligned-sec-hdr">🔴 15m Bearish Breakdowns (Below VWAP & Prev Low)</div>', unsafe_allow_html=True)
            b15_disp = bear_15m_df.rename(columns={"Entry": "Short_Below"})
            st.dataframe(style_colored_table(b15_disp[["Symbol", "Sector", "Price", "VWAP", "Vol_Ratio", "RSI", "1D", "Short_Below", "SL", "Target"]], ["1D"]), use_container_width=True, hide_index=True)
            st.markdown(make_stock_pills(bear_15m_df), unsafe_allow_html=True)
    else:
        bull_15m_df = pd.DataFrame()

    st.markdown("---")
    st.markdown('<div class="aligned-sec-hdr">🧮 Smart Intraday Position Size & Risk Calculator</div>', unsafe_allow_html=True)
    def_ent = float(stocks_df[stocks_df["Ticker"] == st.session_state.selected_stock]["Buy_Entry"].iloc[0]) if st.session_state.selected_stock in stocks_df["Ticker"].values else 500.0
    def_sl = float(stocks_df[stocks_df["Ticker"] == st.session_state.selected_stock]["Buy_SL"].iloc[0]) if st.session_state.selected_stock in stocks_df["Ticker"].values else 490.0
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        cap_amt = st.number_input("💰 Total Capital (₹):", min_value=1000.0, value=50000.0, step=5000.0)
    with rc2:
        risk_pct = st.number_input("⚠️ Safe Risk %:", min_value=0.25, max_value=5.0, value=1.0, step=0.25)
    with rc3:
        ent_p = st.number_input("🎯 Entry Price (₹):", min_value=1.0, value=def_ent, step=1.0)
    with rc4:
        sl_p = st.number_input("🛑 Stop-Loss (₹):", min_value=0.5, value=def_sl, step=1.0)
    max_loss = cap_amt * (risk_pct / 100.0)
    diff = abs(ent_p - sl_p)
    st.success(f"✅ **Max Safe Loss:** ₹{max_loss:,.0f} &nbsp;|&nbsp; 📦 **Safe Quantity:** `{int(max_loss / diff) if diff > 0 else 0} Shares` &nbsp;|&nbsp; 🎯 **1:2 Target:** `₹{(ent_p + 2*diff if ent_p >= sl_p else ent_p - 2*diff):,.2f}`")

with tab3:
    sw1, sw2 = st.columns(2)
    with sw1:
        st.markdown('<div class="aligned-sec-hdr">🚀 Safe Trend Pullback Picks (>50-DMA & Near 20-DMA)</div>', unsafe_allow_html=True)
        sp_df = stocks_df[(stocks_df["Above_50DMA"]) & (stocks_df["Dist_20DMA"].between(-3.0, 4.5)) & (stocks_df["RSI"].between(44, 64))].sort_values("Vol_Ratio", ascending=False).head(18)
        st.dataframe(style_colored_table(sp_df[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W", "1M"]), use_container_width=True, hide_index=True, height=420)
        st.markdown(make_stock_pills(sp_df), unsafe_allow_html=True)
    with sw2:
        st.markdown('<div class="aligned-sec-hdr">🌱 Bottom Turnaround Value Picks (Oversold Recovery)</div>', unsafe_allow_html=True)
        vr_df = stocks_df[(stocks_df["1M"] < 0) & (stocks_df["1D"] > 0) & (stocks_df["RSI"] <= 52)].sort_values("Vol_Ratio", ascending=False).head(18)
        st.dataframe(style_colored_table(vr_df[["Symbol", "Sector", "Price", "1D", "1W", "1M", "Vol_Ratio", "RSI", "Buy_Entry", "Buy_SL", "Buy_Target"]], ["1D", "1W", "1M"]), use_container_width=True, hide_index=True, height=420)
        st.markdown(make_stock_pills(vr_df), unsafe_allow_html=True)
    st.markdown("---")
    st.download_button(f"📥 Download Complete {len(ALL_TICKERS)}+ Nifty 500 Stocks Report (CSV / Excel)", data=stocks_df.to_csv(index=False).encode("utf-8"), file_name="alphapulse_nifty500_report.csv", mime="text/csv", use_container_width=True)

with tab4:
    chart_secs = sectors_df.sort_values(tf_choice, ascending=True)
    fig_b = go.Figure(go.Bar(x=chart_secs[tf_choice], y=chart_secs["Sector"], orientation="h", marker_color=["#10b981" if v >= 0 else "#ef4444" for v in chart_secs[tf_choice]], text=[f"{v:+.2f}%" for v in chart_secs[tf_choice]], textposition="outside"))
    fig_b.update_layout(height=880, template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=40, t=15, b=10), font=dict(color=TEXT_MAIN))
    st.plotly_chart(fig_b, use_container_width=True)
    st.dataframe(style_colored_table(sectors_df.sort_values("Turnaround_Score", ascending=False)[["Sector", "Zone", "Turnaround_Score", "Meter", "1D", "1W", "1M", "3M", "6M", "1Y", "Avg_Vol", "RSI", "Breadth_20DMA", "Breadth_50DMA", "Top_Pick"]], ["1D", "1W", "1M", "3M", "6M", "1Y"]), use_container_width=True, hide_index=True)

# ==============================================================================
# 15. FLOATING RIGHT DOCK (‘🤖 AI Help’ + ‘🚀 Top’) & AUTO-SCROLL ENGINE
# ==============================================================================
st.markdown(
    '<div class="floating-right-dock">'
    '<a href="https://gemini.google.com/app" target="_blank" class="floating-ai-btn" title="Open Gemini AI Live Chat">🤖 AI Chat</a>'
    '<a href="#top-anchor" class="single-top-btn" id="alphapulse-top-btn" title="Scroll back to top">🚀 Top</a>'
    '</div>',
    unsafe_allow_html=True
)

scroll_target_id = st.session_state.scroll_target or ""
st.session_state.scroll_target = None
top_syms = ",".join(bull_15m_df["Symbol"].head(3).tolist()) if (is_mkt_open and not bull_15m_df.empty) else ""
should_ring = "true" if (auto_alert_on and is_mkt_open and top_syms and top_syms != st.session_state.last_alerted) else "false"
if auto_alert_on and is_mkt_open and top_syms:
    st.session_state.last_alerted = top_syms
reload_js = "setTimeout(function(){ window.parent.location.reload(); }, 180000);" if (auto_alert_on and is_mkt_open) else ""

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
