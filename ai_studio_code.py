import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA EKSEKUTIF TELKOM
# ==============================================================================
st.set_page_config(
    page_title="Telkom Indonesia FY2025 | Executive Monitoring & Risk Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

TELKOM_RED = "#E20613"
TELKOM_DARK = "#333333"
TELKOM_GRAY = "#6C757D"
TELKOM_LIGHT_BG = "#F8F9FA"
TELKOM_WHITE = "#FFFFFF"
GREEN_SAFE = "#198754"

# Custom CSS untuk antarmuka eksekutif yang profesional
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {TELKOM_LIGHT_BG};
            color: {TELKOM_DARK};
        }}
        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: {TELKOM_DARK};
            color: {TELKOM_WHITE};
        }}
        section[data-testid="stSidebar"] * {{
            color: {TELKOM_WHITE};
        }}
        section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {{
            background-color: {TELKOM_RED} !important;
            color: {TELKOM_WHITE} !important;
        }}
        /* Header Banner */
        .exec-header {{
            background: linear-gradient(90deg, {TELKOM_DARK} 0%, #1F1F1F 70%, {TELKOM_RED} 100%);
            padding: 1.4rem 1.8rem;
            border-radius: 10px;
            color: {TELKOM_WHITE};
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}
        .exec-header h1 {{
            margin: 0;
            font-size: 1.65rem;
            font-weight: 700;
            letter-spacing: -0.3px;
            color: {TELKOM_WHITE};
        }}
        .exec-header p {{
            margin: 0.35rem 0 0 0;
            font-size: 0.92rem;
            color: #E5E7EB;
        }}
        /* Custom KPI Card */
        .kpi-card {{
            background-color: {TELKOM_WHITE};
            border-radius: 10px;
            padding: 1.15rem 1.25rem;
            border-top: 4px solid {TELKOM_RED};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            margin-bottom: 0.75rem;
        }}
        .kpi-title {{
            font-size: 0.82rem;
            font-weight: 600;
            color: {TELKOM_GRAY};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.4rem;
        }}
        .kpi-value {{
            font-size: 1.7rem;
            font-weight: 700;
            color: {TELKOM_DARK};
            line-height: 1.2;
        }}
        .kpi-delta-neg {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {TELKOM_RED};
            margin-top: 0.35rem;
        }}
        .kpi-delta-pos {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {GREEN_SAFE};
            margin-top: 0.35rem;
        }}
        .kpi-delta-neu {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {TELKOM_GRAY};
            margin-top: 0.35rem;
        }}
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: {TELKOM_WHITE};
            padding: 6px;
            border-radius: 10px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: 600;
            color: {TELKOM_DARK};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {TELKOM_RED} !important;
            color: {TELKOM_WHITE} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# 2. FUNGSI HELPER FORMAT ANGKA INDONESIA
