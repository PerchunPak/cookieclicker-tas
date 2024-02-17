import asyncio

from loguru import logger

from src import utils


async def main() -> None:
    utils.setup_logging()
    logger.info("Hello World!")

    # start app here


if __name__ == "__main__":
    asyncio.run(main())
