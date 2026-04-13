# Tesla vs BYD — Financial Performance Analysis

Συγκριτική ανάλυση οικονομικών δεδομένων **Tesla** και **BYD** με Python,
και οπτικοποίηση αποτελεσμάτων μέσω **Power BI dashboard**.

---

## Τι περιλαμβάνει

| Αρχείο / Φάκελος | Περιγραφή |
|---|---|
| `tesla_vs_byd_analysis.py` | Κύριο Python script — ανάλυση & εξαγωγή δεδομένων |
| `data/Tesla_Financials.csv` | Ετήσια οικονομικά δεδομένα Tesla |
| `data/Byd_Financials.csv` | Ετήσια οικονομικά δεδομένα BYD |
| `output/financial_trend.csv` | Εξαγόμενο CSV → εισάγεται στο Power BI |
| `dashboard/Tesla_vs_BYD.pbix` | Power BI dashboard |

---

## Πώς συνδέονται Python & Power BI

```
Python script
    │
    │  καθαρισμός, υπολογισμός μετρικών
    ▼
output/financial_trend.csv
    │
    │  Get Data → Text/CSV
    ▼
Power BI Dashboard
```

Το Python script επεξεργάζεται τα ακατέργαστα δεδομένα και παράγει το
`financial_trend.csv`. Το Power BI φορτώνει αυτό το αρχείο και χτίζει
πάνω του τα visuals του dashboard.

---

## Μετρικές που αναλύονται

- **Total Revenue** — Συνολικά έσοδα ανά έτος
- **Revenue Growth %** — Ποσοστιαία μεταβολή εσόδων έτος προς έτος
- **Gross Profit Margin %** — Μικτό περιθώριο κέρδους
- **Revenue Difference** — Απόλυτη διαφορά εσόδων Tesla − BYD
- **Revenue % Difference** — Σχετική διαφορά εσόδων

---

## Εγκατάσταση & εκτέλεση

### 1. Κλωνοποίηση repository
```bash
git clone https://github.com/<username>/tesla-vs-byd-analysis.git
cd tesla-vs-byd-analysis
```

### 2. Εγκατάσταση εξαρτήσεων
```bash
pip install pandas plotly
```

### 3. Εκτέλεση
```bash
python tesla_vs_byd_analysis.py
```

Το script:
- Εμφανίζει τα combined metrics στο terminal
- Δημιουργεί το `output/financial_trend.csv`
- Ανοίγει τα interactive Plotly γραφήματα στον browser

### 4. Power BI dashboard
1. Άνοιξε το `dashboard/Tesla_vs_BYD.pbix`
2. **Home → Transform Data → Data Source Settings**
3. Αλλαξε τη διαδρομή ώστε να δείχνει στο τοπικό σου `output/financial_trend.csv`
4. **Refresh**

---

## Σημειώσεις

> **Quarterly data:** Τα τριμηνιαία δεδομένα στο CSV είναι **εκτίμηση**
> (ετήσιο ÷ 4) και όχι πραγματικά quarterly αποτελέσματα.
> Χρησιμοποιούνται για την οπτικοποίηση τάσεων στο Power BI.

---

## Πηγές δεδομένων

- [Tesla Investor Relations](https://ir.tesla.com/)
- [BYD Annual Reports](https://www.bydglobal.com/en/InvestorRelations.html)
- [Macrotrends](https://www.macrotrends.net/)

---

## Τεχνολογίες

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?logo=plotly)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
