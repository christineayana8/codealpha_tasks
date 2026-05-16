import pandas as pd
import numpy as np

df = pd.read_csv("books_data.csv")

print("=" * 55)
print("TASK 2: Exploratory Data Analysis (EDA)")
print("=" * 55)

print("\n── 1. Dataset Overview ──────────────────────────────────")
print(f"  Shape        : {df.shape[0]} rows x {df.shape[1]} columns")
print(f"  Columns      : {list(df.columns)}")
print(f"\n  Missing values:\n{df.isnull().sum()}")
print(f"\n  Data Types:\n{df.dtypes}")

print("\n── 2. Descriptive Statistics ────────────────────────────")
print(df[["price", "rating"]].describe().round(2))

print("\n── 3. Ratings Distribution ──────────────────────────────")
rating_counts = df["rating"].value_counts().sort_index()
for r, c in rating_counts.items():
    bar = "█" * (c // 5)
    print(f"  {r} star : {bar} ({c})")

print("\n── 4. Availability Breakdown ─────────────────────────────")
avail = df["availability"].value_counts()
for k, v in avail.items():
    pct = v / len(df) * 100
    print(f"  {k:<15}: {v} books ({pct:.1f}%)")

print("\n── 5. Genre Analysis ────────────────────────────────────")
genre_stats = df.groupby("genre").agg(
    count=("title", "count"),
    avg_rating=("rating", "mean"),
    avg_price=("price", "mean")
).sort_values("avg_rating", ascending=False).round(2)
print(genre_stats.to_string())

print("\n── 6. Price Analysis ────────────────────────────────────")
print(f"  Cheapest book  : £{df['price'].min():.2f}")
print(f"  Most expensive : £{df['price'].max():.2f}")
print(f"  Average price  : £{df['price'].mean():.2f}")
print(f"  Median price   : £{df['price'].median():.2f}")
price_bins = pd.cut(df["price"], bins=[0,15,25,35,45,60],
                    labels=["£0-15","£15-25","£25-35","£35-45","£45-60"])
print(f"\n  Price ranges:\n{price_bins.value_counts().sort_index()}")

print("\n── 7. Correlation: Price vs Rating ──────────────────────")
corr = df["price"].corr(df["rating"])
print(f"  Pearson correlation : {corr:.4f}")
print(f"  Interpretation      : {'Weak' if abs(corr) < 0.3 else 'Moderate'} {'positive' if corr > 0 else 'negative'} correlation")

print("\n── 8. Top & Bottom Genres by Avg Rating ─────────────────")
print(f"\n  Top 3 genres:\n{genre_stats['avg_rating'].head(3)}")
print(f"\n  Bottom 3 genres:\n{genre_stats['avg_rating'].tail(3)}")

print("\n── 9. Outlier Check (IQR Method) ────────────────────────")
q1 = df["price"].quantile(0.25)
q3 = df["price"].quantile(0.75)
iqr = q3 - q1
outliers = df[(df["price"] < q1 - 1.5*iqr) | (df["price"] > q3 + 1.5*iqr)]
print(f"  Price outliers found: {len(outliers)}")
if len(outliers):
    print(outliers[["title","price","genre"]].to_string(index=False))

print("\n✅ EDA complete.")