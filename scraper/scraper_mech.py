from bs4 import BeautifulSoup
from dotenv import load_dotenv
import mechanize
import os
import re

# load env variables
load_dotenv()
USER = os.getenv('LINKEDIN_USER')
PW = os.getenv('LINKEDIN_PASSWORD')

# login, search url as well as search words and post text DOM element
linkedin_login_url = 'https://www.linkedin.com/login'
linkedin_search_root_url = 'https://www.linkedin.com/search/results/content/?keywords='       
search_words = ['forbes30under30']
post_element_class = 'feed-shared-update-v2__commentary'

# init browser
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)

# open login page and retrieve login form
response = br.open(linkedin_login_url)
br.form = list(br.forms())[1]

# enter user name and password
username = br.form.find_control('session_key')
username.value = USER
password = br.form.find_control('session_password')
password.value = PW
response = br.submit()

response = br.open(linkedin_search_root_url + search_words[0])

test = response.read()
test_dec = test.decode("utf-8")

import json
with open('parsed_text.json', 'w') as file:
    json.dump(test_dec, file, indent = 4)

# regex = r"\"USER_LOCALE\",\"text\":\"(.*?)\",\"attributesV2\""
# matches = re.finditer(regex, (test_dec), re.DOTALL)
# for match in matches:
#     print(match.group())