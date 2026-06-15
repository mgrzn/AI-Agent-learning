from playwright.async_api import async_playwright

AUTH_TOKEN = auth
CT0 = "cto"

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
