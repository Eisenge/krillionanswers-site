#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Krillion daily answer page generator.
Fetches https://krillion.io/api/today, builds /dive/<N>/ pages (5-language shell,
English prompts and rare-answer ideas), refreshes /dive/latest/ redirect and
appends the new dive URL to sitemap.xml. Designed to run unattended on a daily
cron after the game resets (UTC 04:00).
"""
import os, sys, json, re, urllib.request, datetime, html as htmlmod

DEPLOY = os.path.dirname(os.path.abspath(__file__))
KR = "https://krillionanswers.online"  # placeholder; owner provides the real domain
API = "https://krillion.io/api/today"

ORDER = ["en", "ru", "es", "pt", "id"]
LANG_LABELS = {"en": "English", "ru": "Русский", "es": "Español", "pt": "Português", "id": "Bahasa Indonesia"}

# Human-readable dates per language (the daily page title must carry the date).
MONTHS = {
    "en": ["January","February","March","April","May","June","July","August","September","October","November","December"],
    "ru": ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"],
    "es": ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"],
    "pt": ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"],
    "id": ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"],
}

def format_date(iso, lang):
    y, m, d = iso.split("-")
    mo = MONTHS[lang][int(m) - 1]
    if lang == "en":
        return f"{mo} {int(d)}, {y}"
    if lang == "ru":
        return f"{int(d)} {mo} {y}"
    if lang == "es" or lang == "pt":
        return f"{int(d)} de {mo} de {y}"
    return f"{int(d)} {mo} {y}"

# 5-language shell strings for the daily page.
I18N = {
    "en": {
        "title": "Krillion Answers Today — {date} (Dive #{n}) | 7 Prompts & Rare Answers",
        "desc": "Krillion answers today ({date}, Dive #{n}): the 7 official prompts and rare-answer ideas. See what the questions are, how to score deeper, and play the official game.",
        "eyebrow": "DAILY DIVE / ANSWERS",
        "h1": "Krillion Answers for {date} (Dive #{n})",
        "intro": "Here are today's seven Krillion prompts (from the official game) with rare-answer ideas. Answers are suggestions, not official answers; rarity depends on what other players type.",
        "section_q": "Today's 7 prompts",
        "section_a": "Rare-answer ideas",
        "tip": "Rare-answer tip",
        "tip_txt": "Rare answers sink deeper. Prefer a specific, valid pick over a famous one; think of a subcategory before you type.",
        "play": "Play today's dive on the official game",
        "yesterday": "Yesterday's dive",
        "not_official": "Independent guide, not affiliated with Krillion. Questions come from the official game.",
        "lang_label": "Language",
        "home": "Home",
        "nav_back": "Back to guide home",
        "disclaimer": "These are suggested ideas for rare answers, not official answers from the game. Answer pools and scoring belong to krillion.io.",
    },
    "ru": {
        "title": "Krillion Answers Today — {date} (Dive #{n}) | 7 подсказок и редкие ответы",
        "desc": "Krillion answers today ({date}, Dive #{n}): 7 официальных подсказок и идеи редких ответов. Узнайте вопросы дня, как нырять глубже, и сыграйте в официальную игру.",
        "eyebrow": "ДНЕВНОЕ ПОГРУЖЕНИЕ / ОТВЕТЫ",
        "h1": "Krillion Answers за {date} (Dive #{n})",
        "intro": "Вот семь сегодняшних подсказок Krillion (из официальной игры) с идеями редких ответов. Это предложения, а не официальные ответы; редкость зависит от того, что вводят другие игроки.",
        "section_q": "7 подсказок дня",
        "section_a": "Идеи редких ответов",
        "tip": "Совет по редким ответам",
        "tip_txt": "Редкие ответы уводят глубже. Выбирайте конкретный валидный вариант вместо известного; подумайте о подкатегории, прежде чем вводить.",
        "play": "Сыграть сегодняшнее погружение в официальной игре",
        "yesterday": "Вчерашнее погружение",
        "not_official": "Независимый гид, не связан с Krillion. Вопросы взяты из официальной игры.",
        "lang_label": "Язык",
        "home": "Главная",
        "nav_back": "Назад к гайду",
        "disclaimer": "Это предложенные идеи редких ответов, а не официальные ответы игры. Наборы ответов и очки принадлежат krillion.io.",
    },
    "es": {
        "title": "Krillion Answers Today — {date} (Dive #{n}) | 7 pistas y respuestas raras",
        "desc": "Krillion answers today ({date}, Dive #{n}): las 7 pistas oficiales e ideas de respuestas raras. Mira las preguntas del día, cómo puntuar más profundo y juega al juego oficial.",
        "eyebrow": "DAILY DIVE / RESPUESTAS",
        "h1": "Krillion Answers del {date} (Dive #{n})",
        "intro": "Estas son las siete pistas de hoy de Krillion (del juego oficial) con ideas de respuestas raras. Son sugerencias, no respuestas oficiales; la rareza depende de lo que escriban otros jugadores.",
        "section_q": "Las 7 pistas de hoy",
        "section_a": "Ideas de respuestas raras",
        "tip": "Consejo de respuestas raras",
        "tip_txt": "Las respuestas raras hunden más. Prefiere una opción específica y válida sobre una famosa; piensa en una subcategoría antes de escribir.",
        "play": "Juega la inmersión de hoy en el juego oficial",
        "yesterday": "Inmersión de ayer",
        "not_official": "Guía independiente, sin afiliación con Krillion. Las preguntas vienen del juego oficial.",
        "lang_label": "Idioma",
        "home": "Inicio",
        "nav_back": "Volver a la guía",
        "disclaimer": "Son ideas sugeridas de respuestas raras, no respuestas oficiales del juego. Los conjuntos de respuestas y la puntuación pertenecen a krillion.io.",
    },
    "pt": {
        "title": "Krillion Answers Today — {date} (Dive #{n}) | 7 perguntas e respostas raras",
        "desc": "Krillion answers today ({date}, Dive #{n}): as 7 dicas oficiais e ideias de respostas raras. Veja as perguntas do dia, como pontuar mais fundo e jogue o jogo oficial.",
        "eyebrow": "DAILY DIVE / RESPOSTAS",
        "h1": "Krillion Answers de {date} (Dive #{n})",
        "intro": "Aqui estão as sete dicas de hoje do Krillion (do jogo oficial) com ideias de respostas raras. São sugestões, não respostas oficiais; a raridade depende do que outros jogadores digitam.",
        "section_q": "As 7 dicas de hoje",
        "section_a": "Ideias de respostas raras",
        "tip": "Dica de respostas raras",
        "tip_txt": "Respostas raras afundam mais. Prefira uma opção específica e válida a uma famosa; pense numa subcategoria antes de digitar.",
        "play": "Jogue o mergulho de hoje no jogo oficial",
        "yesterday": "Mergulho de ontem",
        "not_official": "Guia independente, sem afiliação com Krillion. As perguntas vêm do jogo oficial.",
        "lang_label": "Idioma",
        "home": "Início",
        "nav_back": "Voltar ao guia",
        "disclaimer": "São ideias sugeridas de respostas raras, não respostas oficiais do jogo. Os conjuntos de respostas e a pontuação pertencem a krillion.io.",
    },
    "id": {
        "title": "Krillion Answers Today — {date} (Dive #{n}) | 7 Petunjuk & Jawaban Langka",
        "desc": "Krillion answers today ({date}, Dive #{n}): 7 petunjuk resmi dan ide jawaban langka. Lihat pertanyaan hari ini, cara mendapat skor lebih dalam, dan mainkan game resminya.",
        "eyebrow": "DAILY DIVE / JAWABAN",
        "h1": "Krillion Answers untuk {date} (Dive #{n})",
        "intro": "Berikut tujuh petunjuk Krillion hari ini (dari game resmi) dengan ide jawaban langka. Ini saran, bukan jawaban resmi; kelangkaan bergantung pada apa yang diketik pemain lain.",
        "section_q": "7 petunjuk hari ini",
        "section_a": "Ide jawaban langka",
        "tip": "Tips jawaban langka",
        "tip_txt": "Jawaban langka menenggelamkan lebih dalam. Pilih pilihan spesifik dan valid daripada yang terkenal; pikirkan subkategori sebelum mengetik.",
        "play": "Mainkan penyelaman hari ini di game resmi",
        "yesterday": "Penyelaman kemarin",
        "not_official": "Panduan independen, tidak berafiliasi dengan Krillion. Pertanyaan berasal dari game resmi.",
        "lang_label": "Bahasa",
        "home": "Beranda",
        "nav_back": "Kembali ke panduan",
        "disclaimer": "Ini ide saran jawaban langka, bukan jawaban resmi game. Kumpulan jawaban dan skor milik krillion.io.",
    },
}

# ---- Rare-answer idea engine ----
# Keyword -> list of rare but valid answers (most unusual first). The engine
# matches prompt text; a generic strategy line is appended as fallback.
RARE_IDEAS = [
    (["sold in a roll"], ["a roll of solder", "a roll of postage stamps", "linoleum roll", "a coin roll of quarters", "wallpaper roll", "a roll of bubble wrap", "duct tape roll"]),
    (["type of table", "kind of table"], ["a drafting table", "a trestle table", "a gateleg table", "a refectory table", "a pier table", "a harvest table", "an altar table", "a drum table"]),
    (["metal", "pure elements"], ["bismuth", "gallium", "indium", "antimony", "rhodium", "tantalum", "cadmium", "scandium", "hafnium", "rhenium", "osmium", "thallium"]),
    (["license or permit", "licence or permit", "kind of license"], ["a falconry permit", "a pyrotechnics permit", "an amateur radio licence", "a peddler's permit", "a chauffeur licence", "a salvage licence", "a hawking licence"]),
    (["app or service for paying", "paying or sending money", "send money"], ["Wise", "Payoneer", "Skrill", "Klarna", "N26", "Monzo", "Apple Cash", "Google Pay", "Revolut", "Stripe"]),
    (["sport that is a race", "sport.*race"], ["pigeon racing", "skeleton", "wheelchair racing", "luge", "biathlon", "bobsled", "sailboat racing", "orienteering", "greyhound racing", "drag racing"]),
    (["borders Iraq", "borders Iran", "border Iraq", "border Iran"], ["Kuwait", "Armenia", "Turkmenistan", "Jordan", "Azerbaijan", "Afghanistan", "Syria"]),
    (["country"], ["a landlocked country you rarely hear in trivia", "a microstate", "an island nation with a small population"]),
    (["sea"], ["an inland sea", "a sea named after a region", "a marginal sea"]),
    (["river"], ["a tributary", "a river with a short name", "a river in Central Asia"]),
    (["bird", "songbird"], ["a regional songbird with a quiet range", "a bird named after a place"]),
    (["dish", "food", "chinese dish"], ["a regional dish", "a dish from a small town", "an unusual street food"]),
    (["city"], ["a regional capital", "a smaller city in a famous country"]),
    (["president"], ["a lesser-known historical president", "a president of a small country"]),
    (["song", "music"], ["a deep cut by a famous band", "a regional folk song"]),
    (["animal"], ["an animal with a small habitat range", "a rarely named species"]),
    (["job", "profession"], ["a niche trade", "a disappearing profession"]),
    (["color", "colour"], ["an unusual shade name", "a named pigment"]),
    (["plant", "flower", "tree"], ["a rare native species", "a plant with a regional name"]),
    (["tool"], ["a specialized hand tool", "a historical tool"]),
    (["game"], ["a regional sport", "a traditional folk game"]),
    (["capital"], ["a lesser-known capital", "a capital with an unusual name"]),
    (["island"], ["a small island group", "an island you rarely hear about"]),
]

def match_ideas(text):
    low = text.lower()
    for kws, ideas in RARE_IDEAS:
        if any(k in low for k in kws):
            return ideas
    return None

def fetch_today():
    req = urllib.request.Request(API, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/147.0 Safari/537.36",
        "Referer": "https://krillion.io/",
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_dive_page(lang, day):
    I = I18N[lang]
    n = day["dayNumber"]
    date = day["date"]
    path = f"/dive/{n}/" if lang == "en" else f"/{lang}/dive/{n}/"
    url = f"{KR}{path}"
    date_h = format_date(date, lang)
    title = I["title"].format(n=n, date=date_h)
    desc = I["desc"].format(n=n, date=date_h)
    # hreflang block
    hrefl = []
    for lo in ORDER:
        href = f"{KR}/dive/{n}/" if lo == "en" else f"{KR}/{lo}/dive/{n}/"
        hrefl.append(f'<link rel="alternate" hreflang="{lo}" href="{href}">')
    hrefl.append(f'<link rel="alternate" hreflang="x-default" href="{KR}/dive/{n}/">')
    hrefl_s = "\n".join(hrefl)
    # language nav
    lnav = []
    for lo in ORDER:
        href = f"/dive/{n}/" if lo == "en" else f"/{lo}/dive/{n}/"
        cur = ' aria-current="page"' if lo == lang else ""
        lnav.append(f'<a href="{href}" lang="{lo}" hreflang="{lo}"{cur}>{LANG_LABELS[lo]}</a>')
    lnav_s = "".join(lnav)
    # questions + ideas
    q_items = []
    a_items = []
    for i, p in enumerate(day["prompts"], 1):
        q_items.append(f'<li><span class="qnum">Q{i}</span> {esc(p["text"])}</li>')
        ideas = match_ideas(p["text"])
        if ideas:
            a_items.append(f'<li><b>{esc(p["text"])}</b><ul class="ideas">' +
                           "".join(f'<li>{esc(idea)}</li>' for idea in ideas) + "</ul></li>")
        else:
            a_items.append(f'<li><b>{esc(p["text"])}</b><p class="noidea">No specific ideas in our engine — prefer a specific, valid pick; think of a subcategory.</p></li>')
    # breadcrumb JSON-LD
    bread = json.dumps([
        {"@type": "ListItem", "position": 1, "name": I["home"], "item": f"{KR}/"},
        {"@type": "ListItem", "position": 2, "name": f"Dive {n}", "item": url},
    ], ensure_ascii=False)
    name_ld = json.dumps(title, ensure_ascii=False)
    desc_ld = json.dumps(desc, ensure_ascii=False)
    yesterday = f"/dive/{n-1}/" if lang == "en" else f"/{lang}/dive/{n-1}/"
    home_href = "/" if lang == "en" else f"/{lang}/"
    howto_href = "/how-to-play/" if lang == "en" else f"/{lang}/how-to-play/"
    tips_href = "/tips/" if lang == "en" else f"/{lang}/tips/"
    crumb = (f'<nav class="breadcrumbs" aria-label="Breadcrumb">'
             f'<a href="{home_href}">{I["home"]}</a><span aria-hidden="true">›</span>'
             f'<span aria-current="page">Dive {n}</span></nav>')
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#15324a"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/style.css?v=20261012"><link rel="canonical" href="{url}">{hrefl_s}<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebPage", "name": {name_ld}, "url": "{url}", "description": {desc_ld}, "inLanguage": "{lang}", "isPartOf": {{"@type": "WebSite", "name": "Krillion Guide", "url": "{KR}/"}}}}</script><script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": {bread}}}</script></head><body><a class="skip" href="#main">{I['nav_back']}</a><header><a class="brand" href="{home_href}">k<span>↗</span> <b>krillion guide</b></a><nav aria-label="Main"><a href="{howto_href}">How to play</a><a href="{tips_href}">Tips</a></nav></header><nav class="languages" aria-label="{I['lang_label']}">{lnav_s}</nav><main id="main"><article class="article dive-page">{crumb}<p class="eyebrow">{esc(I['eyebrow'])}</p><h1>{esc(I['h1'].format(n=n, date=date_h))}</h1><p class="intro">{I['intro']}</p><div class="dive-meta"><span class="badge">DIVE #{n}</span><span class="badge">Date: {date}</span><span class="badge">Resets: {day['resetsAt']}</span></div><h2>{I['section_q']}</h2><ol class="questions">{''.join(q_items)}</ol><h2>{I['section_a']}</h2><ul class="answer-ideas">{''.join(a_items)}</ul><div class="tip-box"><h2>{I['tip']}</h2><p>{I['tip_txt']}</p></div><p class="fine"><a href="https://krillion.io">{I['play']}</a> · <a href="{yesterday}">{I['yesterday']}</a></p><p class="fine">{I['disclaimer']} · {I['not_official']}</p></article></main><footer><a class="brand" href="{home_href}">krillion guide<span>↗</span></a><nav aria-label="Footer"><a href="{home_href}">Home</a><a href="{howto_href}">How to play</a><a href="{tips_href}">Tips</a></nav></footer></body></html>
"""

