from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import get_settings
from app.services.event_catalog import candidate_items, filtered, private_images
from app.integrations.instagram.store import posts,candidates

router=APIRouter(prefix='/api',tags=['events'])


def filters(q:str=Query('',max_length=120),category:Literal['','POPUP_STORE','EXHIBITION','COLLAB_CAFE','FAIR','FESTIVAL','GOODS_EVENT']='',
    when:Literal['','ONGOING','UPCOMING','ENDED','UNKNOWN','CANCELLED','POSTPONED','SOLD_OUT']='',area:str=Query('',max_length=200),
    sort:Literal['latest','opening','ending']='latest',page:int=Query(1,ge=1),size:int=Query(12,ge=1,le=48)):
    return dict(q=q,category=category,when=when,area=area,sort=sort,page=page,size=size)


@router.get('/events')
def list_events(params=Depends(filters),db:Session=Depends(get_db)):
    items=candidate_items(db,get_settings().data_dir)
    for item in items:
        item['verification']='SOURCE_COLLECTED'
        item['images']=[url.replace('/api/admin/event-candidates/images/','/api/events/images/') for url in item['images']]
    return filtered(items,**params)


@router.get('/events/images/{post_id}/{image_index}')
def event_image(post_id:int,image_index:int,db:Session=Depends(get_db)):
    if image_index<0:raise HTTPException(404,'이미지 없음')
    row=db.execute(select(posts.c.external_id,posts.c.caption)
        .join(candidates,candidates.c.post_id==posts.c.id)
        .where(posts.c.id==post_id,posts.c.platform=='instagram',candidates.c.status=='PENDING_REVIEW')).mappings().first()
    if not row:raise HTTPException(404,'이미지 없음')
    entry=private_images(get_settings().data_dir).get(row['external_id'],{})
    files=entry.get('files',[]) if entry.get('caption')==row['caption'] else []
    if image_index>=len(files):raise HTTPException(404,'이미지 없음')
    return FileResponse(files[image_index],headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'})
