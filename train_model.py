"""
Train and validate a churn prediction model.
 
Improvements over v1:
- Baseline comparison (Logistic Regression) so the Random Forest result is
  justified against a simpler model, not just reported in isolation.
- 5-fold stratified cross-validation instead of a single train/test split,
  so the reported ROC-AUC is a stable estimate rather than one lucky split.
- Feature importances are saved to disk so the dashboard reads them live
  instead of hardcoding numbers in the UI code.
"""
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report
 
RANDOM_STATE = 42
 
print("Loading data...")
df = pd.read_csv("cleaned_bank.csv")
 
features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance',
            'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
X = pd.get_dummies(df[features], columns=['Geography', 'Gender'], drop_first=True)
y = df['Exited']
 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
 
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
 
# ── Baseline: Logistic Regression ───────────────────────────────────────
print("\nTraining baseline (Logistic Regression)...")
baseline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE)),
])
baseline_cv_scores = cross_val_score(baseline, X_train, y_train, cv=cv, scoring="roc_auc")
baseline.fit(X_train, y_train)
baseline_test_auc = roc_auc_score(y_test, baseline.predict_proba(X_test)[:, 1])
 
print(f"Logistic Regression — 5-fold CV ROC-AUC: {baseline_cv_scores.mean():.4f} "
      f"(+/- {baseline_cv_scores.std():.4f}) | Test ROC-AUC: {baseline_test_auc:.4f}")
 
# ── Main model: Random Forest ───────────────────────────────────────────
print("\nTraining Random Forest...")
model = RandomForestClassifier(n_estimators=200, max_depth=8,
                                min_samples_leaf=5, random_state=RANDOM_STATE,
                                class_weight='balanced')
rf_cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")
model.fit(X_train, y_train)
 
probs = model.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, probs)
 
print(f"Random Forest      — 5-fold CV ROC-AUC: {rf_cv_scores.mean():.4f} "
      f"(+/- {rf_cv_scores.std():.4f}) | Test ROC-AUC: {test_auc:.4f}")
 
print(f"\nImprovement over baseline: {test_auc - baseline_test_auc:+.4f} ROC-AUC points")
 
print("\nClassification report (Random Forest, test set):")
print(classification_report(y_test, model.predict(X_test)))
 
# ── Feature importances (saved for the dashboard, not hardcoded) ───────
importances = (
    pd.Series(model.feature_importances_, index=X.columns)
    .sort_values(ascending=False)
)
print("\nTop feature importances:")
print(importances.head(10))
 
# ── Score the full dataset for the dashboard ────────────────────────────
X_full = pd.get_dummies(df[features], columns=['Geography', 'Gender'], drop_first=True)
X_full = X_full.reindex(columns=X.columns, fill_value=0)
df['ChurnRiskScore'] = model.predict_proba(X_full)[:, 1]
df.to_csv("cleaned_bank.csv", index=False)
 
joblib.dump(model, "churn_model.pkl")
joblib.dump(list(X.columns), "model_columns.pkl")
joblib.dump(importances, "feature_importances.pkl")
 
# Save a small metrics summary the dashboard can display honestly
metrics = {
    "rf_cv_auc_mean": float(rf_cv_scores.mean()),
    "rf_cv_auc_std": float(rf_cv_scores.std()),
    "rf_test_auc": float(test_auc),
    "baseline_cv_auc_mean": float(baseline_cv_scores.mean()),
    "baseline_test_auc": float(baseline_test_auc),
}
joblib.dump(metrics, "model_metrics.pkl")
 
print("\nDone! ChurnRiskScore, feature_importances.pkl, and model_metrics.pkl saved.")
 