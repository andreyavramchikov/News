# -*- coding: utf-8 -*-
import requests
import hashlib
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
from core.models import News


class Command(BaseCommand):
    GEEKTIMES = 'https://geektimes.ru'

    def handle(self, *args, **options):
        pagination = None
        soup = self.get_soup(self.GEEKTIMES)
        posts = self.get_posts(soup)
        try:
            pagination = soup.find("div", {"class": "page-nav"})
            pagination = pagination.find("ul", {"id": "nav-pages"})
            page_count = len(pagination.findAll('li'))
        except Exception as e:
            print e

        self.get_save_info(posts)

        if pagination:
            for page_index in range(2, page_count):
                soup = self.get_soup('{}/page{}'.format(self.GEEKTIMES, page_index))
                posts = self.get_posts(soup)
                self.get_save_info(posts)

    @staticmethod
    def get_posts(soup):
        posts = soup.findAll("div", {"class": "post post_teaser shortcuts_item"})
        return posts

    @staticmethod
    def get_soup(url):
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content)
        return soup

    @staticmethod
    def get_save_info(posts):
        post__time_published = None
        post__flow = None
        post__title = None
        news_content = None
        count_post = None
        favorite = None
        comments = None
        link = None
        for post in posts:
            try:
                post__time_published = post.find("span", {"class": "post__time_published"}).getText().encode(
                    'utf-8')
            except AttributeError:
                pass
            try:
                post__flow = post.find("a", {"class": "post__flow"}).getText().encode('utf-8')
            except AttributeError:
                pass
            try:
                post__title = post.find("a", {"class": "post__title_link"})
            except AttributeError:
                pass
            try:
                link = post__title.get('href')
            except AttributeError:
                pass
            try:
                post__title = post__title.getText().encode('utf-8')
            except AttributeError:
                pass
            try:
                news_content = post.find("div", {"class": "content html_format"}).getText().encode('utf-8')
            except AttributeError:
                pass
            try:
                count_post = post.find("div", {"class": "views-count_post"}).getText().encode('utf-8')
            except AttributeError:
                pass
            try:
                favorite = int(post.find("span", {"class": "favorite-wjt__counter js-favs_count"}).getText().encode(
                    'utf-8'))
            except AttributeError:
                pass
            try:
                comments = post.find("a",
                                     {"class": "post-comments__link post-comments__link_all"}).getText().encode(
                    'utf-8')
            except AttributeError:
                pass

            hash = hashlib.md5(post__title).hexdigest()

            try:
                News.objects.create(site=News.GEEKTIMES,
                                    link=link,
                                    date_published=post__time_published,
                                    header='{}-{}'.format(post__flow, post__title),
                                    content=news_content,
                                    reviews=count_post,
                                    add_to_favorite=favorite,
                                    comments=comments, unique_hash=hash)
            except IntegrityError:
                pass
