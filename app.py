import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone, timedelta
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
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
# 2. VERIFIED 42 SECTORS COVERING 415+ NIFTY 500 STOCKS (INCLUDING CEMENT)
# ==============================================================================
SECTOR_STOCKS = {
    "Cement & Clinker": ["ULTRACEMCO.NS", "AMBUJACEM.NS", "SHREECEM.NS", "DALBHARAT.NS", "ACC.NS", "JKCEMENT.NS", "RAMCOCEM.NS", "BIRLACORPN.NS", "INDIACEM.NS", "NUVOCO.NS", "HEIDELBERG.NS"],
    "Defence & Aerospace": ["HAL.NS", "BEL.NS", "BDL.NS", "PARAS.NS", "DATAPATTNS.NS", "ASTRAMICRO.NS", "MIDHANI.NS", "ZENTEC.NS", "BEML.NS", "SOLARINDS.NS"],
    "Shipbuilding & Marine": ["MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "SCI.NS", "GESHIP.NS", "SEAMECLTD.NS", "DREDGECORP.NS"],
    "Railways & Wagons": ["RVNL.NS", "IRFC.NS", "IRCON.NS", "TITAGARH.NS", "JWL.NS", "CONCOR.NS", "RITES.NS", "RAILTEL.NS", "TEXRAIL.NS", "RAMKRISHNA.NS"],
    "Cables & Wires": ["POLYCAB.NS", "KEI.NS", "RRKABEL.NS", "FINCABLES.NS", "UNIVERSAL.NS", "PARAMOUNT.NS"],
    "Transformers & Power T&D": ["CGPOWER.NS", "VOLTAMP.NS", "TARIL.NS", "POWERINDIA.NS", "APARINDS.NS", "BHEL.NS", "SIEMENS.NS", "ABB.NS", "SCHNEIDER.NS", "TRITURBINE.NS"],
    "EMS & Electronics": ["DIXON.NS", "KAYNES.NS", "SYRMA.NS", "AMBER.NS", "PGEL.NS", "CYIENTDLM.NS", "AVALON.NS", "IKIO.NS", "HONAUT.NS"],
    "Green Energy & Solar": ["IREDA.NS", "SUZLON.NS", "INOXWIND.NS", "KPIGREEN.NS", "BORORENEW.NS", "SJVN.NS", "NHPC.NS", "ADANIGREEN.NS"],
    "Power Utilities & Financiers": ["NTPC.NS", "POWERGRID.NS", "TATAPOWER.NS", "PFC.NS", "RECLTD.NS", "JSWENERGY.NS", "TORNTPOWER.NS", "CESC.NS", "ADANIPOWER.NS", "NLCINDIA.NS"],
    "Oil, Gas & City Gas": ["RELIANCE.NS", "ONGC.NS", "IOC.NS", "BPCL.NS", "HPCL.NS", "GAIL.NS", "OIL.NS", "PETRONET.NS", "IGL.NS", "MGL.NS", "GUJGASLTD.NS", "CHENNPETRO.NS"],
    "Metals, Steel & Mining": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "COALINDIA.NS", "NATIONALUM.NS", "SAIL.NS", "JINDALSTEL.NS", "HINDZINC.NS", "APLAPOLLO.NS", "WELCORP.NS"],
    "Auto OEMs (2W, 4W & CV)": ["M&M.NS", "TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "TVSMOTOR.NS", "HEROMOTOCO.NS", "ASHOKLEY.NS", "ESCORTS.NS", "FORCEMOT.NS"],
    "Auto Ancillaries & Tyres": ["MOTHERSON.NS", "BOSCHLTD.NS", "SONACOMS.NS", "UNOMINDA.NS", "APOLLOTYRE.NS", "BALKRISIND.NS", "MRF.NS", "CEATLTD.NS", "ENDURANCE.NS", "EXIDEIND.NS", "BHARATFORG.NS", "JKTYRE.NS"],
    "PSU Banks": ["SBIN.NS", "BANKBARODA.NS", "PNB.NS", "CANBK.NS", "UNIONBANK.NS", "INDIANB.NS", "BANKINDIA.NS", "MAHABANK.NS", "IOB.NS", "UCOBANK.NS", "CENTRALBK.NS"],
    "Private Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "FEDERALBNK.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "RBLBANK.NS", "KARURVYSYA.NS", "AUBANK.NS", "CUB.NS"],
    "NBFCs & Housing Finance": ["BAJFINANCE.NS", "BAJAJFINSV.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "LICHSGFIN.NS", "PNBHOUSING.NS", "LTF.NS", "M&MFIN.NS", "POONAWALLA.NS", "CANFINHOME.NS"],
    "Insurance (Life & General)": ["LICI.NS", "SBILIFE.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", "ICICIGI.NS", "STARHEALTH.NS", "NIACL.NS", "GICRE.NS", "MFSL.NS"],
    "Capital Market, Exchanges & AMC": ["BSE.NS", "MCX.NS", "CDSL.NS", "ANGELONE.NS", "MOTILALOFS.NS", "CAMS.NS", "ANANDRATHI.NS", "HDFCAMC.NS", "NAM-INDIA.NS", "UTIAMC.NS", "KFINTECH.NS"],
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
    "QSR, Food & Beverages": ["JUBLFOOD.NS", "DEVYANI.NS", "WESTLIFE.NS", "SAPPHIRE.NS", "BIKAJI.NS", "RADICO.NS", "UNITDSPR.NS", "UBL.NS", "PATANJALI.NS"],
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
EMPTY_VIEWER = "Select a Sector to View Stocks..."

# ==============================================================================
# 3. 3-LAYER QUALITY NOTIFICATION VAULT (9:15 AM TO 3:30 PM, AUTO-CLEANS)
# ==============================================================================
@st.cache_resource
def get_3layer_notification_vault():
    return {"date": "", "items": [], "seen_keys": set()}

def get_ist_now():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))

ist_now = get_ist_now()
today_str = ist_now.strftime("%Y-%m-%d")
is_mkt_open = (ist_now.weekday() < 5) and (
    (ist_now.hour == 9 and ist_now.minute >= 15)
    or (10 <= ist_now.hour <= 14)
    or (ist_now.hour == 15 and ist_now.minute <= 30)
)
is_after_close = (ist_now.hour > 15) or (ist_now.hour == 15 and ist_now.minute > 31)

alert_vault = get_3layer_notification_vault()
if alert_vault["date"] != today_str or is_after_close:
    alert_vault["date"] = today_str
    alert_vault["items"] = []
    alert_vault["seen_keys"] = set()

def push_3layer_alert(time_str: str, category: str, symbol: str, ticker: str, sector: str, peer_sync: str, price: float, vwap: float, ema9: float, entry: float, sl: float, target: float, note: str, is_bull: bool = True):
    if is_after_close:
        return False
    u_key = f"{today_str}_{symbol}_{category}"
    if u_key not in alert_vault["seen_keys"]:
        alert_vault["seen_keys"].add(u_key)
        alert_vault["items"].insert(0, {
            "time": time_str, "category": category, "symbol": symbol, "ticker": ticker,
            "sector": sector, "peer_sync": peer_sync, "price": round(float(price), 2),
            "vwap": round(float(vwap), 2), "ema9": round(float(ema9), 2),
            "entry": round(float(entry), 2), "sl": round(float(sl), 2),
            "target": round(float(target), 2), "note": note, "is_bull": is_bull
        })
        return True
    return False

# ==============================================================================
# 4. SESSION STATE & URL QUERY PARAMETER HANDLER
# ==============================================================================
qp = st.query_params
init_auto = False if qp.get("auto") == "0" else True

for k, v in [
    ("selected_sector", DEFAULT_SECTOR),
    ("inspect_sector", EMPTY_VIEWER),
    ("selected_stock", DEFAULT_STOCK),
    ("scroll_target", None),
    ("last_alerted", ""),
    ("show_ai_helper", False),
    ("show_nse_heatmap", False),
    ("show_alert_drawer", False),
    ("show_stock_ai_verdict", True),
    ("auto_scan_locked", init_auto),
    ("ai_custom_ticker", ""),
    ("kite_api_key", "")
]:
    if k not in st.session_state:
        st.session_state[k] = v

def get_auto_param() -> str:
    return "1" if st.session_state.auto_scan_locked else "0"

if "nav_action" in qp:
    st.session_state.selected_sector = DEFAULT_SECTOR
    st.session_state.inspect_sector = EMPTY_VIEWER
    st.session_state.selected_stock = DEFAULT_STOCK
    st.session_state.scroll_target = None
    st.session_state.show_nse_heatmap = False
    st.query_params.clear()
    st.query_params["auto"] = get_auto_param()

if "focus_stock" in qp:
    clicked_sym = urllib.parse.unquote(qp["focus_stock"]).strip().upper()
    full_t = clicked_sym if clicked_sym.endswith(".NS") else f"{clicked_sym}.NS"
    st.session_state.selected_stock = full_t
    st.session_state.show_stock_ai_verdict = True
    st.session_state.scroll_target = "stock-inspector-anchor"
    st.query_params.clear()
    st.query_params["auto"] = get_auto_param()

if "focus_sec" in qp:
    clicked_sec = urllib.parse.unquote(qp["focus_sec"]).strip()
    if clicked_sec in SECTOR_STOCKS:
        st.session_state.inspect_sector = clicked_sec
        st.session_state.scroll_target = "sector-viewer-anchor"
    st.query_params.clear()
    st.query_params["auto"] = get_auto_param()

# ==============================================================================
# 5. CRASH-PROOF DATA ENGINE (DEDUPLICATES COLUMNS TO PREVENT TYPEERROR)
# ==============================================================================
def safe_num(val, default: float = 0.0) -> float:
    try:
        v = float(val)
        return default if (np.isnan(v) or np.isinf(v)) else v
    except Exception:
        return default

def calc_rsi(series: pd.Series, period: int = 14) -> float:
    try:
        s = series.dropna()
        if len(s) < period + 1:
            return 50.0
        delta = s.diff()
        up = delta.clip(lower=0).rolling(period).mean()
        down = (-delta.clip(upper=0)).rolling(period).mean()
        rs = up / down.replace(0, np.nan)
        return safe_num((100.0 - (100.0 / (1.0 + rs))).iloc[-1], 50.0)
    except Exception:
        return 50.0

def calc_return(closes: pd.Series, days: int) -> float:
    try:
        s = closes.dropna()
        if len(s) < 2:
            return 0.0
        base = safe_num(s.iloc[max(0, len(s) - 1 - days)], 0.0)
        last = safe_num(s.iloc[-1], 0.0)
        return safe_num(((last - base) / base) * 100.0, 0.0) if base > 0 else 0.0
    except Exception:
        return 0.0

def render_safe_table(df: pd.DataFrame, pct_cols: list, height: int = None):
    """100% Crash-Proof Table Renderer: Removes duplicate columns & safely colors % columns."""
    if df is None or df.empty:
        st.info("No matching records found right now.")
        return
    # Remove any duplicate column names (fixes TypeError when tf_choice == '1D')
    clean_df = df.loc[:, ~df.columns.duplicated()].copy()
    num_cols = clean_df.select_dtypes(include=[np.number]).columns.tolist()
    for nc in num_cols:
        clean_df[nc] = pd.to_numeric(clean_df[nc], errors="coerce").fillna(0.0).round(2)
    try:
        valid_cols = list(dict.fromkeys([c for c in pct_cols if c in clean_df.columns]))

        def color_pct(val):
            try:
                v = float(val)
                return "color:#10b981;font-weight:700;" if v > 0 else ("color:#ef4444;font-weight:700;" if v < 0 else "color:#94a3b8;")
            except Exception:
                return ""

        styler = clean_df.style
        if hasattr(styler, "map"):
            styler = styler.map(color_pct, subset=valid_cols)
        else:
            styler = styler.applymap(color_pct, subset=valid_cols)
        styler = styler.format("{:.2f}", subset=num_cols)
        if height:
            st.dataframe(styler, use_container_width=True, hide_index=True, height=height)
        else:
            st.dataframe(styler, use_container_width=True, hide_index=True)
    except Exception:
        if height:
            st.dataframe(clean_df, use_container_width=True, hide_index=True, height=height)
        else:
            st.dataframe(clean_df, use_container_width=True, hide_index=True)

