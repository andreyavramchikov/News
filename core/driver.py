from selenium import webdriver
from fake_useragent import UserAgent
from pyvirtualdisplay import Display


class Driver(object):

    def __init__(self, name, disable=False, headless=False, width=1600, height=1000):
        self.name = name
        self.disable = disable
        self.width = width
        self.height = height
        if headless:
            display = Display(visible=0, size=(1000, 1000))
            display.start()

    @property
    def driver(self):
        driver = None
        if self.name == 'chrome':
            driver = self.get_chrome_driver()
        elif self.name == 'firefox':
            driver = self.get_firefox_driver()
        return driver

    def set_driver_size(self):
        self.driver.set_window_size(self.width, self.height)

    @property
    def chrome_options(self):
        if self.disable:
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            return chrome_options
        else:
            return None

    def get_chrome_driver(self):
        return webdriver.Chrome('/home/andrey/chromedriver', chrome_options=self.chrome_options)

    def set_firefox_preference(self, profile):
        if self.disable:
            profile.set_preference('permissions.default.stylesheet', 2)
            # Disable images
            profile.set_preference('permissions.default.image', 2)
            # Disable Flash
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            profile.set_preference("general.useragent.override", UserAgent().random)
        return profile

    def get_firefox_driver(self):
        return webdriver.Firefox(self.set_firefox_preference(webdriver.FirefoxProfile()))