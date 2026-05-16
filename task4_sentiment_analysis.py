import pandas as pd
from textblob import TextBlob

df = pd.read_csv("books_data.csv")

print("=" * 55)
print("TASK 4: Sentiment Analysis")
print("=" * 55)

# Classify sentiment using TextBlob
def classify_sentiment(text):
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive", polarity
    elif polarity < -0.1:
        return "Negative", polarity
    else:
        return "Neutral", polarity

results = df["description"].apply(classify_sentiment)
df["sentiment"] = results.apply(lambda x: x[0])
df["polarity_score"] = results.apply(lambda x: round(x[1], 4))

print("\n── Sentiment Distribution ───────────────────────────")
sent_counts = df["sentiment"].value_counts()
for s, c in sent_counts.items():
    emoji = {"Positive": ":)", "Neutral": ":|", "Negative": ":("}.get(s, "")
    bar = "█" * (c // 5)
    print(f"  {emoji} {s:<10}: {bar} {c} ({c/len(df)*100:.1f}%)")

print("\n── Avg Polarity by Star Rating ──────────────────────")
rating_sentiment = df.groupby("rating")["polarity_score"].mean().round(4)
for r, score in rating_sentiment.items():
    label = "Positive" if score > 0.1 else "Negative" if score < -0.1 else "Neutral"
    print(f"  {r} star: {score:+.4f} -> {label}")

print("\n── Sentiment by Genre ───────────────────────────────")
genre_sent = df.groupby("genre").agg(
    avg_polarity=("polarity_score", "mean"),
    positive_pct=("sentiment", lambda x: (x == "Positive").sum() / len(x) * 100),
    negative_pct=("sentiment", lambda x: (x == "Negative").sum() / len(x) * 100),
).round(2).sort_values("avg_polarity", ascending=False)
print(genre_sent.to_string())

print("\n── Sample Positive Descriptions ─────────────────────")
pos = df[df["sentiment"] == "Positive"][["title","genre","rating","polarity_score","description"]].head(3)
for _, row in pos.iterrows():
    print(f"  [{row['genre']}] {row['title'][:45]}...")
    print(f"  Rating: {row['rating']} stars | Polarity: {row['polarity_score']}")
    print(f"  \"{row['description'][:100]}...\"")
    print()

print("\n── Sample Negative Descriptions ─────────────────────")
neg = df[df["sentiment"] == "Negative"][["title","genre","rating","polarity_score","description"]].head(3)
for _, row in neg.iterrows():
    print(f"  [{row['genre']}] {row['title'][:45]}...")
    print(f"  Rating: {row['rating']} stars | Polarity: {row['polarity_score']}")
    print(f"  \"{row['description'][:100]}...\"")
    print()

print("\n── Business Insights ────────────────────────────────")
top_genre = genre_sent["avg_polarity"].idxmax()
bot_genre = genre_sent["avg_polarity"].idxmin()
print(f"  Most positively perceived genre : {top_genre}")
print(f"  Most negatively perceived genre : {bot_genre}")
print(f"  Overall avg polarity            : {df['polarity_score'].mean():.4f}")
print(f"  Correlation (rating vs polarity): {df['rating'].corr(df['polarity_score']):.4f}")

df.to_csv("books_with_sentiment.csv", index=False)
print("\n✅ Sentiment analysis complete. Saved to books_with_sentiment.csv")