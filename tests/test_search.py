import unittest
from utils.driver import Driver
from pages.results import ResultsPage
from pages.search import SearchPage


class TestSearchResult(unittest.TestCase):
    def setUp(self):
        self.driver = Driver('Chrome').get_driver()
        self.driver.implicitly_wait(10)
        self.search_page = SearchPage(self.driver)
        self.result_page = ResultsPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_search_panda(self):
        for i, phrase in enumerate(['panda', 'hello']):
            with self.subTest(i=i):
                self.driver.get('https://www.duckduckgo.com')
                self.search_page.search(phrase)
                assert phrase == self.result_page.search_input_value()
                titles = self.result_page.result_link_titles()
                matches = [t for t in titles if phrase.lower() in t.lower()]
                assert len(matches) > 0
                assert phrase in self.driver.title


if __name__ == '__main__':
    unittest.main()
