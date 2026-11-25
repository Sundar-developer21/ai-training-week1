
import pandas as pd

# 1. Load Dataset
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")

print("=" * 60)
print("TASK 2 - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# 2. Summary Statistics
print("\n1. SUMMARY STATISTICS")

numeric_columns = [
    "Age",
    "MonthlyIncome",
    "YearsAtCompany",
    "TotalWorkingYears"
]

summary = df[numeric_columns].agg(
    ["mean", "median", "min", "max", "std"]
)

print(summary.round(2))


# 3. GroupBy and Aggregation
print("\n2. DEPARTMENT-WISE ANALYSIS")

department_analysis = df.groupby("Department").agg(
    Employee_Count=("EmployeeNumber", "count"),
    Average_Age=("Age", "mean"),
    Average_Salary=("MonthlyIncome", "mean"),
    Average_Experience=("TotalWorkingYears", "mean")
)

print(department_analysis.round(2))


# 4. Top 3 Correlations
print("\n3. TOP 3 CORRELATIONS")

correlation = df.corr(numeric_only=True)

correlation_pairs = correlation.where(
    ~pd.DataFrame(
        [[i >= j for j in range(len(correlation.columns))]
         for i in range(len(correlation.columns))],
        index=correlation.index,
        columns=correlation.columns
    )
).stack().reset_index()

correlation_pairs.columns = ["Column 1", "Column 2", "Correlation"]

top_3 = correlation_pairs.reindex(
    correlation_pairs["Correlation"].abs().sort_values(
        ascending=False
    ).index
).head(3)

print(top_3.to_string(index=False))


# 5. Business Questions with Numerical Answers
print("\n4. BUSINESS QUESTIONS")

# Question 1: What is the overall attrition rate?
attrition_rate = (
    df["Attrition"].eq("Yes").mean() * 100
)

print(
    f"Q1. Overall attrition rate: {attrition_rate:.2f}%"
)

# Question 2: Which department has the highest average salary?
salary_by_department = df.groupby(
    "Department"
)["MonthlyIncome"].mean()

highest_salary_department = salary_by_department.idxmax()

print(
    f"Q2. Highest average salary department: "
    f"{highest_salary_department} "
    f"(Rs. {salary_by_department.max():.2f})"
)

# Question 3: Does overtime relate to attrition?
overtime_attrition = pd.crosstab(
    df["OverTime"],
    df["Attrition"],
    normalize="index"
) * 100

print("\nQ3. Attrition percentage based on overtime:")
print(overtime_attrition.round(2))


# 6. Merge with Second Table
print("\n5. MERGE WITH DEPARTMENT BUDGET")

# Illustrative budget data created for this exercise
department_budget = pd.DataFrame({
    "Department": [
        "Sales",
        "Research & Development",
        "Human Resources"
    ],
    "Annual_Budget": [
        5000000,
        8000000,
        2000000
    ]
})

merged_data = pd.merge(
    department_analysis.reset_index(),
    department_budget,
    on="Department",
    how="left"
)

print(merged_data.round(2).to_string(index=False))


# 7. Bonus - Pivot Table
print("\n6. BONUS - PIVOT TABLE")

pivot = pd.pivot_table(
    df,
    values="MonthlyIncome",
    index="Department",
    columns="Attrition",
    aggfunc="mean"
)

print(pivot.round(2))


# 8. Save Results
department_analysis.to_csv(
    "department_analysis.csv"
)

merged_data.to_csv(
    "department_budget_analysis.csv",
    index=False
)

top_3.to_csv(
    "top_3_correlations.csv",
    index=False
)

print("\nAll analysis completed successfully!")
