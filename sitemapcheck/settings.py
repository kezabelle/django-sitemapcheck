# -*- coding: utf-8 -*-
SITEMAPCHECK_CHECKS = (
    'sitemapcheck.checks.check_status_code',
    'sitemapcheck.checks.check_html_title',
    'sitemapcheck.checks.check_html_meta_description',
    'sitemapcheck.checks.check_html_meta_keywords',
    'sitemapcheck.checks.check_html_rel_canonical',
    'sitemapcheck.checks.check_html_android_theme_color',
    'sitemapcheck.checks.check_html_meta_charset',
    'sitemapcheck.checks.check_html_meta_viewport',
    'sitemapcheck.checks.check_mobile_homescreen',
    'sitemapcheck.checks.check_ios_homescreen',
    'sitemapcheck.checks.check_html5_doctype',
    'sitemapcheck.checks.check_allow_header',
    'sitemapcheck.checks.check_csp_header',
    'sitemapcheck.checks.check_frameorigin_header',
    'sitemapcheck.checks.check_content_type_nosniff_header',
    'sitemapcheck.checks.check_html_rel_home',
)


SITEMAPCHECK_MULTIPROCESSING = False
