import unittest
from utils.driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


class TestElements(unittest.TestCase):
    def setUp(self):
        self.driver = Driver('Chrome').get_driver()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_input_and_textarea(self):
        self.driver.get('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_textarea_form')
        self.driver.switch_to.frame('iframeResult')
        text_box = self.driver.find_element(By.CSS_SELECTOR,'input[name="usrname"]')
        text_box.send_keys('hello')
        assert 'hello' == text_box.get_attribute('value')
        text_area = self.driver.find_element(By.CSS_SELECTOR,'textarea[name="comment"]')
        text_area.clear()
        text_area.send_keys('world')
        assert 'world' == text_area.get_attribute('value')

    def test_checkbox(self):
        self.driver.get('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_input_type_checkbox')
        self.driver.switch_to.frame('iframeResult')
        for elem_id in ('vehicle1', 'vehicle2', 'vehicle3'):
            element = self.driver.find_element(By.CSS_SELECTOR, f'#{elem_id}')
            assert not element.is_selected()
            element.click()
            assert element.is_selected()

    def test_radio(self):
        self.driver.get('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml5_input_type_radio')
        self.driver.switch_to.frame('iframeResult')
        for elem_id in ('html', 'css', 'javascript'):
            element = self.driver.find_element(By.CSS_SELECTOR, f'#{elem_id}')
            element.click()
            for elem_id2 in ('html', 'css', 'javascript'):
                element2 = self.driver.find_element(By.CSS_SELECTOR, f'#{elem_id2}')
                if elem_id == elem_id2:
                    assert element2.is_selected()
                else:
                    assert not element2.is_selected()

    def test_select(self):
        self.driver.get('https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_option_selected')
        self.driver.switch_to.frame('iframeResult')
        select = Select(self.driver.find_element(By.CSS_SELECTOR, 'select#cars'))
        select.select_by_visible_text('Saab')
        assert 'Saab' == select.first_selected_option.text


if __name__ == '__main__':
    unittest.main()
