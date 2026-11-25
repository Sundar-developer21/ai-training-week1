
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "WA_Fn-UseC_-HR-Employee-Attrition.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "reports", "figures")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

# Consistent chart style
sns.set_theme(style="whitegrid", palette="Set2")

# 1. Bar Chart - Average salary by department
salary = df.groupby("Department")["MonthlyIncome"].mean()

plt.figure(figsize=(9, 5))
salary.plot(kind="bar", legend=True)
plt.title("Average Monthly Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average Monthly Income (Salary Units)")
plt.xticks(rotation=0)
plt.legend(["Average Salary"])
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "01_bar_salary_by_department.png"))
plt.close()

print("Chart 1 Insight: Sales has the highest average monthly salary.")

# 2. Histogram - Employee age distribution
plt.figure(figsize=(9, 5))
plt.hist(df["Age"], bins=15, edgecolor="black", label="Employees")
plt.title("Employee Age Distribution")
plt.xlabel("Age (Years)")
plt.ylabel("Number of Employees (Count)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "02_histogram_age_distribution.png"))
plt.close()

print("Chart 2 Insight: The histogram shows the distribution of employees across age groups.")

# 3. Scatter Plot - Age vs Monthly Income
plt.figure(figsize=(9, 5))
sns.scatterplot(
    data=df,
    x="Age",
    y="MonthlyIncome",
    hue="Attrition"
)
plt.title("Employee Age vs Monthly Income")
plt.xlabel("Age (Years)")
plt.ylabel("Monthly Income (Salary Units)")
plt.legend(title="Attrition")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "03_scatter_age_vs_income.png"))
plt.close()

print("Chart 3 Insight: Monthly income varies across employees of different ages.")

# 4. Line Chart - Average salary by job level
job_salary = df.groupby("JobLevel")["MonthlyIncome"].mean().sort_index()

plt.figure(figsize=(9, 5))
plt.plot(
    job_salary.index,
    job_salary.values,
    marker="o",
    label="Average Monthly Salary"
)
plt.title("Average Monthly Salary by Job Level")
plt.xlabel("Job Level")
plt.ylabel("Average Monthly Income (Salary Units)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "04_line_salary_by_job_level.png"))
plt.close()

print("Chart 4 Insight: Average monthly salary increases across job levels.")

# 5. Box Plot - Monthly income by department
plt.figure(figsize=(9, 5))
sns.boxplot(data=df, x="Department", y="MonthlyIncome")
plt.title("Monthly Income Distribution by Department")
plt.xlabel("Department")
plt.ylabel("Monthly Income (Salary Units)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "05_boxplot_income_by_department.png"))
plt.close()

print("Chart 5 Insight: The box plot compares salary spread and outliers across departments.")

print("\nAll 5 charts saved successfully in reports/figures/")
