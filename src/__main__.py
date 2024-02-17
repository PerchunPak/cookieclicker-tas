import asyncio
import typing as t

import typer
from loguru import logger

import src.logging
from src import utils
from src.logic import Logic


async def _background_wrapper(func: t.Callable[..., t.Awaitable[None]], sleep_time: float) -> t.Never:  # type: ignore[misc] # Explicit "Any" is not allowed
    while True:
        try:
            await func()
        except Exception as e:
            logger.exception(e)
        else:
            await asyncio.sleep(sleep_time)


@utils.async_to_sync
async def main(
    logging_level: src.logging.LoggingLevel = "info",  # type: ignore[assignment] # typer magic
) -> None:
    src.logging.setup_logging(logging_level)
    logger.info("Hello World!")

    async with Logic.init() as logic:
        await logic.remove_ads()
        await logic.set_settings()
        await logic.rename_bakery()

        asyncio.create_task(_background_wrapper(logic.click_cookie_background, 0.001))
        asyncio.create_task(_background_wrapper(logic.get_balance_background, 1))
        asyncio.create_task(_background_wrapper(logic.buy_buildings_background, 3))

        await logic.page.wait_for_timeout(500000)


if __name__ == "__main__":
    typer.run(main)
