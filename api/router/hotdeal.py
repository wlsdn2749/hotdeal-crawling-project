from fastapi import APIRouter
from typing import Optional, List
from api.database import db

from api.model import Item, HotdealItemDetail
hotdeal = APIRouter(prefix='/hotdeal')


# @hotdeal.get('/', tags=['hotdeal'])
# async def start_hotdeal():
#     '''
#         핫딜 메인페이지
#     '''
#     return {'msg' : 'Here is Hotdeal'}

@hotdeal.get('/', tags=['hotdeal'], response_model=List[Item])
async def read_items(page: int = 0, count: int = 20):
    '''
        각 page는 count만큼의 Item을 보여줌
    '''
    
    conn = db.get_connection()
    columns = list(Item.model_fields)
    
    query = f"""
        SELECT *
        FROM fm
        OFFSET {page*count}
        LIMIT {count}
    """ 
    result = conn.execute(query).fetchall()
    
    items: List[Item] = [Item(**dict(zip(columns,item))) for item in result]
    return items

@hotdeal.get('/detail', tags=['hotdeal'], response_model = HotdealItemDetail)
async def read_item_detail(site: str = "fm", url: str = "https://www.fmkorea.com/7138477950"):
    '''
        site와 url을 통해 item을 읽어옴
        
        type:
            site: default = fm
            url: default = 벨킨..?
            
        rtype:
            HotdealItemDetail
        
    '''
    
    conn = db.get_connection()
    
    colmuns = list(HotdealItemDetail.model_fields)
    
    query = f"""
        SELECT *
        FROM {site}_detail
        WHERE url = '{url}'
    """
    
    result = conn.execute(query).fetchone()
    
    detail: HotdealItemDetail = dict(zip(colmuns, result))
    return detail
    