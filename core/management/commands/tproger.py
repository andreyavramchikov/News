# -*- coding: utf-8 -*-
import requests
import hashlib
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
from core.models import News

from .parser import Parser


class Command(BaseCommand, Parser):

    def __init__(self):
        super(Command, self).__init__()
        self.url = 'https://tproger.ru'
        self.page_count = 4

    def handle(self, *args, **options):
        parser = Parser(default_url=self.url)
        soup = parser.get_soup(self.url)
        pagination = parser.get_pagination("div", "class", "pagination")
        posts = self.get_posts(soup)

        self.get_save_info(posts)

        if pagination:
            for page_index in range(2, self.page_count):
                soup = parser.get_soup('{}/page{}'.format(self.url, page_index))
                posts = self.get_posts(soup)
                self.get_save_info(posts)

    @staticmethod
    def get_posts(soup):
        main_columns = soup.find("div", {"id": "main_columns"})
        posts = main_columns.findAll("article")
        return posts

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
                link = post.find("h1", {"class":"entry-title"}).find('a').get('href').encode('utf-8')
            except AttributeError:
                pass
            try:
                date_published = post.find("time", {"class": "entry-date updated"}).getText().encode(
                    'utf-8')
            except AttributeError:
                pass
            try:
                header = post.find("span", {"class": "entry-title-heading"}).getText().encode('utf-8')
            except AttributeError:
                pass
            try:
                news_content = post.find("div", {"class": "entry-content"}).getText().encode('utf-8')
            except AttributeError:
                pass

            # go to the detail view page
            soup = self.get_soup(link)

            try:
                reviews = soup.find("span", {"class": "post-views-count"}).getText().encode('utf-8')
            except AttributeError:
                pass

            try:
                likes = soup.find("span", {"id": "stats_num"}).getText().encode('utf-8')
            except AttributeError:
                pass

            hash = hashlib.md5(header).hexdigest()

            try:
                News.objects.create(site=News.TPROGER,
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
