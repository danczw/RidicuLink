# LINFLUENC - social media NLP bot

<img src="./assets/linfluenc.png" alt="Icon available under Reshot Free License: https://www.reshot.com/license/" width="400"/>

###### *Icon available under Reshot Free License: https://www.reshot.com/license/*

<br>

**Be active to LinkedIn using computer generated posts via gpt3:**

* **L** - inked
* **IN**
* **F** - or
* **L** - azy
* **U** - sing
* **E** - laborate
* **N** - lp
* **C** - ode

GPT3 created posts are based on other post text post from LinkedIn via specified search key words. Soon to be found here: [LinkedIn: Linfluenc](https://www.linkedin.com/company/linfluenc/)

View [./src/bot_main.py](./src/bot_main.py) for the bot, which calls GPT3 api ([OpenAI](https://openai.com/api/)) for post creation and LinkedIn api for publishing posts. View [./src/scraper_main.py](./src/scraper_main.py) for webscraping LinkedIn using [Selenium Python library](https://selenium-python.readthedocs.io) - an automated web browser scraping tool.

<br>

Setup
=====

Run `conda env create -f environment.yml` for Python environment for local development.

For using the webscraper with Selenium, download the [WebDriver](https://selenium-python.readthedocs.io/installation.html) of your choice and place the *[chrome/firefox/etc.]driver.exe* file in [./src/](./src/)

Download Spacey for filtering data privacey related text parts. Spacey Part of Speech tags, used for identifying privacy related data, can be found here: [POS](https://universaldependencies.org/docs/u/pos/)
