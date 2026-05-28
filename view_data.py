import pandas as pd

df = pd.read_parquet("data/cache/restaurants.parquet")

print("\nCOLUMNS:\n")
print(df.columns)

print("\nTOTAL ROWS:\n")
print(len(df))

print("\nCITY COUNTS:\n")
print(df["city"].value_counts())

print("\nLOCATION SAMPLE:\n")
print(df["location"].unique()[:20])

print("\nBUDGET TIERS:\n")
print(df["budget_tier"].value_counts())