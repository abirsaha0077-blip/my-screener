import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf

# ==============================================================================
# ১. পেজ সেটআপ (বাই-ডিফল্ট ডার্ক থিম)
# ==============================================================================
st.set_page_config(
    page_title="AlphaPulse Pro | Institutional Sector & Stock Terminal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# ২. ৩২টি মাইক্রো-সেক্টর এবং নিফটি ৫০ স্টক লিস্ট
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

# নিফটি ৫০-এর মূল স্টকগুলোর সুনির্দিষ্ট তালিকা (নিফটি মুভার্সের জন্য)
nifty50_symbols = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "HINDUNILVR.NS",
    "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS", "LTIM.NS", "AXISBANK.NS",
    "ASIANPAINT.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "BAJFINANCE.NS", "HCLTECH.NS",
    "WIPRO.NS", "ADANIENT.NS", "ULTRACEMCO.NS", "NTPC.NS", "POWERGRID.NS", "TATASTEEL.NS",
    "M&M.NS", "JSWSTEEL.NS", "ADANIPORTS.NS", "COALINDIA.NS", "GRASIM.NS", "SBILIFE.NS"
]

benchmark = "^NSEI"
all_tickers = sorted(list(set([benchmark] + [t for s in sectors.values() for t in s])))

# ==============================================================================
# ৩. সাইডবার মেনু (বাই-ডিফল্ট ডার্ক থিম ও ক্লিয়ার টগল বাটন)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎛️ থিম ও ডিসপ্লে সেটিংস")
    theme_choice = st.selectbox(
        "🎨 প্রিমিয়াম থিম (Select Theme):",
        [
            "🌙 Obsidian Pro Dark (ডার্ক হাই-কনট্রাস্ট থিম)",
            "💎 Royal Frost Blue (সফট ব্লু প্রিমিয়াম)",
            "☀️ Pure White Luxury (সাদা প্রিমিয়াম থিম)",
        ],
        index=0,
    )
    show_card_meter = st.toggle("🎛️ কার্ডে অ্যানালগ মিটার দেখান", value=True)
    auto_close_sec = st.slider("⏱️ মেনু অটো-ক্লোজ সময় (সেকেন্ড):", 2, 15, 3)
    st.markdown("---")
    st.markdown("#### 📌 মিটার স্কোর গাইড")
    st.markdown(
        "- **🟢 65–100:** Strong Green Leader\n"
        "- **🔄 48–65:** Red ➔ Green Turnaround\n"
        "- **🟡 35–48:** Yellow Watchlist Zone\n"
        "- **🔴 0–35:** Deep Value / Red Zone"
    )

