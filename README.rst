===================
django-sitemapcheck
===================

Runs through your `Django`_ sitemaps, and fetching the response for each URL
therein, running a number of configurable checks against the response.

Writes a report to stdout and an HTML file when invoked.

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
* The presence of the HTML ``<title>`` element
* The presence of an HTML ``<meta name="description" ...``
* The presence of an HTML ``<meta name="keywords" ...``
* The presence of a rel-canonical URL
* The presence of an HTML ``<meta name="theme-color" ...`` for new
  Chrome/Android combos.
* _whaever else I come up with..._

.. _Django: https://www.djangoproject.com/
