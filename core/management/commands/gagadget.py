# -*- coding: utf-8 -*-
import requests
import hashlib
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
from core.models import News


class Command(BaseCommand):
    GAGADGET = 'http://gagadget.com'
    PAGE_COUNT = 3

    def handle(self, *args, **options):
        pagination = None
        soup = self.get_soup('{}/news/'.format(self.GAGADGET))
        try:
            pagination = soup.find("div", {"class": "paginator"})
        except Exception as e:
            print e

        posts = self.get_posts(soup)
        self.get_save_info(posts)
        if pagination:
            for page_index in range(2, self.PAGE_COUNT):
                soup = self.get_soup('{}/news/?page={}'.format(self.GAGADGET, page_index))
                posts = self.get_posts(soup)
                self.get_save_info(posts)

    @staticmethod
    def get_posts(soup):
        main_columns = soup.find("div", {"class": "l-grid_main pull-right"})
        posts = main_columns.findAll("div", {"class": "l-inner"})
        return posts

    @staticmethod
    def get_soup(url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content)
        return soup

    def get_save_info(self, posts):
        date_published = ''
        header = ''
        news_content = ''
        reviews = ''
        favorite = None
        comments = None
        link = ''
        likes = ''
        for post in posts:
            try:
                link = post.find("a", {"class": "cell-img"}).get('href').encode('utf-8')
                link = '{}{}'.format(self.GAGADGET, link)
            except AttributeError:
                pass
            try:
                date_published = post.find("span", {"class": "cell-date"}).getText().encode(
                    'utf-8')
            except AttributeError:
                pass
            try:
                header = post.find("span", {"class": "cell-title"}).find('a').getText().encode('utf-8')
            except AttributeError:
                pass

            # go to the detail view page
            soup = self.get_soup(link)

            try:
                news_content = soup.find("div", {"class": "b-font-def post-links"}).findAll('p')[0].getText().encode('utf-8')
            except AttributeError:
                pass

            hash = hashlib.md5(header).hexdigest()

            try:
                News.objects.create(site=News.GAGADGET,
                                    link=link,
                                    date_published=date_published,
                                    header=header,
                                    content=news_content,
                                    reviews=reviews,
                                    add_to_favorite=favorite,
                                    comments=comments,
                                    likes=likes,
                                    unique_hash=hash)
            except IntegrityError as e:
                print e
