# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.test import TestCase as DbTest
from django.test import SimpleTestCase as Test
from sitemapcheck.checks import CheckedResponse
from sitemapcheck.checks import Success
from sitemapcheck.checks import Error
from sitemapcheck.checks import Caution
from sitemapcheck.checks import check_status_code
from sitemapcheck.checks import check_html_title
from sitemapcheck.checks import check_html_meta_description
from sitemapcheck.checks import check_html_meta_keywords
from sitemapcheck.checks import check_html_rel_canonical
from sitemapcheck.checks import check_html_android_theme_color
from sitemapcheck.checks import check_html_meta_charset
from sitemapcheck.checks import check_html_meta_viewport
from sitemapcheck.checks import check_mobile_homescreen
from sitemapcheck.checks import check_ios_homescreen
from sitemapcheck.checks import check_html5_doctype


class StatusCodeTestCase(Test):
    def test_success(self):
        response = HttpResponse()
        checked = check_status_code(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)

    def test_redirect(self):
        url = 'https://docs.djangoproject.com'
        response = HttpResponseRedirect(redirect_to=url)
        checked = check_status_code(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)

    def test_error(self):
        response = HttpResponse(status=401)
        checked = check_status_code(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Error)

    def test_internal_error(self):
        response = HttpResponse(status=503)
        checked = check_status_code(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Error)


class HtmlTitleTestCase(Test):
    def test_has_title(self):
        response = HttpResponse(content="""
        <html><head><title>test</title></head><body>yay</body></html>
        """)
        checked = check_html_title(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "test")

    def test_has_no_title(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_html_title(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Error)
        self.assertEqual(checked.msg, "Missing <title>")


class HtmlDescriptionTestCase(Test):
    def test_has_description(self):
        response = HttpResponse(content="""
        <html><head><meta name="description" content="test"></head>
        <body>yay</body></html>
        """)
        checked = check_html_meta_description(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "test")

    def test_has_no_description(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_html_meta_description(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'Missing <meta name="description">')


class HtmlKeywordsTestCase(Test):
    def test_has_keywords(self):
        response = HttpResponse(content="""
        <html><head><meta name="keywords" content="test, more test"></head>
        <body>yay</body></html>
        """)
        checked = check_html_meta_keywords(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "test, more test")

    def test_has_no_keywords_is_caution(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_html_meta_keywords(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'Missing <meta name="keywords">')


class RelCanonicalTestCase(Test):
    def test_has_canonical_url(self):
        response = HttpResponse(content="""
        <html><head><link rel="canonical" href="https://google.com/"></head>
        <body>yay</body></html>
        """)
        checked = check_html_rel_canonical(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "https://google.com/")

    def test_has_no_canonical_url(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_html_rel_canonical(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'Missing <link rel="canonical">')


class ThemeColorTestCase(Test):
    def test_has_android_chrome_theme_color(self):
        response = HttpResponse(content="""
        <html><head><meta name="theme-color" content="#EEECCC"></head>
        <body>yay</body></html>
        """)
        checked = check_html_android_theme_color(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "EEECCC")

    def test_doesnt_have_android_chrome_theme_color(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_html_android_theme_color(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'Missing <meta name="theme-color">')


class MetaCharsetTestCase(Test):
    def test_has_charset(self):
        response = HttpResponse(content="""
        <html><head><meta charset="hello-test"></head>
        <body>yay</body></html>
        """)
        checked = check_html_meta_charset(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "hello-test")

    def test_missing_charset(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_html_meta_charset(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'Missing <meta charset="...">')


class MetaViewportTestCase(Test):
    def test_has_viewport(self):
        response = HttpResponse(content="""
        <html><head><meta name="viewport" content="width=device-width"></head>
        <body>yay</body></html>
        """)
        checked = check_html_meta_viewport(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "width=device-width")

    def test_missing_viewport(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_html_meta_viewport(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'Missing <meta name="viewport">')


class AndroidHomescreenTestCase(Test):
    def test_has_mobile_app_capable(self):
        response = HttpResponse(content="""
        <html><head><meta name="mobile-web-app-capable" content="yes"></head>
        <body>yay</body></html>
        """)
        checked = check_mobile_homescreen(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "yes")

    def test_missing_mobile_app_capable(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_mobile_homescreen(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'no')


class IosHomescreenTestCase(Test):
    def test_has_apple_mobile_app_capable(self):
        response = HttpResponse(content="""
        <html><head><meta name="apple-mobile-web-app-capable" content="yes">
        </head><body>yay</body></html>
        """)
        checked = check_ios_homescreen(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "yes")

    def test_missing_apple_mobile_app_capable(self):
        response = HttpResponse(content="""
        <html><head></head><body>yay</body></html>
        """)
        checked = check_ios_homescreen(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Caution)
        self.assertEqual(checked.msg, 'no')


class Html5DoctypeTestCase(Test):
    def test_has_html5_doctype(self):
        response = HttpResponse(content="""
        <!doctype html>
        <html><head><title>...</title></head><body>...</body></html>
        """)
        checked = check_html5_doctype(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Success)
        self.assertEqual(checked.msg, "yes")

    def test_has_non_html5_doctype(self):
        response = HttpResponse(content="""
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html><head><title>...</title></head><body>...</body></html>
        """)
        checked = check_html5_doctype(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Error)
        self.assertEqual(checked.msg, "Missing the HTML5 doctype, or it is not "
                                      "the first element in the document")

    def test_has_misplaced_html5_doctype(self):
        response = HttpResponse(content="""
        <html><head><title>...</title></head><body>...</body></html>
        <!doctype html>
        """)
        checked = check_html5_doctype(response)
        self.assertIsInstance(checked, CheckedResponse)
        self.assertEqual(checked.code, Error)
        self.assertEqual(checked.msg, "Missing the HTML5 doctype, or it is not "
                                      "the first element in the document")
