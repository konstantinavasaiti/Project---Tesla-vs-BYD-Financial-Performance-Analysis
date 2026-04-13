"""
Tesla vs BYD Financial Performance Analysis
============================================
Συγκριτική ανάλυση οικονομικών δεδομένων Tesla & BYD.
Παράγει CSV αρχείο (financial_trend.csv) για χρήση στο Power BI dashboard.

Δομή αρχείων:
    data/
        Tesla_Financials.csv
        Byd_Financials.csv
    output/
        financial_trend.csv   ← εισάγεται στο Power BI
    tesla_vs_byd_analysis.py
"""

import os
import pandas as pd
import plotly.graph_objects as go

# ─── Διαδρομές αρχείων ───────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data")
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TESLA_CSV   = os.path.join(DATA_DIR, "Tesla_Financials.csv")
BYD_CSV     = os.path.join(DATA_DIR, "Byd_Financials.csv")
OUTPUT_CSV  = os.path.join(OUTPUT_DIR, "financial_trend.csv")

REQUIRED_COLS = ["Total Revenue", "Gross Profit"]


# ─── Φόρτωση & καθαρισμός ────────────────────────────────────────────────────
def load_financials(filepath: str, company_name: str) -> pd.DataFrame:
    """
    Φορτώνει CSV οικονομικών δεδομένων και επιστρέφει
    DataFrame με έτος ως index και αριθμητικές στήλες.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"[{company_name}] Δεν βρέθηκε το αρχείο: {filepath}\n"
            f"Βεβαιώσου ότι υπάρχει ο φάκελος 'data/' με τα σωστά CSV."
        )

    df = pd.read_csv(filepath, sep=";", engine="python")
    df = df.set_index("Breakdown").T
    df.index.name = "Year"

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            f"[{company_name}] Λείπουν στήλες: {missing}\n"
            f"Διαθέσιμες: {list(df.columns)}"
        )

    for col in REQUIRED_COLS:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    return df


# ─── Υπολογισμός μετρικών ────────────────────────────────────────────────────
def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Υπολογίζει Revenue Growth % και Gross Profit Margin %."""
    df = df.copy()
    df["Revenue Growth %"] = df["Total Revenue"].pct_change() * 100
    df["Profit Margin %"]  = (df["Gross Profit"] / df["Total Revenue"]) * 100
    return df


def build_combined(tesla: pd.DataFrame, byd: pd.DataFrame) -> pd.DataFrame:
    """Συνδυάζει τα δεδομένα των δύο εταιρειών σε ένα DataFrame."""
    combined = pd.DataFrame({
        "Tesla Revenue":           tesla["Total Revenue"],
        "Tesla Revenue Growth %":  tesla["Revenue Growth %"],
        "Tesla Profit Margin %":   tesla["Profit Margin %"],
        "BYD Revenue":             byd["Total Revenue"],
        "BYD Revenue Growth %":    byd["Revenue Growth %"],
        "BYD Profit Margin %":     byd["Profit Margin %"],
    })

    combined["Revenue Difference"]       = combined["Tesla Revenue"] - combined["BYD Revenue"]
    combined["Profit Margin Difference"] = combined["Tesla Profit Margin %"] - combined["BYD Profit Margin %"]
    combined["Revenue % Difference"]     = (combined["Tesla Revenue"] / combined["BYD Revenue"] - 1) * 100

    return combined


# ─── Εξαγωγή quarterly CSV (για Power BI) ────────────────────────────────────
def export_quarterly_csv(combined: pd.DataFrame, output_path: str) -> None:
    """
    Παράγει quarterly mockup CSV για εισαγωγή στο Power BI.

    ΣΗΜΕΙΩΣΗ: Τα quarterly δεδομένα είναι εκτίμηση (ετήσιο ÷ 4).
    Αν διαθέτεις πραγματικά τριμηνιαία δεδομένα, αντικατέστησε αυτή
    τη συνάρτηση με άμεση φόρτωσή τους.
    """
    datetime_index = pd.to_datetime(combined.index, errors="coerce")
    quarters       = ["Q1", "Q2", "Q3", "Q4"]
    rows           = []

    for year in sorted(datetime_index.year.dropna().unique().astype(int)):
        mask = datetime_index.year == year
        row  = combined.loc[mask].iloc[0]

        for q in quarters:
            for company, rev_col, margin_col in [
                ("Tesla", "Tesla Revenue", "Tesla Profit Margin %"),
                ("BYD",   "BYD Revenue",   "BYD Profit Margin %"),
            ]:
                rows.append({
                    "Company":      company,
                    "Year":         year,
                    "Quarter":      q,
                    "YearQuarter":  f"{year} {q}",
                    "Revenue":      row[rev_col] / 4,
                    "ProfitMargin": row[margin_col],
                })

    df_quarterly = pd.DataFrame(rows)
    df_quarterly[["YearQuarter", "Company", "Revenue", "ProfitMargin"]].to_csv(
        output_path, index=False
    )
    print(f"\n✅ Quarterly CSV εξήχθη → {output_path}")
    print("   (Εισάγαγέ το στο Power BI: Get Data → Text/CSV)")


# ─── Visualizations (Plotly) ─────────────────────────────────────────────────
def plot_revenue_growth(combined: pd.DataFrame) -> None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=combined.index, y=combined["Tesla Revenue Growth %"],
        mode="lines+markers", name="Tesla",
        line=dict(color="#E31937", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=combined.index, y=combined["BYD Revenue Growth %"],
        mode="lines+markers", name="BYD",
        line=dict(color="#1F6FEB", width=2),
    ))
    fig.update_layout(
        title="Revenue Growth %: Tesla vs BYD",
        xaxis_title="Year",
        yaxis_title="Revenue Growth (%)",
        template="plotly_white",
        legend=dict(orientation="h", y=1.12),
    )
    fig.show()


def plot_profit_margin(combined: pd.DataFrame) -> None:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=combined.index, y=combined["Tesla Profit Margin %"],
        mode="lines+markers", name="Tesla",
        line=dict(color="#E31937", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=combined.index, y=combined["BYD Profit Margin %"],
        mode="lines+markers", name="BYD",
        line=dict(color="#1F6FEB", width=2),
    ))
    fig.update_layout(
        title="Gross Profit Margin %: Tesla vs BYD",
        xaxis_title="Year",
        yaxis_title="Profit Margin (%)",
        template="plotly_white",
        legend=dict(orientation="h", y=1.12),
    )
    fig.show()


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("📊 Tesla vs BYD Financial Analysis\n" + "=" * 38)

    # Φόρτωση
    tesla = load_financials(TESLA_CSV, "Tesla")
    byd   = load_financials(BYD_CSV,   "BYD")

    # Μετρικές
    tesla    = compute_metrics(tesla)
    byd      = compute_metrics(byd)
    combined = build_combined(tesla, byd)

    print("\nCombined Metrics:")
    print(combined.to_string())

    # Εξαγωγή CSV για Power BI
    export_quarterly_csv(combined, OUTPUT_CSV)

    # Γραφήματα
    plot_revenue_growth(combined)
    plot_profit_margin(combined)


if __name__ == "__main__":
    main()