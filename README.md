# cookieclicker-tas

[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)

[![Build Status](https://github.com/PerchunPak/cookieclicker-tas/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/PerchunPak/cookieclicker-tas/actions?query=workflow%3Atest)
[![Documentation Build Status](https://readthedocs.org/projects/cookieclicker-tas/badge/?version=latest)](https://cookieclicker-tas.readthedocs.io/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python support versions badge (from pypi)](https://img.shields.io/pypi/pyversions/cookieclicker-tas)](https://www.python.org/downloads/)

Cookieclicker speedrun script which doesn't use `Game` object.

(Written in one night (~5 hours), so don't expect this to be perfect, though I am impressed how good it is)

# WORKS ONLY WITH v2.052

Future versions may break something.

## Features

- Restarts every time with a completely new browser.
- Automatically blocks ads.
- Automatically sets the most performant settings.
- Automatically opens "Stats" page.
- Automatically renames bakery (cuz it gives an achievement so why not).
- Automatically clicks the cookie every 0.001 second.
- Automatically collects golden cookies.
- Automatically buys the most efficient buildings at the moment (cookies per second divided by cost - no the best formula, but good enough).
- Automatically buys upgrades.

## Space to improve

- Which upgrades worth buying? Currently, it buys just everything that it can afford.
- Better formula for buying buildings.
- Farm achievements to increase milk.
- Hardcoded route would be better for speedrun, this program does everything in `while True` loop.
- More features of the game (like prestige and other stuff).

## Benchmarks

TODO (maybe? if I will not be lazy)

## How to run

```bash
git clone https://github.com/PerchunPak/cookieclicker-tas.git
cd cookieclicker-tas
```

### Installing `poetry`

Next we need install `poetry` with [the recommended way](https://python-poetry.org/docs/master/#installation).

If you use Linux, use command:

```bash
curl -sSL https://install.python-poetry.org | python -
```

If you use Windows, open PowerShell with admin privileges and use:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Installing dependencies

```bash
poetry install --only main
```

### Downloading browsers

`playwright` requires browsers to be installed, so you need to run:

```bash
poetry run playwright install
```

### Running the app

And finally:

```bash
poetry run python -m src
```

### If something is not clear

You can always write to me!

## Thanks

Huge thanks to the developers, who made the game practically source-available. Writing this thing was a joy,
not as it usually is with browser-scripting.

This project was generated with [python-template](https://github.com/PerchunPak/python-template).

Also, check out https://www.youtube.com/watch?v=dQf0rQslJmE.
