import abc
import typing as t
from contextlib import asynccontextmanager

from loguru import logger
from playwright.async_api import Browser, Page, async_playwright


class AbstractLogicExtension(abc.ABC):
    def __init__(self, browser: Browser, page: Page) -> None:
        self.browser = browser
        self.page = page

        self.balance = 0
        self.old_balance = 0
        self.produced_per_last_second = 0

    @classmethod
    @asynccontextmanager
    async def init(cls) -> t.AsyncIterator[t.Self]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
            page = await browser.new_page()
            logger.info("Navigating to page...")
            await page.goto("https://orteil.dashnet.org/cookieclicker/", wait_until="domcontentloaded")
            await page.evaluate("window.localStorageSet('CookieClickerLang', 'EN');")  # set language
            logger.info("Waiting for page to load...")
            await page.wait_for_load_state("networkidle")

            logger.info("Executing our steps...")
            yield cls(browser, page)

            await browser.close()
