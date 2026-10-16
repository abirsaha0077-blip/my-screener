import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# ==========================================
# ১. পেজ ও সাইডবার সেটআপ
# ==========================================
st.set_page_config(
    page_title="Pro Screener Suite", page_icon="📈", layout="wide", initial_sidebar_state="expanded"
)

# সাইডবার মেনু
with st.sidebar:
    st.markdown("## ⚙️ সেটিংস ও কন্ট্রোল")
    theme_choice = st.selectbox(
        "🎨 থিম বেছে নিন (Theme):",
        ["☀️ Pure White Luxury", "💎 Executive Frost Blue", "🌙 Midnight Pro Dark"],
        index=0,
    )
    tf_option = st.selectbox(
        "📅 টাইমফ্রেম (Timeframe):",
        ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y"],
        index=2,
    )
    st.markdown("---")
    show_card_meter = st.toggle("🎛️ অ্যানালগ স্পিডোমিটার দেখান", value=True)
    st.markdown("---")
    st.caption("Developed with ❤️ for the Trading Community")

# থিম কনফিগারেশন
if "Pure White" in theme_choice:
    bg_color, card_bg, text_color, sub_text, border_col = "#f8fafc", "#ffffff", "#0f172a", "#475569", "#e2e8f0"
    chart_bg, grid_col, nifty_col_line = "#ffffff", "rgba(15, 23, 42, 0.07)", "#64748b"
elif "Frost Blue" in theme_choice:
    bg_color, card_bg, text_color, sub_text, border_col = "#f0f7ff", "#ffffff", "#0c4a6e", "#334155", "#bae6fd"
    chart_bg, grid_col, nifty_col_line = "#ffffff", "rgba(12, 74, 110, 0.07)", "#0284c7"
else:
    bg_color, card_bg, text_color, sub_text, border_col = "#0b0f19", "#111827", "#f8fafc", "#94a3b8", "#1f2937"
    chart_bg, grid_col, nifty_col_line = "#111827", "rgba(255, 255, 255, 0.07)", "#facc15"

