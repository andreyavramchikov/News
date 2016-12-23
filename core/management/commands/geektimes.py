# -*- coding: utf-8 -*-
import hashlib
from django.core.management.base import BaseCommand
from .parser import Parser
from django.db.utils import IntegrityError
from core.models import News


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.url = 'https://geektimes.ru'
        self.page_count = 3

    def handle(self, *args, **options):
        parser = Parser(default_url=self.url)
        soup = parser.get_soup(self.url)
        pagination = parser.get_pagination("div", "class", "page-nav")
        posts = self.get_posts(soup, "div", "class", "post post_teaser shortcuts_item")

        self.get_save_info(posts)

        if pagination:
            for page_index in range(2, self.page_count):
                soup = parser.get_soup('{}/page{}'.format(self.url, page_index))
                posts = self.get_posts(soup, "div", "class", "post post_teaser shortcuts_item")
                self.get_save_info(posts)

    @staticmethod
    def get_posts(soup, elem, identificator, value):
        posts = soup.findAll(elem, {identificator: value})
        return posts

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