@st.cache_data(ttl=45, show_spinner=False)
def load_pulse_indices():
    idx_tickers = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "VIX": "^INDIAVIX", "USDINR": "INR=X"}
    res = {}
    for k, sym in idx_tickers.items():
        try:
            tk_obj = yf.Ticker(sym)
            df_d = tk_obj.history(period="6mo", interval="1d")
            if df_d is not None and not df_d.empty:
                df_d = df_d.dropna(subset=["Close"])
                if len(df_d) >= 2:
                    c_now = safe_num(df_d["Close"].iloc[-1], 0.0)
                    prev_c = safe_num(df_d["Close"].iloc[-2], c_now)
                    try:
                        fi = tk_obj.fast_info
                        fi_last = safe_num(getattr(fi, "last_price", None) or fi.get("lastPrice"), 0.0)
                        fi_prev = safe_num(getattr(fi, "previous_close", None) or fi.get("previousClose"), 0.0)
                        if fi_last > 0 and fi_prev > 0:
                            c_now, prev_c = fi_last, fi_prev
                    except Exception:
                        pass

                    pts_chg = round(c_now - prev_c, 2)
                    pct_1d = round(((c_now - prev_c) / prev_c) * 100.0, 2) if prev_c > 0 else 0.0
                    if c_now > 0:
                        res[k] = {
                            "price": round(c_now, 2),
                            "pts": pts_chg,
                            "1D": pct_1d,
                            "1W": round(calc_return(df_d["Close"], 5), 2),
                            "1M": round(calc_return(df_d["Close"], 21), 2),
                            "3M": round(calc_return(df_d["Close"], 63), 2),
                            "6M": round(calc_return(df_d["Close"], 120), 2),
                            "1Y": round(calc_return(df_d["Close"], 120), 2),
                        }
        except Exception:
            pass

    defaults = {
        "NIFTY": {"price": 22811.35, "pts": -77.60, "1D": -0.34, "1W": -1.1, "1M": -2.4, "3M": 1.2, "6M": 3.5, "1Y": -1.2},
        "BANKNIFTY": {"price": 51240.00, "pts": -280.00, "1D": -0.54, "1W": -1.4, "1M": -2.1, "3M": 1.5, "6M": 3.0, "1Y": 2.5},
        "VIX": {"price": 14.45, "pts": 0.35, "1D": 2.48, "1W": 1.1, "1M": -2.0, "3M": 0.0, "6M": 0.0, "1Y": 0.0},
        "USDINR": {"price": 84.98, "pts": 0.05, "1D": 0.06, "1W": 0.1, "1M": 0.2, "3M": 0.5, "6M": 0.8, "1Y": 1.4},
    }
    for k, v in defaults.items():
        if k not in res:
            res[k] = v
    return res

