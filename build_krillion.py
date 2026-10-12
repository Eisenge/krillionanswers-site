#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Krillion guide site (independent, unofficial) in 5 languages.
Placeholder domain KR is replaced once the owner picks the real domain.
Pages: index, how-to-play, tips, krillion-game, krillion-unlimited, one-in-a-krillion.
"""
import os, json

DEPLOY = os.path.dirname(os.path.abspath(__file__))
KR = "https://krillionanswers.online"  # placeholder; owner will provide the real domain

LANGS = {
    "ru": {
        "skip": "К содержимому",
        "header_nav": [("Сегодня", "/ru/dive/latest/"), ("Как играть", "/ru/how-to-play/"), ("Советы", "/ru/tips/")],
        "lang_label": "Язык",
        "home": "Главная",
        "guides_name": "Гайды по Krillion",
        "footer_desc": "Независимый неофициальный сайт-гид по Krillion (The Daily Dive). Не связан с разработчиком игры.",
        "footer_nav": [
            ("Как играть", "/ru/how-to-play/"), ("Советы", "/ru/tips/"),
            ("Krillion Game", "/ru/krillion-game/"), ("Безлимит", "/ru/krillion-unlimited/"),
            ("One in a Krillion", "/ru/one-in-a-krillion/"),
            ("Конфиденциальность", "/ru/privacy/"), ("Условия", "/ru/terms/"),
        ],
        "official": "Официальная игра",
    },
    "es": {
        "skip": "Ir al contenido",
        "header_nav": [("Dive de hoy", "/es/dive/latest/"), ("Cómo jugar", "/es/how-to-play/"), ("Consejos", "/es/tips/")],
        "lang_label": "Idioma",
        "home": "Inicio",
        "guides_name": "Guías de Krillion",
        "footer_desc": "Sitio de guía independiente y no oficial sobre Krillion (The Daily Dive). Sin afiliación con el desarrollador del juego.",
        "footer_nav": [
            ("Cómo jugar", "/es/how-to-play/"), ("Consejos", "/es/tips/"),
            ("Krillion Game", "/es/krillion-game/"), ("Sin límites", "/es/krillion-unlimited/"),
            ("One in a Krillion", "/es/one-in-a-krillion/"),
            ("Privacidad", "/es/privacy/"), ("Condiciones", "/es/terms/"),
        ],
        "official": "Juego oficial",
    },
    "pt": {
        "skip": "Ir para o conteúdo",
        "header_nav": [("Dive de hoje", "/pt/dive/latest/"), ("Como jogar", "/pt/how-to-play/"), ("Dicas", "/pt/tips/")],
        "lang_label": "Idioma",
        "home": "Início",
        "guides_name": "Guias de Krillion",
        "footer_desc": "Site de guia independente e não oficial sobre Krillion (The Daily Dive). Sem vínculo com o desenvolvedor do jogo.",
        "footer_nav": [
            ("Como jogar", "/pt/how-to-play/"), ("Dicas", "/pt/tips/"),
            ("Krillion Game", "/pt/krillion-game/"), ("Sem limites", "/pt/krillion-unlimited/"),
            ("One in a Krillion", "/pt/one-in-a-krillion/"),
            ("Privacidade", "/pt/privacy/"), ("Termos", "/pt/terms/"),
        ],
        "official": "Jogo oficial",
    },
    "id": {
        "skip": "Ke konten utama",
        "header_nav": [("Dive hari ini", "/id/dive/latest/"), ("Cara bermain", "/id/how-to-play/"), ("Tips", "/id/tips/")],
        "lang_label": "Bahasa",
        "home": "Beranda",
        "guides_name": "Panduan Krillion",
        "footer_desc": "Situs panduan independen dan tidak resmi tentang Krillion (The Daily Dive). Tidak berafiliasi dengan pengembang game.",
        "footer_nav": [
            ("Cara bermain", "/id/how-to-play/"), ("Tips", "/id/tips/"),
            ("Krillion Game", "/id/krillion-game/"), ("Tanpa batas", "/id/krillion-unlimited/"),
            ("One in a Krillion", "/id/one-in-a-krillion/"),
            ("Privasi", "/id/privacy/"), ("Ketentuan", "/id/terms/"),
        ],
        "official": "Game resmi",
    },
}

EN = {
    "skip": "Skip to content",
    "header_nav": [("Today's Dive", "/dive/latest/"), ("How to play", "/how-to-play/"), ("Tips", "/tips/")],
    "lang_label": "Language",
    "home": "Home",
    "guides_name": "Krillion Guides",
    "footer_desc": "Independent, unofficial guide site about Krillion (The Daily Dive). Not affiliated with the game's developer.",
    "footer_nav": [
        ("How to play", "/how-to-play/"), ("Tips", "/tips/"),
        ("Krillion Game", "/krillion-game/"), ("Unlimited", "/krillion-unlimited/"),
        ("One in a Krillion", "/one-in-a-krillion/"),
        ("Privacy", "/privacy/"), ("Terms", "/terms/"),
    ],
    "official": "Official game",
}

ORDER = ["en", "ru", "es", "pt", "id"]
LANG_LABELS = {"en": "English", "ru": "Русский", "es": "Español", "pt": "Português", "id": "Bahasa Indonesia"}

# Page slugs in build order. index is generated separately.
SLUGS = ["how-to-play", "tips", "krillion-game", "krillion-unlimited", "one-in-a-krillion"]

PAGE_SHORT = {
    "how-to-play": {"en": "How to Play", "ru": "Как играть", "es": "Cómo jugar", "pt": "Como jogar", "id": "Cara bermain"},
    "tips": {"en": "Krillion Tips", "ru": "Советы по Krillion", "es": "Consejos de Krillion", "pt": "Dicas de Krillion", "id": "Tips Krillion"},
    "krillion-game": {"en": "Krillion Game", "ru": "Игра Krillion", "es": "Krillion Game", "pt": "Krillion Game", "id": "Game Krillion"},
    "krillion-unlimited": {"en": "Krillion Unlimited", "ru": "Krillion Unlimited", "es": "Krillion Unlimited", "pt": "Krillion Unlimited", "id": "Krillion Unlimited"},
    "one-in-a-krillion": {"en": "One in a Krillion", "ru": "One in a Krillion", "es": "One in a Krillion", "pt": "One in a Krillion", "id": "One in a Krillion"},
}

# Each page: per-language [title, description, eyebrow, h1, intro, sections, fine]
PAGES = {
    "how-to-play": {
        "en": [
            "Krillion How to Play: 7 Prompts, 25 Seconds, Rare Answers",
            "Step-by-step Krillion guide for new players: how a Daily Dive round works, what counts as a rare answer, and common mistakes to avoid.",
            "GUIDES / NEW PLAYERS",
            "Krillion How to Play: the Daily Dive explained",
            "Krillion (The Daily Dive) gives you seven prompts and about 25 seconds each to type an answer. Rare answers score far more than obvious ones. Here is how a round works from the first prompt to your final depth.",
            [
                ["h2", "What happens in a round"],
                ["p", "Open <a href=\"https://krillion.io\">krillion.io</a> and start the Daily Dive. You get seven prompts, one at a time. Each prompt is a category or open question, for example a country ending in O, a sea, a songbird, a Chinese dish. You have about 25 seconds per prompt to type one answer and confirm it."],
                ["h2", "Why rare answers matter"],
                ["p", "The game compares your answer with what other players type that day. Common answers barely move your score. Unusual, specific answers push you deeper. Krillion describes this with a diving metaphor: the rarer your answers, the deeper you sink below the surface; obvious ones keep you near the top."],
                ["h2", "The depth score"],
                ["ul", ["<b>Rare answers sink you deeper</b> — depth is your score for the day.", "<b>Obvious answers barely count</b> — a common pick keeps you near the surface.", "<b>Same prompts for everyone</b> — all players answer the same seven prompts, so daily scores are comparable.", "<b>One Daily Dive per day</b> — the daily round resets daily; archive and unlimited modes let you play more."]],
                ["h2", "How to enter an answer"],
                ["ul", ["<b>Read the prompt</b> — decide what kind of thing it asks for (a country, a song, a dish).", "<b>Pick a specific, valid answer</b> — precise names usually beat broad categories.", "<b>Type and confirm quickly</b> — the timer is about 25 seconds, so keep your first good idea.", "<b>No account needed to play</b> — the daily game runs free in your browser."]],
                ["h2", "Common mistakes for new players"],
                ["ul", ["<b>Typing a broad category</b> — a general word scores much less than a concrete name.", "<b>Second-guessing yourself</b> — with 25 seconds, the first valid rare idea is often the best.", "<b>Skipping the prompt check</b> — answering a nearby category (a region instead of a country) usually scores worse.", "<b>Assuming you need an app</b> — Krillion is a browser game; nothing to install."]],
                ["h2", "Modes beyond the daily round"],
                ["p", "Krillion.io also has an archive of past dives, themed packs and an unlimited mode. If you want to practice outside the daily round, see our <a href=\"/krillion-unlimited/\">Krillion Unlimited guide</a>."],
                ["h2", "Is this the official Krillion site?"],
                ["p", "No. This is an independent guide. The official game is <a href=\"https://krillion.io\">krillion.io</a>; we only explain how it works and how to play better."],
            ],
            "Sources: krillion.io (official game) and the game's own in-game text, checked October 11, 2026.",
        ],
        "ru": [
            "Krillion: как играть — 7 подсказок, 25 секунд, редкие ответы",
            "Пошаговый гайд по Krillion для новичков: как проходит раунд Daily Dive, что считается редким ответом и каких ошибок избегать.",
            "ГАЙДЫ / НОВИЧКАМ",
            "Krillion: как играть — Daily Dive для новичков",
            "Krillion (The Daily Dive) даёт семь подсказок и примерно 25 секунд на каждую, чтобы ввести ответ. Редкие ответы дают намного больше очков, чем очевидные. Вот как проходит раунд — от первой подсказки до финальной глубины.",
            [
                ["h2", "Что происходит в раунде"],
                ["p", "Откройте <a href=\"https://krillion.io\">krillion.io</a> и начните Daily Dive. Вы получаете семь подсказок по одной. Каждая подсказка — категория или открытый вопрос, например страна на букву О, море, певчая птица, китайское блюдо. На каждую подсказку даётся около 25 секунд, чтобы ввести один ответ и подтвердить его."],
                ["h2", "Почему редкие ответы важны"],
                ["p", "Игра сравнивает ваш ответ с тем, что в этот день вводят другие игроки. Частые ответы почти не двигают счёт. Необычные, конкретные ответы уводят вас глубже. Krillion описывает это метафорой погружения: чем реже ваши ответы, тем глубже вы опускаетесь под поверхность; очевидные оставляют вас у верха."],
                ["h2", "Очки глубины"],
                ["ul", ["<b>Редкие ответы опускают глубже</b> — глубина и есть ваш счёт за день.", "<b>Очевидные ответы почти не считаются</b> — частый выбор держит вас у поверхности.", "<b>Одинаковые подсказки для всех</b> — все игроки отвечают на одни и те же семь подсказок, так что дневные счета сравнимы.", "<b>Одно погружение в день</b> — дневной раунд обновляется ежедневно; архив и безлимитный режим позволяют играть больше."]],
                ["h2", "Как вводить ответ"],
                ["ul", ["<b>Прочитайте подсказку</b> — поймите, о чём она просит (страна, песня, блюдо).", "<b>Выберите конкретный валидный ответ</b> — точные названия обычно бьют широкие категории.", "<b>Вводите и подтверждайте быстро</b> — таймер около 25 секунд, поэтому держитесь первой хорошей идеи.", "<b>Аккаунт не нужен</b> — дневная игра бесплатно работает в браузере."]],
                ["h2", "Частые ошибки новичков"],
                ["ul", ["<b>Ввод широкой категории</b> — общее слово даёт намного меньше конкретного названия.", "<b>Перепроверка себя</b> — за 25 секунд первая валидная редкая идея обычно лучшая.", "<b>Пропуск проверки подсказки</b> — ответ про соседнюю категорию (регион вместо страны) обычно оценивается хуже.", "<b>Уверенность, что нужен апп</b> — Krillion работает в браузере, устанавливать ничего не нужно."]],
                ["h2", "Режимы помимо дневного раунда"],
                ["p", "На krillion.io также есть архив прошлых погружений, тематические наборы и безлимитный режим. Если хотите практиковаться вне дневного раунда, посмотрите наш <a href=\"/krillion-unlimited/\">гайд по Krillion Unlimited</a>."],
                ["h2", "Это официальный сайт Krillion?"],
                ["p", "Нет. Это независимый гайд. Официальная игра — <a href=\"https://krillion.io\">krillion.io</a>; мы лишь объясняем, как она работает и как играть лучше."],
            ],
            "Источники: krillion.io (официальная игра) и текст самой игры, проверено 11 октября 2026 года.",
        ],
        "es": [
            "Krillion: cómo jugar — 7 pistas, 25 segundos, respuestas raras",
            "Guía paso a paso de Krillion para nuevos jugadores: cómo funciona una ronda de Daily Dive, qué cuenta como respuesta rara y errores comunes.",
            "GUÍAS / NUEVOS JUGADORES",
            "Krillion: cómo jugar — Daily Dive explicado",
            "Krillion (The Daily Dive) te da siete pistas y unos 25 segundos en cada una para escribir una respuesta. Las respuestas raras puntúan mucho más que las obvias. Así funciona una ronda, desde la primera pista hasta tu profundidad final.",
            [
                ["h2", "Qué ocurre en una ronda"],
                ["p", "Abre <a href=\"https://krillion.io\">krillion.io</a> y empieza el Daily Dive. Recibes siete pistas, una a una. Cada pista es una categoría o pregunta abierta, por ejemplo un país que termine en O, un mar, un pájaro cantor, un plato chino. Tienes unos 25 segundos por pista para escribir una respuesta y confirmarla."],
                ["h2", "Por qué importan las respuestas raras"],
                ["p", "El juego compara tu respuesta con lo que otros jugadores escriben ese día. Las respuestas comunes apenas mueven tu puntuación. Las respuestas inusuales y específicas te hunden más. Krillion lo describe con una metáfora de buceo: cuanto más raras son tus respuestas, más profundo bajas bajo la superficie; las obvias te mantienen arriba."],
                ["h2", "La puntuación de profundidad"],
                ["ul", ["<b>Las respuestas raras te hunden</b> — la profundidad es tu puntuación del día.", "<b>Las respuestas obvias apenas cuentan</b> — una elección común te mantiene cerca de la superficie.", "<b>Las mismas pistas para todos</b> — todos responden las siete pistas iguales, así que las puntuaciones diarias son comparables.", "<b>Un Daily Dive al día</b> — la ronda diaria se renueva a diario; el archivo y el modo sin límites permiten jugar más."]],
                ["h2", "Cómo escribir una respuesta"],
                ["ul", ["<b>Lee la pista</b> — decide qué tipo de cosa pide (un país, una canción, un plato).", "<b>Elige una respuesta concreta y válida</b> — los nombres precisos suelen ganar a las categorías amplias.", "<b>Escribe y confirma rápido</b> — el temporizador es de unos 25 segundos, así que quédate con tu primera buena idea.", "<b>No hace falta cuenta</b> — el juego diario corre gratis en el navegador."]],
                ["h2", "Errores comunes de los nuevos jugadores"],
                ["ul", ["<b>Escribir una categoría amplia</b> — una palabra general puntúa mucho menos que un nombre concreto.", "<b>Dudar de ti mismo</b> — con 25 segundos, la primera idea rara válida suele ser la mejor.", "<b>Saltarse la comprobación de la pista</b> — responder a una categoría vecina (una región en vez de un país) suele puntuar peor.", "<b>Pensar que necesitas una app</b> — Krillion es un juego de navegador; no hay nada que instalar."]],
                ["h2", "Modos más allá de la ronda diaria"],
                ["p", "Krillion.io también tiene un archivo de inmersiones pasadas, packs temáticos y un modo sin límites. Si quieres practicar fuera de la ronda diaria, mira nuestra <a href=\"/krillion-unlimited/\">guía de Krillion Unlimited</a>."],
                ["h2", "¿Es este el sitio oficial de Krillion?"],
                ["p", "No. Es una guía independiente. El juego oficial está en <a href=\"https://krillion.io\">krillion.io</a>; solo explicamos cómo funciona y cómo jugar mejor."],
            ],
            "Fuentes: krillion.io (juego oficial) y el texto del propio juego, consultado el 11 de octubre de 2026.",
        ],
        "pt": [
            "Krillion: como jogar — 7 dicas, 25 segundos, respostas raras",
            "Guia passo a passo de Krillion para novos jogadores: como funciona uma rodada do Daily Dive, o que conta como resposta rara e erros comuns.",
            "GUIAS / NOVOS JOGADORES",
            "Krillion: como jogar — Daily Dive explicado",
            "Krillion (The Daily Dive) dá sete dicas e cerca de 25 segundos em cada uma para você digitar uma resposta. Respostas raras pontuam muito mais que as óbvias. Veja como funciona uma rodada, da primeira dica até sua profundidade final.",
            [
                ["h2", "O que acontece numa rodada"],
                ["p", "Abra <a href=\"https://krillion.io\">krillion.io</a> e comece o Daily Dive. Você recebe sete dicas, uma por vez. Cada dica é uma categoria ou pergunta aberta, por exemplo um país terminado em O, um mar, uma ave canora, um prato chinês. Você tem cerca de 25 segundos por dica para digitar uma resposta e confirmar."],
                ["h2", "Por que respostas raras importam"],
                ["p", "O jogo compara sua resposta com o que outros jogadores digitam naquele dia. Respostas comuns quase não movem sua pontuação. Respostas incomuns e específicas te levam mais fundo. Krillion descreve isso com uma metáfora de mergulho: quanto mais raras suas respostas, mais fundo você afunda; as óbvias te mantêm perto da superfície."],
                ["h2", "A pontuação de profundidade"],
                ["ul", ["<b>Respostas raras te afundam</b> — a profundidade é sua pontuação do dia.", "<b>Respostas óbvias quase não contam</b> — uma escolha comum te mantém perto da superfície.", "<b>As mesmas dicas para todos</b> — todos respondem as mesmas sete dicas, então as pontuações diárias são comparáveis.", "<b>Um Daily Dive por dia</b> — a rodada diária renova todo dia; arquivo e modo sem limites permitem jogar mais."]],
                ["h2", "Como digitar uma resposta"],
                ["ul", ["<b>Leia a dica</b> — decida que tipo de coisa ela pede (um país, uma música, um prato).", "<b>Escolha uma resposta específica e válida</b> — nomes precisos geralmente ganham de categorias amplas.", "<b>Digite e confirme rápido</b> — o cronômetro é de cerca de 25 segundos, então fique com sua primeira boa ideia.", "<b>Não precisa de conta</b> — o jogo diário roda grátis no navegador."]],
                ["h2", "Erros comuns de novos jogadores"],
                ["ul", ["<b>Digitar uma categoria ampla</b> — uma palavra geral pontua muito menos que um nome concreto.", "<b>Ficar em dúvida</b> — com 25 segundos, a primeira ideia rara válida costuma ser a melhor.", "<b>Pular a checagem da dica</b> — responder a uma categoria vizinha (uma região em vez de um país) costuma pontuar pior.", "<b>Achar que precisa de um app</b> — Krillion é um jogo de navegador; não há nada para instalar."]],
                ["h2", "Modos além da rodada diária"],
                ["p", "O krillion.io também tem um arquivo de mergulhos passados, pacotes temáticos e um modo sem limites. Se quiser praticar fora da rodada diária, veja nosso <a href=\"/krillion-unlimited/\">guia de Krillion Unlimited</a>."],
                ["h2", "Este é o site oficial de Krillion?"],
                ["p", "Não. É um guia independente. O jogo oficial está em <a href=\"https://krillion.io\">krillion.io</a>; apenas explicamos como ele funciona e como jogar melhor."],
            ],
            "Fontes: krillion.io (jogo oficial) e o texto do próprio jogo, consultado em 11 de outubro de 2026.",
        ],
        "id": [
            "Krillion: Cara Bermain — 7 Petunjuk, 25 Detik, Jawaban Langka",
            "Panduan langkah demi langkah Krillion untuk pemain baru: cara kerja satu ronde Daily Dive, apa yang dihitung sebagai jawaban langka, dan kesalahan umum.",
            "PANDUAN / PEMAIN BARU",
            "Krillion: Cara Bermain — Daily Dive Dijelaskan",
            "Krillion (The Daily Dive) memberi Anda tujuh petunjuk dan sekitar 25 detik untuk masing-masing dalam mengetik jawaban. Jawaban langka memberi skor jauh lebih tinggi daripada jawaban umum. Begini cara satu ronde berjalan, dari petunjuk pertama hingga kedalaman akhir Anda.",
            [
                ["h2", "Apa yang terjadi dalam satu ronde"],
                ["p", "Buka <a href=\"https://krillion.io\">krillion.io</a> dan mulai Daily Dive. Anda mendapat tujuh petunjuk, satu per satu. Setiap petunjuk adalah kategori atau pertanyaan terbuka, misalnya negara berakhiran O, laut, burung penyanyi, hidangan Tionghoa. Anda punya sekitar 25 detik per petunjuk untuk mengetik satu jawaban dan mengonfirmasinya."],
                ["h2", "Mengapa jawaban langka penting"],
                ["p", "Game membandingkan jawaban Anda dengan yang diketik pemain lain hari itu. Jawaban umum nyaris tidak menggerakkan skor. Jawaban yang tidak biasa dan spesifik membawa Anda lebih dalam. Krillion menggambarkannya dengan metafora menyelam: semakin langka jawaban Anda, semakin dalam Anda tenggelam; jawaban umum membuat Anda tetap di permukaan."],
                ["h2", "Skor kedalaman"],
                ["ul", ["<b>Jawaban langka menenggelamkan lebih dalam</b> — kedalaman adalah skor Anda hari itu.", "<b>Jawaban umum hampir tidak dihitung</b> — pilihan biasa membuat Anda di permukaan.", "<b>Petunjuk sama untuk semua orang</b> — semua pemain menjawab tujuh petunjuk yang sama, jadi skor harian bisa dibandingkan.", "<b>Satu Daily Dive per hari</b> — ronde harian diperbarui setiap hari; mode arsip dan tanpa batas memungkinkan bermain lebih banyak."]],
                ["h2", "Cara memasukkan jawaban"],
                ["ul", ["<b>Baca petunjuknya</b> — tentukan jenis hal yang diminta (negara, lagu, hidangan).", "<b>Pilih jawaban spesifik dan valid</b> — nama yang tepat biasanya mengalahkan kategori luas.", "<b>Ketik dan konfirmasi cepat</b> — pengatur waktunya sekitar 25 detik, jadi pertahankan ide pertama yang bagus.", "<b>Tidak perlu akun</b> — game harian berjalan gratis di browser."]],
                ["h2", "Kesalahan umum pemain baru"],
                ["ul", ["<b>Mengetik kategori luas</b> — kata umum memberi skor jauh lebih rendah daripada nama konkret.", "<b>Ragu pada diri sendiri</b> — dengan 25 detik, ide langka valid pertama biasanya yang terbaik.", "<b>Melewatkan pengecekan petunjuk</b> — menjawab kategori yang mirip (wilayah alih-alih negara) biasanya memberi skor lebih rendah.", "<b>Mengira butuh aplikasi</b> — Krillion adalah game browser; tidak ada yang perlu diinstal."]],
                ["h2", "Mode selain ronde harian"],
                ["p", "Krillion.io juga punya arsip penyelaman sebelumnya, paket bertema, dan mode tanpa batas. Jika ingin berlatih di luar ronde harian, lihat panduan <a href=\"/krillion-unlimited/\">Krillion Unlimited</a> kami."],
                ["h2", "Apakah ini situs resmi Krillion?"],
                ["p", "Bukan. Ini panduan independen. Game resminya ada di <a href=\"https://krillion.io\">krillion.io</a>; kami hanya menjelaskan cara kerjanya dan cara bermain lebih baik."],
            ],
            "Sumber: krillion.io (game resmi) dan teks dalam game itu sendiri, diperiksa 11 Oktober 2026.",
        ],
    },
    "tips": {
        "en": [
            "Krillion Tips: How to Think of Rare Answers Fast",
            "Practical Krillion tips to score deeper: how to pick rare answers under a 25-second timer, which categories to prepare, and habits of strong players.",
            "GUIDES / STRATEGY",
            "Krillion Tips: rare answers, faster",
            "You do not need encyclopedic knowledge to score deep in Krillion. These tips focus on habits that produce rare, valid answers in under 25 seconds.",
            [
                ["h2", "Tip 1: prefer the specific over the obvious"],
                ["p", "When a prompt asks for a country, a bird or a dish, the first famous answer is usually the most common one. Ask yourself for a second, more specific idea before typing. A lesser-known valid pick almost always scores deeper."],
                ["h2", "Tip 2: think in subcategories"],
                ["p", "Prompts like \u201ca sea\u201d or \u201ca river\u201d reward rare members: an inland sea, a sea named after a region, a tributary instead of the main river. The less central the example, the rarer it tends to be — as long as it is still valid."],
                ["h2", "Tip 3: prepare the recurring categories"],
                ["p", "Countries, capitals, animals, foods and songs appear often. Build a small mental list for each: unusual capitals, obscure animals, regional dishes. That preparation turns a 25-second prompt into a quick choice."],
                ["h2", "Tip 4: type fast, confirm once"],
                ["p", "The timer punishes hesitation. Type your first valid rare idea and confirm it. Going back to rethink usually costs the round; a decent rare answer on time beats a perfect one you never submitted."],
                ["h2", "Tip 5: rare does not mean long or fancy"],
                ["p", "A short, valid, uncommon name scores better than a long invented one. If the answer must be a real thing in the category, choose real and uncommon, not complicated."],
                ["h2", "Tip 6: practice outside the daily round"],
                ["p", "Krillion.io offers an <a href=\"/krillion-unlimited/\">unlimited mode</a> and themed packs. Repetition outside the daily seven prompts is the fastest way to build the habit of picking rare answers quickly."],
                ["h2", "More help"],
                ["p", "New to the game? Start with our <a href=\"/how-to-play/\">how-to-play guide</a>, then come back to these tips. See also <a href=\"/one-in-a-krillion/\">what \u201cone in a krillion\u201d means</a>."],
            ],
            "Independent tips based on the official game at krillion.io, checked October 11, 2026.",
        ],
        "ru": [
            "Советы по Krillion: как быстро придумывать редкие ответы",
            "Практичные советы по Krillion, чтобы нырять глубже: как выбирать редкие ответы за 25 секунд, какие категории готовить и привычки сильных игроков.",
            "ГАЙДЫ / СТРАТЕГИЯ",
            "Советы по Krillion: редкие ответы быстрее",
            "Чтобы глубоко нырять в Krillion, не нужны энциклопедические знания. Эти советы про привычки, которые дают редкие валидные ответы меньше чем за 25 секунд.",
            [
                ["h2", "Совет 1: конкретное вместо очевидного"],
                ["p", "Когда подсказка просит страну, птицу или блюдо, первый известный ответ обычно самый частый. Прежде чем печатать, спросите себя о второй, более конкретной идее. Менее известный валидный вариант почти всегда даёт большую глубину."],
                ["h2", "Совет 2: думайте подкатегориями"],
                ["p", "Подсказки вроде \u201cморе\u201d или \u201cрека\u201d вознаграждают редкие примеры: внутреннее море, море, названное по региону, приток вместо главной реки. Чем менее центральный пример, тем он обычно реже — пока остаётся валидным."],
                ["h2", "Совет 3: готовьте повторяющиеся категории"],
                ["p", "Страны, столицы, животные, еда и песни появляются часто. Составьте небольшой мысленный список для каждой: необычные столицы, редкие животные, региональные блюда. Такая подготовка превращает 25-секундную подсказку в быстрый выбор."],
                ["h2", "Совет 4: печатайте быстро, подтверждайте один раз"],
                ["p", "Таймер наказывает за колебания. Вводите первую валидную редкую идею и подтверждайте. Возврат к переобдумыванию обычно стоит раунда: приличный редкий ответ вовремя лучше идеального, который вы не отправили."],
                ["h2", "Совет 5: редкое не значит длинное"],
                ["p", "Короткое валидное необычное название даёт больше, чем длинное придуманное. Если ответ должен быть реальным объектом категории, выбирайте реальное и необычное, а не сложное."],
                ["h2", "Совет 6: практикуйтесь вне дневного раунда"],
                ["p", "На krillion.io есть <a href=\"/krillion-unlimited/\">безлимитный режим</a> и тематические наборы. Повторение вне дневных семи подсказок — самый быстрый способ выработать привычку быстро выбирать редкие ответы."],
                ["h2", "Ещё помощь"],
                ["p", "Новичок? Начните с <a href=\"/how-to-play/\">гайда о том, как играть</a>, затем вернитесь к советам. См. также, <a href=\"/one-in-a-krillion/\">что значит \u201cone in a krillion\u201d</a>."],
            ],
            "Независимые советы по официальной игре на krillion.io, проверено 11 октября 2026 года.",
        ],
        "es": [
            "Consejos de Krillion: cómo pensar respuestas raras rápido",
            "Consejos prácticos de Krillion para puntuar más profundo: cómo elegir respuestas raras en 25 segundos, qué categorías preparar y hábitos de jugadores fuertes.",
            "GUÍAS / ESTRATEGIA",
            "Consejos de Krillion: respuestas raras, más rápido",
            "No necesitas conocimientos enciclopédicos para bucear profundo en Krillion. Estos consejos son sobre hábitos que producen respuestas raras y válidas en menos de 25 segundos.",
            [
                ["h2", "Consejo 1: prefiere lo específico a lo obvio"],
                ["p", "Cuando la pista pide un país, un ave o un plato, la primera respuesta famosa suele ser la más común. Pregúntate por una segunda idea más concreta antes de escribir. Una opción válida menos conocida casi siempre puntúa más profundo."],
                ["h2", "Consejo 2: piensa en subcategorías"],
                ["p", "Pistas como \u201cun mar\u201d o \u201cun río\u201d premian miembros raros: un mar interior, un mar llamado por una región, un afluente en vez del río principal. Cuanto menos central es el ejemplo, más raro suele ser, mientras siga siendo válido."],
                ["h2", "Consejo 3: prepara las categorías recurrentes"],
                ["p", "Países, capitales, animales, comidas y canciones aparecen a menudo. Hazte una pequeña lista mental para cada una: capitales inusuales, animales poco conocidos, platos regionales. Esa preparación convierte una pista de 25 segundos en una elección rápida."],
                ["h2", "Consejo 4: escribe rápido, confirma una vez"],
                ["p", "El temporizador castiga la duda. Escribe tu primera idea rara válida y confírmala. Volver a pensar suele costar la ronda; una respuesta rara decente a tiempo gana a una perfecta que nunca enviaste."],
                ["h2", "Consejo 5: raro no significa largo"],
                ["p", "Un nombre corto, válido y poco común puntúa mejor que uno largo inventado. Si la respuesta debe ser algo real de la categoría, elige real y poco común, no complicado."],
                ["h2", "Consejo 6: practica fuera de la ronda diaria"],
                ["p", "Krillion.io ofrece un <a href=\"/krillion-unlimited/\">modo sin límites</a> y packs temáticos. Repetir fuera de las siete pistas diarias es la forma más rápida de crear el hábito de elegir respuestas raras con rapidez."],
                ["h2", "Más ayuda"],
                ["p", "¿Nuevo en el juego? Empieza con nuestra <a href=\"/how-to-play/\">guía de cómo jugar</a> y vuelve a estos consejos. También mira <a href=\"/one-in-a-krillion/\">qué significa \u201cone in a krillion\u201d</a>."],
            ],
            "Consejos independientes basados en el juego oficial en krillion.io, consultado el 11 de octubre de 2026.",
        ],
        "pt": [
            "Dicas de Krillion: como pensar respostas raras rápido",
            "Dicas práticas de Krillion para pontuar mais fundo: como escolher respostas raras em 25 segundos, que categorias preparar e hábitos de bons jogadores.",
            "GUIAS / ESTRATÉGIA",
            "Dicas de Krillion: respostas raras, mais rápido",
            "Você não precisa de conhecimento enciclopédico para mergulhar fundo no Krillion. Estas dicas são sobre hábitos que produzem respostas raras e válidas em menos de 25 segundos.",
            [
                ["h2", "Dica 1: prefira o específico ao óbvio"],
                ["p", "Quando a dica pede um país, uma ave ou um prato, a primeira resposta famosa costuma ser a mais comum. Pergunte-se por uma segunda ideia mais específica antes de digitar. Uma opção válida menos conhecida quase sempre pontua mais fundo."],
                ["h2", "Dica 2: pense em subcategorias"],
                ["p", "Dicas como \u201cum mar\u201d ou \u201cum rio\u201d premiam membros raros: um mar interior, um mar chamado por uma região, um afluente em vez do rio principal. Quanto menos central o exemplo, mais raro ele tende a ser, enquanto continuar válido."],
                ["h2", "Dica 3: prepare as categorias recorrentes"],
                ["p", "Países, capitais, animais, comidas e músicas aparecem com frequência. Monte uma pequena lista mental para cada: capitais incomuns, animais pouco conhecidos, pratos regionais. Essa preparação transforma uma dica de 25 segundos em uma escolha rápida."],
                ["h2", "Dica 4: digite rápido, confirme uma vez"],
                ["p", "O cronômetro pune a hesitação. Digite sua primeira ideia rara válida e confirme. Voltar para repensar costuma custar a rodada; uma resposta rara decente no tempo certo ganha de uma perfeita que você nunca enviou."],
                ["h2", "Dica 5: raro não significa longo"],
                ["p", "Um nome curto, válido e incomum pontua melhor do que um longo inventado. Se a resposta precisa ser algo real da categoria, escolha real e incomum, não complicado."],
                ["h2", "Dica 6: pratique fora da rodada diária"],
                ["p", "O krillion.io oferece um <a href=\"/krillion-unlimited/\">modo sem limites</a> e pacotes temáticos. Repetir fora das sete dicas diárias é o caminho mais rápido para criar o hábito de escolher respostas raras rapidamente."],
                ["h2", "Mais ajuda"],
                ["p", "Novo no jogo? Comece pelo nosso <a href=\"/how-to-play/\">guia de como jogar</a> e volte a estas dicas. Veja também <a href=\"/one-in-a-krillion/\">o que significa \u201cone in a krillion\u201d</a>."],
            ],
            "Dicas independentes baseadas no jogo oficial em krillion.io, consultado em 11 de outubro de 2026.",
        ],
        "id": [
            "Tips Krillion: Cara Cepat Memikirkan Jawaban Langka",
            "Tips praktis Krillion untuk skor lebih dalam: cara memilih jawaban langka dalam 25 detik, kategori yang perlu disiapkan, dan kebiasaan pemain kuat.",
            "PANDUAN / STRATEGI",
            "Tips Krillion: jawaban langka, lebih cepat",
            "Anda tidak butuh pengetahuan ensiklopedis untuk menyelam dalam di Krillion. Tips ini tentang kebiasaan yang menghasilkan jawaban langka dan valid dalam waktu kurang dari 25 detik.",
            [
                ["h2", "Tips 1: pilih yang spesifik, bukan yang umum"],
                ["p", "Saat petunjuk meminta negara, burung, atau hidangan, jawaban terkenal pertama biasanya yang paling umum. Tanyakan pada diri Anda ide kedua yang lebih spesifik sebelum mengetik. Pilihan valid yang kurang dikenal hampir selalu memberi skor lebih dalam."],
                ["h2", "Tips 2: pikirkan dalam subkategori"],
                ["p", "Petunjuk seperti \u201claut\u201d atau \u201csungai\u201d memberi hadiah untuk anggota langka: laut pedalaman, laut yang dinamai dari wilayah, anak sungai alih-alih sungai utama. Semakin tidak sentral contohnya, biasanya semakin langka—selama tetap valid."],
                ["h2", "Tips 3: siapkan kategori yang sering muncul"],
                ["p", "Negara, ibu kota, hewan, makanan, dan lagu sering muncul. Bangun daftar mental kecil untuk masing-masing: ibu kota yang tidak biasa, hewan yang jarang dikenal, hidangan daerah. Persiapan itu mengubah petunjuk 25 detik menjadi pilihan cepat."],
                ["h2", "Tips 4: ketik cepat, konfirmasi sekali"],
                ["p", "Pengatur waktu menghukum keraguan. Ketik ide langka valid pertama Anda dan konfirmasi. Kembali berpikir ulang biasanya mengorbankan ronde; jawaban langka yang layak tepat waktu mengalahkan jawaban sempurna yang tidak pernah Anda kirim."],
                ["h2", "Tips 5: langka bukan berarti panjang"],
                ["p", "Nama pendek, valid, dan tidak umum memberi skor lebih baik daripada nama panjang yang dibuat-buat. Jika jawabannya harus hal nyata dalam kategori itu, pilih yang nyata dan tidak umum, bukan yang rumit."],
                ["h2", "Tips 6: berlatih di luar ronde harian"],
                ["p", "Krillion.io menawarkan <a href=\"/krillion-unlimited/\">mode tanpa batas</a> dan paket bertema. Pengulangan di luar tujuh petunjuk harian adalah cara tercepat membangun kebiasaan memilih jawaban langka dengan cepat."],
                ["h2", "Bantuan lain"],
                ["p", "Baru di game? Mulai dengan <a href=\"/how-to-play/\">panduan cara bermain</a> kami, lalu kembali ke tips ini. Lihat juga <a href=\"/one-in-a-krillion/\">arti \u201cone in a krillion\u201d</a>."],
            ],
            "Tips independen berdasarkan game resmi di krillion.io, diperiksa 11 Oktober 2026.",
        ],
    },
    "krillion-game": {
        "en": [
            "Krillion Game: What It Is and Where to Play",
            "Krillion is a daily browser trivia game about rare answers. Find out what it is, who made it, and where to play for free.",
            "ABOUT THE GAME / OVERVIEW",
            "Krillion Game: rare-answer trivia in your browser",
            "Krillion, officially called The Daily Dive, is a free daily browser trivia game where rare answers score higher than obvious ones. This page covers what it is, its origin and where to play.",
            [
                ["h2", "What is the Krillion game?"],
                ["p", "Krillion is a daily browser game with seven prompts and about 25 seconds each. You type one answer per prompt, and the game scores how rare your answer is compared with other players. The rarer the answer, the deeper your score, described in the game as diving into the ocean."],
                ["h2", "Who made it"],
                ["p", "The current game at krillion.io was built by a solo developer who goes by the pseudonym kp. The name and idea trace back to <b>One in a Krillion</b>, a student game made at DigiPen (2024) that also appears on Steam. Krillion is an independent project, not a big-studio game."],
                ["h2", "Where to play"],
                ["p", "The official game is <a href=\"https://krillion.io\">krillion.io</a>. It runs free in the browser, no account or install required. The daily round uses the same seven prompts for every player, so scores are directly comparable."],
                ["h2", "Why people search for it"],
                ["ul", ["<b>Daily freshness</b> — new prompts every day keep players coming back.", "<b>Comparable scores</b> — everyone answers the same prompts, which makes it shareable.", "<b>Simple rules</b> — seven prompts, one answer each, rarity decides your depth.", "<b>Browser-only</b> — nothing to download."]],
                ["h2", "Frequently asked questions"],
                ["ul", ["<b>Is Krillion free?</b> — Yes, the daily game is free in the browser.", "<b>Is there an app?</b> — Krillion is a browser game; the official experience is played at krillion.io.", "<b>Can I play more than once a day?</b> — The daily round resets daily; krillion.io also has archive, themed packs and an <a href=\"/krillion-unlimited/\">unlimited mode</a>.", "<b>Is this the official site?</b> — No. This is an independent guide to the game."]],
                ["h2", "Start playing better"],
                ["p", "New players: read the <a href=\"/how-to-play/\">how-to-play guide</a>, then our <a href=\"/tips/\">rare-answer tips</a>."],
            ],
            "Sources: krillion.io (official game), DigiPen game showcase, checked October 11, 2026.",
        ],
        "ru": [
            "Игра Krillion: что это и где играть",
            "Krillion — ежедневная браузерная игра-викторина про редкие ответы. Узнайте, что это, кто её сделал и где играть бесплатно.",
            "ОБ ИГРЕ / ОБЗОР",
            "Игра Krillion: редкие ответы в браузере",
            "Krillion, официально называемая The Daily Dive, — бесплатная ежедневная браузерная игра-викторина, где редкие ответы дают больше очков, чем очевидные. На этой странице — что это, происхождение и где играть.",
            [
                ["h2", "Что такое игра Krillion?"],
                ["p", "Krillion — ежедневная браузерная игра с семью подсказками и примерно 25 секундами на каждую. Вы вводите один ответ на подсказку, и игра оценивает, насколько ответ редкий по сравнению с другими игроками. Чем реже ответ, тем глубже счёт, что в игре описано как погружение в океан."],
                ["h2", "Кто её сделал"],
                ["p", "Текущую игру на krillion.io сделал соло-разработчик под псевдонимом kp. Название и идея восходят к <b>One in a Krillion</b> — студенческой игре, созданной в DigiPen (2024), которая также появилась в Steam. Krillion — независимый проект, а не игра большой студии."],
                ["h2", "Где играть"],
                ["p", "Официальная игра — <a href=\"https://krillion.io\">krillion.io</a>. Она бесплатно работает в браузере, без аккаунта и установки. В дневном раунде у всех игроков одни и те же семь подсказок, поэтому счета напрямую сравнимы."],
                ["h2", "Почему по ней ищут"],
                ["ul", ["<b>Ежедневная свежесть</b> — новые подсказки каждый день возвращают игроков.", "<b>Сравнимые счета</b> — все отвечают на одни и те же подсказки, поэтому результатом удобно делиться.", "<b>Простые правила</b> — семь подсказок, по одному ответу, редкость решает глубину.", "<b>Только браузер</b> — ничего не нужно скачивать."]],
                ["h2", "Частые вопросы"],
                ["ul", ["<b>Krillion бесплатная?</b> — Да, дневная игра бесплатна в браузере.", "<b>Есть приложение?</b> — Krillion работает в браузере; официальный опыт — на krillion.io.", "<b>Можно играть чаще раза в день?</b> — Дневной раунд обновляется ежедневно; на krillion.io также есть архив, тематические наборы и <a href=\"/krillion-unlimited/\">безлимитный режим</a>.", "<b>Это официальный сайт?</b> — Нет. Это независимый гайд по игре."]],
                ["h2", "Начните играть лучше"],
                ["p", "Новичкам: прочитайте <a href=\"/how-to-play/\">гайд о том, как играть</a>, затем наши <a href=\"/tips/\">советы по редким ответам</a>."],
            ],
            "Источники: krillion.io (официальная игра), витрина студенческих игр DigiPen, проверено 11 октября 2026 года.",
        ],
        "es": [
            "Krillion Game: qué es y dónde jugar",
            "Krillion es un juego de trivia diario en el navegador sobre respuestas raras. Descubre qué es, quién lo hizo y dónde jugar gratis.",
            "SOBRE EL JUEGO / GENERAL",
            "Krillion Game: trivia de respuestas raras en tu navegador",
            "Krillion, oficialmente llamado The Daily Dive, es un juego de trivia diario gratis en el navegador donde las respuestas raras puntúan más que las obvias. Esta página explica qué es, su origen y dónde jugar.",
            [
                ["h2", "¿Qué es el juego Krillion?"],
                ["p", "Krillion es un juego diario de navegador con siete pistas y unos 25 segundos en cada una. Escribes una respuesta por pista y el juego puntúa lo rara que es tu respuesta frente a otros jugadores. Cuanto más rara es la respuesta, más profunda es tu puntuación, descrita en el juego como un buceo en el océano."],
                ["h2", "Quién lo hizo"],
                ["p", "El juego actual en krillion.io lo creó un desarrollador en solitario bajo el seudónimo kp. El nombre y la idea vienen de <b>One in a Krillion</b>, un juego de estudiantes hecho en DigiPen (2024) que también aparece en Steam. Krillion es un proyecto independiente, no un juego de gran estudio."],
                ["h2", "Dónde jugar"],
                ["p", "El juego oficial está en <a href=\"https://krillion.io\">krillion.io</a>. Corre gratis en el navegador, sin cuenta ni instalación. La ronda diaria usa las mismas siete pistas para todos, así que las puntuaciones son directamente comparables."],
                ["h2", "Por qué se busca este juego"],
                ["ul", ["<b>Frescura diaria</b> — pistas nuevas cada día hacen volver a los jugadores.", "<b>Puntuaciones comparables</b> — todos responden las mismas pistas, lo que lo hace compartible.", "<b>Reglas simples</b> — siete pistas, una respuesta cada una, la rareza decide tu profundidad.", "<b>Solo navegador</b> — nada que descargar."]],
                ["h2", "Preguntas frecuentes"],
                ["ul", ["<b>¿Krillion es gratis?</b> — Sí, el juego diario es gratis en el navegador.", "<b>¿Hay una app?</b> — Krillion es un juego de navegador; la experiencia oficial se juega en krillion.io.", "<b>¿Puedo jugar más de una vez al día?</b> — La ronda diaria se renueva a diario; krillion.io también tiene archivo, packs temáticos y un <a href=\"/krillion-unlimited/\">modo sin límites</a>.", "<b>¿Es este el sitio oficial?</b> — No. Es una guía independiente del juego."]],
                ["h2", "Empieza a jugar mejor"],
                ["p", "Nuevos jugadores: leed la <a href=\"/how-to-play/\">guía de cómo jugar</a> y luego nuestros <a href=\"/tips/\">consejos de respuestas raras</a>."],
            ],
            "Fuentes: krillion.io (juego oficial), exhibición de juegos de DigiPen, consultado el 11 de octubre de 2026.",
        ],
        "pt": [
            "Krillion Game: o que é e onde jogar",
            "Krillion é um jogo de trivia diário no navegador sobre respostas raras. Descubra o que é, quem o fez e onde jogar de graça.",
            "SOBRE O JOGO / VISÃO GERAL",
            "Krillion Game: trivia de respostas raras no seu navegador",
            "Krillion, oficialmente chamado The Daily Dive, é um jogo de trivia diário e gratuito no navegador onde respostas raras pontuam mais que as óbvias. Esta página cobre o que é, sua origem e onde jogar.",
            [
                ["h2", "O que é o jogo Krillion?"],
                ["p", "Krillion é um jogo diário de navegador com sete dicas e cerca de 25 segundos em cada uma. Você digita uma resposta por dica e o jogo pontua o quão rara sua resposta é frente a outros jogadores. Quanto mais rara a resposta, mais profunda sua pontuação, descrita no jogo como um mergulho no oceano."],
                ["h2", "Quem o fez"],
                ["p", "O jogo atual em krillion.io foi criado por um desenvolvedor solo sob o pseudônimo kp. O nome e a ideia vêm de <b>One in a Krillion</b>, um jogo de estudantes feito na DigiPen (2024) que também aparece na Steam. Krillion é um projeto independente, não um jogo de grande estúdio."],
                ["h2", "Onde jogar"],
                ["p", "O jogo oficial está em <a href=\"https://krillion.io\">krillion.io</a>. Ele roda grátis no navegador, sem conta nem instalação. A rodada diária usa as mesmas sete dicas para todos, então as pontuações são diretamente comparáveis."],
                ["h2", "Por que as pessoas buscam por ele"],
                ["ul", ["<b>Frescor diário</b> — dicas novas todo dia fazem os jogadores voltarem.", "<b>Pontuações comparáveis</b> — todos respondem as mesmas dicas, o que o torna compartilhável.", "<b>Regras simples</b> — sete dicas, uma resposta cada, a raridade decide sua profundidade.", "<b>Só navegador</b> — nada para baixar."]],
                ["h2", "Perguntas frequentes"],
                ["ul", ["<b>Krillion é grátis?</b> — Sim, o jogo diário é grátis no navegador.", "<b>Tem um app?</b> — Krillion é um jogo de navegador; a experiência oficial é jogada em krillion.io.", "<b>Posso jogar mais de uma vez por dia?</b> — A rodada diária renova todo dia; krillion.io também tem arquivo, pacotes temáticos e um <a href=\"/krillion-unlimited/\">modo sem limites</a>.", "<b>Este é o site oficial?</b> — Não. É um guia independente do jogo."]],
                ["h2", "Comece a jogar melhor"],
                ["p", "Novos jogadores: leiam o <a href=\"/how-to-play/\">guia de como jogar</a> e depois nossas <a href=\"/tips/\">dicas de respostas raras</a>."],
            ],
            "Fontes: krillion.io (jogo oficial), vitrine de jogos da DigiPen, consultado em 11 de outubro de 2026.",
        ],
        "id": [
            "Game Krillion: Apa Itu dan Tempat Bermain",
            "Krillion adalah game trivia harian di browser tentang jawaban langka. Cari tahu apa itu, siapa pembuatnya, dan tempat bermain gratis.",
            "TENTANG GAME / RINGKASAN",
            "Game Krillion: trivia jawaban langka di browser Anda",
            "Krillion, yang resmi disebut The Daily Dive, adalah game trivia harian gratis di browser di mana jawaban langka memberi skor lebih tinggi daripada jawaban umum. Halaman ini membahas apa itu, asal-usulnya, dan tempat bermain.",
            [
                ["h2", "Apa itu game Krillion?"],
                ["p", "Krillion adalah game harian di browser dengan tujuh petunjuk dan sekitar 25 detik untuk masing-masing. Anda mengetik satu jawaban per petunjuk, dan game memberi skor seberapa langka jawaban Anda dibanding pemain lain. Semakin langka jawabannya, semakin dalam skor Anda, yang digambarkan dalam game sebagai menyelam ke laut."],
                ["h2", "Siapa pembuatnya"],
                ["p", "Game saat ini di krillion.io dibuat oleh pengembang solo dengan nama samaran kp. Nama dan idenya berakar dari <b>One in a Krillion</b>, game mahasiswa yang dibuat di DigiPen (2024) dan juga muncul di Steam. Krillion adalah proyek independen, bukan game studio besar."],
                ["h2", "Tempat bermain"],
                ["p", "Game resminya ada di <a href=\"https://krillion.io\">krillion.io</a>. Game berjalan gratis di browser, tanpa akun atau instalasi. Ronde harian memakai tujuh petunjuk yang sama untuk semua pemain, jadi skor bisa langsung dibandingkan."],
                ["h2", "Kenapa orang mencari game ini"],
                ["ul", ["<b>Kesegaran harian</b> — petunjuk baru setiap hari membuat pemain kembali.", "<b>Skor yang bisa dibandingkan</b> — semua menjawab petunjuk yang sama, sehingga mudah dibagikan.", "<b>Aturan sederhana</b> — tujuh petunjuk, satu jawaban masing-masing, kelangkaan menentukan kedalaman Anda.", "<b>Hanya browser</b> — tidak ada yang perlu diunduh."]],
                ["h2", "Pertanyaan yang sering diajukan"],
                ["ul", ["<b>Apakah Krillion gratis?</b> — Ya, game hariannya gratis di browser.", "<b>Apakah ada aplikasinya?</b> — Krillion adalah game browser; pengalaman resminya dimainkan di krillion.io.", "<b>Bisa bermain lebih dari sekali sehari?</b> — Ronde harian diperbarui setiap hari; krillion.io juga punya arsip, paket bertema, dan <a href=\"/krillion-unlimited/\">mode tanpa batas</a>.", "<b>Apakah ini situs resmi?</b> — Bukan. Ini panduan independen tentang game ini."]],
                ["h2", "Mulai bermain lebih baik"],
                ["p", "Pemain baru: baca <a href=\"/how-to-play/\">panduan cara bermain</a>, lalu <a href=\"/tips/\">tips jawaban langka</a> kami."],
            ],
            "Sumber: krillion.io (game resmi), etalase game DigiPen, diperiksa 11 Oktober 2026.",
        ],
    },
    "krillion-unlimited": {
        "en": [
            "Krillion Unlimited: How to Play Endless Krillion",
            "Krillion Unlimited lets you play beyond the daily seven prompts. See the official unlimited mode and how community endless versions compare.",
            "GUIDES / MODES",
            "Krillion Unlimited: play beyond the daily dive",
            "The daily round gives you seven prompts. Krillion Unlimited removes that limit. This page explains the official unlimited mode and what community endless versions offer.",
            [
                ["h2", "What is Krillion Unlimited?"],
                ["p", "Krillion Unlimited is a way to play Krillion without waiting for tomorrow's daily dive. Instead of seven fixed prompts, you keep answering category prompts one after another, scoring rarity the same way. It is useful for practice and for players who want more than one round a day."],
                ["h2", "The official unlimited mode"],
                ["p", "krillion.io itself offers an <b>UNLIMITED</b> mode (labelled with the infinity symbol) alongside archive and themed packs. Start the daily dive on the official site and look for the UNLIMITED entry. Because it is the official implementation, answers and scoring follow the same rules as the daily round."],
                ["h2", "Community endless versions"],
                ["p", "Several independent sites offer their own endless Krillion-style games, for example playdaily.org and alldle.net. These are third-party projects, not the official game, and their answer pools and scoring can differ. Play them at your own discretion; for the authentic experience use krillion.io."],
                ["h2", "Why players look for it"],
                ["ul", ["<b>Practice without waiting</b> — endless rounds mean more reps before the next daily dive.", "<b>Rarity habits</b> — repeated play builds the habit of fast rare answers.", "<b>Beating the daily cap</b> — one round a day can feel short once you are hooked."]],
                ["h2", "Tips for endless rounds"],
                ["p", "The same <a href=\"/tips/\">rare-answer tips</a> apply: prefer specific answers, think in subcategories and type fast. Endless mode is a low-stakes place to experiment with unusual answers."],
            ],
            "Sources: krillion.io (official modes), checked October 11, 2026. Community sites listed for reference only.",
        ],
        "ru": [
            "Krillion Unlimited: как играть без ограничений",
            "Krillion Unlimited позволяет играть сверх ежедневных семи подсказок. Узнайте про официальный безлимитный режим и чем отличаются сторонние бесконечные версии.",
            "ГАЙДЫ / РЕЖИМЫ",
            "Krillion Unlimited: играйте сверх дневного погружения",
            "Дневной раунд даёт семь подсказок. Krillion Unlimited убирает это ограничение. На этой странице — официальный безлимитный режим и что предлагают сторонние бесконечные версии.",
            [
                ["h2", "Что такое Krillion Unlimited?"],
                ["p", "Krillion Unlimited — способ играть в Krillion, не дожидаясь завтрашнего дневного погружения. Вместо семи фиксированных подсказок вы отвечаете на подсказки-категории одну за другой, и редкость оценивается так же. Это удобно для практики и для тех, кому одного раунда в день мало."],
                ["h2", "Официальный безлимитный режим"],
                ["p", "На самом krillion.io есть режим <b>UNLIMITED</b> (обозначен символом бесконечности) вместе с архивом и тематическими наборами. Начните дневное погружение на официальном сайте и найдите пункт UNLIMITED. Так как это официальная реализация, ответы и очки следуют тем же правилам, что и в дневном раунде."],
                ["h2", "Сторонние бесконечные версии"],
                ["p", "Несколько независимых сайтов предлагают собственные бесконечные игры в стиле Krillion, например playdaily.org и alldle.net. Это сторонние проекты, а не официальная игра, и их наборы ответов и очки могут отличаться. Играйте на своё усмотрение; для аутентичного опыта используйте krillion.io."],
                ["h2", "Зачем это ищут"],
                ["ul", ["<b>Практика без ожидания</b> — бесконечные раунды дают больше повторений до следующего дневного погружения.", "<b>Привычка к редкости</b> — повторная игра вырабатывает привычку быстро давать редкие ответы.", "<b>Обход дневного лимита</b> — одного раунда в день может быть мало, когда вы увлеклись."]],
                ["h2", "Советы для бесконечных раундов"],
                ["p", "Применимы те же <a href=\"/tips/\">советы по редким ответам</a>: выбирайте конкретное, думайте подкатегориями и печатайте быстро. Безлимитный режим — место без риска для экспериментов с необычными ответами."],
            ],
            "Источники: krillion.io (официальные режимы), проверено 11 октября 2026 года. Сторонние сайты приведены только для справки.",
        ],
        "es": [
            "Krillion Unlimited: cómo jugar sin límites",
            "Krillion Unlimited te permite jugar más allá de las siete pistas diarias. Mira el modo sin límites oficial y cómo son las versiones infinitas de la comunidad.",
            "GUÍAS / MODOS",
            "Krillion Unlimited: juega más allá del Daily Dive",
            "La ronda diaria te da siete pistas. Krillion Unlimited elimina ese límite. Esta página explica el modo sin límites oficial y qué ofrecen las versiones infinitas de la comunidad.",
            [
                ["h2", "¿Qué es Krillion Unlimited?"],
                ["p", "Krillion Unlimited es una forma de jugar a Krillion sin esperar al Daily Dive de mañana. En lugar de siete pistas fijas, respondes pistas por categoría una tras otra, puntuando la rareza igual. Es útil para practicar y para quienes quieren más de una ronda al día."],
                ["h2", "El modo sin límites oficial"],
                ["p", "krillion.io ofrece un modo <b>UNLIMITED</b> (con el símbolo de infinito) junto al archivo y los packs temáticos. Empieza el Daily Dive en el sitio oficial y busca la entrada UNLIMITED. Como es la implementación oficial, las respuestas y la puntuación siguen las mismas reglas que la ronda diaria."],
                ["h2", "Versiones infinitas de la comunidad"],
                ["p", "Varios sitios independientes ofrecen sus propios juegos infinitos estilo Krillion, por ejemplo playdaily.org y alldle.net. Son proyectos de terceros, no el juego oficial, y sus conjuntos de respuestas y puntuaciones pueden diferir. Juega bajo tu propio criterio; para la experiencia auténtica usa krillion.io."],
                ["h2", "Por qué se busca"],
                ["ul", ["<b>Practicar sin esperar</b> — las rondas infinitas dan más repeticiones antes del siguiente Daily Dive.", "<b>Hábito de rareza</b> — jugar repetido crea el hábito de respuestas raras rápidas.", "<b>Superar el límite diario</b> — una ronda al día puede quedarse corta cuando engancha."]],
                ["h2", "Consejos para rondas infinitas"],
                ["p", "Vale lo mismo de los <a href=\"/tips/\">consejos de respuestas raras</a>: prefiere lo específico, piensa en subcategorías y escribe rápido. El modo sin límites es un lugar sin riesgo para experimentar con respuestas inusuales."],
            ],
            "Fuentes: krillion.io (modos oficiales), consultado el 11 de octubre de 2026. Los sitios de la comunidad se citan solo como referencia.",
        ],
        "pt": [
            "Krillion Unlimited: como jogar sem limites",
            "Krillion Unlimited permite jogar além das sete dicas diárias. Veja o modo sem limites oficial e como são as versões infinitas da comunidade.",
            "GUIAS / MODOS",
            "Krillion Unlimited: jogue além do Daily Dive",
            "A rodada diária dá sete dicas. Krillion Unlimited remove esse limite. Esta página explica o modo sem limites oficial e o que as versões infinitas da comunidade oferecem.",
            [
                ["h2", "O que é Krillion Unlimited?"],
                ["p", "Krillion Unlimited é um jeito de jogar Krillion sem esperar o Daily Dive de amanhã. Em vez de sete dicas fixas, você responde dicas por categoria uma após a outra, pontuando a raridade do mesmo jeito. É útil para praticar e para quem quer mais de uma rodada por dia."],
                ["h2", "O modo sem limites oficial"],
                ["p", "O próprio krillion.io oferece um modo <b>UNLIMITED</b> (com o símbolo de infinito) junto com arquivo e pacotes temáticos. Comece o Daily Dive no site oficial e procure a entrada UNLIMITED. Por ser a implementação oficial, respostas e pontuação seguem as mesmas regras da rodada diária."],
                ["h2", "Versões infinitas da comunidade"],
                ["p", "Vários sites independentes oferecem seus próprios jogos infinitos estilo Krillion, por exemplo playdaily.org e alldle.net. São projetos de terceiros, não o jogo oficial, e seus conjuntos de respostas e pontuações podem diferir. Jogue por sua conta; para a experiência autêntica use krillion.io."],
                ["h2", "Por que as pessoas procuram"],
                ["ul", ["<b>Praticar sem esperar</b> — rodadas infinitas dão mais repetições antes do próximo Daily Dive.", "<b>Hábito de raridade</b> — jogar repetido cria o hábito de respostas raras rápidas.", "<b>Furar o limite diário</b> — uma rodada por dia pode parecer curta quando você vicia."]],
                ["h2", "Dicas para rodadas infinitas"],
                ["p", "Valem as mesmas <a href=\"/tips/\">dicas de respostas raras</a>: prefira o específico, pense em subcategorias e digite rápido. O modo sem limites é um lugar sem risco para experimentar respostas incomuns."],
            ],
            "Fontes: krillion.io (modos oficiais), consultado em 11 de outubro de 2026. Sites da comunidade citados apenas como referência.",
        ],
        "id": [
            "Krillion Unlimited: Cara Bermain Tanpa Batas",
            "Krillion Unlimited memungkinkan Anda bermain melampaui tujuh petunjuk harian. Lihat mode tanpa batas resmi dan bagaimana versi tanpa akhir dari komunitas.",
            "PANDUAN / MODE",
            "Krillion Unlimited: bermain melampaui penyelaman harian",
            "Ronde harian memberi Anda tujuh petunjuk. Krillion Unlimited menghapus batas itu. Halaman ini menjelaskan mode tanpa batas resmi dan apa yang ditawarkan versi tanpa akhir komunitas.",
            [
                ["h2", "Apa itu Krillion Unlimited?"],
                ["p", "Krillion Unlimited adalah cara bermain Krillion tanpa menunggu penyelaman harian besok. Alih-alih tujuh petunjuk tetap, Anda terus menjawab petunjuk kategori satu per satu, dengan penilaian kelangkaan yang sama. Ini berguna untuk latihan dan untuk pemain yang ingin lebih dari satu ronde sehari."],
                ["h2", "Mode tanpa batas resmi"],
                ["p", "krillion.io sendiri menawarkan mode <b>UNLIMITED</b> (ditandai simbol tak hingga) bersama arsip dan paket bertema. Mulai Daily Dive di situs resmi dan cari entri UNLIMITED. Karena ini implementasi resmi, jawaban dan skor mengikuti aturan yang sama dengan ronde harian."],
                ["h2", "Versi tanpa akhir dari komunitas"],
                ["p", "Beberapa situs independen menawarkan game tanpa akhir ala Krillion sendiri, misalnya playdaily.org dan alldle.net. Itu proyek pihak ketiga, bukan game resmi, dan kumpulan jawaban serta skornya bisa berbeda. Mainkan dengan bijak; untuk pengalaman autentik gunakan krillion.io."],
                ["h2", "Kenapa pemain mencarinya"],
                ["ul", ["<b>Latihan tanpa menunggu</b> — ronde tanpa akhir memberi lebih banyak pengulangan sebelum penyelaman harian berikutnya.", "<b>Kebiasaan kelangkaan</b> — bermain berulang membangun kebiasaan jawaban langka yang cepat.", "<b>Melewati batas harian</b> — satu ronde sehari bisa terasa pendek setelah Anda kecanduan."]],
                ["h2", "Tips untuk ronde tanpa akhir"],
                ["p", "<a href=\"/tips/\">Tips jawaban langka</a> yang sama berlaku: pilih yang spesifik, pikirkan subkategori, dan ketik cepat. Mode tanpa batas adalah tempat tanpa risiko untuk bereksperimen dengan jawaban yang tidak biasa."],
            ],
            "Sumber: krillion.io (mode resmi), diperiksa 11 Oktober 2026. Situs komunitas dicantumkan hanya sebagai referensi.",
        ],
    },
    "one-in-a-krillion": {
        "en": [
            "One in a Krillion: Meaning and Origin",
            "What does \u201cone in a krillion\u201d mean? It started as a DigiPen student game title and became Krillion's phrase for an ultra-rare answer.",
            "ABOUT THE GAME / PHRASE",
            "One in a Krillion: meaning and where it comes from",
            "\u201cOne in a krillion\u201d plays on \u201cone in a million\u201d and means something incredibly rare. In the Krillion game it is the dream outcome: an answer so rare it feels like one in a krillion.",
            [
                ["h2", "What does \u201cone in a krillion\u201d mean?"],
                ["p", "The phrase exaggerates \u201cone in a million\u201d and even \u201cone in a billion\u201d: if a million is common, a krillion means something vanishingly rare. People use it for a result that seems almost impossible — like an answer almost nobody else gave."],
                ["h2", "Where the name comes from"],
                ["p", "The title traces to <b>One in a Krillion</b>, a student game made at DigiPen in 2024. The project later became the basis for the daily browser game now at krillion.io, which keeps the phrase as its identity: the game's tagline is literally \u201cOne in a krillion.\u201d"],
                ["h2", "How the phrase is used in the game"],
                ["p", "In Krillion, scoring rewards rarity, so the most unusual valid answers are the closest thing to \u201cone in a krillion.\u201d When a player submits an answer almost nobody else typed, the depth it grants matches the phrase. It also appears on Steam as a playable version of the original student game."],
                ["h2", "Is it an official phrase?"],
                ["p", "The phrase and game name are used by the independent developer of krillion.io; this guide is not affiliated. We simply explain the meaning and history for people who encounter the term."],
                ["h2", "Related pages"],
                ["p", "Learn <a href=\"/how-to-play/\">how to play</a>, get <a href=\"/tips/\">rare-answer tips</a>, or read about <a href=\"/krillion-unlimited/\">Krillion Unlimited</a>."],
            ],
            "Sources: DigiPen game showcase (2024), krillion.io, checked October 11, 2026.",
        ],
        "ru": [
            "One in a Krillion: значение и происхождение",
            "Что значит \u201cone in a krillion\u201d? Фраза началась как название студенческой игры в DigiPen и стала в Krillion обозначением сверхредкого ответа.",
            "ОБ ИГРЕ / ФРАЗА",
            "One in a Krillion: значение и откуда оно взялось",
            "\u201cOne in a krillion\u201d обыгрывает \u201cone in a million\u201d и означает невероятно редкое. В игре Krillion это мечта: ответ настолько редкий, что ощущается как один на крilлион.",
            [
                ["h2", "Что значит \u201cone in a krillion\u201d?"],
                ["p", "Фраза преувеличивает \u201cone in a million\u201d и даже \u201cone in a billion\u201d: если миллион — это обычно, то крilлион означает что-то исчезающе редкое. Люди используют её для результата, который кажется почти невозможным, — например, ответа, который почти никто не дал."],
                ["h2", "Откуда взялось название"],
                ["p", "Название восходит к <b>One in a Krillion</b> — студенческой игре, созданной в DigiPen в 2024 году. Проект позже стал основой ежедневной браузерной игры на krillion.io, которая сохранила фразу как свою идентичность: слоган игры буквально звучит \u201cOne in a krillion.\u201d"],
                ["h2", "Как фраза используется в игре"],
                ["p", "В Krillion очки начисляются за редкость, поэтому самые необычные валидные ответы ближе всего к \u201cone in a krillion.\u201d Когда игрок вводит ответ, которого почти никто не написал, глубина, которую он даёт, соответствует фразе. Она также появляется в Steam как играбельная версия оригинальной студенческой игры."],
                ["h2", "Это официальная фраза?"],
                ["p", "Фраза и название игры используются независимым разработчиком krillion.io; этот гайд не связан с ним. Мы лишь объясняем значение и историю для тех, кто встретил термин."],
                ["h2", "Связанные страницы"],
                ["p", "Узнайте, <a href=\"/how-to-play/\">как играть</a>, получите <a href=\"/tips/\">советы по редким ответам</a> или почитайте про <a href=\"/krillion-unlimited/\">Krillion Unlimited</a>."],
            ],
            "Источники: витрина студенческих игр DigiPen (2024), krillion.io, проверено 11 октября 2026 года.",
        ],
        "es": [
            "One in a Krillion: significado y origen",
            "¿Qué significa \u201cone in a krillion\u201d? Empezó como título de un juego estudiantil de DigiPen y se convirtió en la frase de Krillion para una respuesta ultrarara.",
            "SOBRE EL JUEGO / FRASE",
            "One in a Krillion: significado y de dónde viene",
            "\u201cOne in a krillion\u201d juega con \u201cone in a million\u201d y significa algo increíblemente raro. En el juego Krillion es el resultado soñado: una respuesta tan rara que se siente como una entre un krillion.",
            [
                ["h2", "¿Qué significa \u201cone in a krillion\u201d?"],
                ["p", "La frase exagera \u201cone in a million\u201d e incluso \u201cone in a billion\u201d: si un millón es común, un krillion significa algo extraordinariamente raro. La gente la usa para un resultado que parece casi imposible, como una respuesta que casi nadie más dio."],
                ["h2", "De dónde viene el nombre"],
                ["p", "El título viene de <b>One in a Krillion</b>, un juego estudiantil hecho en DigiPen en 2024. El proyecto después se convirtió en la base del juego diario de navegador que ahora está en krillion.io, que conserva la frase como identidad: el lema del juego es literalmente \u201cOne in a krillion.\u201d"],
                ["h2", "Cómo se usa la frase en el juego"],
                ["p", "En Krillion la puntuación premia la rareza, así que las respuestas válidas más inusuales son lo más cercano a \u201cone in a krillion.\u201d Cuando un jugador envía una respuesta que casi nadie escribió, la profundidad que otorga corresponde a la frase. También aparece en Steam como versión jugable del juego estudiantil original."],
                ["h2", "¿Es una frase oficial?"],
                ["p", "La frase y el nombre del juego los usa el desarrollador independiente de krillion.io; esta guía no está afiliada. Solo explicamos el significado y la historia para quienes encuentren el término."],
                ["h2", "Páginas relacionadas"],
                ["p", "Aprende <a href=\"/how-to-play/\">cómo jugar</a>, mira los <a href=\"/tips/\">consejos de respuestas raras</a> o lee sobre <a href=\"/krillion-unlimited/\">Krillion Unlimited</a>."],
            ],
            "Fuentes: exhibición de juegos de DigiPen (2024), krillion.io, consultado el 11 de octubre de 2026.",
        ],
        "pt": [
            "One in a Krillion: significado e origem",
            "O que significa \u201cone in a krillion\u201d? Começou como título de um jogo estudantil da DigiPen e virou a frase de Krillion para uma resposta ultrarara.",
            "SOBRE O JOGO / FRASE",
            "One in a Krillion: significado e de onde vem",
            "\u201cOne in a krillion\u201d brinca com \u201cone in a million\u201d e significa algo incrivelmente raro. No jogo Krillion é o resultado dos sonhos: uma resposta tão rara que parece uma em um krillion.",
            [
                ["h2", "O que significa \u201cone in a krillion\u201d?"],
                ["p", "A frase exagera \u201cone in a million\u201d e até \u201cone in a billion\u201d: se um milhão é comum, um krillion significa algo extraordinariamente raro. As pessoas usam para um resultado que parece quase impossível — como uma resposta que quase ninguém mais deu."],
                ["h2", "De onde vem o nome"],
                ["p", "O título vem de <b>One in a Krillion</b>, um jogo estudantil feito na DigiPen em 2024. O projeto depois virou a base do jogo diário de navegador que agora está em krillion.io, que mantém a frase como identidade: o slogan do jogo é literalmente \u201cOne in a krillion.\u201d"],
                ["h2", "Como a frase é usada no jogo"],
                ["p", "No Krillion a pontuação premia a raridade, então as respostas válidas mais incomuns são o mais perto de \u201cone in a krillion.\u201d Quando um jogador envia uma resposta que quase ninguém digitou, a profundidade que ela concede corresponde à frase. Também aparece na Steam como versão jogável do jogo estudantil original."],
                ["h2", "É uma frase oficial?"],
                ["p", "A frase e o nome do jogo são usados pelo desenvolvedor independente de krillion.io; este guia não tem afiliação. Apenas explicamos o significado e a história para quem encontra o termo."],
                ["h2", "Páginas relacionadas"],
                ["p", "Aprenda <a href=\"/how-to-play/\">como jogar</a>, veja as <a href=\"/tips/\">dicas de respostas raras</a> ou leia sobre <a href=\"/krillion-unlimited/\">Krillion Unlimited</a>."],
            ],
            "Fontes: vitrine de jogos da DigiPen (2024), krillion.io, consultado em 11 de outubro de 2026.",
        ],
        "id": [
            "One in a Krillion: Arti dan Asal-usulnya",
            "Apa arti \u201cone in a krillion\u201d? Frasa ini berawal sebagai judul game mahasiswa DigiPen dan menjadi ungkapan Krillion untuk jawaban yang sangat langka.",
            "TENTANG GAME / FRASA",
            "One in a Krillion: arti dan asal-usulnya",
            "\u201cOne in a krillion\u201d memainkan \u201cone in a million\u201d dan berarti sesuatu yang sangat langka. Dalam game Krillion ini adalah hasil impian: jawaban yang sangat langka sehingga terasa seperti satu dari sekrillion.",
            [
                ["h2", "Apa arti \u201cone in a krillion\u201d?"],
                ["p", "Frasa ini melebih-lebihkan \u201cone in a million\u201d dan bahkan \u201cone in a billion\u201d: jika satu juta itu umum, satu krillion berarti sesuatu yang sangat langka. Orang menggunakannya untuk hasil yang terasa hampir mustahil — seperti jawaban yang hampir tidak diberikan orang lain."],
                ["h2", "Dari mana nama ini berasal"],
                ["p", "Judulnya berakar dari <b>One in a Krillion</b>, game mahasiswa yang dibuat di DigiPen pada 2024. Proyek itu kemudian menjadi dasar game harian di browser yang sekarang ada di krillion.io, yang mempertahankan frasa ini sebagai identitasnya: tagline game-nya memang \u201cOne in a krillion.\u201d"],
                ["h2", "Bagaimana frasa ini dipakai dalam game"],
                ["p", "Di Krillion, skor memberi hadiah pada kelangkaan, jadi jawaban valid paling tidak biasa adalah yang paling dekat dengan \u201cone in a krillion.\u201d Saat pemain mengirim jawaban yang hampir tidak diketik orang lain, kedalaman yang diberikannya sesuai dengan frasa itu. Frasa ini juga muncul di Steam sebagai versi game mahasiswa asli yang bisa dimainkan."],
                ["h2", "Apakah ini frasa resmi?"],
                ["p", "Frasa dan nama game digunakan oleh pengembang independen krillion.io; panduan ini tidak berafiliasi. Kami hanya menjelaskan makna dan sejarahnya bagi yang menemukan istilah ini."],
                ["h2", "Halaman terkait"],
                ["p", "Pelajari <a href=\"/how-to-play/\">cara bermain</a>, dapatkan <a href=\"/tips/\">tips jawaban langka</a>, atau baca tentang <a href=\"/krillion-unlimited/\">Krillion Unlimited</a>."],
            ],
            "Sumber: etalase game DigiPen (2024), krillion.io, diperiksa 11 Oktober 2026.",
        ],
    },
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render_sections(sections):
    out = []
    for tag, content in sections:
        if tag == "h2":
            out.append(f"<h2>{content}</h2>")
        elif tag == "p":
            out.append(f"<p>{content}</p>")
        elif tag == "ul":
            out.append("<ul>" + "".join(f"<li>{li}</li>" for li in content) + "</ul>")
    return "\n".join(out)

def hreflang_block(lang, path):
    out = []
    for lo in ORDER:
        href = f"{KR}{path}" if lo == "en" else f"{KR}/{lo}{path}"
        out.append(f'<link rel="alternate" hreflang="{lo}" href="{href}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{KR}{path}">')
    return "\n".join(out)

def lang_nav(lang, path):
    out = []
    for lo in ORDER:
        href = path if lo == "en" else f"/{lo}{path}"
        cur = ' aria-current="page"' if lo == lang else ""
        out.append(f'<a href="{href}" lang="{lo}" hreflang="{lo}"{cur}>{LANG_LABELS[lo]}</a>')
    return "".join(out)

def breadcrumbs_json(lang, items):
    return json.dumps(items, ensure_ascii=False)

def build_page(lang, slug, page):
    t, d, eyebrow, h1, intro, sections, fine = page
    L = LANGS.get(lang, EN)
    path = f"/{slug}/" if lang == "en" else f"/{lang}/{slug}/"
    url = f"{KR}{path}"
    short = PAGE_SHORT[slug][lang]
    home_href = "/" if lang == "en" else f"/{lang}/"
    guides_href = "/" if lang == "en" else f"/{lang}/"
    bread = breadcrumbs_json(lang, [
        {"@type": "ListItem", "position": 1, "name": L["home"], "item": f"{KR}/"},
        {"@type": "ListItem", "position": 2, "name": short, "item": url},
    ])
    crumb = (f'<nav class="breadcrumbs" aria-label="Breadcrumb">'
             f'<a href="{home_href}">{L["home"]}</a><span aria-hidden="true">›</span>'
             f'<span aria-current="page">{short}</span></nav>')
    header_nav = "".join(f'<a href="{h}">{txt}</a>' for txt, h in L["header_nav"])
    footer_nav = "".join(f'<a href="{h}">{txt}</a>' for txt, h in L["footer_nav"])
    name_ld = json.dumps(t, ensure_ascii=False)
    desc_ld = json.dumps(d, ensure_ascii=False)
    fine_html = f'<p class="fine">{fine}</p>' if fine else ""
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><title>{esc(t)}</title><meta name="description" content="{esc(d)}"><meta name="theme-color" content="#15324a"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/style.css?v=20261012"><link rel="canonical" href="{url}">{hreflang_block(lang, f"/{slug}/")}<meta property="og:type" content="website"><meta property="og:title" content="{esc(t)}"><meta property="og:description" content="{esc(d)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebPage", "name": {name_ld}, "url": "{url}", "description": {desc_ld}, "inLanguage": "{lang}", "isPartOf": {{"@type": "WebSite", "name": "Krillion Guide", "url": "{KR}/"}}}}</script><script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": {bread}}}</script></head><body><a class="skip" href="#main">{L['skip']}</a><header><a class="brand" href="{home_href}">k<span>↗</span> <b>krillion guide</b></a><nav aria-label="Main">{header_nav}</nav></header><nav class="languages" aria-label="{L['lang_label']}">{lang_nav(lang, f"/{slug}/")}</nav><main id="main"><article class="article">{crumb}<p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(h1)}</h1><p class="intro">{intro}</p>{render_sections(sections)}{fine_html}</article></main><footer><a class="brand" href="{home_href}">krillion guide<span>↗</span></a><p>{L['footer_desc']}</p><nav aria-label="Footer">{footer_nav}</nav></footer></body></html>
"""

