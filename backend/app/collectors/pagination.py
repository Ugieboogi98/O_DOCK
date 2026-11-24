import re
from urllib.parse import parse_qs, urljoin, urldefrag, urlparse
from bs4 import BeautifulSoup

PAGE_KEYS = {"page", "p", "paged", "page_num", "pageno", "page_no", "offset", "start"}
NEXT_WORDS = {
    "next",
    "next page",
    "older",
    "次へ",
    "次のページ",
    "다음",
    "다음 페이지",
    "›",
    "»",
    "≫",
    "«",
    ">",
}
PAGE_PATH = re.compile(r"/(?:page|pages)/\d+/?$", re.I)


def canonical(url):
    # Keep query parameters, as they often encode pagination.
    return urldefrag(url)[0]


def pagination_links(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    found = []
    for a in soup.select("a[href], link[rel~=next][href]"):
        raw = a.get("href", "").strip()
        if not raw or raw.startswith(("javascript:", "mailto:", "#")):
            continue
        url = canonical(urljoin(page_url, raw))
        txt = a.get_text(" ", strip=True).casefold()
        rel = a.get("rel", [])
        rel = [str(x).casefold() for x in rel]
        aria = (a.get("aria-label") or "").strip().casefold()
        qs = parse_qs(urlparse(url).query, keep_blank_values=True)
        has_page_param = any(k.lower() in PAGE_KEYS for k in qs)
        by_semantics = "next" in rel or "next" in aria or txt in NEXT_WORDS
        numeric_pager = (
            txt.isdecimal()
            and a.find_parent(class_=re.compile("pagin", re.I)) is not None
        )
        parsed = urlparse(url)
        origin = urlparse(page_url)
        # MegaHouse uses /products/2/?sort=new (not /page/2/), and its
        # pagination anchors may not have a CSS class containing "pagin".
        # Only accept numbered /products/N/ paths on the same MegaHouse host.
        megahobby_numbered = (
            origin.hostname in {"megahobby.jp", "www.megahobby.jp"}
            and parsed.hostname == origin.hostname
            and re.fullmatch(r"/products/[0-9]+/?", parsed.path) is not None
            and (txt.isdecimal() or by_semantics)
        )
        if (
            by_semantics
            or numeric_pager
            or has_page_param
            or PAGE_PATH.search(parsed.path)
            or megahobby_numbered
        ):
            found.append(url)
    return list(dict.fromkeys(found))
