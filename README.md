# Tesla vs BYD — Financial Performance Analysis

Συγκριτική ανάλυση οικονομικών δεδομένων **Tesla** και **BYD** με Python,
και οπτικοποίηση αποτελεσμάτων μέσω **Power BI dashboard**.

---

## Τι περιλαμβάνει

| Αρχείο / Φάκελος | Περιγραφή |
|---|---|
| `tesla_vs_byd_analysis.py` | Κύριο Python script — ανάλυση & εξαγωγή δεδομένων |
| `Tesla_vs_BYD_Analysis.ipynb` | Jupyter Notebook — βήμα προς βήμα ανάλυση |
| `data/Tesla_Financials.csv` | Ετήσια οικονομικά δεδομένα Tesla (USD) |
| `data/Byd_Financials.csv` | Ετήσια οικονομικά δεδομένα BYD (CNY) |
| `output/financial_trend.xlsx` | Εξαγόμενο Excel → εισάγεται στο Power BI |
| `dashboard/Tesla_vs_BYD.pbix` | Power BI dashboard |

---

## Πώς συνδέονται Python & Power BI

```
Python script
    │
    │  καθαρισμός, μετατροπή CNY→USD, υπολογισμός μετρικών
    ▼
output/financial_trend.xlsx
    │
    │  Get Data → Excel Workbook
    ▼
Power BI Dashboard
```

Το Python script επεξεργάζεται τα ακατέργαστα δεδομένα, μετατρέπει τα
δεδομένα BYD από CNY σε USD και παράγει το `financial_trend.xlsx`.
Το Power BI φορτώνει αυτό το αρχείο και χτίζει πάνω του τα visuals του dashboard.

---

## Μετρικές που αναλύονται

- **Total Revenue** — Συνολικά έσοδα ανά έτος (B USD)
- **Revenue Growth %** — Ποσοστιαία μεταβολή εσόδων έτος προς έτος
- **Gross Profit Margin %** — Μικτό περιθώριο κέρδους
- **Revenue Difference** — Απόλυτη διαφορά εσόδων Tesla − BYD (B USD)

---

## Συμπεράσματα

- 📈 **Revenue Growth:** Η BYD εμφάνισε σταθερά υψηλότερους ρυθμούς ανάπτυξης εσόδων (avg ~24.8%) έναντι της Tesla (avg ~5.6%), αντανακλώντας την ταχεία επέκτασή της στην κινεζική και παγκόσμια αγορά.

- 💰 **Profit Margin:** Η Tesla διατηρούσε υψηλότερο Gross Profit Margin έως το 2022 (~25.6%), ωστόσο από το 2023 τα περιθώρια των δύο εταιρειών συγκλίνουν (~18%), υποδεικνύοντας αυξημένο ανταγωνισμό και πιέσεις τιμών.

- 💵 **Revenue:** Η BYD ξεπέρασε την Tesla σε συνολικά έσοδα το 2024 (111.66B USD vs 94.83B USD), σηματοδοτώντας μια κομβική αλλαγή στο ανταγωνιστικό τοπίο των ηλεκτρικών οχημάτων.

- ⚡ **Ανταγωνιστικό πλεονέκτημα:** Η Tesla παραμένει πιο κερδοφόρα σε όρους margin, ενώ η BYD υπερέχει σε όγκο εσόδων και ανάπτυξη. Το κλειδί για το μέλλον είναι αν η Tesla μπορεί να ανακτήσει ρυθμούς ανάπτυξης ή αν η BYD θα βελτιώσει την κερδοφορία της.

---

## Εγκατάσταση & εκτέλεση

### 1. Κλωνοποίηση repository
```bash
git clone https://github.com/<username>/tesla-vs-byd-analysis.git
cd tesla-vs-byd-analysis
```

### 2. Εγκατάσταση εξαρτήσεων
```bash
pip install pandas openpyxl
```

### 3. Εκτέλεση Python script
```bash
python tesla_vs_byd_analysis.py
```

Το script:
- Φορτώνει και καθαρίζει τα δεδομένα Tesla & BYD
- Μετατρέπει τα δεδομένα BYD από CNY σε USD
- Υπολογίζει Revenue Growth % και Gross Profit Margin %
- Δημιουργεί το `output/financial_trend.xlsx`

### 4. Εκτέλεση Jupyter Notebook
```bash
pip install jupyter
jupyter notebook Tesla_vs_BYD_Analysis.ipynb
```

### 5. Power BI dashboard
1. Άνοιξε το `dashboard/Tesla_vs_BYD.pbix`
2. **Home → Transform Data → Data Source Settings**
3. Άλλαξε τη διαδρομή ώστε να δείχνει στο τοπικό σου `output/financial_trend.xlsx`
4. **Refresh**

---

## Πηγές δεδομένων

- [Tesla Investor Relations](https://ir.tesla.com/)
- [BYD Annual Reports](https://www.bydglobal.com/en/InvestorRelations.html)
- [Macrotrends](https://www.macrotrends.net/)

---

## Τεχνολογίες

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