components.html(
    f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        let closeTimer = null;

        function collapseSidebarNow() {{
            if (doc.querySelector('div[data-baseweb="popover"]')) return;
            const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
            if (sidebar && sidebar.getAttribute('aria-expanded') === 'true') {{
                const closeBtn =
                    doc.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
                    doc.querySelector('[data-testid="stSidebarHeader"] button') ||
                    sidebar.querySelector('button[kind="headerNoPadding"]') ||
                    sidebar.querySelector('button[kind="header"]') ||
                    sidebar.querySelector('button');
                if (closeBtn) closeBtn.click();
            }}
        }

        function attachAutoClose() {{
            const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
            if (sidebar && !sidebar.dataset.boundAutoClose) {{
                sidebar.dataset.boundAutoClose = "true";
                sidebar.addEventListener('mouseleave', () => {{
                    clearTimeout(closeTimer);
                    closeTimer = setTimeout(collapseSidebarNow, {auto_close_sec * 1000});
                }});
                sidebar.addEventListener('mouseenter', () => {{
                    clearTimeout(closeTimer);
                }});
            }}
        }
        setInterval(attachAutoClose, 700);
    }})();
    </script>
    """,
    height=1,
)

# ==============================================================================
# ৪. থিম কালার ও সিএসএস স্টাইল (টগল বাটন স্পষ্ট করার জন্য হাই-কনট্রাস্ট)
# ==============================================================================
if "Pure White" in theme_choice:
    bg_color, card_bg, input_bg, text_color, sub_text, border_col, chart_bg, grid_col, nifty_col_line, accent_col, shadow_css = (
        "#f4f6f9", "#ffffff", "#ffffff", "#0f172a", "#475569", "#cbd5e1", "#ffffff", "rgba(15, 23, 42, 0.08)", "#475569", "#2563eb", "0 6px 18px rgba(15, 23, 42, 0.06)"
    )
elif "Frost Blue" in theme_choice:
    bg_color, card_bg, input_bg, text_color, sub_text, border_col, chart_bg, grid_col, nifty_col_line, accent_col, shadow_css = (
        "#eef6ff", "#ffffff", "#ffffff", "#082f49", "#334155", "#93c5fd", "#ffffff", "rgba(8, 47, 73, 0.08)", "#0284c7", "#0284c7", "0 6px 18px rgba(2, 132, 199, 0.08)"
    )
else:
    bg_color, card_bg, input_bg, text_color, sub_text, border_col, chart_bg, grid_col, nifty_col_line, accent_col, shadow_css = (
        "#090d16", "#111827", "#1e293b", "#f8fafc", "#cbd5e1", "#334155", "#111827", "rgba(255, 255, 255, 0.08)", "#facc15", "#38bdf8", "0 8px 24px rgba(0, 0, 0, 0.55)"
    )

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; color: {text_color} !important; }}
    h1, h2, h3, h4, h5, h6, p, span, label, div[data-testid="stMarkdownContainer"] {{ color: {text_color} !important; }}
    section[data-testid="stSidebar"] {{ background-color: {card_bg} !important; border-right: 1px solid {border_col} !important; }}
    /* সাইডবার টগল বাটনটি স্পষ্ট এবং দৃশ্যমান রাখার জন্য স্টাইল */
    button[kind="header"], [data-testid="collapsedControl"] {{
        background-color: {accent_col} !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }}
    div[data-baseweb="select"] > div {{ background-color: {input_bg} !important; color: {text_color} !important; border: 1px solid {border_col} !important; border-radius: 10px !important; font-weight: 600 !important; }}
    div.stButton > button {{ width: 100%; background-color: {input_bg} !important; color: {accent_col} !important; border: 1px solid {border_col} !important; border-radius: 10px !important; font-weight: 700 !important; font-size: 13px !important; padding: 6px 10px !important; }}
    div.stButton > button:hover {{ border-color: {accent_col} !important; background-color: rgba(59, 130, 246, 0.12) !important; }}
    .pro-card {{ background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 14px; padding: 16px 18px; margin-bottom: 10px; box-shadow: {shadow_css}; }}
    .kpi-card {{ background-color: {card_bg}; border: 1px solid {border_col}; border-top: 4px solid {accent_col}; border-radius: 14px; padding: 14px 16px; box-shadow: {shadow_css}; margin-bottom: 6px; min-height: 112px; }}
    .kpi-title {{ font-size: 13px; font-weight: 700; color: {sub_text} !important; margin-bottom: 4px; }}
    .kpi-main {{ font-size: 21px; font-weight: 800; color: {text_color} !important; line-height: 1.25; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .kpi-sub-pos {{ display: inline-block; font-size: 12px; font-weight: 700; color: #10b981 !important; background: rgba(16, 185, 129, 0.14); padding: 2px 8px; border-radius: 99px; }}
    .kpi-sub-neg {{ display: inline-block; font-size: 12px; font-weight: 700; color: #ef4444 !important; background: rgba(239, 68, 68, 0.14); padding: 2px 8px; border-radius: 99px; }}
    .badge-green {{ background: rgba(16, 185, 129, 0.16); color: #10b981 !important; border: 1px solid rgba(16, 185, 129, 0.45); padding: 4px 12px; border-radius: 999px; font-weight: 800; font-size: 14px; }}
    .badge-red {{ background: rgba(239, 68, 68, 0.16); color: #ef4444 !important; border: 1px solid rgba(239, 68, 68, 0.45); padding: 4px 12px; border-radius: 999px; font-weight: 800; font-size: 14px; }}
    .stage-banner {{ display: inline-block; padding: 5px 12px; border-radius: 8px; font-size: 12.5px; font-weight: 700; margin: 6px 0; background: rgba(59, 130, 246, 0.12); border-left: 4px solid {accent_col}; }}
    .action-btn {{ display: inline-block; padding: 4px 10px; margin: 3px 4px 3px 0; border-radius: 6px; font-size: 12px; font-weight: 700; text-decoration: none !important; border: 1px solid {border_col}; background: {input_bg}; color: {text_color} !important; }}
    .ticker-wrap {{ width: 100%; overflow: hidden; background: {card_bg}; border: 1px solid {border_col}; border-radius: 10px; padding: 9px 14px; margin: 8px 0 14px 0; white-space: nowrap; box-shadow: {shadow_css}; }}
    .ticker-move {{ display: inline-block; animation: ticker 155s linear infinite; }}
    .ticker-wrap:hover .ticker-move {{ animation-play-state: paused; }}
    @keyframes ticker {{ 0% {{ transform: translateX(0%); }} 100% {{ transform: translateX(-50%); }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("## 🧭 AlphaPulse Pro — Institutional Sector & Stock Terminal")

# ==============================================================================
# ৫. ডেটা লোডিং ও স্টাইলিং ইঞ্জিন
# ==============================================================================
@st.cache_data(ttl=3600)
def load_full_history():
    raw = yf.download(all_tickers, period="5y", interval="1d", auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.levels[0]:
            return raw["Close"].ffill()
    return raw.ffill()

with st.spinner("মার্কেট ডেটা এবং অ্যানালগ মিটার লোড হচ্ছে..."):
    full_df = load_full_history()

tf_days_map = {"1D": 2, "1W": 6, "1M": 22, "3M": 64, "6M": 126, "1Y": 252, "3Y": 756, "5Y": len(full_df)}

def calc_return(series, days):
    s = series.dropna()
    if len(s) < 2: return 0.0
    sub = s.tail(min(days, len(s)))
    if len(sub) < 2 or sub.iloc[0] == 0: return 0.0
    return round(((sub.iloc[-1] / sub.iloc[0]) - 1) * 100, 2)

def safe_colored_table(df_in, primary_col):
    disp_df = df_in.copy()
    pct_cols = [c for c in ["1D %", "1W %", "1M %", "3M %", "6M %", "1Y %", "5Y %", "From 52W High %", primary_col] if c in disp_df.columns]
    
    fmt = {}
    if "CMP (₹)" in disp_df.columns: fmt["CMP (₹)"] = "₹{:.2f}"
    if "Meter Score" in disp_df.columns: fmt["Meter Score"] = "{:.0f}/100"
    if "Now Meter (0-100)" in disp_df.columns: fmt["Now Meter (0-100)"] = "{:.1f}"
    if "Prev Meter" in disp_df.columns: fmt["Prev Meter"] = "{:.1f}"
    if "Shift (Δ)" in disp_df.columns: fmt["Shift (Δ)"] = "{:+.1f}"
    for c in pct_cols: fmt[c] = "{:+.2f}%"

    def highlight_row(row):
        val = row.get(primary_col, 0.0)
        if pd.isna(val): return [''] * len(row)
        bg = 'background-color: rgba(16, 185, 129, 0.11);' if val >= 0 else 'background-color: rgba(239, 68, 68, 0.11);'
        return [bg] * len(row)

    try:
        return disp_df.style.apply(highlight_row, axis=1).format(fmt)
    except Exception:
        return disp_df

def make_analog_gauge(score, prev_score, title_txt, height_px=215):
    bar_col = "#10b981" if score >= 65 else "#84cc16" if score >= 48 else "#f59e0b" if score >= 35 else "#ef4444"
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=score,
        delta={"reference": prev_score, "increasing": {"color": "#10b981"}, "decreasing": {"color": "#ef4444"}, "valueformat": ".1f"},
        title={"text": title_txt, "font": {"size": 12, "color": text_color}},
        number={"font": {"size": 23, "color": text_color}, "valueformat": ".0f"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": sub_text},
            "bar": {"color": bar_col, "thickness": 0.32},
            "bgcolor": chart_bg, "borderwidth": 1, "bordercolor": border_col,
            "steps": [
                {"range": [0, 35], "color": "rgba(239, 68, 68, 0.22)"},
                {"range": [35, 48], "color": "rgba(245, 158, 11, 0.22)"},
                {"range": [48, 65], "color": "rgba(132, 204, 22, 0.22)"},
                {"range": [65, 100], "color": "rgba(16, 185, 129, 0.28)"},
            ],
            "threshold": {"line": {"color": text_color, "width": 4}, "thickness": 0.82, "value": score}
        }
    ))
    fig_g.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, font={"color": text_color}, height=height_px, margin=dict(t=32, b=8, l=18, r=18))
    return fig_g

nifty_col = full_df[benchmark] if benchmark in full_df.columns else pd.Series(dtype=float)
nifty_multi_ret = {tf: calc_return(nifty_col, d) for tf, d in tf_days_map.items()}

sector_master = []
all_stocks_master = {}

for s_name, tickers in sectors.items():
    valid = [t for t in tickers if t in full_df.columns and len(full_df[t].dropna()) > 5]
    if not valid: continue

    st_rows = []
    for t in valid:
        s_price = full_df[t].dropna()
        curr_p = round(float(s_price.iloc[-1]), 2)
        high_52w = float(s_price.tail(252).max())
        low_52w = float(s_price.tail(252).min())
        dd_52w = round(((curr_p / high_52w) - 1) * 100, 2) if high_52w > 0 else 0.0

        sma50_val = float(s_price.tail(50).mean()) if len(s_price) >= 50 else curr_p
        sma200_val = float(s_price.tail(200).mean()) if len(s_price) >= 200 else curr_p
        above_50dma = curr_p >= sma50_val
        above_200dma = curr_p >= sma200_val

        r_1d = calc_return(s_price, 2)
        r_1w = calc_return(s_price, 6)
        r_1m = calc_return(s_price, 22)
        r_3m = calc_return(s_price, 64)
        r_6m = calc_return(s_price, 126)
        r_1y = calc_return(s_price, 252)
        r_5y = calc_return(s_price, len(full_df))

        st_score = float(np.clip(50 + (r_1w * 2.2) + (r_1m * 1.2) + (r_3m * 0.4), 2, 98))
        st_prev = float(np.clip(50 + (r_3m * 0.9) + (r_1y * 0.3), 2, 98))

        row_dict = {
            "Ticker": t, "Stock": t.replace(".NS", ""), "Sector": s_name, "CMP (₹)": curr_p,
            "Meter Score": round(st_score, 1), "Prev Meter": round(st_prev, 1),
            "1D %": r_1d, "1W %": r_1w, "1M %": r_1m, "3M %": r_3m, "6M %": r_6m, "1Y %": r_1y, "5Y %": r_5y,
            "From 52W High %": dd_52w, "52W High": round(high_52w, 2), "52W Low": round(low_52w, 2),
            "50 DMA Trend": "🟢 Above 50DMA" if above_50dma else "🔴 Below 50DMA",
            "200 DMA Trend": "🟢 Above 200DMA" if above_200dma else "🔴 Below 200DMA",
            "Above_50": above_50dma,
            "Is_Nifty50": t in nifty50_symbols,
        }
        st_rows.append(row_dict)
        all_stocks_master[t] = row_dict

    st_df = pd.DataFrame(st_rows)
    sec_rets = {tf: round(float(st_df[f"{tf} %"].mean()), 2) for tf in ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"]}

    alpha_1w = sec_rets["1W"] - nifty_multi_ret["1W"]
    alpha_1m = sec_rets["1M"] - nifty_multi_ret["1M"]
    alpha_3m = sec_rets["3M"] - nifty_multi_ret["3M"]
    alpha_1y = sec_rets["1Y"] - nifty_multi_ret["1Y"]
    breadth_1m = float((st_df["1M %"] > 0).mean()) * 100

    curr_meter = float(np.clip(50 + (alpha_1w * 2.5) + (alpha_1m * 1.5) + ((breadth_1m - 50) * 0.25), 3, 98))
    prev_meter = float(np.clip(50 + (alpha_3m * 1.2) + (alpha_1y * 0.5), 3, 98))

    if prev_meter < 46 and curr_meter >= 50:
        meter_status = "🔄 Red ➔ Green Turnaround"
    elif curr_meter >= 65 and prev_meter >= 50:
        meter_status = "🚀 Strong Green Leader"
    elif prev_meter >= 55 and curr_meter < 46:
        meter_status = "⚠️ Green ➔ Red Cooling"
    elif 38 <= curr_meter < 52:
        meter_status = "🟡 Yellow Watchlist"
    else:
        meter_status = "🔴 Red Zone Beaten Down"

    sector_master.append({
        "Sector": s_name, "Meter_Status": meter_status,
        "Curr_Meter": round(curr_meter, 1), "Prev_Meter": round(prev_meter, 1),
        "Meter_Diff": round(curr_meter - prev_meter, 1),
        "valid_tickers": valid, "stocks_df": st_df,
        **{f"{k} %": v for k, v in sec_rets.items()},
    })

# ==============================================================================
# ৬. কন্ট্রোল প্যানেল (সঠিক ফিল্টার লজিকসহ সচল)
# ==============================================================================
c1, c2, c3, c4 = st.columns([1, 1.4, 1.4, 1.4])
with c1:
    tf_option = st.selectbox("📅 টাইমফ্রেম (Timeframe):", ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"], index=2, key="sel_tf")
with c2:
    sort_option = st.selectbox(
        "🔃 সাজানোর ক্রম (Sort By):",
        ["Top Performers First", "Beaten Down First", "Meter Score High to Low", "Red ➔ Green Turnaround First"],
        key="sel_sort"
    )
with c3:
    stage_filter = st.selectbox(
        "🎯 জোন ফিল্টার:",
        ["সব সেক্টর (All 32 Sectors)", "Strong Green", "Turnaround", "Yellow Watchlist", "Cooling", "Red Zone"],
        key="sel_stage"
    )
with c4:
    quick_sec_jump = st.selectbox(
        "🔍 নির্দিষ্ট সেক্টর খুঁজুন:",
        ["সবগুলো একসাথে দেখুন (Show All 32)"] + [s["Sector"] for s in sector_master],
        key="sel_jump"
    )

# ==============================================================================
# ৭. টিকার বার
# ==============================================================================
ret_key = f"{tf_option} %"
ticker_items = []
for s in sorted(sector_master, key=lambda x: x[ret_key], reverse=True):
    r_val = s[ret_key]
    col_hex = "#10b981" if r_val >= 0 else "#ef4444"
    arrow = "▲" if r_val >= 0 else "▼"
    ticker_items.append(f"<span style='margin-right:34px; font-weight:700; font-size:14px;'>{s['Sector']}: <span style='color:{col_hex} !important;'>{arrow} {r_val:+.2f}%</span></span>")
st.markdown(f'<div class="ticker-wrap" title="মাউস রাখলে স্ক্রলিং থামবে"><div class="ticker-move">{"".join(ticker_items * 2)}</div></div>', unsafe_allow_html=True)

# ==============================================================================
# ৮. KPI কার্ড প্যানেল (সঠিক নিফটি ৫০ ফিল্টারিং সহ)
# ==============================================================================
all_st_df_global = pd.DataFrame(list(all_stocks_master.values()))
adv_count = int((all_st_df_global[ret_key] >= 0).sum())
dec_count = len(all_st_df_global) - adv_count
pct_above_50 = round(float(all_st_df_global["Above_50"].mean()) * 100, 1)
best_sec_now = max(sector_master, key=lambda x: x[ret_key])
worst_sec_now = min(sector_master, key=lambda x: x[ret_key])
nifty_curr_val = nifty_multi_ret[tf_option]

if "active_kpi_panel" not in st.session_state:
    st.session_state["active_kpi_panel"] = None

def toggle_kpi(p_name):
    st.session_state["active_kpi_panel"] = None if st.session_state["active_kpi_panel"] == p_name else p_name

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Nifty 50 Benchmark ({tf_option})</div>
        <div class="kpi-main">{nifty_curr_val:+.2f}%</div>
        <span class="{'kpi-sub-pos' if nifty_multi_ret['1W']>=0 else 'kpi-sub-neg'}">1W: {nifty_multi_ret['1W']:+.2f}% | 1Y: {nifty_multi_ret['1Y']:+.1f}%</span>
    </div>""", unsafe_allow_html=True)
    if st.button("📊 নিফটি মুভার্স লিস্ট দেখুন ▾", key="btn_kpi_nifty"): toggle_kpi("nifty")

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">মার্কেট ব্রেডথ ({tf_option})</div>
        <div class="kpi-main">🟢 {adv_count} | 🔴 {dec_count}</div>
        <span class="kpi-sub-pos">{pct_above_50}% শেয়ার 50-DMA উপরে</span>
    </div>""", unsafe_allow_html=True)
    if st.button("📋 বাড়তে থাকা ও ডাউন শেয়ার দেখুন ▾", key="btn_kpi_breadth"): toggle_kpi("breadth")

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">টপ লিডার সেক্টর ({tf_option})</div>
        <div class="kpi-main">👑 {best_sec_now['Sector']}</div>
        <span class="kpi-sub-pos">↑ {best_sec_now[ret_key]:+.2f}% (Meter: {best_sec_now['Curr_Meter']:.0f})</span>
    </div>""", unsafe_allow_html=True)
    if st.button(f"🔍 {best_sec_now['Sector']}-এর শেয়ার দেখুন ▾", key="btn_kpi_leader"): toggle_kpi("leader")

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">সবচেয়ে ডাউন সেক্টর ({tf_option})</div>
        <div class="kpi-main">📉 {worst_sec_now['Sector']}</div>
        <span class="kpi-sub-neg">↓ {worst_sec_now[ret_key]:+.2f}% (Value Zone)</span>
    </div>""", unsafe_allow_html=True)
    if st.button(f"🔍 {worst_sec_now['Sector']}-এর শেয়ার দেখুন ▾", key="btn_kpi_laggard"): toggle_kpi("laggard")

active_p = st.session_state["active_kpi_panel"]
if active_p is not None:
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    bc1, bc2 = st.columns([5, 1])
    with bc2:
        if st.button("✖ প্যানেল বন্ধ করুন", key="close_kpi_panel"):
            st.session_state["active_kpi_panel"] = None
            st.rerun()

    disp_cols_kpi = ["Stock", "Sector", "CMP (₹)", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %", "50 DMA Trend"]

    if active_p == "nifty":
        with bc1: st.markdown(f"### 📊 Nifty 50 স্টক মুভার্স বিশ্লেষণ ({tf_option}: {nifty_curr_val:+.2f}%)")
        nifty_subset = all_st_df_global[all_st_df_global["Is_Nifty50"] == True]
        nc1, nc2 = st.columns(2)
        with nc1:
            st.markdown(f"#### 🟢 নিফটি ৫০ গেইনার্স ({tf_option})")
            top_pull = nifty_subset.sort_values(by=ret_key, ascending=False).head(12).reset_index(drop=True)
            st.dataframe(safe_colored_table(top_pull[disp_cols_kpi], ret_key), use_container_width=True, hide_index=True)
        with nc2:
            st.markdown(f"#### 🔴 নিফটি ৫০ ড্রাগার্স ({tf_option})")
            top_drag = nifty_subset.sort_values(by=ret_key, ascending=True).head(12).reset_index(drop=True)
            st.dataframe(safe_colored_table(top_drag[disp_cols_kpi], ret_key), use_container_width=True, hide_index=True)

    elif active_p == "breadth":
        with bc1: st.markdown(f"### 📋 মার্কেট ব্রেডথ রিপোর্ট: 🟢 {adv_count}টি প্লাসে | 🔴 {dec_count}টি মাইনাসে ({tf_option})")
        br1, br2 = st.columns(2)
        with br1:
            st.markdown("#### 🟢 প্লাসে থাকা শেয়ারসমূহ")
            adv_df = all_st_df_global[all_st_df_global[ret_key] >= 0].sort_values(by=ret_key, ascending=False).reset_index(drop=True)
            st.dataframe(safe_colored_table(adv_df[disp_cols_kpi], ret_key), use_container_width=True, height=360, hide_index=True)
        with br2:
            st.markdown("#### 🔴 ডাউন বা মাইনাসে থাকা শেয়ারসমূহ")
            dec_df = all_st_df_global[all_st_df_global[ret_key] < 0].sort_values(by=ret_key, ascending=True).reset_index(drop=True)
            st.dataframe(safe_colored_table(dec_df[disp_cols_kpi], ret_key), use_container_width=True, height=360, hide_index=True)

    elif active_p in ["leader", "laggard"]:
        target_sec = best_sec_now if active_p == "leader" else worst_sec_now
        with bc1: st.markdown(f"### 🔍 সেক্টর বিস্তারিত: **{target_sec['Sector']}** ({tf_option}: {target_sec[ret_key]:+.2f}%)")
        t_df = target_sec["stocks_df"].sort_values(by=ret_key, ascending=False).reset_index(drop=True)
        lc1, lc2 = st.columns([1.3, 1.7])
        with lc1:
            sub_k = full_df.tail(tf_days_map[tf_option]).copy()
            norm_k = pd.DataFrame({c: (sub_k[c]/sub_k[c].dropna().iloc[0])*100 for c in target_sec["valid_tickers"] if len(sub_k[c].dropna())>0}, index=sub_k.index)
            fig_k = go.Figure()
            for t_c in norm_k.columns:
                fig_k.add_trace(go.Scatter(x=norm_k.index, y=norm_k[t_c], name=f"{t_c.replace('.NS','')}", mode="lines", line=dict(width=2)))
            fig_k.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, font=dict(color=text_color, size=11), height=280, margin=dict(t=25,b=10,l=10,r=10))
            st.plotly_chart(fig_k, use_container_width=True, theme=None)
        with lc2:
            st.dataframe(safe_colored_table(t_df[disp_cols_kpi], ret_key), use_container_width=True, height=280, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# ৯. মেইন ট্যাবসমূহ (ফিল্টার ও সেক্টর জাম্প নিখুঁতভাবে সচল)
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧭 ১. সেক্টর চার্ট, মিটার ও সব শেয়ার",
    "🔥 ২. প্রো অটো-স্ক্যানার",
    "🔄 ৩. সম্পূর্ণ রোটেশন হিটম্যাপ ম্যাট্রিক্স",
    "📈 ৪. সিঙ্গেল স্টক অ্যানালাইজার",
    "🗺️ ৫. Finviz ট্রি-ম্যাপ হিটম্যাপ",
])

with tab1:
    days_sel = tf_days_map[tf_option]
    nifty_curr_ret = nifty_multi_ret[tf_option]

    # ফিল্টার লজিক ঠিক করা হয়েছে
    filtered_sectors = []
    for s in sector_master:
        match_stage = stage_filter.startswith("সব") or (stage_filter.lower() in s["Meter_Status"].lower())
        match_jump = quick_sec_jump.startswith("সবগুলো") or (s["Sector"] == quick_sec_jump)
        if match_stage and match_jump:
            filtered_sectors.append(s)

    # সর্টিং লজিক ঠিক করা হয়েছে
    if "Top Performers" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[ret_key], reverse=True)
    elif "Beaten Down" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[ret_key], reverse=False)
    elif "Meter Score" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x["Curr_Meter"], reverse=True)
    else:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x["Curr_Meter"], reverse=True)

    sub_df = full_df.tail(days_sel).copy()
    norm_sub = pd.DataFrame({col: (sub_df[col]/sub_df[col].iloc[0])*100 for col in sub_df.columns if sub_df[col].iloc[0]!=0}, index=sub_df.index)
    nifty_norm_line = norm_sub[benchmark] if benchmark in norm_sub.columns else None

    cols = st.columns(2)
    for idx, sec in enumerate(filtered_sectors):
        with cols[idx % 2]:
            s_name = sec["Sector"]
            s_ret = sec[ret_key]
            st_df = sec["stocks_df"].sort_values(by=ret_key, ascending=False).reset_index(drop=True)
            up_cnt = int((st_df[ret_key] >= 0).sum())
            dn_cnt = len(st_df) - up_cnt

            st.markdown(f"""
            <div class="pro-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:19px; font-weight:800;">#{idx+1} {s_name}</span>
                    <span class="{'badge-green' if s_ret>=0 else 'badge-red'}">{s_ret:+.2f}% ({tf_option})</span>
                </div>
                <div class="stage-banner">{sec['Meter_Status']}</div>
                <div style="font-size:13px; color:{sub_text};">🟢 বাড়ছে: <b>{up_cnt}টি</b> | 🔴 ডাউন: <b>{dn_cnt}টি</b> | 🧭 <b>Meter:</b> {sec['Curr_Meter']}/100</div>
            </div>""", unsafe_allow_html=True)

            valid_cols = [t for t in sec["valid_tickers"] if t in norm_sub.columns]
            sec_line = norm_sub[valid_cols].mean(axis=1)

            ch_col, mt_col = st.columns([1.65, 1]) if show_card_meter else (st.container(), None)
            with ch_col:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=norm_sub.index, y=sec_line, name=s_name, line=dict(color="#10b981" if s_ret>=nifty_curr_ret else "#ef4444", width=2.8)))
                if nifty_norm_line is not None:
                    fig.add_trace(go.Scatter(x=norm_sub.index, y=nifty_norm_line, name="Nifty 50", line=dict(color=nifty_col_line, width=1.6, dash="dot")))
                fig.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, font=dict(color=text_color), height=215, margin=dict(t=15,b=10,l=10,r=10), showlegend=False, xaxis=dict(gridcolor=grid_col), yaxis=dict(gridcolor=grid_col))
                st.plotly_chart(fig, use_container_width=True, theme=None, key=f"ch_{idx}")
            
            if show_card_meter:
                with mt_col:
                    st.plotly_chart(make_analog_gauge(sec["Curr_Meter"], sec["Prev_Meter"], "Meter", 215), use_container_width=True, theme=None, key=f"mg_{idx}")

            with st.expander(f"🔍 {s_name} ওপেন করুন — সব শেয়ারের তালিকা ও লিংক ({len(st_df)}টি শেয়ার)"):
                disp_cols = ["Stock", "CMP (₹)", "Meter Score", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %", "50 DMA Trend"]
                st.dataframe(safe_colored_table(st_df[disp_cols], ret_key), use_container_width=True, hide_index=True)
                btn_html = "".join([f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{r["Stock"]}" target="_blank">📈 {r["Stock"]} (TV)</a><a class="action-btn" href="https://www.screener.in/company/{r["Stock"]}/" target="_blank">📊 Screener</a> &nbsp;' for _, r in st_df.iterrows()])
                st.markdown(btn_html, unsafe_allow_html=True)

with tab2:
    st.subheader("🔥 ইনস্টিটিউশনাল অটো-স্ক্যানার")
    brk_df = all_st_df_global[all_st_df_global["Above_50"]].sort_values(by=ret_key, ascending=False).head(15).reset_index(drop=True)
    st.markdown(f"#### 🚀 Top Momentum Breakouts ({tf_option})")
    st.dataframe(safe_colored_table(brk_df[["Stock", "Sector", "CMP (₹)", ret_key, "1M %", "From 52W High %", "Meter Score"]], ret_key), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("🔄 সম্পূর্ণ সেক্টর রোটেশন ম্যাট্রিক্স")
    mat_df = pd.DataFrame(sector_master)[["Sector", "Curr_Meter", "Prev_Meter", "1D %", "1W %", "1M %", "3M %", "1Y %"]].sort_values(by="Curr_Meter", ascending=False).reset_index(drop=True)
    st.dataframe(safe_colored_table(mat_df, "Curr_Meter"), use_container_width=True, height=600, hide_index=True)

with tab4:
    st.subheader("📈 সিঙ্গেল স্টক ডিপ-ডাইভ অ্যানালাইজার")
    sel_sec = st.selectbox("সেক্টর:", list(sectors.keys()), key="s_sec")
    sel_stk = st.selectbox("শেয়ার:", [t.replace(".NS","") for t in sectors[sel_sec]], key="s_stk")
    if sel_stk:
        sym = sel_stk+".NS"
        if sym in full_df.columns:
            s_full = full_df[sym].dropna()
            fig_ind = go.Figure()
            fig_ind.add_trace(go.Scatter(x=s_full.index, y=s_full, name="Price", line=dict(color=accent_col, width=2.5)))
            fig_ind.add_trace(go.Scatter(x=s_full.index, y=s_full.rolling(50).mean(), name="50 DMA", line=dict(color="#10b981", width=1.5)))
            fig_ind.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, font=dict(color=text_color), height=380, xaxis=dict(gridcolor=grid_col), yaxis=dict(gridcolor=grid_col))
            st.plotly_chart(fig_ind, use_container_width=True)
            st.markdown(f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{sel_stk}" target="_blank">📈 TradingView-তে {sel_stk} খুলুন</a>', unsafe_allow_html=True)

with tab5:
    st.subheader(f"🗺️ মার্কেট ট্রি-ম্যাপ হিটম্যাপ ({tf_option})")
    tree_df = all_st_df_global.copy()
    tree_df["Weight"] = 10
    fig_tree = go.Figure(go.Treemap(
        labels=tree_df["Stock"], parents=tree_df["Sector"], values=tree_df["Weight"],
        customdata=np.stack((tree_df[ret_key], tree_df["CMP (₹)"]), axis=-1),
        texttemplate="<b>%{label}</b><br>%{customdata[0]:+.1f}%",
        marker=dict(colors=tree_df[ret_key], colorscale=[[0.0, "#dc2626"], [0.45, "#f59e0b"], [0.55, "#84cc16"], [1.0, "#059669"]], cmid=0)
    ))
    fig_tree.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, font=dict(color=text_color), height=600)
    st.plotly_chart(fig_tree, use_container_width=True)
