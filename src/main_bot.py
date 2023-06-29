import os
import random

import yaml
from dotenv import load_dotenv
from utils.bot import RidicuBot
from utils.database import PostDB


def main():
    # get parameters from config yaml file
    config_params = yaml.safe_load(open("./conf/config.yml", "r"))

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

    # initialize bot
    bot = RidicuBot(
        openai_key=OPENAI_API_KEY.strip('"'),
        linkedin_api_ulr=config_params["linkedin_post_url"],
        linkedin_org_id=LINKEDIN_ORG_ID.strip('"'),
        linkedin_token=LINKEDIN_ACCESS_TOKEN.strip('"'),
    )

    # get all topics and select a random one
    topic = random.choice(db.get_topics())[0]

    # get all texts for the random topic
    texts = db.get_texts(topic)
    if len(texts) == 0:
        raise ValueError(f"No texts found for topic {topic}")
    # shuffle texts and select the first 3
    random.shuffle(texts)
    texts = texts[:3]

    # prepare user message for api call
    bot.create_prompt_message(
        example_posts=texts, prefix=config_params["oai_prompt_prefix"], suffix=config_params["oai_prompt_suffix"]
    )

    # create text
    bot.oai_request(
        engine=config_params["oai_model"],
        max_tokens=random.randint(config_params["oai_max_tokens"] - 50, config_params["oai_max_tokens"] + 50),
        n_completions=config_params["oai_n_completions"],
        temperatur=random.normalvariate(config_params["oai_temperature"], 0.1),
    )
    # print(bot.new_post)

    # post text
    bot.post_text(topic=topic)


if __name__ == "__main__":
    main()
