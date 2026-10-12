#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_ga.py — inject the GA4 gtag snippet into every built HTML page.
Idempotent: skips files that already contain the tag, and skips redirect
pages (meta refresh / noindex), which must not be counted.

Usage: python3 inject_ga.py   (run AFTER build_krillion.py / build_daily.py,
BEFORE deploy_krillion.py)
"""
import os

LOCAL_ROOT = os.path.dirname(os.path.abspath(__file__))
GID = "G-2SVZ3QE217"
GTAG = (
    '<script async src="https://www.googletagmanager.com/gtag/js?id=' + GID + '"></script>\n'
    '<script>\n'
    'window.dataLayer = window.dataLayer || [];\n'
    'function gtag(){dataLayer.push(arguments);}\n'
    "gtag('js', new Date());\n"
    "gtag('config', '" + GID + "');\n"
    '</script>\n'
)
SKIP_DIRS = {".secrets", "__pycache__", ".git", "logs"}


def is_redirect(html):
    return 'http-equiv="refresh"' in html or "noindex" in html


def process(root):
    n = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            with open(p, encoding="utf-8") as f:
                html = f.read()
            if "googletagmanager.com/gtag/js" in html:
                continue
            if is_redirect(html):
                continue
            if "</head>" not in html:
                continue
            html = html.replace("</head>", GTAG + "</head>", 1)
            with open(p, "w", encoding="utf-8") as f:
                f.write(html)
            n += 1
    print(f"Injected GA4 ({GID}) into {n} HTML files")


if __name__ == "__main__":
    process(LOCAL_ROOT)
