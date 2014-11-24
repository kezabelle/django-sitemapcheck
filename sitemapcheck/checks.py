# -*- coding: utf-8 -*-
from django.utils.encoding import force_text
import re
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple

Success = _("Success")
Error = _("Error")
Caution = _("Warning")
Info = _("Info")
CheckedResponse = namedtuple('CheckedResponse', 'msg code name')


DEFAULT_RE_FLAGS = re.DOTALL | re.IGNORECASE | re.MULTILINE
title_re = re.compile(r'<title>(.+?)</title>', flags=DEFAULT_RE_FLAGS)

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
    data = title_re.search(force_text(response.content))
    if data is None:
        return CheckedResponse(msg="Missing <title>", code=Error,
                               name=checkname)
    outdata = ','.join(data.groups())
    collapsed_outdata = re.sub('\s+', ' ', outdata)
    return CheckedResponse(msg=collapsed_outdata, code=Success, name=checkname)


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
    copied_content = force_text(response.content.strip())
    if not copied_content.startswith('<!doctype html>'):
        return CheckedResponse(msg='Missing the HTML5 doctype, or it is not '
                                   'the first element in the document',
                               code=Error, name=checkname)
    return CheckedResponse(msg='yes', code=Success,
                           name=checkname)


def check_allow_header(response):
    checkname = _("Allows HTTP methods")
    if 'Allow' in response:
        return CheckedResponse(msg=response['Allow'], code=Success,
                               name=checkname)
    return CheckedResponse(msg="Unknown", code=Info, name=checkname)


def check_csp_header(response):
    checkname = _("Has content security policy")
    if 'Content-Security-Policy' in response:
        return CheckedResponse(msg=response['Content-Security-Policy'],
                               code=Success, name=checkname)
    return CheckedResponse(msg="Missing Content-Security-Policy header, "
                               "anything is permitted", code=Caution,
                           name=checkname)


def check_frameorigin_header(response):
    checkname = _("Clickjacking via X-Frame-Options")
    if 'X-Frame-Options' in response:
        return CheckedResponse(msg=response['X-Frame-Options'], code=Success,
                               name=checkname)
    return CheckedResponse(msg="No X-Frame-Options set.", code=Error,
                           name=checkname)


def check_content_type_nosniff_header(response):
    checkname = _("Browser content-type sniffing")
    if 'X-Content-Type-Options' in response:
        return CheckedResponse(msg=response['X-Content-Type-Options'],
                               code=Success,
                               name=checkname)
    return CheckedResponse(msg="No X-Content-Type-Options set, browsers may "
                               "sniff the stream to decide on a content-type",
                           code=Info,
                           name=checkname)


def check_html_rel_home(response):
    checkname = _("rel=home")
    if 'rel="home"' not in force_text(response.content):
        return CheckedResponse(msg='Missing rel="home" microformat',
                               code=Info, name=checkname)
    count = force_text(response.content).count('rel="home"')
    return CheckedResponse(msg='{count} found'.format(count=count),
                           code=Success, name=checkname)


def check_html_schemaorg_breadcrumbs(response):
    checkname = _("Schema.org breadcrumbs")
    breadcrumbs = 'itemtype="http://schema.org/Breadcrumb"'
    breadcrumbs_found = breadcrumbs in force_text(response.content)
    if not breadcrumbs_found:
        return CheckedResponse(msg="Doesn't have breadcrumbs itemtype",
                               code=Info, name=checkname)
    count = force_text(response.content).count(breadcrumbs)
    return CheckedResponse(msg='{count} found'.format(count=count),
                           code=Success, name=checkname)
