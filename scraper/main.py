import os

from dotenv import load_dotenv

import scraper as scrp


def main():
    # webdriver path and type: [chrome, firefox, edge]
    # TODO: change according to your setup
    selenium_driver_type = "chrome"
    selenium_driver_path = "./scraper/chromedriver"
    # TODO: optional, only needed if you want to use a specific browser binary, set to "" otherwise
    binary_location = ""

    # TODO: update search words
    search_words = [
        "ChatGPT",
    ]

    # load env variables
    load_dotenv()
    USER = os.getenv("LINKEDIN_USER")
    PW = os.getenv("LINKEDIN_PASSWORD")
    # check if env variables are set
    if USER is None or PW is None:
        raise ValueError("Please set environment variables LINKEDIN_USER and LINKEDIN_PASSWORD")

    # login, search url as well as search words and text DOM element
    linkedin_login_url = "https://www.linkedin.com/login"
    linkedin_search_root_url = "https://www.linkedin.com/feed/hashtag/"
    text_element_class = "feed-shared-update-v2__commentary"

    # login to LinkedIn
    linkedin_scraper = scrp.scraper(
        driver_type=selenium_driver_type,
        driver_path=selenium_driver_path,
        login_url=linkedin_login_url,
        search_root_url=linkedin_search_root_url,
        browser_binary_location=binary_location,
    )
    linkedin_scraper.login(USER, PW)

    # tokens for data privacy filter
    tokens = ["PROPN"]  # PROPN = proper noun

    for word in search_words:
        # reset previous results of loop
        linkedin_scraper.reset_results()

        # execute crawling
        linkedin_scraper.get_text(word.lower(), text_element_class, 5)
        linkedin_scraper.clean_texts(tokens)
        linkedin_scraper.keep_language_texts("en")

        n_texts = len(linkedin_scraper.all_texts_clean)
        print(f'>>> scraper successful: found {n_texts} texts for "{word}" <<<')

        # save results
        # TODO: implement

    # close connection
    linkedin_scraper.close_connection()


if __name__ == "__main__":
    main()
