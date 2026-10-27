"""WEEK 1 / DAY 5: Cleaning, EDA, five charts, report, notebook, Streamlit bonus.
Run: python day5.py

IMPORTANT: Day 5 assignment does not provide a dataset. This script creates and
clearly labels a SMALL SYNTHETIC PRACTICE DATASET; it is NOT the trainer's data.
If your trainer gives you a real dataset, replace the practice source and revisit
column-specific cleaning decisions and business interpretations.
"""
from pathlib import Path
from io import StringIO
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
for folder in (DATA, REPORTS, FIGURES):
    folder.mkdir(exist_ok=True, parents=True)

# EXTRA DEMONSTRATION ROWS ARE SYNTHETIC (NO DAY 5 DATASET WAS SUPPLIED).
# Three deliberately messy values, two missing amounts, and two duplicate rows
# make it possible to practice the exact cleaning questions in the assignment.
RAW_CSV = """id,name,department,salary,city,gender,contract_type,start_date,performance_score,experience_years
1, Arun ,Sales,30000, Chennai ,Male,Full-Time,2020-01-10,3.8,3
2,Priya,HR,45000,Chennai,Female,Full-Time,2020-03-02,4.2,5
3,Rahul, IT ,60000,Bangalore,Male,Full-Time,2019-07-11,4.6,7
4,Divya,IT,"₹75,000",Chennai,Female,Full-Time,2021-02-15,4.8,6
5,Karthik,Finance,90000,Mumbai,Male,Full-Time,2017-04-24,4.5,9
6,Meena,Sales,52000,Bangalore,Female,Contract,2022-01-12,4.0,4
7,Suresh,IT,68000,Chennai,Male,Full-Time,2018-09-17,4.3,8
8,Anitha,HR,48000,Mumbai,Female,Contract,2020-10-03,4.1,5
9,Vijay,IT,,Chennai,Male,Full-Time,2023-07-09,3.9,2
10,Latha,Sales,42000,Bangalore,Female,Contract,2023-05-20,3.5,3
11,Ganesh,Finance,82000,Chennai,Male,Full-Time,2017-10-21,4.6,9
12,Rekha,IT,72000,Mumbai,Female,Full-Time,2019-11-30,4.4,7
13,Naveen,HR,38000,Chennai,Male,Contract,2024-02-01,3.6,2
14,Swathi,Marketing,missing,Mumbai,Female,Contract,2022-08-16,4.2,4
15,Manoj,IT,80000,Bangalore,Male,Full-Time,2018-06-22,4.7,8
16,Deepa,Sales,34000,,Female,Contract,2024-08-12,3.8,2
17,Farah,Marketing,65000,Mumbai,Female,Full-Time,not-a-date,4.3,6
18,Bala,IT,250000,Chennai,Male,Full-Time,2015-02-10,4.9,12
19,Ritu,Finance,50000,Chennai,,Full-Time,2022-11-13,,4
20,Joseph,,58000,Bangalore,Male,,2021-12-08,4.1,
"""
BUDGETS_CSV = """department,annual_budget_inr
Sales,4800000
HR,3200000
IT,9000000
Finance,5600000
Marketing,4000000
"""
PALETTE = ["#235789", "#2A9D8F", "#F29E4C", "#8E6CBE", "#DD6B6B"]


def heading(text):
    print("\n" + "=" * 78 + "\n" + text + "\n" + "=" * 78)


def create_demo_data():
    raw_path = DATA / "weekly_project_raw.csv"
    budget_path = DATA / "department_budgets.csv"
    if not raw_path.exists():
        raw = pd.read_csv(StringIO(RAW_CSV))
        raw = pd.concat([raw, raw.iloc[[3, 6]]], ignore_index=True)
        raw.to_csv(raw_path, index=False)
        print("Created synthetic data/weekly_project_raw.csv (22 rows; 2 duplicates).")
    else:
        print("Using existing data/weekly_project_raw.csv")
    if not budget_path.exists():
        budget_path.write_text(BUDGETS_CSV, encoding="utf-8")
    return pd.read_csv(raw_path), pd.read_csv(budget_path)


def normalize_department(x):
    if pd.isna(x):
        return np.nan
    name = str(x).strip().lower()
    return {"it": "IT", "hr": "HR"}.get(name, name.title())


