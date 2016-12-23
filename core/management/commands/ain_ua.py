# -*- coding: utf-8 -*-
import requests
import hashlib
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
from core.models import News


class Command(BaseCommand):
    AIN = 'http://ain.ua/category/startupscat'

    def handle(self, *args, **options):
        soup = self.get_soup(self.AIN)
        posts = self.get_posts(soup)
        self.get_save_info(posts)

    @staticmethod
    def get_posts(soup):
        main_columns = soup.find("div", {"class": "top_posts_wrapper"})
        posts = main_columns.findAll("div", {"class": "fresh_latest_post"})
        return posts

    @staticmethod
    def get_soup(url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content)
        return soup

    def get_save_info(self, posts):
        date_published = None
        header = None
        news_content = None
        favorite = None
        comments = None
        link = None
        likes = ''
        reviews = ''
        for post in posts:
            try:
                link = post.find("a").get('href').encode('utf-8')
            except AttributeError:
                pass
            try:
                date_published = post.find("P", {"class": "fresh_small"}).getText().encode(
                    'utf-8')
            except AttributeError:
                pass
            try:
                header = post.find("h3", {"class": "fresh_big "}).getText().encode('utf-8')
            except AttributeError:
                pass

            # go to the detail view page
            soup = self.get_soup(link)

            try:
                news_content = soup.find("div", {"class": "post"}).findAll('p')[0].getText().encode('utf-8')
            except AttributeError:
                pass
            hash = hashlib.md5(header).hexdigest()

            try:
                News.objects.create(site=News.AIN,
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
