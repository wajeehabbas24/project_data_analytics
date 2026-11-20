import numpy as np
import pandas as pd

np.random.seed(42)
n = 150

names = [f"Student_{i:03d}" for i in range(1, n + 1)]

departments = np.random.choice(
    ["CSE", "cse", "Cse", "IT", "it", "ECE", "ece"], size=n
)
marks = np.random.randint(35, 100, size=n).astype(float)
attendance = np.random.randint(60, 100, size=n).astype(float)


marks[np.random.choice(n, 10, replace=False)] = np.nan
attendance[np.random.choice(n, 6, replace=False)] = np.nan

df = pd.DataFrame({
    "Student_ID": range(1001, 1001 + n),
    "Name": names,
    "Department": departments,
    "Marks": marks,
    "Attendance": attendance,
})


df = pd.concat([df, df.iloc[:5]], ignore_index=True)

df.to_csv("student_records.csv", index=False)
print("Created student_records.csv with", len(df), "rows!")