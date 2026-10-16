import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf

# ==============================================================================
# ১. পেজ সেটআপ
# ==============================================================================
st.set_page_config(
    page_title="AlphaPulse Pro | Sector & Stock Terminal",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# ২. ৩২টি মাইক্রো-সেক্টর এবং শেয়ারের তালিকা
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

benchmark = "^NSEI"
all_tickers = sorted(list(set([benchmark] + [t for s in sectors.values() for t in s])))

# ==============================================================================
# ৩. সাইডবার মেনু (থিম ও মিটার কন্ট্রোল মেনুবারে নিয়ে আসা হয়েছে + অটো-ক্লোজ)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎛️ থিম ও ডিসপ্লে সেটিংস")
    theme_choice = st.selectbox(
        "🎨 প্রিমিয়াম থিম (Select Theme):",
        [
            "💎 Royal Frost Blue (সফট ব্লু প্রিমিয়াম)",
            "☀️ Pure White Luxury (সাদা প্রিমিয়াম থিম)",
            "🌙 Obsidian Pro Dark (ডার্ক হাই-কনট্রাস্ট থিম)",
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
    st.caption("মাউস কার্সার সরিয়ে নিলে এই মেনু স্বয়ংক্রিয়ভাবে বন্ধ হয়ে যাবে।")

# সাইডবার অটো-ক্লোজ করার উন্নত জাভাস্ক্রিপ্ট সেন্সর
components.html(
    f"""
    <script>
    (function() {{
        const doc = window.parent.document;
        let closeTimer = null;

        function collapseSidebarNow() {{
            // যদি কোনো ড্রপডাউন লিস্ট খোলা থাকে, তাহলে মেনু বন্ধ করবে না
            if (doc.querySelector('div[data-baseweb="popover"]')) return;

            const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
            if (sidebar && sidebar.getAttribute('aria-expanded') === 'true') {{
                const closeBtn =
                    doc.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
                    doc.querySelector('[data-testid="stSidebarHeader"] button') ||
                    sidebar.querySelector('button[kind="headerNoPadding"]') ||
                    sidebar.querySelector('button[kind="header"]') ||
                    sidebar.querySelector('button');

                if (closeBtn) {{
                    closeBtn.click();
                }}
                setTimeout(() => {{
                    if (sidebar.getAttribute('aria-expanded') === 'true') {{
                        sidebar.setAttribute('aria-expanded', 'false');
                    }}
                }}, 180);
            }}
        }}

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

            const expandBtn = doc.querySelector('[data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"]');
            if (expandBtn && !expandBtn.dataset.boundExpand) {{
                expandBtn.dataset.boundExpand = "true";
                expandBtn.addEventListener('click', () => {{
                    const sb = doc.querySelector('section[data-testid="stSidebar"]');
                    if (sb) sb.setAttribute('aria-expanded', 'true');
                }});
            }}
        }}

        setInterval(attachAutoClose, 700);
    }})();
    </script>
    """,
    height=1,
)

# ==============================================================================
# ৪. থিম কালার ও প্রিমিয়াম CSS
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
    sub_text = "#cbd5e1"
    border_col = "#334155"
    chart_bg = "#111827"
    grid_col = "rgba(255, 255, 255, 0.08)"
    nifty_col_line = "#facc15"
    accent_col = "#38bdf8"
    shadow_css = "0 8px 24px rgba(0, 0, 0, 0.55)"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    h1, h2, h3, h4, h5, h6, p, span, label, div[data-testid="stMarkdownContainer"] {{
        color: {text_color} !important;
    }}
    section[data-testid="stSidebar"] {{
        background-color: {card_bg} !important;
        border-right: 1px solid {border_col} !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_col} !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}
    div[data-baseweb="select"] span {{
        color: {text_color} !important;
    }}
    div[data-baseweb="popover"] ul {{
        background-color: {card_bg} !important;
        border: 1px solid {border_col} !important;
    }}
    div[data-baseweb="popover"] li {{
        color: {text_color} !important;
    }}
    /* বাটন ডিজাইন (ক্লিকেবল কার্ড বাটনের জন্য) */
    div.stButton > button {{
        width: 100%;
        background-color: {input_bg} !important;
        color: {accent_col} !important;
        border: 1px solid {border_col} !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        padding: 6px 10px !important;
        transition: all 0.2s ease;
    }}
    div.stButton > button:hover {{
        border-color: {accent_col} !important;
        background-color: rgba(59, 130, 246, 0.12) !important;
    }}
    button[data-baseweb="tab"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_col} !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 10px 18px !important;
        margin-right: 6px !important;
        font-weight: 700 !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        border-bottom: 3px solid {accent_col} !important;
        color: {accent_col} !important;
    }}
    div[data-testid="stExpander"] details {{
        background-color: {card_bg} !important;
        border: 1px solid {border_col} !important;
        border-radius: 12px !important;
        padding: 4px 10px !important;
    }}
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p {{
        color: {text_color} !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }}
    .pro-card {{
        background-color: {card_bg};
        border: 1px solid {border_col};
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 10px;
        box-shadow: {shadow_css};
        transition: all 0.2s ease;
    }}
    .pro-card:hover {{
        border-color: {accent_col};
    }}
    /* ৫ নম্বর বক্সের ৪টি KPI কার্ড ডিজাইন */
    .kpi-card {{
        background-color: {card_bg};
        border: 1px solid {border_col};
        border-top: 4px solid {accent_col};
        border-radius: 14px;
        padding: 14px 16px;
        box-shadow: {shadow_css};
        margin-bottom: 6px;
        min-height: 112px;
    }}
    .kpi-title {{
        font-size: 13px;
        font-weight: 700;
        color: {sub_text} !important;
        margin-bottom: 4px;
    }}
    .kpi-main {{
        font-size: 21px;
        font-weight: 800;
        color: {text_color} !important;
        line-height: 1.25;
        margin-bottom: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .kpi-sub-pos {{
        display: inline-block;
        font-size: 12px;
        font-weight: 700;
        color: #10b981 !important;
        background: rgba(16, 185, 129, 0.14);
        padding: 2px 8px;
        border-radius: 99px;
    }}
    .kpi-sub-neg {{
        display: inline-block;
        font-size: 12px;
        font-weight: 700;
        color: #ef4444 !important;
        background: rgba(239, 68, 68, 0.14);
        padding: 2px 8px;
        border-radius: 99px;
    }}
    .badge-green {{
        background: rgba(16, 185, 129, 0.16);
        color: #10b981 !important;
        border: 1px solid rgba(16, 185, 129, 0.45);
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 14px;
    }}
    .badge-red {{
        background: rgba(239, 68, 68, 0.16);
        color: #ef4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.45);
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 14px;
    }}
    .stage-banner {{
        display: inline-block;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 12.5px;
        font-weight: 700;
        margin: 6px 0;
        background: rgba(59, 130, 246, 0.12);
        border-left: 4px solid {accent_col};
    }}
    .action-btn {{
        display: inline-block;
        padding: 4px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        text-decoration: none !important;
        border: 1px solid {border_col};
        background: {input_bg};
        color: {text_color} !important;
    }}
    .action-btn:hover {{
        border-color: {accent_col};
        background: rgba(59, 130, 246, 0.15);
    }}
    /* ৪ নম্বর বক্স: ধীরগতির স্ক্রলিং টিকার টেপ (মাউস রাখলে থামবে) */
    .ticker-wrap {{
        width: 100%;
        overflow: hidden;
        background: {card_bg};
        border: 1px solid {border_col};
        border-radius: 10px;
        padding: 9px 14px;
        margin: 8px 0 14px 0;
        white-space: nowrap;
        box-shadow: {shadow_css};
    }}
    .ticker-move {{
        display: inline-block;
        animation: ticker 155s linear infinite;
    }}
    .ticker-wrap:hover .ticker-move {{
        animation-play-state: paused;
    }}
    @keyframes ticker {{
        0% {{ transform: translateX(0%); }}
        100% {{ transform: translateX(-50%); }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# ৫. ক্লিন হেডার (১ ও ২ নম্বর বক্স সরিয়ে একদম পরিষ্কার করা হয়েছে)
# ==============================================================================
st.markdown("## 🧭 AlphaPulse Pro — Institutional Sector & Stock Terminal")

# ==============================================================================
# ৬. ডেটা লোডিং এবং টেবিলের সবুজ/লাল কালার শেডিং ফাংশন
# ==============================================================================
@st.cache_data(ttl=3600)
def load_full_history():
    raw = yf.download(all_tickers, period="5y", interval="1d", auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.levels[0]:
            return raw["Close"].ffill()
    return raw.ffill()

with st.spinner("৫ বছরের সম্পূর্ণ মার্কেট ডেটা এবং ৩২টি সেক্টরের অ্যানালগ মিটার লোড হচ্ছে..."):
    full_df = load_full_history()

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

# প্লাসে থাকলে হালকা সবুজ এবং মাইনাসে থাকলে হালকা লাল শেডিং করার ফাংশন
def style_colored_table(df_in, primary_col):
    pct_cols = [
        c for c in ["1D %", "1W %", "1M %", "3M %", "6M %", "1Y %", "5Y %", "From 52W High %"]
        if c in df_in.columns
    ]

    def row_tint(row):
        val = row.get(primary_col, 0.0)
        if pd.isna(val):
            return [""] * len(row)
        if val >= 0:
            return ["background-color: rgba(16, 185, 129, 0.13);"] * len(row)
        return ["background-color: rgba(239, 68, 68, 0.13);"] * len(row)

    def cell_tint(val):
        if not isinstance(val, (int, float, np.number)) or pd.isna(val):
            return ""
        if val > 0:
            return "background-color: rgba(16, 185, 129, 0.25); color: #059669; font-weight: 700;"
        elif val < 0:
            return "background-color: rgba(239, 68, 68, 0.25); color: #dc2626; font-weight: 700;"
        return ""

    fmt = {}
    if "CMP (₹)" in df_in.columns:
        fmt["CMP (₹)"] = "₹{:.2f}"
    if "Meter Score" in df_in.columns:
        fmt["Meter Score"] = "{:.0f}/100"
    if "Now Meter (0-100)" in df_in.columns:
        fmt["Now Meter (0-100)"] = "{:.1f}"
    if "Prev Meter" in df_in.columns:
        fmt["Prev Meter"] = "{:.1f}"
    if "Shift (Δ)" in df_in.columns:
        fmt["Shift (Δ)"] = "{:+.1f}"
    for c in pct_cols:
        fmt[c] = "{:+.2f}%"

    styler = df_in.style.apply(row_tint, axis=1)
    if pct_cols:
        if hasattr(styler, "map"):
            styler = styler.map(cell_tint, subset=pct_cols)
        else:
            styler = styler.applymap(cell_tint, subset=pct_cols)
    return styler.format(fmt)

def make_analog_gauge(score, prev_score, title_txt, height_px=215):
    if score >= 65:
        bar_col = "#10b981"
    elif score >= 48:
        bar_col = "#84cc16"
    elif score >= 35:
        bar_col = "#f59e0b"
    else:
        bar_col = "#ef4444"

    fig_g = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=score,
            delta={
                "reference": prev_score,
                "increasing": {"color": "#10b981"},
                "decreasing": {"color": "#ef4444"},
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
                    {"range": [0, 35], "color": "rgba(239, 68, 68, 0.22)"},
                    {"range": [35, 48], "color": "rgba(245, 158, 11, 0.22)"},
                    {"range": [48, 65], "color": "rgba(132, 204, 22, 0.22)"},
                    {"range": [65, 100], "color": "rgba(16, 185, 129, 0.28)"},
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

nifty_col = full_df[benchmark] if benchmark in full_df.columns else pd.Series(dtype=float)
nifty_multi_ret = {tf: calc_return(nifty_col, d) for tf, d in tf_days_map.items()}

sector_master = []
all_stocks_master = {}

for s_name, tickers in sectors.items():
    valid = [t for t in tickers if t in full_df.columns and len(full_df[t].dropna()) > 5]
    if not valid:
        continue

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
            "Ticker": t,
            "Stock": t.replace(".NS", ""),
            "Sector": s_name,
            "CMP (₹)": curr_p,
            "Meter Score": round(st_score, 1),
            "Prev Meter": round(st_prev, 1),
            "1D %": r_1d,
            "1W %": r_1w,
            "1M %": r_1m,
            "3M %": r_3m,
            "6M %": r_6m,
            "1Y %": r_1y,
            "5Y %": r_5y,
            "From 52W High %": dd_52w,
            "52W High": round(high_52w, 2),
            "52W Low": round(low_52w, 2),
            "50 DMA Trend": "🟢 Above 50DMA" if above_50dma else "🔴 Below 50DMA",
            "200 DMA Trend": "🟢 Above 200DMA" if above_200dma else "🔴 Below 200DMA",
            "Above_50": above_50dma,
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
        stage = "🔄 Red ➔ Green (রেড থেকে গ্রিন হচ্ছে)"
        meter_status = "🔴 রেড জোন থেকে ঘুরে 🟢 গ্রিন জোনে প্রবেশ করছে (Bullish Turnaround)"
    elif curr_meter >= 65 and prev_meter >= 50:
        stage = "🚀 Strong Green (স্ট্রং গ্রিন জোন)"
        meter_status = "🟢 ফুল গ্রিন জোন — মার্কেটকে লিড দিচ্ছে (Strong Momentum Leader)"
    elif prev_meter >= 55 and curr_meter < 46:
        stage = "⚠️ Green ➔ Red (গ্রিন থেকে নামছে)"
        meter_status = "🟢 গ্রিন থেকে কমে 🟡 ইয়েলো/রেড জোনের দিকে নামছে (Cooling Off)"
    elif 38 <= curr_meter < 52:
        stage = "🟡 Yellow Zone (ইয়েলো ওয়াচলিস্ট জোন)"
        meter_status = "🟡 ইয়েলো জোন — ব্রেকআউট বা রিভার্সালের অপেক্ষায় (Neutral Watchlist)"
    else:
        stage = "🔴 Red Zone (ডিপ ভ্যালু / ডাউন জোন)"
        meter_status = "🔴 রেড জোন — সেক্টরটি এখন ডাউন বা ডিপ ভ্যালু জোনে আছে (Beaten Down)"

    sector_master.append({
        "Sector": s_name,
        "Stage": stage,
        "Meter_Status": meter_status,
        "Curr_Meter": round(curr_meter, 1),
        "Prev_Meter": round(prev_meter, 1),
        "Meter_Diff": round(curr_meter - prev_meter, 1),
        "valid_tickers": valid,
        "stocks_df": st_df,
        **{f"{k} %": v for k, v in sec_rets.items()},
    })

# ==============================================================================
# ৭. অন-পেজ ৪টি মূল ফিল্টার (ওপরের খালি বক্স ছাড়া সরাসরি ক্লিন লেআউট)
# ==============================================================================
c1, c2, c3, c4 = st.columns([1, 1.4, 1.4, 1.4])
with c1:
    tf_option = st.selectbox("📅 টাইমফ্রেম (Timeframe):", ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"], index=2)
with c2:
    sort_option = st.selectbox(
        "🔃 কীভাবে সাজাতে চান (Sort By):",
        [
            "Top Performers First (সবচেয়ে বেশি বাড়া সেক্টর আগে)",
            "Beaten Down First (সবচেয়ে বেশি ডাউন সেক্টর আগে)",
            "Meter Score High to Low (স্ট্রং গ্রিন মিটার আগে)",
            "Red ➔ Green Turnaround First (রেড থেকে গ্রিন হওয়া আগে)",
        ],
    )
with c3:
    stage_filter = st.selectbox(
        "🎯 রোটেশন জোন ফিল্টার:",
        [
            "সব সেক্টর (All 32 Sectors)",
            "🔄 Red ➔ Green (রেড থেকে গ্রিন হচ্ছে)",
            "🚀 Strong Green (স্ট্রং গ্রিন জোন)",
            "🟡 Yellow Zone (ইয়েলো ওয়াচলিস্ট জোন)",
            "⚠️ Green ➔ Red (গ্রিন থেকে নামছে)",
            "🔴 Red Zone (ডিপ ভ্যালু / ডাউন জোন)",
        ],
    )
with c4:
    quick_sec_jump = st.selectbox(
        "🔍 নির্দিষ্ট সেক্টর খুঁজুন:",
        ["সবগুলো একসাথে দেখুন (Show All 32)"] + [s["Sector"] for s in sector_master],
    )

# ==============================================================================
# ৮. ধীরগতির স্ক্রলিং টিকার বার (বক্স ৪: স্লো স্পিড + মাউস রাখলে থামবে)
# ==============================================================================
ticker_items = []
for s in sorted(sector_master, key=lambda x: x[f"{tf_option} %"], reverse=True):
    r_val = s[f"{tf_option} %"]
    col_hex = "#10b981" if r_val >= 0 else "#ef4444"
    arrow = "▲" if r_val >= 0 else "▼"
    ticker_items.append(
        f"<span style='margin-right:34px; font-weight:700; font-size:14px;'>{s['Sector']}: "
        f"<span style='color:{col_hex} !important;'>{arrow} {r_val:+.2f}%</span></span>"
    )
ticker_html = "".join(ticker_items * 2)
st.markdown(
    f'<div class="ticker-wrap" title="মাউস রাখলে স্ক্রলিং থামবে"><div class="ticker-move">{ticker_html}</div></div>',
    unsafe_allow_html=True,
)

# ==============================================================================
# ৯. ক্লিকেবল ৪টি মেইন KPI বক্স (বক্স ৫: ক্লিক করলেই ভেতরের শেয়ারের লিস্ট খুলবে)
# ==============================================================================
all_st_df_global = pd.DataFrame(list(all_stocks_master.values()))
ret_col_now = f"{tf_option} %"
adv_count = int((all_st_df_global[ret_col_now] >= 0).sum())
dec_count = len(all_st_df_global) - adv_count
pct_above_50 = round(float(all_st_df_global["Above_50"].mean()) * 100, 1)
best_sec_now = max(sector_master, key=lambda x: x[ret_col_now])
worst_sec_now = min(sector_master, key=lambda x: x[ret_col_now])
nifty_curr_val = nifty_multi_ret[tf_option]

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
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Nifty 50 Benchmark ({tf_option})</div>
            <div class="kpi-main">{nifty_curr_val:+.2f}%</div>
            <span class="{sub_cls}">1W: {nifty_multi_ret['1W']:+.2f}% | 1Y: {nifty_multi_ret['1Y']:+.1f}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("📊 নিফটি মুভার্স লিস্ট দেখুন ▾", key="btn_kpi_nifty"):
        toggle_kpi("nifty")

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">মার্কেট ব্রেডথ ({tf_option} Adv vs Dec)</div>
            <div class="kpi-main">🟢 {adv_count} বাড়ছে | 🔴 {dec_count} ডাউন</div>
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
            <div class="kpi-main" title="{best_sec_now['Sector']}">👑 {best_sec_now['Sector']}</div>
            <span class="kpi-sub-pos">↑ {best_sec_now[ret_col_now]:+.2f}% (Meter: {best_sec_now['Curr_Meter']:.0f})</span>
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
            <div class="kpi-main" title="{worst_sec_now['Sector']}">📉 {worst_sec_now['Sector']}</div>
            <span class="kpi-sub-neg">↓ {worst_sec_now[ret_col_now]:+.2f}% (Value Zone)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"🔍 {worst_sec_now['Sector']}-এর শেয়ার দেখুন ▾", key="btn_kpi_laggard"):
        toggle_kpi("laggard")

# ৫ নম্বর বক্সের যেকোনো কার্ডে ক্লিক করলে তার বিস্তারিত প্যানেল এখানে খুলবে
active_p = st.session_state["active_kpi_panel"]
if active_p is not None:
    st.markdown('<div class="pro-card">', unsafe_allow_html=True)
    top_bar_c1, top_bar_c2 = st.columns([5, 1])
    with top_bar_c2:
        if st.button("✖ লিস্ট বন্ধ করুন", key="close_kpi_panel"):
            st.session_state["active_kpi_panel"] = None
            st.rerun()

    disp_cols_kpi = ["Stock", "Sector", "CMP (₹)", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %", "50 DMA Trend"]

    if active_p == "nifty":
        with top_bar_c1:
            st.markdown(f"### 📊 Nifty 50 ও মার্কেট মুভার্স বিশ্লেষণ ({tf_option}: {nifty_curr_val:+.2f}%)")
            st.caption("এই সময়ে কোন কোন শেয়ার মার্কেটকে সবচেয়ে বেশি উপরে টানছে (Top Gainers) এবং কারা নিচে নামাচ্ছে (Top Draggers):")
        nc1, nc2 = st.columns(2)
        with nc1:
            st.markdown(f"#### 🟢 মার্কেটকে উপরে টানছে (Top 12 Pullers - {tf_option})")
            top_pull = all_st_df_global.sort_values(by=ret_col_now, ascending=False).head(12).reset_index(drop=True)
            st.dataframe(style_colored_table(top_pull[disp_cols_kpi], ret_col_now), use_container_width=True, hide_index=True)
        with nc2:
            st.markdown(f"#### 🔴 মার্কেটকে নিচে নামাচ্ছে (Top 12 Draggers - {tf_option})")
            top_drag = all_st_df_global.sort_values(by=ret_col_now, ascending=True).head(12).reset_index(drop=True)
            st.dataframe(style_colored_table(top_drag[disp_cols_kpi], ret_col_now), use_container_width=True, hide_index=True)

    elif active_p == "breadth":
        with top_bar_c1:
            st.markdown(f"### 📋 মার্কেট ব্রেডথ রিপোর্ট: 🟢 {adv_count}টি শেয়ার প্লাসে | 🔴 {dec_count}টি শেয়ার মাইনাসে ({tf_option})")
        bc1, bc2 = st.columns(2)
        with bc1:
            st.markdown(f"#### 🟢 প্লাসে থাকা শেয়ারসমূহ ({adv_count}টি)")
            adv_df = all_st_df_global[all_st_df_global[ret_col_now] >= 0].sort_values(by=ret_col_now, ascending=False).reset_index(drop=True)
            st.dataframe(style_colored_table(adv_df[disp_cols_kpi], ret_col_now), use_container_width=True, height=360, hide_index=True)
        with bc2:
            st.markdown(f"#### 🔴 ডাউন বা মাইনাসে থাকা শেয়ারসমূহ ({dec_count}টি)")
            dec_df = all_st_df_global[all_st_df_global[ret_col_now] < 0].sort_values(by=ret_col_now, ascending=True).reset_index(drop=True)
            st.dataframe(style_colored_table(dec_df[disp_cols_kpi], ret_col_now), use_container_width=True, height=360, hide_index=True)

    elif active_p in ["leader", "laggard"]:
        target_sec = best_sec_now if active_p == "leader" else worst_sec_now
        sec_title_prefix = "👑 টপ লিডার সেক্টর" if active_p == "leader" else "📉 সবচেয়ে ডাউন সেক্টর"
        with top_bar_c1:
            st.markdown(
                f"### {sec_title_prefix}: **{target_sec['Sector']}** ({tf_option} রিটার্ন: {target_sec[ret_col_now]:+.2f}%)"
            )
            st.caption("সবুজ লাইনের শেয়ারগুলো এই সেক্টরে ভালো পারফর্ম করছে এবং লাল লাইনের শেয়ারগুলো পিছিয়ে বা ডাউন আছে:")

        t_df = target_sec["stocks_df"].sort_values(by=ret_col_now, ascending=False).reset_index(drop=True)
        lc1, lc2 = st.columns([1.3, 1.7])
        with lc1:
            sub_k = full_df.tail(tf_days_map[tf_option]).copy()
            norm_k = pd.DataFrame(
                {c: (sub_k[c] / sub_k[c].dropna().iloc[0]) * 100 for c in target_sec["valid_tickers"] if len(sub_k[c].dropna()) > 0},
                index=sub_k.index,
            )
            fig_k = go.Figure()
            for t_c in norm_k.columns:
                sn = t_c.replace(".NS", "")
                sr = all_stocks_master[t_c][ret_col_now]
                fig_k.add_trace(go.Scatter(x=norm_k.index, y=norm_k[t_c], name=f"{sn} ({sr:+.1f}%)", mode="lines", line=dict(width=2.2)))
            fig_k.update_layout(
                title=f"{target_sec['Sector']} - শেয়ারগুলোর তুলনামূলক চার্ট ({tf_option})",
                paper_bgcolor=chart_bg,
                plot_bgcolor=chart_bg,
                font=dict(color=text_color, size=11),
                height=300,
                margin=dict(t=35, b=15, l=10, r=10),
                xaxis=dict(gridcolor=grid_col),
                yaxis=dict(gridcolor=grid_col, title="Base 100"),
            )
            st.plotly_chart(fig_k, use_container_width=True, theme=None, key=f"kpi_chart_{active_p}")
        with lc2:
            cols_sec_show = ["Stock", "CMP (₹)", "Meter Score", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %", "50 DMA Trend"]
            st.dataframe(style_colored_table(t_df[cols_sec_show], ret_col_now), use_container_width=True, height=300, hide_index=True)
            btn_links = "".join(
                [
                    f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{r["Stock"]}" target="_blank">📈 {r["Stock"]} (TV)</a>'
                    f'<a class="action-btn" href="https://www.screener.in/company/{r["Stock"]}/" target="_blank">📊 Screener</a> &nbsp;'
                    for _, r in t_df.iterrows()
                ]
            )
            st.markdown(btn_links, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# ১০. মেইন ৫টি প্রো ট্যাব
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧭 ১. সেক্টর চার্ট, মিটার ও সব শেয়ার (Gainers/Losers)",
    "🔥 ২. প্রো অটো-স্ক্যানার (Breakout, Turnaround & Value)",
    "🔄 ৩. সম্পূর্ণ রোটেশন হিটম্যাপ ম্যাট্রিক্স",
    "📈 ৪. যেকোনো শেয়ারের নিজস্ব চার্ট ও মিটার",
    "🗺️ ৫. Finviz সেক্টর ট্রি-ম্যাপ (Visual Map)",
])

# ==============================================================================
# TAB 1: সেক্টর গ্রিড + অ্যানালগ মিটার + সবুজ/লাল শেডেড শেয়ার লিস্ট
# ==============================================================================
with tab1:
    days_sel = tf_days_map[tf_option]
    nifty_curr_ret = nifty_multi_ret[tf_option]

    filtered_sectors = [
        s for s in sector_master
        if (stage_filter.startswith("সব") or s["Stage"] == stage_filter)
        and (quick_sec_jump.startswith("সবগুলো") or s["Sector"] == quick_sec_jump)
    ]

    if "Top Performers" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[f"{tf_option} %"], reverse=True)
    elif "Beaten Down" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[f"{tf_option} %"], reverse=False)
    elif "Meter Score" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x["Curr_Meter"], reverse=True)
    else:
        filtered_sectors = sorted(
            filtered_sectors,
            key=lambda x: (x["Stage"].startswith("🔄"), x["Meter_Diff"]),
            reverse=True,
        )

    sub_df = full_df.tail(days_sel).copy()
    norm_sub = pd.DataFrame(index=sub_df.index)
    for col in sub_df.columns:
        s = sub_df[col].dropna()
        if len(s) > 0 and s.iloc[0] != 0:
            norm_sub[col] = (sub_df[col] / s.iloc[0]) * 100

    nifty_norm_line = norm_sub[benchmark] if benchmark in norm_sub.columns else None

    cols = st.columns(2)
    for idx, sec in enumerate(filtered_sectors):
        with cols[idx % 2]:
            s_name = sec["Sector"]
            s_ret = sec[f"{tf_option} %"]
            alpha_val = round(s_ret - nifty_curr_ret, 2)
            outperform = s_ret >= nifty_curr_ret
            st_df = sec["stocks_df"].sort_values(by=f"{tf_option} %", ascending=False).reset_index(drop=True)

            up_cnt = int((st_df[f"{tf_option} %"] >= 0).sum())
            dn_cnt = len(st_df) - up_cnt
            badge_cls = "badge-green" if s_ret >= 0 else "badge-red"

            st.markdown(
                f"""
                <div class="pro-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:19px; font-weight:800;">#{idx+1} {s_name}</span>
                        <span class="{badge_cls}">{s_ret:+.2f}% ({tf_option})</span>
                    </div>
                    <div class="stage-banner">{sec['Meter_Status']}</div>
                    <div style="font-size:13px; color:{sub_text}; margin-top:4px;">
                        <b>Alpha vs Nifty:</b> {alpha_val:+.2f}% &nbsp;|&nbsp;
                        🟢 বাড়ছে: <b>{up_cnt}টি</b> &nbsp;|&nbsp; 🔴 ডাউন: <b>{dn_cnt}টি</b> &nbsp;|&nbsp;
                        🧭 <b>Meter:</b> {sec['Curr_Meter']}/100 (Prev: {sec['Prev_Meter']})
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            valid_cols = [t for t in sec["valid_tickers"] if t in norm_sub.columns]
            sec_line = norm_sub[valid_cols].mean(axis=1)

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
                        line=dict(color="#10b981" if outperform else "#ef4444", width=2.8),
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
                    margin=dict(t=22, b=12, l=10, r=10),
                    legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11, color=text_color)),
                    xaxis=dict(gridcolor=grid_col),
                    yaxis=dict(gridcolor=grid_col, title="Base 100"),
                )
                st.plotly_chart(fig, use_container_width=True, theme=None, key=f"sec_ch_{idx}")

            if show_card_meter:
                with mt_col:
                    fig_gauge = make_analog_gauge(
                        sec["Curr_Meter"],
                        sec["Prev_Meter"],
                        "Rotation Meter",
                        height_px=225,
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True, theme=None, key=f"sec_g_{idx}")

            top_st = st_df.iloc[0]
            bot_st = st_df.iloc[-1]
            st.markdown(
                f"🟢 **টপ গেইনার:** `{top_st['Stock']} ({top_st[f'{tf_option} %']:+.1f}%)` &nbsp;|&nbsp; "
                f"🔴 **সবচেয়ে ডাউন:** `{bot_st['Stock']} ({bot_st[f'{tf_option} %']:+.1f}%)`"
            )

            with st.expander(f"🔍 {s_name} ওপেন করুন — সবুজ/লাল শেয়ার তালিকা, চার্ট ও TradingView লিংক ({len(st_df)}টি শেয়ার)"):
                ex_c1, ex_c2 = st.columns([1, 2])
                with ex_c1:
                    big_gauge = make_analog_gauge(
                        sec["Curr_Meter"],
                        sec["Prev_Meter"],
                        f"Prev: {sec['Prev_Meter']} ➔ Now: {sec['Curr_Meter']}",
                        height_px=250,
                    )
                    st.plotly_chart(big_gauge, use_container_width=True, theme=None, key=f"big_g_{idx}")

                with ex_c2:
                    fig_st = go.Figure()
                    for t in valid_cols:
                        st_name = t.replace(".NS", "")
                        st_r = all_stocks_master[t][f"{tf_option} %"]
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
                        margin=dict(t=35, b=12, l=10, r=10),
                        xaxis=dict(gridcolor=grid_col),
                        yaxis=dict(gridcolor=grid_col, title="Base 100"),
                    )
                    st.plotly_chart(fig_st, use_container_width=True, theme=None, key=f"st_cmp_{idx}")

                disp_cols = [
                    "Stock", "CMP (₹)", "Meter Score", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %", "50 DMA Trend"
                ]
                # এখানে প্লাস শেয়ারগুলো হালকা সবুজ এবং মাইনাস শেয়ারগুলো হালকা লাল দেখাবে
                st.dataframe(
                    style_colored_table(st_df[disp_cols], f"{tf_option} %"),
                    use_container_width=True,
                    hide_index=True,
                )

                st.markdown("##### 🔗 এক ক্লিকে চার্ট (TradingView) ও ফান্ডামেন্টাল (Screener.in) খুলুন:")
                btn_html = "".join(
                    [
                        f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{r["Stock"]}" target="_blank">📈 {r["Stock"]} (TV)</a>'
                        f'<a class="action-btn" href="https://www.screener.in/company/{r["Stock"]}/" target="_blank">📊 Screener</a> &nbsp;'
                        for _, r in st_df.iterrows()
                    ]
                )
                st.markdown(btn_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: প্রো অটো-স্ক্যানার (সবুজ/লাল কালার শেডিং সহ)
# ==============================================================================
with tab2:
    st.subheader("🔥 ইনস্টিটিউশনাল অটো-স্ক্যানার (180+ Active Stocks)")
    sc_col1, sc_col2 = st.columns(2)
    with sc_col1:
        st.markdown(f"#### 🚀 ১. High Momentum Breakouts ({tf_option})")
        brk_df = (
            all_st_df_global[all_st_df_global["Above_50"]]
            .sort_values(by=f"{tf_option} %", ascending=False)
            .head(15)
            .reset_index(drop=True)
        )
        cols_b = ["Stock", "Sector", "CMP (₹)", f"{tf_option} %", "1M %", "From 52W High %", "Meter Score"]
        st.dataframe(style_colored_table(brk_df[cols_b], f"{tf_option} %"), use_container_width=True, hide_index=True)

    with sc_col2:
        st.markdown("#### 🔄 ২. Bullish Turnaround / Reversal Gems")
        turn_df = (
            all_st_df_global[(all_st_df_global["From 52W High %"] < -15) & (all_st_df_global["1W %"] > 1.5)]
            .sort_values(by="1W %", ascending=False)
            .head(15)
            .reset_index(drop=True)
        )
        cols_t = ["Stock", "Sector", "CMP (₹)", "1W %", "1M %", "From 52W High %", "Meter Score"]
        st.dataframe(style_colored_table(turn_df[cols_t], "1W %"), use_container_width=True, hide_index=True)

    st.markdown("---")
    sc_col3, sc_col4 = st.columns(2)
    with sc_col3:
        st.markdown("#### 💎 ৩. Deep Value / Beaten Down Stocks")
        val_df = all_st_df_global.sort_values(by="From 52W High %", ascending=True).head(15).reset_index(drop=True)
        cols_v = ["Stock", "Sector", "CMP (₹)", "From 52W High %", "1W %", "1M %", "1Y %"]
        st.dataframe(style_colored_table(val_df[cols_v], "1W %"), use_container_width=True, hide_index=True)

    with sc_col4:
        st.markdown("#### 📥 ৪. কুইক চার্ট লঞ্চার ও এক্সেল ডাউনলোড")
        quick_pick = st.selectbox(
            "যেকোনো শেয়ার সিলেক্ট করে সরাসরি চার্ট খুলুন:",
            sorted(all_st_df_global["Stock"].unique()),
        )
        if quick_pick:
            st.markdown(
                f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{quick_pick}" target="_blank">📈 TradingView-তে {quick_pick} এর চার্ট খুলুন</a> '
                f'<a class="action-btn" href="https://www.screener.in/company/{quick_pick}/" target="_blank">📊 Screener.in-এ ফান্ডামেন্টাল দেখুন</a>',
                unsafe_allow_html=True,
            )
        csv_bytes = all_st_df_global.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 সব শেয়ারের সম্পূর্ণ ডেটা Excel/CSV হিসেবে ডাউনলোড করুন",
            data=csv_bytes,
            file_name="AlphaPulse_Full_Screener.csv",
            mime="text/csv",
        )

# ==============================================================================
# TAB 3: সম্পূর্ণ মাল্টি-টাইমফ্রেম রোটেশন ম্যাট্রিক্স (সবুজ/লাল শেডিং সহ)
# ==============================================================================
with tab3:
    st.subheader("🔄 ৩২টি সেক্টরের সম্পূর্ণ রোটেশন হিটম্যাপ ও মিটার টেবিল")
    mat_df = pd.DataFrame(sector_master)[
        ["Sector", "Stage", "Curr_Meter", "Prev_Meter", "Meter_Diff", "1D %", "1W %", "1M %", "3M %", "6M %", "1Y %", "5Y %"]
    ].rename(
        columns={
            "Curr_Meter": "Now Meter (0-100)",
            "Prev_Meter": "Prev Meter",
            "Meter_Diff": "Shift (Δ)",
        }
    )
    mat_df = mat_df.sort_values(by=f"{tf_option} %", ascending=False).reset_index(drop=True)

    st.dataframe(
        style_colored_table(mat_df, f"{tf_option} %"),
        use_container_width=True,
        height=680,
        hide_index=True,
    )

# ==============================================================================
# TAB 4: যেকোনো শেয়ারের নিজস্ব চার্ট, 20/50/200 DMA এবং স্টকের অ্যানালগ মিটার
# ==============================================================================
with tab4:
    st.subheader("📈 সিঙ্গেল স্টক ডিপ-ডাইভ অ্যানালাইজার ও অ্যানালগ মিটার")

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        chosen_sec = st.selectbox("১. সেক্টর বেছে নিন:", list(sectors.keys()))
    with sc2:
        sec_tickers = [t.replace(".NS", "") for t in sectors[chosen_sec] if t in full_df.columns]
        chosen_stock = st.selectbox("২. শেয়ার বেছে নিন:", sec_tickers)
    with sc3:
        chart_tf = st.selectbox("৩. চার্টের সময়কাল:", ["3M", "6M", "1Y", "3Y", "5Y"], index=2)

    if chosen_stock:
        t_sym = chosen_stock + ".NS"
        s_info = all_stocks_master.get(t_sym, {})

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("বর্তমান দাম (CMP)", f"₹{s_info.get('CMP (₹)', 0)}")
        m2.metric("1W Return", f"{s_info.get('1W %', 0):+.2f}%")
        m3.metric("1M Return", f"{s_info.get('1M %', 0):+.2f}%")
        m4.metric("1Y Return", f"{s_info.get('1Y %', 0):+.2f}%")
        m5.metric("52W High থেকে দূরত্ব", f"{s_info.get('From 52W High %', 0):+.2f}%")
        m6.metric("50 DMA স্ট্যাটাস", s_info.get("50 DMA Trend", ""))

        st.markdown(
            f'<a class="action-btn" href="https://in.tradingview.com/chart/?symbol=NSE:{chosen_stock}" target="_blank">📈 TradingView-তে {chosen_stock}-এর পূর্ণাঙ্গ চার্ট খুলুন</a> '
            f'<a class="action-btn" href="https://www.screener.in/company/{chosen_stock}/" target="_blank">📊 Screener.in-এ {chosen_stock}-এর ফান্ডামেন্টাল দেখুন</a>',
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
                go.Scatter(x=s_sub.index, y=sma50.tail(d_cnt), name="50 DMA", line=dict(color="#10b981", width=1.8))
            )
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=sma200.tail(d_cnt), name="200 DMA", line=dict(color="#ef4444", width=2.0))
            )
            fig_ind.update_layout(
                title=f"{chosen_stock} ({chosen_sec}) - প্রাইস ও মুভিং অ্যাভারেজ চার্ট ({chart_tf})",
                paper_bgcolor=chart_bg,
                plot_bgcolor=chart_bg,
                font=dict(color=text_color),
                height=400,
                margin=dict(t=45, b=20, l=15, r=15),
                xaxis=dict(gridcolor=grid_col),
                yaxis=dict(gridcolor=grid_col, title="Price (₹)"),
                legend=dict(orientation="h", y=1.08, x=0, font=dict(color=text_color)),
            )
            st.plotly_chart(fig_ind, use_container_width=True, theme=None, key="ind_stock_chart")

        with ind_c2:
            fig_st_gauge = make_analog_gauge(
                s_info.get("Meter Score", 50.0),
                s_info.get("Prev Meter", 50.0),
                f"{chosen_stock} মোমেন্টাম মিটার",
                height_px=360,
            )
            st.plotly_chart(fig_st_gauge, use_container_width=True, theme=None, key="ind_stock_gauge")

# ==============================================================================
# TAB 5: Finviz-Style Interactive Market Treemap Heatmap
# ==============================================================================
with tab5:
    st.subheader(f"🗺️ ইন্টারঅ্যাক্টিভ মার্কেট ট্রি-ম্যাপ হিটম্যাপ ({tf_option} Performance)")
    st.caption("যেকোনো সেক্টরের বক্সে ক্লিক করলে সেটি বড় হয়ে ভেতরের সব শেয়ারের লাল-সবুজ হিটম্যাপ দেখাবে!")

    tree_df = all_st_df_global.copy()
    tree_df["Weight"] = 10

    fig_tree = go.Figure(
        go.Treemap(
            labels=tree_df["Stock"],
            parents=tree_df["Sector"],
            values=tree_df["Weight"],
            customdata=np.stack((tree_df[f"{tf_option} %"], tree_df["CMP (₹)"], tree_df["From 52W High %"]), axis=-1),
            hovertemplate="<b>%{label}</b><br>Return: %{customdata[0]:+.2f}%<br>CMP: ₹%{customdata[1]}<br>From 52W High: %{customdata[2]:+.2f}%<extra></extra>",
            texttemplate="<b>%{label}</b><br>%{customdata[0]:+.1f}%",
            marker=dict(
                colors=tree_df[f"{tf_option} %"],
                colorscale=[[0.0, "#dc2626"], [0.45, "#f59e0b"], [0.55, "#84cc16"], [1.0, "#059669"]],
                cmid=0,
                showscale=True,
            ),
        )
    )
    fig_tree.update_layout(
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font=dict(color=text_color, size=13),
        height=650,
        margin=dict(t=20, b=20, l=10, r=10),
    )
    st.plotly_chart(fig_tree, use_container_width=True, theme=None)
