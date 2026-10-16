import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# ওয়েব অ্যাপের পেজ সেটআপ
st.set_page_config(
    page_title="Pro Sector & Stock Screener", page_icon="📊", layout="wide"
)

st.title("📊 Pro Sector Rotation & Stock Deep-Dive Screener")
st.markdown(
    "মাইক্রো-সেক্টর রোটেশন, টার্নঅ্যারাউন্ড ট্র্যাকার এবং প্রতিটি শেয়ারের "
    "পৃথক চার্ট অ্যানালাইজার।"
)

# ৩০টি মাইক্রো-সেক্টর এবং তার প্রধান শেয়ারের তালিকা
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
        "CGPOWER.NS", "ABB.NS", "SIEMENS.NS", "TARIL.NS", "VOLTAMP.NS", "GEVT&D.NS"
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
        "MOTHERSON.NS", "SONACOMS.NS", "UNO-MINDA.NS", "MRF.NS", "BALKRISIND.NS", "APOLLOTYRE.NS"
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
        "UFLEX.NS", "POLYaaS.NS" if False else "JINDALPOLY.NS", "COSMOFIRST.NS", "EPL.NS", "MOLDTKPAC.NS"
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

@st.cache_data(ttl=3600)
def load_full_history():
    raw = yf.download(all_tickers, period="5y", interval="1d", auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.levels[0]:
            return raw["Close"].ffill()
    return raw.ffill()

with st.spinner("৫ বছরের সম্পূর্ণ মার্কেট ডেটা প্রস্তুত হচ্ছে (প্রথমবার ১৫-২০ সেকেন্ড লাগবে, এরপর এক ক্লিকেই কাজ করবে)..."):
    full_df = load_full_history()

# টাইমফ্রেম অনুযায়ী ট্রেডিং দিনের হিসাব
tf_days_map = {
    "1D": 2,
    "1W": 6,
    "1M": 22,
    "3M": 64,
    "6M": 126,
    "1Y": 252,
    "3Y": 756,
    "5Y": len(full_df),
}

def calc_return(series, days):
    s = series.dropna()
    if len(s) < 2:
        return 0.0
    sub = s.tail(min(days, len(s)))
    if len(sub) < 2 or sub.iloc[0] == 0:
        return 0.0
    return round(((sub.iloc[-1] / sub.iloc[0]) - 1) * 100, 2)

# সব টাইমফ্রেমে নিফটির রিটার্ন হিসাব
nifty_col = full_df[benchmark] if benchmark in full_df.columns else pd.Series(dtype=float)
nifty_multi_ret = {tf: calc_return(nifty_col, d) for tf, d in tf_days_map.items()}

# প্রতিটি সেক্টর এবং স্টকের মাল্টি-টাইমফ্রেম ডেটা তৈরি
sector_master = []
all_stocks_master = {}

for s_name, tickers in sectors.items():
    valid = [t for t in tickers if t in full_df.columns and len(full_df[t].dropna()) > 5]
    if not valid:
        continue

    # প্রতিটি স্টকের মাল্টি-টাইমফ্রেম রিটার্ন এবং ৫২-সপ্তাহের হাই থেকে দূরত্ব
    st_rows = []
    for t in valid:
        s_price = full_df[t].dropna()
        curr_p = round(float(s_price.iloc[-1]), 2)
        high_52w = float(s_price.tail(252).max())
        low_52w = float(s_price.tail(252).min())
        dd_52w = round(((curr_p / high_52w) - 1) * 100, 2) if high_52w > 0 else 0.0

        row_dict = {
            "Ticker": t,
            "Stock": t.replace(".NS", ""),
            "Sector": s_name,
            "CMP (₹)": curr_p,
            "1D %": calc_return(s_price, 2),
            "1W %": calc_return(s_price, 6),
            "1M %": calc_return(s_price, 22),
            "3M %": calc_return(s_price, 64),
            "6M %": calc_return(s_price, 126),
            "1Y %": calc_return(s_price, 252),
            "5Y %": calc_return(s_price, len(full_df)),
            "From 52W High %": dd_52w,
            "52W High": round(high_52w, 2),
            "52W Low": round(low_52w, 2),
        }
        st_rows.append(row_dict)
        all_stocks_master[t] = row_dict

    st_df = pd.DataFrame(st_rows)

    # সেক্টরের গড় রিটার্ন (Equal-Weight)
    sec_rets = {tf: round(float(st_df[f"{tf} %"].mean()), 2) for tf in ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"]}

    # সেক্টর রোটেশন স্টেজ নির্ধারণ (কেমন উপরে ছিল, কোনটা নিচে আসছে বা ঘুরছে)
    r_1y = sec_rets["1Y"]
    r_1m = sec_rets["1M"]
    r_1w = sec_rets["1W"]
    n_1y = nifty_multi_ret["1Y"]
    n_1m = nifty_multi_ret["1M"]

    if r_1y < n_1y and (r_1m > n_1m + 2 or r_1w > 2.5):
        stage = "🔄 Turnaround (নিচ থেকে ঘুরছে)"
    elif r_1y >= n_1y and r_1m >= n_1m:
        stage = "🚀 Strong Leader (উপরে ছুটছে)"
    elif r_1y >= n_1y and r_1m < n_1m - 2:
        stage = "⚠️ Cooling Off (উপর থেকে নামছে)"
    else:
        stage = "💎 Value / Lagging (ডাউন জোন)"

    sector_master.append({
        "Sector": s_name,
        "Stage": stage,
        "valid_tickers": valid,
        "stocks_df": st_df,
        **{f"{k} %": v for k, v in sec_rets.items()},
    })

# ==========================================
# উপরের গ্লোবাল কন্ট্রোল প্যানেল
# ==========================================
st.markdown("### ⚙️ কন্ট্রোল প্যানেল ও ফিল্টার")
c1, c2, c3 = st.columns([1.2, 1.5, 1.5])

with c1:
    tf_option = st.selectbox(
        "📅 টাইমফ্রেম (Timeframe):",
        ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"],
        index=5,
    )

with c2:
    sort_option = st.selectbox(
        "🔃 কীভাবে সাজাতে চান (Sort By):",
        [
            "Top Performers First (সবচেয়ে বেশি বাড়া সেক্টর আগে)",
            "Beaten Down First (সবচেয়ে বেশি ডাউন সেক্টর আগে)",
            "Turnaround / Reversal First (নিচ থেকে ঘুরে দাঁড়ানো আগে)",
        ],
    )

with c3:
    stage_filter = st.selectbox(
        "🎯 রোটেশন ফিল্টার (Rotation Stage):",
        [
            "সব সেক্টর (All 32 Sectors)",
            "🚀 Strong Leader (উপরে ছুটছে)",
            "🔄 Turnaround (নিচ থেকে ঘুরছে)",
            "⚠️ Cooling Off (উপর থেকে নামছে)",
            "💎 Value / Lagging (ডাউন জোন)",
        ],
    )

# মেইন ৩টি ট্যাব
tab1, tab2, tab3 = st.tabs([
    "📊 ১. সেক্টর চার্ট ও সব শেয়ার (Gainers & Losers)",
    "🔄 ২. সেক্টর রোটেশন ম্যাট্রিক্স (উপরে ওঠা ও নিচে নামার পুরো ছবি)",
    "📈 ৩. যেকোনো শেয়ারের নিজস্ব চার্ট (Stock Chart Explorer)",
])

# ==============================================================================
# TAB 1: সেক্টর গ্রিড + প্রতিটি সেক্টরের সব শেয়ার (উপরে ও নিচে থাকা শেয়ার) ও চার্ট
# ==============================================================================
with tab1:
    days_sel = tf_days_map[tf_option]
    nifty_curr_ret = nifty_multi_ret[tf_option]

    st.info(
        f"💡 **নির্বাচিত টাইমফ্রেম ({tf_option})**: Nifty 50 রিটার্ন করেছে **{nifty_curr_ret:+.2f}%**। "
        f"প্রতিটি চার্টের নিচে **'🔍 সব শেয়ার ও চার্ট দেখুন'**-এ ক্লিক করলে ওই সেক্টরের কোন শেয়ার বেড়েছে এবং কোন শেয়ার ডাউন আছে তার পুরো তালিকা ও চার্ট খুলে যাবে!"
    )

    filtered_sectors = [
        s for s in sector_master
        if stage_filter.startswith("সব") or s["Stage"] == stage_filter
    ]

    if "Top Performers" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[f"{tf_option} %"], reverse=True)
    elif "Beaten Down" in sort_option:
        filtered_sectors = sorted(filtered_sectors, key=lambda x: x[f"{tf_option} %"], reverse=False)
    else:
        filtered_sectors = sorted(
            filtered_sectors,
            key=lambda x: (x["Stage"].startswith("🔄"), x["1M %"] - x["1Y %"]),
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

            st.markdown(f"### #{idx+1} {s_name} ({s_ret:+.2f}%)")
            st.caption(
                f"**স্টেজ:** {sec['Stage']} | **Nifty:** {nifty_curr_ret:+.2f}% | "
                f"🟢 বাড়ছে: **{up_cnt}টি** | 🔴 ডাউন: **{dn_cnt}টি**"
            )

            valid_cols = [t for t in sec["valid_tickers"] if t in norm_sub.columns]
            sec_line = norm_sub[valid_cols].mean(axis=1)

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
                        line=dict(color="#facc15", width=1.8, dash="dot"),
                    )
                )

            fig.update_layout(
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",
                font=dict(color="#f8fafc"),
                height=260,
                margin=dict(t=25, b=15, l=15, r=15),
                legend=dict(orientation="h", y=1.14, x=0, font=dict(size=11)),
                xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="Base 100"),
            )
            st.plotly_chart(fig, use_container_width=True, theme=None)

            # টপ গেইনার এবং সবচেয়ে ডাউন শেয়ার এক নজরে
            top_st = st_df.iloc[0]
            bot_st = st_df.iloc[-1]
            st.markdown(
                f"🟢 **টপ গেইনার:** `{top_st['Stock']} ({top_st[f'{tf_option} %']:+.1f}%)` &nbsp;|&nbsp; "
                f"🔴 **সবচেয়ে ডাউন:** `{bot_st['Stock']} ({bot_st[f'{tf_option} %']:+.1f}%)`"
            )

            # খুলে দেখার বক্স (Drill-Down Expander)
            with st.expander(f"🔍 {s_name}-এর সব শেয়ারের তালিকা ও তুলনামূলক চার্ট খুলে দেখুন ({len(st_df)}টি শেয়ার)"):
                # ১. সেক্টরের ভেতরের সব শেয়ারের একসাথে চার্ট
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
                    paper_bgcolor="#0f172a",
                    plot_bgcolor="#0f172a",
                    font=dict(color="#f8fafc", size=11),
                    height=300,
                    margin=dict(t=35, b=15, l=15, r=15),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="Base 100"),
                )
                st.plotly_chart(fig_st, use_container_width=True, theme=None)

                # ২. সব শেয়ারের বিস্তারিত টেবিল
                disp_cols = ["Stock", "CMP (₹)", "1D %", "1W %", "1M %", "3M %", "1Y %", "From 52W High %"]
                st.dataframe(
                    st_df[disp_cols].style.format({
                        "CMP (₹)": "₹{:.2f}",
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

                # ৩. সরাসরি চার্ট ও ফান্ডামেন্টাল খোলার লিংক
                links_md = " 🔗 **সরাসরি চার্ট খুলুন:** " + " | ".join(
                    [
                        f"[{r['Stock']} (TV)](https://in.tradingview.com/chart/?symbol=NSE:{r['Stock']}) • "
                        f"[Screener](https://www.screener.in/company/{r['Stock']}/)"
                        for _, r in st_df.iterrows()
                    ]
                )
                st.markdown(links_md)

            st.markdown("---")

# ==============================================================================
# TAB 2: সেক্টর রোটেশন ম্যাট্রিক্স (কোনটা উপরে ছিল, কোনটা নিচে আসছে বা ঘুরছে)
# ==============================================================================
with tab2:
    st.subheader("🔄 সম্পূর্ণ সেক্টর রোটেশন টেবিল (Multi-Timeframe Heatmap)")
    st.markdown(
        "এখানে যেকোনো কলামের নামের ওপর ক্লিক করে **সবচেয়ে বেশি বাড়া** বা **সবচেয়ে বেশি পড়া** সেক্টর সাজিয়ে নিতে পারবেন। "
        "যারা আগে ডাউন ছিল কিন্তু গত ১ সপ্তাহে বা ১ মাসে প্লাসে এসেছে, তারাই আসল **Turnaround সেক্টর**!"
    )

    mat_df = pd.DataFrame(sector_master)[
        ["Sector", "Stage", "1D %", "1W %", "1M %", "3M %", "6M %", "1Y %", "5Y %"]
    ].sort_values(by=f"{tf_option} %", ascending=False)

    st.dataframe(
        mat_df.style.format({
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
# TAB 3: যেকোনো শেয়ারের ইন্ডিভিজুয়াল চার্ট ও মুভিং অ্যাভারেজ (Stock Explorer)
# ==============================================================================
with tab3:
    st.subheader("📈 শেয়ারের নিজস্ব চার্ট এবং মুভিং অ্যাভারেজ (Individual Stock Analyzer)")

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

        fig_ind = go.Figure()
        fig_ind.add_trace(
            go.Scatter(x=s_sub.index, y=s_sub, name=f"{chosen_stock} Price", line=dict(color="#38bdf8", width=2.5))
        )
        fig_ind.add_trace(
            go.Scatter(x=s_sub.index, y=sma20.tail(d_cnt), name="20 DMA", line=dict(color="#facc15", width=1.3, dash="dot"))
        )
        fig_ind.add_trace(
            go.Scatter(x=s_sub.index, y=sma50.tail(d_cnt), name="50 DMA", line=dict(color="#10b981", width=1.5))
        )
        fig_ind.add_trace(
            go.Scatter(x=s_sub.index, y=sma200.tail(d_cnt), name="200 DMA", line=dict(color="#ef4444", width=1.8))
        )

        fig_ind.update_layout(
            title=f"{chosen_stock} ({chosen_sec}) - প্রাইস চার্ট ও মুভিং অ্যাভারেজ ({chart_tf})",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="#f8fafc"),
            height=450,
            margin=dict(t=45, b=20, l=20, r=20),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="Price (₹)"),
            legend=dict(orientation="h", y=1.08, x=0),
        )
        st.plotly_chart(fig_ind, use_container_width=True, theme=None)
