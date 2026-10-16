import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# ওয়েব অ্যাপের পেজ সেটআপ
st.set_page_config(
    page_title="Pro Sector & Stock Screener", page_icon="🧭", layout="wide"
)

# ==========================================
# থিম এবং ভিউ সেটিংস (টপ বার)
# ==========================================
top_c1, top_c2, top_c3 = st.columns([2.2, 1.2, 1])
with top_c1:
    st.markdown("## 🧭 Pro Sector Rotation & Analog Meter Suite")
with top_c2:
    theme_choice = st.selectbox(
        "🎨 ইন্টারফেস থিম (Select Theme):",
        [
            "☀️ Pure White Luxury (সাদা প্রিমিয়াম থিম)",
            "💎 Executive Frost Blue (সফট ব্লু প্রিমিয়াম)",
            "🌙 Midnight Pro Dark (ডার্ক প্রিমিয়াম থিম)",
        ],
        index=0,
    )
with top_c3:
    show_card_meter = st.toggle("🎛️ সব কার্ডে মিটার দেখান", value=True)

# থিম অনুযায়ী রঙের কনফিগারেশন
if "Pure White" in theme_choice:
    bg_color = "#f8fafc"
    card_bg = "#ffffff"
    text_color = "#0f172a"
    sub_text = "#475569"
    border_col = "#e2e8f0"
    chart_bg = "#ffffff"
    grid_col = "rgba(15, 23, 42, 0.07)"
    nifty_col_line = "#64748b"
    shadow_css = "0 4px 16px rgba(15, 23, 42, 0.06)"
elif "Frost Blue" in theme_choice:
    bg_color = "#f0f7ff"
    card_bg = "#ffffff"
    text_color = "#0c4a6e"
    sub_text = "#334155"
    border_col = "#bae6fd"
    chart_bg = "#ffffff"
    grid_col = "rgba(12, 74, 110, 0.07)"
    nifty_col_line = "#0284c7"
    shadow_css = "0 4px 18px rgba(2, 132, 199, 0.08)"
else:
    bg_color = "#0b0f19"
    card_bg = "#111827"
    text_color = "#f8fafc"
    sub_text = "#94a3b8"
    border_col = "#1f2937"
    chart_bg = "#111827"
    grid_col = "rgba(255, 255, 255, 0.07)"
    nifty_col_line = "#facc15"
    shadow_css = "0 4px 20px rgba(0, 0, 0, 0.4)"

