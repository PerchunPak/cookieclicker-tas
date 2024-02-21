from loguru import logger

from src.logic import AbstractLogicExtension
from src.utils import extract_number_from_string


class BuyUpgradesLogic(AbstractLogicExtension):
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