# প্রিমিয়াম CSS (Hover Effects, Metric Cards)
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; font-family: 'Inter', sans-serif; }}
    .premium-card {{
        background-color: {card_bg}; border: 1px solid {border_col}; border-radius: 12px;
        padding: 16px 20px; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .premium-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
    .metric-box {{
        background: linear-gradient(135deg, {card_bg} 0%, {bg_color} 100%);
        border: 1px solid {border_col}; border-radius: 12px; padding: 20px;
        text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }}
    .metric-val {{ font-size: 28px; font-weight: 800; color: {text_color}; margin: 5px 0; }}
    .metric-lbl {{ font-size: 14px; font-weight: 600; color: {sub_text}; text-transform: uppercase; letter-spacing: 1px; }}
    .pill-green {{ background: rgba(16,185,129,0.15); color: #059669; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 13px; }}
    .pill-red {{ background: rgba(239,68,68,0.15); color: #dc2626; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 13px; }}
    </style>
    """, unsafe_allow_html=True
)

st.markdown(f"<h1 style='text-align:center; color:{text_color}; font-weight:800;'>📊 Pro Sector Rotation Suite</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{sub_text}; font-size:16px;'>ইন্ডিয়ান শেয়ার বাজারের রিয়েল-টাইম মোমেন্টাম, টার্নঅ্যারাউন্ড এবং ব্রেকআউট স্ক্যানার</p><br>", unsafe_allow_html=True)

# ==========================================
# ২. সেক্টর ও ডেটা ফেচিং
# ==========================================
sectors = {
    "Defence & Aerospace": ["HAL.NS", "BEL.NS", "BDL.NS", "MAZDOCK.NS", "DATAPATTNS.NS"],
    "Shipbuilding & Marine": ["COCHINSHIP.NS", "GRSE.NS", "SCI.NS", "GEESHIP.NS"],
    "Railways": ["RVNL.NS", "IRFC.NS", "TITAGARH.NS", "JWL.NS", "IRCON.NS"],
    "Cables & Wires": ["POLYCAB.NS", "KEI.NS", "FINCABLES.NS", "RRKABEL.NS"],
    "EMS (Electronics)": ["DIXON.NS", "KAYNES.NS", "SYRMA.NS", "CYIENTDLM.NS"],
    "Green Energy": ["IREDA.NS", "SUZLON.NS", "KPIGREEN.NS", "WAAREEENER.NS"],
    "Power Utilities": ["PFC.NS", "RECLTD.NS", "POWERGRID.NS", "NTPC.NS", "TATAPOWER.NS"],
    "Cooling & HVAC": ["VOLTAS.NS", "BLUESTARCO.NS", "TRITURBINE.NS", "ELGIEQUIP.NS"],
    "Infra & EPC": ["LT.NS", "KPIL.NS", "KEC.NS", "NCC.NS", "PNCINFRA.NS"],
    "Real Estate": ["DLF.NS", "MACROTECH.NS", "PRESTIGE.NS", "GODREJPROP.NS"],
    "CDMO Pharma": ["LAURUSLABS.NS", "DIVISLAB.NS", "NEULANDLAB.NS", "SYNGENE.NS"],
    "Hospitals": ["APOLLOHOSP.NS", "MAXHEALTH.NS", "LALPATHLAB.NS", "NH.NS"],
    "Auto OEMs": ["M&M.NS", "TATAMOTORS.NS", "MARUTI.NS", "TVSMOTOR.NS", "OLECTRA.NS"],
    "IT Largecap": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS"],
    "IT Midcap": ["PERSISTENT.NS", "COFORGE.NS", "KPITTECH.NS", "TATAELXSI.NS"],
    "PSU Banks": ["SBIN.NS", "PNB.NS", "BANKBARODA.NS", "CANBK.NS"],
    "Private Banks": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS"],
    "NBFCs": ["BAJFINANCE.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS"],
    "Specialty Chem": ["SRF.NS", "PIIND.NS", "NAVINFLUOR.NS", "DEEPAKNTR.NS"],
    "Hotels": ["INDIGO.NS", "INDHOTEL.NS", "EIHOTEL.NS", "LEMONTREE.NS"],
    "Metals": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "COALINDIA.NS"],
}

benchmark = "^NSEI"
all_tickers = sorted(list(set([benchmark] + [t for s in sectors.values() for t in s])))

@st.cache_data(ttl=3600)
def load_data():
    raw = yf.download(all_tickers, period="5y", interval="1d", auto_adjust=True, progress=False)
    return raw["Close"].ffill() if isinstance(raw.columns, pd.MultiIndex) else raw.ffill()

with st.spinner("লাইভ মার্কেট ডেটা আনা হচ্ছে..."):
    full_df = load_data()

tf_days_map = {"1D": 2, "1W": 6, "1M": 22, "3M": 64, "6M": 126, "1Y": 252, "5Y": len(full_df)}
def calc_ret(series, days):
    s = series.dropna()
    return round(((s.iloc[-1] / s.iloc[0]) - 1) * 100, 2) if len(s) >= 2 and s.iloc[0] != 0 else 0.0

nifty_col = full_df[benchmark] if benchmark in full_df.columns else pd.Series(dtype=float)
nifty_ret = calc_ret(nifty_col, tf_days_map[tf_option])

# ==========================================
# ৩. অ্যানালগ মিটার ফাংশন
# ==========================================
def make_analog_gauge(score, prev_score, title_txt, height_px=220):
    bar_col = "#10b981" if score >= 65 else "#84cc16" if score >= 50 else "#f59e0b" if score >= 35 else "#ef4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=score,
        delta={"reference": prev_score, "increasing": {"color": "#10b981"}, "decreasing": {"color": "#ef4444"}},
        title={"text": title_txt, "font": {"size": 13, "color": text_color}},
        number={"font": {"size": 24, "color": text_color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": sub_text},
            "bar": {"color": bar_col, "thickness": 0.3},
            "bgcolor": chart_bg, "borderwidth": 1, "bordercolor": border_col,
            "steps": [
                {"range": [0, 35], "color": "rgba(239,68,68,0.15)"},
                {"range": [35, 50], "color": "rgba(245,158,11,0.15)"},
                {"range": [50, 65], "color": "rgba(132,204,22,0.15)"},
                {"range": [65, 100], "color": "rgba(16,185,129,0.15)"},
            ],
            "threshold": {"line": {"color": text_color, "width": 4}, "thickness": 0.8, "value": score}
        }
    ))
    fig.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, height=height_px, margin=dict(t=35, b=10, l=15, r=15))
    return fig

# প্রসেসিং ডেটা
sector_master = []
all_stocks_list = []
total_up, total_dn = 0, 0

for s_name, tickers in sectors.items():
    valid = [t for t in tickers if t in full_df.columns and len(full_df[t].dropna()) > 5]
    if not valid: continue

    st_rows = []
    for t in valid:
        s_price = full_df[t].dropna()
        curr_p = float(s_price.iloc[-1])
        high_52w = float(s_price.tail(252).max())
        dd_52w = round(((curr_p / high_52w) - 1) * 100, 2) if high_52w > 0 else 0.0
        
        r_opt = calc_ret(s_price, tf_days_map[tf_option])
        r_1w, r_1m, r_3m = calc_ret(s_price, 6), calc_ret(s_price, 22), calc_ret(s_price, 64)
        
        if r_opt >= 0: total_up += 1
        else: total_dn += 1

        row = {"Stock": t.replace(".NS", ""), "Sector": s_name, "CMP": curr_p, "Ret": r_opt, "1W": r_1w, "1M": r_1m, "DD_52W": dd_52w}
        st_rows.append(row)
        all_stocks_list.append(row)

    st_df = pd.DataFrame(st_rows)
    s_ret = round(float(st_df["Ret"].mean()), 2)
    s_1w = round(float(st_df["1W"].mean()), 2)
    s_1m = round(float(st_df["1M"].mean()), 2)
    
    curr_meter = np.clip(50 + (s_1w * 2.5) + (s_1m * 1.5), 5, 98)
    prev_meter = np.clip(50 + (s_1m * 1.5), 5, 98)
    
    status = "🚀 Strong Leader" if curr_meter >= 65 else "🔄 Turning Green" if curr_meter >= 50 else "⚠️ Cooling Off" if curr_meter >= 35 else "🔴 Red Zone"
    
    sector_master.append({
        "Sector": s_name, "Ret": s_ret, "Meter": curr_meter, "PrevMeter": prev_meter,
        "Status": status, "Valid": valid, "Stocks": st_df
    })

# ==========================================
# ৪. মার্কেট পালস (Hero Dashboard)
# ==========================================
top_sec = max(sector_master, key=lambda x: x["Ret"]) if sector_master else None

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Nifty 50 ({tf_option})</div>
        <div class="metric-val">{'🟢' if nifty_ret>=0 else '🔴'} {nifty_ret:+.2f}%</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Market Breadth (Top 100 Stocks)</div>
        <div class="metric-val" style="color:#10b981; font-size:22px;">▲ {total_up} Adv <span style="color:{sub_text};">|</span> <span style="color:#ef4444;">▼ {total_dn} Dec</span></div>
    </div>""", unsafe_allow_html=True)
with m3:
    if top_sec:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-lbl">Top Leading Sector</div>
            <div class="metric-val">👑 {top_sec['Sector']} <span style="font-size:16px;">({top_sec['Ret']:+.2f}%)</span></div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# ৫. ৪টি মেইন ট্যাব (Tabs)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🧭 ১. সেক্টর ড্যাশবোর্ড ও মিটার", 
    "🔥 ২. অটো-স্ক্যানার (Breakout & Value)", 
    "🔄 ৩. রোটেশন ম্যাট্রিক্স", 
    "📈 ৪. স্টক অ্যানালাইজার"
])

# ----- TAB 1: সেক্টর ড্যাশবোর্ড -----
with tab1:
    filter_col, sort_col = st.columns([1, 1])
    with filter_col:
        stage_filter = st.selectbox("🎯 মিটার ফিল্টার:", ["All Sectors", "🚀 Strong Leader", "🔄 Turning Green", "⚠️ Cooling Off", "🔴 Red Zone"])
    with sort_col:
        sort_by = st.selectbox("🔃 সাজান:", ["Meter Score (High to Low)", f"Return ({tf_option})"])

    filtered_secs = [s for s in sector_master if stage_filter == "All Sectors" or s["Status"] == stage_filter]
    if "Meter" in sort_by: filtered_secs.sort(key=lambda x: x["Meter"], reverse=True)
    else: filtered_secs.sort(key=lambda x: x["Ret"], reverse=True)

    sub_df = full_df.tail(tf_days_map[tf_option]).copy()
    norm_sub = pd.DataFrame({col: (sub_df[col]/sub_df[col].iloc[0])*100 for col in sub_df.columns if sub_df[col].iloc[0]!=0}, index=sub_df.index)
    nifty_line = norm_sub[benchmark] if benchmark in norm_sub.columns else None

    cols = st.columns(2)
    for idx, sec in enumerate(filtered_secs):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="premium-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:18px; font-weight:700;">#{idx+1} {sec['Sector']}</div>
                    <div class="{'pill-green' if sec['Ret']>=0 else 'pill-red'}">{sec['Ret']:+.2f}%</div>
                </div>
                <div style="color:{sub_text}; font-size:13px; margin-top:5px;">{sec['Status']} • Meter: {sec['Meter']:.0f}/100</div>
            </div>""", unsafe_allow_html=True)

            sec_line = norm_sub[sec["Valid"]].mean(axis=1)
            
            c_ch, c_mt = st.columns([1.7, 1]) if show_card_meter else (st.container(), None)
            with c_ch:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=norm_sub.index, y=sec_line, name="Sector", line=dict(color="#10b981" if sec['Ret']>=nifty_ret else "#ef4444", width=3)))
                if nifty_line is not None: fig.add_trace(go.Scatter(x=norm_sub.index, y=nifty_line, name="Nifty", line=dict(color=nifty_col_line, width=1.5, dash="dot")))
                fig.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, font=dict(color=text_color), height=200, margin=dict(t=10, b=10, l=10, r=10), showlegend=False, xaxis=dict(gridcolor=grid_col), yaxis=dict(gridcolor=grid_col))
                st.plotly_chart(fig, use_container_width=True, key=f"c_{idx}")
            
            if show_card_meter:
                with c_mt:
                    st.plotly_chart(make_analog_gauge(sec["Meter"], sec["PrevMeter"], "Momentum", 200), use_container_width=True, key=f"m_{idx}")
            
            with st.expander(f"🔍 {sec['Sector']}-এর সব শেয়ার দেখুন"):
                st.dataframe(sec["Stocks"].sort_values(by="Ret", ascending=False).style.format({"CMP":"₹{:.1f}", "Ret":"{:+.2f}%", "DD_52W":"{:+.2f}%"}), use_container_width=True, hide_index=True)

# ----- TAB 2: অটো-স্ক্যানার -----
with tab2:
    st.markdown("### 🔥 মার্কেট স্ক্যানার (Top 100 Stocks)")
    all_df = pd.DataFrame(all_stocks_list)
    
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f"#### 🚀 Top Breakout / Momentum (Last {tf_option})")
        st.caption("যে শেয়ারগুলো সবচেয়ে বেশি রিটার্ন দিচ্ছে।")
        top_m = all_df.sort_values(by="Ret", ascending=False).head(10)
        st.dataframe(top_m[["Stock", "Sector", "CMP", "Ret"]].style.format({"CMP":"₹{:.1f}", "Ret":"{:+.2f}%"}), hide_index=True, use_container_width=True)

    with sc2:
        st.markdown("#### 💎 Deep Value / Beaten Down")
        st.caption("যে শেয়ারগুলো ৫২-সপ্তাহের হাই থেকে সবচেয়ে বেশি নিচে পড়ে আছে।")
        top_v = all_df.sort_values(by="DD_52W", ascending=True).head(10)
        st.dataframe(top_v[["Stock", "Sector", "CMP", "DD_52W"]].style.format({"CMP":"₹{:.1f}", "DD_52W":"{:+.2f}%"}), hide_index=True, use_container_width=True)

# ----- TAB 3 & 4: (সংক্ষিপ্ত) -----
with tab3:
    st.markdown("### 🔄 রোটেশন ম্যাট্রিক্স")
    mat_df = pd.DataFrame(sector_master)[["Sector", "Meter", "Ret"]].sort_values(by="Meter", ascending=False)
    st.dataframe(mat_df.style.format({"Meter":"{:.1f}", "Ret":"{:+.2f}%"}), use_container_width=True, hide_index=True)

with tab4:
    st.markdown("### 📈 সিঙ্গেল স্টক অ্যানালাইজার")
    sel_sec = st.selectbox("সেক্টর:", list(sectors.keys()), key="s1")
    sel_stk = st.selectbox("শেয়ার:", [t.replace(".NS","") for t in sectors[sel_sec]], key="s2")
    if sel_stk:
        sym = sel_stk+".NS"
        if sym in full_df.columns:
            s_data = full_df[sym].dropna().tail(252)
            fig_s = go.Figure()
            fig_s.add_trace(go.Scatter(x=s_data.index, y=s_data, name="Price", line=dict(color="#3b82f6", width=2)))
            fig_s.add_trace(go.Scatter(x=s_data.index, y=s_data.rolling(50).mean(), name="50 DMA", line=dict(color="#10b981", width=1.5)))
            fig_s.update_layout(paper_bgcolor=chart_bg, plot_bgcolor=chart_bg, font=dict(color=text_color), height=400, xaxis=dict(gridcolor=grid_col), yaxis=dict(gridcolor=grid_col))
            st.plotly_chart(fig_s, use_container_width=True)
            st.markdown(f"👉 **[TradingView-তে {sel_stk} দেখুন](https://in.tradingview.com/chart/?symbol=NSE:{sel_stk})**")
