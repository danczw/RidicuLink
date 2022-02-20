from dotenv import load_dotenv
import os
import scraper_sel as scrp

# webdriver path and file name
chrome_driver_path = './scraper/chromedriver.exe'
# output data path
data_path = './data/'

# load env variables
load_dotenv()
USER = os.getenv('LINKEDIN_USER')
PW = os.getenv('LINKEDIN_PASSWORD')

# login, search url as well as search words and post text DOM element
linkedin_login_url = 'https://www.linkedin.com/login'
linkedin_search_root_url = 'https://www.linkedin.com/search/results/content/?keywords='       
search_words = ['forbes30under30', 'Marketing', 'ceolunch']
post_element_class = 'feed-shared-update-v2__commentary'

# tokens for data privacy filter
tokens = ['PROPN'] # PROPN = proper noun

# login to LinkedIn
linkedin_scraper = scrp.scraper(chrome_driver_path,
                                linkedin_login_url,
                                linkedin_search_root_url)
linkedin_scraper.login(USER, PW)

for word in search_words:
    # reset previous results of loop
    linkedin_scraper.reset_results()

    # execute crawling
    linkedin_scraper.get_post_text(word, post_element_class, 10)
    linkedin_scraper.clean_texts(tokens)
    linkedin_scraper.keep_language_texts('en')
    linkedin_scraper.save_clean_text(data_path)
    
    n_posts = len(linkedin_scraper.all_texts_clean)
    print(f'>>> scraper successful: found {n_posts} posts for "{word}" <<<')