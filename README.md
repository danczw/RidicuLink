# LINFLUENC - social media NLP bot

<img src="./assets/linfluenc.png" alt="Icon available under Reshot Free License: https://www.reshot.com/license/" width="300"/>

###### *Icon available under Reshot Free License: https://www.reshot.com/license/*

<br>

## **L**inked**IN**  **F**or  **L**azy  **U**sing  **E**laborate  **N**lp  **C**ode

**Be active to LinkedIn using computer generated posts via gpt3**

<br>

Create finctional GPT3 based posts based on existing text post from LinkedIn via specified search key words. Live bot can be found here: [LinkedIn: Linfluenc](https://www.linkedin.com/company/linfluenc/)

View [./bot](./bot) for the posting bot, which calls GPT3 API for post creation and LinkedIn API for publishing posts - automated using Azure Functions.
View [./scraper](./scraper) for webscraping real LinkedIn posts as basis for the bot using Selenium Python library - an automated web browser scraping tool.

<br>

Setup - Scraper
=====

[./scraper](./scraper) can be used to scrape LinkedIn posts using [Selenium Python library](https://selenium-python.readthedocs.io) and saving results in an Azure blob storage instance.

### Local development

Run `conda env create -f environment.yml` for Python environment for local development of the webscraper.

For using the webscraper with Selenium, download the [WebDriver](https://selenium-python.readthedocs.io/installation.html) of your choice and place the *[chrome/firefox/etc.]driver.exe* file in [./scraper](./scraper/)

Download Spacey for filtering data privacey related text parts. Spacey Part of Speech tags, used for identifying privacy related data, can be found here: [POS](https://universaldependencies.org/docs/u/pos/)

- [./scraper/main.py](./scraper/main.py) - main file for executing scraper
- [./scraper/blob.py](./scraper/blob.py) - Azure blob storage class setup
- [./scraper/scraper.py](./scraper/scraper.py) - Selenium webscraper class setup

Make sure to include *LINKEDIN_USER* and *LINKEDIN_PASSWORD* variables in your local `.env` file for successful scraping, as well as Azure blob storage connection string as *BLOB_CON_STRING*.

Results are saved as a json file in the Azure blob storage. Due to the browser driver needed for Selenium, the scraping script can currently be only run locally.

<br>

Setup - bot
=====

[./bot](./bot) can be used to publish GPT3 ([OpenAI](https://openai.com/api/)) based posts to LinkedIn, based on real LinkedIn text posts previously saved in an Azure blob storage instance. The [Linfluenc bot (LinkedIn)](https://www.linkedin.com/company/linfluenc/) is automated using [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-overview). Posts are created and distributed via a LinkedIn organization page. View [LinkedIn Docs](https://developer.linkedin.com/product-catalog/consumer) for more details on how to share content via the API.

## Local development

Create virtual env with pip in the root azure function folder ([./bot](./bot)) based on `requirements.txt`:

- `python -m venv .venv`
- `source .venv/Scripts/activate`
- `pip install -r requirements.txt`

Test the function locally: `func host start`

- [./bot/linfluenc_time_trigger/__init__.py](./bot/linfluenc_time_trigger/__init__.py) - main file for running bot Azure function
- [./bot/linfluenc_time_trigger/blob.py](./bot/linfluenc_time_trigger/blob.py) - Azure blob storage class setup
- [./bot/linfluenc_time_trigger/bot_nlp.py](./bot/linfluenc_time_trigger/bot_nlp.py) - OpenAI post creation class setup

Make sure to create a *local.settings.json* as per the example: [local.settings.json](./bot/example.local.settings.json). Including your *OPENAI_API_KEY*, LinkedIn organization ID (*LINKEDIN_ORG_ID*) and respective access token (*LINKEDIN_ACCESS_TOKEN*) for sharing the posts as well as the Azure blob storage connection string (*BLOB_CON_STRING*).

Change the bot post schedule via the time trigger CRON exporession in the [bot/linfluenc_time_trigger/function.json](bot/linfluenc_time_trigger/function.json) file.

## TimerTrigger - Python

The `TimerTrigger` makes it incredibly easy to have your functions executed on a schedule. This sample demonstrates a simple use case of calling your function every 5 minutes.

For a `TimerTrigger` to work, you provide a schedule in the form of a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression). A cron expression is a string with 6 separate expressions which represent a given schedule via patterns. The pattern we use to represent every 5 minutes is `0 */5 * * * *`. This, in plain text, means: "When seconds is equal to 0, minutes is divisible by 5, for any hour, day of the month, month, day of the week, or year".