# ==============================================================================
def fmt_id(value: float, decimals: int = 0) -> str:
    """Format angka ke standar Indonesia (titik ribuan, koma desimal)."""
    if decimals == 0:
        s = f"{value:,.0f}"
    else:
        s = f"{value:,.{decimals}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def render_kpi_card(title: str, value: str, delta_text: str, delta_type: str = "neu"):
    delta_class = {
        "pos": "kpi-delta-pos",
        "neg": "kpi-delta-neg",
        "neu": "kpi-delta-neu",
    }.get(delta_type, "kpi-delta-neu")
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="{delta_class}">{delta_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 3. SIMULASI DATA TERSTRUKTUR (FY 2025 TELKOM INDONESIA)
# ==============================================================================
@st.cache_data
def load_telkom_fy2025_data():
    # --- A. Data Keuangan & Pergeseran Pendapatan per Segmen (Rp Miliar) ---
    df_revenue_streams = pd.DataFrame(
        [
            {
                "Segmen": "B2C",
                "Lini_Bisnis": "Legacy Voice & SMS",
                "Kategori": "Legacy",
                "FY2024_M": 6259.0,
                "FY2025_M": 4400.0,
                "EBITDA_M": 2112.0,
                "Laba_Bersih_M": 680.0,
            },
            {
                "Segmen": "B2C",
                "Lini_Bisnis": "Mobile Data & Digital Services",
                "Kategori": "Data & Digital",
                "FY2024_M": 76500.0,
                "FY2025_M": 74100.0,
                "EBITDA_M": 38902.5,
                "Laba_Bersih_M": 10950.0,
            },
            {
                "Segmen": "B2C",
                "Lini_Bisnis": "IndiHome Fixed Broadband",
                "Kategori": "Data & Digital",
                "FY2024_M": 26800.0,
                "FY2025_M": 27642.0,
                "EBITDA_M": 13544.6,
                "Laba_Bersih_M": 3210.0,
            },
            {
                "Segmen": "B2B Enterprise",
                "Lini_Bisnis": "Enterprise Connectivity, Cloud & IT",
                "Kategori": "Data & Digital",
                "FY2024_M": 21484.0,
                "FY2025_M": 21100.0,
                "EBITDA_M": 6963.0,
                "Laba_Bersih_M": 724.0,
            },
            {
                "Segmen": "Wholesale & International",
                "Lini_Bisnis": "Wholesale, Tower & Carrier",
                "Kategori": "Infrastructure & Wholesale",
                "FY2024_M": 19000.0,
                "FY2025_M": 19500.0,
                "EBITDA_M": 10675.0,
                "Laba_Bersih_M": 2250.0,
            },
        ]
    )
    df_revenue_streams["Delta_M"] = (
        df_revenue_streams["FY2025_M"] - df_revenue_streams["FY2024_M"]
    )
    df_revenue_streams["YoY_Pct"] = (
        df_revenue_streams["Delta_M"] / df_revenue_streams["FY2024_M"] * 100
    )

    # --- B. Data Aging Schedule Piutang & Risiko Bad Debt (Rp Miliar) ---
    df_aging = pd.DataFrame(
        [
            {
                "Segmen_Klien": "Enterprise",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": "0-30 Hari",
                "Gross_Piutang_M": 4350.0,
                "Cadangan_Kerugian_M": 130.5,
                "Tingkat_Risiko": "Rendah",
            },
            {
                "Segmen_Klien": "Enterprise",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": "31-60 Hari",
                "Gross_Piutang_M": 2250.0,
                "Cadangan_Kerugian_M": 337.5,
                "Tingkat_Risiko": "Menengah",
            },
            {
                "Segmen_Klien": "Enterprise",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": "61-90 Hari",
                "Gross_Piutang_M": 1680.0,
                "Cadangan_Kerugian_M": 756.0,
                "Tingkat_Risiko": "Tinggi",
            },
            {
                "Segmen_Klien": "Enterprise",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": ">90 Hari",
                "Gross_Piutang_M": 2920.0,
                "Cadangan_Kerugian_M": 2336.0,
                "Tingkat_Risiko": "Kritis",
            },
            {
                "Segmen_Klien": "Government",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": "0-30 Hari",
                "Gross_Piutang_M": 1820.0,
                "Cadangan_Kerugian_M": 54.6,
                "Tingkat_Risiko": "Rendah",
            },
            {
                "Segmen_Klien": "Government",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": "31-60 Hari",
                "Gross_Piutang_M": 1410.0,
                "Cadangan_Kerugian_M": 211.5,
                "Tingkat_Risiko": "Menengah",
            },
            {
                "Segmen_Klien": "Government",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": "61-90 Hari",
                "Gross_Piutang_M": 1390.0,
                "Cadangan_Kerugian_M": 625.5,
                "Tingkat_Risiko": "Tinggi",
            },
            {
                "Segmen_Klien": "Government",
                "Segmen_Layanan": "B2B Enterprise",
                "Bucket": ">90 Hari",
                "Gross_Piutang_M": 3130.0,
                "Cadangan_Kerugian_M": 2503.4,
                "Tingkat_Risiko": "Kritis",
            },
        ]
    )

    # --- C. Data Tren Pelanggan Kuartalan (Q1 - Q4 2025) ---
    df_subs_quarterly = pd.DataFrame(
        [
            {
                "Kuartal": "FY24 (Base)",
                "Seluler_Juta": 159.4,
                "IndiHome_Juta": 9.65,
                "Churn_Rate_Seluler_Pct": 2.4,
            },
            {
                "Kuartal": "Q1 2025",
                "Seluler_Juta": 158.7,
                "IndiHome_Juta": 9.82,
                "Churn_Rate_Seluler_Pct": 2.7,
            },
            {
                "Kuartal": "Q2 2025",
                "Seluler_Juta": 157.6,
                "IndiHome_Juta": 10.04,
                "Churn_Rate_Seluler_Pct": 3.0,
            },
            {
                "Kuartal": "Q3 2025",
                "Seluler_Juta": 156.8,
                "IndiHome_Juta": 10.26,
                "Churn_Rate_Seluler_Pct": 2.9,
            },
            {
                "Kuartal": "Q4 2025",
                "Seluler_Juta": 156.1,
                "IndiHome_Juta": 10.48,
                "Churn_Rate_Seluler_Pct": 2.8,
            },
        ]
    )

    # --- D. Data Perbandingan ARPU Pasca-Merger XLSmart (Rp Ribu / Bulan) ---
    df_arpu_competitor = pd.DataFrame(
        [
            {"Operator": "Telkomsel", "Segmen_ARPU": "Prepaid Mass", "ARPU_Ribu": 41.2},
            {"Operator": "Telkomsel", "Segmen_ARPU": "Postpaid (Halo)", "ARPU_Ribu": 112.5},
            {"Operator": "Telkomsel", "Segmen_ARPU": "Blended ARPU", "ARPU_Ribu": 44.5},
            {"Operator": "Telkomsel", "Segmen_ARPU": "Fixed-Mobile (FMC)", "ARPU_Ribu": 68.4},
            {"Operator": "XLSmart (Merged)", "Segmen_ARPU": "Prepaid Mass", "ARPU_Ribu": 40.5},
            {"Operator": "XLSmart (Merged)", "Segmen_ARPU": "Postpaid (Halo)", "ARPU_Ribu": 98.0},
            {"Operator": "XLSmart (Merged)", "Segmen_ARPU": "Blended ARPU", "ARPU_Ribu": 43.8},
            {"Operator": "XLSmart (Merged)", "Segmen_ARPU": "Fixed-Mobile (FMC)", "ARPU_Ribu": 64.0},
            {"Operator": "Indosat (IOH)", "Segmen_ARPU": "Prepaid Mass", "ARPU_Ribu": 36.8},
            {"Operator": "Indosat (IOH)", "Segmen_ARPU": "Postpaid (Halo)", "ARPU_Ribu": 89.5},
            {"Operator": "Indosat (IOH)", "Segmen_ARPU": "Blended ARPU", "ARPU_Ribu": 39.2},
            {"Operator": "Indosat (IOH)", "Segmen_ARPU": "Fixed-Mobile (FMC)", "ARPU_Ribu": 54.5},
        ]
    )

    # --- E. Data Portofolio Investasi Digital ---
    df_investments = pd.DataFrame(
        [
            {
                "Klaster_Investasi": "MDI Ventures (Venture Fund)",
                "Nilai_Portofolio_M": 3150.0,
                "Unrealized_Gain_Loss_M": -78.0,
                "Segmen": "B2B Enterprise",
            },
            {
                "Klaster_Investasi": "GoTo Strategic Equity",
                "Nilai_Portofolio_M": 1950.0,
                "Unrealized_Gain_Loss_M": -164.0,
                "Segmen": "B2C",
            },
            {
                "Klaster_Investasi": "Data Center & Cloud (NeutraDC)",
                "Nilai_Portofolio_M": 1680.0,
                "Unrealized_Gain_Loss_M": 115.0,
                "Segmen": "Wholesale & International",
            },
            {
                "Klaster_Investasi": "FinTech & Digital Payment",
                "Nilai_Portofolio_M": 670.0,
                "Unrealized_Gain_Loss_M": -32.0,
                "Segmen": "B2C",
            },
            {
                "Klaster_Investasi": "B2B SaaS & Agri/HealthTech",
                "Nilai_Portofolio_M": 400.0,
                "Unrealized_Gain_Loss_M": -18.0,
                "Segmen": "B2B Enterprise",
            },
        ]
    )

    # --- F. Data Kesehatan Keuangan Entitas Anak ---
    df_subsidiaries = pd.DataFrame(
        [
            {
                "Entitas Anak": "Telkomsat",
                "Segmen_Utama": "Wholesale & International",
                "Fokus Bisnis": "Layanan Satelit & Konektivitas Maritim/3T",
                "Pendapatan FY25 (Rp M)": 2140.0,
                "Laba/Rugi Bersih (Rp M)": -249.5,
                "EBITDA Margin (%)": 28.4,
                "Debt-to-Equity (x)": 1.85,
                "ROIC (%)": -4.2,
                "Status Kesehatan": "🔴 High Risk (Turnaround)",
            },
            {
                "Entitas Anak": "InfraNexia",
                "Segmen_Utama": "Wholesale & International",
                "Fokus Bisnis": "Fiber Optic Wholesale & Neutral InfraCo",
                "Pendapatan FY25 (Rp M)": 8420.0,
                "Laba/Rugi Bersih (Rp M)": 1185.0,
                "EBITDA Margin (%)": 58.6,
                "Debt-to-Equity (x)": 0.92,
                "ROIC (%)": 8.9,
                "Status Kesehatan": "🟡 Watchlist (Capex Heavy)",
            },
            {
                "Entitas Anak": "Mitratel (MTEL)",
                "Segmen_Utama": "Wholesale & International",
                "Fokus Bisnis": "Menara Telekomunikasi & Fiber-to-the-Tower",
                "Pendapatan FY25 (Rp M)": 9310.0,
                "Laba/Rugi Bersih (Rp M)": 2120.0,
                "EBITDA Margin (%)": 82.8,
                "Debt-to-Equity (x)": 0.56,
                "ROIC (%)": 11.4,
                "Status Kesehatan": "🟢 Healthy (Outperform)",
            },
            {
                "Entitas Anak": "Telkomsel",
                "Segmen_Utama": "B2C",
                "Fokus Bisnis": "Seluler & Fixed Broadband (IndiHome)",
                "Pendapatan FY25 (Rp M)": 106142.0,
                "Laba/Rugi Bersih (Rp M)": 14840.0,
                "EBITDA Margin (%)": 51.4,
                "Debt-to-Equity (x)": 0.44,
                "ROIC (%)": 18.7,
                "Status Kesehatan": "🟡 Watchlist (ARPU Pressure)",
            },
            {
                "Entitas Anak": "TelkomSigma",
                "Segmen_Utama": "B2B Enterprise",
                "Fokus Bisnis": "Enterprise IT Services, Cloud & System Integrator",
                "Pendapatan FY25 (Rp M)": 4890.0,
                "Laba/Rugi Bersih (Rp M)": 142.0,
                "EBITDA Margin (%)": 16.5,
                "Debt-to-Equity (x)": 1.12,
                "ROIC (%)": 5.1,
                "Status Kesehatan": "🟡 Watchlist (Piutang B2B)",
            },
        ]
    )

    return (
        df_revenue_streams,
        df_aging,
        df_subs_quarterly,
        df_arpu_competitor,
        df_investments,
        df_subsidiaries,
    )


(
    df_rev,
    df_aging,
    df_subs,
    df_arpu,
    df_inv,
    df_subsi,
) = load_telkom_fy2025_data()


# ==============================================================================
# 4. SIDEBAR & FILTER GLOBAL
# ==============================================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #4B5563;">
            <div style="font-size: 1.3rem; font-weight: 800; color: {TELKOM_WHITE};">
                <span style="color: {TELKOM_RED};">●</span> TELKOM INDONESIA
            </div>
            <div style="font-size: 0.82rem; color: #D1D5DB; margin-top: 2px;">
                Executive Monitoring & Risk Cockpit<br>Tahun Fiskal 2025
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎛️ Filter Global Segmen")
    all_segments = ["B2C", "B2B Enterprise", "Wholesale & International"]
    selected_segments = st.multiselect(
        "Pilih Segmen Layanan:",
        options=all_segments,
        default=all_segments,
        help="Filter ini menyesuaikan metrik pendapatan, EBITDA, serta konteks risiko pada setiap tab.",
    )

    if not selected_segments:
        st.warning("Minimal satu segmen harus dipilih. Menampilkan seluruh segmen.")
        selected_segments = all_segments

    is_consolidated = set(selected_segments) == set(all_segments)

    st.markdown("---")
    st.markdown("### 📌 Ringkasan Risiko Utama FY25")
    st.markdown(
        """
        - **Revenue Shift:** Penurunan tajam *Legacy Voice/SMS* (-29,7% YoY).
        - **Credit Risk:** Provisi piutang melonjak **+62,1% YoY** ke Rp6.601 Miliar.
        - **Market Competition:** Konsolidasi **XLSmart** menekan ARPU & *churn* seluler (-3,3 Juta).
        - **Portfolio Drag:** Rugi Telkomsat (-Rp249,5 M) & *unrealized loss* GoTo/MDI (-Rp242 M).
        """
    )
    st.markdown("---")
    st.caption("Versi 2025.4 | Board Risk & Strategy Committee")


# ==============================================================================
# 5. HEADER UTAMA & NAVIGASI 4 TAB
# ==============================================================================
segment_badge = (
    "Konsolidasian (Seluruh Segmen)"
    if is_consolidated
    else "Terfilter: " + ", ".join(selected_segments)
)

st.markdown(
    f"""
    <div class="exec-header">
        <h1>Dashboard Executive Monitoring & Risk Management — PT Telkom Indonesia Tbk (FY 2025)</h1>
        <p>Pemantauan Kinerja Keuangan, Mitigasi Risiko Piutang (Bad Debt), Retensi Pelanggan Seluler, & Kesehatan Entitas Anak &nbsp;|&nbsp; <b>Scope: {segment_badge}</b></p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Financial & Operational Overview",
        "⚠️ Credit Risk & Bad Debt Analytics",
        "📉 Subscriber Churn & ARPU Tracker",
        "🏢 Subsidiary & Investment Health Check",
    ]
)


# ==============================================================================
# TAB 1: FINANCIAL & OPERATIONAL OVERVIEW
# ==============================================================================
with tab1:
    df_rev_filt = df_rev[df_rev["Segmen"].isin(selected_segments)].copy()

    rev_2025 = df_rev_filt["FY2025_M"].sum()
    rev_2024 = df_rev_filt["FY2024_M"].sum()
    rev_yoy = ((rev_2025 - rev_2024) / rev_2024) * 100
    ebitda_2025 = df_rev_filt["EBITDA_M"].sum()
    ebitda_margin = (ebitda_2025 / rev_2025) * 100
    net_income_2025 = df_rev_filt["Laba_Bersih_M"].sum()
    ni_yoy_text = (
        "▼ -17,1% YoY (vs FY24: Rp21.489 M)"
        if is_consolidated
        else f"Kontribusi Laba Segmen Terpilih ({(net_income_2025/17814)*100:.1f}% Konsol.)"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card(
            "Pendapatan Konsolidasian" if is_consolidated else "Pendapatan Segmen Terpilih",
            f"Rp{fmt_id(rev_2025)} Miliar",
            f"▼ {fmt_id(rev_yoy, 1)}% YoY (FY24: Rp{fmt_id(rev_2024)} M)",
            "neg" if rev_yoy < 0 else "pos",
        )
    with col2:
        render_kpi_card(
            "Laba Bersih Induk" if is_consolidated else "Laba Bersih Segmen Terpilih",
            f"Rp{fmt_id(net_income_2025)} Miliar",
            ni_yoy_text,
            "neg" if is_consolidated else "neu",
        )
    with col3:
        render_kpi_card(
            "EBITDA Margin",
            f"{fmt_id(ebitda_margin, 1)}%",
            f"EBITDA: Rp{fmt_id(ebitda_2025)} Miliar",
            "pos" if ebitda_margin >= 48 else "neu",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    c_left, c_right = st.columns([1.35, 1])

    with c_left:
        st.subheader("Bridge Pergeseran Pendapatan: FY 2024 → FY 2025 (Rp Miliar)")
        wf_x = ["Pendapatan FY2024"] + df_rev_filt["Lini_Bisnis"].tolist() + ["Pendapatan FY2025"]
        wf_y = [rev_2024] + df_rev_filt["Delta_M"].tolist() + [0]
        wf_measure = ["absolute"] + ["relative"] * len(df_rev_filt) + ["total"]
        wf_text = (
            [f"Rp{fmt_id(rev_2024)}M"]
            + [
                f"{'+' if d >= 0 else ''}Rp{fmt_id(d)}M ({y:+.1f}%)"
                for d, y in zip(df_rev_filt["Delta_M"], df_rev_filt["YoY_Pct"])
            ]
            + [f"Rp{fmt_id(rev_2025)}M"]
        )

        fig_wf = go.Figure(
            go.Waterfall(
                name="Revenue Bridge",
                orientation="v",
                measure=wf_measure,
                x=wf_x,
                y=wf_y,
                text=wf_text,
                textposition="outside",
                connector={"line": {"color": "#9CA3AF", "width": 1.2, "dash": "dot"}},
                decreasing={"marker": {"color": TELKOM_RED}},
                increasing={"marker": {"color": GREEN_SAFE}},
                totals={"marker": {"color": TELKOM_DARK}},
            )
        )
        fig_wf.update_layout(
            height=430,
            margin=dict(t=30, b=30, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="Nilai (Rp Miliar)",
            yaxis=dict(gridcolor="#E5E7EB", range=[0, max(rev_2024, rev_2025) * 1.15]),
            xaxis=dict(tickangle=-15),
            showlegend=False,
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with c_right:
        st.subheader("Komparasi Legacy Voice/SMS vs Data & Digital")
        df_comp = df_rev_filt.melt(
            id_vars=["Lini_Bisnis", "Kategori", "YoY_Pct"],
            value_vars=["FY2024_M", "FY2025_M"],
            var_name="Tahun",
            value_name="Pendapatan_M",
        )
        df_comp["Tahun"] = df_comp["Tahun"].replace(
            {"FY2024_M": "FY 2024", "FY2025_M": "FY 2025"}
        )

        fig_bar_rev = px.bar(
            df_comp,
            x="Pendapatan_M",
            y="Lini_Bisnis",
            color="Tahun",
            barmode="group",
            orientation="h",
            text_auto=".0f",
            color_discrete_map={"FY 2024": "#9CA3AF", "FY 2025": TELKOM_RED},
            labels={"Pendapatan_M": "Pendapatan (Rp Miliar)", "Lini_Bisnis": ""},
        )
        fig_bar_rev.update_layout(
            height=430,
            margin=dict(t=30, b=30, l=10, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="#E5E7EB"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_bar_rev, use_container_width=True)

    st.info(
        "💡 **Executive Insight (Tab 1):** Pendapatan *Legacy Voice/SMS* terkontraksi tajam **-29,7% YoY** menjadi **Rp4.400 Miliar**. "
        "Meskipun *IndiHome* (+3,1%) dan *Wholesale/Tower* (+2,6%) bertumbuh, perlambatan *Mobile Data* (-3,1%) akibat perang harga membuat pertumbuhan digital belum sepenuhnya mengompensasi kanibalisasi *legacy*."
    )


# ==============================================================================
# TAB 2: CREDIT RISK & BAD DEBT ANALYTICS
# ==============================================================================
with tab2:
    if "B2B Enterprise" not in selected_segments:
        st.warning(
            "Catatan: Eksposur piutang korporasi & pemerintahan terutama berada pada segmen **B2B Enterprise**. "
            "Grafik di bawah menampilkan profil lengkap risiko piutang Enterprise & Government Telkom."
        )

    total_cadangan = 6955.0
    beban_provisi = 6601.0
    total_gross_b2b = df_aging["Gross_Piutang_M"].sum()
    high_risk_pool = df_aging[df_aging["Bucket"].isin(["61-90 Hari", ">90 Hari"])][
        "Gross_Piutang_M"
    ].sum()

    k1, k2, k3 = st.columns(3)
    with k1:
        render_kpi_card(
            "Total Cadangan Piutang (ECL)",
            f"Rp{fmt_id(total_cadangan)} Miliar",
            f"Rasio Coverage: {(total_cadangan / total_gross_b2b * 100):.1f}% dari Gross Piutang B2B/Gov",
            "neg",
        )
    with k2:
        render_kpi_card(
            "Beban Provisi Piutang FY25",
            f"Rp{fmt_id(beban_provisi)} Miliar",
            "▲ +62,1% YoY (vs FY24: Rp4.072 Miliar)",
            "neg",
        )
    with k3:
        render_kpi_card(
            "Piutang Menunggak (>60 Hari)",
            f"Rp{fmt_id(high_risk_pool)} Miliar",
            "Fokus Utama Penagihan (Enterprise & Gov)",
            "neg",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_age, col_sim = st.columns([1.2, 1])

    with col_age:
        st.subheader("Aging Schedule Piutang: Enterprise vs Government (Rp Miliar)")
        bucket_order = ["0-30 Hari", "31-60 Hari", "61-90 Hari", ">90 Hari"]

        metric_choice = st.radio(
            "Tampilkan Metrik Piutang:",
            ["Gross Piutang (Rp Miliar)", "Cadangan Kerugian / Bad Debt (Rp Miliar)"],
            horizontal=True,
        )
        y_col = (
            "Gross_Piutang_M"
            if metric_choice.startswith("Gross")
            else "Cadangan_Kerugian_M"
        )

        fig_aging = px.bar(
            df_aging,
            x="Bucket",
            y=y_col,
            color="Segmen_Klien",
            barmode="group",
            category_orders={"Bucket": bucket_order},
            text_auto=".0f",
            color_discrete_map={"Enterprise": TELKOM_DARK, "Government": TELKOM_RED},
            labels={
                "Bucket": "Umur Piutang",
                y_col: "Nilai (Rp Miliar)",
                "Segmen_Klien": "Segmen Klien",
            },
        )
        fig_aging.update_layout(
            height=410,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#E5E7EB"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_aging, use_container_width=True)

    with col_sim:
        st.subheader("🛠️ Interactive Credit Recovery Simulator")
        st.markdown(
            "Simulasikan dampak peningkatan efektivitas penagihan pada piutang bermasalah "
            f"(**>60 hari** senilai **Rp{fmt_id(high_risk_pool)} Miliar** dan cadangan kerugian **Rp{fmt_id(6220.9, 1)} Miliar**) "
            "terhadap pemulihan arus kas operasional (*cash flow recovery*)."
        )

        recovery_eff = st.slider(
            "Target Rasio Efisiensi Penagihan Piutang (%)",
            min_value=5,
            max_value=75,
            value=25,
            step=5,
            help="Persentase piutang macet (>60 hari) yang berhasil ditagih melalui restrukturisasi, legal action, atau offset proyek pemerintah.",
        )

        cash_flow_recovery = high_risk_pool * (recovery_eff / 100.0)
        provision_reversal = 6220.9 * (recovery_eff / 100.0) * 0.85
        adjusted_net_provision = beban_provisi - provision_reversal
        projected_net_income_boost = provision_reversal * 0.78

        s1, s2 = st.columns(2)
        with s1:
            render_kpi_card(
                "Cash Flow Recovery",
                f"+Rp{fmt_id(cash_flow_recovery, 1)} M",
                f"Dari Rp{fmt_id(high_risk_pool)} M piutang >60 hari",
                "pos",
            )
        with s2:
            render_kpi_card(
                "Potensi Reversal Provisi",
                f"Rp{fmt_id(provision_reversal, 1)} M",
                f"Potensi Tambahan Laba Bersih: +Rp{fmt_id(projected_net_income_boost, 1)} M",
                "pos",
            )

        df_sim_chart = pd.DataFrame(
            {
                "Skenario": ["Aktual FY25 (Baseline)", f"Simulasi Recovery ({recovery_eff}%)"],
                "Beban Provisi Neto (Rp Miliar)": [beban_provisi, adjusted_net_provision],
            }
        )
        fig_sim = px.bar(
            df_sim_chart,
            x="Skenario",
            y="Beban Provisi Neto (Rp Miliar)",
            color="Skenario",
            text_auto=".0f",
            color_discrete_map={
                "Aktual FY25 (Baseline)": TELKOM_RED,
                f"Simulasi Recovery ({recovery_eff}%)": GREEN_SAFE,
            },
        )
        fig_sim.update_layout(
            height=235,
            margin=dict(t=15, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#E5E7EB"),
            showlegend=False,
        )
        st.plotly_chart(fig_sim, use_container_width=True)


# ==============================================================================
# TAB 3: SUBSCRIBER CHURN & ARPU TRACKER
# ==============================================================================
with tab3:
    if "B2C" not in selected_segments:
        st.warning(
            "Catatan: Metrik pelanggan seluler & IndiHome bersumber dari segmen **B2C (Telkomsel)**. "
            "Data industri ditampilkan lengkap untuk kebutuhan *benchmarking* kompetitif."
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card(
            "Total Pelanggan Seluler (FY25)",
            "156,1 Juta",
            "▼ Turun dari 159,4 Juta (Akhir FY24)",
            "neg",
        )
    with c2:
        render_kpi_card(
            "Net Churn Pelanggan Seluler",
            "-3,3 Juta",
            "Tekanan Akuisisi & Multi-SIM Consolidation",
            "neg",
        )
    with c3:
        render_kpi_card(
            "Pelanggan IndiHome (FY25)",
            "10,48 Juta",
            "▲ +830 Ribu (+8,6% YoY) | FMC Growth Engine",
            "pos",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_trend, col_arpu = st.columns([1.15, 1])

    with col_trend:
        st.subheader("Tren Pelanggan Seluler & IndiHome per Kuartal (Q1 - Q4 2025)")
        fig_subs = go.Figure()
        fig_subs.add_trace(
            go.Scatter(
                x=df_subs["Kuartal"],
                y=df_subs["Seluler_Juta"],
                name="Pelanggan Seluler (Juta)",
                mode="lines+markers+text",
                text=[f"{v:.1f} Jt" for v in df_subs["Seluler_Juta"]],
                textposition="top center",
                line=dict(color=TELKOM_RED, width=3),
                marker=dict(size=9),
                yaxis="y1",
            )
        )
        fig_subs.add_trace(
            go.Scatter(
                x=df_subs["Kuartal"],
                y=df_subs["IndiHome_Juta"],
                name="Pelanggan IndiHome (Juta)",
                mode="lines+markers+text",
                text=[f"{v:.2f} Jt" for v in df_subs["IndiHome_Juta"]],
                textposition="bottom center",
                line=dict(color=TELKOM_DARK, width=3, dash="dash"),
                marker=dict(size=9, symbol="diamond"),
                yaxis="y2",
            )
        )
        fig_subs.update_layout(
            height=420,
            margin=dict(t=35, b=20, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(
                title="Seluler (Juta Pelanggan)",
                range=[153, 162],
                gridcolor="#E5E7EB",
            ),
            yaxis2=dict(
                title="IndiHome (Juta Pelanggan)",
                overlaying="y",
                side="right",
                range=[9.0, 11.2],
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_subs, use_container_width=True)

    with col_arpu:
        st.subheader("Komparasi ARPU Pasca-Merger XLSmart (Rp Ribu/Bulan)")
        view_mode = st.radio(
            "Mode Visualisasi ARPU:",
            ["Grouped Bar Chart", "Heatmap Matrix"],
            horizontal=True,
        )

        if view_mode == "Grouped Bar Chart":
            fig_arpu = px.bar(
                df_arpu,
                x="Segmen_ARPU",
                y="ARPU_Ribu",
                color="Operator",
                barmode="group",
                text_auto=".1f",
                color_discrete_map={
                    "Telkomsel": TELKOM_RED,
                    "XLSmart (Merged)": "#2563EB",
                    "Indosat (IOH)": "#9CA3AF",
                },
                labels={"Segmen_ARPU": "", "ARPU_Ribu": "ARPU (Rp Ribu)"},
            )
            fig_arpu.update_layout(
                height=380,
                margin=dict(t=20, b=20, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(gridcolor="#E5E7EB"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_arpu, use_container_width=True)
        else:
            df_heat = df_arpu.pivot(
                index="Operator", columns="Segmen_ARPU", values="ARPU_Ribu"
            )
            fig_heat = px.imshow(
                df_heat,
                text_auto=".1f",
                aspect="auto",
                color_continuous_scale=["#F3F4F6", "#FCA5A5", TELKOM_RED],
                labels=dict(x="Segmen ARPU", y="Operator", color="Rp Ribu"),
            )
            fig_heat.update_layout(
                height=380,
                margin=dict(t=20, b=20, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_heat, use_container_width=True)

    st.info(
        "💡 **Competitive Insight (Tab 3):** Entitas hasil merger **XLSmart** mencatat *Blended ARPU* **Rp43,8 ribu**—hanya terpaut tipis **Rp0,7 ribu** dari Telkomsel (**Rp44,5 ribu**). "
        "Penetrasi *Fixed-Mobile Convergence (FMC)* melalui IndiHome menjadi benteng utama untuk menekan *churn* segmen *high-value*."
    )


# ==============================================================================
# TAB 4: SUBSIDIARY & INVESTMENT HEALTH CHECK
# ==============================================================================
with tab4:
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        render_kpi_card(
            "Unrealized Loss Investasi (GoTo/MDI)",
            "-Rp242,0 Miliar",
            "GoTo (-Rp164 M) & MDI Ventures (-Rp78 M)",
            "neg",
        )
    with ic2:
        render_kpi_card(
            "Rugi Bersih Telkomsat (FY25)",
            "-Rp249,5 Miliar",
            "Tekanan Depresiasi Satelit & Utilitas Kapasitas",
            "neg",
        )
    with ic3:
        total_porto = df_inv["Nilai_Portofolio_M"].sum()
        render_kpi_card(
            "Total Portofolio Investasi Digital",
            f"Rp{fmt_id(total_porto)} Miliar",
            "Tersebar di 5 Klaster Strategis",
            "neu",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_donut, col_subsi = st.columns([1, 1.35])

    with col_donut:
        st.subheader("Alokasi Portofolio Investasi Digital (Rp Miliar)")
        fig_donut = px.pie(
            df_inv,
            names="Klaster_Investasi",
            values="Nilai_Portofolio_M",
            hole=0.55,
            color_discrete_sequence=[
                TELKOM_DARK,
                TELKOM_RED,
                GREEN_SAFE,
                "#6B7280",
                "#D97706",
            ],
        )
        fig_donut.update_traces(
            textposition="outside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Nilai: Rp%{value:,.0f} Miliar<br>Porsi: %{percent}<extra></extra>",
        )
        fig_donut.update_layout(
            height=410,
            margin=dict(t=30, b=30, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            annotations=[
                dict(
                    text=f"<b>Rp{fmt_id(total_porto)} M</b><br>Total AUM",
                    x=0.5,
                    y=0.5,
                    font_size=14,
                    showarrow=False,
                )
            ],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_subsi:
        st.subheader("Scorecard Kesehatan Keuangan Entitas Anak")

        filter_status = st.multiselect(
            "Filter Status Kesehatan Entitas:",
            options=df_subsi["Status Kesehatan"].unique().tolist(),
            default=df_subsi["Status Kesehatan"].unique().tolist(),
        )

        focus_entities = st.checkbox(
            "Fokus Entitas Sorotan (Telkomsat, InfraNexia, Mitratel)",
            value=False,
        )

        df_subsi_view = df_subsi[df_subsi["Status Kesehatan"].isin(filter_status)].copy()
        if focus_entities:
            df_subsi_view = df_subsi_view[
                df_subsi_view["Entitas Anak"].isin(["Telkomsat", "InfraNexia", "Mitratel (MTEL)"])
            ]

        st.dataframe(
            df_subsi_view[
                [
                    "Entitas Anak",
                    "Fokus Bisnis",
                    "Pendapatan FY25 (Rp M)",
                    "Laba/Rugi Bersih (Rp M)",
                    "EBITDA Margin (%)",
                    "Debt-to-Equity (x)",
                    "Status Kesehatan",
                ]
            ],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Pendapatan FY25 (Rp M)": st.column_config.NumberColumn(
                    format="Rp %.1f M"
                ),
                "Laba/Rugi Bersih (Rp M)": st.column_config.NumberColumn(
                    format="Rp %.1f M"
                ),
                "EBITDA Margin (%)": st.column_config.ProgressColumn(
                    min_value=0,
                    max_value=100,
                    format="%.1f%%",
                ),
                "Debt-to-Equity (x)": st.column_config.NumberColumn(format="%.2fx"),
            },
        )

        df_plot_sub = df_subsi_view.sort_values("Laba/Rugi Bersih (Rp M)")
        fig_sub_bar = px.bar(
            df_plot_sub,
            x="Laba/Rugi Bersih (Rp M)",
            y="Entitas Anak",
            orientation="h",
            text_auto=".1f",
            color="Laba/Rugi Bersih (Rp M)",
            color_continuous_scale=[TELKOM_RED, "#F59E0B", GREEN_SAFE],
            title="Perbandingan Laba / Rugi Bersih Entitas Anak (Rp Miliar)",
        )
        fig_sub_bar.update_layout(
            height=230,
            margin=dict(t=35, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            yaxis_title="",
        )
        st.plotly_chart(fig_sub_bar, use_container_width=True)

    st.warning(
        "⚠️ **Portfolio Action Plan (Tab 4):** Diperlukan *turnaround plan* segera pada **Telkomsat** (rugi -Rp249,5 Miliar, DER 1,85x) melalui optimalisasi kapasitas satelit Merah Putih 2, "
        "sementara **Mitratel** (EBITDA margin 82,8%) dan **InfraNexia** terus menjadi penopang nilai infrastruktur jangka panjang."
    )