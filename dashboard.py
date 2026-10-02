import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
 
st.set_page_config(page_title="Churn Risk Dashboard | European Bank", layout="wide", page_icon="📉")
 
BG, PANEL, CARD, BORDER = "#0B111E", "#111827", "#141D2E", "#233046"
TEXT, MUTED = "#E8ECF3", "#8B96AB"
ACCENT, GOOD, BAD, AMBER, PURPLE = "#4F8FE8", "#22C55E", "#F0596A", "#F5A623", "#9B6BCE"
AGE = ["<30", "30-45", "46-60", "60+"]
TIER_COL = {"Low": GOOD, "Medium": AMBER, "High": BAD}
 
st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family:'Inter',sans-serif; }}
#MainMenu, footer, .stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display:none !important; }}
header[data-testid="stHeader"] {{ background:transparent; }}  /* keeps the sidebar toggle usable on mobile */
.stApp {{ background:{BG}; }}
.block-container {{ padding-top:2.2rem; max-width:1250px; }}
section[data-testid="stSidebar"] {{ background:{PANEL} !important; border-right:1px solid {BORDER}; }}
.stMultiSelect [data-baseweb="tag"] {{ background:{ACCENT} !important; border-radius:6px !important; }}
.hdr {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:18px; }}
.hdr .t {{ font-size:23px; font-weight:800; color:{TEXT}; }}
.hdr .s {{ color:{MUTED}; font-size:12.5px; margin-top:3px; }}
.pill {{ background:rgba(34,197,94,.12); border:1px solid rgba(34,197,94,.35); color:{GOOD};
        font-size:11px; font-weight:700; padding:5px 12px; border-radius:20px; }}
.kpi {{ background:{CARD}; border:1px solid {BORDER}; border-radius:12px; padding:14px 16px; margin-bottom:10px; }}
.kpi .lbl {{ color:{MUTED}; font-size:11px; font-weight:600; letter-spacing:.4px; }}
.kpi .val {{ font-size:24px; font-weight:800; color:{TEXT}; margin:6px 0 3px; }}
.kpi .d {{ font-size:11.5px; font-weight:600; }}
.up {{ color:{GOOD}; }} .down {{ color:{BAD}; }} .flat {{ color:{MUTED}; }}
.insight {{ background:{CARD}; border:1px solid {BORDER}; border-left:3px solid {ACCENT}; border-radius:10px;
           padding:12px 14px; font-size:13px; color:{TEXT}; height:100%; }}
