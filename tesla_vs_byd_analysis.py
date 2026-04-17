import os
import pandas as pd

# ─── FX Rate ───────────────────────────────────────────
CNY_TO_USD = 1 / 7.2  # adjust if needed

# ─── Paths ─────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TESLA_CSV   = os.path.join(DATA_DIR, "Tesla_Financials.csv")
BYD_CSV     = os.path.join(DATA_DIR, "Byd_Financials.csv")
OUTPUT_XLSX = os.path.join(OUTPUT_DIR, "financial_trend.xlsx")

REQUIRED_COLS = ["Total Revenue", "Gross Profit"]


# ─── Load & Clean ──────────────────────────────────────
def load_financials(filepath: str, company: str, currency: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{company} file not found: {filepath}")

    df = pd.read_csv(filepath, sep=";", engine="python")

    # reshape
    df = df.set_index("Breakdown").T
    df.index.name = "Year"

    # remove TTM
    df = df[~df.index.astype(str).str.contains("TTM", na=False)]

    # extract year
    df.index = df.index.astype(str).str.extract(r"(\d{4})")[0]

    # clean numeric columns
    for col in REQUIRED_COLS:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    # ─── Convert currency FIRST ─────────────────────────
    if currency == "CNY":
        df[REQUIRED_COLS] = df[REQUIRED_COLS] * CNY_TO_USD

    # ─── Thousands → actual values ─────────────────────
    df[REQUIRED_COLS] = df[REQUIRED_COLS] * 1000

    # ─── Convert to BILLIONS USD ───────────────────────
    df[REQUIRED_COLS] = df[REQUIRED_COLS] / 1e9

    # ─── SORT (CRITICAL for correct growth) ────────────
    df = df.sort_index()

    return df


# ─── Metrics ───────────────────────────────────────────
def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Revenue Growth %"] = df["Total Revenue"].pct_change() * 100
    df["Profit Margin %"]  = (df["Gross Profit"] / df["Total Revenue"]) * 100

    return df


# ─── Combine ───────────────────────────────────────────
def build_combined(tesla: pd.DataFrame, byd: pd.DataFrame) -> pd.DataFrame:
    combined = pd.DataFrame({
        "Tesla Revenue (B USD)": tesla["Total Revenue"],
        "Tesla Growth %": tesla["Revenue Growth %"],
        "Tesla Margin %": tesla["Profit Margin %"],

        "BYD Revenue (B USD)": byd["Total Revenue"],
        "BYD Growth %": byd["Revenue Growth %"],
        "BYD Margin %": byd["Profit Margin %"],
    })

    combined["Revenue Difference (B USD)"] = (
        combined["Tesla Revenue (B USD)"] - combined["BYD Revenue (B USD)"]
    )

    return combined


# ─── Export ────────────────────────────────────────────
def export_to_powerbi(df: pd.DataFrame, path: str):
    df.index.name = "Year"
    df = df.reset_index()

    df.to_excel(path, index=False)

    print(f"\n✅ Excel dataset exported → {path}")
    print(df.head())


# ─── MAIN ──────────────────────────────────────────────
def main():
    print("📊 Tesla vs BYD Clean Financial Pipeline")

    tesla = load_financials(TESLA_CSV, "Tesla", currency="USD")
    byd   = load_financials(BYD_CSV, "BYD", currency="CNY")

    tesla = compute_metrics(tesla)
    byd   = compute_metrics(byd)

    combined = build_combined(tesla, byd)

    print("\n📈 Combined dataset:")
    print(combined)

    export_to_powerbi(combined, OUTPUT_XLSX)


if __name__ == "__main__":
    main()
