
import pandas as pd
import matplotlib.pyplot as plt

# Read employee data
df = pd.read_csv("employees.csv")

# Display employee data
print(df)


# Calculate average salary per department
avg_salary = df.groupby("department")["salary"].mean()

# Create bar chart
plt.figure(figsize=(8, 5))

bars = plt.bar(avg_salary.index, avg_salary.values)

# Add title and axis labels
plt.title("Average Salary per Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")

# Display salary values on bars
plt.bar_label(bars, fmt="%.2f")

# Save chart as PNG
plt.tight_layout()
plt.savefig("charts/average_salary_by_department.png")

plt.show()


# Histogram of salaries
plt.figure(figsize=(8, 5))

plt.hist(df["salary"], bins=5, edgecolor="black")

# Add title and labels
plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Number of Employees")

# Save chart
plt.tight_layout()
plt.savefig("charts/salary_histogram.png")

plt.show()


# Scatter plot of ID vs Salary by Department
plt.figure(figsize=(8, 5))

for department in df["department"].unique():
    department_data = df[df["department"] == department]

    plt.scatter(
        department_data["id"],
        department_data["salary"],
        label=department
    )

# Add title and labels
plt.title("Employee ID vs Salary by Department")
plt.xlabel("Employee ID")
plt.ylabel("Salary")

# Display legend
plt.legend(title="Department")

# Save chart
plt.tight_layout()
plt.savefig("charts/id_vs_salary_scatter.png")

plt.show()


# Monthly Sales Line Chart

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [12, 15, 14, 18, 22, 25]

plt.figure(figsize=(8, 5))

plt.plot(
    months,
    sales,
    marker="o",
    label="Monthly Sales"
)

# Add title and labels
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")

# Display legend
plt.legend()

# Save chart
plt.tight_layout()
plt.savefig("charts/monthly_sales.png")

plt.show()
