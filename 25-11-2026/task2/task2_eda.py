
from pathlib import Path
import pandas as pd

# File paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

print("DATASET OVERVIEW")
print("Shape:", df.shape)

# 1. Summary statistics
numeric_columns = [
    "Age", "MonthlyIncome", "YearsAtCompany",
    "TotalWorkingYears"
]

print("\n1. SUMMARY STATISTICS")
summary_stats = df[numeric_columns].agg(
    ["mean", "median", "min", "max", "std"]
)
print(summary_stats.round(2))

# 2. Department groupby analysis
print("\n2. DEPARTMENT ANALYSIS")

department_analysis = df.groupby("Department").agg(
    Employee_Count=("EmployeeNumber", "count"),
    Average_Age=("Age", "mean"),
    Average_Salary=("MonthlyIncome", "mean"),
    Average_Experience=("TotalWorkingYears", "mean"),
    Attrition_Count=("Attrition", lambda x: (x == "Yes").sum())
).round(2)

department_analysis["Attrition_Rate"] = (
    department_analysis["Attrition_Count"] /
    department_analysis["Employee_Count"] * 100
).round(2)

print(department_analysis)

department_analysis.to_csv(
    OUTPUT_DIR / "department_analysis.csv"
)

# 3. Correlation analysis
print("\n3. TOP 3 CORRELATIONS")

corr = df.select_dtypes(include="number").corr()

upper_triangle = corr.where(
    pd.DataFrame(
        True,
        index=corr.index,
        columns=corr.columns
    ).where(
        pd.DataFrame(
            [[i < j for j in range(len(corr.columns))]
             for i in range(len(corr.columns))],
            index=corr.index,
            columns=corr.columns
        )
    )
)

top_correlations = (
    upper_triangle.stack()
    .reset_index()
)
top_correlations.columns = ["Column 1", "Column 2", "Correlation"]

top_correlations["Absolute Correlation"] = (
    top_correlations["Correlation"].abs()
)

top_3 = top_correlations.sort_values(
    "Absolute Correlation", ascending=False
).head(3)

print(top_3)
top_3.to_csv(
    OUTPUT_DIR / "top_3_correlations.csv",
    index=False
)

# 4. Business questions with numeric answers
print("\n4. BUSINESS QUESTIONS AND ANSWERS")

total_employees = len(df)
attrition_count = (df["Attrition"] == "Yes").sum()

print(
    f"Q1. What is the overall attrition rate? "
    f"{attrition_count / total_employees * 100:.2f}%"
)

department_attrition = df.groupby("Department").apply(
    lambda x: (x["Attrition"] == "Yes").mean() * 100,
    include_groups=False
)

print(
    f"Q2. Which department has the highest attrition rate? "
    f"{department_attrition.idxmax()} "
    f"({department_attrition.max():.2f}%)"
)

overtime_attrition = df.groupby("OverTime")["Attrition"].apply(
    lambda x: (x == "Yes").mean() * 100
)

print(
    f"Q3. What is the attrition rate for employees working overtime? "
    f"{overtime_attrition.get('Yes', 0):.2f}%"
)

print(
    f"Q4. Which department has the highest average monthly income? "
    f"{department_analysis['Average_Salary'].idxmax()}"
)

print(
    f"Q5. What is the average employee age? "
    f"{df['Age'].mean():.2f} years"
)

# 5. Merge department budget table
print("\n5. DEPARTMENT BUDGET MERGE")

# Illustrative budget figures, not actual company budgets
budget_df = pd.DataFrame({
    "Department": [
        "Human Resources",
        "Research & Development",
        "Sales"
    ],
    "Illustrative_Budget": [500000, 3000000, 2000000]
})

merged_df = pd.merge(
    department_analysis.reset_index(),
    budget_df,
    on="Department",
    how="left"
)

print(merged_df)

merged_df.to_csv(
    OUTPUT_DIR / "department_budget_analysis.csv",
    index=False
)

# Bonus: Pivot table
print("\n6. BONUS PIVOT TABLE")

pivot = pd.pivot_table(
    df,
    index="Department",
    columns="Gender",
    values="EmployeeNumber",
    aggfunc="count",
    fill_value=0
)

print(pivot)

pivot.to_csv(OUTPUT_DIR / "department_gender_pivot.csv")

print("\nTASK 2 ANALYSIS COMPLETED SUCCESSFULLY!")
