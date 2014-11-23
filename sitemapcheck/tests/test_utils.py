# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.test import SimpleTestCase as Test, Client
from sitemapcheck.utils import get_view_sitemaps
from sitemapcheck.utils import sitemap_urls_iterator
from sitemapcheck.utils import sitemap_request_iterator
from sitemapcheck.utils import handle_request_response


class GetViewSitemapsTestCase(Test):
    def test_invalid_reverse(self):
        results = get_view_sitemaps(name='yay.hello')
        self.assertFalse(results.success)
        self.assertIsNone(results.sitemaps)
        self.assertIsNone(results.mount_url)

    def test_empty_sitemaps(self):
        results = get_view_sitemaps(name='empty_sitemaps')
        self.assertFalse(results.success)
        self.assertIsNone(results.sitemaps)
        self.assertEqual('/sitemap_a.xml', results.mount_url)
        self.assertIn('`sitemaps`', results.message)

    def test_sitemaps_key_exists(self):
        results = get_view_sitemaps(name='sitemaps_key_exists')
        self.assertTrue(results.success)
        self.assertIsNotNone(results.sitemaps)
        self.assertEqual(results.sitemaps, {
            'hello': None,
        })
        self.assertEqual('/sitemap_b.xml', results.mount_url)
        self.assertIsNone(results.message)


class FakeSitemap(Sitemap):
    def location(self, obj):
        return obj

    def items(self):
        return '/test/', '/test2/', '/test3/test4/'


class SitemapUrlsIteratorTestCase(Test):
    def test_yields_every_url(self):
        sitemaps = (FakeSitemap,)
        results = tuple(sitemap_urls_iterator(sitemaps))
        self.assertEqual(len(results), len(FakeSitemap().items()))
        self.assertEqual(results, (
            {'priority': '',
             'item': '/test/',
             'lastmod': None,
             'changefreq': None,
             'location': u'http://example.com/test/'},
            {'priority': '',
             'item': '/test2/',
             'lastmod': None,
             'changefreq': None,
             'location': u'http://example.com/test2/'},
            {'priority': '',
             'item': '/test3/test4/',
             'lastmod': None,
             'changefreq': None,
             'location': u'http://example.com/test3/test4/'}
        ))


class SitemapRequestIteratorTestCase(Test):
    def test_yields_clients_and_paths(self):
        sitemap_urls = (
            {'priority': '',
             'item': '/test/',
             'lastmod': None,
             'changefreq': None,
             'location': u'http://example.com/test/'},
            {'priority': '',
             'item': '/test2/',
             'lastmod': None,
             'changefreq': None,
             'location': u'http://example.com/test2/'},
            # this one is missing a location on purpose ...
            {'priority': '',
             'item': '/test3/test4/',
             'lastmod': None,
             'changefreq': None}
        )
        results = tuple(sitemap_request_iterator(sitemap_results=sitemap_urls))
        self.assertEqual(len(results), 2)
        result_1, result_2 = results
        self.assertIsInstance(result_1.handler(), Client)
        self.assertIsInstance(result_2.handler(), Client)
        self.assertEqual(result_1.path, '/test/')
        self.assertEqual(result_2.path, '/test2/')


class HandleRequestResponseTestCase(Test):
    def test_crap_data_goes_ok(self):
        response = handle_request_response(client=Client, path='/test/')
        self.assertEqual(404, response.status_code)

    def test_real_path_works(self):
        response = handle_request_response(client=Client, path='/sitemap_c.xml')
        self.assertEqual(200, response.status_code)
        self.assertEqual('/sitemap_c.xml', response.path)
        self.assertGreater(len(response.check_results), 0)
