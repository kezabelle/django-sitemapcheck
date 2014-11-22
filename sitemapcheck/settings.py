# -*- coding: utf-8 -*-
SITEMAPCHECK_CHECKS = (
    'sitemapcheck.checks.check_status_code',
    'sitemapcheck.checks.check_html_title',
    'sitemapcheck.checks.check_html_meta_description',
    'sitemapcheck.checks.check_html_meta_keywords',
    'sitemapcheck.checks.check_html_rel_canonical',
    'sitemapcheck.checks.check_html_android_theme_color',
)


SITEMAPCHECK_MULTIPROCESSING = False
