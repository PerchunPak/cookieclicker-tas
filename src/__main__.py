import typer, typing as t
from loguru import logger

import src.logging
from src import utils


@utils.async_to_sync
async def main(
    logging_level: src.logging.LoggingLevel = "info",
) -> None:
    src.logging.setup_logging(logging_level)
    logger.info("Hello World!")

    # start app here


if __name__ == "__main__":
    typer.run(main)
