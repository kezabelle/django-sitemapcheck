===================
django-sitemapcheck
===================

Runs through your `Django`_ sitemaps, and fetching the response for each URL
therein, running a number of configurable checks against the response.

Writes a report to stdout and an HTML file when invoked.

.. image:: https://travis-ci.org/kezabelle/django-sitemapcheck.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-sitemapcheck

Usage
-----

Simple, shove ``sitemapcheck`` into your ``INSTALLED_APPS`` and run the
following::

    python manage.py sitemapcheck

You can use either one or many processes, by setting
``SITEMAPCHECK_MULTIPROCESSING`` to ``True`` or ``False``

Checks
------

Currently checks exist for:

* The HTTP response code (200 is good, 3xx is a caution, everything else is an
  error)
* The presence of an HTML5 doctype (``<!doctype html>``)
* The presence of the HTML ``<title>`` element
* The presence of an HTML ``<meta name="description" ...``
* The presence of an HTML ``<meta name="keywords" ...``
* The presence of a rel-canonical URL
* The presence of an HTML ``<meta name="theme-color" ...`` for new
  Chrome/Android combos.
* The presence of an HTML ``<meta charset="...">``
* The presence of an HTML ``<meta name="viewport" ...``
* The presence of an ``<meta name="mobile-web-app-capable" ...`` (used by
  Android devices to decide if a website may be added to the homescreen)
* The presence of an ``<meta name="apple-mobile-web-app-capable" ...`` (used by
  iOS devices to decide if a website may be added to the homescreen)
* If the page returns an ``Allow`` HTTP header defining HTTP verbs available.
* If the page has a `Content-Security-Policy`_ header.
* If the page as a `X-Frame-Options`_ header.
* If the page has an `X-Content-Type-Options`_ header, (`django-secure`_ can
  provide one)
* If the page makes use of the `rel="home"`_ microformat.
* If the page makes use of `Schema.org`_ breadcrumbs structured data.

Third party support
-------------------

Should support `django-fastsitemaps`_ and `django-static-sitemaps`_, assuming
their views are used in lieu of the normal
``django.contrib.sitemaps.views.sitemap``.


.. _Django: https://www.djangoproject.com/
.. _django-fastsitemaps: https://github.com/litchfield/django-fastsitemaps
.. _django-static-sitemaps: https://github.com/xaralis/django-static-sitemaps
.. _Content-Security-Policy: http://en.wikipedia.org/wiki/Content_Security_Policy
.. _X-Frame-Options: https://docs.djangoproject.com/en/stable/ref/clickjacking/
.. _X-Content-Type-Options: https://www.owasp.org/index.php/List_of_useful_HTTP_headers
.. _django-secure: https://readthedocs.org/projects/django-secure/
.. _rel="home": http://microformats.org/wiki/rel-home
.. _Schema.org: http://schema.org/docs/gs.html
