from blob import blob
from dotenv import load_dotenv
import os
import scraper as scrp

# webdriver path and file name
chrome_driver_path = './scraper/chromedriver.exe' # TODO: change to your path

# load env variables
load_dotenv()
USER = os.getenv('LINKEDIN_USER')
PW = os.getenv('LINKEDIN_PASSWORD')
BLOB_CON_STRING = os.getenv('BLOB_CON_STRING')

# login, search url as well as search words and text DOM element
linkedin_login_url = 'https://www.linkedin.com/login'
linkedin_search_root_url = 'https://www.linkedin.com/feed/hashtag/'
text_element_class = 'feed-shared-update-v2__commentary'
# TODO: update search words       
search_words = ['beavoicenotanecho', 'linkedin', 'thoughtleadership', 'thoughtleader']

# tokens for data privacy filter
tokens = ['PROPN'] # PROPN = proper noun

# Azure Blob Storage container name
container_name = 'linfluenc-parsed-texts'

# blob name
file_name = 'parsed_text.json'

# login to LinkedIn
linkedin_scraper = scrp.scraper(chrome_driver_path,
                                linkedin_login_url,
                                linkedin_search_root_url)
linkedin_scraper.login(USER, PW)

# init azure connections
azure_blob = blob(BLOB_CON_STRING, container_name, file_name)

for word in search_words:
    # reset previous results of loop
    linkedin_scraper.reset_results()

    # execute crawling
    linkedin_scraper.get_text(word.lower(), text_element_class, 10)
    linkedin_scraper.clean_texts(tokens)
    linkedin_scraper.keep_language_texts('en')

    n_texts = len(linkedin_scraper.all_texts_clean)
    print(f'>>> scraper successful: found {n_texts} texts for "{word}" <<<')

    # upload new data
    azure_blob.upload_texts(linkedin_scraper.all_texts_clean,
                            linkedin_scraper.search_word)

# close connection
linkedin_scraper.close_connection()