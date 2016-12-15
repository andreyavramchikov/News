# -*- coding: utf-8 -*-
import arrow

from django.utils.html import format_html
from django.core.urlresolvers import reverse

from django.contrib import admin
from django.core.management import call_command
from django.conf.urls import url

from django.http.response import HttpResponseRedirect

from core.utils import publish_news
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    ordering = ('date_parsed', 'comments', 'add_to_favorite')

    list_display = ('site', 'header', 'show_link', 'news_actions', 'date_parsed', 'date_published',
                    'comments', 'add_to_favorite', 'reviews', 'likes')

    list_filter = ('site', 'date_parsed',)

    def show_link(self, obj):
        return '<a href="{}">Переход</a>'.format(obj.link)

    show_link.allow_tags = True

    def queryset(self, request):
        return super(NewsAdmin, self).queryset(request).filter(date_parsed__gte=arrow.now().replace(weeks=+2).datetime)

    def get_urls(self):
        urls = super(NewsAdmin, self).get_urls()
        custom_urls = [
            url(
                r'^(?P<news_id>.+)/publish/$',
                self.admin_site.admin_view(self.publish_news),
                name='news-publish',
            ),
        ]
        return custom_urls + urls

    def publish_news(self, request, news_id, *args, **kwargs):
        publish_news(news_id)
        return HttpResponseRedirect(reverse('admin:core_news_changelist'))

    def news_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Publish news</a>&nbsp;',
            reverse('admin:news-publish', args=[obj.pk]),
        )

    news_actions.short_description = 'Publish Action'
    news_actions.allow_tags = True


def parse_all_sites(modeladmin, request, queryset):
    call_command('parse_habr')
    call_command('parse_geektimes')
    call_command('parse_tproger')


def parse_habr(modeladmin, request, queryset):
    call_command('parse_habr')


def parse_geektimes(modeladmin, request, queryset):
    call_command('parse_geektimes')


def parse_tproger(modeladmin, request, queryset):
    call_command('parse_tproger')


admin.site.add_action(parse_all_sites)
admin.site.add_action(parse_habr)
admin.site.add_action(parse_geektimes)
admin.site.add_action(parse_tproger)