.insight b {{ color:{ACCENT}; }}
.sec {{ color:{TEXT}; font-size:15px; font-weight:700; margin:26px 0 10px; padding-left:10px; border-left:3px solid {ACCENT}; }}
.annot {{ color:{MUTED}; font-size:12px; margin:-4px 0 12px; }}
.stTabs [data-baseweb="tab-list"] {{ gap:20px; border-bottom:1px solid {BORDER}; }}
.stTabs [data-baseweb="tab"] {{ color:{MUTED}; font-weight:600; font-size:13.5px; }}
.stTabs [aria-selected="true"] {{ color:{ACCENT} !important; }}
div[data-testid="stDownloadButton"] button {{ background:{ACCENT}; color:#fff; font-weight:700; border:none; border-radius:8px; }}
</style>""", unsafe_allow_html=True)
 
LAY = dict(paper_bgcolor=CARD, plot_bgcolor=CARD, font=dict(color=TEXT, family="Inter", size=12),
           xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER), yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
           legend=dict(bgcolor="rgba(0,0,0,0)"), margin=dict(t=48, l=12, r=12, b=12),
           hoverlabel=dict(bgcolor=PANEL, font_color=TEXT, bordercolor=BORDER), title_font=dict(size=13.5, color=TEXT))
 
 
# ── DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    d = pd.read_csv("cleaned_bank.csv")
    d.columns = d.columns.str.strip()
    if "ChurnRiskScore" in d:
        d["Tier"] = pd.cut(d["ChurnRiskScore"], [-0.01, 0.3, 0.5, 1.01], labels=["Low", "Medium", "High"]).astype(str)
        d["ExpectedLoss"] = d["Balance"] * d["ChurnRiskScore"]
    return d
 
 
@st.cache_data
def load_model_info():
    info = {"metrics": {}, "imp": None}
    try:
        info["metrics"] = dict(joblib.load("model_metrics.pkl"))
    except Exception:
        pass
    try:
        s = pd.Series(joblib.load("feature_importances.pkl")).sort_values().tail(10)
        info["imp"] = s.rename_axis("Feature").reset_index(name="Importance")
    except Exception:
        pass
    return info
 
 
df = load()
MODEL = load_model_info()
AUC = MODEL["metrics"].get("rf_test_auc")
BASE_AUC = MODEL["metrics"].get("baseline_test_auc")
CV_M = MODEL["metrics"].get("rf_cv_auc_mean")
CV_S = MODEL["metrics"].get("rf_cv_auc_std")
HAS_RISK = "ChurnRiskScore" in df.columns
FULL = df["Exited"].mean() * 100
 
 
def kpi(label, value, delta="", kind="flat"):
    arrow = {"up": "▲ ", "down": "▼ ", "flat": ""}[kind]
    st.markdown(f'<div class="kpi"><div class="lbl">{label}</div><div class="val">{value}</div>'
                f'<div class="d {kind}">{arrow}{delta}</div></div>', unsafe_allow_html=True)
 
 
def sec(t, note=None):
    st.markdown(f'<div class="sec">{t}</div>', unsafe_allow_html=True)
    if note:
        st.markdown(f'<p class="annot">{note}</p>', unsafe_allow_html=True)
 
 
def risk_color(v):
    return GOOD if v < FULL * 0.9 else (AMBER if v < FULL * 1.5 else BAD)
 
 
def rate_bar(data, col, title, order=None, height=330):
    g = data.groupby(col)["Exited"].agg(Churn="mean", n="count").reset_index()
    g["Churn"] *= 100
    if order:
        g[col] = pd.Categorical(g[col], order, ordered=True)
        g = g.sort_values(col)
    else:
        g = g.sort_values("Churn", ascending=False)
    fig = go.Figure(go.Bar(x=g[col].astype(str), y=g["Churn"], marker_color=[risk_color(v) for v in g["Churn"]],
                           text=[f"{v:.1f}%" for v in g["Churn"]], textposition="outside", customdata=g["n"], width=0.5,
                           hovertemplate="%{x}<br>Churn: %{y:.1f}%<br>Customers: %{customdata:,}<extra></extra>"))
    fig.add_hline(y=FULL, line_dash="dot", line_color=MUTED, annotation_text=f"Portfolio avg {FULL:.1f}%",
                  annotation_font_color=MUTED)
    fig.update_layout(**LAY, title=title, yaxis_title="Churn %", height=height,
                      yaxis_range=[0, max(g["Churn"].max() * 1.25, FULL * 1.3)])
    return fig
 
 
def gauge(v, title):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=v, number={"suffix": "%", "font": {"size": 30, "color": TEXT}},
        title={"text": title, "font": {"size": 13, "color": MUTED}},
        gauge={"axis": {"range": [0, 60], "tickcolor": MUTED}, "bar": {"color": ACCENT, "thickness": 0.28},
               "bgcolor": CARD, "borderwidth": 0,
               "steps": [{"range": [0, 15], "color": "rgba(34,197,94,.28)"}, {"range": [15, 28], "color": "rgba(245,166,35,.28)"},
                         {"range": [28, 60], "color": "rgba(240,89,106,.28)"}]}))
    fig.update_layout(paper_bgcolor=CARD, font=dict(color=TEXT), margin=dict(t=40, l=16, r=16, b=8), height=230)
    return fig
 
 
# ── HEADER + FILTERS ─────────────────────────────────────────────────────
auc_txt = f"ROC-AUC {AUC:.3f}" if AUC else "Risk model"
st.markdown(f"""<div class="hdr"><div><div class="t">🏦 Churn Risk Dashboard — European Banking</div>
<div class="s">{len(df):,} customer profiles · France · Germany · Spain · Unified Mentor Project</div></div>
<div class="pill">● MODEL LIVE · {auc_txt}</div></div>""", unsafe_allow_html=True)
 
sb = st.sidebar
sb.markdown("**Filter Customers**")
geo = sb.multiselect("Geography", sorted(df["Geography"].unique()), default=sorted(df["Geography"].unique()))
gender = sb.multiselect("Gender", sorted(df["Gender"].unique()), default=sorted(df["Gender"].unique()))
age_g = sb.multiselect("Age group", AGE, default=AGE)
act = sb.multiselect("Activity", [0, 1], default=[0, 1], format_func=lambda x: "Active" if x else "Inactive")
fdf = df[df["Geography"].isin(geo) & df["Gender"].isin(gender) & df["AgeGroup"].isin(age_g) & df["IsActiveMember"].isin(act)]
if fdf.empty:
    st.warning("No customers match this filter combination. Adjust the filters.")
    st.stop()
sb.caption(f"Showing {len(fdf):,} of {len(df):,} customers")
if len(fdf) < 200:
    sb.warning("Small sample — rates can swing a lot.")
 
cr = fdf["Exited"].mean() * 100
diff = cr - FULL
inact = fdf[fdf["IsActiveMember"] == 0]["Exited"].mean() * 100 if (fdf["IsActiveMember"] == 0).any() else float("nan")
act_r = fdf[fdf["IsActiveMember"] == 1]["Exited"].mean() * 100 if (fdf["IsActiveMember"] == 1).any() else float("nan")
lost_bal = fdf.loc[fdf["Exited"] == 1, "Balance"].sum()
 
# ── KPI ROW ──────────────────────────────────────────────────────────────
c1, c2 = st.columns([1.8, 1], gap="medium")
with c1:
    a, b = st.columns(2)
    with a:
        kpi("CUSTOMERS IN VIEW", f"{len(fdf):,}", f"{len(fdf)/len(df):.0%} of portfolio")
        kpi("BALANCE LOST TO CHURN", f"€{lost_bal/1e6:.1f}M", f"{lost_bal/df.loc[df.Exited==1,'Balance'].sum():.0%} of total churned balance", "down")
    with b:
        kpi("CHURN RATE", f"{cr:.1f}%", f"{abs(diff):.1f} pts {'above' if diff > 0 else 'below'} portfolio" if abs(diff) >= 0.05 else "in line with portfolio",
            "down" if diff >= 0.05 else ("up" if diff <= -0.05 else "flat"))
        kpi("INACTIVE vs ACTIVE CHURN", f"{inact:.1f}%" if inact == inact else "—",
            f"{inact/act_r:.1f}× the active rate" if inact == inact and act_r == act_r and act_r > 0 else "needs both groups", "down")
with c2:
    st.plotly_chart(gauge(cr, "Churn Rate (current filter)"), width="stretch", config={"displayModeBar": False})
 
# ── AUTO INSIGHTS ────────────────────────────────────────────────────────
def worst(col, min_n=50):
    g = fdf.groupby(col)["Exited"].agg(r="mean", n="count")
    g = g[g.n >= min_n]
    return (g["r"].idxmax(), g["r"].max() * 100) if len(g) else (None, None)
 
ins = []
for col, label in [("Geography", "country"), ("AgeGroup", "age group")]:
    k, v = worst(col)
    if k is not None:
        ins.append(f"Highest-risk {label}: <b>{k}</b> at <b>{v:.1f}%</b> churn ({v/FULL:.1f}× portfolio).")
ins.append(f"Churned customers took <b>€{lost_bal/1e6:.1f}M</b> in balances with them.")
if HAS_RISK:
    hr = fdf[(fdf.Exited == 0) & (fdf.Tier == "High")]
    ins.append(f"<b>{len(hr):,}</b> still-active customers are model-flagged High risk (<b>€{hr.Balance.sum()/1e6:.1f}M</b> balance) — see Action List.")
cols = st.columns(len(ins))
for c, t in zip(cols, ins):
    c.markdown(f'<div class="insight">{t}</div>', unsafe_allow_html=True)
 
st.write("")
tabs = st.tabs(["Overview", "Geography", "Age & Engagement", "High-Value", "Risk Model", "Action List"])
 
# ── OVERVIEW ─────────────────────────────────────────────────────────────
with tabs[0]:
    sec("Churn Composition")
    a, b = st.columns([1, 1.5])
    with a:
        cc = fdf["Exited"].map({0: "Retained", 1: "Churned"}).value_counts()
        fig = px.pie(values=cc.values, names=cc.index, hole=0.55, color=cc.index, color_discrete_map={"Retained": ACCENT, "Churned": BAD})
        fig.update_traces(textinfo="percent+label", marker=dict(line=dict(color=CARD, width=2)))
        fig.update_layout(**LAY, title="Retained vs Churned", showlegend=False)
        st.plotly_chart(fig, width="stretch")
    with b:
        st.plotly_chart(rate_bar(fdf, "Gender", "Churn Rate by Gender"), width="stretch")
    sec("Credit Score & Products")
    a, b = st.columns(2)
    a.plotly_chart(rate_bar(fdf, "CreditScoreBand", "Churn by Credit Score Band", ["Low", "Medium", "High"]), width="stretch")
    b.plotly_chart(rate_bar(fdf.assign(P=fdf.NumOfProducts.astype(str)), "P", "Churn by Number of Products", ["1", "2", "3", "4"]), width="stretch")
    sec("Balance vs Salary", "Random sample of up to 3,000 customers. Red = churned.")
    s = fdf.sample(min(3000, len(fdf)), random_state=1).assign(Status=lambda x: x.Exited.map({0: "Retained", 1: "Churned"}))
    fig = px.scatter(s, x="Balance", y="EstimatedSalary", color="Status", opacity=0.6,
                     color_discrete_map={"Retained": ACCENT, "Churned": BAD}, hover_data=["Age", "Geography", "NumOfProducts"])
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(**LAY, title="Balance vs Estimated Salary", legend_title="")
    st.plotly_chart(fig, width="stretch")
 
# ── GEOGRAPHY ────────────────────────────────────────────────────────────
with tabs[1]:
    sec("Country Risk Index")
    g = fdf.groupby("Geography").agg(Rate=("Exited", "mean"), n=("Exited", "count"), Churned=("Exited", "sum")).reset_index()
    g["Rate"] *= 100
    g["Bal"] = [fdf[(fdf.Geography == x) & (fdf.Exited == 1)].Balance.sum() / 1e6 for x in g.Geography]
    for col, (_, r) in zip(st.columns(len(g)), g.iterrows()):
        with col:
            kpi(r.Geography.upper(), f"{r.Rate:.1f}%", f"{int(r.Churned):,} of {int(r.n):,} churned · €{r.Bal:.1f}M lost",
                "down" if r.Rate > FULL * 1.2 else ("up" if r.Rate < FULL * 0.9 else "flat"))
    st.plotly_chart(rate_bar(fdf, "Geography", "Churn Rate by Country"), width="stretch")
    sec("Geography × Age Heatmap", "Darker red = higher churn. Cells with fewer than 30 customers are blanked out.")
    p = fdf.pivot_table(values="Exited", index="AgeGroup", columns="Geography", aggfunc="mean").reindex(AGE) * 100
    n = fdf.pivot_table(values="Exited", index="AgeGroup", columns="Geography", aggfunc="count").reindex(AGE)
    p = p.where(n >= 30)
    fig = px.imshow(p, text_auto=".1f", aspect="auto", color_continuous_scale=[[0, PANEL], [0.5, ACCENT], [1, BAD]])
    fig.update_layout(**LAY, title="Churn % by age group and country", coloraxis_colorbar_title="%")
    st.plotly_chart(fig, width="stretch")
 
# ── AGE & ENGAGEMENT ─────────────────────────────────────────────────────
with tabs[2]:
    sec("Age Group")
    st.plotly_chart(rate_bar(fdf, "AgeGroup", "Churn Rate by Age Group", AGE), width="stretch")
    a, b = st.columns(2)
    a.plotly_chart(rate_bar(fdf, "TenureGroup", "Churn by Tenure Group", ["New", "Mid-term", "Long-term"]), width="stretch")
    b.plotly_chart(rate_bar(fdf, "ActivityStatus", "Active vs Inactive Members"), width="stretch")
    sec("Highest-Risk Segments", "Country × age group × activity combinations with at least 50 customers. Lift = segment churn ÷ portfolio churn.")
    seg = fdf.groupby(["Geography", "AgeGroup", "ActivityStatus"]).agg(
        Customers=("Exited", "count"), Churn=("Exited", "mean"), BalanceLost=("Balance", lambda x: x[fdf.loc[x.index, "Exited"] == 1].sum())).reset_index()
    seg = seg[seg.Customers >= 50].assign(Churn=lambda x: x.Churn * 100)
    seg["Lift"] = seg.Churn / FULL
    st.dataframe(seg.sort_values("Churn", ascending=False).head(10), width="stretch", hide_index=True,
                 column_config={"Churn": st.column_config.ProgressColumn("Churn %", format="%.1f", min_value=0, max_value=100),
                                "Lift": st.column_config.NumberColumn(format="%.1f×"),
                                "BalanceLost": st.column_config.NumberColumn("Balance lost", format="€%,.0f")})
 
# ── HIGH VALUE ───────────────────────────────────────────────────────────
with tabs[3]:
    sec("High-Value Customer Explorer")
    thr = st.slider("Balance threshold (€)", 0, 250000, 100000, step=5000)
    hv = fdf[fdf.Balance > thr]
    if hv.empty:
        st.info("No customers above this balance in the current filter.")
    else:
        ch = hv[hv.Exited == 1]
        a, b, c, d = st.columns(4)
        with a: kpi("PREMIUM CUSTOMERS", f"{len(hv):,}", f"above €{thr:,}")
        with b: kpi("THEIR CHURN RATE", f"{hv.Exited.mean()*100:.1f}%", f"vs {cr:.1f}% in view", "down" if hv.Exited.mean()*100 > cr else "up")
        with c: kpi("BALANCE LOST", f"€{ch.Balance.sum()/1e6:.1f}M", "from premium churners", "down")
        with d: kpi("AVG CHURNED BALANCE", f"€{ch.Balance.mean()/1000:.0f}K" if len(ch) else "—", "per churned customer")
        a, b = st.columns(2)
        a.plotly_chart(rate_bar(hv, "Geography", "Premium Churn by Geography"), width="stretch")
        fig = px.histogram(hv, x="Balance", color=hv.Exited.map({0: "Retained", 1: "Churned"}), nbins=25, opacity=0.75,
                           barmode="overlay", color_discrete_map={"Retained": ACCENT, "Churned": BAD})
        fig.update_layout(**LAY, title="Balance Distribution", xaxis_title="Balance (€)", legend_title="", height=330)
        b.plotly_chart(fig, width="stretch")
        sec("Top 50 Premium Customers")
        cols = [c for c in ["CustomerId", "Geography", "Gender", "Age", "Balance", "NumOfProducts", "IsActiveMember", "Exited", "ChurnRiskScore"] if c in hv]
        top = hv.sort_values("Balance", ascending=False).head(50)[cols].rename(columns={"IsActiveMember": "Active", "Exited": "Churned", "ChurnRiskScore": "Risk Score"})
        st.dataframe(top, width="stretch", hide_index=True,
                     column_config={"Balance": st.column_config.NumberColumn(format="€%,.0f"),
                                    "Risk Score": st.column_config.ProgressColumn(format="%.2f", min_value=0, max_value=1)})
        st.download_button("Download premium customers (CSV)", hv.to_csv(index=False).encode(), "premium_customers.csv", "text/csv")
 
# ── RISK MODEL ───────────────────────────────────────────────────────────
with tabs[4]:
    if not HAS_RISK:
        st.warning("Run `python train_model.py` to generate risk scores.")
    else:
        sec("Predictive Churn Risk Model")
        a, b, c, d = st.columns(4)
        with a: kpi("TEST ROC-AUC", f"{AUC:.3f}" if AUC else "—", f"5-fold CV {CV_M:.3f} ± {CV_S:.3f} · +{AUC-BASE_AUC:.3f} vs baseline" if AUC and CV_M and BASE_AUC else "run train_model.py to refresh metrics", "up" if AUC else "flat")
        with b: kpi("HIGH-RISK RETAINED", f"{len(fdf[(fdf.Exited==0)&(fdf.Tier=='High')]):,}", "score above 0.50", "down")
        with c: kpi("AVG RISK SCORE", f"{fdf.ChurnRiskScore.mean():.1%}", "across customers in view")
        with d: kpi("EXPECTED BALANCE LOSS", f"€{fdf[fdf.Exited==0].ExpectedLoss.sum()/1e6:.1f}M", "balance × risk, retained only", "down")
        st.markdown(f'<p class="annot">Scores come from a class-balanced Random Forest, so treat them as a <b>ranking of relative risk</b>, not exact probabilities. '
                    f'Each customer is scored by a model that never saw them (5-fold out-of-fold predictions), so the scores below are not inflated by training data.</p>', unsafe_allow_html=True)
        a, b = st.columns([1, 1.3])
        with a:
            if MODEL["imp"] is not None:
                fig = px.bar(MODEL["imp"], x="Importance", y="Feature", orientation="h", color="Importance",
                             color_continuous_scale=[[0, ACCENT], [0.5, AMBER], [1, BAD]])
                fig.update_layout(**LAY, title="What Drives Churn? (Feature Importance)", coloraxis_showscale=False)
                st.plotly_chart(fig, width="stretch")
            else:
                st.info("feature_importances.pkl could not be loaded — re-run `python train_model.py`.")
        with b:
            fig = px.histogram(fdf, x="ChurnRiskScore", color=fdf.Exited.map({0: "Retained", 1: "Churned"}), nbins=40, opacity=0.75,
                               barmode="overlay", color_discrete_map={"Retained": ACCENT, "Churned": BAD})
            fig.update_layout(**LAY, title="Risk Score Distribution", xaxis_title="Model risk score", legend_title="")
            st.plotly_chart(fig, width="stretch")
        sec("Risk Tiers", "Low < 0.30 · Medium 0.30–0.50 · High > 0.50. Actual churn should rise sharply across tiers if the model is useful.")
        t = fdf.groupby("Tier").agg(Customers=("Exited", "count"), Actual=("Exited", "mean")).reindex(["Low", "Medium", "High"]).dropna().reset_index()
        t["Actual"] *= 100
        fig = go.Figure(go.Bar(x=t.Tier, y=t.Actual, marker_color=[TIER_COL[x] for x in t.Tier], width=0.45, customdata=t.Customers,
                               text=[f"{v:.1f}%" for v in t.Actual], textposition="outside",
                               hovertemplate="%{x} tier<br>Actual churn: %{y:.1f}%<br>Customers: %{customdata:,}<extra></extra>"))
        fig.update_layout(**LAY, title="Actual churn rate by risk tier", yaxis_title="Churn %", height=320, yaxis_range=[0, max(t.Actual.max() * 1.25, 10)])
        st.plotly_chart(fig, width="stretch")
 
# ── ACTION LIST ──────────────────────────────────────────────────────────
with tabs[5]:
    if not HAS_RISK:
        st.warning("Run `python train_model.py` to generate risk scores.")
    else:
        sec("Retention Action List", "Still-active customers ranked by expected balance loss (balance × risk score). This is the call list for relationship managers.")
        cut = st.slider("Minimum risk score", 0.30, 0.90, 0.50, step=0.05)
        al = fdf[(fdf.Exited == 0) & (fdf.ChurnRiskScore >= cut)].sort_values("ExpectedLoss", ascending=False)
        a, b, c = st.columns(3)
        with a: kpi("CUSTOMERS TO CONTACT", f"{len(al):,}", f"risk ≥ {cut:.2f}", "down")
        with b: kpi("BALANCE EXPOSED", f"€{al.Balance.sum()/1e6:.1f}M", "held by these customers")
        with c: kpi("AVG RISK SCORE", f"{al.ChurnRiskScore.mean():.1%}" if len(al) else "—", "in this list")
        if al.empty:
            st.info("No retained customers above this risk score for the current filter.")
        else:
            out = al[["CustomerId", "Geography", "Age", "Balance", "NumOfProducts", "IsActiveMember", "ChurnRiskScore", "ExpectedLoss"]].rename(
                columns={"IsActiveMember": "Active", "ChurnRiskScore": "Risk Score", "ExpectedLoss": "Expected Loss"})
            st.dataframe(out.head(100), width="stretch", hide_index=True,
                         column_config={"Balance": st.column_config.NumberColumn(format="€%,.0f"),
                                        "Expected Loss": st.column_config.NumberColumn(format="€%,.0f"),
                                        "Risk Score": st.column_config.ProgressColumn(format="%.2f", min_value=0, max_value=1)})
            st.caption(f"Showing top 100 of {len(out):,}. The download has the full list.")
            st.download_button("Download full action list (CSV)", out.to_csv(index=False).encode(), "retention_action_list.csv", "text/csv")
        sec("Customer Lookup")
        cid = st.selectbox("Customer ID", fdf.sort_values("ChurnRiskScore", ascending=False).CustomerId.unique())
        r = fdf[fdf.CustomerId == cid].iloc[0]
        peers = df[df.Geography == r.Geography].ChurnRiskScore.mean()
        lvl = r.Tier.upper()
        a, b, c, d = st.columns(4)
        with a: kpi("RISK SCORE", f"{r.ChurnRiskScore:.1%}", f"{lvl} tier", {"HIGH": "down", "MEDIUM": "flat", "LOW": "up"}[lvl])
        with b: kpi("AGE / COUNTRY", f"{int(r.Age)} / {r.Geography}", f"vs {peers:.1%} avg risk in {r.Geography}")
        with c: kpi("BALANCE", f"€{r.Balance:,.0f}", f"{int(r.NumOfProducts)} product(s)")
        with d: kpi("MEMBER STATUS", "Active" if r.IsActiveMember else "Inactive", "engaged" if r.IsActiveMember else "re-engage first", "up" if r.IsActiveMember else "down")
 
st.markdown(f'<div style="margin-top:36px;padding:14px 20px;background:{PANEL};border:1px solid {BORDER};border-radius:10px;'
            f'color:{MUTED};font-size:11.5px;">Customer Segmentation &amp; Churn Pattern Analytics · Python · scikit-learn · Streamlit · Plotly</div>',
            unsafe_allow_html=True)
 