def build_latest(lang, n):
    """/dive/latest -> meta-refresh + canonical to today's dive."""
    path = "/dive/latest/" if lang == "en" else f"/{lang}/dive/latest/"
    url = f"{KR}{path}"
    target = f"/dive/{n}/" if lang == "en" else f"/{lang}/dive/{n}/"
    tgt_url = f"{KR}/dive/{n}/" if lang == "en" else f"{KR}/{lang}/dive/{n}/"
    label = {"en": "Latest Krillion Dive Answers", "ru": "Последний Dive Krillion", "es": "Último Krillion Dive", "pt": "Último Krillion Dive", "id": "Krillion Dive Terbaru"}[lang]
    home_href = "/" if lang == "en" else f"/{lang}/"
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>{label}</title><link rel="canonical" href="{tgt_url}"><meta http-equiv="refresh" content="0; url={target}"></head><body><a href="{target}">{label}</a></body></html>
"""

def update_sitemap():
    # regenerate full sitemap: static pages + dive pages found on disk
    sitemap_path = os.path.join(DEPLOY, "sitemap.xml")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    static = ["index", "how-to-play", "tips", "krillion-game", "krillion-unlimited", "one-in-a-krillion"]
    for lang in ORDER:
        for slug in static:
            if slug == "index":
                url = f"{KR}/" if lang == "en" else f"{KR}/{lang}/"
            else:
                url = f"{KR}/{slug}/" if lang == "en" else f"{KR}/{lang}/{slug}/"
            lines.append(f"  <url><loc>{url}</loc><lastmod>2026-10-11</lastmod></url>")
    # dive dirs on disk
    dive_dir = os.path.join(DEPLOY, "dive")
    nums = []
    if os.path.isdir(dive_dir):
        for name in os.listdir(dive_dir):
            if name.isdigit():
                nums.append(int(name))
    for n in sorted(nums):
        for lang in ORDER:
            url = f"{KR}/dive/{n}/" if lang == "en" else f"{KR}/{lang}/dive/{n}/"
            lines.append(f"  <url><loc>{url}</loc><lastmod>{datetime.date.today().isoformat()}</lastmod></url>")
    lines.append("</urlset>")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return len(lines) - 3

def main():
    day = fetch_today()
    n = day["dayNumber"]
    date = day["date"]
    print(f"Fetched dive #{n} for {date}, {len(day['prompts'])} prompts")
    for lang in ORDER:
        html = build_dive_page(lang, day)
        d = os.path.join(DEPLOY, "dive", str(n)) if lang == "en" else os.path.join(DEPLOY, lang, "dive", str(n))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        # latest redirect
        ld = os.path.join(DEPLOY, "dive", "latest") if lang == "en" else os.path.join(DEPLOY, lang, "dive", "latest")
        os.makedirs(ld, exist_ok=True)
        with open(os.path.join(ld, "index.html"), "w", encoding="utf-8") as f:
            f.write(build_latest(lang, n))
        print("wrote", lang, "dive", n)
    count = update_sitemap()
    print("sitemap urls:", count)

if __name__ == "__main__":
    main()
