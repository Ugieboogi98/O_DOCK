"""Real supplied source text, mocked model outputs. No network/API calls."""
import hashlib
import json
from pathlib import Path
import pytest
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from app.models.entities import Base, Manufacturer, Figure, FigureVariant, SourceDocument
from app.services.product_semantics import add_documents, context_candidates, source_of, validate_result, save_record, current
from app.repositories.figures import list_figures

SAMPLES = json.loads((Path(__file__).parent/'fixtures/furyu_semantic_samples.json').read_text())


def source(sample):
    value = {k: sample.get(k) for k in ('name_original', 'official_url', 'manufacturer', 'product_line', 'franchise', 'character', 'scale')}
    value.update(type='figure', manufacturer_ko='후류')
    return add_documents(value, [{**d, 'id': i+1} for i,d in enumerate(sample['sources'])])


def entity(original, ko, proof):
    return {'original': original, 'ko': ko, 'evidence_field': proof['evidence_field'], 'evidence': proof['evidence'], 'confidence': .99}


@pytest.mark.parametrize('sample', SAMPLES, ids=lambda s: str(s['id']))
def test_real_introductions_yield_work_and_subject(sample):
    candidates = context_candidates(source(sample))
    work = 'ステラソラ' if sample['id'] <= 50 else '葬送のフリーレン'
    assert {c['original'] for c in candidates if c['kind']=='franchise'} == {work}
    expected = {48:'魔王ちゃん',49:'ヴェルジュ',50:'ヴェルナー',51:'フリーレン',52:'フェルン'}[sample['id']]
    assert {c['original'] for c in candidates if c['kind']=='character'} == {expected}


@pytest.mark.parametrize('sample', SAMPLES[:3], ids=lambda s:str(s['id']))
def test_general_document_entity_extraction_for_stella_samples(sample):
    s = source(sample); candidates = context_candidates(s)
    c = next(c for c in candidates if c['kind']=='character')
    work = next(c for c in candidates if c['kind']=='franchise')
    ko = {48:'마왕짱',49:'베르주',50:'베르너'}[sample['id']]  # Translation fixtures, not official-name assertions.
    r = {'name_ko': 'TENITOL ' + ko + ('(버니)' if sample['id']!=48 else '') + ' [mini]',
         'franchise': entity(work['original'], '스텔라 소라', work),
         'characters':[entity(c['original'],ko,c)], 'figure_form':None}
    fields, issues = validate_result(s,r)
    assert not issues
    assert fields['franchise_ko']=='스텔라 소라'
    assert fields['character_ko']==ko
    assert fields['figure_form']=='mini_figure'
    assert fields['classification_status']=='ready'
    assert fields['characters'][0]['source_url']==sample['sources'][0]['url']


def test_cross_sell_and_mentor_do_not_become_product_characters():
    for sample, wrong in [(SAMPLES[3],'フェルン'),(SAMPLES[4],'フリーレン')]:
        s=source(sample)
        r={'name_ko':'TENITOL TALL 프리렌 클래식 원피스ver.' if sample['id']==51 else 'TENITOL TALL 페른 클래식 원피스ver.',
           'franchise':None,'characters':[{'original':wrong,'ko':'다른 인물','evidence_field':'document_0','evidence':wrong,'confidence':1}], 'figure_form':None}
        fields,issues=validate_result(s,r)
        assert any(x in issues for x in ('RELATED_PRODUCT_CHARACTER_REJECTED','RELATED_PRODUCT_EVIDENCE_REJECTED'))
        assert fields['classification_status']=='review'


def test_explicit_but_omitted_subject_is_review_not_success():
    s=source(SAMPLES[1])
    _,issues=validate_result(s,{'name_ko':'TENITOL 베르주(버니) [mini]','franchise':None,'characters':[],'figure_form':None})
    assert any(i.startswith('EXPLICIT_MAIN_CHARACTER_OMITTED:') for i in issues)


