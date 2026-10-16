import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# ==============================================================================
# ১. পেজ সেটআপ (সুপার-ফাস্ট ফিনান্সিয়াল টার্মিনাল মোড)
# ==============================================================================
st.set_page_config(
    page_title="AlphaPulse Pro | Institutional Screener",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    header[data-testid="stHeader"] { display: none !important; }
    section[data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 100% !important; }
    .pro-card { background-color: #111827; border: 1px solid #334155; border-radius: 14px; padding: 16px; margin-bottom: 12px; }
    .kpi-card { background-color: #111827; border: 1px solid #334155; border-top: 4px solid #38bdf8; border-radius: 12px; padding: 12px; margin-bottom: 6px; }
    .kpi-title { font-size: 12.5px; font-weight: 700; color: #94a3b8; }
    .kpi-main { font-size: 19px; font-weight: 800; color: #f8fafc; margin: 4px 0; }
    .badge-green { background: rgba(0, 230, 118, 0.15); color: #00e676; padding: 3px 10px; border-radius: 99px; font-weight: 800; font-size: 13px; }
    .badge-red { background: rgba(255, 82, 82, 0.15); color: #ff5252; padding: 3px 10px; border-radius: 99px; font-weight: 800; font-size: 13px; }
    .action-btn { display: inline-block; padding: 4px 10px; margin: 2px 4px 2px 0; border-radius: 6px; font-size: 12px; font-weight: 700; text-decoration: none !important; border: 1px solid #334155; background: #1e293b; color: #38bdf8 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 🧭 AlphaPulse Pro — Institutional Sector & Stock Terminal")

# ==============================================================================
# ২. সেক্টর ও নিফটি ৫০ স্টক লিস্ট
# ==============================================================================
sectors = {
    "Defence & Aerospace": ["HAL.NS", "BEL.NS", "BDL.NS", "MAZDOCK.NS", "DATAPATTNS.NS", "PARAS.NS"],
    "Shipbuilding & Marine": ["MAZDOCK.NS", "COCHINSHIP.NS", "GRSE.NS", "SCI.NS", "GEESHIP.NS"],
    "Railways & Wagons": ["RVNL.NS", "IRFC.NS", "TITAGARH.NS", "JWL.NS", "IRCON.NS", "TEXRAIL.NS", "BEML.NS"],
    "Cables & Wires": ["POLYCAB.NS", "KEI.NS", "FINCABLES.NS", "RRKABEL.NS", "UNIVERSAL.NS"],
    "Transformers & Power T&D": ["CGPOWER.NS", "ABB.NS", "SIEMENS.NS", "TARIL.NS", "VOLTAMP.NS"],
    "EMS (Electronics Mfg)": ["DIXON.NS", "KAYNES.NS", "SYRMA.NS", "CYIENTDLM.NS", "AMBER.NS", "PGEL.NS"],
    "Green Energy & Solar": ["IREDA.NS", "SUZLON.NS", "KPIGREEN.NS", "WAAREEENER.NS", "BORORENEW.NS", "INOXWIND.NS"],
    "Power Utilities & Finance": ["PFC.NS", "RECLTD.NS", "POWERGRID.NS", "NTPC.NS", "TATAPOWER.NS", "JSWENERGY.NS"],
    "Cooling, HVAC & Data Center": ["VOLTAS.NS", "BLUESTARCO.NS", "KIRLOSENG.NS", "TRITURBINE.NS", "ANUP.NS", "ELGIEQUIP.NS"],
    "CNC, Bearings & Precision Engg": ["SKFINDIA.NS", "TIMKEN.NS", "SCHAEFFLER.NS", "THERMAX.NS", "CUMMINSIND.NS", "MTARTECH.NS"],
    "Pre-Engineered & Infra EPC": ["LT.NS", "KPIL.NS", "KEC.NS", "PENNARIND.NS", "NCC.NS", "PNCINFRA.NS"],
    "Real Estate & Developers": ["DLF.NS", "MACROTECH.NS", "PRESTIGE.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "BRIGADE.NS"],
    "Building Materials (Pipes & Sanitary)": ["ASTRAL.NS", "SUPREMEIND.NS", "CERA.NS", "KAJARIACER.NS", "CENTURYPLY.NS", "FINPIPE.NS"],
    "CDMO & API Pharma": ["LAURUSLABS.NS", "DIVISLAB.NS", "NEULANDLAB.NS", "SYNGENE.NS", "SUVENPHAR.NS", "PIRAMALPH.NS"],
    "Largecap & US Generics Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "LUPIN.NS", "AUROPHARMA.NS", "ZYDUSLIFE.NS"],
    "Hospitals & Diagnostics": ["APOLLOHOSP.NS", "MAXHEALTH.NS", "LALPATHLAB.NS", "NH.NS", "METROPOLIS.NS", "FORTIS.NS"],
    "QSR & Food Chains": ["JUBLFOOD.NS", "DEVYANI.NS", "WESTLIFE.NS", "RBA.NS", "SAPPHIRE.NS"],
    "FMCG Staples": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS", "TATACONSUM.NS", "DABUR.NS", "MARICO.NS"],
    "Retail, Apparel & Footwear": ["TRENT.NS", "DMART.NS", "METROBRAND.NS", "BATAINDIA.NS", "MANYAVAR.NS", "PAGEIND.NS"],
    "Jewellery & Luxury": ["TITAN.NS", "KALYANKJIL.NS", "SENCO.NS", "THANGAMAYL.NS"],
    "Auto OEMs & EV": ["M&M.NS", "TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "TVSMOTOR.NS", "OLECTRA.NS", "EICHERMOT.NS"],
    "Auto Ancillaries & Tyres": ["MOTHERSON.NS", "SONACOMS.NS", "UNOMINDA.NS", "MRF.NS", "BALKRISIND.NS", "APOLLOTYRE.NS"],
    "IT Largecap": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"],
    "IT Midcap & Niche Tech": ["PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS", "ZENSARTECH.NS", "AFFLE.NS"],
    "PSU Banks": ["SBIN.NS", "PNB.NS", "BANKBARODA.NS", "CANBK.NS", "UNIONBANK.NS", "INDIANB.NS"],
    "Private Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "FEDERALBNK.NS"],
    "NBFCs & Housing Finance": ["BAJFINANCE.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "LICHSGFIN.NS", "MANAPPURAM.NS"],
    "Capital Market & Wealth": ["BSE.NS", "CDSL.NS", "MCX.NS", "ANGELONE.NS", "MOTILALOFS.NS", "CAMS.NS"],
    "Specialty Chemicals & Agrochem": ["SRF.NS", "PIIND.NS", "NAVINFLUOR.NS", "DEEPAKNTR.NS", "AARTIIND.NS", "CLEAN.NS"],
    "Packaging & BOPP Films": ["UFLEX.NS", "JINDALPOLY.NS", "COSMOFIRST.NS", "EPL.NS", "MOLDTKPAC.NS"],
    "Hotels & Aviation": ["INDIGO.NS", "INDHOTEL.NS", "EIHOTEL.NS", "LEMONTREE.NS", "CHALET.NS"],
    "Metals & Mining": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "COALINDIA.NS", "VEDL.NS", "NMDC.NS"],
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
all_tickers = sorted(list(set([benchmark] + NIFTY_50_TICKERS + [t for s in sectors.values() for t in s])))

# ==============================================================================
# ৩. কন্ট্রোল প্যানেল
# ==============================================================================
col1, col2, col3 = st.columns([1, 1.5, 1.5])
with col1:
    tf_option = st.selectbox("📅 টাইমফ্রেম:", ["1D", "1W", "1M", "3M", "6M", "1Y"], index=1)
with col2:
    sort_option = st.selectbox("🔃 সাজানোর ক্রম:", ["Top Gainers First", "Top Losers First", "Turnaround Reversal First"])
with col3:
    selected_sector = st.selectbox("🔍 নির্দিষ্ট সেক্টর:", ["সব সেক্টর একসাথে (All)"] + sorted(list(sectors.keys())))

ret_key = f"{tf_option} %"
tf_days_map = {"1D": 2, "1W": 6, "1M": 22, "3M": 64, "6M": 126, "1Y": 252}

# ==============================================================================
# ৪. ডেটা ইঞ্জিন (সুপার ফাস্ট ফেচিং)
# ==============================================================================
@st.cache_data(ttl=3600)
def load_market_data():
    raw = yf.download(all_tickers, period="2y", interval="1d", auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        close_df = raw["Close"].ffill() if "Close" in raw.columns.levels[0] else pd.DataFrame()
        high_df = raw["High"].ffill() if "High" in raw.columns.levels[0] else close_df.copy()
        low_df = raw["Low"].ffill() if "Low" in raw.columns.levels[0] else close_df.copy()
        vol_df = raw["Volume"].fillna(0) if "Volume" in raw.columns.levels[0] else pd.DataFrame()
    else:
        close_df = raw.ffill()
        high_df = close_df.copy()
        low_df = close_df.copy()
        vol_df = pd.DataFrame(index=close_df.index)
    return close_df, high_df, low_df, vol_df

with st.spinner("মার্কেট ডেটা এবং টেকনিক্যাল স্ক্যানার লোড হচ্ছে..."):
    df_close, df_high, df_low, df_vol = load_market_data()

def calc_ret(series, days):
    s = series.dropna()
    if len(s) < 2: return 0.0
    sub = s.tail(min(days, len(s)))
    if len(sub) < 2 or sub.iloc[0] == 0: return 0.0
    return round(((sub.iloc[-1] / sub.iloc[0]) - 1) * 100, 2)

def calc_rsi(series, period=14):
    s = series.dropna()
    if len(s) < period + 2: return 50.0
    delta = s.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    lg = float(gain.iloc[-1]) if not pd.isna(gain.iloc[-1]) else 0.0
    ll = float(loss.iloc[-1]) if not pd.isna(loss.iloc[-1]) else 0.0
    if ll == 0: return 100.0 if lg > 0 else 50.0
    return round(100.0 - (100.0 / (1.0 + (lg / ll))), 1)

# ==============================================================================
# ৫. সেক্টর ও স্টক প্রসেসিং
# ==============================================================================
sector_master = []
all_stocks_list = []

for s_name, tickers in sectors.items():
    valid = [t for t in tickers if t in df_close.columns and len(df_close[t].dropna()) > 5]
    if not valid: continue

    st_rows = []
    for t in valid:
        s_ser = df_close[t].dropna()
        curr_p = round(float(s_ser.iloc[-1]), 2)
        h_ser = df_high[t].dropna() if t in df_high.columns else s_ser
        l_ser = df_low[t].dropna() if t in df_low.columns else s_ser
        
        dh = float(h_ser.iloc[-1]) if len(h_ser) > 0 else curr_p
        dl = float(l_ser.iloc[-1]) if len(l_ser) > 0 else curr_p
        dr = max(dh - dl, 0.01)
        clv = round(float(np.clip(((curr_p - dl) / dr) * 100.0, 0.0, 100.0)), 1)

        r1d = calc_ret(s_ser, 2)
        r1w = calc_ret(s_ser, 6)
        r1m = calc_ret(s_ser, 22)
        r3m = calc_ret(s_ser, 64)
        r1y = calc_ret(s_ser, 252)
        rsi = calc_rsi(s_ser, 14)

        # ক্যান্ডেল প্যাটার্ন ডিটেকশন (Doji / Hammer / Reversal)
        body = abs(curr_p - float(s_ser.iloc[-2])) if len(s_ser) >= 2 else 0
        is_doji = (body / dr) <= 0.25
        is_hammer = (min(curr_p, float(s_ser.iloc[-2])) - dl) >= (dr * 0.5) and clv >= 60

        pat = "Doji Reversal" if is_doji else ("Hammer" if is_hammer else "Standard")

        row = {
            "Ticker": t, "Stock": t.replace(".NS", ""), "Sector": s_name,
            "CMP (₹)": curr_p, "1D %": r1d, "1W %": r1w, "1M %": r1m, "3M %": r3m, "1Y %": r1y,
            "RSI (14)": rsi, "Pattern": pat, "CLV %": clv,
            "Is_Nifty50": t in NIFTY_50_TICKERS
        }
        st_rows.append(row)
        all_stocks_list.append(row)

    st_df = pd.DataFrame(st_rows)
    s_ret = round(float(st_df[ret_key].mean()), 2)
    sector_master.append({"Sector": s_name, "Return": s_ret, "stocks_df": st_df, "valid": valid})

all_stocks_df = pd.DataFrame(all_stocks_list)

# ==============================================================================
# ৬. মেইন ট্যাবসমূহ (কোনো জটিল HTML বা SyntaxError ছাড়া ১০০% ক্লিন)
# ==============================================================================
tab1, tab2, tab3 = st.tabs([
    "🧭 ১. সেক্টর ও মার্কেট ড্যাশবোর্ড",
    "⚡ ২. ইন্ট্রাডে ডোজি/হ্যামার রাডার",
    "📈 ৩. সিঙ্গেল স্টক চার্ট"
])

with tab1:
    st.subheader("📊 সেক্টর পারফরম্যান্স ও মোমেন্টাম টার্মিনাল")
    
    if selected_sector != "সব সেক্টর একসাথে (All)":
        display_secs = [s for s in sector_master if s["Sector"] == selected_sector]
    else:
        display_secs = sorted(sector_master, key=lambda x: x["Return"], reverse=("Top Gainers" in sort_option))

    cols = st.columns(2)
    for idx, sec in enumerate(display_secs):
        with cols[idx % 2]:
            s_nm = sec["Sector"]
            s_rt = sec["Return"]
            st_tbl = sec["stocks_df"].sort_values(by=ret_key, ascending=False).reset_index(drop=True)
            
            badge = "badge-green" if s_rt >= 0 else "badge-red"
            st.markdown(f"""
            <div class="pro-card">
                <div style="display:flex; justify-content:space-between;">
                    <b style="font-size:18px; color:#f8fafc;">#{idx+1} {s_nm}</b>
                    <span class="{badge}">{s_rt:+.2f}% ({tf_option})</span>
                </div>
            </div>""", unsafe_allow_html=True)

            with st.expander(f"🔍 {s_nm}-এর শেয়ার তালিকা দেখুন ({len(st_tbl)}টি)"):
                st.dataframe(st_tbl[["Stock", "CMP (₹)", "RSI (14)", "Pattern", "1D %", "1W %", "1M %"]], use_container_width=True, hide_index=True)
                for _, r in st_tbl.iterrows():
                    stk = r["Stock"]
                    st.markdown(f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{stk}" target="_blank">📈 {stk} (TV)</a>', unsafe_allow_html=True)

with tab2:
    st.subheader("⚡ আগামীকালের ইন্ট্রাডে রিভার্সাল ও ডোজি/হ্যামার ফোকাস")
    st.markdown("যে শেয়ারগুলো গত কয়েক দিন পতনের পর আজ সাপোর্টে ডোজি বা হ্যামার ক্যান্ডেল তৈরি করেছে:")
    
    bull_intraday = all_stocks_df[(all_stocks_df["1W %"] < 4.0) & (all_stocks_df["Pattern"].isin(["Doji Reversal", "Hammer"]))]
    if bull_intraday.empty:
        bull_intraday = all_stocks_df.sort_values(by="1D %", ascending=False).head(10)

    st.dataframe(bull_intraday[["Stock", "Sector", "CMP (₹)", "Pattern", "RSI (14)", "1D %", "1W %"]], use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📈 সিঙ্গেল স্টক প্রাইস চার্ট ও অ্যানালাইসিস")
    s1, s2 = st.columns(2)
    with s1:
        chosen_sec = st.selectbox("সেক্টর বেছে নিন:", list(sectors.keys()), key="t3_sec")
    with s2:
        stks = [t.replace(".NS", "") for t in sectors[chosen_sec] if t in df_close.columns]
        chosen_stk = st.selectbox("শেয়ার বেছে নিন:", stks, key="t3_stk")

    if chosen_stk:
        sym = chosen_stk + ".NS"
        s_ser = df_close[sym].dropna()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=s_ser.index, y=s_ser, name=chosen_stk, line=dict(color="#38bdf8", width=2.5)))
        fig.update_layout(paper_bgcolor="#111827", plot_bgcolor="#111827", font=dict(color="#f8fafc"), height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{chosen_stk}" target="_blank">📈 TradingView-তে পূর্ণাঙ্গ চার্ট খুলুন</a>', unsafe_allow_html=True)
