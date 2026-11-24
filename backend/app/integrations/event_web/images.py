"""Official event poster URLs used by collection and the public feed."""
from urllib.parse import urljoin, urlsplit


IMAGE_HOSTS = {
    'www.duex.co.kr', 'spacegalleria.co.kr',
    'www.animate-onlineshop.co.kr',
    'cdn-pro-web-250-117.cdn-nhncommerce.com',
    'bc8azosk4j.ecn.cdn.ofs.kr',
    'www.popcondplay.com', 'cdn.popcondplay.com',
    'daewonmedia.com', 'www.agfkorea.com',
}


def image_url(value, base=''):
    if not isinstance(value, str) or not value.strip():
        return None
    url = urljoin(base, value.strip())
    try:
        parsed = urlsplit(url)
        if (parsed.scheme == 'https' and parsed.hostname in IMAGE_HOSTS
                and parsed.port in (None, 443) and not parsed.username
                and not parsed.password and not parsed.fragment):
            return url
    except ValueError:
        pass
    return None


def poster_images(root, base, selector):
    if root is None:
        return []
    urls = []
    for node in root.select(selector):
        url = image_url(node.get('content') or node.get('data-src') or node.get('src'), base)
        if url and url not in urls:
            urls.append(url)
    return urls[:8]
