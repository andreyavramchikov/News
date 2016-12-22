# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


class Parser(object):

    def __init__(self, default_url=None):
        self.URL = default_url

    def get_pagination(self, element, identificator, value):
        try:
            return self.soup.find(element, {identificator: value})
        except Exception as e:
            return None

    def is_pagination_exist(self):
        pass

    def get_soup(self, url):
        response = requests.get(url)
        content = response.content
        self.soup = BeautifulSoup(content)
        return self.soup

    def run(self):
        pass
