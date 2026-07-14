from pathlib import Path

import pandas as pd


RAW_FILE = Path("European_Bank.csv")
CLEAN_FILE = Path("cleaned_bank.csv")

REQUIRED_COLUMNS = {
    "CustomerId",
    "Surname",
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
}


def validate_data(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    binary_columns = ["HasCrCard", "IsActiveMember", "Exited"]
    for column in binary_columns:
        values = set(df[column].dropna().unique())
        if not values.issubset({0, 1}):
            raise ValueError(f"{column} must contain only 0/1 values. Found: {sorted(values)}")

    geographies = set(df["Geography"].dropna().unique())
    expected_geographies = {"France", "Germany", "Spain"}
    if not geographies.issubset(expected_geographies):
        raise ValueError(f"Unexpected geography values: {sorted(geographies)}")


def add_segments(df: pd.DataFrame) -> pd.DataFrame:
    segmented = df.copy()

    segmented["AgeGroup"] = pd.cut(
        segmented["Age"],
        bins=[0, 29, 45, 60, 150],
        labels=["<30", "30-45", "46-60", "60+"],
        include_lowest=True,
    )

    segmented["CreditScoreBand"] = pd.cut(
        segmented["CreditScore"],
        bins=[0, 579, 739, 900],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    )

    segmented["TenureGroup"] = pd.cut(
        segmented["Tenure"],
        bins=[-1, 2, 6, 10],
        labels=["New", "Mid-term", "Long-term"],
    )

    segmented["BalanceSegment"] = pd.cut(
        segmented["Balance"],
        bins=[-0.01, 0, 100000, float("inf")],
        labels=["Zero-balance", "Low-balance", "High-balance"],
    )

    segmented["ActivityStatus"] = segmented["IsActiveMember"].map({1: "Active", 0: "Inactive"})
    segmented["CardStatus"] = segmented["HasCrCard"].map({1: "Has credit card", 0: "No credit card"})
    segmented["ChurnStatus"] = segmented["Exited"].map({1: "Churned", 0: "Retained"})
    segmented["HighValueCustomer"] = segmented["Balance"] > 100000
    segmented["BalanceAtRisk"] = segmented["Balance"].where(segmented["Exited"].eq(1), 0)

    return segmented


def main() -> None:
    df = pd.read_csv(RAW_FILE)
    validate_data(df)

    analytical = df.drop(columns=["Surname"], errors="ignore")
    analytical = analytical.drop(columns=["Year"], errors="ignore")
    analytical = add_segments(analytical)

    analytical.to_csv(CLEAN_FILE, index=False)
    print(f"Wrote {CLEAN_FILE} with {len(analytical):,} rows and {len(analytical.columns)} columns.")
    print(f"Overall churn rate: {analytical['Exited'].mean():.1%}")


if __name__ == "__main__":
    main()