def build_index(lang):
    L = LANGS.get(lang, EN)
    home_href = "/" if lang == "en" else f"/{lang}/"
    path = "/" if lang == "en" else f"/{lang}/"
    url = f"{KR}/" if lang == "en" else f"{KR}/{lang}/"
    if lang == "en":
        title = "Krillion Answers Today & Guide — Daily Dive Answers, Tips & How to Play"
        desc = "Krillion answers today, how to play the Daily Dive, tips for rare answers, unlimited mode and what one in a krillion means — an independent guide to the daily trivia game."
        eyebrow = "DAILY ANSWERS / INDEPENDENT GUIDE"
        h1 = "Krillion Answers Today & Daily Dive Guide"
        intro = ("Krillion is a free daily browser trivia game: seven prompts, about 25 seconds each, "
                 "and rare answers score deeper than obvious ones. This guide explains the game, how to play "
                 "and how to score better — the official game is at krillion.io.")
        sections = [
            ["h2", "What is Krillion?"],
            ["p", "Krillion, officially called The Daily Dive, is a daily browser game where you answer seven prompts and your score depends on how rare your answers are. The rarer the answer, the deeper you dive. It is free, plays in the browser and needs no account. Everyone gets the same seven prompts each day, so scores are comparable."],
            ["h2", "How the game works"],
            ["ul", ["<b>Seven prompts</b> — categories and open questions, from countries to dishes to songs.", "<b>About 25 seconds each</b> — type one answer and confirm it before time runs out.", "<b>Rarity decides depth</b> — uncommon valid answers sink your score; obvious ones barely count.", "<b>Official game</b> — <a href=\"https://krillion.io\">krillion.io</a>."]],
            ["h2", "Start here"],
            ["ul", ["<a href=\"/dive/latest/\">Today's Dive answers</a> — today's 7 questions with rare-answer ideas, updated automatically every day.", "<a href=\"/how-to-play/\">How to play</a> — a step-by-step guide to a Daily Dive round.", "<a href=\"/tips/\">Krillion tips</a> — how to think of rare answers fast.", "<a href=\"/krillion-unlimited/\">Krillion Unlimited</a> — play beyond the daily seven prompts.", "<a href=\"/one-in-a-krillion/\">One in a Krillion</a> — the meaning behind the phrase."]],
            ["h2", "Why people play it"],
            ["p", "The daily format brings fresh prompts every day, and the rarity scoring makes even a short game feel competitive. Because everyone answers the same prompts, sharing your depth score is part of the fun — and so is trying to beat yesterday's dive."],
            ["h2", "Is this the official Krillion site?"],
            ["p", "No. This is an independent, unofficial guide. The game belongs to its developer and is played at <a href=\"https://krillion.io\">krillion.io</a>; this site only explains it."],
        ]
        fine = "Independent guide, not affiliated with Krillion or its developer. Sources: krillion.io, checked October 11, 2026."
    else:
        Ld = {
            "ru": ("Krillion Answers Today и гайд — ответы Daily Dive, советы и как играть",
                   "Krillion Answers Today, как играть в Daily Dive, советы по редким ответам, безлимитный режим и смысл one in a krillion — независимый гид по ежедневной игре-викторине.",
                   "НЕЗАВИСИМЫЙ ГИД / THE DAILY DIVE",
                   "Krillion для новичков",
                   "Krillion — бесплатная ежедневная браузерная викторина: семь подсказок, около 25 секунд на каждую, и редкие ответы дают больше очков, чем очевидные. Этот гид объясняет игру, как в неё играть и как набирать больше очков. Официальная игра — на krillion.io.",
                   [
                       ["h2", "Что такое Krillion?"],
                       ["p", "Krillion, официально называемая The Daily Dive, — ежедневная браузерная игра, где вы отвечаете на семь подсказок, а ваш счёт зависит от того, насколько редки ваши ответы. Чем реже ответ, тем глубже вы ныряете. Это бесплатно, играется в браузере и не требует аккаунта. Каждый день все получают одни и те же семь подсказок, поэтому счета сравнимы."],
                       ["h2", "Как работает игра"],
                       ["ul", ["<b>Семь подсказок</b> — категории и открытые вопросы: от стран до блюд и песен.", "<b>Около 25 секунд на каждую</b> — введите один ответ и подтвердите, пока не вышло время.", "<b>Редкость решает глубину</b> — необычные валидные ответы опускают счёт; очевидные почти не считаются.", "<b>Официальная игра</b> — <a href=\"https://krillion.io\">krillion.io</a>."]],
                       ["h2", "С чего начать"],
                       ["ul", ["<a href=\"/dive/latest/\">Ответы сегодняшнего Dive</a> — 7 вопросов дня с идеями редких ответов, обновляется автоматически каждый день.", "<a href=\"/how-to-play/\">Как играть</a> — пошаговый гайд по раунду Daily Dive.", "<a href=\"/tips/\">Советы по Krillion</a> — как быстро придумывать редкие ответы.", "<a href=\"/krillion-unlimited/\">Krillion Unlimited</a> — играйте сверх семи дневных подсказок.", "<a href=\"/one-in-a-krillion/\">One in a Krillion</a> — смысл фразы."]],
                       ["h2", "Почему в неё играют"],
                       ["p", "Ежедневный формат приносит свежие подсказки каждый день, а редкие ответы делают даже короткую игру соревновательной. Так как все отвечают на одни и те же подсказки, делиться своей глубиной — часть удовольствия, как и попытка побить вчерашний результат."],
                       ["h2", "Это официальный сайт Krillion?"],
                       ["p", "Нет. Это независимый неофициальный гид. Игра принадлежит её разработчику и играется на <a href=\"https://krillion.io\">krillion.io</a>; этот сайт лишь объясняет её."],
                   ],
                   "Независимый гид, не связан с Krillion и её разработчиком. Источники: krillion.io, проверено 11 октября 2026 года."),
            "es": ("Krillion Answers Today y guía — respuestas del Daily Dive, consejos y cómo jugar",
                   "Krillion Answers Today, cómo jugar al Daily Dive, consejos para respuestas raras, modo sin límites y el significado de one in a krillion — guía independiente del juego de trivia diario.",
                   "GUÍA INDEPENDIENTE / THE DAILY DIVE",
                   "Krillion explicado para nuevos jugadores",
                   "Krillion es un juego de trivia diario gratis en el navegador: siete pistas, unos 25 segundos en cada una, y las respuestas raras puntúan más que las obvias. Esta guía explica el juego, cómo jugar y cómo puntuar mejor. El juego oficial está en krillion.io.",
                   [
                       ["h2", "¿Qué es Krillion?"],
                       ["p", "Krillion, oficialmente llamado The Daily Dive, es un juego diario de navegador donde respondes siete pistas y tu puntuación depende de lo raras que sean tus respuestas. Cuanto más rara es la respuesta, más profundo buceas. Es gratis, se juega en el navegador y no requiere cuenta. Cada día todos reciben las mismas siete pistas, así que las puntuaciones son comparables."],
                       ["h2", "Cómo funciona el juego"],
                       ["ul", ["<b>Siete pistas</b> — categorías y preguntas abiertas: de países a platos y canciones.", "<b>Unos 25 segundos en cada una</b> — escribe una respuesta y confírmala antes de que acabe el tiempo.", "<b>La rareza decide la profundidad</b> — las respuestas válidas inusuales hunden tu puntuación; las obvias apenas cuentan.", "<b>Juego oficial</b> — <a href=\"https://krillion.io\">krillion.io</a>."]],
                       ["h2", "Empieza aquí"],
                       ["ul", ["<a href=\"/dive/latest/\">Respuestas del Dive de hoy</a> — las 7 preguntas del día con ideas de respuestas raras, actualizadas cada día automáticamente.", "<a href=\"/how-to-play/\">Cómo jugar</a> — guía paso a paso de una ronda de Daily Dive.", "<a href=\"/tips/\">Consejos de Krillion</a> — cómo pensar respuestas raras rápido.", "<a href=\"/krillion-unlimited/\">Krillion Unlimited</a> — juega más allá de las siete pistas diarias.", "<a href=\"/one-in-a-krillion/\">One in a Krillion</a> — el significado de la frase."]],
                       ["h2", "Por qué la gente juega"],
                       ["p", "El formato diario trae pistas nuevas cada día, y la puntuación por rareza hace competitiva incluso una partida corta. Como todos responden las mismas pistas, compartir tu profundidad es parte de la diversión — y también intentar superar la inmersión de ayer."],
                       ["h2", "¿Es este el sitio oficial de Krillion?"],
                       ["p", "No. Es una guía independiente y no oficial. El juego pertenece a su desarrollador y se juega en <a href=\"https://krillion.io\">krillion.io</a>; este sitio solo lo explica."],
                   ],
                   "Guía independiente, sin afiliación con Krillion ni su desarrollador. Fuentes: krillion.io, consultado el 11 de octubre de 2026."),
            "pt": ("Krillion Answers Today e guia — respostas do Daily Dive, dicas e como jogar",
                   "Krillion Answers Today, como jogar o Daily Dive, dicas para respostas raras, modo sem limites e o significado de one in a krillion — guia independente do jogo de trivia diário.",
                   "GUIA INDEPENDENTE / THE DAILY DIVE",
                   "Krillion explicado para novos jogadores",
                   "Krillion é um jogo de trivia diário e gratuito no navegador: sete dicas, cerca de 25 segundos em cada uma, e respostas raras pontuam mais que as óbvias. Este guia explica o jogo, como jogar e como pontuar melhor. O jogo oficial está em krillion.io.",
                   [
                       ["h2", "O que é Krillion?"],
                       ["p", "Krillion, oficialmente chamado The Daily Dive, é um jogo diário de navegador onde você responde sete dicas e sua pontuação depende de quão raras são suas respostas. Quanto mais rara a resposta, mais fundo você mergulha. É grátis, roda no navegador e não exige conta. Todo dia todos recebem as mesmas sete dicas, então as pontuações são comparáveis."],
                       ["h2", "Como funciona o jogo"],
                       ["ul", ["<b>Sete dicas</b> — categorias e perguntas abertas: de países a pratos e músicas.", "<b>Cerca de 25 segundos em cada uma</b> — digite uma resposta e confirme antes do tempo acabar.", "<b>A raridade decide a profundidade</b> — respostas válidas incomuns afundam sua pontuação; as óbvias quase não contam.", "<b>Jogo oficial</b> — <a href=\"https://krillion.io\">krillion.io</a>."]],
                       ["h2", "Comece aqui"],
                       ["ul", ["<a href=\"/dive/latest/\">Respostas do Dive de hoje</a> — as 7 perguntas do dia com ideias de respostas raras, atualizadas automaticamente todo dia.", "<a href=\"/how-to-play/\">Como jogar</a> — guia passo a passo de uma rodada do Daily Dive.", "<a href=\"/tips/\">Dicas de Krillion</a> — como pensar respostas raras rápido.", "<a href=\"/krillion-unlimited/\">Krillion Unlimited</a> — jogue além das sete dicas diárias.", "<a href=\"/one-in-a-krillion/\">One in a Krillion</a> — o significado da frase."]],
                       ["h2", "Por que as pessoas jogam"],
                       ["p", "O formato diário traz dicas novas todo dia, e a pontuação por raridade torna competitiva até uma partida curta. Como todos respondem as mesmas dicas, compartilhar sua profundidade é parte da diversão — e também tentar superar o mergulho de ontem."],
                       ["h2", "Este é o site oficial de Krillion?"],
                       ["p", "Não. É um guia independente e não oficial. O jogo pertence ao desenvolvedor e é jogado em <a href=\"https://krillion.io\">krillion.io</a>; este site apenas o explica."],
                   ],
                   "Guia independente, sem afiliação com Krillion nem com o desenvolvedor. Fontes: krillion.io, consultado em 11 de outubro de 2026."),
            "id": ("Krillion Answers Today dan panduan — jawaban Daily Dive, tips, dan cara bermain",
                   "Krillion Answers Today, cara bermain Daily Dive, tips jawaban langka, mode tanpa batas, dan arti one in a krillion — panduan independen untuk game trivia harian.",
                   "PANDUAN INDEPENDEN / THE DAILY DIVE",
                   "Krillion dijelaskan untuk pemain baru",
                   "Krillion adalah game trivia harian gratis di browser: tujuh petunjuk, sekitar 25 detik untuk masing-masing, dan jawaban langka memberi skor lebih dalam daripada jawaban umum. Panduan ini menjelaskan game, cara bermain, dan cara mendapat skor lebih baik. Game resminya ada di krillion.io.",
                   [
                       ["h2", "Apa itu Krillion?"],
                       ["p", "Krillion, yang resmi disebut The Daily Dive, adalah game harian di browser di mana Anda menjawab tujuh petunjuk dan skor Anda bergantung pada seberapa langka jawaban Anda. Semakin langka jawabannya, semakin dalam Anda menyelam. Game ini gratis, dimainkan di browser, dan tidak perlu akun. Setiap hari semua orang mendapat tujuh petunjuk yang sama, jadi skor bisa dibandingkan."],
                       ["h2", "Cara kerja game"],
                       ["ul", ["<b>Tujuh petunjuk</b> — kategori dan pertanyaan terbuka: dari negara hingga hidangan dan lagu.", "<b>Sekitar 25 detik per petunjuk</b> — ketik satu jawaban dan konfirmasi sebelum waktu habis.", "<b>Kelangkaan menentukan kedalaman</b> — jawaban valid yang tidak biasa menenggelamkan skor; yang umum hampir tidak dihitung.", "<b>Game resmi</b> — <a href=\"https://krillion.io\">krillion.io</a>."]],
                       ["h2", "Mulai dari sini"],
                       ["ul", ["<a href=\"/dive/latest/\">Jawaban Dive hari ini</a> — 7 pertanyaan hari ini dengan ide jawaban langka, diperbarui otomatis setiap hari.", "<a href=\"/how-to-play/\">Cara bermain</a> — panduan langkah demi langkah satu ronde Daily Dive.", "<a href=\"/tips/\">Tips Krillion</a> — cara cepat memikirkan jawaban langka.", "<a href=\"/krillion-unlimited/\">Krillion Unlimited</a> — bermain melampaui tujuh petunjuk harian.", "<a href=\"/one-in-a-krillion/\">One in a Krillion</a> — makna di balik frasa ini."]],
                       ["h2", "Kenapa orang memainkannya"],
                       ["p", "Format harian membawa petunjuk baru setiap hari, dan penilaian kelangkaan membuat permainan singkat pun terasa kompetitif. Karena semua menjawab petunjuk yang sama, berbagi skor kedalaman adalah bagian dari kesenangan—begitu juga mencoba mengalahkan penyelaman kemarin."],
                       ["h2", "Apakah ini situs resmi Krillion?"],
                       ["p", "Bukan. Ini panduan independen dan tidak resmi. Game ini milik pengembangnya dan dimainkan di <a href=\"https://krillion.io\">krillion.io</a>; situs ini hanya menjelaskannya."],
                   ],
                   "Panduan independen, tidak berafiliasi dengan Krillion atau pengembangnya. Sumber: krillion.io, diperiksa 11 Oktober 2026."),
        }
        title, desc, eyebrow, h1, intro, sections, fine = Ld[lang]
    bread = breadcrumbs_json(lang, [
        {"@type": "ListItem", "position": 1, "name": L["home"], "item": url},
    ])
    crumb = (f'<nav class="breadcrumbs" aria-label="Breadcrumb">'
             f'<a href="{home_href}">{L["home"]}</a><span aria-hidden="true">›</span>'
             f'<span aria-current="page">{h1.split(":")[0]}</span></nav>')
    header_nav = "".join(f'<a href="{h}">{txt}</a>' for txt, h in L["header_nav"])
    footer_nav = "".join(f'<a href="{h}">{txt}</a>' for txt, h in L["footer_nav"])
    name_ld = json.dumps(title, ensure_ascii=False)
    desc_ld = json.dumps(desc, ensure_ascii=False)
    fine_html = f'<p class="fine">{fine}</p>'
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="index,follow"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#15324a"><link rel="icon" href="/favicon.svg"><link rel="stylesheet" href="/style.css?v=20261012"><link rel="canonical" href="{url}">{hreflang_block(lang, "/")}<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary"><script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebPage", "name": {name_ld}, "url": "{url}", "description": {desc_ld}, "inLanguage": "{lang}", "isPartOf": {{"@type": "WebSite", "name": "Krillion Guide", "url": "{KR}/"}}}}</script><script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": {bread}}}</script></head><body><a class="skip" href="#main">{L['skip']}</a><header><a class="brand" href="{home_href}">k<span>↗</span> <b>krillion guide</b></a><nav aria-label="Main">{header_nav}</nav></header><nav class="languages" aria-label="{L['lang_label']}">{lang_nav(lang, "/")}</nav><main id="main"><article class="article home">{crumb}<p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(h1)}</h1><p class="intro">{intro}</p>{render_sections(sections)}{fine_html}</article></main><footer><a class="brand" href="{home_href}">krillion guide<span>↗</span></a><p>{L['footer_desc']}</p><nav aria-label="Footer">{footer_nav}</nav></footer></body></html>
"""

count = 0
for lang in ORDER:
    # index
    html = build_index(lang)
    d = DEPLOY if lang == "en" else os.path.join(DEPLOY, lang)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    count += 1
    print("wrote", lang, "index")
    # pages
    for slug in SLUGS:
        page = PAGES[slug][lang]
        html = build_page(lang, slug, page)
        d = os.path.join(DEPLOY, slug) if lang == "en" else os.path.join(DEPLOY, lang, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print("wrote", lang, slug)

# sitemap
lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
all_pages = ["index"] + SLUGS
for lang in ORDER:
    for slug in all_pages:
        if slug == "index":
            url = f"{KR}/" if lang == "en" else f"{KR}/{lang}/"
        else:
            url = f"{KR}/{slug}/" if lang == "en" else f"{KR}/{lang}/{slug}/"
        lines.append(f"  <url><loc>{url}</loc><lastmod>2026-10-11</lastmod></url>")
lines.append("</urlset>")
with open(os.path.join(DEPLOY, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("sitemap urls:", len(lines) - 3)
print("TOTAL", count)
