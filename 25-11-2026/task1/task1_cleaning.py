
import pandas as pd

# Load dataset
df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

# Display first 5 rows
print("FIRST 5 ROWS")
print(df.head())

# Dataset information
print("\nDATASET INFORMATION")
print(df.info())

# Dataset shape
print("\nDATASET SHAPE")
print(df.shape)

# Missing values
print("\nMISSING VALUES")
print(df.isnull().sum().sum())

# Duplicate rows
print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

print("\nCOLUMN DATA TYPES")
print(df.dtypes)

print("\nNUMERIC COLUMNS")
print(df.select_dtypes(include="number").columns.tolist())

print("\nTEXT COLUMNS")
print(df.select_dtypes(include="object").columns.tolist())

print("\nDATASET INFORMATION")
df.info()

print("\nTEXT COLUMN NAMES")
print(df.select_dtypes(include=["object", "str"]).columns.tolist())

print("\nUNIQUE VALUES IN TEXT COLUMNS")

text_columns = df.select_dtypes(include=["object", "str"]).columns

for col in text_columns:
    print(f"\n{col}:")
    print(df[col].unique())

# TEXT STANDARDIZATION

clean_df = df.copy()

text_columns = clean_df.select_dtypes(include=["str"]).columns

for col in text_columns:
    clean_df[col] = clean_df[col].str.strip()

print("\nTEXT STANDARDIZATION COMPLETED")

for col in text_columns:
    print(f"{col}: {clean_df[col].nunique()} unique values")

# OUTLIER DETECTION USING IQR

numeric_columns = clean_df.select_dtypes(include="number").columns

print("\nOUTLIER DETECTION")

for col in numeric_columns:
    Q1 = clean_df[col].quantile(0.25)
    Q3 = clean_df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = clean_df[
        (clean_df[col] < lower_limit) |
        (clean_df[col] > upper_limit)
    ]

    if len(outliers) > 0:
        print(f"{col}: {len(outliers)} outliers")

# BEFORE AND AFTER SUMMARY

before_summary = {
    "Rows": len(df),
    "Missing Values": df.isnull().sum().sum(),
    "Duplicates": df.duplicated().sum()
}

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

# SAVE CLEANED DATA

clean_df.to_csv("output/clean_data.csv", index=False)

print("\nCleaned dataset saved successfully!")

