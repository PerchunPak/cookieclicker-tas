import asyncio
import typing as t
from asyncio import CancelledError
from contextlib import asynccontextmanager

from loguru import logger
from playwright.async_api import Browser, Page, async_playwright

from src.utils import log


class Logic:
    def __init__(self, browser: Browser, page: Page) -> None:
        self.browser = browser
        self.page = page

    @classmethod
    @asynccontextmanager
    async def init(cls) -> t.AsyncIterator[t.Self]:
        for method in dir(cls):  # decorate everything with `utils.log`
            if not method.startswith("_") or method == "init":
                setattr(cls, method, log(getattr(cls, method)))

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            logger.info("Navigating to page...")
            await page.goto("https://orteil.dashnet.org/cookieclicker/", wait_until="domcontentloaded")
            await page.evaluate("window.localStorageSet('CookieClickerLang', 'EN');")  # set language
            logger.info("Waiting for page to load...")
            await page.wait_for_load_state("networkidle")

            logger.info("Executing our steps...")
            yield cls(browser, page)

            await browser.close()

    async def remove_ads(self) -> None:
        elements_to_block = [
            "#google_esf",  # root google ad stuff
            "#smallSupport,.ifNoAds",  # ads upper upgrades
            "#support,#detectAds",  # under buildings
            "body > *:not(#wrapper)",  # other ads in body tag
        ]
        await self.page.evaluate(
            f"for (const el of document.querySelectorAll('{", ".join(elements_to_block)}')) el.remove();"
        )

    async def set_settings(self) -> None:
        await self.page.click("#prefsButton > .subButton")
        await self.page.fill("#volumeSlider", "0")
        await self.page.click("#fancyButton")
        await self.page.click("#particlesButton")
        await self.page.click("#numbersButton")
        await self.page.click("#milkButton")
        await self.page.click("#wobblyButton")
        await self.page.click("#monospaceButton")
        await self.page.click("#formatButton")
        await self.page.click("#notifsButton")
        await self.page.click("#prefsButton > .subButton")

    async def rename_bakery(self) -> None:
        await self.page.click("#bakeryName")
        await self.page.fill("#bakeryNameInput", "Perchun's TAS")
        await self.page.click("#promptOption0")

    async def click_loop(self) -> t.Never:
        while True:
            try:
                await self.page.click("#bigCookie")
            except Exception as e:
                if isinstance(e, CancelledError):  # probably application exited
                    logger.error("click_loop: CancelledError")
                    return  # type: ignore[misc] # Return statement in function which does not return # see upper
                else:
                    logger.exception(e)
            else:
                await asyncio.sleep(0.001)

    async def click_in_the_background(self) -> None:
        await asyncio.create_task(self.click_loop(), name="click_loop")
