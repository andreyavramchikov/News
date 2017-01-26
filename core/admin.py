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

    list_display = ('site', 'title', 'date_parsed', 'date_published',
                    'comments', 'add_to_favorite', 'reviews', 'likes')

    list_filter = ('site', 'date_parsed',)

    def title(self, obj):
        return '<a href="{}" target="_blank">{}</a>'.format(obj.link, obj.header.encode('utf-8'))

    title.allow_tags = True

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

    # if the user did not select any items we still need to proceed with all actions except deletion
    def changelist_view(self, request, extra_context=None):
        HARDCODED_ID = 1
        if 'action' in request.POST and request.POST['action'] != 'delete':
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                # for u in News.objects.all():
                post.update({admin.ACTION_CHECKBOX_NAME: HARDCODED_ID})
                request._set_post(post)
        return super(NewsAdmin, self).changelist_view(request, extra_context)


def parse_all_sites(modeladmin, request, queryset):
    call_command('habrahabr')
    call_command('geektimes')
    call_command('tproger')
    call_command('ain_ua')
    call_command('gagadget')
    call_command('itmentor')


def parse_habr(modeladmin, request, queryset):
    call_command('habrahabr')

def parse_itmentor(modeladmin, request, queryset):
    call_command('itmentor')

def parse_geektimes(modeladmin, request, queryset):
    call_command('geektimes')


def parse_tproger(modeladmin, request, queryset):
    call_command('tproger')


def parse_ain_ua(modeladmin, request, queryset):
    call_command('ain_ua')


def parse_gagadget(modeladmin, request, queryset):
    call_command('gagadget')


# admin.site.add_action(parse_all_sites)
admin.site.add_action(parse_habr)
admin.site.add_action(parse_geektimes)
admin.site.add_action(parse_tproger)
admin.site.add_action(parse_ain_ua)
admin.site.add_action(parse_gagadget)
admin.site.add_action(parse_itmentor)
