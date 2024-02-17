import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

import aiohttp
from loguru import logger
from playwright.async_api import BrowserContext, async_playwright

from src.utils import BASE_DIR


async def download_adblock() -> Path:
    adblock_dir = BASE_DIR / "data" / "adblock"
    adblock_dir.mkdir(exist_ok=True)
    archive_path = adblock_dir / "uBlock0.chromium.zip"
    output_path = adblock_dir / "uBlock0.chromium"

    if output_path.exists():
        logger.info("Adblock is already downloaded.")
        return output_path

    async with aiohttp.ClientSession() as session:
        async with session.get("https://github.com/gorhill/uBlock/releases/latest") as resp:
            version = resp.url.parts[-1]
        logger.info(f"Latest uBlock version is {version}. Downloading...")
        async with session.get(
            f"https://github.com/gorhill/uBlock/releases/latest/download/uBlock0_{version}.chromium.zip"
        ) as resp:
            with archive_path.open("wb") as f:  # this is pre-start of program, we can allow sync code
                f.write(await resp.read())

        with zipfile.ZipFile(str(archive_path), "r") as zip_ref:
            zip_ref.extractall(
                str(output_path.parent)
            )  # inside archive is a folder, so we extract it to the parent folder
        logger.success("uBlock is downloaded.")

    return output_path


@asynccontextmanager
async def start_browser() -> BrowserContext:
    adblock_path = await download_adblock()

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="data/browser",
            headless=False,
            args=[
                f"--disable-extensions-except={adblock_path}",
                f"--load-extension={adblock_path}",
            ],
        )
        page = browser.pages[0]

        logger.info("Waiting for uBlock Origin to initialise...")
        await page.wait_for_timeout(1000)

        await page.goto("https://orteil.dashnet.org/cookieclicker/")
        yield browser
        await browser.close()
