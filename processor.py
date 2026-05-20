import pandas as pd
import json
import glob
import os


def load_json(prefix):
    """Loads all JSON files matching a prefix into one DataFrame"""
    files = glob.glob(f"data/{prefix}_*.json")
    if not files:
        print(f"[Warning] No files found for prefix '{prefix}' in data/")
        return pd.DataFrame()
    all_rows = []
    for f in files:
        with open(f, encoding="utf-8") as file:
            all_rows.extend(json.load(file))
    df = pd.DataFrame(all_rows)
    print(f"[{prefix}] Loaded {len(df)} rows from {len(files)} file(s)")
    return df


# ─── YOUTUBE ─────────────────────────────────────────────────────
def clean_youtube(df):
    if df.empty:
        return df
    df = df.drop_duplicates(subset=["id"])
    df = df.dropna(subset=["title"])
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
    df["year"]  = df["published_at"].dt.year
    df["month"] = df["published_at"].dt.month_name()

    # Engagement score = likes + (comments * 2)
    df["engagement"] = df["like_count"] + (df["comment_count"] * 2)

    # Keyword flags in title
    for kw in ["Python", "AI", "Machine Learning", "Data", "Tutorial"]:
        col = f"has_{kw.lower().replace(' ', '_')}"
        df[col] = df["title"].str.contains(kw, case=False, na=False)

    return df


# ─── NEWS ─────────────────────────────────────────────────────────
def clean_news(df):
    if df.empty:
        return df
    df = df.drop_duplicates(subset=["title"])
    df = df.dropna(subset=["title"])
    df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True)
    df["date"]  = df["published_at"].dt.date
    df["hour"]  = df["published_at"].dt.hour
    df["title_length"]    = df["title"].str.len()
    df["has_description"] = df["description"].str.len() > 10
    return df


# ─── REPORT ──────────────────────────────────────────────────────
def generate_report(yt_df, news_df):
    print("\n" + "=" * 50)
    print("         ANALYTICS REPORT")
    print("=" * 50)

    if not yt_df.empty:
        print(f"\n[YouTube]")
        print(f"  Total videos   : {len(yt_df)}")
        print(f"  Avg views      : {yt_df['view_count'].mean():,.0f}")
        print(f"  Avg likes      : {yt_df['like_count'].mean():,.0f}")
        print(f"  Avg engagement : {yt_df['engagement'].mean():,.0f}")
        top = yt_df.nlargest(1, "view_count").iloc[0]
        print(f"  Most viewed    : {top['title'][:60]}...")
        print(f"  Top channels:\n{yt_df['channel'].value_counts().head(5).to_string()}")

    if not news_df.empty:
        print(f"\n[News]")
        print(f"  Total articles  : {len(news_df)}")
        print(f"  Unique sources  : {news_df['source'].nunique()}")
        print(f"  Avg title length: {news_df['title_length'].mean():.0f} chars")
        print(f"  Top sources:\n{news_df['source'].value_counts().head(5).to_string()}")

    # Save cleaned CSVs
    os.makedirs("data/cleaned", exist_ok=True)
    if not yt_df.empty:
        yt_df.to_csv("data/cleaned/youtube_clean.csv", index=False)
    if not news_df.empty:
        news_df.to_csv("data/cleaned/news_clean.csv", index=False)
    print("\nCleaned CSVs saved to data/cleaned/")


# ─── RUN ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    yt_df   = clean_youtube(load_json("youtube"))
    news_df = clean_news(load_json("news"))
    generate_report(yt_df, news_df)