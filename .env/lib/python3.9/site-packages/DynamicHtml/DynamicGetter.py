from pyppeteer import launch
import asyncio

def DynamicHtml(url, script=None):
    content = asyncio.run(DynamicHtmlGetter(url, script))
    return content

async def DynamicHtmlGetter(url, script):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    if script:
        await page.evaluate(script)
    content = await page.content()
    await browser.close()
    return content