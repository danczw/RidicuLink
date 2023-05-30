import openai


class RidicuBot:
    def __init__(self, openai_key: str, linkedin_org_id: str, linkedin_token: str):
        self.openai_key = openai_key
        self.linkedin_org_id = linkedin_org_id
        self.linkedin_token = linkedin_token
        self.new_post = ""

        openai.api_key = self.openai_key

    def create_text(self, engine: str, max_tokens: int, n_completions: int, temperatur: float, prompt: str):
        """Create new text using GPT3 based on previously scraped texts

        Args:
            engine (str): OpenAI model to use for text generation
            max_tokens (int): maximum number of tokens to generate in the created text
            n_completions (int): how many completions to generate for each prompt
            temperature (float): What sampling temperature to use. Higher values means the model will take more risks.
                Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer
            prompt (str): prompt for the text generation
        """
        # call openai api
        response = openai.Completion.create(
            engine=engine, prompt=prompt, max_tokens=max_tokens, n=n_completions, temperature=temperatur
        )

        self.new_post = response
