"""Private static HTML review artifact. No JavaScript, external media or auto-publication."""
from html import escape
import re


def render(report):
    esc = lambda value: escape(str(value or ''), quote=True)
    category_names = {'COLLAB_CAFE':'콜라보 카페','POPUP_STORE':'팝업·팝업스토어','EXHIBITION':'전시회'}
    cards = []
    rows = sorted(report['posts'], key=lambda r: r['candidate']['status'] != 'PENDING_REVIEW')
    for row in rows:
        c = row['candidate']
        pending = c['status'] == 'PENDING_REVIEW'
        badges = ''.join('<span class="badge">'+esc(category_names.get(v,v))+'</span>' for v in c['categories'])
        pictures = []
        for image in row.get('images', []):
            if image.get('status') == 'DOWNLOADED' and re.fullmatch(r'media/[a-f0-9]{64}\.(?:jpg|png|webp)',image.get('path','')):
                path=esc(image['path'])
                label='영상 썸네일' if image.get('role')=='VIDEO_THUMBNAIL' else '게시물 이미지'
                pictures.append(f'<a href="{path}" target="_blank" rel="noopener"><img src="{path}" alt="{label}" loading="lazy"></a>')
        gallery = '<div class="post-images">'+''.join(pictures)+'</div>' if pictures else ''
        cards.append(f'''<article class="{'candidate' if pending else 'excluded'}">
<div class="meta">@{esc(row['source_username'])} · {esc(row['timestamp'])}</div>
<div>{badges}<span class="state">{esc('검수 대기' if pending else c['status'])}</span></div>
<h2>{esc(c['title'] or '본문 없음')}</h2>
{gallery}
<dl><dt>작품/IP 후보</dt><dd>{esc(' · '.join(c['franchises']) or '원문 확인 필요')}</dd>
<dt>행사 기간</dt><dd>{esc(c['start_date'] or '미확인')} ~ {esc(c['end_date'] or '미확인')}</dd>
<dt>장소</dt><dd>{esc(c['venue'] or '미확인')}</dd></dl>
<details><summary>판별 근거 · 주의 사항</summary><pre>{esc(chr(10).join(e['field']+': '+e['quote'] for e in c['evidence']))}</pre><p>{esc(' · '.join(c['warnings']))}</p></details>
<details {'open' if pending else ''}><summary>게시물 원문</summary><p class="caption">{esc(row['caption'])}</p></details>
<a href="{esc(row['permalink'])}" target="_blank" rel="noopener noreferrer">Instagram 공식 원문 보기 ↗</a></article>''')
    count = sum(r['candidate']['status']=='PENDING_REVIEW' for r in rows)
    image_note='공식 API 이미지의 내부 검수용 사본 · 사이트 공개/재배포 미적용' if report.get('image_summary') else '이미지는 다운로드하지 않았습니다'
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' file:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>O_DOCK 행사 검수</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f7fb;color:#26374f;font-family:system-ui,'Malgun Gothic',sans-serif;line-height:1.7}}main{{max-width:1080px;margin:60px auto;padding:0 22px}}h1{{font-size:32px;margin-bottom:8px}}header{{margin-bottom:32px}}header p,.meta{{color:#6d7d95;font-size:13px}}article{{background:#fff;padding:28px;margin:20px 0;border:1px solid #dfe6f0;border-radius:12px}}article.candidate{{border-top:3px solid #5679ba}}h2{{font-size:20px;overflow-wrap:anywhere}}.badge,.state{{display:inline-block;padding:3px 9px;background:#eaf0fc;border-radius:5px;font-size:11px;margin:10px 6px 5px 0}}.state{{background:#f0f2f6}}dl{{display:grid;grid-template-columns:120px 1fr;font-size:13px}}dt{{color:#7c8ca2}}dd{{margin:0}}summary{{cursor:pointer;font-size:13px;padding:12px 0}}.caption,pre{{white-space:pre-wrap;overflow-wrap:anywhere;font-family:inherit;font-size:13px}}a{{display:inline-block;margin-top:16px;color:#4267a8;font-size:13px}}.excluded{{opacity:.85}}.notice{{padding:16px;background:#eaf0fb;border-radius:8px;font-size:13px}}@media(max-width:600px){{main{{margin-top:28px}}article{{padding:20px}}dl{{grid-template-columns:95px 1fr}}}}
.post-images{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:18px 0}}.post-images a{{margin:0;display:block}}.post-images img{{display:block;width:100%;height:310px;object-fit:contain;background:#f6f8fc;border:1px solid #e3e9f3;border-radius:8px}}@media(max-width:600px){{.post-images{{grid-template-columns:repeat(2,minmax(0,1fr))}}.post-images img{{height:210px}}}}
</style></head><body><main><header><div>O_DOCK / EVENT RESEARCH</div><h1>서브컬처 행사 검수함</h1><p>팝업 · 팝업스토어 · 전시회 · 콜라보 카페</p><div class="notice">원본 {len(rows)}건 · 검수 후보 {count}건 · 그 외 {len(rows)-count}건<br>규칙 기반 후보이며 확정 행사 목록이 아닙니다. 관리자 검수 전 공개되지 않습니다.</div><p>수집: {esc(report['collected_at'])} · 자동 스케줄러 미활성 · {esc(image_note)}</p></header>{''.join(cards)}</main></body></html>'''
