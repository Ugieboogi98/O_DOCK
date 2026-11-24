"""Only the official sources explicitly requested by the user. No X/aggregator scraping."""
SOURCES={
 'duex':{'name':'DUEX','url':'https://www.duex.co.kr/page/22','terms_url':None},
 'spacegalleria':{'name':'Space Galleria','url':'https://spacegalleria.co.kr/','terms_url':'https://spacegalleria.co.kr/terms'},
 'animate':{'name':'애니메이트 코리아','url':'https://www.animate-onlineshop.co.kr/board/list.php?bdId=event','terms_url':'https://www.animate-onlineshop.co.kr/service/agreement.php'},
 'aniplus':{'name':'애니플러스','url':'https://shop.aniplustv.com/offline-shop/collabo-cafe','terms_url':None},
 'popcondplay':{'name':'팝콘D플레이','url':'https://www.popcondplay.com/','terms_url':None},
 'daewon':{'name':'대원미디어','url':'https://daewonmedia.com/board/news-event','terms_url':None},
 'agf':{'name':'AGF Korea','url':'https://www.agfkorea.com/event?idx=1','terms_url':None},
 'gstar':{'name':'G-STAR','url':'https://www.gstar.or.kr/gstar/gstar_info.do','terms_url':'https://www.gstar.or.kr/member/terms.do'},
}
DISABLED_SOURCES=[
 {'name':'NIKKE_kr','platform':'x','status':'API_ACCESS_AND_PRICING_NOT_CONFIGURED','url':'https://x.com/NIKKE_kr'},
 {'name':'animate_hongdae','platform':'x','status':'API_ACCESS_AND_PRICING_NOT_CONFIGURED','url':'https://x.com/animate_hongdae'},
 {'name':'Popga','platform':'reference','status':'DISCOVERY_REFERENCE_ONLY_NO_COLLECTION','url':'https://popga.co.kr/'},
 {'name':'Popply','platform':'reference','status':'DISCOVERY_REFERENCE_ONLY_NO_COLLECTION','url':'https://popply.co.kr/'},
]
