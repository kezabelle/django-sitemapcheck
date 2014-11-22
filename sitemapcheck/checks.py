# -*- coding: utf-8 -*-
from django.utils.encoding import force_text
import re
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple

Success = _("Success")
Error = _("Error")
Caution = _("Warning")
CheckedResponse = namedtuple('CheckedResponse', 'msg code name')


def check_status_code(response):
    checkname = _("Status code")
    if response.status_code > 300 and response.status_code < 400:
        msg = "Performs a redirect (%d)" % response.status_code
        return CheckedResponse(msg=msg, code=Caution, name=checkname)
    if response.status_code != 200:
        msg = "Unexpected (%d)" % response.status_code
        return CheckedResponse(msg=msg, code=Error, name=checkname)
    if response.status_code == 200:
        return CheckedResponse(msg="OK!", code=Success, name=checkname)


def check_html_title(response):
    checkname = _("HTML title")
    data = re.search(r'<title>(.+)</title>', force_text(response.content))
    if data is None:
        return CheckedResponse(msg="Missing <title>", code=Error,
                               name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_html_meta_description(response):
    checkname = _("HTML meta description")
    data = re.search(r'<meta name="description" content="(.+?)">',
                     force_text(response.content))
    if data is None:
        return CheckedResponse(msg='Missing <meta name="description">',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_html_meta_keywords(response):
    checkname = _("HTML meta keywords")
    data = re.search(r'<meta name="keywords" content="(.+?)">',
                     force_text(response.content))
    if data is None:
        return CheckedResponse(msg='Missing <meta name="keywords">',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_html_rel_canonical(response):
    checkname = _("rel=canonical")
    data = re.search(r'<link rel="canonical" href="(.+?)">',
                     force_text(response.content))
    if data is None:
        return CheckedResponse(msg='Missing <link rel="canonical">',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_html_android_theme_color(response):
    checkname = _("Android theme colour")
    data = re.search(r'<meta name="theme-color" content="#([a-fA-F0-9]{6})">',
                     force_text(response.content))
    if data is None:
        return CheckedResponse(msg='Missing <meta name="theme-color">',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_html_meta_charset(response):
    checkname = _("HTML meta charset")
    data = re.search(r'<meta charset="(.+?)">',
                     force_text(response.content))
    if data is None:
        return CheckedResponse(msg='Missing <meta charset="...">',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_html_meta_viewport(response):
    checkname = _("HTML meta viewport")
    data = re.search(r'<meta name="viewport" content="(.+?)">',
                     force_text(response.content))
    if data is None:
        return CheckedResponse(msg='Missing <meta name="viewport">',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_mobile_homescreen(response):
    checkname = _("May be added to Android homescreen")
    data = re.search(r'<meta name="mobile-web-app-capable" content="(.+?)">',
                     force_text(response.content))
    if data is None:
        return CheckedResponse(msg='no',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_ios_homescreen(response):
    checkname = _("May be added to iOS homescreen")
    data = re.search(r'<meta name="apple-mobile-web-app-capable" '
                     r'content="(.+?)">', force_text(response.content))
    if data is None:
        return CheckedResponse(msg='no',
                               code=Caution, name=checkname)
    return CheckedResponse(msg=','.join(data.groups()), code=Success,
                           name=checkname)


def check_html5_doctype(response):
    checkname = _("HTML5 doctype")
    copied_content = response.content.strip()
    if not copied_content.startswith('<!doctype html>'):
        return CheckedResponse(msg='Missing the HTML5 doctype, or it is not '
                                   'the first element in the document',
                               code=Error, name=checkname)
    return CheckedResponse(msg='yes', code=Success,
                           name=checkname)
