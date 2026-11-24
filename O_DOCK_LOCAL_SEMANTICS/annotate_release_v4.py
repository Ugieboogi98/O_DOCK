"""Frozen agent source audit, authored without inspecting candidate outputs.

Conventional Korean spellings are not independent human gold. Uncertain packaging,
robots/vehicles and transformation identity taxonomies are explicitly excluded.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# id | acceptable work families separated by / | characters separated by comma,
# acceptable spellings separated by / | acceptable forms separated by comma
ROWS = '''
277|원피스|몽키 D 루피/몽키 D. 루피|action_figure
648|기동전사 건담 UC/기동전사 건담 유니콘||?
146|미소녀전사 세일러문/미소녀 전사 세일러문||mini_figure,?
787|신세기 GPX 사이버 포뮬러/신세기 GPX 사이버 포뮬러 11/신세기 GPX 사이버 포뮬러 더블 원||?
569|주술회전|이에이리 쇼코|chibi_figure
896|기동전사 Z 건담/기동전사 Z건담|카미유 비단|completed_figure,?
5077|키즈나 아이/키즈나아이|키즈나 아이/키즈나아이|scale_figure
5192|귀멸의 칼날|토미오카 기유|prize_figure,?
673|원피스|몽키 D 루피/몽키 D. 루피|?
1496|2.5차원의 유혹|리리엘/아마노 리리사|scale_figure
892|단다단|치키치타|soft_vinyl
5549|하츠네 미쿠/VOCALOID/보컬로이드||noodle_stopper
1140|디즈니 트위스티드 원더랜드/트위스티드 원더랜드|빌 셴하이트/빌 쉔하이트|chibi_figure
1422|우마무스메 프리티 더비|히시 미라클|scale_figure
1050|귀멸의 칼날|렌고쿠 쿄쥬로|chibi_figure
1471|가끔씩 툭하고 러시아어로 부끄러워하는 옆자리의 아랴 양/가끔씩 툭하고 러시아어로 부끄러워하는 옆자리의 아랴양|아랴/알리사 미하일로브나 쿠죠|scale_figure
680|봇치 더 록!|고토 히토리/고토 히토리/고토 히토리|chibi_figure
5482|Re:제로부터 시작하는 이세계 생활|람,렘|scale_figure
6128|좀비 랜드 사가/좀비랜드 사가|미즈노 아이|scale_figure
4799|기동전사 건담 지온의 재흥/기동전사 건담||model_kit
6042|Re:제로부터 시작하는 이세계 생활|에밀리아|scale_figure
1033|드래곤볼 Z/드래곤볼|손오공|completed_figure,?
5980|연애 플롭스|아멜리아 어빙/아멜리아 어빈|scale_figure
5757|5등분의 신부|나카노 요츠바|lottery_goods
1440|Re:제로부터 시작하는 이세계 생활|렘|scale_figure
270|기동전사 V 건담/기동전사 V건담|카테지나 루스|completed_figure,?
1426|프리즈마☆이리야/프리즈마 이리야|이리야/이리야스필 폰 아인츠베른,미유/미유 에델펠트|scale_figure
4950|블루 록/블루록||?
4893|귀멸의 칼날|토미오카 기유|plush
717|사카모토 데이즈||mini_figure,?
207|디즈니 트위스티드 원더랜드/트위스티드 원더랜드|말레우스 드라코니아|chibi_figure
6016|오버로드|시즈 델타|scale_figure
1010|하이큐!!|미야 오사무/사무키츠네|figure_parts,?
4985|||lottery_goods
531|괴수 8호|히비노 카프카|chibi_figure,?
5032|던전에서 만남을 추구하면 안 되는 걸까/극장판 던전에서 만남을 추구하면 안 되는 걸까 -오리온의 화살-|헤스티아|scale_figure
4809|나의 히어로 아카데미아|미르코/우사기야마 루미|scale_figure
1245|명탐정 코난|괴도 키드|chibi_figure
1410|우마무스메 프리티 더비|스틸 인 러브|scale_figure
1051|귀멸의 칼날|이구로 오바나이|chibi_figure
1026|위키드|글린다|chibi_figure,?
190|하이큐!!|카게야마 토비오|chibi_figure,?
6002|오버로드|알베도|scale_figure
5361|러브 라이브! 선샤인!!/러브 라이브!|마츠우라 카난|prize_figure,?
709|고질라/고지라-1.0/고질라 마이너스 원|고질라|action_figure,?
5391|러브 라이브! 선샤인!!/러브 라이브!|와타나베 요우|prize_figure,?
538|나루토 질풍전/나루토||mini_figure,?
732|윈드 브레이커/WIND BREAKER|토미야마 쵸지|chibi_figure,?
5044|어떤 과학의 초전자포/어떤 과학의 초전자포 T|미사카 미코토|scale_figure
4734|체인소 맨/체인소맨|체인소 맨/덴지,사무라이 소드/사무라이소드|completed_figure,?
5236|CLANNAD/클라나드/클라나드 (비디오 게임)|이치노세 코토미|prize_figure,?
6086|소드 아트 온라인|아스나/유우키 아스나|scale_figure
6116|소녀전선|에이전트|scale_figure
5873|명탐정 코난|아무로 토오루/아무로 토루|non_scale_figure,completed_figure,?
4945|||?
4715|나의 히어로 아카데미아|토도로키 쇼토|scale_figure
4907|5등분의 신부|나카노 미쿠|plush
1573|가면라이더 V3||?
4894|우마무스메 프리티 더비|키타산 블랙|plush
4736|하츠네 미쿠|하츠네 미쿠|chibi_figure
4938|블루 록/블루록|나기 세이시로|plush
4876|나의 히어로 아카데미아|토가 히미코|scale_figure
4892|귀멸의 칼날|시나즈가와 사네미|plush
1571|가면라이더 V3||?
4740|하츠네 미쿠|KAITO/카이토|chibi_figure
4754|가끔씩 툭하고 러시아어로 부끄러워하는 옆자리의 아랴 양/가끔씩 툭하고 러시아어로 부끄러워하는 옆자리의 아랴양|아랴/알리사 미하일로브나 쿠죠|completed_figure,?
4940|블루 록/블루록||rubber_mascot
4814|유유백서|우라메시 유스케|completed_figure,?
4853|마녀의 여행|일레이나|scale_figure
1551|가면라이더 고스트||action_figure
4788|명탐정 코난|하이바라 아이|chibi_figure
4872|데이트 어 라이브|토키사키 쿠루미|scale_figure
4868|길티 기어/길티기어/길티 기어 스트라이브|브리짓|scale_figure
4764|그 비스크 돌은 사랑을 한다/그 비스크돌은 사랑을 한다|키타가와 마린|completed_figure,?
4714|나의 히어로 아카데미아|미도리야 이즈쿠,스테인|completed_figure
4934|블루 록/블루록|이사기 요이치|plush
4864|하츠네 미쿠|하츠네 미쿠|scale_figure
4804|원펀맨|전율의 타츠마키/타츠마키|completed_figure,?
4813|카드캡터 사쿠라/카드캡터 사쿠라 클리어 카드 편|키노모토 사쿠라|plush
4811|스즈미야 하루히의 우울|아사히나 미쿠루|plush
4720|나의 히어로 아카데미아|토가 히미코|scale_figure
1548|울트라맨 메비우스|울트라맨 히카리|action_figure
4773|에반게리온/에반게리온 신극장판/신세기 에반게리온|아스카/아스카 랑그레이/시키나미 아스카 랑그레이|chibi_figure
1563|울트라맨|앤트라/앤틀러/안토라|action_figure
4902|빙과|치탄다 에루|plush
4829|데스 스트랜딩 2/데스 스트랜딩 2: 온 더 비치/데스 스트랜딩|샘/샘 포터 브리지스|scale_figure,static_figure
4713|나의 히어로 아카데미아|바쿠고 카츠키|scale_figure
4887|데이트 어 라이브|토키사키 쿠루미|plush
4722|Re:제로부터 시작하는 이세계 생활|람|scale_figure
4723|Re:제로부터 시작하는 이세계 생활|에밀리아|scale_figure
4861|옆집 천사님 때문에 어느샌가 인간적으로 타락한 사연|시이나 마히루|scale_figure
4815|유유백서|쿠라마|completed_figure,?
1575|가면라이더 V3|라이더맨|action_figure
1546|장송의 프리렌|슈타르크|action_figure
4777|하츠네 미쿠|사쿠라 미쿠/하츠네 미쿠|chibi_figure
4922|블루 록/블루록|치기리 효마|plush,?
104|장송의 프리렌|페른|action_figure
4785|체인소 맨/체인소맨/극장판 체인소 맨 레제편|레제|completed_figure,?
4732|주술회전|후시구로 메구미|scale_figure
4783|주술회전|이타도리 유지|chibi_figure
'''


def main():
    cases = []
    for line in ROWS.strip().splitlines():
        ident, work, characters, forms = line.split('|')
        row = {'id': int(ident), 'work': work.split('/') if work else [],
               'characters': [c.split('/') for c in characters.split(',')] if characters else [],
               'forms': [None if f == '?' else f for f in forms.split(',')]}
        if not characters:
            row['skip'] = ['characters']
            row['review_note'] = 'Collection inventory, implicit subject, transformation or non-human taxonomy is not labeled.'
        if int(ident) in (4985, 4945):
            row.setdefault('skip', []).append('work')
            row['review_note'] = 'No unambiguous work in supplied source, or Korean convention uncertain.'
        cases.append(row)
    source = ROOT / 'reports/release_sources_v4_20261111.json'
    ids = {r['figure_id'] for r in json.loads(source.read_text(encoding='utf-8'))['records']}
    assert ids == {r['id'] for r in cases} and len(cases) == 100
    output = ROOT / 'samples/release_labels_v4_20261111.json'
    if output.exists():
        raise RuntimeError('REFUSE_OVERWRITE_LABELS')
    output.write_text(json.dumps({'label_origin': 'Agent source audit before inspecting candidate outputs; not independent human gold',
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'note': 'Family titles accepted where source makes installment identity immaterial. Null forms allow uncertainty only when explicit type unavailable. Characters deduplicated by identity.',
        'cases': cases}, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
