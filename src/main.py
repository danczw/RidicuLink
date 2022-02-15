from dotenv import load_dotenv
import json
import openai
import os

# load env variables and set api key
load_dotenv()
OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPEN_AI_KEY

# load data
file_path = './data/'
file_name = 'parsed_text.json'
with open(file_path + file_name, 'r') as file:
    text_data = json.load(file)

keys = list(text_data.keys())

# call openai api
response = openai.Completion.create(engine="text-davinci-001", prompt=text_data[keys[0]][0], max_tokens=20)
print(response)