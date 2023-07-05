from datetime import datetime

import openai
import requests


class RidicuBot:
    def __init__(self, openai_key: str, linkedin_api_ulr: str, linkedin_org_id: str, linkedin_token: str):
        self.openai_key = openai_key
        self.linkedin_api_ulr = linkedin_api_ulr
        self.linkedin_org_id = linkedin_org_id
        self.linkedin_token = linkedin_token
        self.user_message = ""
        self.new_post = ""

        openai.api_key = self.openai_key

    def create_prompt_message(self, example_posts: list, prefix: str, suffix: str):
        """Create the prompt message to be used for text generation

        Args:
            example_posts (list): example posts to be used for text generation
            prefix (str): prefix for the prompt
            suffix (str): suffix for the prompt
        """
        message = f"{prefix}\n"
        for index, text in enumerate(example_posts):
            message += f"{index+1}. {text}\n"
        message += suffix

        self.user_message = message

    def oai_request(self, engine: str, max_tokens: int, n_completions: int, temperatur: float):
        """Create new text using GPT3 based on previously scraped texts

        Args:
            engine (str): OpenAI model to use for text generation
            max_tokens (int): maximum number of tokens to generate in the created text
            n_completions (int): how many completions to generate for each prompt
            temperature (float): What sampling temperature to use. Higher values means the model will take more risks.
                Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer
        """
        # call openai api
        response_oai = openai.ChatCompletion.create(
            model=engine,
            messages=[{"role": "user", "content": self.user_message}],
            max_tokens=max_tokens,
            n=n_completions,
            temperature=temperatur,
            # frequency_penalty=1.1
        )

        # extract response text
        response = response_oai.choices[0].message.content  # type: ignore
        self.new_post = response

    def post_text(self, topic: str):
        """Post text to LinkedIn

        Args:
            topic (str): topic of the post
        """
        headers = {
            "Authorization": f"Bearer {self.linkedin_token}",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": "202305",
        }

        post_body = {
            "author": f"urn:li:organization:{self.linkedin_org_id}",
            "commentary": f"{self.new_post}\n\n---\n\nAI generated content based on existing posts with topic #{topic}",
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }

        response = requests.post(self.linkedin_api_ulr, headers=headers, json=post_body)
        if response.status_code == 201:
            print(f"{datetime.now()}: Post successfully created!")
        else:
            print(f"{datetime.now()}: Post creation failed with status code {response.status_code}: {response.text}")
