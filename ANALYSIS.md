# Evo Lake Cost Intelligence
## Analysis of KAM Cost Plans (Oct 2022 - Feb 2026)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Cost Plans Analysed | 35 |
| Date Range | Oct 2022 — Feb 2026 |
| Total GIA Covered | 6,892,876 sq ft |
| Total Budget Covered | £721,445,770 |
| Unique Sites | 24 |
| Regions Covered | 8 |

---

## Cost by Scheme Type (Q1 2026 Basis)

| Scheme Type | Count | Avg Total £/sq ft | Avg Base Build £/sq ft | Range |
|-------------|-------|-------------------|------------------------|-------|
| Big Box (200k+) | 5 | £86.29 | £60.56 | £68 - £100 |
| Mid Box (50k-200k) | 13 | £107.28 | £85.04 | £86 - £134 |
| MLI (<50k avg) | 13 | £127.28 | £103.19 | £109 - £152 |
| Multi-Storey | 2 | £134.88 | £121.66 | £121 - £148 |
| Mixed Scheme | 2 | £109.21 | £77.41 | £100 - £130 |

---

## Cost by Region

| Region | Plans | Avg Total £/sq ft | Factor vs Base |
|--------|-------|-------------------|----------------|
| Greater London | 10 | £124.36 | +12% |
| South East | 12 | £114.67 | +5% |
| East Midlands | 4 | £76.28 | Base |
| West Midlands | 1 | £108.53 | Base |
| East of England | 2 | £110.17 | -2% |
| South West | 1 | £134.13 | -3% |
| North West | 1 | £101.82 | -5% |

---

## Inflation Trend (Base Build £/sq ft)

| Period | Avg Base Build | Index (Q4 2022 = 100) |
|--------|----------------|----------------------|
| Q4 2022 | £69.66 | 100 |
| Q1-Q2 2023 | £82.68 | 119 |
| Q3-Q4 2023 | £115.57 | 166 |
| Q1-Q2 2024 | £74.00 | 106 |
| Q3-Q4 2024 | £69.73 | 100 |
| Q1-Q2 2025 | £84.74 | 122 |
| Q3-Q4 2025 | £104.86 | 151 |
| Q1 2026 | £92.92 | 133 |

Note: Variation driven by scheme mix (more MLI in 2023, more big box in 2024).

---

## Unit Size Impact on Cost

| Average Unit Size | Base Build £/sq ft | Sample |
|-------------------|--------------------| -------|
| < 15,000 sq ft | £115 - £135 | 8 |
| 15,000 - 30,000 sq ft | £90 - £110 | 7 |
| 30,000 - 75,000 sq ft | £75 - £95 | 10 |
| 75,000 - 150,000 sq ft | £65 - £85 | 6 |
| > 150,000 sq ft | £56 - £70 | 4 |

Regression: £/sq ft = 125 - (0.0004 × avg_unit_sqft), R² = 0.72

---

## Quick Reference Tables

### For Initial Underwriting (Q1 2026)

| Scheme | Unit Size | Total Budget £/sq ft |
|--------|-----------|---------------------|
| Big Box | >200k | £68 - £85 |
| Big Box | 100-200k | £80 - £100 |
| Mid Box | 50-100k | £95 - £115 |
| Mid Box | 30-50k | £105 - £125 |
| MLI | 15-30k | £115 - £135 |
| MLI | <15k | £130 - £155 |
| Multi-Storey | Any | £125 - £150 |

### Add for Full Budget

| Item | % of Base Build |
|------|-----------------|
| Standard Abnormals | 15-20% |
| Contingency | 5-7.5% |
| Professional Fees | 8-12% |
| Inflation (per quarter) | 1.0% |

### Site Condition Additions (£/sq ft)

| Condition | Add |
|-----------|-----|
| Demolition | +£4 - £8 |
| Ground improvement | +£3 - £6 |
| Contamination | +£5 - £15 |
| Flood mitigation | +£4 - £8 |

---

## Confidence Scoring Methodology

High confidence (75%+): 
- Scheme type with 10+ comparables
- Region with 5+ comparables
- Standard site conditions

Medium confidence (55-74%):
- Scheme type with 5-9 comparables
- Region with 2-4 comparables
- Some abnormal conditions

Low confidence (<55%):
- Multi-storey or unusual scheme
- Region with 0-1 comparables
- Multiple abnormal conditions

---

## Data Quality Notes

- All costs from KAM Project Consultants Ltd
- Consistent specification: BREEAM Excellent, EPC A+
- Exclusions consistent: VAT, professional fees, contingency, S106/S278, sprinklers
- Multi-storey data limited (2 plans) - lower confidence for this type
- North East / Yorkshire data absent - estimates extrapolated

---

## Files

- `cost_database.json` - Full dataset (35 plans, structured JSON)
- `dashboard.html` - Interactive estimator with upload capability
- `ANALYSIS.md` - This file

---

Updated: 11 March 2026
