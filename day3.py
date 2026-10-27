"""WEEK 1 / DAY 3: NumPy, Pandas, data cleaning, merging, and bonuses.
Run from VS Code terminal: python day3.py
The three input CSV files are written to ./data if they do not already exist.
"""
from pathlib import Path
from io import StringIO
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

EMPLOYEES_CSV = """id,name,department,salary,city
1,Arun,Sales,30000,Chennai
2,Priya,HR,45000,Chennai
3,Rahul,IT,60000,Bangalore
4,Divya,IT,75000,Chennai
5,Karthik,Finance,90000,Mumbai
6,Meena,Sales,52000,Bangalore
7,Suresh,IT,68000,Chennai
8,Anitha,HR,48000,Mumbai
"""
ORDERS_CSV = """order_id,customer_id,amount
1,101,500
2,102,
3,101,700
3,101,700
4,103,300
5,104,900
"""
CUSTOMERS_CSV = """customer_id,name,city
101,Arun,Chennai
102,Priya,Mumbai
103,Rahul,Chennai
105,Divya,Bangalore
"""


def section(title):
    print("\n" + "=" * 76)
    print(title)
    print("=" * 76)


def create_input(name, text):
    file_path = DATA / name
    if not file_path.exists():
        file_path.write_text(text, encoding="utf-8")
        print(f"Created: {file_path.relative_to(ROOT)}")
    else:
        print(f"Using existing: {file_path.relative_to(ROOT)}")
    return file_path


def first_half_numpy():
    section("DAY 3 / FIRST HALF / TASK 1: NumPy Arrays")
    marks = np.array([[70, 80, 90], [60, 75, 85], [88, 92, 79], [55, 65, 70]])
    print("Marks array:\n", marks)
    print("Shape:", marks.shape)
    print("Dtype:", marks.dtype)
    print("Size:", marks.size)
    print("First two students:\n", marks[:2, :])
    print("Last subject for all students:", marks[:, -1])
    print("Student averages:", np.round(np.mean(marks, axis=1), 2))
    print("Subject averages:", np.round(np.mean(marks, axis=0), 2))
    print("Total marks per student (sum, axis=1):", np.sum(marks, axis=1))
    print("After adding 5 grace marks (broadcasting):\n", marks + 5)
    weights = np.array([0.3, 0.3, 0.4])
    print("Weighted scores:", np.dot(marks, weights))
    print("np.arange(12).reshape(3, 4):\n", np.arange(12).reshape(3, 4))

    section("DAY 3 / FIRST HALF / BONUS: Reshape 24 values into 2x3x4")
    cube = np.arange(24).reshape(2, 3, 4)
    print("Full shape:", cube.shape)
    for index, array_slice in enumerate(cube):
        print(f"Slice along axis 0, index {index}: shape {array_slice.shape}\n{array_slice}")


def first_half_pandas():
    section("DAY 3 / FIRST HALF / TASK 2: Pandas DataFrame Basics")
    csv_path = create_input("employees.csv", EMPLOYEES_CSV)
    df = pd.read_csv(csv_path)
    print("First five rows (head):\n", df.head())
    print("\nDataFrame information (info):")
    df.info()
    print("\nNumerical summary (describe):\n", df.describe())
    print("\nName column:\n", df["name"].to_string(index=False))
    print("\nName and salary columns:\n", df[["name", "salary"]].to_string(index=False))
    chennai = df.loc[df["city"] == "Chennai", "name"]
    print("\nChennai:", ", ".join(chennai))
    print("\niloc[0:3, 1:3]:\n", df.iloc[0:3, 1:3])
    high_salary = df.loc[df["salary"] > 50000]
    it_employees = df.loc[df["department"] == "IT"]
    print("\nSalary above 50000:", len(high_salary), "employees")
    print(high_salary[["name", "salary"]].to_string(index=False))
    print("IT department:", ", ".join(it_employees["name"]))
    print("IT department count:", len(it_employees))
    print("\nThree-line explanation:")
    print("1. head() previews the first five rows.")
    print("2. info() shows row/column structure, non-null counts and data types.")
    print("3. describe() summarizes numeric columns using count, mean, min, max and more.")


