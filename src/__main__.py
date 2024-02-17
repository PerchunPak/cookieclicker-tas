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
        page = logic.browser.pages[0]
        await page.wait_for_timeout(500000)


if __name__ == "__main__":
    typer.run(main)