# প্রিমিয়াম লুকের জন্য কাস্টম CSS
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .premium-card {{
        background-color: {card_bg};
        border: 1px solid {border_col};
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: {shadow_css};
    }}
    .sec-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}
    .sec-title {{
        font-size: 19px;
        font-weight: 700;
        color: {text_color};
    }}
    .ret-badge-pos {{
        background: rgba(16, 185, 129, 0.14);
        color: #059669;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }}
    .ret-badge-neg {{
        background: rgba(239, 68, 68, 0.14);
        color: #dc2626;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }}
    .transition-pill {{
        display: inline-block;
        padding: 5px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        margin-top: 4px;
        margin-bottom: 6px;
        background: rgba(100, 116, 139, 0.1);
        color: {text_color};
        border-left: 4px solid #3b82f6;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# ৩২টি মাইক্রো-সেক্টর এবং শেয়ার তালিকা
# ==========================================
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

benchmark = "^NSEI"
all_tickers = sorted(list(set([benchmark] + [t for s in sectors.values() for t in s])))

@st.cache_data(ttl=3600)
def load_full_history():
    raw = yf.download(all_tickers, period="5y", interval="1d", auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.levels[0]:
            return raw["Close"].ffill()
    return raw.ffill()

with st.spinner("প্রিমিয়াম ড্যাশবোর্ড এবং অ্যানালগ মিটার প্রস্তুত হচ্ছে..."):
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

# অ্যানালগ স্পিডোমিটার চার্ট তৈরির ফাংশন
def make_analog_gauge(score, prev_score, title_txt, height_px=210):
    if score >= 68:
        bar_col = "#10b981"  # Deep Green
    elif score >= 48:
        bar_col = "#84cc16"  # Lime / Yellow-Green
    elif score >= 32:
        bar_col = "#f59e0b"  # Yellow / Amber
    else:
        bar_col = "#ef4444"  # Red

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
            title={"text": title_txt, "font": {"size": 13, "color": text_color}},
            number={"font": {"size": 24, "color": text_color}, "valueformat": ".0f"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": sub_text},
                "bar": {"color": bar_col, "thickness": 0.32},
                "bgcolor": chart_bg,
                "borderwidth": 1,
                "bordercolor": border_col,
                "steps": [
                    {"range": [0, 32], "color": "rgba(239, 68, 68, 0.22)"},
                    {"range": [32, 48], "color": "rgba(245, 158, 11, 0.22)"},
                    {"range": [48, 68], "color": "rgba(132, 204, 22, 0.22)"},
                    {"range": [68, 100], "color": "rgba(16, 185, 129, 0.28)"},
                ],
                "threshold": {
                    "line": {"color": text_color, "width": 4},
                    "thickness": 0.8,
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
        margin=dict(t=35, b=10, l=20, r=20),
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

        r_1w = calc_return(s_price, 6)
        r_1m = calc_return(s_price, 22)
        r_3m = calc_return(s_price, 64)
        r_1y = calc_return(s_price, 252)

        # স্টকের নিজস্ব মিটার স্কোর (0-100)
        st_score = float(np.clip(50 + (r_1w * 2.2) + (r_1m * 1.2) + (r_3m * 0.4), 2, 98))

        row_dict = {
            "Ticker": t,
            "Stock": t.replace(".NS", ""),
            "Sector": s_name,
            "CMP (₹)": curr_p,
            "Meter Score": round(st_score, 1),
            "1D %": calc_return(s_price, 2),
            "1W %": r_1w,
            "1M %": r_1m,
            "3M %": r_3m,
            "6M %": calc_return(s_price, 126),
            "1Y %": r_1y,
            "5Y %": calc_return(s_price, len(full_df)),
            "From 52W High %": dd_52w,
            "52W High": round(high_52w, 2),
            "52W Low": round(low_52w, 2),
        }
        st_rows.append(row_dict)
        all_stocks_master[t] = row_dict

    st_df = pd.DataFrame(st_rows)
    sec_rets = {tf: round(float(st_df[f"{tf} %"].mean()), 2) for tf in ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"]}

    # নিফটির তুলনায় আলফা (Relative Outperformance)
    alpha_1w = sec_rets["1W"] - nifty_multi_ret["1W"]
    alpha_1m = sec_rets["1M"] - nifty_multi_ret["1M"]
    alpha_3m = sec_rets["3M"] - nifty_multi_ret["3M"]
    alpha_1y = sec_rets["1Y"] - nifty_multi_ret["1Y"]

    breadth_1m = float((st_df["1M %"] > 0).mean()) * 100

    # বর্তমান মোমেন্টাম মিটার স্কোর (0-100) এবং আগের স্কোর (ট্রানজিশন বোঝার জন্য)
    curr_meter = float(np.clip(50 + (alpha_1w * 2.5) + (alpha_1m * 1.5) + ((breadth_1m - 50) * 0.25), 3, 98))
    prev_meter = float(np.clip(50 + (alpha_3m * 1.2) + (alpha_1y * 0.5), 3, 98))

    # রেড -> ইয়েলো -> গ্রিন ট্রানজিশন নির্ধারণ
    if prev_meter < 45 and curr_meter >= 52:
        stage = "🔄 Red ➔ Green (রেড থেকে গ্রিন হচ্ছে)"
        meter_status = "🔴 রেড জোন থেকে ঘুরে 🟢 গ্রিন জোনে প্রবেশ করছে (Bullish Reversal)"
    elif curr_meter >= 65 and prev_meter >= 50:
        stage = "🚀 Strong Green (স্ট্রং গ্রিন জোন)"
        meter_status = "🟢 ফুল গ্রিন জোন — মার্কেটকে লিড দিচ্ছে (Strong Leader)"
    elif prev_meter >= 55 and curr_meter < 45:
        stage = "⚠️ Green ➔ Red (গ্রিন থেকে নামছে)"
        meter_status = "🟢 গ্রিন থেকে কমে 🟡 ইয়েলো/রেড জোনের দিকে নামছে (Cooling Off)"
    elif 40 <= curr_meter < 55:
        stage = "🟡 Yellow Zone (ইয়েলো / ওয়াচলিস্ট জোন)"
        meter_status = "🟡 ইয়েলো জোন — ব্রেকআউট বা রিভার্সালের অপেক্ষায় (Neutral / Watch)"
    else:
        stage = "🔴 Red Zone (ডিপ ভ্যালু / ডাউন জোন)"
        meter_status = "🔴 রেড জোন — সেক্টরটি এখন চাপে বা ভ্যালু জোনে আছে (Beaten Down)"

    sector_master.append({
        "Sector": s_name,
        "Stage": stage,
        "Meter_Status": meter_status,
        "Curr_Meter": round(curr_meter, 1),
        "Prev_Meter": round(prev_meter, 1),
        "valid_tickers": valid,
        "stocks_df": st_df,
        **{f"{k} %": v for k, v in sec_rets.items()},
    })

# ==========================================
# কন্ট্রোল প্যানেল ও ফিল্টার
# ==========================================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([1, 1.4, 1.4, 1.4])

with c1:
    tf_option = st.selectbox("📅 টাইমফ্রেম:", ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"], index=2)
with c2:
    sort_option = st.selectbox(
        "🔃 সাজানোর ক্রম (Sort By):",
        [
            "Meter Score High to Low (স্ট্রং গ্রিন সেক্টর আগে)",
            "Top Return First (সর্বোচ্চ রিটার্ন আগে)",
            "Beaten Down / Red Zone First (সবচেয়ে ডাউন সেক্টর আগে)",
            "Red ➔ Green Turnaround First (রেড থেকে গ্রিন হওয়া আগে)",
        ],
    )
with c3:
    stage_filter = st.selectbox(
        "🎯 মিটার জোন ফিল্টার:",
        [
            "সব সেক্টর (All 32 Sectors)",
            "🔄 Red ➔ Green (রেড থেকে গ্রিন হচ্ছে)",
            "🚀 Strong Green (স্ট্রং গ্রিন জোন)",
            "🟡 Yellow Zone (ইয়েলো / ওয়াচলিস্ট জোন)",
            "⚠️ Green ➔ Red (গ্রিন থেকে নামছে)",
            "🔴 Red Zone (ডিপ ভ্যালু / ডাউন জোন)",
        ],
    )
with c4:
    quick_sec_jump = st.selectbox(
        "🔍 নির্দিষ্ট একটি সেক্টর দেখুন:",
        ["সবগুলো একসাথে দেখুন (Show All)"] + [s["Sector"] for s in sector_master],
    )
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# মেইন ৩টি ট্যাব
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "🧭 ১. প্রিমিয়াম সেক্টর কার্ড ও অ্যানালগ মিটার",
    "🔄 ২. রোটেশন হিটম্যাপ ও মিটার টেবিল",
    "📈 ৩. শেয়ারের নিজস্ব চার্ট ও স্টক মিটার",
])

# ==============================================================================
# TAB 1: প্রিমিয়াম কার্ড + অ্যানালগ স্পিডোমিটার + ড্রিল-ডাউন শেয়ার তালিকা
# ==============================================================================
with tab1:
    days_sel = tf_days_map[tf_option]
    nifty_curr_ret = nifty_multi_ret[tf_option]

    filtered_sectors = [
        s for s in sector_master
        if (stage_filter.startswith("সব") or s["Stage"] == stage_filter)
        and (quick_sec_jump.startswith("সবগুলো") or s["Sector"] == quick_sec_jump)
    ]

    if "Meter Score" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x["Curr_Meter"], reverse=True)
    elif "Top Return" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[f"{tf_option} %"], reverse=True)
    elif "Beaten Down" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[f"{tf_option} %"], reverse=False)
    else:
        filtered_sectors = sorted(
            filtered_sectors,
            key=lambda x: (x["Stage"].startswith("🔄"), x["Curr_Meter"] - x["Prev_Meter"]),
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
            outperform = s_ret >= nifty_curr_ret
            st_df = sec["stocks_df"].sort_values(by=f"{tf_option} %", ascending=False).reset_index(drop=True)

            up_cnt = int((st_df[f"{tf_option} %"] >= 0).sum())
            dn_cnt = len(st_df) - up_cnt
            badge_cls = "ret-badge-pos" if s_ret >= 0 else "ret-badge-neg"

            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="sec-header">
                        <span class="sec-title">#{idx+1} {s_name}</span>
                        <span class="{badge_cls}">{s_ret:+.2f}% ({tf_option})</span>
                    </div>
                    <div class="transition-pill">{sec['Meter_Status']}</div>
                    <div style="font-size:13px; color:{sub_text}; margin-bottom:6px;">
                        <b>Nifty 50:</b> {nifty_curr_ret:+.2f}% &nbsp;|&nbsp;
                        🟢 বাড়ছে: <b>{up_cnt}টি</b> &nbsp;|&nbsp; 🔴 ডাউন: <b>{dn_cnt}টি</b> &nbsp;|&nbsp;
                        🧭 <b>Meter Score:</b> {sec['Curr_Meter']}/100
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            valid_cols = [t for t in sec["valid_tickers"] if t in norm_sub.columns]
            sec_line = norm_sub[valid_cols].mean(axis=1)

            # চার্ট এবং অ্যানালগ মিটার পাশাপাশি দেখানো
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
                        name=f"{s_name}",
                        line=dict(color="#10b981" if outperform else "#ef4444", width=2.8),
                    )
                )
                if nifty_norm_line is not None:
                    fig.add_trace(
                        go.Scatter(
                            x=norm_sub.index,
                            y=nifty_norm_line,
                            name="Nifty 50",
                            line=dict(color=nifty_col_line, width=1.8, dash="dot"),
                        )
                    )
                fig.update_layout(
                    paper_bgcolor=chart_bg,
                    plot_bgcolor=chart_bg,
                    font=dict(color=text_color),
                    height=220,
                    margin=dict(t=20, b=15, l=10, r=10),
                    legend=dict(orientation="h", y=1.15, x=0, font=dict(size=11)),
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
                        height_px=220,
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True, theme=None, key=f"sec_g_{idx}")

            top_st = st_df.iloc[0]
            bot_st = st_df.iloc[-1]
            st.markdown(
                f"🚀 **টপ শেয়ার:** `{top_st['Stock']} ({top_st[f'{tf_option} %']:+.1f}%)` &nbsp;|&nbsp; "
                f"📉 **পিছিয়ে থাকা শেয়ার:** `{bot_st['Stock']} ({bot_st[f'{tf_option} %']:+.1f}%)`"
            )

            # সেক্টর ওপেন করলে বড় অ্যানালগ মিটার + সব শেয়ারের চার্ট ও টেবিল
            with st.expander(f"🔍 {s_name} ওপেন করুন — অ্যানালগ মিটার, সব শেয়ার ও চার্ট ({len(st_df)}টি শেয়ার)"):
                ex_c1, ex_c2 = st.columns([1, 2])
                with ex_c1:
                    st.markdown(f"**🧭 {s_name} লাইভ রোটেশন মিটার**")
                    big_gauge = make_analog_gauge(
                        sec["Curr_Meter"],
                        sec["Prev_Meter"],
                        f"Prev: {sec['Prev_Meter']} ➔ Now: {sec['Curr_Meter']}",
                        height_px=240,
                    )
                    st.plotly_chart(big_gauge, use_container_width=True, theme=None, key=f"big_g_{idx}")
                    st.caption(
                        "🔺 সবুজ তীর মানে আগের তুলনায় মোমেন্টাম বাড়ছে (Red ➔ Green)। "
                        "🔻 লাল তীর মানে মোমেন্টাম কমছে (Green ➔ Red)।"
                    )

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
                        title=f"{s_name} - সব শেয়ারের তুলনামূলক চার্ট ({tf_option})",
                        paper_bgcolor=chart_bg,
                        plot_bgcolor=chart_bg,
                        font=dict(color=text_color, size=11),
                        height=260,
                        margin=dict(t=35, b=15, l=10, r=10),
                        xaxis=dict(gridcolor=grid_col),
                        yaxis=dict(gridcolor=grid_col, title="Base 100"),
                    )
                    st.plotly_chart(fig_st, use_container_width=True, theme=None, key=f"st_cmp_{idx}")

                disp_cols = [
                    "Stock", "CMP (₹)", "Meter Score", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %"
                ]
                st.dataframe(
                    st_df[disp_cols].style.format({
                        "CMP (₹)": "₹{:.2f}",
                        "Meter Score": "{:.0f}/100",
                        "1D %": "{:+.2f}%",
                        "1W %": "{:+.2f}%",
                        "1M %": "{:+.2f}%",
                        "3M %": "{:+.2f}%",
                        "1Y %": "{:+.2f}%",
                        "From 52W High %": "{:+.2f}%",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )

                links_md = " 🔗 **সরাসরি চার্ট খুলুন:** " + " | ".join(
                    [
                        f"[{r['Stock']} (TV)](https://in.tradingview.com/chart/?symbol=NSE:{r['Stock']}) • "
                        f"[Screener](https://www.screener.in/company/{r['Stock']}/)"
                        for _, r in st_df.iterrows()
                    ]
                )
                st.markdown(links_md)

            st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: রোটেশন হিটম্যাপ ও মিটার টেবিল
# ==============================================================================
with tab2:
    st.subheader("🔄 সেক্টর রোটেশন ও মিটার স্কোর ম্যাট্রিক্স")
    mat_df = pd.DataFrame(sector_master)[
        ["Sector", "Stage", "Curr_Meter", "Prev_Meter", "1D %", "1W %", "1M %", "3M %", "6M %", "1Y %", "5Y %"]
    ].rename(columns={"Curr_Meter": "Current Meter (0-100)", "Prev_Meter": "Previous Meter"})

    mat_df = mat_df.sort_values(by="Current Meter (0-100)", ascending=False)

    st.dataframe(
        mat_df.style.format({
            "Current Meter (0-100)": "{:.1f}",
            "Previous Meter": "{:.1f}",
            "1D %": "{:+.2f}%",
            "1W %": "{:+.2f}%",
            "1M %": "{:+.2f}%",
            "3M %": "{:+.2f}%",
            "6M %": "{:+.2f}%",
            "1Y %": "{:+.2f}%",
            "5Y %": "{:+.2f}%",
        }),
        use_container_width=True,
        height=650,
        hide_index=True,
    )

# ==============================================================================
# TAB 3: শেয়ারের নিজস্ব চার্ট + স্টকের নিজস্ব অ্যানালগ মিটার
# ==============================================================================
with tab3:
    st.subheader("📈 শেয়ারের নিজস্ব অ্যানালগ মিটার এবং টেকনিক্যাল চার্ট")

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

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("বর্তমান দাম (CMP)", f"₹{s_info.get('CMP (₹)', 0)}")
        m2.metric("1W Return", f"{s_info.get('1W %', 0):+.2f}%")
        m3.metric("1M Return", f"{s_info.get('1M %', 0):+.2f}%")
        m4.metric("1Y Return", f"{s_info.get('1Y %', 0):+.2f}%")
        m5.metric("52W High থেকে দূরত্ব", f"{s_info.get('From 52W High %', 0):+.2f}%")

        st.markdown(
            f"👉 **[TradingView-তে {chosen_stock}-এর পূর্ণাঙ্গ চার্ট খুলুন](https://in.tradingview.com/chart/?symbol=NSE:{chosen_stock})** "
            f"&nbsp;|&nbsp; 📊 **[Screener.in-এ {chosen_stock}-এর ফান্ডামেন্টাল দেখুন](https://www.screener.in/company/{chosen_stock}/)**"
        )

        s_full = full_df[t_sym].dropna()
        sma20 = s_full.rolling(20).mean()
        sma50 = s_full.rolling(50).mean()
        sma200 = s_full.rolling(200).mean()

        d_cnt = tf_days_map[chart_tf]
        s_sub = s_full.tail(d_cnt)

        ind_c1, ind_c2 = st.columns([2.3, 1])
        with ind_c1:
            fig_ind = go.Figure()
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=s_sub, name=f"{chosen_stock} Price", line=dict(color="#2563eb", width=2.6))
            )
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=sma20.tail(d_cnt), name="20 DMA", line=dict(color="#f59e0b", width=1.4, dash="dot"))
            )
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=sma50.tail(d_cnt), name="50 DMA", line=dict(color="#10b981", width=1.6))
            )
            fig_ind.add_trace(
                go.Scatter(x=s_sub.index, y=sma200.tail(d_cnt), name="200 DMA", line=dict(color="#ef4444", width=1.8))
            )
            fig_ind.update_layout(
                title=f"{chosen_stock} ({chosen_sec}) - প্রাইস ও মুভিং অ্যাভারেজ ({chart_tf})",
                paper_bgcolor=chart_bg,
                plot_bgcolor=chart_bg,
                font=dict(color=text_color),
                height=380,
                margin=dict(t=45, b=20, l=15, r=15),
                xaxis=dict(gridcolor=grid_col),
                yaxis=dict(gridcolor=grid_col, title="Price (₹)"),
                legend=dict(orientation="h", y=1.08, x=0),
            )
            st.plotly_chart(fig_ind, use_container_width=True, theme=None, key="ind_stock_chart")

        with ind_c2:
            st_score_now = s_info.get("Meter Score", 50.0)
            st_score_prev = float(np.clip(50 + s_info.get("3M %", 0) * 0.8, 5, 95))
            fig_st_gauge = make_analog_gauge(
                st_score_now,
                st_score_prev,
                f"{chosen_stock} মোমেন্টাম মিটার",
                height_px=320,
            )
            st.plotly_chart(fig_st_gauge, use_container_width=True, theme=None, key="ind_stock_gauge")
