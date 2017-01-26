# -*- coding: utf-8 -*-
import hashlib
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from core.models import News
from .parser import Parser


class Command(BaseCommand, Parser):

    def __init__(self):
        super(Command, self).__init__()
        self.url = 'http://itmentor.by'

    def handle(self, *args, **options):
        URLS = ['/news', '/articles']
        for url in URLS:
            default_url = '{}{}'.format(self.url, url)
            parser = Parser(default_url=default_url)
            soup = parser.get_soup(default_url)
            posts = self.get_posts(soup)
            self.get_save_info(posts)

    @staticmethod
    def get_posts(soup):
        posts = soup.find("div", {"id": "field"})
        posts = posts.findAll("div", {"class": "col-md-3 col-sm-3 link"})
        return posts[0:8]

    def get_save_info(self, posts):
        post__time_published = None
        header = None
        news_content = ''
        reviews = ''
        favorite = None
        comments = None
        link = None
        for post in posts:
            try:
                post__time_published = post.find("p", {"class": "date"}).getText().encode(
                    'utf-8')
            except AttributeError:
                pass
            try:
                title = post.find("div", {"class": "iterator-block"}).find('h3')
                header = title.getText().encode('utf-8')
                link = '{}{}'.format(self.url, title.find('a').get('href'))
            except AttributeError:
                pass

            # go to the detail view page
            soup = self.get_soup(link)

            try:
                news_content = soup.find("div", {"class": "resourse-content"}).find('span').getText().encode('utf-8')
            except AttributeError:
                pass

            hash = hashlib.md5(header).hexdigest()

            try:
                News.objects.create(site=News.ITMENTOR,
                                    link=link,
                                    date_published=post__time_published,
                                    header=header,
                                    content=news_content,
                                    reviews=reviews,
                                    add_to_favorite=favorite,
                                    comments=comments, unique_hash=hash)
            except IntegrityError as e:
                print e
