import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
 
st.set_page_config(page_title="Churn Risk Dashboard | European Bank",
                    layout="wide", page_icon="📉")
 
# ── TOKENS — flat, professional BI-tool palette ─────────────────────────
BG      = "#0B111E"
PANEL   = "#111827"
CARD    = "#141D2E"
BORDER  = "#233046"
TEXT    = "#E8ECF3"
MUTED   = "#8B96AB"
ACCENT  = "#4F8FE8"   # primary blue
SKY     = "#38BDF8"
GOOD    = "#22C55E"
BAD     = "#F0596A"
AMBER   = "#F5A623"
PURPLE  = "#9B6BCE"
TEAL    = "#2FC5A0"
PALETTE = [ACCENT, BAD, AMBER, PURPLE, TEAL, GOOD]
 
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
 
html, body, [class*="css"] {{ font-family:'Inter',sans-serif; }}
#MainMenu, footer {{ visibility:hidden; }}
header[data-testid="stHeader"] {{ display:none !important; }}
.stDeployButton {{ display:none !important; }}
button[kind="header"] {{ display:none !important; }}
[data-testid="stToolbar"] {{ display:none !important; }}
div[data-testid="stDecoration"] {{ display:none; }}
.block-container {{ padding-top:1.6rem; max-width:1200px; overflow-x:hidden; }}
.stApp {{ background:{BG}; overflow-x:hidden; }}
div[data-testid="column"] {{ overflow:visible; }}
 
section[data-testid="stSidebar"] {{ background:{PANEL} !important; border-right:1px solid {BORDER}; }}
section[data-testid="stSidebar"] * {{ color:{TEXT} !important; }}
/* filter pill tags */
.stMultiSelect [data-baseweb="tag"] {{
    background:{ACCENT} !important; border-radius:6px !important;
}}
div[data-baseweb="select"] > div {{ background:{CARD} !important; border-color:{BORDER} !important; }}
 
/* ── header ───────────────────────────────────────────────── */
.hdr {{ display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;
        gap:14px; margin-bottom:26px; padding-top:6px; }}
.hdr .titlewrap {{ display:flex; align-items:center; gap:12px; }}
.hdr .iconbox {{
    width:42px; height:42px; border-radius:11px; background:rgba(79,143,232,0.14);
    display:flex; align-items:center; justify-content:center; font-size:21px; flex-shrink:0;
}}
.hdr .txt {{ display:flex; flex-direction:column; justify-content:center; }}
.hdr .t {{ 
    font-size:22px; font-weight:800; 
    background:linear-gradient(90deg, {TEXT}, {ACCENT});
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; line-height:1.2; margin:0; 
}}
.hdr .s {{ color:{MUTED}; font-size:12.5px; margin-top:3px; }}
.livepill {{
    background:rgba(34,197,94,0.12); border:1px solid rgba(34,197,94,0.35); color:{GOOD};
    font-size:11px; font-weight:700; padding:5px 12px; border-radius:20px; letter-spacing:.4px;
}}
 
