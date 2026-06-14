from playwright.async_api import async_playwright

AUTH_TOKEN = "8afdbcb11a719877916949f8694f39f9d305b806"
CT0 = "b569f300ac631962dc0f0c3afddbacf79c3abc1abe6ebb05a460d87f649adb7c2897668553456e03eda2ec453602ec56e9f7fd12918f455e7229bc0e3b3f181afab107c62d3485645f843d48580587b7"

async def web_search(query: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            
            # Inject cookies X
            await context.add_cookies([
                {"name": "auth_token", "value": AUTH_TOKEN, "domain": ".x.com", "path": "/"},
                {"name": "ct0", "value": CT0, "domain": ".x.com", "path": "/"},
            ])
            
            page = await context.new_page()
            search_url = f"https://x.com/search?q={query.replace(' ', '+')}&src=typed_query&f=live"
            await page.goto(search_url, wait_until="networkidle")
            await page.wait_for_timeout(4000)
            await page.evaluate("window.scrollBy(0, 500)")
            await page.wait_for_timeout(2000)
            
            elements = await page.query_selector_all('div[dir="auto"].font-chirp')
            results = []
            for el in elements:
                text = (await el.inner_text()).strip()
                if text and len(text) > 20:
                    results.append(text)
                if len(results) >= 10:
                    break
            
            await browser.close()
        
        if not results:
            return "Tidak ada hasil ditemukan."
        
        return f"Hasil pencarian '{query}' di X:\n\n" + "\n\n".join(results)
    
    except Exception as e:
        return f"Gagal search: {str(e)}"