<div align="center">

# 🏦 European Bank Churn Intelligence Dashboard

### Segmentation-driven churn analytics for a 10,000-customer European retail bank

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Random%20Forest-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**🔗 [Live Demo](https://iqra-churn-analytics.streamlit.app)**

*Unified Mentor Internship Project · Customer Segmentation & Churn Pattern Analytics in European Banking*

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Results](#-key-results)
- [Dashboard Preview](#-dashboard-preview)
- [Dashboard Features](#-dashboard-features)
- [Model Validation](#-model-validation-approach)
- [Business Recommendations](#-business-recommendations)
- [Project Files](#-project-files)
- [Run Locally](#-run-locally)
- [Tech Stack](#-tech-stack)
- [Deploy & Publish](#-deploy--publish)

---

## 🎯 Overview

Customer churn is one of the largest hidden costs in retail banking — every lost customer means lost lifetime value and higher acquisition pressure to replace them. Most banks track a single churn number, but that hides *where* the risk actually concentrates.

This project answers three questions for a European retail bank's 10,000 customers:

1. **Which customer segments are most likely to churn** — by geography, age, engagement, and balance?
2. **Where is the financial exposure concentrated** — and how much revenue is genuinely at risk?
3. **Can churn be predicted before it happens** — with a model rigorous enough to act on?

The result is an interactive dashboard plus a validated machine learning risk model, backed by a full research paper and an executive summary for stakeholders.

---

## 📊 Key Results

| Metric | Value |
|---|---|
| **Overall Churn Rate** | 20.4% |
| **Germany Churn Rate** | 🔴 32.4% — highest-risk country |
| **Age 46–60 Churn Rate** | 🔴 51.1% — highest-risk age group |
| **Inactive Member Churn** | 26.9% vs. 14.3% active |
| **Total Balance at Risk** | €185.6M |
| **Random Forest Test ROC-AUC** | **0.867** |
| **Logistic Regression Baseline** | 0.777 |
| **5-fold CV ROC-AUC (Random Forest)** | 0.860 ± 0.011 |

> The model isn't reported in isolation — it's benchmarked against a linear baseline and validated with 5-fold stratified cross-validation, so the performance figure is a stable estimate, not one lucky train/test split.

---

## 🖼️ Dashboard Preview

*Add a screenshot or short GIF of the dashboard here — this is the single highest-impact addition you can make. Drag an image into this spot in GitHub's editor, or reference it like:*

```markdown
![Dashboard Screenshot](https://raw.githubusercontent.com/iqra-insights/european-bank-churn-analytics/main/dashboard_preview.png)
```

---

## 🧭 Dashboard Features

| Tab | What it shows |
|---|---|
| 📊 **Overview** | Churn distribution, gender, credit score, products, scatter |
| 🌍 **Geography** | Country risk index, churn bars, Geography × Age heatmap |
| 👥 **Age & Engagement** | Age group bars, tenure, active vs. inactive |
| 💎 **High-Value Explorer** | Premium customer churn, balance risk, CSV export |
| 🤖 **Predictive Risk** | Live feature importance, baseline comparison, risk scores, top at-risk customers, customer lookup |

All tabs respond live to sidebar filters — **Geography, Gender, Age group, Activity status** — with dynamic KPI cards and drill-down tables.

---

## 🔬 Model Validation Approach

- **Baseline:** Logistic Regression (scaled features) → Test ROC-AUC **0.777**
- **Main model:** Random Forest (200 trees, max depth 8, balanced class weights) → Test ROC-AUC **0.867**
- **Validation:** 5-fold stratified cross-validation on the training set for both models
- **Result:** Random Forest improves on the linear baseline by **+0.090 ROC-AUC points**, justifying the added model complexity instead of just picking the fancier algorithm by default

---

## 💡 Business Recommendations

1. **Launch a dedicated retention program for Germany** — churn nearly double France/Spain
2. **Build an age-specific strategy for the 46–60 group** — the single highest-risk segment
3. **Use inactivity as an early warning signal** — inactive customers churn ~2× more than active ones
4. **Assign relationship managers to high-balance customers** — €185.6M in exposure
5. **Investigate 3–4 product customers for possible over-selling** — disproportionately high churn

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `dashboard.py` | Interactive Streamlit dashboard — **run this file** |
| `cleaned_bank.csv` | Cleaned, segmented dataset with ML risk scores |
| `European_Bank.csv` | Original raw dataset |
| `churn_analysis.ipynb` | Full EDA + ML analysis notebook |
| `prepare_churn_data.py` | Data validation and segmentation pipeline |
| `train_model.py` | Trains Random Forest + Logistic Regression baseline, runs 5-fold CV |
| `feature_importances.pkl` | Saved feature importances (dashboard reads these live) |
| `model_metrics.pkl` | Saved CV/baseline/test metrics (dashboard reads these live) |
| `research_paper.md` | Full research paper — EDA, findings, recommendations |
| `executive_summary.md` | Condensed summary for stakeholders |
| `requirements.txt` | Python dependencies |

---

## ⚙️ Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) rebuild the cleaned dataset and retrain the model
python prepare_churn_data.py
python train_model.py

# 3. Launch the dashboard
streamlit run dashboard.py
```

Open the Local URL shown in the terminal — usually `http://localhost:8501`.

> ⚠️ **Common mistake:** typing `streamlit dashboard.py` (missing `run`) throws `Error: No such command`. Always include `run`.

---

## 🛠️ Tech Stack

`Python` · `Pandas` · `scikit-learn` · `Streamlit` · `Plotly` · `Random Forest` · `Jupyter`

---

## 🚀 Deploy & Publish

**Push to GitHub:**
```bash
git init
git add .
git commit -m "European Bank Churn Intelligence Dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bank-churn-intelligence-dashboard.git
git push -u origin main
```

**Deploy the live demo (Streamlit Community Cloud — free):**
1. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub → **Create app**
2. Repo: your repo · Branch: `main` · File: `dashboard.py`
3. Click **Deploy**

Once live, paste the URL into the badge at the top of this README.

---

<div align="center">

**Built as part of the Unified Mentor Data Analytics Internship**

⭐ If you found this useful, consider starring the repo!

</div>
