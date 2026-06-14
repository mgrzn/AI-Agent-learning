from src.monitor import get_tweets

async def scrape_twitter(username: str, limit: int = 5) -> str:
    try:
        tweets = await get_tweets(username, limit=limit)
        if not tweets:
            return f"Tidak ada tweet ditemukan dari @{username}."
        result = f"Tweet terbaru dari @{username}:\n\n"
        for i, t in enumerate(tweets, 1):
            result += f"{i}. {t[:200]}\n\n"
        return result
    except Exception as e:
        return f"Gagal mengambil tweet dari @{username}: {str(e)}"