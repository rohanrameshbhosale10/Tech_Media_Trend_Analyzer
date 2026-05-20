import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


# ─── YOUTUBE COLLECTOR ───────────────────────────────────────────
def collect_youtube(query="data science", max_results=50):
    """
    Fetches YouTube videos by keyword and saves as JSON.
    Uses 2 API calls: one to search, one to get detailed stats.
    """
    api_key = os.getenv("YOUTUBE_API_KEY")

    print(f"\n[YouTube] Searching for: '{query}'...")

    # Call 1 — search for video IDs
    search_resp = requests.get(
        "https://www.googleapis.com/youtube/v3/search",
        params={
            "part":       "snippet",
            "q":          query,
            "type":       "video",
            "maxResults": max_results,
            "order":      "viewCount",
            "key":        api_key,
        }
    )
    search_data = search_resp.json()

    if "error" in search_data:
        print(f"[YouTube] Error: {search_data['error']['message']}")
        return []

    video_ids = [item["id"]["videoId"] for item in search_data.get("items", [])]

    # Call 2 — get detailed stats using the video IDs
    stats_resp = requests.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "part": "statistics,snippet",
            "id":   ",".join(video_ids),
            "key":  api_key,
        }
    )
    stats_data = stats_resp.json()

    videos = []
    for item in stats_data.get("items", []):
        stats   = item.get("statistics", {})
        snippet = item.get("snippet", {})
        videos.append({
            "id":            item["id"],
            "title":         snippet.get("title", ""),
            "channel":       snippet.get("channelTitle", ""),
            "published_at":  snippet.get("publishedAt", ""),
            "view_count":    int(stats.get("viewCount",    0)),
            "like_count":    int(stats.get("likeCount",    0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "description":   snippet.get("description", "")[:300],
        })

    os.makedirs("data", exist_ok=True)
    filename = f"data/youtube_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=2, ensure_ascii=False)

    print(f"[YouTube] Saved {len(videos)} videos → {filename}")
    return videos


# ─── NEWSAPI COLLECTOR ───────────────────────────────────────────
def collect_news(query="artificial intelligence", max_articles=50):
    """
    Fetches news articles by keyword from 80,000+ sources.
    Free tier: 100 requests/day, articles from last 30 days.
    """
    api_key = os.getenv("NEWS_API_KEY")

    print(f"\n[News] Searching for: '{query}'...")

    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q":        query,
            "language": "en",
            "sortBy":   "popularity",
            "pageSize": max_articles,
            "apiKey":   api_key,
        }
    )
    data = response.json()

    if data.get("status") != "ok":
        print(f"[News] Error: {data.get('message', 'Unknown error')}")
        return []

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title":        article.get("title", ""),
            "source":       article.get("source", {}).get("name", ""),
            "author":       article.get("author", ""),
            "published_at": article.get("publishedAt", ""),
            "description":  article.get("description", "") or "",
            "url":          article.get("url", ""),
            "content":      (article.get("content", "") or "")[:300],
        })

    os.makedirs("data", exist_ok=True)
    filename = f"data/news_{query.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"[News]    Saved {len(articles)} articles → {filename}")
    return articles


# ─── RUN ALL COLLECTORS ──────────────────────────────────────────
if __name__ == "__main__":
    collect_youtube(query="data science", max_results=50)
    collect_news(query="artificial intelligence", max_articles=50)