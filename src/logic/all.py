import asyncio

from loguru import logger

from src.logic.buy_buildings import BuyBuildingsLogic
from src.logic.buy_upgrades import BuyUpgradesLogic
from src.utils import extract_number_from_string


class AllLogic(BuyBuildingsLogic, BuyUpgradesLogic):
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

        produced_per_last_second = self.balance - self.old_balance
        if produced_per_last_second > 0:  # if we bought something, this might be negative
            self.produced_per_last_second = produced_per_last_second

        self.old_balance = self.balance

    async def collect_golden_cookies(self) -> None:
        cookies = await self.page.query_selector_all("#shimmers > .shimmer")
        for cookie in cookies:
            await cookie.click()
