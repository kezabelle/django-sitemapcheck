# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.utils.encoding import force_text
from django.utils import six
from django.utils.safestring import mark_safe
import os
import sys
from django.core.management import BaseCommand
from sitemapcheck.checks import Error
from sitemapcheck.checks import Caution
from sitemapcheck.checks import Success
from sitemapcheck.utils import get_view_sitemaps
from sitemapcheck.utils import prepare_sitemap_requests
from sitemapcheck.utils import sitemap_urls
from sitemapcheck.utils import use_multiprocessing
from sitemapcheck.utils import singleprocessor
from sitemapcheck.utils import multiprocessor
from sitemapcheck.utils import render_report


class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    # help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        view_sitemaps = get_view_sitemaps()
        if view_sitemaps.success is False:
            if view_sitemaps.message is not None:
                self.stderr.write(self.style.ERROR(view_sitemaps.message))
            # return view_sitemaps
            return sys.exit(1)
        iterable_sitemaps = view_sitemaps.sitemaps.values()
        data = sitemap_urls(iterable_sitemaps)
        prepared_requests = prepare_sitemap_requests(sitemap_results=data)
        if use_multiprocessing():
            if options.get('interactive', True):
                msg = ("You're about to check {count!s} URLs using multiple "
                       "processes, where using Ctrl-C to stop processing is "
                       "flakey, if you have trouble with it, set "
                       "`SITEMAPCHECK_MULTIPROCESSING` to False".format(
                           count=len(prepared_requests)))
                self.stderr.write(self.style.ERROR(msg))
                msg = "Are you sure you wish to continue? [y/N] "
                yes_or_no = six.moves.input(msg)
                if not yes_or_no.lower().startswith('y'):
                    msg = "URL checks cancelled"
                    self.stderr.write(self.style.ERROR(msg))
                    return sys.exit(1)
            results = multiprocessor(prepared_requests)
        else:
            results = singleprocessor(prepared_requests)
        results_for_reports = []
        for result in results:
            self.stdout.write(self.style.HTTP_SUCCESS(result.path))
            results_for_reports.append(result)
            for check in result.check_results:
                if check is None:
                    continue
                name = force_text(check.name).encode('ascii', 'ignore')
                check_msg = mark_safe(check.msg).encode('ascii', 'ignore')
                msg = '{name!s}: {msg!s}'.format(name=name, msg=check_msg)
                if check.code == Error:
                    self.stderr.write("    " + self.style.ERROR(msg))
                elif check.code == Caution:
                    self.stdout.write("    " + self.style.WARNING(msg))
                elif check.code == Success:
                    self.stdout.write("    " + self.style.HTTP_REDIRECT(msg))
                else:
                    self.stderr.write("    " + self.style.ERROR(msg))
        render_report(results_for_reports, root_dir=os.getcwd())
