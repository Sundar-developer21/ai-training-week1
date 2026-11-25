
from pathlib import Path
import pandas as pd

# File paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)

print("ORIGINAL DATASET")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Before cleaning summary
before_summary = {
    "Rows": len(df),
    "Missing Values": df.isnull().sum().sum(),
    "Duplicates": df.duplicated().sum()
}

# Create cleaning copy
clean_df = df.copy()

# Handle missing values
print("\nMISSING VALUE HANDLING")

for col in clean_df.columns:
    missing_count = clean_df[col].isnull().sum()

    if missing_count > 0:
        if pd.api.types.is_numeric_dtype(clean_df[col]):
            clean_df[col] = clean_df[col].fillna(clean_df[col].median())
            print(f"{col}: Filled with median")
        else:
            mode_value = clean_df[col].mode()
            if not mode_value.empty:
                clean_df[col] = clean_df[col].fillna(mode_value[0])
                print(f"{col}: Filled with mode")
            else:
                print(f"{col}: Missing values retained")

if clean_df.isnull().sum().sum() == 0:
    print("No missing values found.")

# Remove duplicate rows
duplicates = clean_df.duplicated().sum()
clean_df = clean_df.drop_duplicates()
print("\nDuplicates removed:", duplicates)

# Standardize text columns
text_columns = clean_df.select_dtypes(
    include=["object", "str"]
).columns

for col in text_columns:
    clean_df[col] = clean_df[col].str.strip().str.title()

print("\nTEXT STANDARDIZATION COMPLETED")

# Check data types
print("\nDATA TYPES")
print(clean_df.dtypes)

# IQR outlier detection
outlier_columns = [
    "Age", "DailyRate", "DistanceFromHome", "HourlyRate",
    "MonthlyIncome", "MonthlyRate", "NumCompaniesWorked",
    "TotalWorkingYears", "TrainingTimesLastYear",
    "YearsAtCompany", "YearsInCurrentRole",
    "YearsSinceLastPromotion", "YearsWithCurrManager"
]

outlier_results = []

print("\nOUTLIER DETECTION USING IQR")

for col in outlier_columns:
    Q1 = clean_df[col].quantile(0.25)
    Q3 = clean_df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    count = (
        (clean_df[col] < lower_limit) |
        (clean_df[col] > upper_limit)
    ).sum()

    outlier_results.append({
        "Column": col,
        "Outliers": count
    })

    print(f"{col}: {count} outliers")

# Outliers are retained because extreme values
# may represent valid employee records.
outlier_df = pd.DataFrame(outlier_results)
outlier_df.to_csv(OUTPUT_DIR / "outlier_summary.csv", index=False)

# After cleaning summary
after_summary = {
    "Rows": len(clean_df),
    "Missing Values": clean_df.isnull().sum().sum(),
    "Duplicates": clean_df.duplicated().sum()
}

summary = pd.DataFrame({
    "Before Cleaning": before_summary,
    "After Cleaning": after_summary
})

print("\nBEFORE AND AFTER CLEANING SUMMARY")
print(summary)

# Save output files
clean_df.to_csv(OUTPUT_DIR / "clean_data.csv", index=False)
summary.to_csv(OUTPUT_DIR / "cleaning_summary.csv")

print("\nCleaned dataset saved successfully!")
print("Cleaning summary saved successfully!")
print("Outlier summary saved successfully!")
