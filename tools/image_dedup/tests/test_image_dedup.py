import importlib.util
from pathlib import Path
import sys
import pytest
from PIL import Image, ImageDraw
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT.parents[1]/'backend'))
spec=importlib.util.spec_from_file_location('dedup',ROOT/'image_dedup.py')
tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)
from app.models.entities import Base,Manufacturer,Figure,FigureVariant,ProductImage


@pytest.fixture
def data(tmp_path):
    engine=create_engine('sqlite://');Base.metadata.create_all(engine)
    with Session(engine,expire_on_commit=False) as db:
        m=Manufacturer(name='Test',name_ko='테스트',official_url='https://example.test');db.add(m);db.flush()
        f=Figure(manufacturer_id=m.id,name_original='<test>',official_url='https://example.test/f');db.add(f);db.flush()
        variants=[FigureVariant(figure_id=f.id,variant_key=str(i)) for i in range(2)];db.add_all(variants);db.flush()
        yield db,tmp_path,variants


def add(db,media,variant,name,image,status='personal_local'):
    image.save(media/name)
    row=ProductImage(variant_id=variant.id,image_url='/api/media/'+name,source_url='https://example.test/'+name,usage_status=status)
    db.add(row);db.commit();return row


def picture():
    image=Image.new('RGB',(400,400),'white');d=ImageDraw.Draw(image)
    d.rectangle((80,40,220,330),fill='red');d.ellipse((100,45,170,110),fill='blue');return image


def test_audit_exact_apply_restore_and_other_variant(data):
    db,media,vs=data;im=picture()
    a=add(db,media,vs[0],'a.png',im);b=add(db,media,vs[0],'b.png',im)
    c=add(db,media,vs[1],'c.png',im)
    path=media/'audit.json';journal=media/'journal.json'
    result=tool.audit(db,media,path)
    assert result['candidates']=={'exact_bytes':1}
    assert a.usage_status==b.usage_status=='personal_local'
    assert '&lt;test&gt;' in path.with_suffix('.html').read_text()
    assert tool.apply(db,media,path,journal)['hidden']==1
    assert b.usage_status==tool.HIDDEN and c.usage_status=='personal_local'
    assert all((media/n).is_file() for n in ['a.png','b.png','c.png'])
    assert tool.restore(db,journal)['restored']==1
    assert tool.restore(db,journal)['restored']==0


def test_similar_requires_opt_in_and_keeps_larger(data):
    db,media,vs=data;im=picture()
    small=add(db,media,vs[0],'small.jpg',im.resize((200,200)))
    big=add(db,media,vs[0],'big.jpg',im)
    path=media/'audit.json';tool.audit(db,media,path)
    import json
    plan=json.loads(path.read_text())['candidates'];assert len(plan)==1
    assert plan[0]['reason']=='similar' and plan[0]['keep']['id']==big.id
    assert tool.apply(db,media,path,media/'first.json')['hidden']==0
    assert tool.apply(db,media,path,media/'second.json',True,{small.id})['hidden']==1


def test_different_angle_and_crop_not_candidates(data):
    db,media,vs=data;im=picture()
    add(db,media,vs[0],'a.png',im)
    add(db,media,vs[0],'b.png',ImageOps_mirror(im))
    add(db,media,vs[0],'c.png',im.crop((80,20,250,360)).resize((400,400)))
    assert tool.audit(db,media,media/'audit.json')['candidates']=={}


def ImageOps_mirror(im):
    return im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


def test_changed_file_refuses_entire_apply(data):
    db,media,vs=data;im=picture()
    a=add(db,media,vs[0],'a.png',im);b=add(db,media,vs[0],'b.png',im)
    path=media/'audit.json';tool.audit(db,media,path)
    Image.new('RGB',(400,400),'black').save(media/'b.png')
    with pytest.raises(ValueError,match='IMAGE_CHANGED'):tool.apply(db,media,path,media/'j.json')
    db.rollback();assert a.usage_status==b.usage_status=='personal_local'


def test_row_change_refuses_apply(data):
    db,media,vs=data;im=picture()
    a=add(db,media,vs[0],'a.png',im);b=add(db,media,vs[0],'b.png',im)
    path=media/'audit.json';tool.audit(db,media,path)
    b.source_url='https://example.test/changed';db.commit()
    with pytest.raises(ValueError,match='DATABASE_CHANGED'):tool.apply(db,media,path,media/'j.json')


@pytest.mark.parametrize('url',['/api/media/../outside.jpg','/api/media/%2e%2e/outside.jpg','https://example.test/a.jpg'])
def test_path_guard(tmp_path,url):
    with pytest.raises(ValueError):tool.local_path(url,tmp_path)


def test_missing_and_animated_files_skipped(data):
    db,media,vs=data
    add(db,media,vs[0],'a.png',picture())
    b=add(db,media,vs[0],'b.png',picture());(media/'b.png').unlink()
    result=tool.audit(db,media,media/'audit.json');assert result['skipped']==1
    assert result['candidates']=={}


def test_shared_file_reference_preserved(data):
    db,media,vs=data
    a=add(db,media,vs[0],'a.png',picture())
    b=ProductImage(variant_id=vs[0].id,image_url=a.image_url,source_url='https://example.test/b',usage_status='personal_local')
    c=ProductImage(variant_id=vs[1].id,image_url=a.image_url,source_url='https://example.test/c',usage_status='personal_local')
    db.add_all([b,c]);db.commit()
    path=media/'audit.json';tool.audit(db,media,path);tool.apply(db,media,path,media/'j.json')
    assert c.usage_status=='personal_local' and (media/'a.png').is_file()


def test_exact_pixels_with_different_encoding(data):
    db,media,vs=data;im=picture()
    add(db,media,vs[0],'a.png',im)
    add(db,media,vs[0],'b.png',im)
    im.save(media/'b.png',compress_level=0)
    assert tool.audit(db,media,media/'audit.json')['candidates']=={'exact_pixels':1}


def test_authorized_image_retained_and_hidden_row_not_in_gallery(data):
    db,media,vs=data;im=picture()
    a=add(db,media,vs[0],'a.png',im,status='authorized')
    b=add(db,media,vs[0],'b.png',im)
    path=media/'audit.json';tool.audit(db,media,path)
    tool.apply(db,media,path,media/'j.json')
    from app.services.image_order import ordered_images
    f=db.get(Figure,vs[0].figure_id)
    assert [row.id for row in ordered_images(db,f)]==[a.id]
    assert b.usage_status==tool.HIDDEN
