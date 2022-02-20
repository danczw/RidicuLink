# LINFLUENC - social media NLP bot
 
Be active to LinkedIn using computer generated posts via gpt3:

* L - inked
* I
* N
* F - or
* L - azy
* U - sing
* E - laborate
* N - lp
* C - ode

;)

GPT3 created posts are based on other post text post scraped from LinkedIn via specified search key words. View [./scraper/](./scraper/) for webscraping code using either [Selenium Python library](https://selenium-python.readthedocs.io) for automated web browser based scraping.

View [./src/](./src/) for the bot, which calls GPT3 api ([OpenAI](https://openai.com/api/)) for post creation and LinkedIn api for publishing posts.

## Setup

Run `conda env create -f environment.yml` for Python environment for local development.

For using the webscraper with Selenium, download the [WebDriver](https://selenium-python.readthedocs.io/installation.html) of your choice and place the *[crhome/firefox/etc.]driver.exe* file in [./scraper/](./scraper/)

Download Spacey for filtering data privacey related text parts. Spacey Part of Speech tags, used for identifying privacy related data, can be found here: [POS](https://universaldependencies.org/docs/u/pos/)
