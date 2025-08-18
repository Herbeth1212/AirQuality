import numpy as np
import pandas as pd
df = pd.read_csv("Cases_data.csv")

df["date"] = pd.to_datetime(
    df["Month"].astype(str) + " " + df["Year"].astype(str) + " 01",
    format="%B %Y %d",   # Use %b instead of %B if months are in short form (Jan, Feb)
    errors="coerce"      # In case there are invalid values
)

# Convert to dd-mm-yy
df["date"] = df["date"].dt.strftime("%d-%m-%y")
df.to_csv("Cases_data.csv", index=False)
print(df["date"])