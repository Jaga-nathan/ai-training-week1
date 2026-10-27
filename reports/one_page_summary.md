# Weekly Employee / Customer Analysis — One-Page Summary

**Dataset:** 20 cleaned employee records; generated practice data, not a real company's records.

## Problem and Data
Explore staff salary, departmental differences, employee locations and hiring dates after correcting missing values, duplicates and inconsistent formats. Department budgets are joined for context, but no expenditure claims are made.

## Three Key Findings
1. **Overall mean salary:** INR 67,850.00; **median:** INR 59,000.00.
2. **Highest departmental mean:** IT at INR 90,250.00.
3. **Most represented city:** Chennai with 10 employees. There are 1 salary outlier(s) flagged.

## Two Recommendations
1. Validate flagged salary amounts and missing original start dates with a trusted data source.
2. Monitor salary by department and location monthly using a repeatable data-quality pipeline.

## Limitations
Synthetic, small sample; imputed fields and one outlier can affect conclusions. Correlations do not imply causation. This analysis cannot represent an actual company without real data.

## Charts
See `reports/figures/` and `reports/chart_insights.md` for five labeled figures and one-sentence insights.
