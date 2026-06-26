import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/online_retail_II.csv")

# Remove Unnamed columns
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Remove duplicates
df = df.drop_duplicates()

# Remove missing descriptions
df = df.dropna(subset=["Description"])

# Keep only valid sales
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

# Save cleaned dataset
df.to_csv("data/clean/online_retail_cleaned.csv", index=False)

print("=" * 60)
print("Dataset cleaned successfully!")
print("=" * 60)

print("\nFinal Shape:")
print(df.shape)

print("\nSaved Successfully!")
print("Location: data/clean/online_retail_cleaned.csv")