def second_half_clean_and_merge():
    section("DAY 3 / SECOND HALF / TASK 1: Cleaning and Aggregation")
    orders_path = create_input("orders.csv", ORDERS_CSV)
    customers_path = create_input("customers.csv", CUSTOMERS_CSV)
    raw = pd.read_csv(orders_path)
    print("Original orders:\n", raw.to_string(index=False))
    print("\nMissing values by column:\n", raw.isna().sum())
    print("Duplicate mask:\n", raw.duplicated().to_string(index=False))
    print("Duplicate count:", int(raw.duplicated().sum()))
    print("Example dropna (how many rows would be kept):", len(raw.dropna()))

    cleaned = raw.drop_duplicates().copy()
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")
    median = cleaned["amount"].median()
    cleaned["amount"] = cleaned["amount"].fillna(median)
    cleaned["order_id"] = cleaned["order_id"].astype(str)
    print("Median used:", median)
    print("\nCleaned orders:\n", cleaned.to_string(index=False))
    print("Cleaned data types:\n", cleaned.dtypes)
    cleaned.to_csv(DATA / "orders_cleaned.csv", index=False)

    totals = cleaned.groupby("customer_id").agg(
        total=("amount", "sum"), orders=("order_id", "count")
    )
    print("\nGroupBy totals and order counts:\n", totals.to_string())
    totals.to_csv(DATA / "customer_order_summary.csv")

    section("DAY 3 / SECOND HALF / TASK 2: Merge inner, left, and outer")
    customers = pd.read_csv(customers_path)
    print("Customer table:\n", customers.to_string(index=False))
    inner = pd.merge(cleaned, customers, on="customer_id", how="inner")
    print("\nInner join rows:", len(inner))
    print(inner.to_string(index=False))
    customer_left = pd.merge(customers, cleaned, on="customer_id", how="left", indicator=True)
    no_orders = customer_left.loc[customer_left["_merge"] == "left_only", "name"]
    print("\nCustomers without orders:", ", ".join(no_orders))
    order_outer = pd.merge(cleaned, customers, on="customer_id", how="outer", indicator=True)
    orphan = order_outer.loc[order_outer["_merge"] == "left_only", "customer_id"]
    print("Orders without customer record (IDs):", orphan.astype(int).tolist())
    print("\nThree join explanations:")
    print("1. Inner join: retain rows with matching customer IDs in both tables.")
    print("2. Left join: retain all rows from the left table, even without a match.")
    print("3. Outer join: retain all rows from both tables, including unmatched ones.")
    inner.to_csv(DATA / "orders_customers_inner.csv", index=False)

    section("DAY 3 / SECOND HALF / BONUS: Concatenate monthly files")
    jan, feb = cleaned.iloc[:3].copy(), cleaned.iloc[3:].copy()
    jan.insert(0, "month", "January")
    feb.insert(0, "month", "February")
    jan.to_csv(DATA / "orders_january.csv", index=False)
    feb.to_csv(DATA / "orders_february.csv", index=False)
    month_a = pd.read_csv(DATA / "orders_january.csv", dtype={"order_id": str})
    month_b = pd.read_csv(DATA / "orders_february.csv", dtype={"order_id": str})
    combined = pd.concat([month_a, month_b], ignore_index=True)
    print("Concatenated monthly orders:\n", combined.to_string(index=False))
    print("GroupBy after concat:\n", combined.groupby("customer_id").agg(
        total=("amount", "sum"), orders=("order_id", "count")
    ).to_string())
    combined.to_csv(DATA / "orders_combined_months.csv", index=False)


def main():
    first_half_numpy()
    first_half_pandas()
    second_half_clean_and_merge()
    print("\nDAY 3 COMPLETE. CSV outputs are in the data/ folder. Now run: python day4.py")


if __name__ == "__main__":
    main()