/* ── flat KPI card ────────────────────────────────────────── */
.kpi {{
    background:{CARD}; border:1px solid {BORDER}; border-radius:12px;
    padding:16px 18px; height:100%; transition:transform .15s ease, border-color .15s ease;
}}
.kpi:hover {{ transform:translateY(-2px); border-color:rgba(79,143,232,0.4); }}
.kpi .top {{ display:flex; align-items:center; gap:8px; }}
.kpi .icon {{
    width:26px; height:26px; border-radius:7px; display:flex; align-items:center; justify-content:center;
    font-size:13px; background:rgba(79,143,232,0.14); color:{ACCENT}; flex-shrink:0;
}}
.kpi .icon.up {{ background:rgba(34,197,94,0.14); }}
.kpi .icon.down {{ background:rgba(240,89,106,0.14); }}
.kpi .icon.flat {{ background:rgba(79,143,232,0.14); }}
.kpi .lbl {{ color:{MUTED}; font-size:11.5px; font-weight:600; letter-spacing:.2px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.kpi .val {{ font-size:25px; font-weight:800; color:{TEXT}; margin:10px 0 5px; }}
.kpi .delta {{ font-size:11.5px; font-weight:700; display:inline-flex; align-items:center; gap:4px; }}
.kpi .delta.up {{ color:{GOOD}; }}
.kpi .delta.down {{ color:{BAD}; }}
.kpi .delta.flat {{ color:{MUTED}; }}
 
/* ── section labels ───────────────────────────────────────── */
.sec {{ color:{TEXT}; font-size:15px; font-weight:700; margin:30px 0 12px; padding-left:10px;
        border-left:3px solid {ACCENT}; }}
.annot {{ color:{MUTED}; font-size:12px; margin:-8px 0 14px; }}
 
/* ── chart card wrapper ───────────────────────────────────── */
.chartcard {{ background:{CARD}; border:1px solid {BORDER}; border-radius:12px; padding:6px 10px 2px; }}
 
/* ── tabs, flat underline ─────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{ gap:22px; background:transparent; border-bottom:1px solid {BORDER}; }}
.stTabs [data-baseweb="tab"] {{ background:transparent; color:{MUTED}; font-weight:600; font-size:13.5px; padding:8px 2px; }}
.stTabs [aria-selected="true"] {{ color:{ACCENT} !important; border-bottom:2px solid {ACCENT} !important; }}
 
div[data-testid="stDownloadButton"] button {{
    background:{ACCENT}; color:#fff; font-weight:700; border:none; border-radius:8px; padding:9px 22px;
}}
.stDataFrame {{ border:1px solid {BORDER} !important; border-radius:10px; overflow:hidden; }}
.stSlider [data-baseweb="slider"] {{ margin-top:6px; }}
 
.closing {{ margin-top:40px; padding:16px 22px; background:{PANEL}; border:1px solid {BORDER};
    border-radius:10px; display:flex; justify-content:space-between; align-items:center; }}
.closing .h {{ font-size:12.5px; font-weight:700; color:{TEXT}; }}
.closing .m {{ color:{MUTED}; font-size:11px; }}
</style>
""", unsafe_allow_html=True)
 
LAY = dict(
    paper_bgcolor=CARD, plot_bgcolor=CARD,
    font=dict(color=TEXT, family="Inter", size=12),
    xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
    margin=dict(t=44, l=10, r=10, b=10),
    hoverlabel=dict(bgcolor=PANEL, font_color=TEXT, bordercolor=BORDER),
    title_font=dict(size=13.5, color=TEXT),
)
 
@st.cache_data
def load():
    return pd.read_csv("cleaned_bank.csv")
 
df = load()
 
def kpi(icon, label, value, delta_text, delta_kind="flat"):
    arrow = "▲" if delta_kind=="up" else ("▼" if delta_kind=="down" else "•")
    st.markdown(f"""
    <div class="kpi">
        <div class="top"><div class="icon {delta_kind}">{icon}</div><div class="lbl">{label}</div></div>
        <div class="val">{value}</div>
        <div class="delta {delta_kind}">{arrow} {delta_text}</div>
    </div>""", unsafe_allow_html=True)
 
def sec(title):
    st.markdown(f'<div class="sec">{title}</div>', unsafe_allow_html=True)
 
def gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x':[0.05,0.95],'y':[0,1]},
        number={'suffix':"%", 'font':{'size':32,'color':TEXT}},
        title={'text':title, 'font':{'size':13,'color':MUTED}},
        gauge={
            'axis':{'range':[0,50],'tickcolor':MUTED,'tickfont':{'color':MUTED,'size':9}},
            'bar':{'color':ACCENT,'thickness':0.28},
            'bgcolor':CARD,'borderwidth':0,
            'steps':[
                {'range':[0,15],'color':'rgba(34,197,94,0.28)'},
                {'range':[15,28],'color':'rgba(245,166,35,0.28)'},
                {'range':[28,50],'color':'rgba(240,89,106,0.28)'},
            ],
            'threshold':{'line':{'color':TEXT,'width':2},'thickness':0.8,'value':value}
        }
    ))
    fig.update_layout(paper_bgcolor=CARD, font=dict(color=TEXT, family="Inter"),
                       margin=dict(t=40,l=16,r=16,b=10), height=240, autosize=True)
    return fig
 
# ── HEADER ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hdr">
    <div class="titlewrap">
        <div class="iconbox">🏦</div>
        <div class="txt">
            <div class="t">Churn Risk Dashboard — European Banking</div>
            <div class="s">Unified Mentor Project · 10,000 Customer Profiles · France 🇫🇷 · Germany 🇩🇪 · Spain 🇪🇸</div>
        </div>
    </div>
    <div class="livepill">● MODEL LIVE · ROC-AUC 0.867</div>
</div>
""", unsafe_allow_html=True)
 
# ── SIDEBAR ──────────────────────────────────────────────────────────────
st.sidebar.markdown('<p style="font-weight:700;font-size:14px;margin-bottom:12px;">Filter Customers</p>', unsafe_allow_html=True)
geo    = st.sidebar.multiselect("Geography", sorted(df['Geography'].unique()), default=sorted(df['Geography'].unique()))
gender = st.sidebar.multiselect("Gender", sorted(df['Gender'].unique()), default=sorted(df['Gender'].unique()))
age_g  = st.sidebar.multiselect("Age group", ['<30','30-45','46-60','60+'], default=['<30','30-45','46-60','60+'])
act    = st.sidebar.multiselect("Activity", [0,1], default=[0,1], format_func=lambda x:"Active" if x==1 else "Inactive")
 
fdf = df[df['Geography'].isin(geo) & df['Gender'].isin(gender) & df['AgeGroup'].isin(age_g) & df['IsActiveMember'].isin(act)]
if len(fdf)==0:
    st.warning("No customers match this filter combination. Adjust the filters.")
    st.stop()
st.sidebar.markdown(f'<p style="color:{MUTED};font-size:11.5px;margin-top:14px;">Showing {len(fdf):,} of {len(df):,} customers</p>', unsafe_allow_html=True)
 
# ── KPI ROW + GAUGE ──────────────────────────────────────────────────────
cr    = fdf['Exited'].mean()*100
full  = df['Exited'].mean()*100
hv    = fdf[fdf['Balance']>100000]
hvr   = hv['Exited'].mean()*100 if len(hv) else 0
inac  = fdf[fdf['IsActiveMember']==0]
inr   = inac['Exited'].mean()*100 if len(inac) else 0
bar   = fdf[fdf['Exited']==1]['Balance'].sum()
diff  = cr - full
 
c1,c2 = st.columns([1.7,1], gap="medium")
with c1:
    r1,r2 = st.columns(2)
    with r1:
        kpi("👥","TOTAL CUSTOMERS",f"{len(fdf):,}","vs full dataset","flat")
        kpi("💶","BALANCE AT RISK",f"€{bar/1e6:.1f}M","from churned accounts","down")
    with r2:
        kpi("📊","OVERALL CHURN",f"{cr:.1f}%",f"{abs(diff):.1f} pts {'above' if diff>0 else 'below'} baseline","down" if diff>0 else "up")
        kpi("⚠️","INACTIVE CHURN",f"{inr:.1f}%","vs active members","down")
with c2:
    st.markdown('<div class="chartcard">', unsafe_allow_html=True)
    st.plotly_chart(gauge(cr,"Churn Rate"), use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)
 
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
t1,t2,t3,t4,t5 = st.tabs(["Overview","Geography","Age & Engagement","High-Value","Predictive Risk"])
 
# ── TAB 1 ────────────────────────────────────────────────────────────────
with t1:
    sec("Churn Composition")
    c1,c2 = st.columns([1,1.5])
    with c1:
        cc = fdf['Exited'].map({0:'Retained',1:'Churned'}).value_counts()
        fig=px.pie(values=cc.values,names=cc.index,hole=0.55,color=cc.index,
                   color_discrete_map={'Retained':ACCENT,'Churned':BAD})
        fig.update_traces(textinfo='percent+label',textfont=dict(color=TEXT,size=12),
                          marker=dict(line=dict(color=CARD,width=2)))
        fig.update_layout(**LAY,title="Retained vs Churned")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        gc=fdf.groupby('Gender')['Exited'].mean().reset_index(); gc['Exited']*=100
        fig2=px.bar(gc,x='Gender',y='Exited',text_auto='.1f',color='Gender',
                    color_discrete_map={'Female':BAD,'Male':ACCENT})
        fig2.update_traces(textfont=dict(color=TEXT,size=12),textposition='outside',marker_line_width=0,width=0.45)
        fig2.update_layout(**LAY,title="Churn Rate by Gender (%)",showlegend=False,yaxis_title="Churn %",yaxis_range=[0,33])
        st.plotly_chart(fig2,use_container_width=True)
 
    sec("Credit Score & Product Analysis")
    c1,c2=st.columns(2)
    with c1:
        cs=fdf.groupby('CreditScoreBand')['Exited'].mean().reindex(['Low','Medium','High']).reset_index(); cs['Exited']*=100
        fig3=px.bar(cs,x='CreditScoreBand',y='Exited',text_auto='.1f',color_discrete_sequence=[ACCENT])
        fig3.update_traces(textfont=dict(color=TEXT),marker_line_width=0,width=0.45)
        fig3.update_layout(**LAY,title="Churn by Credit Score (%)",yaxis_title="Churn %")
        st.plotly_chart(fig3,use_container_width=True)
    with c2:
        pr=fdf.groupby('NumOfProducts')['Exited'].mean().reset_index(); pr['Exited']*=100
        colors=[GOOD if v<20 else (AMBER if v<50 else BAD) for v in pr['Exited']]
        fig4=px.bar(pr,x='NumOfProducts',y='Exited',text_auto='.1f')
        fig4.update_traces(marker_color=colors,textfont=dict(color=TEXT),marker_line_width=0,width=0.4)
        fig4.update_layout(**LAY,title="Churn by Number of Products (%)",xaxis_title="Products",yaxis_title="Churn %")
        st.plotly_chart(fig4,use_container_width=True)
 
    sec("Balance vs Salary")
    st.markdown('<p class="annot">Sample of 3,000 customers — red markers are churned accounts.</p>', unsafe_allow_html=True)
    samp=fdf.sample(min(3000,len(fdf)),random_state=1).copy()
    samp['Status']=samp['Exited'].map({0:'Retained',1:'Churned'})
    fig5=px.scatter(samp,x='Balance',y='EstimatedSalary',color='Status',opacity=0.65,
                    color_discrete_map={'Retained':ACCENT,'Churned':BAD},
                    hover_data=['Age','Geography','NumOfProducts'])
    fig5.update_traces(marker=dict(size=5))
    fig5.update_layout(**LAY,title="Balance vs Estimated Salary")
    st.plotly_chart(fig5,use_container_width=True)
 
# ── TAB 2 ────────────────────────────────────────────────────────────────
with t2:
    sec("Geographic Risk Index")
    gc2=fdf.groupby('Geography').agg(ChurnRate=('Exited','mean'),Count=('Exited','count'),Churned=('Exited','sum')).reset_index()
    gc2['ChurnRate']*=100
    gc2['BalRisk']=[fdf[(fdf['Geography']==g)&(fdf['Exited']==1)]['Balance'].sum()/1e6 for g in gc2['Geography']]
    c1,c2,c3=st.columns(3)
    icons=["🇫🇷","🇩🇪","🇪🇸"]
    for i,row in gc2.iterrows():
        dk = "down" if row['ChurnRate']>25 else ("flat" if row['ChurnRate']>18 else "up")
        with [c1,c2,c3][i]:
            icon = icons[i] if i < len(icons) else "🌍"
            kpi(icon, row['Geography'].upper(), f"{row['ChurnRate']:.1f}%", f"{int(row['Churned']):,} churned · €{row['BalRisk']:.1f}M at risk", dk)
 
    sec("Churn Rate by Country")
    fig6=px.bar(gc2.sort_values('ChurnRate',ascending=False),x='Geography',y='ChurnRate',text_auto='.1f',
                color='Geography',color_discrete_map={'Germany':BAD,'France':ACCENT,'Spain':PURPLE})
    fig6.update_traces(textfont=dict(color=TEXT,size=13),marker_line_width=0,width=0.45)
    fig6.update_layout(**LAY,showlegend=False,yaxis_title="Churn %",yaxis_range=[0,42])
    st.plotly_chart(fig6,use_container_width=True)
 
    sec("Geography × Age Group Heatmap")
    pivot=fdf.pivot_table(values='Exited',index='AgeGroup',columns='Geography',aggfunc='mean').reindex(['<30','30-45','46-60','60+'])*100
    fig7=px.imshow(pivot,text_auto='.1f',aspect='auto',color_continuous_scale=[[0,PANEL],[0.5,ACCENT],[1,BAD]])
    fig7.update_layout(**LAY,title="Churn % — darker = higher risk")
    st.plotly_chart(fig7,use_container_width=True)
 
# ── TAB 3 ────────────────────────────────────────────────────────────────
with t3:
    sec("Age Group Analysis")
    ac=fdf.groupby('AgeGroup')['Exited'].mean().reindex(['<30','30-45','46-60','60+']).reset_index(); ac['Exited']*=100
    colors2=[GOOD if v<20 else (AMBER if v<35 else BAD) for v in ac['Exited']]
    fig8=px.bar(ac,x='AgeGroup',y='Exited',text_auto='.1f')
    fig8.update_traces(marker_color=colors2,textfont=dict(color=TEXT,size=13),marker_line_width=0,width=0.45)
    fig8.update_layout(**LAY,yaxis_title="Churn %",title="Age 46–60 is highest risk — 51.1% churn rate")
    st.plotly_chart(fig8,use_container_width=True)
 
    c1,c2=st.columns(2)
    with c1:
        tc=fdf.groupby('TenureGroup')['Exited'].mean().reindex(['New','Mid-term','Long-term']).reset_index(); tc['Exited']*=100
        fig9=px.bar(tc,x='TenureGroup',y='Exited',text_auto='.1f',color_discrete_sequence=[PURPLE])
        fig9.update_traces(textfont=dict(color=TEXT),marker_line_width=0,width=0.45)
        fig9.update_layout(**LAY,title="Churn by Tenure Group (%)",yaxis_title="Churn %")
        st.plotly_chart(fig9,use_container_width=True)
    with c2:
        ac2=fdf.groupby('IsActiveMember')['Exited'].mean().reset_index()
        ac2['IsActiveMember']=ac2['IsActiveMember'].map({0:'Inactive',1:'Active'}); ac2['Exited']*=100
        fig10=px.bar(ac2,x='IsActiveMember',y='Exited',text_auto='.1f',color='IsActiveMember',
                     color_discrete_map={'Active':ACCENT,'Inactive':BAD})
        fig10.update_traces(textfont=dict(color=TEXT),marker_line_width=0,width=0.45)
        fig10.update_layout(**LAY,showlegend=False,title="Inactive members churn ~2x more",yaxis_title="Churn %",yaxis_range=[0,33])
        st.plotly_chart(fig10,use_container_width=True)
 
# ── TAB 4 ────────────────────────────────────────────────────────────────
with t4:
    sec("High-Value Customer Explorer")
    thr=st.slider("Balance Threshold (€)",0,250000,100000,step=5000)
    hv2=fdf[fdf['Balance']>thr]
    c1,c2,c3,c4=st.columns(4)
    with c1: kpi("💎","PREMIUM CUSTOMERS", f"{len(hv2):,}", f"above €{thr:,}", "flat")
    with c2: kpi("📉","THEIR CHURN RATE", f"{hv2['Exited'].mean()*100:.1f}%" if len(hv2) else "—", f"vs {cr:.1f}% overall", "down")
    with c3: kpi("💶","BALANCE AT RISK", f"€{hv2[hv2['Exited']==1]['Balance'].sum()/1e6:.1f}M", "from premium churners", "down")
    with c4: kpi("📊","AVG CHURNED BAL", f"€{hv2[hv2['Exited']==1]['Balance'].mean()/1000:.0f}K" if len(hv2[hv2['Exited']==1]) else "—", "per churned customer", "flat")
 
    c1,c2=st.columns(2)
    with c1:
        hg=hv2.groupby('Geography')['Exited'].mean().reset_index(); hg['Exited']*=100
        fig11=px.bar(hg,x='Geography',y='Exited',text_auto='.1f',color='Geography',
                     color_discrete_map={'Germany':BAD,'France':ACCENT,'Spain':PURPLE})
        fig11.update_traces(textfont=dict(color=TEXT),marker_line_width=0,width=0.45)
        fig11.update_layout(**LAY,showlegend=False,title="Premium Churn by Geography",yaxis_title="Churn %")
        st.plotly_chart(fig11,use_container_width=True)
    with c2:
        fig12=px.histogram(hv2,x='Balance',color=hv2['Exited'].map({0:'Retained',1:'Churned'}),
                           nbins=25,opacity=0.75,barmode='overlay',color_discrete_map={'Retained':ACCENT,'Churned':BAD})
        fig12.update_layout(**LAY,title="Balance Distribution: Churned vs Retained",xaxis_title="Balance (€)",legend_title="")
        st.plotly_chart(fig12,use_container_width=True)
 
    sec("Top 50 Premium Customers")
    scols=['CustomerId','Geography','Gender','Age','Balance','EstimatedSalary','NumOfProducts','IsActiveMember','Exited']
    if 'ChurnRiskScore' in hv2.columns: scols.append('ChurnRiskScore')
    st.dataframe(hv2.sort_values('Balance',ascending=False).head(50)[scols]
                   .rename(columns={'IsActiveMember':'Active','Exited':'Churned','ChurnRiskScore':'Risk Score'}),
                 use_container_width=True)
    st.download_button("Download Filtered Data (CSV)", fdf.to_csv(index=False).encode(), "filtered_customers.csv","text/csv")
 
# ── TAB 5 ────────────────────────────────────────────────────────────────
with t5:
    sec("Predictive Churn Risk Model")
    st.markdown(f'<p class="annot">Random Forest trained on 10,000 profiles · <b style="color:{ACCENT}">ROC-AUC: 0.867</b> · predicts churn probability per customer so the bank can intervene before they leave.</p>', unsafe_allow_html=True)
 
    if 'ChurnRiskScore' in fdf.columns:
        hr=fdf[(fdf['Exited']==0)&(fdf['ChurnRiskScore']>0.5)]
        c1,c2,c3=st.columns(3)
        with c1: kpi("🚨","HIGH RISK RETAINED", f"{len(hr):,}", "score > 50% — act now", "down")
        with c2: kpi("📈","AVG RISK SCORE", f"{fdf['ChurnRiskScore'].mean():.1%}", "across all customers", "flat")
        with c3: kpi("🎯","MODEL ROC-AUC", "0.867", "87% discrimination power", "up")
 
        sec("What Drives Churn?")
        c1,c2=st.columns([1,1.3])
        with c1:
            imp=pd.DataFrame({'Feature':['Age','Num Products','Balance','Germany','Active Member','Credit Score','Salary','Tenure','Gender Male'],
                               'Importance':[0.365,0.249,0.101,0.065,0.063,0.048,0.048,0.025,0.023]}).sort_values('Importance')
            fig13=px.bar(imp,x='Importance',y='Feature',orientation='h',
                         color='Importance',color_continuous_scale=[[0,ACCENT],[0.5,AMBER],[1,BAD]])
            fig13.update_layout(**LAY,title="Feature Importance (ML Model)",coloraxis_showscale=False)
            st.plotly_chart(fig13,use_container_width=True)
        with c2:
            fig14=px.histogram(fdf,x='ChurnRiskScore',color=fdf['Exited'].map({0:'Retained',1:'Churned'}),
                               nbins=40,opacity=0.75,barmode='overlay',color_discrete_map={'Retained':ACCENT,'Churned':BAD})
            fig14.update_layout(**LAY,title="Risk Score Distribution",xaxis_title="Predicted Churn Probability",legend_title="")
            st.plotly_chart(fig14,use_container_width=True)
 
        sec("Top 25 At-Risk Customers")
        st.markdown(f'<p class="annot">Currently retained, but the model flags them as highest risk — target immediately for retention campaigns.</p>', unsafe_allow_html=True)
        ar=fdf[fdf['Exited']==0].sort_values('ChurnRiskScore',ascending=False).head(25)
        st.dataframe(ar[['CustomerId','Geography','Age','Balance','NumOfProducts','IsActiveMember','ChurnRiskScore']]
                       .rename(columns={'IsActiveMember':'Active','ChurnRiskScore':'Risk Score'})
                       .style.format({'Risk Score':'{:.1%}','Balance':'€{:,.0f}'}),
                     use_container_width=True)
 
        sec("Individual Customer Lookup")
        cid=st.selectbox("Select Customer ID",fdf['CustomerId'].unique())
        row=fdf[fdf['CustomerId']==cid].iloc[0]
        risk=row['ChurnRiskScore']
        rl="HIGH" if risk>0.5 else ("MEDIUM" if risk>0.3 else "LOW")
        rk = "down" if risk>0.5 else ("flat" if risk>0.3 else "up")
        c1,c2,c3,c4=st.columns(4)
        with c1: kpi("🎯","CHURN RISK SCORE", f"{risk:.1%}", rl, rk)
        with c2: kpi("🌍","AGE / COUNTRY", f"{int(row['Age'])} / {row['Geography']}", "", "flat")
        with c3: kpi("💶","BALANCE", f"€{row['Balance']:,.0f}", f"{int(row['NumOfProducts'])} product(s)", "flat")
        with c4: kpi("👤","STATUS", "Active" if row['IsActiveMember']==1 else "Inactive", "member", "up" if row['IsActiveMember']==1 else "down")
    else:
        st.warning("Run `python train_model.py` to generate risk scores.")
 
# ── CLOSING ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="closing">
    <div class="h">Customer Segmentation &amp; Churn Pattern Analytics — European Banking</div>
    <div class="m">Unified Mentor Project · Python · scikit-learn · Streamlit · Plotly · 10,000 Customer Profiles</div>
</div>
""", unsafe_allow_html=True)
 