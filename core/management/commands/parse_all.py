# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('habrahabr')
        call_command('geektimes')
        call_command('tproger')
        call_command('ain_ua')
        call_command('gagadget')
