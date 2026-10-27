# Day 5 Cleaning Decisions (synthetic demonstration)

- **Dataset:** Synthetic practice rows, NOT trainer-provided data.
- **Duplicates:** Drop exact duplicate employee records to avoid double counting.
- **Names and categories:** Trim whitespace; standardize case; preserve IT capitalization.
- **Salary, rating and experience:** Convert text to numbers; impute missing with column median.
- **Department, city, gender, contract type:** Fill blanks with most frequent nonblank category.
- **Start date:** Parse to datetime; replace missing/invalid date with middle observed date, and store `start_date_was_missing` flag. A real study should confirm dates with source.
- **Outliers:** Use 1.5 × IQR salary thresholds; mark outliers but retain them for review.
- **Salary bounds:** 9000.00–111000.00 INR.
- **Missing/duplicates before:** 7/2; **after:** 0/0.
