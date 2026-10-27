"""WEEK 1 / DAY 4: Four Matplotlib charts + 2x2 subplot bonus.
Run Day 3 first to create data/employees.csv; then: python day4.py
The Git/GitHub task is performed with terminal commands in README.md.
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Save PNG charts even if a graphical display isn't available.
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
EMPLOYEES = ROOT / "data" / "employees.csv"
FIGURES = ROOT / "reports" / "day4_figures"
FIGURES.mkdir(parents=True, exist_ok=True)
COLORS = {"Finance": "#235789", "HR": "#F29E4C", "IT": "#2A9D8F", "Sales": "#8E6CBE"}


def finish(filename):
    path = FIGURES / filename
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()
    print("Saved:", path.relative_to(ROOT))


def bar_chart(df):
    averages = df.groupby("department")["salary"].mean().sort_index()
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(averages.index, averages.values,
                  color=[COLORS.get(d, "#235789") for d in averages.index])
    ax.set(title="Average Salary by Department", xlabel="Department", ylabel="Average Salary (INR)")
    ax.bar_label(bars, labels=[f"₹{v:,.0f}" for v in averages.values], padding=3)
    ax.set_ylim(0, averages.max() * 1.18)
    fig.tight_layout()
    finish("01_department_average_salary.png")


def histogram(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["salary"], bins=5, color="#235789", edgecolor="white")
    ax.set(title="Employee Salary Distribution (5 bins)", xlabel="Salary (INR)", ylabel="Employees (count)")
    fig.tight_layout()
    finish("02_salary_histogram.png")


def scatter_chart(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    for department, subset in df.groupby("department"):
        ax.scatter(subset["id"], subset["salary"], label=department,
                   color=COLORS.get(department, "#235789"), s=75, alpha=.9)
    ax.set(title="Employee ID vs Salary", xlabel="Employee ID", ylabel="Salary (INR)")
    ax.legend(title="Department")
    fig.tight_layout()
    finish("03_id_vs_salary_scatter.png")


def line_chart():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    sales = [12, 15, 14, 18, 22, 25]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(months, sales, color="#2A9D8F", marker="o", linewidth=2.5, label="Monthly sales")
    ax.set(title="Monthly Sales (January–June)", xlabel="Month", ylabel="Sales (units)")
    ax.legend()
    ax.grid(alpha=.2)
    fig.tight_layout()
    finish("04_monthly_sales_line.png")


def bonus_subplots(df):
    averages = df.groupby("department")["salary"].mean().sort_index()
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    a, b, c, d = axes.flat
    bars = a.bar(averages.index, averages, color=[COLORS.get(x, "#235789") for x in averages.index])
    a.bar_label(bars, fmt="%.0f", padding=2, fontsize=8)
    a.set(title="Average Salary by Department", xlabel="Department", ylabel="INR")
    b.hist(df["salary"], bins=5, color="#235789", edgecolor="white")
    b.set(title="Salary Histogram (5 bins)", xlabel="INR", ylabel="Employees")
    for department, subset in df.groupby("department"):
        c.scatter(subset["id"], subset["salary"], label=department, color=COLORS.get(department, "#235789"))
    c.set(title="ID vs Salary", xlabel="Employee ID", ylabel="INR")
    c.legend(fontsize=8, title="Department")
    d.plot(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [12, 15, 14, 18, 22, 25],
           marker="o", color="#2A9D8F", label="Monthly sales")
    d.set(title="Monthly Sales", xlabel="Month", ylabel="Sales (units)")
    d.legend()
    fig.suptitle("Week 1 Day 4 – Four Charts in One Figure", fontsize=15, weight="bold")
    fig.tight_layout()
    finish("05_bonus_subplots_2x2.png")


def main():
    if not EMPLOYEES.exists():
        raise SystemExit("Missing data/employees.csv. Run 'python day3.py' first.")
    df = pd.read_csv(EMPLOYEES)
    bar_chart(df)
    histogram(df)
    scatter_chart(df)
    line_chart()
    bonus_subplots(df)
    print("\nDAY 4 COMPLETE: 4 required PNGs and 1 bonus PNG saved.")
    print("GitHub steps (main branch only): open README.md and follow the Git section.")
    print("Next: python day5.py")


if __name__ == "__main__":
    main()