def test_scale_marketing_phrase_is_not_numeric_scale():
    s=source(SAMPLES[3])
    r={'name_ko':'TENITOL TALL 프리렌 클래식 원피스ver.','franchise':None,'characters':[],
       'figure_form':{'code':'scale_figure','evidence_field':'document_0','evidence':'スケール感','confidence':1}}
    fields,issues=validate_result(s,r)
    assert fields['figure_form'] is None
    assert 'FORM_KEYWORD_NOT_SUPPORTED' in issues


def test_db_context_and_changed_document_invalidate_search():
    e=create_engine('sqlite://');Base.metadata.create_all(e)
    with Session(e,expire_on_commit=False) as db:
        sample=SAMPLES[3]
        m=Manufacturer(name='FuRyu',name_ko='후류',official_url='https://www.furyu.jp/');db.add(m);db.flush()
        f=Figure(manufacturer_id=m.id,name_original=sample['name_original'],official_url=sample['official_url']);db.add(f);db.flush()
        v=FigureVariant(figure_id=f.id,variant_key='test');db.add(v);db.flush()
        d=SourceDocument(variant_id=v.id,**{k:sample['sources'][0][k] for k in ('title','url','source_type','body')},language='ja',content_hash=hashlib.sha256(sample['sources'][0]['body'].encode()).hexdigest())
        db.add(d);db.commit()
        s=source_of(f)
        assert s['document_0']==d.body
        r={'name_ko':'TENITOL TALL 프리렌 클래식 원피스ver.','franchise':None,'characters':[],'figure_form':None}
        from app.services.product_semantics import source_hash
        assert save_record(db,{'figure_id':f.id,'source':s,'source_hash':source_hash(s),'model':'mock','result':r})=='partial'
        assert list_figures(db,franchise='장송의 프리렌')['total']==1
        d.body='Changed source text';db.commit()
        assert current(db,f) is None
        assert list_figures(db,franchise='장송의 프리렌')['total']==0


def test_batch_profiles_use_same_document_order_and_reject_changed_context():
    from sqlalchemy import event
    from sqlalchemy.orm import selectinload
    from app.services.product_semantics import current_many, source_hash
    e = create_engine('sqlite://')
    Base.metadata.create_all(e)
    with Session(e, expire_on_commit=False) as db:
        m = Manufacturer(name='FuRyu', name_ko='후류', official_url='https://www.furyu.jp/')
        db.add(m)
        db.flush()
        figures = []
        for i in range(6):
            f = Figure(manufacturer_id=m.id, name_original='TENITOL フェルン',
                       official_url=f'https://example.com/{i}')
            db.add(f)
            db.flush()
            v = FigureVariant(figure_id=f.id, variant_key='main')
            db.add(v)
            db.flush()
            for n in range(5):
                db.add(SourceDocument(variant_id=v.id, url=f'https://example.com/{i}/{n}',
                    title=str(n), source_type='official_detail' if n < 2 else 'other',
                    body=f'body {i} {n}', language='ja', content_hash='fixture'))
            db.commit()
            s = source_of(f)
            r = {'name_ko': 'TENITOL 페른', 'franchise': None, 'characters': [], 'figure_form': None}
            save_record(db, {'figure_id': f.id, 'source': s, 'source_hash': source_hash(s),
                             'model': 'fixture', 'result': r})
            figures.append(f)
        # Establish the same eager-loading contract as list_figures().
        figures = list(db.scalars(select(Figure).options(
            selectinload(Figure.manufacturer), selectinload(Figure.product_line))))
        expected = {f.id: current(db, f).source_hash for f in figures}
        statements = []

        def count(conn, cursor, statement, parameters, context, many):
            statements.append(statement)

        event.listen(e, 'before_cursor_execute', count)
        try:
            batch = current_many(db, figures)
        finally:
            event.remove(e, 'before_cursor_execute', count)
        assert {fid: p.source_hash for fid, p in batch.items()} == expected
        assert len(statements) == 2
        doc = db.scalar(select(SourceDocument).where(SourceDocument.title == '1'))
        doc.body = 'changed'
        db.commit()
        assert current(db, figures[0]) is None
        assert figures[0].id not in current_many(db, figures)
        assert len(current_many(db, figures)) == 5
    e.dispose()
