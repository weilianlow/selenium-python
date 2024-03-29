import selenium.webdriver


class Driver:
    def __init__(self, browser, options=None):
        self.driver = None
        if browser == 'Firefox':
            self.driver = selenium.webdriver.Firefox()
        elif browser == 'Chrome':
            if options:
                self.driver = selenium.webdriver.Chrome(options=options)
            else:
                self.driver = selenium.webdriver.Chrome()
        elif browser == 'Headless Chrome':
            opts = selenium.webdriver.ChromeOptions()
            opts.add_argument('headless')
            self.driver = selenium.webdriver.Chrome(options=opts)
        else:
            raise Exception(f'Browser "{browser}" is not supported')

    def get_driver(self):
        return self.driver
