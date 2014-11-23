# -*- coding: utf-8 -*-
from collections import namedtuple
import logging
from multiprocessing import cpu_count, Pool
from django.utils import six
from django.utils.encoding import force_text
import os
from django.conf import settings
from django.core.paginator import InvalidPage
from django.core.urlresolvers import (reverse, NoReverseMatch, resolve,
                                      Resolver404)
from django.template.loader import render_to_string
from django.test import Client
from .settings import SITEMAPCHECK_CHECKS, SITEMAPCHECK_MULTIPROCESSING
from .checks import Success
from .checks import Caution
from .checks import Error

try:  # try for Django 1.7+ first.
    from django.utils.module_loading import import_string
except ImportError:  # < Django 1.7
    from django.utils.module_loading import import_by_path as import_string


logger = logging.getLogger(__name__)
ViewSitemaps = namedtuple('ViewSitemaps', 'success sitemaps mount_url message')


def get_view_sitemaps(name='django.contrib.sitemaps.views.sitemap'):
    url = None
    try:
        url = reverse('static_sitemaps.views.serve_index')
    except NoReverseMatch:
        logger.info("django-static-sitemaps is probably not being used",
                    exc_info=1)
    if url is None:
        try:
            url = reverse('fastsitemaps.views.sitemap')
        except NoReverseMatch:
            logger.info("django-fastsitemaps is probably not being used",
                        exc_info=1)
    if url is None:
        try:
            url = reverse(name)
        except NoReverseMatch:
            docs_url = "https://docs.djangoproject.com/en/dev/ref/contrib/sitemaps/"  # noqa
            msg = ("no URL named `{name!s}` as per the documentation: "
                   "{docs_url!s}".format(name=name, docs_url=docs_url))
            return ViewSitemaps(success=False, sitemaps=None, mount_url=None,
                                message=msg)

    try:
        view = resolve(url)
    except Resolver404:
        msg = "Couldn't resolve `{url!s}` to a view".format(url=url)
        return ViewSitemaps(success=False, sitemaps=None, mount_url=url,
                            message=msg)

    if 'sitemaps' not in view.kwargs:
        msg = ("No `sitemaps` key within the kwargs for the named "
               "view `{name!s}`".format(name=name))
        return ViewSitemaps(success=False, sitemaps=None, mount_url=url,
                            message=msg)
    return ViewSitemaps(success=True, sitemaps=view.kwargs.get('sitemaps'),
                        mount_url=url, message=None)


def sitemap_urls_iterator(sitemaps):
    for site in sitemaps:
        if callable(site):
            site = site()
        pages = site.paginator.page_range
        for page in pages:
            try:
                for url in site.get_urls(page=page):
                    yield url
            except InvalidPage:
                pass


SitemapRequestResponse = namedtuple('SitemapRequestResponse',
                                    'handler path sitemap_item')


def sitemap_request_iterator(sitemap_results, client=None):
    if client is None:
        client = Client
    for urlinfo in sitemap_results:
        if 'location' not in urlinfo:
            continue
        full_url = urlinfo.get('location')
        path = six.moves.urllib_parse.urlsplit(full_url).path
        yield SitemapRequestResponse(handler=client, path=path,
                                     sitemap_item=urlinfo)


def run_checks_over_response(response):
    checks = getattr(settings, 'SITEMAPCHECK_CHECKS', SITEMAPCHECK_CHECKS)
    imported_checks = (import_string(check) for check in checks)
    for check in imported_checks:
        yield check(response)


Response = namedtuple('Response', 'raw_data status_code path check_results')


def handle_request_response(client, path):
    if callable(client):
        # instantiates the test client or whatever
        client = client()
    data = client.get(path)
    # the following modifications allow the django test Client to be
    # pickled, allowing us to multiplex over more than one process using
    # the stdlib's multiprocessing module.
    if isinstance(client, Client):
        # this first one is https://code.djangoproject.com/ticket/23895#ticket
        data._request.resolver_match = None
        data._request.environ['wsgi.input'] = None
        data._request.environ['wsgi.errors'] = None
        data._request._stream = None
        data.client.handler._request_middleware = []
        data.client.handler._exception_middleware = []
        data.client.handler._view_middleware = []
        data.client.handler._response_middleware = []
        data.client.handler._template_response_middleware = []
        data.client.errors = None
    return Response(raw_data=data, path=path, status_code=data.status_code,
                    check_results=tuple(run_checks_over_response(data)))


def _unpack_handle_request_response(args):
    return handle_request_response(*args)


def singleprocessor(prepared_requests):
    for x in prepared_requests:
        yield handle_request_response(x.handler, x.path)


def multiprocessor(prepared_requests):
    processes = use_multiprocessing()
    if processes is True:
        processes = cpu_count()
    else:
        # let this bubble up an error if the user has configured it stupidly.
        processes = int(processes)
    pool = Pool(cpu_count())
    for_pooling = ((x.handler, x.path) for x in prepared_requests)
    try:
        results = pool.map_async(func=_unpack_handle_request_response,
                             iterable=for_pooling)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        results = ()
    else:
        results = results.get()
    return results


def use_multiprocessing():
    setting = getattr(settings, 'SITEMAPCHECK_MULTIPROCESSING',
                      SITEMAPCHECK_MULTIPROCESSING)
    return setting is not False

ReportLocations = namedtuple('ReportLocations', 'from_file, output_file context')  # noqa


def render_report(results, root_dir):
    template_path = "sitemapcheck/report.html"
    context = {'results': results,
               'Success': Success,
               'Warning': Caution,
               'Caution': Caution,
               'Error': Error}
    report_output = render_to_string(template_name=template_path,
                                     dictionary=context)
    report_output_text = force_text(report_output)
    out_html_path = os.path.realpath(
        os.path.join(root_dir, 'sitemapcheck_report.html'))
    with open(out_html_path, mode='w') as f:
        f.write(report_output_text)
    return ReportLocations(from_file=template_path, output_file=out_html_path,
                           context=context)
