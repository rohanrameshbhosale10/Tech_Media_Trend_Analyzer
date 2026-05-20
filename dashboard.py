import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os

os.makedirs("charts", exist_ok=True)
plt.rcParams["figure.facecolor"]  = "white"
plt.rcParams["axes.facecolor"]    = "#f9f9f9"
plt.rcParams["axes.spines.top"]   = False
plt.rcParams["axes.spines.right"] = False


# ─── YOUTUBE DASHBOARD ───────────────────────────────────────────
def plot_youtube(df):
    if df.empty:
        print("[YouTube] No data to plot.")
        return

    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("YouTube Analytics Dashboard", fontsize=18, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    # 1. Top 10 videos by views
    ax1 = fig.add_subplot(gs[0, :2])
    top10 = df.nlargest(10, "view_count")[["title", "view_count"]].copy()
    top10["short_title"] = top10["title"].str[:40] + "..."
    bars = ax1.barh(top10["short_title"], top10["view_count"] / 1_000_000,
                    color="#FF0000", alpha=0.8)
    ax1.set_title("Top 10 Videos by Views", fontweight="bold")
    ax1.set_xlabel("Views (millions)")
    ax1.invert_yaxis()
    for bar in bars:
        ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                 f"{bar.get_width():.1f}M", va="center", fontsize=8)

    # 2. Likes vs Comments scatter
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.scatter(df["like_count"] / 1000, df["comment_count"] / 1000,
                alpha=0.5, color="#FF6600", s=30)
    ax2.set_title("Likes vs Comments", fontweight="bold")
    ax2.set_xlabel("Likes (thousands)")
    ax2.set_ylabel("Comments (thousands)")

    # 3. Top channels by video count
    ax3 = fig.add_subplot(gs[1, 0])
    top_channels = df["channel"].value_counts().head(8)
    ax3.bar(range(len(top_channels)), top_channels.values, color="#CC0000", alpha=0.8)
    ax3.set_xticks(range(len(top_channels)))
    ax3.set_xticklabels(top_channels.index, rotation=45, ha="right", fontsize=7)
    ax3.set_title("Top Channels by Video Count", fontweight="bold")
    ax3.set_ylabel("Videos")

    # 4. Engagement distribution
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.hist(df["engagement"].clip(upper=df["engagement"].quantile(0.95)),
             bins=20, color="#FF4444", edgecolor="white", alpha=0.8)
    ax4.set_title("Engagement Score Distribution", fontweight="bold")
    ax4.set_xlabel("Engagement Score")
    ax4.set_ylabel("Videos")

    # 5. Keyword presence pie
    ax5 = fig.add_subplot(gs[1, 2])
    kw_cols = [c for c in df.columns if c.startswith("has_")]
    kw_counts = {c.replace("has_", "").replace("_", " ").title(): df[c].sum()
                 for c in kw_cols if df[c].sum() > 0}
    if kw_counts:
        ax5.pie(kw_counts.values(), labels=kw_counts.keys(),
                autopct="%1.0f%%",
                colors=["#FF0000", "#FF6600", "#FF9900", "#FFCC00", "#FF3333"],
                startangle=90)
        ax5.set_title("Keyword Presence in Titles", fontweight="bold")

    plt.savefig("charts/youtube_dashboard.png", dpi=150, bbox_inches="tight")
    print("[YouTube] Saved charts/youtube_dashboard.png")
    plt.show()


# ─── NEWS DASHBOARD ──────────────────────────────────────────────
def plot_news(df):
    if df.empty:
        print("[News] No data to plot.")
        return

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("News Analytics Dashboard", fontsize=18, fontweight="bold")

    # 1. Top sources by article count
    top_sources = df["source"].value_counts().head(10)
    axes[0].barh(top_sources.index, top_sources.values, color="#1565C0", alpha=0.8)
    axes[0].set_title("Top 10 News Sources", fontweight="bold")
    axes[0].set_xlabel("Articles")
    axes[0].invert_yaxis()

    # 2. Articles published by hour
    hourly = df["hour"].value_counts().sort_index()
    axes[1].plot(hourly.index, hourly.values, marker="o",
                 color="#1976D2", linewidth=2, markersize=5)
    axes[1].fill_between(hourly.index, hourly.values, alpha=0.15, color="#1976D2")
    axes[1].set_title("Articles Published by Hour (UTC)", fontweight="bold")
    axes[1].set_xlabel("Hour of Day")
    axes[1].set_ylabel("Articles")
    axes[1].set_xticks(range(0, 24, 2))

    # 3. Title length distribution
    axes[2].hist(df["title_length"].dropna(), bins=20,
                 color="#42A5F5", edgecolor="white", alpha=0.8)
    axes[2].set_title("Article Title Length Distribution", fontweight="bold")
    axes[2].set_xlabel("Title Length (chars)")
    axes[2].set_ylabel("Articles")

    plt.tight_layout()
    plt.savefig("charts/news_dashboard.png", dpi=150, bbox_inches="tight")
    print("[News]    Saved charts/news_dashboard.png")
    plt.show()


# ─── RUN ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        yt_df = pd.read_csv("data/cleaned/youtube_clean.csv")
        plot_youtube(yt_df)
    except FileNotFoundError:
        print("[YouTube] Run processor.py first!")

    try:
        news_df = pd.read_csv("data/cleaned/news_clean.csv")
        plot_news(news_df)
    except FileNotFoundError:
        print("[News] Run processor.py first!")