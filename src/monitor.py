import asyncio
from playwright.async_api import async_playwright

async def get_tweets(username: str, limit: int = 5) -> list[str]:
    tweets = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto(f"https://x.com/{username}", wait_until="networkidle")
        await page.wait_for_timeout(3000)
        
        # Dismiss cookie popup
        try:
            await page.get_by_role("button", name="Refuse non-essential cookies").click()
            await page.wait_for_timeout(2000)
        except:
            pass
        
        # Scroll buat trigger lazy load
        await page.evaluate("window.scrollBy(0, 500)")
        await page.wait_for_timeout(2000)
        
        elements = await page.query_selector_all('div[dir="auto"].font-chirp')
        for el in elements:
            text = (await el.inner_text()).strip()
            if text and len(text) > 10:  # filter noise
                tweets.append(text)
                if len(tweets) >= limit:
                    break
        
        await browser.close()
    return tweets

if __name__ == "__main__":
    async def test():
        tweets = await get_tweets("elonmusk", limit=5)
        for t in tweets:
            print(t[:150])
            print("---")
    
    asyncio.run(test())