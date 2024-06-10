from fastapi import APIRouter
from typing import Optional, List
from api.database import db

from api.model import Item
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