from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import spacy
import time

#-----SCRAPING-----------------------------------------------------------------#

# init chrome webdriver
driver_path = 'webdriver/chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)

# get LinkedIn login data
load_dotenv()
USER = os.getenv('LINKEDIN_USER')
PASSWORD = os.getenv('LINKEDIN_PASSWORD')

# login to LinkedIn
driver.get('https://www.linkedin.com/login')
time.sleep(3)
driver.find_element_by_id('username').send_keys(USER)
driver.find_element_by_id('password').send_keys(PASSWORD)
driver.find_element_by_id('password').send_keys(Keys.RETURN)

# set hashtags to scrape post text from
hashtags = ['forbes30under30']
content_root_path = 'https://www.linkedin.com/search/results/content/?keywords='

all_text = []

# iterate through hashtags to get posts
for word in hashtags:
    time.sleep(3)

    # get hashtag search results
    driver.get(content_root_path + word)
    time.sleep(3)

    for i in range(2):
        # get a list of all text elements from post by HTML element class name
        all_posts = driver.find_elements_by_class_name(
            'feed-shared-update-v2__commentary')
        
        # executes JavaScript to scroll the div into view
        driver.execute_script("arguments[0].scrollIntoView();", all_posts[-1])
        time.sleep(3)

    # itereate through posts
    for post in all_posts:
        # get post text
        all_text.append(post.text)


#-----CLEANING-----------------------------------------------------------------#

# load nlp model for cleanin data privacy related text content
nlp = spacy.load('nl_core_news_sm')

all_text_clean = []

# iterate through previously scraped texts
for text in all_text:
    # parse text to list of tokens
    doc = nlp(text)

    filtered_text = ''
    for token in doc:
        # replace word if proper noun, noun, or number
        if token.pos_ in ['PROPN']:
            new_token = f" <{token.ent_type_}>"
        else:
            new_token = f' {token.text}'
        
        # concatenate
        filtered_text += new_token
    
    # remove leading space
    filtered_text = filtered_text[1:]
    
    print(filtered_text)
