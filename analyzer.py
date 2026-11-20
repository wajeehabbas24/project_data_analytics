import numpy as np
import pandas as pd


df = pd.read_csv("student_records.csv")
print(f"Initial row count: {len(df)}")


df = df.drop_duplicates(subset="Student_ID", keep="first").copy()


df["Department"] = df["Department"].str.strip().str.upper()


df["Marks"] = df["Marks"].fillna(0)

df["Attendance"] = df["Attendance"].fillna(df["Attendance"].mean()).round(1)

print(f"Cleaned row count: {len(df)}\n")


conditions = [
    df["Marks"] >= 85,
    df["Marks"] >= 70,
    df["Marks"] >= 50,
    df["Marks"] < 50,
]
grades = ["A", "B", "C", "F"]


df["Grade"] = np.select(conditions, grades, default="F")


df["Exam_Eligible"] = np.where(df["Attendance"] >= 75, "Yes", "No")

print("--- Sample Processed Data ---")
print(df.head(10).to_string(index=False))
print("\n")


dept_summary = (
    df.groupby("Department")
    .agg(
        Total_Students=("Student_ID", "count"),
        Avg_Marks=("Marks", "mean"),
        Avg_Attendance=("Attendance", "mean"),
    )
    .round(2)
    .reset_index()
)

print("--- Department Summary ---")
print(dept_summary.to_string(index=False))
print("\n")


topper_indices = df.groupby("Department")["Marks"].idxmax()
dept_toppers = df.loc[
    topper_indices, ["Department", "Student_ID", "Name", "Marks", "Attendance"]
]

print("--- Department Toppers ---")
print(dept_toppers.to_string(index=False))
print("\n")


corr_matrix = np.corrcoef(df["Attendance"], df["Marks"])
correlation = corr_matrix[0, 1]
print(f"Correlation between Attendance and Marks: {correlation:.2f}\n")


at_risk_df = df[(df["Marks"] < 50) | (df["Attendance"] < 75)].copy()


at_risk_df = at_risk_df.sort_values(by="Marks", ascending=True)

at_risk_df.to_csv("at_risk_students.csv", index=False)
print(
    f"Saved {len(at_risk_df)} at-risk student records to 'at_risk_students.csv'."
)