# Customer Segmentation and Churn Pattern Analytics in European Banking

## Abstract

This project analyzes 10,000 European banking customer records to identify churn patterns across geography, age, tenure, credit profile, balance, engagement, and customer value. The analysis shows an overall churn rate of 20.4%, with materially higher churn among German customers, customers aged 46-60, inactive customers, and high-balance customers. These findings support targeted retention strategies instead of broad, generic churn campaigns.

## Business Context

Customer churn is a major hidden cost in retail banking because it reduces lifetime value, increases acquisition pressure, and destabilizes revenue. Traditional churn reporting often stops at a single churn rate, but banking leaders need segment-level insight to understand where churn is concentrated and which customers carry the highest balance exposure.

## Objectives

- Measure the overall churn rate.
- Identify churn distribution across customer segments.
- Compare churn behavior across France, Germany, and Spain.
- Analyze churn among high-value customers.
- Evaluate engagement and tenure patterns.
- Support strategic planning and marketing decisions.

## Dataset

The source dataset contains customer-level records from a European bank. Key fields include customer ID, credit score, geography, gender, age, tenure, balance, number of products, credit card ownership, active membership status, estimated salary, and the churn target `Exited`.

Non-analytical fields such as `Surname` were removed from the prepared dataset. Binary fields were validated to ensure that `HasCrCard`, `IsActiveMember`, and `Exited` contain only 0/1 values.

## Segmentation Design

The prepared dataset creates the following analytical segments:

- Geographic segmentation: France, Germany, Spain.
- Age segmentation: `<30`, `30-45`, `46-60`, `60+`.
- Credit score bands: Low, Medium, High.
- Tenure groups: New, Mid-term, Long-term.
- Balance segments: Zero-balance, Low-balance, High-balance.
- Engagement status: Active, Inactive.
- High-value customer flag: balance above EUR 100,000.

## Key Findings

Overall churn is 20.4%, representing 2,037 churned customers out of 10,000.

Germany has the highest geographic churn rate at 32.4%, compared with Spain at 16.7% and France at 16.2%. Germany also carries the largest balance exposure among churned customers, with approximately EUR 98.0M in balance at risk.

The 46-60 age band is the highest-risk demographic segment, with a churn rate of 51.1%. Customers below 30 show the lowest churn rate at 7.6%.

Inactive customers churn at 26.9%, while active customers churn at 14.3%. This creates an engagement drop indicator of 12.6 percentage points.

High-balance customers have a churn rate of 25.2%, above the portfolio average of 20.4%. Churned high-balance customers represent approximately EUR 159.5M in balance at risk.

Churned customers are older on average than retained customers. Churned customers have an average age of 44.8 compared with 37.4 among retained customers.

## KPI Summary

| KPI | Result |
| --- | ---: |
| Overall churn rate | 20.4% |
| Churned customers | 2,037 |
| Highest geographic churn | Germany, 32.4% |
| Highest age churn | 46-60, 51.1% |
| High-value churn ratio | 25.2% |
| Inactive churn rate | 26.9% |
| Active churn rate | 14.3% |
| Engagement drop indicator | 12.6 percentage points |
| Total balance at risk | EUR 185.6M |

## Recommendations

Prioritize Germany for regional churn intervention. The bank should investigate service quality, product fit, pricing, and competitor pressure in Germany because churn is nearly double the rate observed in France and Spain.

Create a dedicated high-value retention program. High-balance customers represent disproportionate financial exposure, so they should be routed to relationship managers, priority service channels, and tailored retention offers.

Launch inactivity-based early warning campaigns. Since inactive customers churn much more frequently, the bank should use inactivity as a trigger for reactivation campaigns, product education, and targeted communication.

Design age-aware retention strategies. Customers aged 46-60 require deeper investigation because this group has the highest churn rate. Product bundles, advisory support, and service experience should be reviewed for this segment.

Use segment dashboards for continuous monitoring. The Streamlit dashboard should be used to filter customer segments, monitor KPIs, and export customer-level drill-downs for action planning.

## Deliverables

- `prepare_churn_data.py`: reproducible data validation and segmentation pipeline.
- `cleaned_bank.csv`: cleaned analytical dataset with segmentation fields.
- `churn_dashboard.py`: Streamlit dashboard for live analytics.
- `executive_summary.md`: concise summary for government and senior stakeholders.
