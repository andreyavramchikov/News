# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class News(models.Model):
    HABRAHABR = 'HABRAHABR'
    GEEKTIMES = 'GEEKTIMES'
    TPROGER = 'TPROGER'
    SITE_CHOICES = (
        (HABRAHABR, 'HABRAHABR'),
        (GEEKTIMES, 'GEEKTIMES'),
        (TPROGER, 'TPROGER'),
    )

    site = models.CharField(choices=SITE_CHOICES, max_length=255)
    link = models.CharField(max_length=255, blank=True)
    header = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    date_parsed = models.DateTimeField(auto_now_add=True, verbose_name="Parsed")
    date_published = models.CharField(verbose_name="Published", max_length=255, blank=True)
    comments = models.IntegerField(null=True, blank=True, verbose_name="Comments")
    likes = models.CharField(max_length=255, blank=True)
    add_to_favorite = models.IntegerField(null=True, blank=True, verbose_name="Favorite")
    reviews = models.CharField(max_length=255, blank=True)
    unique_hash = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return '{}-{}'.format(self.site, self.header)

    class Meta:
        verbose_name = u"News"
        verbose_name_plural = u"News"
