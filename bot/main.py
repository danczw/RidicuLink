import os
import random

import yaml
from dotenv import load_dotenv

from bot.bot import RidicuBot
from scraper.database import PostDB


def main():
    # get parameters from config yaml file
    config_params = yaml.safe_load(open("./conf/config.yml"))

    # load env variables
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LINKEDIN_ORG_ID = os.getenv("LINKEDIN_ORG_ID")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    # check if env variables are set
    if OPENAI_API_KEY is None or LINKEDIN_ORG_ID is None or LINKEDIN_ACCESS_TOKEN is None:
        raise ValueError("Please set environment variables OPENAI_API_KEY, LINKEDIN_ORG_ID and LINKEDIN_ACCESS_TOKEN")

    # initialize database
    db = PostDB(db_name=config_params["db_name"], table_name=config_params["db_table_name"])

    # get all topics and select a random one
    topics = db.get_topics()
    rand_topic = random.choice(topics)[0]

    # get all texts for the random topic
    texts = db.get_texts(rand_topic)
    if len(texts) == 0:
        raise ValueError(f"No texts found for topic {rand_topic}")
    # shuffle texts and select the first 3
    random.shuffle(texts)
    texts = texts[:3]

    # create prompt
    prompt = config_params["oai_prompt_prefix"]
    for index, text in enumerate(texts):
        prompt += f"{index+1}. {text[0]}\n"

    # initialize bot
    bot = RidicuBot(
        openai_key=OPENAI_API_KEY,
        linkedin_org_id=LINKEDIN_ORG_ID,
        linkedin_token=LINKEDIN_ACCESS_TOKEN,
    )

    # create text
    bot.create_text(
        prompt=prompt,
        engine=config_params["oai_model"],
        max_tokens=config_params["oai_max_tokens"],
        n_completions=config_params["oai_n_completions"],
        temperatur=config_params["oai_temperature"],
    )


if __name__ == "__main__":
    main()
