class nlp_bot():
    import json
    import math
    import nlp_bot
    import openai
    import random

    def __init__(self, api_key: str, data_json: json):
        self.openai.api_key = api_key
        self.text_data = data_json
        self.all_keys = list(self.text_data.keys())
        self.new_post = ''

    def create_post(self, perc: float, max_tokens: int, n: int, temperatur: float):
        '''
        Create new post text using GPT3 based on previously scraped post text

        Parameter
        ---------
        perc : float
            select % of texts from scrape run to be used for gpt3
            => i.e. 0.7 means 70% of text post found for the random selected
                scrape run will be used to create a new post text
        max_tokens : int
            maximum number of tokens to generate in the created post text
        n : int
            how many completions to generate for each prompt
        temperature : float
            What sampling temperature to use. Higher values means the model
                will take more risks.
            Try 0.9 for more creative applications, and 0 (argmax sampling)
                for ones with a well-defined answer
        '''
        # select random scrape run
        # (scrape run = search word and scrape datetime)
        if len(self.all_keys) == 1:
            self.key_index = 0
        else:
            key_index = self.random.randint(0, len(self.all_keys) - 1)

        random_key = self.all_keys[key_index]
        random_key_texts = self.text_data[random_key]

        # select % random text from scrape run to be used for gpt3 post text
        n_texts = self.math.floor(len(random_key_texts) * perc)
        if n_texts == 0:
            n_texts = 1
        random_texts = self.random.sample(random_key_texts, n_texts)

        print('Number of posts used for GPT3:', len(random_texts), f'(key word: {random_key})')

        # call openai api
        response = self.openai.Completion.create(engine = "text-davinci-001",
                                        prompt = random_texts,
                                        max_tokens = max_tokens,
                                        n = 2,
                                        temperature = temperatur)

        # filter for longeste reponse text and clean text
        all_resp = [i.text for i in response.choices]
        long_resp = max(all_resp, key=len)
        long_resp = long_resp.replace('  ', ' ')
        # TODO: clean-up multiple new line characters with regex

        self.new_post = long_resp