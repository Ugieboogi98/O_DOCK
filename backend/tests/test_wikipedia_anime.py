from app.services.reference_classifier import cached_knowledge, search_title_aliases, norm
from app.repositories.figures import list_figures
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.entities import Base, Figure, Manufacturer


def test_reference_supplement_and_exact_title_search():
    data = cached_knowledge()
    assert len(data['works']) > 600
    assert search_title_aliases('존재하지 않는 제목') == ['존재하지 않는 제목']
    assert search_title_aliases('강철') == ['강철']
    aliases = search_title_aliases('가난뱅이 신이!')
    assert '貧乏神が!' in aliases
    assert any(norm(a) == norm('가난뱅이 신이!') for a in aliases)


def test_korean_title_finds_japanese_product_and_escapes_wildcards():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        maker = Manufacturer(name='Test', name_ko='테스트', official_url='https://example.com')
        db.add(maker)
        db.flush()
        db.add(Figure(manufacturer_id=maker.id, name_original='貧乏神が! フィギュア',
                      official_url='https://example.com/1', type='figure'))
        db.commit()
        assert list_figures(db, q='가난뱅이 신이!')['total'] == 1
        assert list_figures(db, q='%')['total'] == 0
