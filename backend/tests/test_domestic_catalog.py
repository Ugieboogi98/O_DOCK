import threading
from contextlib import nullcontext

import pytest

from app.collectors.retailers.catalog import canonical_page, discover_page
from app.collectors.retailers.checkpoint import Checkpoint
from app.collectors.safe_http import CollectionDenied
from scripts.collect_domestic_catalog import CatalogFetcher, fetch_page
from scripts import collect_domestic_catalog as catalog_worker


def test_category_and_pagination_keep_identity_and_exclude_non_catalog_paths():
    page = 'https://maniahouse.co.kr/product/list.html?cate_no=45'
    html = '''<a href="?cate_no=45&page=2&sort_method=3">2</a>
    <a href="/product/list.html?cate_no=45&page=1">처음</a>
    <a href="/product/name/123/category/45/display/1/">A</a>
    <a href="/product/detail.html?product_no=123&tracking=unused">A</a>
    <a href="/member/login.html">로그인</a>
    <a href="/board/list.html?board_no=4&page=2">리뷰</a>
    <a href="https://other.example/product/list.html?cate_no=2">기타</a>'''
    pages, products = discover_page(html, page, 'maniahouse')
    assert pages == ['https://maniahouse.co.kr/product/list.html?cate_no=45&page=2']
    assert products == ['https://maniahouse.co.kr/product/detail.html?product_no=123']
    assert canonical_page(page + '&page=1', 'maniahouse') == page
    assert canonical_page(page.replace('https:', 'http:'), 'maniahouse') is None


def test_figurefarm_list_and_query_tracking():
    root = 'https://www.figurefarm.net/'
    html = '''<a href="/shop/big_section.php?cno1=1079&page=2">다음</a>
    <a href="/shop/detail.php?pno=606FEC164FBB88E0D5775CD55852E6A8&rURL=tracking">상품</a>'''
    pages, products = discover_page(html, root, 'figurefarm')
    assert pages == [root + 'shop/big_section.php?cno1=1079&page=2']
    assert len(products) == 1 and 'rURL' not in products[0]


def test_frontier_resumes_and_deduplicates_after_interruption(tmp_path):
    path = tmp_path / 'state.sqlite'
    queue = Checkpoint(path)
    queue.add(pages=['page1'], products=['product1', 'product1'])
    job = queue.next()
    assert job['url'] == 'product1'
    queue.close()  # interruption before completion leaves the same job pending
    queue = Checkpoint(path)
    assert queue.next() == job
    queue.finish(job)
    queue.add(products=['product1'])
    assert queue.next()['url'] == 'page1'
    assert queue.counts() == {'page_pending': 1, 'product_done': 1}
    queue.close()


def test_full_fetcher_allows_categories_but_keeps_member_paths_blocked():
    fetcher = CatalogFetcher('herotime')
    assert fetcher.allowed_path('https://www.herotime.co.kr/product/list.html?cate_no=399&page=2')
    assert not fetcher.allowed_path('https://www.herotime.co.kr/member/login.html')
    assert not fetcher.allowed_path('https://other.example/product/list.html?cate_no=399')


def test_denied_source_is_not_retried():
    class BlockedFetcher:
        calls = 0
        def fetch(self, url):
            self.calls += 1
            raise CollectionDenied('HTTP_429')
    fetcher = BlockedFetcher()
    with pytest.raises(CollectionDenied, match='HTTP_429'):
        fetch_page(fetcher, 'https://maniahouse.co.kr/', threading.Event())
    assert fetcher.calls == 1


@pytest.mark.parametrize('restricted', [False, True])
def test_deleted_or_restricted_product_does_not_stop_other_products(tmp_path, monkeypatch, restricted):
    class Fetcher:
        def fetch(self, url):
            if url.endswith('/'):
                return '<a href="/product/detail.html?product_no=1">A</a><a href="/product/detail.html?product_no=2">B</a>'
            if url.endswith('=1'):
                if restricted:
                    return "<script>location.replace('/intro/adult_im.html');</script>"
                raise CollectionDenied('HTTP_404')
            return '<p>product</p>'
    monkeypatch.setattr(catalog_worker, 'CatalogFetcher', lambda name: Fetcher())
    monkeypatch.setattr(catalog_worker, 'SessionLocal', lambda: nullcontext(None))
    monkeypatch.setattr(catalog_worker, 'matches', lambda db, row: {'status': 'UNMATCHED'})
    source = dict(catalog_worker.SOURCES['maniahouse'], parse=lambda html, url: {'title_raw': 'Figure'})
    monkeypatch.setitem(catalog_worker.SOURCES, 'maniahouse', source)
    result = catalog_worker.run_source('maniahouse', tmp_path, False, threading.Event())
    assert result['state'] == 'completed'
    assert result['counts']['product_restricted' if restricted else 'product_unavailable'] == 1
    assert result['counts']['product_done'] == 1
