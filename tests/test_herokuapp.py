import unittest
from utils.driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from requests import get
import getpass


class TestElements(unittest.TestCase):
    def setUp(self):
        """
        options = Options()
        options.add_experimental_option("prefs", {
            "download.default_directory": f"/Users/{getpass.getuser()}/Downloads",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        """
        self.driver = Driver('Chrome').get_driver()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.url = lambda x: self.driver.get(f'http://the-internet.herokuapp.com/{x}')

    def tearDown(self):
        self.driver.quit()

    def test_add_delete_elements(self):
        self.url('add_remove_elements/')
        self.driver.find_element(By.CSS_SELECTOR, '#content > div > button').click()
        self.driver.find_element(By.CSS_SELECTOR, '#elements > button').click()

    def test_broken(self):
        self.url('broken_images')
        expected = [False, False, True]
        for i, img in enumerate(self.driver.find_elements(By.CSS_SELECTOR, '#content > div > img')):
            src = img.get_attribute('src')
            res = get(src)
            actual = True if res.status_code == 200 else False
            assert expected[i] == actual

    def test_checkboxes(self):
        self.url('checkboxes')
        expected = [False, True]
        for i, checkbox in enumerate(self.driver.find_elements(By.CSS_SELECTOR, '#checkboxes > input[type=checkbox]')):
            assert expected[i] == checkbox.is_selected()
            checkbox.click()
            assert expected[i] != checkbox.is_selected()

    def test_context_click(self):
        self.url('context_menu')
        actionChains = ActionChains(self.driver)
        actionChains.context_click(self.driver.find_element(By.CSS_SELECTOR, '#hot-spot')).perform()
        alert = self.driver.switch_to.alert
        alert.accept()
        actionChains.send_keys('I', Keys.ENTER).perform()

    def test_dropdown(self):
        self.url('dropdown')
        select = Select(self.driver.find_element(By.CSS_SELECTOR, '#dropdown'))
        assert 'Please select an option' == select.first_selected_option.text
        select.select_by_visible_text('Option 2')
        assert 'Option 2' == select.first_selected_option.text

    def test_remove_element_and_add_back(self):
        self.url('dynamic_controls')
        for val in [('#checkbox > input[type=checkbox]', EC.staleness_of),
                    ('#checkbox-example > button', EC.visibility_of)]:
            self.driver.find_element(By.CSS_SELECTOR, '#checkbox-example > button').click()
            cb = self.driver.find_element(By.CSS_SELECTOR, val[0])
            WebDriverWait(self.driver, 10).until(val[1](cb))

    def test_hide_element(self):
        self.url('download')
        btn = self.driver.find_element(By.CSS_SELECTOR, '#content > div > a:nth-child(2)')
        btn.click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element(btn))

    def test_download(self):
        self.url('downloads')

    def test_iframe(self):
        self.url('iframe')
        self.driver.switch_to.frame('mce_0_ifr')
        content = self.driver.find_element(By.CSS_SELECTOR, '#tinymce > p')
        content.clear()
        content.send_keys('Hello')  # this triggers a change to the element, resulting it to be stale
        assert 'Hello' == self.driver.find_element(By.CSS_SELECTOR, '#tinymce > p').text

    def test_hover(self):
        self.url('hovers')
        actionChains = ActionChains(self.driver)
        actionChains.move_to_element(self.driver.find_element(By.CSS_SELECTOR, '#content > div > div:nth-child(3) > img')).perform()
        assert 'View profile' == self.driver.find_element(By.XPATH, '//a[text()="View profile"]').text