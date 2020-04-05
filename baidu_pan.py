import os
import asyncio
from pyppeteer import launch


USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')


async def main():
    browser = await launch(headless=False, slowMo=25)
    page = await browser.newPage()
    await page.setViewport({
        'width': 1200,
        'height': 800
    })
    await page.goto('https://pan.baidu.com/')
    await page.click('.tang-pass-footerBarULogin')
    await page.type('#TANGRAM__PSP_4__userName', USERNAME)
    await page.type('#TANGRAM__PSP_4__password', PASSWORD)
    await page.click('#TANGRAM__PSP_4__submit')
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
