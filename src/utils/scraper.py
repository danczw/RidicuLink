import os
import time

import spacy
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Scraper:
    def __init__(
        self,
        driver_type: str,
        driver_path: str,
        login_url: str,
        search_root_url: str,
    ):
        self.driver = self.get_web_driver(driver_type=driver_type, driver_path=driver_path)
        self.login_url = login_url
        self.search_root_url = search_root_url
        self.search_word = ""
        self.all_posts = []
        self.all_texts = []
        self.all_texts_clean = []

    def get_web_driver(self, driver_type: str, driver_path: str):
        """Get the web driver for selenium

        Args:
            driver_type (str): type of driver: [chrome, firefox, edge]
            driver_path (str): path to the driver
            binary_location (str): path to the browser binary
            browser_binary_location (str, optional): path to the browser binary. Defaults to "".
        """
        # check if file exists
        if not os.path.isfile(driver_path):
            raise ValueError(f"driver_path {driver_path} does not exist, please check if file exists")

        # check if driver type is supported and return driver
        match driver_type:
            case "chrome":
                return webdriver.Chrome(executable_path=driver_path)
            case "firefox":
                return webdriver.Firefox(executable_path=driver_path)
            case "edge":
                return webdriver.Edge(executable_path=driver_path)
            case _:
                raise ValueError(f"driver_type {driver_type} not supported, please choose from [chrome, firefox, edge]")

    def login(self, user: str, password: str):
        """Login to url with provided user name and password

        Args:
            user (str): user name as needed for login
            password (str): password as needed for login
        """
        try:
            self.driver.get(self.login_url)
            time.sleep(3)
            self.driver.find_element(By.ID, "username").send_keys(user)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Login failed: {e}")

    def get_text(self, search_word: str, dom_element: str, iterations: int):
        """Scrape LinkedIn texts of posts found by a specified word

        Args:
            search_word (str): Keyword / hashtag to search posts for
            dom_element (str): DOM element in LinkedIn containing post text
            iterations (int): Number of iterations to scroll though posts found. Initially, only first few search
                results are loaded by LinkedIn and found by selenium. The higher the iteration, the more post texts
                can potentially be scraped.
        """
        self.search_word = search_word
        time.sleep(3)
        self.driver.get(self.search_root_url + search_word)
        time.sleep(3)

        # iterate through posts to load more
        for i in range(iterations):
            # get a list of all text elements from post by HTML element class name
            self.all_posts = self.driver.find_elements(By.CLASS_NAME, dom_element)

            # executes JavaScript to scroll the last found div into view
            self.driver.execute_script("arguments[0].scrollIntoView();", self.all_posts[-1])
            time.sleep(1)

        # itereate through posts to get post text
        for post in self.all_posts:
            # get post text
            self.all_texts.append(post.text)

    def clean_texts(self, tokens: list):
        """Clean text of data privacy related content (e.g. names)

        Args:
            tokens (list): List of str tokens to be replaced. Spacey part of speech tags, used for identifying privacy
                related data, found here: https://universaldependencies.org/docs/u/pos/
        """
        # load nlp model for cleanin data privacy related text content
        nlp = spacy.load("en_core_web_sm")

        # iterate through previously scraped texts
        for text in self.all_texts:
            # parse text to list of tokens
            doc = nlp(text)

            filtered_text = ""
            for token in doc:
                # replace word if word classified as specific tokens
                if token.pos_ in tokens:
                    # new_token = f' <{token.ent_type_}>'
                    new_token = ""
                else:
                    new_token = f" {token.text}"

                # concatenate
                filtered_text += new_token

            # remove leading space and new lines
            filtered_text = filtered_text.replace("\n", "").strip()
            self.all_texts_clean.append(filtered_text)

    def keep_language_texts(self, lang: str = "en"):
        """Keep all texts from cleaned texts which are the specified language

        Args:
            lang (str, optional): language which texts to keep, default is english
        """
        all_texts = self.all_texts_clean
        all_texts_filtered = []

        for text in all_texts:
            try:
                # detect language of text
                lang = detect(text)

                # keep text if language is english
                if lang == "en":
                    all_texts_filtered.append(text)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Text: {text}\n")

        self.all_texts_clean = all_texts_filtered

    def reset_results(self):
        """Reset crawled results saved in current class object"""
        self.search_word = ""
        self.all_posts = []
        self.all_texts = []
        self.all_texts_clean = []

    def close_connection(self):
        """Close WebDriver session"""
        self.driver.quit()
