from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import re


class SearchScraper:

    def __init__(self, search):
        self._search_url = search
        self._logged_in = False

        # Instantiate selenium chrome web driver.
        path = r"C:\Users\james\PythonProjects\selenium\chromedriver.exe"
        self._driver = webdriver.Chrome(executable_path=path)

    def fetch_element(self, query):
        # Following section heavily based on tutorial from tutorialspoint:
        # https://www.tutorialspoint.com/python_web_scraping/python_web_scraping_dynamic_websites.htm
        try:
            self._driver.get(self._search_url)
            self._driver.find_element_by_id("search").send_keys(query)
            self._driver.find_element_by_id("search").send_keys(Keys.ENTER)
            self._driver.implicitly_wait(45)
            link = self._driver.find_element_by_css_selector(".product > .product > .product-item-link")
            print("Following link:", link.text)
            link.click()
            login_link = self._driver.find_element_by_css_selector("#simple-" + query + " .add-to-cart-btn span")
            if not self._logged_in:
                self.login(login_link)

            return self._driver.find_element_by_xpath("//div[@id='simple-" + query + "']/div[3]/div")

        except NoSuchElementException:
            return ""

    def fetch_data(self, query, regex):
        # Get the element being searched for and convert it to text.
        element = self.fetch_element(query).text
        data = re.search(regex, element).group(0)
        print("Located Data: " + data)
        return data

    def login(self, login_link):
        # Get username and password from user.
        username = input("Username: ")
        password = input("Password: ")
        # Navigate to the login screen and enter details.
        print("Login required...")
        print("Following link: " + login_link.text)
        self._driver.execute_script("arguments[0].click();", login_link)

        # Enter login details as required.
        self._driver.find_element_by_id("email").send_keys(username)
        self._driver.find_element_by_id("pass").send_keys(password)
        login_button = self._driver.find_element_by_id("send2")
        print("Following link: " + login_button.text)
        login_button.click()
        self._logged_in = True

    def close(self):
        # Close the web driver.
        self._driver.close()