def clean(raw):
    heading("DAY 5 / FIRST HALF / TASK 1: Data Cleaning")
    before = {"rows": len(raw),
              "missing_cells": int(raw.isna().sum().sum()),
              "exact_duplicate_rows": int(raw.duplicated().sum())}
    df = raw.drop_duplicates().copy()
    df["id"] = pd.to_numeric(df["id"], errors="raise").astype(int)
    df["name"] = df["name"].astype("string").str.strip().str.title()
    df["department"] = df["department"].map(normalize_department)
    for col in ("city", "gender", "contract_type"):
        df[col] = df[col].astype("string").str.strip().str.title()
    # Convert amounts stored as strings, including '₹75,000' and 'missing'.
    cleaned_money = df["salary"].astype("string").str.replace(r"[^0-9.-]", "", regex=True)
    df["salary"] = pd.to_numeric(cleaned_money, errors="coerce")
    for col in ("performance_score", "experience_years"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    # Record imputation flags BEFORE filling, so decisions are auditable.
    df["salary_was_missing"] = df["salary"].isna()
    df["start_date_was_missing"] = df["start_date"].isna()
    for col in ("salary", "performance_score", "experience_years"):
        df[col] = df[col].fillna(df[col].median())
    for col in ("department", "city", "gender", "contract_type"):
        mode = df[col].mode(dropna=True)
        if mode.empty:
            raise ValueError(f"Can't impute {col}: no observed values")
        df[col] = df[col].fillna(mode.iloc[0])
    # Practice-only date imputation. Preserve a flag for traceability.
    valid_dates = df["start_date"].dropna().sort_values()
    if valid_dates.empty:
        raise ValueError("No valid start dates for practice date imputation")
    representative_date = valid_dates.iloc[len(valid_dates) // 2]
    df["start_date"] = df["start_date"].fillna(representative_date)

    # Identify IQR outliers; RETAIN them because we can't verify they are errors.
    q1, q3 = df["salary"].quantile([.25, .75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    df["salary_iqr_outlier"] = ~df["salary"].between(lower, upper)
    df = df.sort_values("id").reset_index(drop=True)

    after = {"rows": len(df),
             "missing_cells": int(df.isna().sum().sum()),
             "exact_duplicate_rows": int(df.duplicated().sum())}
    summary = pd.DataFrame([before, after], index=["Before", "After"])
    summary.to_csv(REPORTS / "before_after_cleaning.csv")
    df.to_csv(DATA / "clean_data.csv", index=False, date_format="%Y-%m-%d")
    print("Before/after cleaning:\n", summary.to_string())
    print(f"Salary IQR boundaries: {lower:.2f} to {upper:.2f} INR")
    print("Flagged outlier IDs:", df.loc[df.salary_iqr_outlier, "id"].tolist())
    print("\nCleaning decisions:")
    print("- Exact duplicates: remove so the same person isn't double-counted.")
    print("- salary, performance_score, experience_years: convert to numeric, fill with median.")
    print("- department, city, gender, contract_type: standardize case/spaces, fill with mode.")
    print("- start_date: parse as date, fill missing/invalid with representative observed date, flag it.")
    print("- salary outliers: flag with IQR rule, keep pending validation.")
    (REPORTS / "cleaning_decisions.md").write_text(
        "# Day 5 Cleaning Decisions (synthetic demonstration)\n\n"
        "- **Dataset:** Synthetic practice rows, NOT trainer-provided data.\n"
        "- **Duplicates:** Drop exact duplicate employee records to avoid double counting.\n"
        "- **Names and categories:** Trim whitespace; standardize case; preserve IT capitalization.\n"
        "- **Salary, rating and experience:** Convert text to numbers; impute missing with column median.\n"
        "- **Department, city, gender, contract type:** Fill blanks with most frequent nonblank category.\n"
        "- **Start date:** Parse to datetime; replace missing/invalid date with middle observed date, "
        "and store `start_date_was_missing` flag. A real study should confirm dates with source.\n"
        "- **Outliers:** Use 1.5 × IQR salary thresholds; mark outliers but retain them for review.\n"
        f"- **Salary bounds:** {lower:.2f}–{upper:.2f} INR.\n"
        f"- **Missing/duplicates before:** {before['missing_cells']}/{before['exact_duplicate_rows']}; "
        f"**after:** {after['missing_cells']}/{after['exact_duplicate_rows']}.\n",
        encoding="utf-8"
    )
    return df, summary


def analysis(df, budgets):
    heading("DAY 5 / FIRST HALF / TASK 2: Exploratory Analysis")
    numeric_cols = ["salary", "performance_score", "experience_years"]
    stats = df[numeric_cols].agg(["mean", "median", "min", "max", "std"]).T
    print("Summary statistics:\n", stats.round(2).to_string())
    stats.to_csv(REPORTS / "summary_statistics.csv")

    dept = df.groupby("department").agg(employee_count=("id", "count"),
                                         average_salary=("salary", "mean"),
                                         total_salary=("salary", "sum")).sort_index()
    city = df.groupby("city").agg(employee_count=("id", "count"),
                                  average_salary=("salary", "mean")).sort_index()
    print("\nBy department:\n", dept.round(2).to_string())
    print("\nBy city:\n", city.round(2).to_string())
    dept.to_csv(REPORTS / "by_department.csv")
    city.to_csv(REPORTS / "by_city.csv")

    correlation = df[numeric_cols].corr(numeric_only=True)
    pairs = []
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i + 1:]:
            pairs.append((col1, col2, float(correlation.loc[col1, col2])))
    pairs.sort(key=lambda item: abs(item[2]), reverse=True)
    print("\nTop 3 numeric relationships by ABSOLUTE correlation (descriptive only):")
    for col1, col2, value in pairs[:3]:
        print(f"  {col1} vs {col2}: r={value:.3f}")
    correlation.to_csv(REPORTS / "correlations.csv")

    merged = pd.merge(df, budgets, on="department", how="left", validate="many_to_one", indicator=True)
    print("\nMerged budget statuses:\n", merged["_merge"].value_counts().to_string())
    merged.drop(columns="_merge").to_csv(DATA / "employee_budget_merged.csv", index=False)
    print("Merged employee / budget rows:", len(merged))

    # Explicitly answer all five business questions with computed values.
    top_dept = dept["average_salary"].idxmax()
    top_city = city["employee_count"].idxmax()
    employment = df.groupby("contract_type")["salary"].mean().sort_index()
    qa = [
        ("Q1. How many distinct employees are there?", str(df["id"].nunique())),
        ("Q2. What is the overall average salary?", f"INR {df['salary'].mean():,.2f}"),
        ("Q3. Which department has the highest average salary?",
         f"{top_dept} – INR {dept.loc[top_dept, 'average_salary']:,.2f}"),
        ("Q4. Which city has the largest number of employees?",
         f"{top_city} – {int(city.loc[top_city, 'employee_count'])} employees"),
        ("Q5. What is the average salary for each contract type?",
         "; ".join(f"{key}: INR {value:,.2f}" for key, value in employment.items())),
    ]
    print("\nFive business questions answered:")
    for question, answer in qa:
        print(question, "\n ", answer)
    (REPORTS / "business_questions.md").write_text(
        "# Five Business Questions – Day 5\n\n"
        "**Note:** Answers use synthetic practice data.\n\n" +
        "\n\n".join(f"**{q}**\n\n{a}" for q, a in qa) + "\n", encoding="utf-8"
    )

    heading("DAY 5 / FIRST HALF / BONUS: Pivot Table")
    pivot = pd.pivot_table(df, index="department", columns="city", values="salary",
                           aggfunc="mean", fill_value=0)
    print("Mean salary by department and city (0 means no matching employees):\n", pivot.round(2).to_string())
    pivot.to_csv(REPORTS / "pivot_department_city.csv")
    return dept, city, qa, pairs, pivot


def save_chart(fig, filename):
    path = FIGURES / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("Saved:", path.relative_to(ROOT))
    return filename


def charts(df, dept, city):
    heading("DAY 5 / SECOND HALF / TASK 1: Five Visualisations")
    insights = []
    avg = dept["average_salary"].sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(avg.index, avg.values, color=PALETTE[:len(avg)])
    ax.bar_label(bars, labels=[f"₹{value:,.0f}" for value in avg.values], padding=3)
    ax.set_ylim(0, avg.max() * 1.20)
    ax.set(title="Mean Salary by Department", xlabel="Department", ylabel="Salary (INR)")
    name = save_chart(fig, "01_average_salary_by_department.png")
    insights.append((name, f"Highest mean salary is in {avg.index[0]} (INR {avg.iloc[0]:,.0f})."))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(df["salary"], bins=8, color=PALETTE[0], edgecolor="white")
    ax.set(title="Salary Distribution", xlabel="Salary (INR)", ylabel="Number of Employees")
    name = save_chart(fig, "02_salary_histogram.png")
    insights.append((name, f"Median salary is INR {df.salary.median():,.0f}; flagged IQR outliers: {df.salary_iqr_outlier.sum()}."))

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, (department, group) in enumerate(df.groupby("department")):
        ax.scatter(group["experience_years"], group["salary"], label=department,
                   color=PALETTE[i % len(PALETTE)], s=65, alpha=.9)
    ax.set(title="Experience and Salary by Department", xlabel="Experience (years)", ylabel="Salary (INR)")
    ax.legend(title="Department")
    name = save_chart(fig, "03_experience_vs_salary.png")
    insights.append((name, "Experience and salary are compared by department; the high salary outlier needs review."))

    hires_by_year = df["start_date"].dt.year.value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(hires_by_year.index, hires_by_year.values, color=PALETTE[1], marker="o", label="Hires")
    ax.set(title="Employees by Recorded Start Year", xlabel="Start year", ylabel="Employees (count)")
    ax.legend()
    ax.grid(alpha=.2)
    name = save_chart(fig, "04_start_year_trend.png")
    insights.append((name, f"The largest recorded hiring cohort is {int(hires_by_year.idxmax())} with {int(hires_by_year.max())} employees; one date was imputed."))

    fig, ax = plt.subplots(figsize=(9, 5))
    groups = [group["salary"].to_numpy() for _, group in df.groupby("department")]
    names = [str(name) for name, _ in df.groupby("department")]
    ax.boxplot(groups, tick_labels=names, patch_artist=False)
    ax.set(title="Salary Spread by Department", xlabel="Department", ylabel="Salary (INR)")
    name = save_chart(fig, "05_salary_boxplot.png")
    insights.append((name, "Salary varies across departments; unusually high values should be validated before removal."))

    report_lines = ["# Five Charts and Their Insights", "", "*Synthetic demonstration data.*", ""]
    for index, (name, insight) in enumerate(insights, 1):
        report_lines.extend([f"## Chart {index}", f"![Chart {index}](figures/{name})", "", f"**Insight:** {insight}", ""])
    (REPORTS / "chart_insights.md").write_text("\n".join(report_lines), encoding="utf-8")
    return insights


def write_report(df, dept, city, insights, qa):
    heading("DAY 5 / SECOND HALF / TASK 2: Summary Report + Presentation")
    report = f"""# Weekly Employee / Customer Analysis — One-Page Summary

**Dataset:** {len(df)} cleaned employee records; generated practice data, not a real company's records.

## Problem and Data
Explore staff salary, departmental differences, employee locations and hiring dates after correcting missing values, duplicates and inconsistent formats. Department budgets are joined for context, but no expenditure claims are made.

## Three Key Findings
1. **Overall mean salary:** INR {df.salary.mean():,.2f}; **median:** INR {df.salary.median():,.2f}.
2. **Highest departmental mean:** {dept.average_salary.idxmax()} at INR {dept.average_salary.max():,.2f}.
3. **Most represented city:** {city.employee_count.idxmax()} with {int(city.employee_count.max())} employees. There are {int(df.salary_iqr_outlier.sum())} salary outlier(s) flagged.

## Two Recommendations
1. Validate flagged salary amounts and missing original start dates with a trusted data source.
2. Monitor salary by department and location monthly using a repeatable data-quality pipeline.

## Limitations
Synthetic, small sample; imputed fields and one outlier can affect conclusions. Correlations do not imply causation. This analysis cannot represent an actual company without real data.

## Charts
See `reports/figures/` and `reports/chart_insights.md` for five labeled figures and one-sentence insights.
"""
    (REPORTS / "one_page_summary.md").write_text(report, encoding="utf-8")
    notes = f"""# Five-Minute Presentation Notes (Practice Data)

**00:00–00:45 — Question and scope.** How do cleaned employee data reveal salary patterns? All records are synthetic examples.

**00:45–01:30 — Cleaning.** Show before/after counts (`reports/before_after_cleaning.csv`), median/mode filling, date imputation flag, duplicate removal and IQR review.

**01:30–02:30 — Chart 1: Mean salary by department.** {insights[0][1]}

**02:30–03:30 — Chart 2: Salary distribution.** {insights[1][1]}

**03:30–04:15 — Chart 3: Experience versus salary.** {insights[2][1]}

**04:15–05:00 — Recommendations.** Verify outliers and source dates. Automate quality checks and publish a monthly department/city dashboard.

**Prepare:** Open the three PNG charts in `reports/figures/` and rehearse aloud. A presentation to your trainer cannot be performed by this script.
"""
    (REPORTS / "presentation_notes.md").write_text(notes, encoding="utf-8")
    print("Saved reports/one_page_summary.md and reports/presentation_notes.md")


def create_notebook(df, qa, insights):
    """Make an executable, clean notebook. Run the nbconvert command in README.md."""
    def markdown(source):
        return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}
    def code(source):
        return {"cell_type": "code", "metadata": {}, "execution_count": None,
                "outputs": [], "source": source.splitlines(keepends=True)}

    cells = [
        markdown("# Day 5: Employee Data Analysis\n\n**Practice only:** the Day 5 assignment has no data file; these data are synthetic.\n"),
        markdown("## 1. Load the cleaned data\n"),
        code("from pathlib import Path\nimport pandas as pd\nfrom IPython.display import display\nbase = Path.cwd()\nif not (base / 'data' / 'clean_data.csv').exists():\n    base = base.parent\ndf = pd.read_csv(base / 'data' / 'clean_data.csv', parse_dates=['start_date'])\ndisplay(df.head())\n"),
        markdown("## 2. Cleaning audit and decisions\n\nReview `cleaning_decisions.md` and the saved before/after file.\n"),
        code("display(pd.read_csv(base / 'reports' / 'before_after_cleaning.csv'))\n"),
        markdown("## 3. Numeric summary, groups, and correlations\n"),
        code("numeric = ['salary', 'performance_score', 'experience_years']\ndisplay(df[numeric].agg(['mean', 'median', 'min', 'max', 'std']))\ndisplay(df.groupby('department').agg(employees=('id','count'), avg_salary=('salary','mean')))\ndisplay(df[numeric].corr())\n"),
        markdown("## 4. Five Business Questions (with numeric answers)\n\n" +
                 "\n\n".join(f"**{q}**\n\n{answer}" for q, answer in qa) + "\n"),
        markdown("## 5. Department budget merge + pivot table\n"),
        code("budgets = pd.read_csv(base / 'data' / 'department_budgets.csv')\nmerged = pd.merge(df, budgets, on='department', how='left')\ndisplay(merged[['name','department','annual_budget_inr']].head())\ndisplay(pd.pivot_table(df,index='department',columns='city',values='salary',aggfunc='mean',fill_value=0))\n"),
        markdown("## 6. Five visualisations and one-sentence insights\n"),
    ]
    for idx, (filename, insight) in enumerate(insights, 1):
        cells.append(markdown(f"### Chart {idx}\n\n![Chart {idx}](figures/{filename})\n\n**Insight:** {insight}\n"))
    cells.append(markdown("## 7. Summary and limitations\n\nOpen `one_page_summary.md` for three findings, two recommendations and limitations. The data are synthetic and correlations are descriptive, not causal.\n"))
    notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                               "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 4}
    (REPORTS / "day5_analysis.ipynb").write_text(json.dumps(notebook, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved reports/day5_analysis.ipynb (open in VS Code or export with nbconvert)")


def create_streamlit_app():
    app_path = ROOT / "app.py"
    app = '''"""Optional Day 5 BONUS: run with streamlit run app.py"""\nfrom pathlib import Path\nimport streamlit as st\nimport pandas as pd\nROOT = Path(__file__).resolve().parent\nst.set_page_config(page_title="Week 1 Employee Analysis", layout="wide")\nst.title("Day 5: Employee Analysis – Practice Dashboard")\nst.caption("Synthetic demonstration data: not real employee records")\ndf = pd.read_csv(ROOT / "data" / "clean_data.csv")\nst.metric("Cleaned employee records", len(df))\nleft, right = st.columns(2)\nwith left:\n    st.subheader("Average Salary by Department")\n    st.image(str(ROOT / "reports" / "figures" / "01_average_salary_by_department.png"), use_container_width=True)\nwith right:\n    st.subheader("Salary Distribution")\n    st.image(str(ROOT / "reports" / "figures" / "02_salary_histogram.png"), use_container_width=True)\nst.subheader("Cleaned preview")\nst.dataframe(df.head(10), use_container_width=True)\n'''
    if not app_path.exists():
        app_path.write_text(app, encoding="utf-8")
        print("Created app.py for optional Streamlit bonus")
    else:
        print("Preserved your existing app.py")


def main():
    print("WARNING: Day 5 uses explicitly synthetic PRACTICE DATA; no Day 5 dataset was supplied.")
    raw, budgets = create_demo_data()
    cleaned, audit = clean(raw)
    dept, city, qa, pairs, pivot = analysis(cleaned, budgets)
    insights = charts(cleaned, dept, city)
    write_report(cleaned, dept, city, insights, qa)
    create_notebook(cleaned, qa, insights)
    create_streamlit_app()
    print("\nDAY 5 COMPLETE. See README.md for notebook export, Streamlit and GitHub main-branch push.")


if __name__ == "__main__":
    main()
