"""Optional Day 5 BONUS: run with streamlit run app.py"""
from pathlib import Path
import streamlit as st
import pandas as pd
ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Week 1 Employee Analysis", layout="wide")
st.title("Day 5: Employee Analysis – Practice Dashboard")
st.caption("Synthetic demonstration data: not real employee records")
df = pd.read_csv(ROOT / "data" / "clean_data.csv")
st.metric("Cleaned employee records", len(df))
left, right = st.columns(2)
with left:
    st.subheader("Average Salary by Department")
    st.image(str(ROOT / "reports" / "figures" / "01_average_salary_by_department.png"), width="stretch")
with right:
    st.subheader("Salary Distribution")
    st.image(str(ROOT / "reports" / "figures" / "02_salary_histogram.png"), width="stretch")
st.subheader("Cleaned preview")
st.dataframe(df.head(10), width="stretch")