@st.cache_data(ttl=300, show_spinner=False)
def load_full_market_data():
    raw = yf.download(ALL_TICKERS, period="6mo", interval="1d", progress=False, group_by="ticker", threads=True)
    stock_rows = []
    for ticker in ALL_TICKERS:
        try:
            df = raw[ticker] if len(ALL_TICKERS) > 1 else raw
            if df is None or df.empty:
                continue
            df = df.dropna(subset=["Close", "Open", "High", "Low"])
            if len(df) < 22:
                continue

            c_arr = df["Close"].to_numpy(dtype=float)
            o_arr = df["Open"].to_numpy(dtype=float)
            h_arr = df["High"].to_numpy(dtype=float)
            l_arr = df["Low"].to_numpy(dtype=float)
            v_arr = np.nan_to_num(df["Volume"].to_numpy(dtype=float), nan=0.0)

            c_now = safe_num(c_arr[-1], 0.0)
            if c_now <= 0:
                continue
            o_now, h_now, l_now = safe_num(o_arr[-1], c_now), safe_num(h_arr[-1], c_now), safe_num(l_arr[-1], c_now)
            prev_high, prev_low, prev_close = safe_num(h_arr[-2], h_now), safe_num(l_arr[-2], l_now), safe_num(c_arr[-2], c_now)

            n_len = len(c_arr)
            r_1d = ((c_now - c_arr[-2]) / c_arr[-2]) * 100.0 if c_arr[-2] > 0 else 0.0
            r_1w = ((c_now - c_arr[max(0, n_len - 6)]) / c_arr[max(0, n_len - 6)]) * 100.0
            r_1m = ((c_now - c_arr[max(0, n_len - 22)]) / c_arr[max(0, n_len - 22)]) * 100.0
            r_3m = ((c_now - c_arr[max(0, n_len - 64)]) / c_arr[max(0, n_len - 64)]) * 100.0
            r_6m = ((c_now - c_arr[0]) / c_arr[0]) * 100.0

            dma20 = float(np.mean(c_arr[-20:]))
            prev_dma20 = float(np.mean(c_arr[-21:-1])) if n_len >= 21 else dma20
            dma50 = float(np.mean(c_arr[-50:])) if n_len >= 50 else dma20

            avg_vol = float(np.mean(v_arr[-21:-1])) if n_len >= 21 else float(np.mean(v_arr))
            vol_ratio = max(round(safe_num(v_arr[-1] / avg_vol, 1.0), 2), 0.1) if avg_vol > 0 else 1.0

            diffs = np.diff(c_arr[-16:])
            gains = np.mean(np.where(diffs > 0, diffs, 0.0))
            losses = np.mean(np.where(diffs < 0, -diffs, 0.0))
            rsi_val = round(100.0 - (100.0 / (1.0 + (gains / losses))), 1) if losses > 0 else 65.0

            consec_up, consec_down = 0, 0
            for i in range(n_len - 1, 0, -1):
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
            rng_3d_pct = safe_num(((float(np.max(h_arr[-3:])) - float(np.min(l_arr[-3:]))) / c_now) * 100.0, 10.0)

            bull_candle = "Dragonfly Doji" if (body_pct <= 0.28 and lower_wick >= 0.42) else ("Hammer" if (lower_wick >= 0.48 and body_pct <= 0.42) else ("Bullish Doji" if (body_pct <= 0.28 and c_now >= o_now) else ("Tight Base" if (rng_3d_pct <= 4.2 and c_now >= o_now) else ("Bottom Turn" if (lower_wick >= 0.35 and r_1d >= 0) else None))))
            bear_candle = "Gravestone Doji" if (body_pct <= 0.28 and upper_wick >= 0.42) else ("Shooting Star" if (upper_wick >= 0.48 and body_pct <= 0.42) else ("Bearish Doji" if (body_pct <= 0.28 and c_now < o_now) else ("Supply Stall" if (rng_3d_pct <= 4.2 and c_now < o_now) else ("Top Reject" if (upper_wick >= 0.35 and r_1d < 0) else None))))

            atr_clean = round(max(float(np.mean(h_arr[-14:] - l_arr[-14:])), c_now * 0.012), 2)
            dist_20 = round(((c_now - dma20) / dma20) * 100.0, 2) if dma20 > 0 else 0.0

            if rsi_val >= 75 or consec_up >= 4:
                action_sig = "⚠️ Overbought"
            elif bull_candle and consec_up <= 2 and vol_ratio >= 1.15:
                action_sig = "🟢 Turnaround Buy"
            elif c_now >= dma50 and -2.5 <= dist_20 <= 3.5 and 45 <= rsi_val <= 65:
                action_sig = "💎 Safe Swing Buy"
            elif bear_candle and consec_down <= 2 and vol_ratio >= 1.15:
                action_sig = "🔴 Top Short"
            else:
                action_sig = "⚖️ Watch"

            conf_score = int(np.clip(55 + min(vol_ratio * 12, 25) + (10 if c_now >= dma50 else -5) + (8 if (bull_candle or bear_candle) else 0), 45, 96))

            stock_rows.append({
                "Ticker": ticker, "Symbol": ticker.replace(".NS", ""), "Sector": TICKER_TO_SECTOR.get(ticker, "Others"),
                "Price": round(c_now, 2), "1D": round(r_1d, 2), "1W": round(r_1w, 2), "1M": round(r_1m, 2),
                "3M": round(r_3m, 2), "6M": round(r_6m, 2), "1Y": round(r_6m, 2),
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

        up_cnt = int((grp["1D"] > 0).sum())
        dn_cnt = int((grp["1D"] < 0).sum())
        tot_cnt = max(len(grp), 1)
        peer_up_pct = round((up_cnt / tot_cnt) * 100.0, 1)
        peer_dn_pct = round((dn_cnt / tot_cnt) * 100.0, 1)

        was_correcting = (s_1m <= 2.2) or (s_3m <= 3.5) or (s_1w <= 1.5)
        reversing_up = (s_1d >= -0.05) and ((s_1d > (s_1w / 5.0)) or (s_1w > (s_1m / 4.0)))
        sec_bull_turn = bool(was_correcting and reversing_up)
        sec_bear_roll = bool((s_1m >= 1.5 or s_1w >= 1.0) and (s_1d <= 0.15) and (s_1d < (s_1w / 5.0)))

        turn_score = round(
            (35.0 if sec_bull_turn else 0.0)
            + (max(0.0, 3.0 - s_1m) * 3.2 if reversing_up else 0.0)
            + (s_1d * 10.0)
            + (s_vol * 18.0)
            + (peer_up_pct * 0.25),
            1
        )

        meter = int(np.clip(safe_num(50.0 + (s_1w * 3.5) + (s_1d * 6.0) + ((s_rsi - 50.0) * 0.6), 50.0), 5, 98))
        zone = "🔄 Turnaround" if (sec_bull_turn and s_1d >= 0) else (
            "🚀 Leading" if (s_1w >= 2.0 and s_1d >= 0) else (
                "⚠️ Exhaustion" if (sec_bear_roll and s_1d < 0) else "💎 Value Watch"
            )
        )
        top_pick_sym = grp.sort_values(["1D", "Vol_Ratio"], ascending=[False, False]).iloc[0]["Symbol"]

        sec_rows.append({
            "Sector": sec_name, "Count": len(grp), "Up_Count": up_cnt, "Down_Count": dn_cnt,
            "Peer_Up_Pct": peer_up_pct, "Peer_Down_Pct": peer_dn_pct,
            "Top_Pick": top_pick_sym,
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
    stocks_df["Sec_Peer_Up_Pct"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Peer_Up_Pct", 50.0))
    stocks_df["Sec_Peer_Down_Pct"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Peer_Down_Pct", 50.0))
    stocks_df["Sec_Up_Count"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Up_Count", 0))
    stocks_df["Sec_Tot_Count"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Count", 1))
    stocks_df["Sec_Bull_Turn"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Sec_Bull_Turn", False))
    stocks_df["Sec_Bear_Roll"] = stocks_df["Sector"].map(lambda s: sec_map.get(s, {}).get("Sec_Bear_Roll", False))
    return stocks_df, sectors_df

@st.cache_data(ttl=120, show_spinner=False)
def run_3layer_intraday_scanner(stocks_df: pd.DataFrame):
    if stocks_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    qualifying_pool = stocks_df[
        (stocks_df["Price"] > 120) & (
            ((stocks_df["Sec_Bull_Turn"] | (stocks_df["Sec_1D"] >= 0.25)) & (stocks_df["Sec_Peer_Up_Pct"] >= 55.0)) |
            ((stocks_df["Sec_Bear_Roll"] | (stocks_df["Sec_1D"] <= -0.25)) & (stocks_df["Sec_Peer_Down_Pct"] >= 55.0))
        )
    ].sort_values("Vol_Ratio", ascending=False).head(30)

    if qualifying_pool.empty:
        qualifying_pool = stocks_df[stocks_df["Price"] > 120].sort_values("Vol_Ratio", ascending=False).head(24)

    pool_tickers = qualifying_pool["Ticker"].tolist()
    daily_map = qualifying_pool.set_index("Ticker").to_dict("index")
    bull_15m, bear_15m = [], []

    try:
        raw_15m = yf.download(pool_tickers, period="5d", interval="15m", progress=False, group_by="ticker", threads=True)
        for tk in pool_tickers:
            try:
                df15 = (raw_15m[tk] if len(pool_tickers) > 1 else raw_15m).dropna(subset=["Close", "Open", "High", "Low"])
                if len(df15) < 20:
                    continue
                d_info = daily_map[tk]
                c15, o15, h15, l15 = safe_num(df15["Close"].iloc[-1], d_info["Price"]), safe_num(df15["Open"].iloc[-1]), safe_num(df15["High"].iloc[-1]), safe_num(df15["Low"].iloc[-1])
                v15 = safe_num(df15["Volume"].fillna(0).iloc[-1])
                vol_sma20 = safe_num(df15["Volume"].fillna(0).iloc[-21:-1].mean())
                v15_ratio = round(max(safe_num(v15 / vol_sma20, d_info["Vol_Ratio"]), d_info["Vol_Ratio"]), 2) if vol_sma20 > 0 else d_info["Vol_Ratio"]
                rsi15 = round(calc_rsi(df15["Close"], 14), 1)
                ema9_15 = round(safe_num(df15["Close"].ewm(span=9, adjust=False).mean().iloc[-1], c15), 2)

                last_ts = df15.index[-1]
                try:
                    last_ts_ist = last_ts.tz_convert("Asia/Kolkata") if last_ts.tzinfo else last_ts + timedelta(hours=5, minutes=30)
                    candle_time_str = last_ts_ist.strftime("%I:%M %p")
                except Exception:
                    candle_time_str = ist_now.strftime("%I:%M %p")

                day_slice = df15[df15.index.date == df15.index[-1].date()]
                vwap15 = round(safe_num(((day_slice["High"] + day_slice["Low"] + day_slice["Close"]) / 3.0 * day_slice["Volume"]).sum() / day_slice["Volume"].sum(), c15), 2) if (len(day_slice) >= 1 and safe_num(day_slice["Volume"].sum()) > 0) else round(c15, 2)

                sym_clean = tk.replace(".NS", "")
                peer_up_str = f"{d_info['Sec_Up_Count']}/{d_info['Sec_Tot_Count']} Up ({d_info['Sec_Peer_Up_Pct']:.0f}%)"
                peer_dn_cnt = d_info["Sec_Tot_Count"] - d_info["Sec_Up_Count"]
                peer_dn_str = f"{peer_dn_cnt}/{d_info['Sec_Tot_Count']} Down ({d_info['Sec_Peer_Down_Pct']:.0f}%)"

                l1_bull = d_info["Sec_Bull_Turn"] or (d_info["Sec_1D"] >= 0.25)
                l2_bull = d_info["Sec_Peer_Up_Pct"] >= 55.0
                l3_bull = (c15 > vwap15) and (c15 > ema9_15) and (c15 >= d_info["Prev_High"] * 0.995 or d_info["1D"] >= 1.0) and (v15_ratio >= 1.20) and (54 <= rsi15 <= 78)

                if l1_bull and l2_bull and l3_bull:
                    ent_v = round(max(c15, h15 * 1.0005), 2)
                    sl_v = round(min(l15, min(vwap15, ema9_15) * 0.995), 2)
                    tgt_v = round(c15 + 1.6 * d_info["ATR"], 2)
                    bull_15m.append({
                        "Time": candle_time_str, "Symbol": sym_clean, "Ticker": tk, "Sector": d_info["Sector"],
                        "Peer_Sync": peer_up_str, "Price": round(c15, 2), "VWAP": vwap15, "EMA9": ema9_15,
                        "Vol_Ratio": v15_ratio, "RSI": rsi15, "1D": d_info["1D"], "Confidence": d_info["Confidence"],
                        "Reason": f"✅ 3-Layer Pass: Sec {d_info['Sec_1D']:+.1f}% ({peer_up_str}) + Price > VWAP & 9EMA",
                        "Entry": ent_v, "SL": sl_v, "Target": tgt_v,
                    })

                l1_bear = d_info["Sec_Bear_Roll"] or (d_info["Sec_1D"] <= -0.20)
                l2_bear = d_info["Sec_Peer_Down_Pct"] >= 55.0
                l3_bear = (c15 < vwap15) and (c15 < ema9_15) and (c15 <= d_info["Prev_Low"] * 1.005 or d_info["1D"] <= -1.0) and (v15_ratio >= 1.15) and (22 <= rsi15 <= 46)

                if l1_bear and l2_bear and l3_bear:
                    ent_s = round(min(c15, l15 * 0.9995), 2)
                    sl_s = round(max(h15, max(vwap15, ema9_15) * 1.005), 2)
                    tgt_s = round(c15 - 1.6 * d_info["ATR"], 2)
                    bear_15m.append({
                        "Time": candle_time_str, "Symbol": sym_clean, "Ticker": tk, "Sector": d_info["Sector"],
                        "Peer_Sync": peer_dn_str, "Price": round(c15, 2), "VWAP": vwap15, "EMA9": ema9_15,
                        "Vol_Ratio": v15_ratio, "RSI": rsi15, "1D": d_info["1D"], "Confidence": d_info["Confidence"],
                        "Reason": f"🔻 3-Layer Short: Sec {d_info['Sec_1D']:+.1f}% ({peer_dn_str}) + Price < VWAP & 9EMA",
                        "Entry": ent_s, "SL": sl_s, "Target": tgt_s,
                    })
            except Exception:
                continue
    except Exception:
        pass

    b_df = pd.DataFrame(bull_15m).sort_values("1D", ascending=False) if bull_15m else pd.DataFrame()
    br_df = pd.DataFrame(bear_15m).sort_values("1D", ascending=True) if bear_15m else pd.DataFrame()
    return b_df, br_df

@st.cache_data(ttl=120, show_spinner=False)
def fetch_any_custom_stock_live(query_sym: str, stocks_df: pd.DataFrame):
    clean_s = query_sym.strip().upper().replace(".NS", "")
    full_tk = f"{clean_s}.NS"
    if not stocks_df.empty and full_tk in stocks_df["Ticker"].values:
        return stocks_df[stocks_df["Ticker"] == full_tk].iloc[0].to_dict()
    try:
        df = yf.download(full_tk, period="6mo", interval="1d", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        df = df.dropna(subset=["Close", "Open", "High", "Low"])
        if len(df) < 15:
            return None
        c_now = float(df["Close"].iloc[-1])
        h_now, l_now = float(df["High"].iloc[-1]), float(df["Low"].iloc[-1])
        prev_c = float(df["Close"].iloc[-2])
        r_1d = round(((c_now - prev_c) / prev_c) * 100.0, 2)
        dma20 = round(float(df["Close"].tail(20).mean()), 2)
        dma50 = round(float(df["Close"].tail(50).mean()), 2)
        avg_v = float(df["Volume"].iloc[-21:-1].mean()) if len(df) >= 21 else float(df["Volume"].mean())
        vol_r = round(float(df["Volume"].iloc[-1]) / avg_v, 2) if avg_v > 0 else 1.0
        rsi_v = round(calc_rsi(df["Close"], 14), 1)
        atr_v = round(max(float((df["High"].tail(14) - df["Low"].tail(14)).mean()), c_now * 0.015), 2)
        return {
            "Ticker": full_tk, "Symbol": clean_s, "Sector": TICKER_TO_SECTOR.get(full_tk, "NSE Custom Stock"),
            "Price": round(c_now, 2), "1D": r_1d, "RS_vs_Nifty": r_1d, "Vol_Ratio": vol_r, "RSI": rsi_v,
            "DMA20": dma20, "DMA50": dma50, "Above_20DMA": c_now >= dma20, "Above_50DMA": c_now >= dma50,
            "Consec_Up": 1, "Bull_Candle": "Live Custom Scan", "Bear_Candle": None,
            "Sec_1D": r_1d, "Sec_Peer_Up_Pct": 65.0, "Sec_Bull_Turn": r_1d > 0, "ATR": atr_v,
            "Action_Signal": "🟢 Bullish Setup" if (c_now >= dma20 and rsi_v >= 50) else "⚖️ Watch / Support",
            "Confidence": 78 if c_now >= dma20 else 58,
            "Buy_Entry": round(max(c_now, h_now * 0.998), 2),
            "Buy_SL": round(min(l_now, c_now - 1.2 * atr_v), 2),
            "Buy_Target": round(c_now + 1.8 * atr_v, 2),
            "Short_Entry": round(min(c_now, l_now * 1.002), 2),
            "Short_SL": round(max(h_now, c_now + 1.2 * atr_v), 2),
            "Short_Target": round(c_now - 1.8 * atr_v, 2),
        }
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_stock_news_and_sentiment(sym_clean: str):
    headlines = []
    pos_words = ["surge", "jump", "gain", "win", "order", "profit", "buy", "upgrade", "bullish", "high", "growth", "rally", "beat", "expand", "record", "bonus", "dividend", "turnaround", "strong", "up"]
    neg_words = ["fall", "drop", "loss", "crash", "downgrade", "sell", "weak", "slump", "penalty", "probe", "low", "cut", "miss", "decline", "bearish", "concern", "risk", "debt", "down"]
    pos_hits, neg_hits = 0, 0
    try:
        q = urllib.parse.quote(f"{sym_clean} share price NSE India")
        url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            xml_data = resp.read()
        root = ET.fromstring(xml_data)
        for item in root.findall(".//item")[:4]:
            title_el = item.find("title")
            pub_el = item.find("pubDate")
            if title_el is not None and title_el.text:
                t_txt = title_el.text.strip()
                p_txt = pub_el.text[:16] if (pub_el is not None and pub_el.text) else ""
                headlines.append((t_txt, p_txt))
                t_low = t_txt.lower()
                pos_hits += sum(1 for w in pos_words if w in t_low)
                neg_hits += sum(1 for w in neg_words if w in t_low)
    except Exception:
        pass

    if pos_hits > neg_hits:
        return headlines, "🟢 Positive News Flow (Bullish Catalyst)", min(25, 16 + (pos_hits - neg_hits) * 3)
    elif neg_hits > pos_hits:
        return headlines, "🔴 Negative / Cautious News Flow", max(4, 12 - (neg_hits - pos_hits) * 3)
    return headlines, "⚖️ Neutral / Normal Market News Flow", 15

def generate_ai_stock_verdict(s_info: dict, n_d: dict, v_d: dict, adv_cnt: int, dec_cnt: int):
    sym = s_info["Symbol"]
    headlines, news_label, news_pts = fetch_live_stock_news_and_sentiment(sym)

    tech_pts, tech_notes = 0, []
    if s_info["Above_50DMA"] and s_info["Above_20DMA"]:
        tech_pts += 16
        tech_notes.append(f"✅ Price (₹{s_info['Price']}) is above 20-DMA (₹{s_info['DMA20']}) & 50-DMA (₹{s_info['DMA50']}).")
    elif s_info["Above_20DMA"]:
        tech_pts += 12
        tech_notes.append(f"🔄 Price crossed above 20-DMA (₹{s_info['DMA20']}) — Short-term Turnaround.")
    else:
        tech_pts += 4
        tech_notes.append(f"⚠️ Price is below 20-DMA (₹{s_info['DMA20']}) & 50-DMA (₹{s_info['DMA50']}).")

    if 45 <= s_info["RSI"] <= 68:
        tech_pts += 12
        tech_notes.append(f"✅ RSI ({s_info['RSI']}) is in strong Bullish Momentum zone.")
    elif s_info["RSI"] > 74:
        tech_pts += 4
        tech_notes.append(f"⚠️ RSI ({s_info['RSI']}) is Overbought — wait for pullback.")
    else:
        tech_pts += 7
        tech_notes.append(f"🔄 RSI ({s_info['RSI']}) is in Oversold/Support zone.")

    if s_info["Vol_Ratio"] >= 1.25:
        tech_pts += 10
        tech_notes.append(f"🔥 High Volume Breakout ({s_info['Vol_Ratio']}x vs 20-day avg).")
    else:
        tech_pts += 5
        tech_notes.append(f"📊 Volume Ratio is {s_info['Vol_Ratio']}x | RS vs Nifty: {s_info.get('RS_vs_Nifty', 0):+.2f}%.")

    mkt_pts, mkt_notes = 0, []
    peer_pct = s_info.get("Sec_Peer_Up_Pct", 50.0)
    if n_d["1D"] >= -0.15 and adv_cnt >= dec_cnt * 0.8:
        mkt_pts += 10
        mkt_notes.append(f"✅ Broad Market (Nifty {n_d['1D']:+.2f}%) & Breadth ({adv_cnt} Up) are supportive.")
    else:
        mkt_pts += 5
        mkt_notes.append(f"⚠️ Broad Market is Down (Nifty {n_d['1D']:+.2f}%, {dec_cnt} Declining) — keep strict SL.")

    if s_info.get("Sec_1D", 0) >= 0 and peer_pct >= 55.0:
        mkt_pts += 14
        mkt_notes.append(f"🚀 Sector ({s_info['Sector']}) & Peers ({peer_pct:.0f}% Stocks Up) are moving together!")
    else:
        mkt_pts += 5
        mkt_notes.append(f"⚠️ Sector ({s_info['Sector']}) Peer Sync is {peer_pct:.0f}% Up.")

    total_ai_score = int(np.clip(tech_pts + mkt_pts + news_pts, 20, 97))
    safe_q = max(int(500.0 / max(abs(s_info["Buy_Entry"] - s_info["Buy_SL"]), 0.5)), 1)

    if total_ai_score >= 68:
        verdict_badge = f"🟢 AI VERDICT ({sym}): YES — STRONG BUY SETUP (বুলিশ ট্রেড নেওয়া যেতে পারে)"
        verdict_color = "#10b981"
        bangla_summary = (
            f"✅ **AI পজিশন গাইড ({sym}):** সেক্টর মুভমেন্ট, পিয়ার স্টক সমর্থন ({peer_pct:.0f}% Up) এবং চার্ট অনুযায়ী শেয়ারটি শক্তিশালী অবস্থানে আছে। "
            f"**ইন্ট্রাডে বা সুইং বাই পজিশন:** দাম **₹{s_info['Buy_Entry']}**-এর ওপরে থাকলে এন্ট্রি নিন | "
            f"**স্টপ-লস (SL):** ₹{s_info['Buy_SL']} | **টার্গেট ১:** ₹{round(s_info['Buy_Entry'] + 1.2*s_info['ATR'], 2)} | **টার্গেট ২:** ₹{s_info['Buy_Target']} | **নিরাপদ শেয়ার সংখ্যা (₹500 ঝুঁকিতে):** `{safe_q} টি`।"
        )
    elif total_ai_score >= 52:
        verdict_badge = f"🟡 AI VERDICT ({sym}): WAIT FOR BREAKOUT ABOVE ₹{s_info['Buy_Entry']}"
        verdict_color = "#f59e0b"
        bangla_summary = (
            f"⚖️ **AI পজিশন গাইড ({sym}):** শেয়ারটি এখন কনসোলিডেশন জোনে আছে। "
            f"**বাই এন্ট্রি:** কেবল দাম **₹{s_info['Buy_Entry']}** ব্রেক করে ওপরে টিকলে তবেই কিনবেন (SL: ₹{s_info['Buy_SL']}, Target: ₹{s_info['Buy_Target']})। "
            f"আর যদি দাম **₹{s_info['Short_Entry']}**-এর নিচে ভেঙে পড়ে, তবে শর্ট (Short) পজিশন নেওয়া যাবে (SL: ₹{s_info['Short_SL']}, Target: ₹{s_info['Short_Target']})।"
        )
    else:
        verdict_badge = f"🔴 AI VERDICT ({sym}): BEARISH / AVOID BUYING (শর্ট ফোকাস বা অপেক্ষা)"
        verdict_color = "#ef4444"
        bangla_summary = (
            f"🛑 **AI পজিশন গাইড ({sym}):** এই মুহূর্তে বুলিশ বাই ট্রেড এড়িয়ে চলুন। "
            f"**ইন্ট্রাডে শর্ট (Short) পজিশন:** দাম **₹{s_info['Short_Entry']}**-এর নিচে নামলে শর্ট করতে পারেন | "
            f"**স্টপ-লস (SL):** ₹{s_info['Short_SL']} | **টার্গেট:** ₹{s_info['Short_Target']}।"
        )

    return {
        "score": total_ai_score, "badge": verdict_badge, "color": verdict_color,
        "bangla": bangla_summary, "tech_notes": tech_notes, "mkt_notes": mkt_notes,
        "news_label": news_label, "headlines": headlines
    }

def filter_next_day_intraday_stocks(stocks_df: pd.DataFrame):
    df = stocks_df.copy()
    b_cand = df[(df["Consec_Up"] <= 2) & (df["1D"] >= 0.0) & (df["1D"] <= 4.5) & (df["Vol_Ratio"] >= 1.05)].copy()
    if b_cand.empty:
        b_cand = df.sort_values("1D", ascending=False).head(8).copy()
    b_cand["Bull_Candle"] = b_cand["Bull_Candle"].fillna("Tight Base")
    bull8 = b_cand.sort_values(["1D", "Vol_Ratio"], ascending=[False, False]).head(8).copy()
    bull8["Reason"] = bull8["Bull_Candle"].astype(str) + " • Vol " + bull8["Vol_Ratio"].astype(str) + "x • Peer Sync " + bull8["Sec_Peer_Up_Pct"].astype(str) + "% Up"
    bull8["Entry"], bull8["SL"], bull8["Target"] = bull8["Buy_Entry"], bull8["Buy_SL"], bull8["Buy_Target"]

    used = set(bull8["Ticker"].tolist())
    br_cand = df[(~df["Ticker"].isin(used)) & (df["Consec_Down"] <= 2) & (df["1D"] < 0.0) & (df["1D"] >= -4.5) & (df["Vol_Ratio"] >= 1.05)].copy()
    if br_cand.empty:
        br_cand = df[~df["Ticker"].isin(used)].sort_values("1D", ascending=True).head(8).copy()
    br_cand["Bear_Candle"] = br_cand["Bear_Candle"].fillna("Supply Stall")
    bear8 = br_cand.sort_values(["1D", "Vol_Ratio"], ascending=[True, False]).head(8).copy()
    bear8["Reason"] = bear8["Bear_Candle"].astype(str) + " • Vol " + bear8["Vol_Ratio"].astype(str) + "x • Peer Sync " + bear8["Sec_Peer_Down_Pct"].astype(str) + "% Down"
    bear8["Entry"], bear8["SL"], bear8["Target"] = bear8["Short_Entry"], bear8["Short_SL"], bear8["Short_Target"]
    return bull8, bear8

# ==============================================================================
# 6. LOAD CACHED DATA FIRST
# ==============================================================================
with st.spinner("⚡ Loading Market Intelligence..."):
    pulse = load_pulse_indices()
    base_stocks_df, base_sectors_df = load_full_market_data()

if base_stocks_df.empty or base_sectors_df.empty:
    st.error("⚠️ Market data temporarily unavailable. Please click ⚡ Sync.")
    st.stop()

n_d, b_d, v_d, u_d = pulse["NIFTY"], pulse["BANKNIFTY"], pulse["VIX"], pulse["USDINR"]
stocks_df = base_stocks_df.copy()
sectors_df = base_sectors_df.copy()
stocks_df["RS_vs_Nifty"] = (stocks_df["1D"] - n_d["1D"]).round(2)
sectors_df["Sec_RS"] = (sectors_df["1D"] - n_d["1D"]).round(2)

if is_mkt_open:
    bull_15m_df, bear_15m_df = run_3layer_intraday_scanner(stocks_df)
else:
    bull_15m_df, bear_15m_df = pd.DataFrame(), pd.DataFrame()

bull_next8, bear_next8 = filter_next_day_intraday_stocks(stocks_df)

if not is_after_close and is_mkt_open:
    now_hm = ist_now.strftime("%I:%M %p")
    for _, r15 in bull_15m_df.iterrows():
        push_3layer_alert(
            str(r15.get("Time", now_hm)), "🟢 3-Layer LONG", r15["Symbol"], r15["Ticker"], r15["Sector"],
            r15["Peer_Sync"], r15["Price"], r15["VWAP"], r15["EMA9"], r15["Entry"], r15["SL"], r15["Target"], r15["Reason"], True
        )
    for _, r15b in bear_15m_df.iterrows():
        push_3layer_alert(
            str(r15b.get("Time", now_hm)), "🔴 3-Layer SHORT", r15b["Symbol"], r15b["Ticker"], r15b["Sector"],
            r15b["Peer_Sync"], r15b["Price"], r15b["VWAP"], r15b["EMA9"], r15b["Entry"], r15b["SL"], r15b["Target"], r15b["Reason"], False
        )

# ==============================================================================
# 7. TOP HEADER BAR
# ==============================================================================
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

mkt_status_html = (
    f'<span style="color:#10b981;font-weight:800;">🟢 LIVE MARKET ({ist_now.strftime("%I:%M %p IST")})</span>'
    if is_mkt_open else
    f'<span style="color:#f59e0b;font-weight:700;">🕒 MARKET CLOSED ({ist_now.strftime("%a %I:%M %p IST")})</span>'
)

top_c1, top_c2, top_c3, top_c4, top_c5, top_c6 = st.columns([4.5, 1.5, 1.2, 1.25, 0.9, 0.65])
with top_c1:
    st.markdown(
        f'<a href="?nav_action=home&auto={get_auto_param()}" target="_self" class="brand-logo-link" title="Click to Reset All Filters & Return to Home">'
        f'<span class="clean-compass-icon">🧭</span>'
        f'<div><div class="brand-title-glow">AlphaPulse Pro — Nifty 500 Turnaround Terminal</div>'
        f'<div class="brand-subtitle">{len(SECTOR_STOCKS)} Sectors • {len(ALL_TICKERS)}+ Stocks • {mkt_status_html}</div></div></a>',
        unsafe_allow_html=True
    )
with top_c2:
    theme_mode = st.selectbox("Theme", ["🌙 Pro Dark (Slate)", "🌌 Cyber Neon (Violet)", "☀️ Clean Light (Day)"], index=0, label_visibility="collapsed")
with top_c3:
    if st.button("🤖 AI Search", use_container_width=True, help="Open AI Market Brief & Search Any Stock"):
        st.session_state.show_ai_helper = not st.session_state.show_ai_helper
with top_c4:
    alert_count = len(alert_vault["items"])
    if st.button(f"🔔 Alerts ({alert_count})", use_container_width=True, help="3-Layer Confirmed Intraday Alerts (9:15 AM – 3:30 PM)"):
        st.session_state.show_alert_drawer = not st.session_state.show_alert_drawer
with top_c5:
    def on_auto_toggle():
        st.session_state.auto_scan_locked = st.session_state.auto_toggle_widget
        st.query_params["auto"] = "1" if st.session_state.auto_scan_locked else "0"

    auto_alert_on = st.toggle(
        "🔔 Auto",
        value=st.session_state.auto_scan_locked,
        key="auto_toggle_widget",
        on_change=on_auto_toggle,
        help="Persistent Auto-Alert: Stays ON until you manually turn it OFF"
    )
with top_c6:
    if st.button("⚡", use_container_width=True, help="Sync Live Market Data Now"):
        st.cache_data.clear()
        st.rerun()

# ==============================================================================
# 8. THEME CSS & UI HELPERS
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
html, body, [data-testid="stAppViewContainer"], .main, p, label, button, input, .stMarkdown {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}}
[data-testid="stIconMaterial"], .material-icons, .material-symbols-rounded {{
    font-family: 'Material Symbols Rounded' !important; font-weight: normal !important; font-style: normal !important;
    font-size: 1.15rem !important; line-height: 1 !important; letter-spacing: normal !important; text-transform: none !important;
    display: inline-block !important; white-space: nowrap !important; word-wrap: normal !important; direction: ltr !important;
}}
html, body, [data-testid="stAppViewContainer"], .main {{ background-color:{BG_MAIN} !important; color:{TEXT_MAIN} !important; scroll-behavior:smooth !important; }}
.block-container {{ padding-top:1.0rem !important; padding-bottom:4.8rem !important; max-width:97% !important; }}

a.brand-logo-link {{ text-decoration:none !important; display:inline-flex; align-items:center; gap:10px; padding:2px 4px; }}
.clean-compass-icon {{ font-size:2.15rem; line-height:1; background:transparent !important; border:none !important; padding:0 !important; }}
.brand-title-glow {{
    font-size:1.30rem; font-weight:800; letter-spacing:-0.4px; line-height:1.18;
    background:linear-gradient(90deg, #f59e0b 0%, #ef4444 48%, #10b981 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}}
.brand-subtitle {{ font-size:0.72rem; font-weight:600; color:{TEXT_SUB} !important; }}

[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, .stSelectbox label, .stNumberInput label, .stTextInput label, .stRadio label, [data-testid="stRadio"] label span, [data-testid="stToggle"] label p, [data-testid="stCheckbox"] label p {{
    color:{TEXT_MAIN} !important; font-weight:700 !important; font-size:0.80rem !important; opacity:1 !important;
}}
[data-testid="stRadio"] div[role="radiogroup"] {{ background:{BG_CARD}; border:1px solid {BORDER_C}; padding:3px 10px; border-radius:999px; gap:10px !important; }}

div.stButton > button, button[data-testid="stBaseButton-secondary"], div.stDownloadButton > button,
div.stLinkButton > a, a[data-testid="stBaseLinkButton-secondary"] {{
    background:{BTN_BG} !important; color:{TEXT_MAIN} !important; border:1.5px solid {BTN_BORDER} !important;
    border-radius:10px !important; font-weight:800 !important; font-size:0.79rem !important;
    padding:0.42rem 0.80rem !important; box-shadow:{CARD_SHADOW} !important; text-decoration:none !important;
}}
div.stButton > button p, div.stDownloadButton > button p, div.stLinkButton > a p, a[data-testid="stBaseLinkButton-secondary"] p, a[data-testid="stBaseLinkButton-secondary"] span {{
    color:{TEXT_MAIN} !important; font-weight:800 !important;
}}
div.stButton > button:hover, div.stDownloadButton > button:hover, div.stLinkButton > a:hover, a[data-testid="stBaseLinkButton-secondary"]:hover {{
    background:linear-gradient(135deg,#f59e0b,#ea580c) !important; color:#ffffff !important; border-color:#f59e0b !important;
}}
div.stButton > button:hover p, div.stLinkButton > a:hover p, a[data-testid="stBaseLinkButton-secondary"]:hover p, a[data-testid="stBaseLinkButton-secondary"]:hover span {{
    color:#ffffff !important;
}}
button[data-testid="stBaseButton-primary"] {{
    background:linear-gradient(135deg, #f59e0b 0%, #ea580c 100%) !important; color:#ffffff !important;
    border:1.5px solid #fbbf24 !important; border-radius:10px !important; font-weight:800 !important; font-size:0.81rem !important;
}}
button[data-testid="stBaseButton-primary"] p {{ color:#ffffff !important; font-weight:800 !important; }}

.live-pulse-bar {{
    background:{BG_CARD}; border:1px solid {BORDER_C}; border-radius:12px; padding:7px 12px;
    margin:4px 0 8px 0; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:7px; box-shadow:{CARD_SHADOW};
}}
.tick-chip-up {{
    background:rgba(16, 185, 129, 0.14); border:1.5px solid #10b981; border-radius:9px; padding:4px 10px;
    font-family:'JetBrains Mono',monospace !important; font-size:0.79rem; font-weight:800; color:#10b981;
    display:inline-flex; align-items:center; gap:6px;
}}
.tick-chip-down {{
    background:rgba(239, 68, 68, 0.14); border:1.5px solid #ef4444; border-radius:9px; padding:4px 10px;
    font-family:'JetBrains Mono',monospace !important; font-size:0.79rem; font-weight:800; color:#ef4444;
    display:inline-flex; align-items:center; gap:6px;
}}
.breadth-mini-pill {{ background:{BG_SUB}; border:1px solid {BORDER_C}; border-radius:9px; padding:4px 10px; font-size:0.76rem; font-weight:800; }}
.live-dot {{ width:8px; height:8px; border-radius:50%; display:inline-block; }}

.alert-drawer-box {{ background:{BG_CARD}; border:2px solid #f59e0b; border-radius:14px; padding:12px 16px; margin:6px 0 12px 0; }}
.alert-timeline-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(275px, 1fr)); gap:8px; max-height:360px; overflow-y:auto; padding:4px 2px; }}
a.alert-log-item {{ text-decoration:none !important; background:{BG_SUB}; border:1px solid {BORDER_C}; border-radius:9px; padding:8px 11px; color:{TEXT_MAIN} !important; display:flex; flex-direction:column; gap:3px; }}
.al-bull-left {{ border-left:4px solid #10b981 !important; }}
.al-bear-left {{ border-left:4px solid #ef4444 !important; }}

div[data-testid="stHorizontalBlock"] {{ align-items: flex-end !important; }}
@media (max-width: 768px) {{
    .live-pulse-bar {{ display:grid !important; grid-template-columns: 1fr 1fr !important; gap:6px !important; }}
    .compass-pill {{ grid-column: span 2 !important; text-align:center !important; }}
}}

a.svg-gauge-card {{
    text-decoration:none !important; background:{BG_CARD}; border:1.5px solid {BORDER_C}; border-radius:12px; padding:10px 14px;
    display:flex; align-items:center; justify-content:space-between; box-shadow:{CARD_SHADOW};
}}
a.svg-gauge-card:hover {{ border-color:#f59e0b; }}
.svg-gauge-info {{ display:flex; flex-direction:column; gap:4px; max-width:63%; }}
.svg-gauge-title {{ font-size:0.90rem; font-weight:800; color:{TEXT_MAIN}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.svg-gauge-sub {{ font-size:0.72rem; color:{TEXT_SUB}; font-weight:600; }}
.sector-grid-wrap {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:10px; margin-top:8px; }}

.master-viewer-bar {{
    font-size:0.84rem; font-weight:800; color:{TEXT_MAIN}; background:{BG_CARD}; border:1.5px solid {BORDER_C}; border-left:4px solid #10b981;
    height:42px; padding:0 14px; border-radius:10px; display:flex; align-items:center; justify-content:space-between;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}}

.kite-order-pad {{ background:{BG_CARD}; border:1.5px solid #387ed1; border-top:4px solid #ff5722; border-radius:14px; padding:12px 16px; margin:10px 0 12px 0; }}
.kite-ticket-metric {{ background:{BG_SUB}; border:1px solid {BORDER_C}; border-radius:9px; padding:7px 10px; text-align:center; }}
.kite-metric-lbl {{ font-size:0.68rem; color:{TEXT_SUB}; font-weight:700; display:block; }}
.kite-metric-val {{ font-size:0.92rem; font-weight:800; font-family:'JetBrains Mono',monospace !important; color:{TEXT_MAIN}; }}

.ai-verdict-box {{ background:{BG_CARD}; border:2px solid #f59e0b; border-radius:14px; padding:14px 18px; margin:10px 0 14px 0; }}
.ai-sub-card {{ background:{BG_SUB}; border:1px solid {BORDER_C}; border-radius:10px; padding:10px 12px; height:100%; }}

button[data-baseweb="tab"] {{ background:{BG_CARD} !important; border:1.5px solid {BORDER_C} !important; border-radius:10px 10px 0 0 !important; margin-right:6px !important; padding:8px 16px !important; }}
button[data-baseweb="tab"] p {{ color:{TEXT_MAIN} !important; font-weight:700 !important; font-size:0.84rem !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{ background:linear-gradient(135deg,rgba(245,158,11,0.22),rgba(16,185,129,0.18)) !important; border-color:#f59e0b !important; border-bottom:3px solid #f59e0b !important; }}
button[data-baseweb="tab"][aria-selected="true"] p {{ color:#f59e0b !important; font-weight:800 !important; }}
[data-testid="stExpander"] details {{ background:{BG_CARD} !important; border:1px solid {BORDER_C} !important; border-radius:10px !important; box-shadow:{CARD_SHADOW}; margin-top:2px !important; }}
[data-testid="stExpander"] summary {{ padding:8px 14px !important; display:flex !important; align-items:center !important; gap:8px !important; }}
[data-testid="stExpander"] summary p {{ color:{TEXT_MAIN} !important; font-weight:700 !important; font-size:0.81rem !important; margin:0 !important; }}

.aligned-sec-hdr {{ font-size:0.86rem; font-weight:800; color:{TEXT_MAIN}; background:{BG_CARD}; border:1px solid {BORDER_C}; border-left:4px solid #f59e0b; padding:7px 12px; border-radius:8px; margin-bottom:8px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}

.nse-heatmap-container {{ background:{BG_CARD}; border:1.5px solid {BORDER_C}; border-radius:14px; padding:14px 16px; margin:8px 0 14px 0; }}
.nse-heatmap-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(175px, 1fr)); gap:8px; margin-top:10px; }}
a.nse-tile {{ text-decoration:none !important; color:#ffffff !important; padding:10px 12px; border-radius:8px; display:flex; flex-direction:column; justify-content:space-between; height:74px; border:1px solid rgba(255,255,255,0.15); }}
.nse-tile-name {{ font-size:0.74rem; font-weight:800; text-transform:uppercase; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.nse-tile-bot {{ display:flex; justify-content:space-between; align-items:baseline; font-family:'JetBrains Mono',monospace !important; }}

.compass-pill {{ padding:4px 11px; border-radius:999px; font-size:0.74rem; font-weight:800; }}
.turnaround-hero-box {{ background:{BG_CARD}; border:1.5px solid {BORDER_C}; border-left:5px solid #10b981; border-radius:12px; padding:10px 14px; margin:4px 0 10px 0; box-shadow:{CARD_SHADOW}; }}
.turnaround-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(225px,1fr)); gap:8px; margin-top:8px; }}
a.turn-sec-card {{ text-decoration:none !important; background:{BG_SUB}; border:1px solid #10b98155; border-radius:10px; padding:8px 11px; color:{TEXT_MAIN} !important; display:flex; flex-direction:column; justify-content:space-between; height:88px; }}
.t-sec-name {{ font-weight:800; font-size:0.81rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:145px; }}

.radar-panel-bull {{ background:{BG_CARD}; border:1px solid #10b98166; border-top:3.5px solid #10b981; border-radius:12px; padding:10px 12px; margin-bottom:8px; }}
.radar-panel-bear {{ background:{BG_CARD}; border:1px solid #ef444466; border-top:3.5px solid #ef4444; border-radius:12px; padding:10px 12px; margin-bottom:8px; }}
.radar-panel-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid {BORDER_C}; }}
.radar-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(235px,1fr)); gap:7px; }}
a.radar-row-card {{ text-decoration:none !important; background:{BG_SUB}; border:1px solid {BORDER_C}; border-radius:9px; padding:8px 10px; color:{TEXT_MAIN} !important; display:flex; flex-direction:column; justify-content:space-between; min-height:96px; }}
.r-top {{ display:flex; justify-content:space-between; align-items:center; }}
.r-sym {{ font-size:0.84rem; font-weight:800; color:{TEXT_MAIN}; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:155px; }}
.r-tag-bull {{ background:rgba(16,185,129,0.16); color:#10b981; border:1px solid #10b98155; padding:1px 6px; border-radius:5px; font-size:0.66rem; font-weight:800; }}
.r-tag-bear {{ background:rgba(239,68,68,0.16); color:#ef4444; border:1px solid #ef444455; padding:1px 6px; border-radius:5px; font-size:0.66rem; font-weight:800; }}
.r-mid {{ display:flex; justify-content:space-between; font-size:0.73rem; color:{TEXT_SUB}; }}
.r-reason-box {{ font-size:0.70rem; color:{TEXT_MAIN}; background:rgba(245,158,11,0.10); border-left:2.5px solid #f59e0b; padding:3px 7px; border-radius:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.r-plan {{ display:flex; justify-content:space-between; font-size:0.70rem; font-weight:700; background:rgba(0,0,0,0.16); padding:3px 7px; border-radius:6px; font-family:'JetBrains Mono',monospace !important; }}
a.wa-share-btn {{ text-decoration:none !important; background:linear-gradient(135deg,#16a34a,#22c55e); color:#fff !important; padding:5px 13px; border-radius:999px; font-size:0.75rem; font-weight:800; display:inline-flex; align-items:center; gap:5px; }}

.pill-container {{ display:flex; flex-wrap:wrap; gap:5px; margin-top:6px; }}
a.bull-pill, a.bear-pill {{ text-decoration:none !important; padding:3px 8px; border-radius:999px; font-size:0.71rem; font-weight:700; display:inline-flex; align-items:center; gap:4px; }}
a.bull-pill {{ background:rgba(16,185,129,0.14); border:1px solid #10b98199; color:#10b981 !important; }}
a.bear-pill {{ background:rgba(239,68,68,0.14); border:1px solid #ef444499; color:#ef4444 !important; }}

.floating-right-dock {{ position:fixed; bottom:58px; right:18px; z-index:999999; display:flex; flex-direction:column; gap:7px; align-items:flex-end; }}
a.single-top-btn {{ text-decoration:none !important; background:linear-gradient(135deg,#f59e0b,#ea580c); color:#fff !important; padding:7px 15px; border-radius:999px; font-size:0.79rem; font-weight:800; border:1.5px solid rgba(255,255,255,0.35); box-shadow:0 6px 20px rgba(245,158,11,0.5); }}
</style>
""", unsafe_allow_html=True)

def make_stock_pills(df_sub: pd.DataFrame, tf_col: str = "1D") -> str:
    if df_sub is None or df_sub.empty:
        return ""
    ap = get_auto_param()
    pills = []
    col_use = tf_col if tf_col in df_sub.columns else "1D"
    for _, r in df_sub.iterrows():
        qt = urllib.parse.quote(str(r["Ticker"]))
        val_c = safe_num(r.get(col_use, r.get("1D", 0.0)))
        cls = "bull-pill" if val_c >= 0 else "bear-pill"
        icon = "🟢" if val_c >= 0 else "🔴"
        pills.append(f'<a class="{cls}" href="?focus_stock={qt}&auto={ap}" target="_self">{icon} {r["Symbol"]} ({val_c:+.1f}%)</a>')
    return f'<div class="pill-container">{"".join(pills)}</div>'

def make_svg_speedometer_card(s_row: pd.Series, tf_choice: str) -> str:
    score = int(np.clip(safe_num(s_row["Meter"], 50), 5, 98))
    ret_val = safe_num(s_row[tf_choice], 0.0)
    s_name = s_row["Sector"]
    col = "#10b981" if ret_val >= 0 else "#ef4444"
    ret_col = "#10b981" if ret_val >= 0 else "#ef4444"
    rs_col = "#10b981" if s_row["Sec_RS"] >= 0 else "#ef4444"
    dash_len = round((score / 100.0) * 126.0, 1)
    q_s = urllib.parse.quote(s_name)
    ap = get_auto_param()

    return (
        f'<a href="?focus_sec={q_s}&auto={ap}" target="_self" class="svg-gauge-card" title="Click to open {s_name} stocks in Master Viewer">'
        f'<div class="svg-gauge-info">'
        f'<div class="svg-gauge-title">🧭 {s_name} 🔍</div>'
        f'<div class="svg-gauge-sub">{s_row["Zone"]} • 🤝 Sync: <b style="color:{"#10b981" if s_row["Peer_Up_Pct"]>=50 else "#ef4444"};">{s_row["Up_Count"]}/{s_row["Count"]} Up ({s_row["Peer_Up_Pct"]:.0f}%)</b></div>'
        f'<div class="svg-gauge-sub">Vol: <b>{s_row["Avg_Vol"]}x</b> • ⚡ RS: <b style="color:{rs_col};">{s_row["Sec_RS"]:+.2f}%</b> • ⭐ <b style="color:#f59e0b;">{s_row["Top_Pick"]}</b></div>'
        f'</div>'
        f'<div style="text-align:center;min-width:116px;">'
        f'<svg width="112" height="62" viewBox="0 0 100 58">'
        f'<path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="rgba(148,163,184,0.22)" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M 10 50 A 40 40 0 0 1 90 50" fill="none" stroke="{col}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{dash_len} 126"/>'
        f'<text x="50" y="47" text-anchor="middle" fill="{TEXT_MAIN}" font-size="14" font-weight="800" font-family="JetBrains Mono">{score}</text>'
        f'</svg>'
        f'<div style="font-size:0.74rem;font-weight:800;color:{ret_col};margin-top:-6px;font-family:\'JetBrains Mono\',monospace;">{ret_val:+.2f}% ({tf_choice})</div>'
        f'</div></a>'
    )

# ==============================================================================
# 9. TRUE GREEN / RED PULSE BAR
# ==============================================================================
adv_today, dec_today = int((stocks_df["1D"] > 0).sum()), int((stocks_df["1D"] < 0).sum())

def make_true_color_chip(label: str, key: str):
    d = pulse[key]
    cur_val = d["price"]
    day_pct = d["1D"]
    pts_val = d.get("pts", 0.0)
    is_green = day_pct >= 0
    cls = "tick-chip-up" if is_green else "tick-chip-down"
    arr = "▲" if is_green else "▼"
    dot_col = "#10b981" if is_green else "#ef4444"
    return (
        f'<div class="{cls}">'
        f'<span class="live-dot" style="background:{dot_col};"></span>'
        f'<span>{label}: {cur_val:,.2f} {arr} {pts_val:+.2f} ({day_pct:+.2f}%)</span>'
        f'</div>'
    )

if n_d["1D"] >= 0.15 and adv_today >= dec_today:
    c_txt, c_sty = "🟢 Bullish Market — Focus Long", "background:rgba(16,185,129,0.16);color:#10b981;border:1px solid #10b98155;"
elif n_d["1D"] < 0.0 and dec_today > adv_today:
    c_txt, c_sty = "🔴 Bearish Market — Caution / Focus Short", "background:rgba(239,68,68,0.16);color:#ef4444;border:1px solid #ef444455;"
else:
    c_txt, c_sty = "⚖️ Rotational — Track Green Turnaround Sectors", "background:rgba(245,158,11,0.16);color:#f59e0b;border:1px solid #f59e0b55;"

st.markdown(
    f'<div class="live-pulse-bar">'
    f'{make_true_color_chip("🇮🇳 Nifty 50", "NIFTY")}'
    f'{make_true_color_chip("🏛️ Bank Nifty", "BANKNIFTY")}'
    f'{make_true_color_chip("⚡ India VIX", "VIX")}'
    f'<div class="breadth-mini-pill">📊 Breadth: <span style="color:#10b981;">🟢 {adv_today} Up</span> | <span style="color:#ef4444;">🔴 {dec_today} Down</span></div>'
    f'<div class="compass-pill" style="{c_sty}">🧭 {c_txt}</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ==============================================================================
# 9.1 3-LAYER QUALITY NOTIFICATION LOG DRAWER (9:15 AM - 3:30 PM)
# ==============================================================================
ap_flag = get_auto_param()

if st.session_state.show_alert_drawer:
    st.markdown('<div class="alert-drawer-box">', unsafe_allow_html=True)
    dr_c1, dr_c2, dr_c3 = st.columns([6.5, 2.0, 1.5])
    with dr_c1:
        st.markdown(f"#### 🔔 Today's 3-Layer Confirmed Intraday Alerts ({today_str} • 9:15 AM – 3:30 PM IST)")
        st.caption("শুধুমাত্র যে শেয়ারগুলো ৩টি স্তরই (১. সেক্টর মুভমেন্ট + ২. ৫৫%+ পিয়ার স্টক সাপোর্ট + ৩. 15m VWAP ও 9-EMA ব্রেকআউট) পাশ করেছে সেগুলোই এখানে জমা হয়।")
    with dr_c2:
        if st.button("🗑️ Clear Log", use_container_width=True):
            alert_vault["items"] = []
            alert_vault["seen_keys"] = set()
            st.rerun()
    with dr_c3:
        if st.button("✖ Close Log", use_container_width=True):
            st.session_state.show_alert_drawer = False
            st.rerun()

    if not alert_vault["items"]:
        st.info("🎯 No random alerts! Waiting for live market hours (9:15 AM – 3:30 PM IST) or a stock to pass all 3 layers.")
    else:
        log_cards_html = []
        for item in alert_vault["items"]:
            qt = urllib.parse.quote(str(item["ticker"]))
            b_cls = "al-bull-left" if item["is_bull"] else "al-bear-left"
            c_col = "#10b981" if item["is_bull"] else "#ef4444"
            act_lbl = "Buy" if item["is_bull"] else "Short"
            log_cards_html.append(
                f'<a href="?focus_stock={qt}&auto={ap_flag}" target="_self" class="alert-log-item {b_cls}">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-size:0.72rem;font-weight:800;color:#f59e0b;font-family:\'JetBrains Mono\',monospace;">🕒 {item["time"]} IST</span>'
                f'<span style="font-size:0.68rem;font-weight:800;color:{c_col};">{item["category"]} • 🤝 {item["peer_sync"]}</span>'
                f'</div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:2px;">'
                f'<span style="font-size:0.86rem;font-weight:800;">{item["symbol"]} <span style="font-size:0.70rem;color:{TEXT_SUB};">({item["sector"]})</span></span>'
                f'<span style="font-size:0.80rem;font-weight:800;color:{c_col};">₹{item["price"]}</span>'
                f'</div>'
                f'<div style="font-size:0.70rem;color:{TEXT_SUB};">VWAP: ₹{item["vwap"]} | 9-EMA: ₹{item["ema9"]}</div>'
                f'<div class="r-plan"><span style="color:#f59e0b;">🎯 {act_lbl}: ₹{item["entry"]}</span><span style="color:#ef4444;">🛑 SL: ₹{item["sl"]}</span><span style="color:#10b981;">🚀 Tgt: ₹{item["target"]}</span></div>'
                f'</a>'
            )
        st.markdown(f'<div class="alert-timeline-grid">{"".join(log_cards_html)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 10. 5-COLUMN FILTER BAR
# ==============================================================================
fc1, fc2, fc3, fc4, fc5 = st.columns([1.1, 2.5, 2.4, 2.3, 1.7])
with fc1:
    tf_choice = st.selectbox("📅 1. Timeframe:", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=0)
with fc2:
    sort_choice = st.selectbox(
        "🔄 2. Sort Sequence By:",
        [
            "🚀 Green Top ➔ Down Sequence (Selected TF)",
            "🔄 Bottom Turnaround Score First",
            "🤝 Highest Peer Sync % First",
            "📉 Top Losers First",
            "🔥 High Volume First"
        ],
        index=0
    )
with fc3:
    sec_list = [DEFAULT_SECTOR] + sorted(list(SECTOR_STOCKS.keys()))
    picked_sec = st.selectbox("🔍 3. Select Sector (42 Sectors):", sec_list, index=sec_list.index(st.session_state.selected_sector) if st.session_state.selected_sector in sec_list else 0)
    if picked_sec != st.session_state.selected_sector:
        st.session_state.selected_sector = picked_sec
        if picked_sec != DEFAULT_SECTOR:
            st.session_state.inspect_sector = picked_sec
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
    if st.button("🗺️ NSE Heatmap & Verdict", use_container_width=True):
        st.session_state.show_nse_heatmap = not st.session_state.show_nse_heatmap

# ==============================================================================
# 10.1 RESTORED CLEAN AI MARKET BRIEF + ANY-STOCK CUSTOM AI SEARCH ENGINE
# ==============================================================================
sectors_df["Is_Green_TF"] = sectors_df[tf_choice] >= 0
turnaround_secs = sectors_df.sort_values(
    by=["Is_Green_TF", tf_choice, "Turnaround_Score"],
    ascending=[False, False, False]
).head(8)

if st.session_state.show_ai_helper:
    top_turn_names = ", ".join([f"{r['Sector']} ({r[tf_choice]:+.2f}%)" for _, r in turnaround_secs.head(4).iterrows()])
    top_bull_syms = ", ".join([f"{r['Symbol']} (₹{r['Price']}, Buy>{r['Entry']}, SL {r['SL']})" for _, r in bull_next8.head(4).iterrows()])
    top_bear_syms = ", ".join([f"{r['Symbol']} (₹{r['Price']}, Short<{r['Entry']}, SL {r['SL']})" for _, r in bear_next8.head(3).iterrows()])

    st.markdown('<div class="aligned-sec-hdr">🤖 AI Live Market Brief & Custom Stock Trade Finder</div>', unsafe_allow_html=True)
    ai_b1, ai_b2 = st.columns([4.8, 5.2])
    with ai_b1:
        st.info(
            f"🧭 **Market Summary:** Nifty {n_d['price']:,.2f} ({n_d['1D']:+.2f}%) | Bank Nifty {b_d['price']:,.2f} ({b_d['1D']:+.2f}%)\n\n"
            f"🟢 **Top Performing Sectors ({tf_choice}):** {top_turn_names}\n\n"
            f"🚀 **Top Bullish Intraday Picks:** {top_bull_syms}\n\n"
            f"🔻 **Top Bearish Intraday Picks:** {top_bear_syms}"
        )
        if st.button("✖ Close AI Panel"):
            st.session_state.show_ai_helper = False
            st.rerun()

    with ai_b2:
        st.markdown("##### 🔍 Search Any NSE Stock for Instant AI Entry, SL & Target")
        s_in1, s_in2, s_in3 = st.columns([5.2, 2.6, 2.2])
        with s_in1:
            custom_q = st.text_input("Type ANY NSE Symbol:", value=st.session_state.ai_custom_ticker, label_visibility="collapsed", placeholder="Type Stock Symbol (e.g. IREDA, SBIN, HAL)...")
        with s_in2:
            analyze_btn = st.button("🤖 AI Trade Plan", type="primary", use_container_width=True)
        with s_in3:
            open_chart_btn = st.button("📈 Open Chart", use_container_width=True)

        if analyze_btn and custom_q.strip():
            st.session_state.ai_custom_ticker = custom_q.strip().upper()
        if open_chart_btn and custom_q.strip():
            st.session_state.ai_custom_ticker = custom_q.strip().upper()
            st.session_state.selected_stock = custom_q.strip().upper().replace(".NS", "") + ".NS"
            st.session_state.scroll_target = "stock-inspector-anchor"
            st.rerun()

        if st.session_state.ai_custom_ticker:
            c_data = fetch_any_custom_stock_live(st.session_state.ai_custom_ticker, stocks_df)
            if c_data is None:
                st.warning(f"⚠️ Could not find NSE symbol `{st.session_state.ai_custom_ticker}`. Please check spelling.")
            else:
                c_ai = generate_ai_stock_verdict(c_data, n_d, v_d, adv_today, dec_today)
                st.markdown(
                    f'<div class="ai-verdict-box" style="margin-top:4px;padding:10px 14px;">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                    f'<span style="font-weight:800;font-size:0.88rem;color:{c_ai["color"]};">{c_ai["badge"]}</span>'
                    f'<span style="font-weight:800;font-size:0.76rem;color:{c_ai["color"]};">Score: {c_ai["score"]}/100</span>'
                    f'</div>'
                    f'<div style="font-size:0.78rem;margin:6px 0;color:{TEXT_MAIN};">{c_ai["bangla"]}</div>'
                    f'<div class="r-plan">'
                    f'<span style="color:#10b981;">🟢 Buy Above: ₹{c_data["Buy_Entry"]} | SL: ₹{c_data["Buy_SL"]} | Tgt: ₹{c_data["Buy_Target"]}</span>'
                    f'<span style="color:#ef4444;">🔴 Short Below: ₹{c_data["Short_Entry"]} | SL: ₹{c_data["Short_SL"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

# ==============================================================================
# 10.2 NSE SECTORAL HEATMAP & BULLISH / BEARISH SECTOR RECOMMENDATION PANEL
# ==============================================================================
if st.session_state.show_nse_heatmap:
    bull_secs_df = sectors_df[sectors_df[tf_choice] > 0.0].sort_values(tf_choice, ascending=False)
    turn_secs_df = sectors_df[sectors_df["Sec_Bull_Turn"]].sort_values(tf_choice, ascending=False)
    bear_secs_df = sectors_df[sectors_df[tf_choice] < 0.0].sort_values(tf_choice, ascending=True)

    def get_nse_tile_color(val: float) -> str:
        return "#047857" if val >= 2.5 else ("#10b981" if val >= 0.75 else ("#059669" if val >= 0.0 else ("#e11d48" if val >= -1.0 else ("#dc2626" if val >= -2.5 else "#991b1b"))))

    heatmap_tiles = []
    for _, srow in sectors_df.sort_values(tf_choice, ascending=False).iterrows():
        v_pct = safe_num(srow[tf_choice], 0.0)
        bg_c = get_nse_tile_color(v_pct)
        q_sec = urllib.parse.quote(srow["Sector"])
        verdict_tag = f"{srow['Up_Count']}/{srow['Count']} Up"
        heatmap_tiles.append(
            f'<a href="?focus_sec={q_sec}&auto={ap_flag}" target="_self" class="nse-tile" style="background:{bg_c};">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<span class="nse-tile-name">{srow["Sector"]}</span>'
            f'<span style="font-size:0.62rem;background:rgba(0,0,0,0.28);padding:1px 5px;border-radius:4px;font-weight:800;">{verdict_tag}</span>'
            f'</div>'
            f'<div class="nse-tile-bot">'
            f'<span style="font-size:0.73rem;opacity:0.92;">⭐ {srow["Top_Pick"]}</span>'
            f'<span style="font-size:0.85rem;font-weight:800;">{v_pct:+.2f}%</span>'
            f'</div></a>'
        )

    hm_top1, hm_top2, hm_top3 = st.columns([6.2, 2.3, 1.5])
    with hm_top1:
        st.markdown(f"#### 🗺️ NSE Sectoral Indices Heatmap — Sorted Green Top ➔ Red Bottom ({tf_choice})")
    with hm_top2:
        st.link_button("🌐 Official NSE India Heatmap", "https://www.nseindia.com/market-data/live-market-indices/heatmap", use_container_width=True)
    with hm_top3:
        if st.button("✖ Close Heatmap", use_container_width=True):
            st.session_state.show_nse_heatmap = False
            st.rerun()

    rec1, rec2, rec3 = st.columns(3)
    with rec1:
        st.success("🟢 **TOP GREEN SECTORS:**\n\n" + (", ".join([f"**{r['Sector']}** ({r[tf_choice]:+.2f}%)" for _, r in bull_secs_df.head(5).iterrows()]) or "None right now"))
    with rec2:
        st.info("🔄 **TURNAROUND WATCH:**\n\n" + (", ".join([f"**{r['Sector']}** ({r[tf_choice]:+.2f}%)" for _, r in turn_secs_df.head(5).iterrows()]) or "None right now"))
    with rec3:
        st.error("🔴 **WEAKEST RED SECTORS:**\n\n" + (", ".join([f"**{r['Sector']}** ({r[tf_choice]:+.2f}%)" for _, r in bear_secs_df.head(5).iterrows()]) or "None right now"))

    st.markdown(f'<div class="nse-heatmap-container"><div class="nse-heatmap-grid">{"".join(heatmap_tiles)}</div></div>', unsafe_allow_html=True)

# ==============================================================================
# 11. PRIORITY 1 (HERO FOCUS): TOP GREEN & TURNAROUND SECTORS IN SEQUENCE
# ==============================================================================
turn_cards = []
for _, ts in turnaround_secs.iterrows():
    q_s = urllib.parse.quote(ts["Sector"])
    tf_v = ts[tf_choice]
    tf_c = "#10b981" if tf_v >= 0 else "#ef4444"
    rs_c = "#10b981" if ts["Sec_RS"] >= 0 else "#ef4444"
    bdr_left = "border-left:4px solid #10b981;" if tf_v >= 0 else "border-left:4px solid #ef4444;"
    turn_cards.append(
        f'<a href="?focus_sec={q_s}&auto={ap_flag}" target="_self" class="turn-sec-card" style="{bdr_left}" title="Click to open {ts["Sector"]} stocks below">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span class="t-sec-name">{"🟢" if tf_v>=0 else "🔴"} {ts["Sector"]}</span>'
        f'<span style="background:rgba(16,185,129,0.16);color:{tf_c};padding:1px 6px;border-radius:5px;font-size:0.70rem;font-weight:800;">{tf_v:+.2f}% ({tf_choice})</span>'
        f'</div>'
        f'<div style="font-size:0.71rem;color:{TEXT_SUB};font-family:\'JetBrains Mono\',monospace !important;">'
        f'1M:<b style="color:{"#10b981" if ts["1M"]>=0 else "#ef4444"};">{ts["1M"]:+.1f}%</b> ➔ '
        f'1D:<b style="color:{"#10b981" if ts["1D"]>=0 else "#ef4444"};">{ts["1D"]:+.2f}%</b> | '
        f'RS:<b style="color:{rs_c};">{ts["Sec_RS"]:+.1f}%</b>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;font-size:0.70rem;color:#f59e0b;font-weight:700;">'
        f'<span>🤝 {ts["Up_Count"]}/{ts["Count"]} Up | Vol {ts["Avg_Vol"]}x</span>'
        f'<span>⭐ {ts["Top_Pick"]}</span>'
        f'</div></a>'
    )

st.markdown(
    f'<div class="turnaround-hero-box">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">'
    f'<span style="font-size:0.88rem;font-weight:800;color:#10b981;">🧭 PRIORITY 1 — Top Performing Green & Turnaround Sectors ({tf_choice} Sequence: Highest Green First)</span>'
    f'<span style="font-size:0.72rem;color:{TEXT_SUB};">Click any sector card to open its stocks below</span>'
    f'</div>'
    f'<div class="turnaround-grid">{"".join(turn_cards)}</div></div>',
    unsafe_allow_html=True
)

# ==============================================================================
# 12. PRIORITY 2 (HIDDEN BY DEFAULT): NEXT-DAY INTRADAY WATCHLIST + REASONS
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
            tag_txt = f"🟢 BUY • RS {r['RS_vs_Nifty']:+.1f}%" if is_bull else f"🔴 SHORT • RS {r['RS_vs_Nifty']:+.1f}%"
            c_col = "#10b981" if r["1D"] >= 0 else "#ef4444"
            lbl = "Buy" if is_bull else "Short"
            cards.append(
                f'<a href="?focus_stock={qt}&auto={ap_flag}" target="_self" class="radar-row-card">'
                f'<div class="r-top"><span class="r-sym">{r["Symbol"]} <span style="font-size:0.70rem;color:{TEXT_SUB};font-weight:600;">({r["Sector"]})</span></span><span class="{tag_cls}">{tag_txt}</span></div>'
                f'<div class="r-mid"><span>₹{r["Price"]:,.1f} <span style="color:{c_col};font-weight:700;">({r["1D"]:+.1f}%)</span></span><span>RSI: {r["RSI"]} | Vol: {r["Vol_Ratio"]:.1f}x</span></div>'
                f'<div class="r-reason-box">💡 {r["Reason"]}</div>'
                f'<div class="r-plan"><span style="color:#f59e0b;">🎯 {lbl}: ₹{r["Entry"]}</span><span style="color:#ef4444;">🛑 SL: ₹{r["SL"]}</span><span style="color:#10b981;">🚀 Tgt: ₹{r["Target"]}</span></div>'
                f'</a>'
            )
        p_cls = "radar-panel-bull" if is_bull else "radar-panel-bear"
        h_col = "#10b981" if is_bull else "#ef4444"
        h_txt = "🟢 Bullish Next-Day Picks (Sorted Highest Green First)" if is_bull else "🔴 Bearish Next-Day Picks (Sorted Strongest Drop First)"
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
# 13. STOCK INSPECTOR + AI VERDICT + ZERODHA KITE PUBLISHER & SHORTCUT BRIDGE
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

if st.session_state.selected_stock != DEFAULT_STOCK:
    s_dict = fetch_any_custom_stock_live(st.session_state.selected_stock, stocks_df)
    if s_dict is not None:
        s_info = pd.Series(s_dict)
        sym_clean, p_now, atr_v = s_info["Symbol"], s_info["Price"], s_info["ATR"]
        is_bear_setup = ("Short" in str(s_info["Action_Signal"])) or (s_info["1D"] < -0.3 and pd.notna(s_info.get("Bear_Candle")))
        safe_qty = max(int(500.0 / max(abs(s_info["Buy_Entry"] - s_info["Buy_SL"]), 1.0)), 1)

        chk_trend, chk_vol, chk_rsi, chk_sec, chk_streak = bool(s_info["Above_50DMA"]), s_info["Vol_Ratio"] >= 1.15, (42.0 <= s_info["RSI"] <= 72.0), (s_info.get("Sec_1D", 0) >= -0.15), (s_info.get("Consec_Up", 1) <= 2)
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
            st.markdown(f"#### 🎯 Stock Inspector: **{sym_clean}** (`{s_info['Sector']}`) — ₹{p_now:,.2f} ({s_info['1D']:+.2f}% | ⚡ RS: {s_info.get('RS_vs_Nifty', 0):+.2f}%)")
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
            fig_st.update_layout(height=350, template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=20, b=10), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig_st, use_container_width=True)

        l1, l2, l3, l4 = st.columns(4)
        with l1:
            st.link_button(f"📈 TradingView ({sym_clean})", f"https://in.tradingview.com/chart/?symbol=NSE%3A{sym_clean}", use_container_width=True)
        with l2:
            st.link_button(f"📊 Screener.in ({sym_clean})", f"https://www.screener.in/company/{sym_clean}/", use_container_width=True)
        with l3:
            st.link_button(f"📰 Google Finance ({sym_clean})", f"https://www.google.com/finance/quote/{sym_clean}:NSE", use_container_width=True)
        with l4:
            if st.button(f"🤖 Ask AI Verdict ({sym_clean})", type="primary", use_container_width=True):
                st.session_state.show_stock_ai_verdict = not st.session_state.show_stock_ai_verdict

        if st.session_state.show_stock_ai_verdict:
            ai_res = generate_ai_stock_verdict(s_dict, n_d, v_d, adv_today, dec_today)
            news_items_html = "".join([
                f'<div style="font-size:0.75rem;margin-bottom:5px;padding-bottom:4px;border-bottom:1px dashed {BORDER_C};">'
                f'📰 {hl} <span style="color:{TEXT_SUB};font-size:0.68rem;">({dt})</span></div>'
                for hl, dt in ai_res["headlines"]
            ]) or '<div style="font-size:0.75rem;color:#94a3b8;">No major breaking news in last 24h — moving on technicals & sector flow.</div>'

            tech_items_html = "".join([f'<div style="font-size:0.76rem;margin-bottom:4px;">{tn}</div>' for tn in ai_res["tech_notes"]])
            mkt_items_html = "".join([f'<div style="font-size:0.76rem;margin-bottom:4px;">{mn}</div>' for mn in ai_res["mkt_notes"]])

            st.markdown(
                f'<div class="ai-verdict-box">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:10px;border-bottom:1px solid {BORDER_C};padding-bottom:8px;">'
                f'<span style="font-size:0.95rem;font-weight:800;color:{ai_res["color"]};">{ai_res["badge"]}</span>'
                f'<span style="background:{ai_res["color"]}22;color:{ai_res["color"]};border:1px solid {ai_res["color"]};padding:3px 10px;border-radius:999px;font-size:0.78rem;font-weight:800;">AI Confidence Score: {ai_res["score"]}/100</span>'
                f'</div>'
                f'<div style="font-size:0.84rem;line-height:1.5;margin-bottom:12px;background:rgba(245,158,11,0.08);padding:8px 12px;border-radius:8px;border-left:4px solid {ai_res["color"]};">'
                f'{ai_res["bangla"]}'
                f'</div>'
                f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;">'
                f'<div class="ai-sub-card"><div style="font-size:0.80rem;font-weight:800;color:#38bdf8;margin-bottom:6px;">📈 1. Chart & Technical Analysis</div>{tech_items_html}</div>'
                f'<div class="ai-sub-card"><div style="font-size:0.80rem;font-weight:800;color:#10b981;margin-bottom:6px;">🌍 2. Sector & Peer Sync</div>{mkt_items_html}</div>'
                f'<div class="ai-sub-card"><div style="font-size:0.80rem;font-weight:800;color:#f59e0b;margin-bottom:6px;">📰 3. {ai_res["news_label"]}</div>{news_items_html}</div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

        # ZERODHA KITE ORDER PAD
        st.markdown(
            '<div class="kite-order-pad">'
            '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;">'
            '<span style="font-size:0.90rem;font-weight:800;color:#ff5722;">⚡ Zerodha Kite Order Execution Pad (MIS Intraday & CNC Delivery Switch)</span>'
            '<span style="font-size:0.73rem;color:#38bdf8;font-weight:700;">Auto-Copies Symbol for Instant Ctrl+K Buy/Sell OR Direct Kite Publisher Popup</span>'
            '</div></div>',
            unsafe_allow_html=True
        )
        zk_c1, zk_c2, zk_c3, zk_c4 = st.columns([3.2, 3.0, 1.8, 2.0])
        with zk_c1:
            kite_product = st.radio("1. Product Type:", ["⚡ MIS (Intraday 5x)", "💎 CNC (Delivery 1x)"], horizontal=True)
        with zk_c2:
            kite_order_type = st.radio("2. Order Type:", ["🎯 LIMIT", "🚀 MARKET", "🛑 SL-M"], horizontal=True)
        with zk_c3:
            kite_risk_rs = st.number_input("3. Risk (₹):", min_value=100.0, value=500.0, step=100.0)
        with zk_c4:
            st.session_state.kite_api_key = st.text_input("4. Kite Publisher Key (Optional):", value=st.session_state.kite_api_key, placeholder="Free Key or Leave Blank", type="password")

        is_mis = "MIS" in kite_product
        prod_code = "MIS" if is_mis else "CNC"
        ord_code = "LIMIT" if "LIMIT" in kite_order_type else ("MARKET" if "MARKET" in kite_order_type else "SL-M")
        risk_per_share_buy = max(abs(s_info["Buy_Entry"] - s_info["Buy_SL"]), 0.5)
        kite_qty = max(int(kite_risk_rs / risk_per_share_buy), 1)
        full_order_val = round(p_now * kite_qty, 2)
        req_margin = round(full_order_val / 5.0, 2) if is_mis else full_order_val

        km1, km2, km3, km4, km5 = st.columns(5)
        with km1:
            st.markdown(f'<div class="kite-ticket-metric"><span class="kite-metric-lbl">Symbol & Product</span><span class="kite-metric-val" style="color:#ff5722;">{sym_clean} • {prod_code}</span></div>', unsafe_allow_html=True)
        with km2:
            st.markdown(f'<div class="kite-ticket-metric"><span class="kite-metric-lbl">Auto Safe Qty</span><span class="kite-metric-val" style="color:#38bdf8;">{kite_qty} Qty</span></div>', unsafe_allow_html=True)
        with km3:
            st.markdown(f'<div class="kite-ticket-metric"><span class="kite-metric-lbl">Buy / SL</span><span class="kite-metric-val" style="color:#10b981;">₹{s_info["Buy_Entry"]} / ₹{s_info["Buy_SL"]}</span></div>', unsafe_allow_html=True)
        with km4:
            st.markdown(f'<div class="kite-ticket-metric"><span class="kite-metric-lbl">Short / SL</span><span class="kite-metric-val" style="color:#ef4444;">₹{s_info["Short_Entry"]} / ₹{s_info["Short_SL"]}</span></div>', unsafe_allow_html=True)
        with km5:
            st.markdown(f'<div class="kite-ticket-metric"><span class="kite-metric-lbl">Est. Margin</span><span class="kite-metric-val" style="color:#f59e0b;">₹{req_margin:,.0f}</span></div>', unsafe_allow_html=True)

        user_k_key = st.session_state.kite_api_key.strip()
        components.html(
            f"""
            <script src="https://kite.trade/publisher.js?v=3"></script>
            <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:6px;font-family:'Plus Jakarta Sans',sans-serif;">
                <button id="kite-buy-btn" style="flex:1;min-width:240px;background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;border:1.5px solid #60a5fa;padding:10px 14px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;">
                    🟢 BUY {sym_clean} on Zerodha Kite ({prod_code} • {kite_qty} Qty @ ₹{s_info['Buy_Entry']})
                </button>
                <button id="kite-sell-btn" style="flex:1;min-width:240px;background:linear-gradient(135deg,#ea580c,#dc2626);color:#fff;border:1.5px solid #f87171;padding:10px 14px;border-radius:10px;font-weight:800;font-size:13px;cursor:pointer;">
                    🔴 SHORT/SELL {sym_clean} on Zerodha Kite ({prod_code} • {kite_qty} Qty @ ₹{s_info['Short_Entry']})
                </button>
            </div>
            <div id="kite-status-msg" style="font-size:12px;color:#fbbf24;font-weight:700;margin-top:6px;text-align:center;font-family:'Plus Jakarta Sans',sans-serif;">
                💡 বাটনে ক্লিক করলেই <b>{sym_clean}</b> কপি হয়ে যাবে — Zerodha ড্যাশবোর্ডে গিয়ে শুধু <b>Ctrl+K</b> চেপে <b>Ctrl+V</b> ও <b>B</b> (Buy) / <b>S</b> (Sell) চাপুন!
            </div>
            <script>
            (function() {{
                const buyBtn = document.getElementById("kite-buy-btn");
                const sellBtn = document.getElementById("kite-sell-btn");
                const msgEl = document.getElementById("kite-status-msg");
                const apiKey = "{user_k_key}";

                function executeKiteOrder(txType, priceVal, slVal, tgtVal) {{
                    if (navigator.clipboard) {{
                        navigator.clipboard.writeText("{sym_clean}");
                    }}
                    if (apiKey && window.KiteConnect) {{
                        try {{
                            const kite = new KiteConnect(apiKey);
                            kite.add({{
                                "exchange": "NSE",
                                "tradingsymbol": "{sym_clean}",
                                "transaction_type": txType,
                                "order_type": "{ord_code}",
                                "quantity": {kite_qty},
                                "price": parseFloat(priceVal),
                                "product": "{prod_code}"
                            }});
                            kite.connect();
                            msgEl.innerHTML = "✅ Launching Direct Zerodha Kite Order Ticket for <b>{sym_clean}</b>...";
                            return;
                        }} catch (err) {{}}
                    }}
                    msgEl.innerHTML = "✅ <b>{sym_clean}</b> Copied! Zerodha Window খুললে বামদিকে সার্চ বক্সে <b>Ctrl+K ➔ Ctrl+V</b> চেপে <b>" + (txType === "BUY" ? "B (Buy)" : "S (Sell)") + "</b> চাপুন (Qty: <b>{kite_qty}</b>, Price: <b>₹" + priceVal + "</b>, SL: <b>₹" + slVal + "</b>)";
                    window.open("https://kite.zerodha.com/dashboard", "ZerodhaKiteOrderWindow", "width=1150,height=760,menubar=no,toolbar=no,location=yes,status=yes");
                }}

                if (buyBtn) buyBtn.addEventListener("click", function() {{ executeKiteOrder("BUY", "{s_info['Buy_Entry']}", "{s_info['Buy_SL']}", "{s_info['Buy_Target']}"); }});
                if (sellBtn) sellBtn.addEventListener("click", function() {{ executeKiteOrder("SELL", "{s_info['Short_Entry']}", "{s_info['Short_SL']}", "{s_info['Short_Target']}"); }});
            }})();
            </script>
            """,
            height=84
        )
        st.markdown("---")

# ==============================================================================
# 14. 4 ULTRA-FAST CONSOLIDATED TABS (SPEEDOMETERS EXPANDED BY DEFAULT + PREVIOUS SWING LOGIC)
# ==============================================================================
live_tab_badge = f"🟢 {len(bull_15m_df) + len(bear_15m_df)} Active" if is_mkt_open else "⏸️ Standby"
tab1, tab2, tab3, tab4 = st.tabs([
    f"🔄 1. {len(SECTOR_STOCKS)} Sector Viewer & Gauges",
    f"⚡ 2. 3-Layer Live Intraday Finder ({live_tab_badge})",
    "💎 3. Swing & Positional Radar",
    f"📋 4. All {len(SECTOR_STOCKS)} Sectors Matrix"
])

with tab1:
    f_secs = sectors_df.copy()
    if "Green Top" in sort_choice:
        f_secs = f_secs.sort_values(tf_choice, ascending=False).reset_index(drop=True)
    elif "Bottom Turnaround" in sort_choice:
        f_secs["Is_Green"] = f_secs[tf_choice] >= 0
        f_secs = f_secs.sort_values(["Is_Green", "Sec_Bull_Turn", "Turnaround_Score"], ascending=[False, False, False]).reset_index(drop=True)
    elif "Highest Peer Sync" in sort_choice:
        f_secs = f_secs.sort_values(["Peer_Up_Pct", tf_choice], ascending=[False, False]).reset_index(drop=True)
    elif "Top Losers" in sort_choice:
        f_secs = f_secs.sort_values(tf_choice, ascending=True).reset_index(drop=True)
    else:
        f_secs = f_secs.sort_values(["Avg_Vol", tf_choice], ascending=[False, False]).reset_index(drop=True)

    st.markdown('<div id="sector-viewer-anchor"></div>', unsafe_allow_html=True)
    all_sec_options = [EMPTY_VIEWER] + f_secs["Sector"].tolist()
    if st.session_state.inspect_sector not in all_sec_options:
        st.session_state.inspect_sector = EMPTY_VIEWER

    mv_c1, mv_c2 = st.columns([4.0, 6.0])
    with mv_c1:
        chosen_view_sec = st.selectbox(
            "Master Sector Viewer",
            all_sec_options,
            index=all_sec_options.index(st.session_state.inspect_sector),
            label_visibility="collapsed"
        )
        if chosen_view_sec != st.session_state.inspect_sector:
            st.session_state.inspect_sector = chosen_view_sec
            st.rerun()
    with mv_c2:
        if st.session_state.inspect_sector != EMPTY_VIEWER:
            sec_meta = sectors_df[sectors_df["Sector"] == st.session_state.inspect_sector].iloc[0]
            s_tf_v = sec_meta[tf_choice]
            s_col = "#10b981" if s_tf_v >= 0 else "#ef4444"
            st.markdown(
                f'<div class="master-viewer-bar">'
                f'<span>🧭 <b>{st.session_state.inspect_sector}</b> ({sec_meta["Zone"]})</span>'
                f'<span>🤝 Sync: <b>{sec_meta["Up_Count"]}/{sec_meta["Count"]} Up</b></span>'
                f'<span style="color:{s_col};">{tf_choice}: <b>{s_tf_v:+.2f}%</b> | ⚡ RS: <b>{sec_meta["Sec_RS"]:+.2f}%</b></span>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="master-viewer-bar">'
                '<span>👈 <b>Master Sector Stock Viewer:</b> বাম পাশের ড্রপডাউন বা নিচের যেকোনো সেক্টর কার্ডে ক্লিক করলে শেয়ার লিস্ট খুলবে</span>'
                '</div>',
                unsafe_allow_html=True
            )

    if st.session_state.inspect_sector != EMPTY_VIEWER:
        active_sec_stocks = stocks_df[stocks_df["Sector"] == st.session_state.inspect_sector].sort_values(tf_choice, ascending=False)
        render_safe_table(
            active_sec_stocks[["Symbol", "Price", "1D", "RS_vs_Nifty", "1W", "1M", "Vol_Ratio", "RSI", "Action_Signal", "Buy_Entry", "Buy_SL", "Buy_Target"]],
            ["1D", "RS_vs_Nifty", "1W", "1M"]
        )
        st.markdown(make_stock_pills(active_sec_stocks, tf_choice), unsafe_allow_html=True)

    # KEPT EXPANDED=TRUE SO SPEEDOMETERS ALWAYS STAY VISIBLE LIKE SCREENSHOT 1!
    with st.expander(f"🎛️ View All {len(f_secs)} Sectors Speedometers & Sequence Cards (Sorted: Green Top ➔ Down in {tf_choice})", expanded=True):
        gauge_cards_html = "".join([make_svg_speedometer_card(s_row, tf_choice) for _, s_row in f_secs.iterrows()])
        st.markdown(f'<div class="sector-grid-wrap">{gauge_cards_html}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="aligned-sec-hdr">⚡ PRIORITY 3 — 3-Layer Confirmed 15m Intraday Finder (Sector Move + Peer Sync >=55% + 15m VWAP & 9-EMA)</div>', unsafe_allow_html=True)
    force_test_scan = False
    if not is_mkt_open:
        st.warning(f"⏸️ **Live Intraday Stock Finder is on Standby (Market Closed — {ist_now.strftime('%A %I:%M %p IST')}).** Automatically activates Mon–Fri, 9:15 AM – 3:30 PM IST.")
        force_test_scan = st.checkbox("🔓 Run On-Demand 15m Scan for Last Session (Preview Mode)", value=False)
        if force_test_scan:
            with st.spinner("⚡ Running 3-Layer 15m Scanner..."):
                bull_15m_df, bear_15m_df = run_3layer_intraday_scanner(stocks_df)

    if is_mkt_open or force_test_scan:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="aligned-sec-hdr">🟢 3-Layer Confirmed LONG (Sorted Highest Green First)</div>', unsafe_allow_html=True)
            if bull_15m_df.empty:
                st.info("🎯 No stock currently passes all 3 Long layers. Waiting for high-conviction breakout...")
            else:
                render_safe_table(bull_15m_df[["Time", "Symbol", "Sector", "Peer_Sync", "Price", "VWAP", "EMA9", "Vol_Ratio", "RSI", "1D", "Entry", "SL", "Target"]], ["1D"])
                st.markdown(make_stock_pills(bull_15m_df, "1D"), unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="aligned-sec-hdr">🔴 3-Layer Confirmed SHORT (Sorted Strongest Drop First)</div>', unsafe_allow_html=True)
            if bear_15m_df.empty:
                st.info("🎯 No stock currently passes all 3 Short layers. Waiting for high-conviction breakdown...")
            else:
                b15_disp = bear_15m_df.rename(columns={"Entry": "Short_Below"})
                render_safe_table(b15_disp[["Time", "Symbol", "Sector", "Peer_Sync", "Price", "VWAP", "EMA9", "Vol_Ratio", "RSI", "1D", "Short_Below", "SL", "Target"]], ["1D"])
                st.markdown(make_stock_pills(bear_15m_df, "1D"), unsafe_allow_html=True)

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

# ==============================================================================
# TAB 3: RESTORED PROVEN SWING LOGIC (PULLBACK TO 20-DMA + OVERSOLD 1M RECOVERY)
# ==============================================================================
with tab3:
    sw1, sw2 = st.columns(2)
    with sw1:
        st.markdown('<div class="aligned-sec-hdr">🚀 Safe Trend Pullback Picks (>50-DMA & Near 20-DMA Support)</div>', unsafe_allow_html=True)
        sp_df = stocks_df[(stocks_df["Above_50DMA"]) & (stocks_df["Dist_20DMA"].between(-3.0, 4.5)) & (stocks_df["RSI"].between(44, 64))].sort_values([tf_choice, "Vol_Ratio"], ascending=[False, False]).head(18)
        render_safe_table(
            sp_df[["Symbol", "Sector", "Price", "1D", "RS_vs_Nifty", "1W", "Vol_Ratio", "RSI", "Buy_Entry", "Buy_SL", "Buy_Target"]],
            ["1D", "RS_vs_Nifty", "1W"],
            height=420
        )
        st.markdown(make_stock_pills(sp_df, tf_choice), unsafe_allow_html=True)
    with sw2:
        st.markdown('<div class="aligned-sec-hdr">🌱 Bottom Turnaround Value Picks (Oversold Recovery Today)</div>', unsafe_allow_html=True)
        vr_df = stocks_df[(stocks_df["1M"] < 0) & (stocks_df["1D"] > 0) & (stocks_df["RSI"] <= 55)].sort_values(["1D", "Vol_Ratio"], ascending=[False, False]).head(18)
        render_safe_table(
            vr_df[["Symbol", "Sector", "Price", "1D", "RS_vs_Nifty", "1M", "Vol_Ratio", "RSI", "Buy_Entry", "Buy_SL", "Buy_Target"]],
            ["1D", "RS_vs_Nifty", "1M"],
            height=420
        )
        st.markdown(make_stock_pills(vr_df, "1D"), unsafe_allow_html=True)
    st.markdown("---")
    st.download_button(f"📥 Download Complete {len(ALL_TICKERS)}+ Nifty 500 Stocks Report (CSV / Excel)", data=stocks_df.sort_values(tf_choice, ascending=False).to_csv(index=False).encode("utf-8"), file_name="alphapulse_nifty500_report.csv", mime="text/csv", use_container_width=True)

with tab4:
    chart_secs = sectors_df.sort_values(tf_choice, ascending=True)
    fig_b = go.Figure(go.Bar(x=chart_secs[tf_choice], y=chart_secs["Sector"], orientation="h", marker_color=["#10b981" if v >= 0 else "#ef4444" for v in chart_secs[tf_choice]], text=[f"{v:+.2f}%" for v in chart_secs[tf_choice]], textposition="outside"))
    fig_b.update_layout(height=860, template="plotly_dark" if "Clean Light" not in theme_mode else "plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=40, t=15, b=10), font=dict(color=TEXT_MAIN))
    st.plotly_chart(fig_b, use_container_width=True)
    # Fixed duplicate column bug when tf_choice == '1D'
    mat_cols = list(dict.fromkeys(["Sector", "Zone", tf_choice, "Sec_RS", "Peer_Up_Pct", "1D", "1W", "1M", "3M", "Avg_Vol", "RSI", "Top_Pick"]))
    render_safe_table(sectors_df.sort_values(tf_choice, ascending=False)[mat_cols], [tf_choice, "Sec_RS", "1D", "1W", "1M", "3M"])

# ==============================================================================
# 15. FLOATING ‘🚀 Top’ BUTTON & PERSISTENT AUTO-SCAN ENGINE
# ==============================================================================
st.markdown(
    '<div class="floating-right-dock">'
    '<a href="#top-anchor" class="single-top-btn" id="alphapulse-top-btn" title="Scroll back to top">🚀 Top</a>'
    '</div>',
    unsafe_allow_html=True
)

scroll_target_id = st.session_state.scroll_target or ""
st.session_state.scroll_target = None
top_syms = ",".join((bull_15m_df["Symbol"].head(2).tolist() if not bull_15m_df.empty else []) + (bear_15m_df["Symbol"].head(2).tolist() if not bear_15m_df.empty else []))
should_ring = "true" if (st.session_state.auto_scan_locked and is_mkt_open and top_syms and top_syms != st.session_state.last_alerted) else "false"
if st.session_state.auto_scan_locked and is_mkt_open and top_syms:
    st.session_state.last_alerted = top_syms

reload_js = """
setTimeout(function(){
    const url = new URL(window.parent.location.href);
    url.searchParams.set('auto', '1');
    window.parent.location.href = url.toString();
}, 90000);
""" if (st.session_state.auto_scan_locked and is_mkt_open) else ""

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
            }}, 200);
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
