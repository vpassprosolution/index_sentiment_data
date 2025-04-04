# ✅ news_fetcher_index.py – Google News 1 article scraper (1 per index)

import time
from googlesearch import search
from newspaper import Article
from database import save_sentiment, fetch_latest_prices

# 19 indexes
INDEXES = {
    "DJI": "dow jones",
    "IXIC": "nasdaq",
    "GSPC": "s&p 500",
    "FTSE": "ftse 100",
    "N225": "nikkei 225",
    "HSI": "hang seng",
    "DAX": "dax index",
    "CAC40": "cac 40",
    "STOXX50": "euro stoxx 50",
    "AORD": "asx 200",
    "BSESN": "bse sensex",
    "NSEI": "nifty 50",
    "KS11": "kospi index",
    "TWII": "taiwan index",
    "BVSP": "bovespa index",
    "MXX": "mexico ipc",
    "RUT": "russell 2000",
    "VIX": "vix index",
    "XU100": "bist 100"
}

def fetch_article(query):
    try:
        print(f"🔍 Searching: {query}")
        urls = list(search(f"{query} stock market news", num_results=5, lang="en"))
        for url in urls:
            if "youtube.com" in url or "twitter.com" in url:
                continue
            article = Article(url)
            article.download()
            article.parse()
            return {
                "title": article.title,
                "summary": article.text[:300],
                "sentiment": "neutral"
            }
    except Exception as e:
        print(f"❌ Error fetching article: {e}")
    return None

def run():
    print("📡 Running Index News Fetcher...\n")
    prices = fetch_latest_prices()  # dict from DB: {"DJI": 38314.85, ...}

    for symbol, keyword in INDEXES.items():
        print(f"\n🔍 {symbol} → keyword: {keyword}")
        article = fetch_article(keyword)

        if not article:
            print("❌ No article found.")
            print("--------------------------------------------------")
            continue

        price = prices.get(symbol)
        if price is None:
            print(f"❌ Price not found for {symbol}")
            print("--------------------------------------------------")
            continue

        save_sentiment(symbol, price, "neutral", "HOLD", article)
        print(f"✅ Saved → {symbol} | {article['title'][:60]}...")
        print("--------------------------------------------------")
        time.sleep(3)  # polite pause

if __name__ == "__main__":
    run()
