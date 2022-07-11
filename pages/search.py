from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base import BasePage


class SearchPage(BasePage):
    SEARCH_INPUT = (By.ID, 'search_form_input_homepage')

    def search(self, phrase):
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(phrase, Keys.RETURN)
