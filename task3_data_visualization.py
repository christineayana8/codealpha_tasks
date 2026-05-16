import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("books_data.csv")

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "#0f1117",
    "axes.facecolor": "#1a1d27",
    "text.color": "#e0e0e0",
    "axes.labelcolor": "#e0e0e0",
    "xtick.color": "#aaaaaa",
    "ytick.color": "#aaaaaa",
    "axes.titlecolor": "#ffffff",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "grid.color": "#2e3247",
    "grid.linewidth": 0.6,
})

ACCENT = ["#4e9af1","#f1914e","#4ef19a","#f14e6e","#b04ef1",
          "#f1d44e","#4ef1e8","#f14eb0","#9af14e","#f16e4e"]

fig, axes = plt.subplots(2, 3, figsize=(24, 14))
fig.suptitle("Books Data Analytics Dashboard", fontsize=22,
             fontweight="bold", color="white", y=0.98)
fig.patch.set_facecolor("#0f1117")

# Chart 1: Rating Distribution
ax = axes[0, 0]
rating_counts = df["rating"].value_counts().sort_index()
colors = ["#f14e6e","#f1914e","#f1d44e","#4e9af1","#4ef19a"]
bars = ax.bar(rating_counts.index, rating_counts.values,
              color=colors, width=0.6, edgecolor="none", zorder=3)
ax.set_title("Rating Distribution")
ax.set_xlabel("Star Rating")
ax.set_ylabel("Number of Books")
ax.grid(axis="y", zorder=0)
for bar, val in zip(bars, rating_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            str(val), ha="center", va="bottom", fontsize=11, color="white")

# Chart 2: Price Distribution
ax = axes[0, 1]
ax.hist(df["price"], bins=20, color="#4e9af1", edgecolor="#0f1117",
        linewidth=0.5, zorder=3)
ax.axvline(df["price"].mean(), color="#f1914e", linestyle="--",
           linewidth=1.5, label=f"Mean: £{df['price'].mean():.2f}")
ax.axvline(df["price"].median(), color="#4ef19a", linestyle="--",
           linewidth=1.5, label=f"Median: £{df['price'].median():.2f}")
ax.set_title("Price Distribution")
ax.set_xlabel("Price (£)")
ax.set_ylabel("Count")
ax.legend(fontsize=10)
ax.grid(axis="y", zorder=0)

# Chart 3: Avg Rating by Genre (Top 15 only)
ax = axes[0, 2]
genre_avg = df.groupby("genre")["rating"].mean().sort_values(ascending=True).tail(15)
colors_genre = [ACCENT[i % len(ACCENT)] for i in range(len(genre_avg))]
bars = ax.barh(genre_avg.index, genre_avg.values, color=colors_genre,
               edgecolor="none", height=0.6)
ax.set_title("Avg Rating by Genre (Top 15)")
ax.set_xlabel("Average Rating")
ax.set_xlim(0, 6.2)
ax.axvline(df["rating"].mean(), color="white", linestyle="--",
           linewidth=1, alpha=0.5)
for bar, val in zip(bars, genre_avg.values):
    ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
            f"{val:.2f}", va="center", fontsize=9, color="white")
ax.tick_params(axis="y", labelsize=10)

# Chart 4: Books per Genre (Pie)
ax = axes[1, 0]
genre_counts = df["genre"].value_counts()
top_genres = genre_counts.head(8)
other = genre_counts[8:].sum()
pie_data = pd.concat([top_genres, pd.Series({"Other": other})])
wedges, texts, autotexts = ax.pie(
    pie_data.values, labels=pie_data.index,
    autopct="%1.1f%%", colors=ACCENT[:len(pie_data)],
    startangle=140, pctdistance=0.82,
    wedgeprops={"edgecolor": "#0f1117", "linewidth": 1.5}
)
for t in texts: t.set_color("white"); t.set_fontsize(10)
for at in autotexts: at.set_color("white"); at.set_fontsize(9)
ax.set_title("Books per Genre")

# Chart 5: Price by Rating (Box Plot)
ax = axes[1, 1]
groups = [df[df["rating"] == r]["price"].values for r in sorted(df["rating"].unique())]
bp = ax.boxplot(groups, patch_artist=True,
                medianprops={"color": "white", "linewidth": 2},
                whiskerprops={"color": "#aaaaaa"},
                capprops={"color": "#aaaaaa"},
                flierprops={"marker": "o", "color": "#f14e6e", "markersize": 4})
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color); patch.set_alpha(0.8)
ax.set_title("Price Distribution by Rating")
ax.set_xlabel("Star Rating")
ax.set_ylabel("Price (£)")
ax.set_xticklabels(["1 star","2 star","3 star","4 star","5 star"])
ax.grid(axis="y")

# Chart 6: Availability (Donut)
ax = axes[1, 2]
avail = df["availability"].value_counts()
wedges, texts, autotexts = ax.pie(
    avail.values, labels=avail.index,
    autopct="%1.1f%%", colors=["#4ef19a","#f14e6e"],
    startangle=90, pctdistance=0.75,
    wedgeprops={"edgecolor": "#0f1117", "linewidth": 2, "width": 0.55}
)
for t in texts: t.set_color("white"); t.set_fontsize(12)
for at in autotexts: at.set_color("white"); at.set_fontsize(11)
ax.set_title("Stock Availability")
centre = plt.Circle((0,0), 0.42, fc="#1a1d27")
ax.add_patch(centre)
ax.text(0, 0, f"{len(df)}\nbooks", ha="center", va="center",
        fontsize=13, color="white", fontweight="bold")

plt.tight_layout(rect=[0, 0, 1, 0.96], h_pad=4, w_pad=3)
plt.savefig("task3_visualization.png", dpi=150,
            bbox_inches="tight", facecolor="#0f1117")
print("✅ Visualization saved as task3_visualization.png")
plt.show()