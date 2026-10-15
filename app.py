import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# ওয়েব অ্যাপের পেজ সেটআপ
st.set_page_config(
    page_title="Pro Sector Screener", page_icon="📈", layout="wide"
)

st.title("📊 Pro Market Sector Rotation Screener")
st.markdown("বাজারের ২৫টি গুরুত্বপূর্ণ মাইক্রো-সেক্টরের লাইভ পারফরম্যান্স এবং মোমেন্টাম ট্র্যাকার।")

# টাইমফ্রেম সিলেকশন
tf_option = st.selectbox(
    "টাইমফ্রেম নির্বাচন করুন (Timeframe):",
    ["1W", "1M", "3M", "6M", "1Y", "5Y"],
    index=4,
)

period_map = {
    "1W": ("7d", "1d"),
    "1M": ("1mo", "1d"),
    "3M": ("3mo", "1d"),
    "6M": ("6mo", "1d"),
    "1Y": ("1y", "1d"),
    "5Y": ("5y", "1wk"),
}
period_str, interval_str = period_map[tf_option]

# ২৫টি মেগা ও মাইক্রো-সেক্টর তালিকা
sectors = {
    "Defence & Aerospace": ["MAZDOCK.NS", "COCHINSHIP.NS", "HAL.NS", "BEL.NS", "BDL.NS"],
    "Railways & Wagons": ["RVNL.NS", "IRFC.NS", "TITAGARH.NS", "JWL.NS", "IRCON.NS"],
    "Cables & Wires": ["POLYCAB.NS", "KEI.NS", "FINCABLES.NS", "RRKABEL.NS"],
    "Capital Goods & Heavy Elec": ["ABB.NS", "SIEMENS.NS", "CGPOWER.NS", "CUMMINSIND.NS"],
    "EMS (Electronics Mfg)": ["DIXON.NS", "KAYNES.NS", "SYRMA.NS", "CYIENTDLM.NS"],
    "Green Energy & Solar": ["IREDA.NS", "SUZLON.NS", "WAAREEENER.NS", "KPIGREEN.NS", "BORORENEW.NS"],
    "Power Finance & Trans": ["PFC.NS", "RECLTD.NS", "POWERGRID.NS", "NTPC.NS"],
    "Cooling & Data Center Engg": ["VOLTAS.NS", "BLUESTARCO.NS", "LLOYDSME.NS", "TRITURBINE.NS"],
    "Real Estate & Builders": ["DLF.NS", "MACROTECH.NS", "PRESTIGE.NS", "GODREJPROP.NS"],
    "Building Materials (Pipes/Tiles)": ["ASTRAL.NS", "SUPREMEIND.NS", "KAJARIRCER.NS", "CERA.NS"],
    "CDMO & Niche Pharma": ["LAURUSLABS.NS", "DIVISLAB.NS", "NEULANDLAB.NS", "SYNGENE.NS"],
    "Hospitals & Diagnostics": ["APOLLOHOSP.NS", "MAXHEALTH.NS", "LALPATHLAB.NS", "METROPOLIS.NS"],
    "Auto Ancillaries (Bearings/Tyres)": ["SKFINDIA.NS", "TIMKEN.NS", "MRF.NS", "BALKRISIND.NS"],
    "EV & Auto OEMs": ["TATAMOTORS.NS", "M&M.NS", "OLECTRA.NS", "TVSMOTOR.NS"],
    "IT Midcap & Niche Tech": ["PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS"],
    "IT Largecap": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS"],
    "PSU Banks": ["SBIN.NS", "PNB.NS", "BOB.NS", "CANBK.NS"],
    "Private Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS"],
    "NBFCs & Microfinance": ["BAJFINANCE.NS", "CHOLAFIN.NS", "CREDITACC.NS", "M&MFIN.NS"],
    "QSR & Food Chains": ["JUBLFOOD.NS", "DEVYANI.NS", "WESTLIFE.NS", "RBA.NS"],
    "FMCG Staples": ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS"],
    "Hotels & Tourism": ["INDHOTEL.NS", "EIHOTEL.NS", "LEMONTREE.NS", "CHALET.NS"],
    "Specialty Chemicals": ["SRF.NS", "PIIND.NS", "NAVINFLUOR.NS", "DEEPAKNTR.NS"],
    "Shipbuilding": ["GRSE.NS", "GMDCLTD.NS", "SCI.NS", "SJVN.NS"], # Mixed proxy for marine/shipping
    "Metals & Mining": ["TATASTEEL.NS", "COALINDIA.NS", "HINDALCO.NS", "JINDALSTEL.NS"]
}

benchmark = "^NSEI"
all_tickers = [benchmark] + [t for s in sectors.values() for t in s]

@st.cache_data(ttl=3600)
def load_data(p_str, i_str):
    raw = yf.download(all_tickers, period=p_str, interval=i_str, auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.levels[0]:
            return raw["Close"].ffill().bfill()
    return raw.ffill().bfill()

with st.spinner("লাইভ মার্কেট ডেটা আনা হচ্ছে (১৫-২০ সেকেন্ড সময় লাগতে পারে)..."):
    df = load_data(period_str, interval_str)

if df is not None and not df.empty:
    norm = pd.DataFrame(index=df.index)
    for col in df.columns:
        s = df[col].dropna()
        if len(s) > 0:
            norm[col] = (df[col] / s.iloc[0]) * 100

    nifty_series = norm[benchmark] if benchmark in norm.columns else None

    sector_results = []
    for s_name, tickers in sectors.items():
        valid = [t for t in tickers if t in norm.columns]
        if valid:
            sec_line = norm[valid].mean(axis=1)
            sec_ret = float(sec_line.iloc[-1] - 100)
            nifty_ret = float(nifty_series.iloc[-1] - 100) if nifty_series is not None else 0.0
            outperform = sec_ret >= nifty_ret

            stocks_perf = []
            for t in valid:
                st_ret = float(norm[t].dropna().iloc[-1] - 100)
                stocks_perf.append({"name": t.replace(".NS", ""), "ret": round(st_ret, 2)})
            
            stocks_perf = sorted(stocks_perf, key=lambda x: x["ret"], reverse=True)

            sector_results.append({
                "name": s_name,
                "ret": round(sec_ret, 2),
                "outperform": outperform,
                "line": sec_line,
                "stocks": stocks_perf,
            })

    # যে সেক্টর সবচেয়ে বেশি রিটার্ন দিয়েছে সেটি প্রথমে থাকবে
    sector_results = sorted(sector_results, key=lambda x: x["ret"], reverse=True)

    cols = st.columns(2)
    for idx, sec in enumerate(sector_results):
        with cols[idx % 2]:
            st.markdown(f"### #{idx+1} {sec['name']} ({sec['ret']:+.2f}%)")

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=norm.index, y=sec["line"], name=sec["name"],
                    line=dict(color="#10b981" if sec["outperform"] else "#ef4444", width=2.5)
                )
            )
            if nifty_series is not None:
                fig.add_trace(
                    go.Scatter(
                        x=norm.index, y=nifty_series, name="Nifty 50",
                        line=dict(color="rgba(255,255,255,0.5)", width=1.5, dash="dot")
                    )
                )

            fig.update_layout(
                template="plotly_dark", height=250, margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="h", y=1.1, x=0)
            )
            st.plotly_chart(fig, use_container_width=True)

            stock_tags = " | ".join([f"**{st['name']}**: `{st['ret']:+.1f}%`" for st in sec["stocks"][:3]])
            st.markdown(f"🔥 টপ শেয়ার: {stock_tags}")
            st.markdown("---")
