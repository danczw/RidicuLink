import os

import yaml
from database import PostDB
from dotenv import load_dotenv

import scraper as scrp


def main():
    # get parameters from config yaml file
    config_params = yaml.safe_load(open("./conf/config.yml"))

    # load env variables
    load_dotenv()
    USER = os.getenv("LINKEDIN_USER")
    PW = os.getenv("LINKEDIN_PASSWORD")
    # check if env variables are set
    if USER is None or PW is None:
        raise ValueError("Please set environment variables LINKEDIN_USER and LINKEDIN_PASSWORD")

    # login to LinkedIn
    linkedin_scraper = scrp.scraper(
        driver_type=config_params["selenium_driver_type"],
        driver_path=config_params["selenium_driver_path"],
        login_url=config_params["linkedin_login_url"],
        search_root_url=config_params["linkedin_search_root_url"],
    )
    linkedin_scraper.login(USER, PW)

    # tokens for data privacy filter
    tokens = ["PROPN"]  # PROPN = proper noun

    # initialize database
    db = PostDB(db_name=config_params["db_name"], table_name=config_params["db_table_name"])
    db.create_table(drop=True)

    for word in config_params["search_topics"]:
        # reset previous results of loop
        linkedin_scraper.reset_results()

        # execute crawling
        linkedin_scraper.get_text(word.lower(), config_params["text_element_class"], 5)
        linkedin_scraper.clean_texts(tokens)
        linkedin_scraper.keep_language_texts("en")

        n_texts = len(linkedin_scraper.all_texts_clean)
        print(f'>>> scraper successful: found {n_texts} texts for "{word}" <<<')

        # save results into database
        for text in linkedin_scraper.all_texts_clean:
            db.insert(word, text)

    # close connection
    linkedin_scraper.close_connection()


if __name__ == "__main__":
    main()
