import asyncio

import typer
from loguru import logger

import src.logging
from src import utils
from src.logic import Logic


@utils.async_to_sync
async def main(
    logging_level: src.logging.LoggingLevel = "info",  # type: ignore[assignment] # typer magic
) -> None:
    src.logging.setup_logging(logging_level)
    logger.info("Hello World!")

    async with Logic.init() as logic:
        await logic.remove_ads()
        await logic.set_settings()
        await logic.open_stats_page()
        await logic.rename_bakery()
        await logic.click_cookie_in_the_background()
        logger.success("All setup done! Starting to run infinite loop!")

        while True:
            await logic.collect_golden_cookies()
            await logic.update_balance()
            await logic.buy_buildings()
            await logic.buy_upgrades()
            await asyncio.sleep(1)


if __name__ == "__main__":
    typer.run(main)
