import asyncio
import typing as t
from contextlib import asynccontextmanager

from loguru import logger
from playwright.async_api import Browser, Page, async_playwright

from src.building import Building
from src.utils import extract_number_from_string


class Logic:
    def __init__(self, browser: Browser, page: Page) -> None:
        self.browser = browser
        self.page = page

        self.balance = 0

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

    async def remove_ads(self) -> None:
        logger.info("Removing ads...")
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
        logger.info("Setting settings...")
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

    async def open_stats_page(self) -> None:
        logger.info("Opening stats page...")
        await self.page.click("#statsButton")

    async def rename_bakery(self) -> None:
        logger.info("Renaming bakery...")
        await self.page.click("#bakeryName")
        await self.page.fill("#bakeryNameInput", "Perchun's TAS")
        await self.page.click("#promptOption0")

    async def click_cookie_loop(self) -> None:
        while True:
            try:
                await self.page.click("#bigCookie")
            except Exception as e:
                logger.exception(e)
            else:
                await asyncio.sleep(0.0001)

    async def click_cookie_in_the_background(self) -> None:
        logger.info("Starting clicking cookie in the background...")
        asyncio.create_task(self.click_cookie_loop())

    async def update_balance(self) -> None:
        element = await self.page.query_selector("#cookies > span.monospace")
        assert element is not None
        self.balance = int(extract_number_from_string(await element.inner_text()))

    async def _get_buyable_buildings(self) -> list[Building]:
        buildings = await self.page.query_selector_all("#products > .product.unlocked")

        to_return: list[Building] = []
        for building_html in buildings:
            id = await building_html.get_attribute("id")
            assert id is not None
            to_return.append(await Building.create(self.page, id))
        return to_return

    def _get_the_best_thing_to_buy(self, buildings: list[Building]) -> Building:
        if buildings[0].produces is None:
            return buildings[0]

        return max(enumerate(buildings), key=lambda x: x[1].produces or buildings[x[0] - 1].produces * 10)[1]  # type: ignore[operator] # it just cant

    async def buy_buildings(self) -> None:
        buildings = await self._get_buyable_buildings()
        if not buildings:
            return

        best_building = self._get_the_best_thing_to_buy(buildings)
        if best_building.costs <= self.balance:
            logger.info(f"Buying building number {best_building.id} for {best_building.costs} cookies")
            await self.page.click(f"#{best_building.html_id}")

    async def buy_upgrades(self) -> None:
        upgrade_elements = await self.page.query_selector_all("#upgrades > *.upgrade.enabled")
        for upgrade in upgrade_elements:
            upgrade_id = await upgrade.get_attribute("id")
            assert upgrade_id is not None

            await self.page.locator("#" + upgrade_id).hover()
            price_as_element = await self.page.query_selector("#tooltipCrate > div > span.price")

            if price_as_element is None:
                logger.error(f"Could not find price for upgrade {upgrade_id}")
                continue

            price = extract_number_from_string(await price_as_element.inner_text())
            if price <= self.balance:
                logger.info(f"Buying upgrade {upgrade_id} for {price} cookies")
                await self.page.click(f"#{upgrade_id}")

    async def collect_golden_cookies(self) -> None:
        cookies = await self.page.query_selector_all("#shimmers > .shimmer")
        for cookie in cookies:
            await cookie.click()
