
class scraper:
    from datetime import datetime
    import json
    import langdetect
    import os
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import spacy
    import time

    def __init__(self, chrome_driver_path, login_url, search_root_url):        
        self.driver = self.webdriver.Chrome(executable_path=chrome_driver_path)
        self.login_url = login_url
        self.search_root_url = search_root_url
        self.search_word = ''
        self.all_posts = []
        self.all_texts = []
        self.all_texts_clean = []
    
    def login(self, user: str, password: str):
        '''
        Login to url with provided user name and password

        Parameter
        ---------
        user : str
            user name as needed for login
        password : str
            password as needed for login
        '''
        self.driver.get(self.login_url)
        self.time.sleep(3)
        self.driver.find_element_by_id('username').send_keys(user)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password').send_keys(self.Keys.RETURN)
    
    
    def get_post_text(self, search_word: str, dom_element: str, iterations: int):
        '''
        Scrape LinkedIn post text of posts found by a specified word

        Parameter
        ---------
        website : str
            root url for searching posts by word
        search_root_url : str
            word to search posts for
        dom_element : str
            DOM element in LinkedIn containing post text
        iterations : int
            number of iterations to scroll though posts found
            initially, only first few search results are loaded and found by selenium
            the higher the iteration, the more post can potentially be scraped
        '''
        self.search_word = search_word
        self.time.sleep(3)
        self.driver.get(self.search_root_url + search_word)
        self.time.sleep(3)

        # iterate through posts to load more
        for i in range(iterations):
        # get a list of all text elements from post by HTML element class name
            self.all_posts = self.driver.find_elements_by_class_name(dom_element)
        
            # executes JavaScript to scroll the last found div into view
            self.driver.execute_script("arguments[0].scrollIntoView();", self.all_posts[-1])
            self.time.sleep(1)

        # itereate through posts to get post text
        for post in self.all_posts:
            # get post text
            self.all_texts.append(post.text)
    
    def clean_texts(self, tokens: list):
        '''
        Clean text of data privacy related content (e.g. names)

        Parameter
        ---------
        tokens : list[str]
            list of str tokens to be replaced
            spacey part of speech tags, used for identifying privacy related
                data, found here: https://universaldependencies.org/docs/u/pos/
        '''
        # load nlp model for cleanin data privacy related text content
        nlp = self.spacy.load('nl_core_news_sm')

        # iterate through previously scraped texts
        for text in self.all_texts:
            # parse text to list of tokens
            doc = nlp(text)

            filtered_text = ''
            for token in doc:
                # replace word if word classified as specific tokens
                # TODO: review and expand
                if token.pos_ in tokens:
                    # new_token = f' <{token.ent_type_}>'
                    new_token = ''
                else:
                    new_token = f' {token.text}'
                
                # concatenate
                filtered_text += new_token
            
            # remove leading space and new lines
            filtered_text = filtered_text[1:]
            filtered_text = filtered_text.replace('\n', '')

            self.all_texts_clean.append(filtered_text)
            # print(filtered_text)

    def keep_language_texts(self, lang='en'):
        '''
        Keep all texts from cleaned texts wich are the specified language
        
        Parameter
        ---------
        lang : str
            language which texts to keep, default is english 
        '''
        all_texts = self.all_texts_clean
        all_texts_filtered = []

        for text in all_texts:
            detected_lang = self.langdetect.detect(text)
            
            if detected_lang == lang:
                all_texts_filtered.append(text)
        
        self.all_texts_clean = all_texts_filtered

    def save_clean_text(self, file_path: str):
        '''
        Translate list into json and save file named after
            search word and run date

        Parameter
        ---------
        file_path : str
            path to save JSON to
        '''
        new_data_key = self.search_word + \
                       '_' + \
                       self.datetime.now().strftime("%Y%m%d-%H%M%S")
        new_data_dict = {}
        new_data_dict[new_data_key] = self.all_texts_clean

        if not self.os.path.isfile(file_path + 'parsed_text.json'):
            # save data
            with open(file_path + 'parsed_text.json', 'w') as file:
                self.json.dump(new_data_dict, file, indent = 4)
        else:
            # save data
            with open(file_path + 'parsed_text.json', 'r+') as file:
                existing_data = self.json.load(file)
                existing_data.update(new_data_dict)
                file.seek(0)
                self.json.dump(existing_data, file, indent = 4)

    def reset_results(self):
        '''
        Reset crawled results saved in current class object
        '''
        self.search_word = ''
        self.all_posts = []
        self.all_texts = []
        self.all_texts_clean = []