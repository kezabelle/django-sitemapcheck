# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap


class FakeSitemap(Sitemap):
    def location(self, obj):
        return obj

    def items(self):
        return '/test/', '/test2/', '/test3/test4/'


urlpatterns = patterns('',
    url(r'^admin_mountpoint/', include(admin.site.urls)),
    url('sitemap_a\.xml', sitemap, {}, name='empty_sitemaps'),
    url('sitemap_b\.xml', sitemap, {'sitemaps': {
        'hello': None,
        }},
        name='sitemaps_key_exists'),
    url('sitemap_c\.xml', sitemap, {'sitemaps': {
        'hello': FakeSitemap,
        }},
        name='sitemaps_key_exists_with_sitemap'),
)
