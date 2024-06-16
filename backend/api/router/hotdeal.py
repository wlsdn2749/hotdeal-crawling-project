import pickle
import base64

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List, Annotated, Literal
from pydantic import Field, field_validator, BaseModel, ValidationInfo
from api.database import db
from api.utils import load_valid_categories
from api.model import Item, HotdealItemDetail
hotdeal = APIRouter(prefix='/hotdeal')

VALID_CATEGORIES = load_valid_categories("./api/static/categories_fm.txt")

class ItemList(BaseModel):
    '''
        각 page는 count만큼의 Item을 보여줌
        categories 필터를 추가함, 기본값은 모든 카테고리
    '''
    page: int = Field(Query(1, ge=1, description='Page number'))
    count: int = Field(Query(20, description='Number of items per page'))
    categories: List[str] = Field(Query([], description='List of categories'))
    order: str = Field(Query('desc', description='time order of items'))
    
    @field_validator('categories', 'order')
    @classmethod
    def check_attrs(cls, v, info: ValidationInfo):
        
        if info.field_name == 'categories':
            if not v:
                return None
            
            invalid_categories = [category for category in v if category not in VALID_CATEGORIES]
            if invalid_categories:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid categories: {', '.join(invalid_categories)}. Valid categories are: {', '.join(VALID_CATEGORIES)}"
                )
                
        if info.field_name == 'order':
            if v not in ['asc', 'desc']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Time order must be eiter 'asc' or 'desc'"
                )
                
        return v

class SearchParameters(BaseModel):
    '''
        검색시 파라미터들을 선언
        search_mode: title, title_content 이외 에러
        search_query: 2글자 이하 에러
    '''
    page: int = Field(Query(1, ge=1, description='Page number'))
    count: int = Field(Query(20, description='Number of items per page'))
    search_mode: str = Field(Query('title', description='search criteria'))
    search_query: str = Field(Query(..., description='search query'))
    order: str = Field(Query('desc', description='time order of items'))
    
    @field_validator('search_mode', 'search_query', )
    @classmethod
    def check_attrs(cls, v, info: ValidationInfo):
        
        if info.field_name == 'search_mode':
            if v not in ['title', 'title_content']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid search mode, Valid search mode are : 'title', 'content'" 
                )
                
        if info.field_name == 'search_query':
            if len(v) < 2:
                raise HTTPException(
                    status_code=400,
                    detail=f"검색어는 2자 이상 이어야 합니다."
                )
                
        if info.field_name == 'order':
            if v not in ['asc', 'desc']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Time order must be eiter 'asc' or 'desc'"
                )
        
        return v
    
    
@hotdeal.get('/', tags=['hotdeal'], response_model=List[Item])
async def read_items(itemlist: ItemList = Depends()):
    
    categories = itemlist.categories
    page = itemlist.page
    count = itemlist.count
    order = itemlist.order
    
    
    conn = db.get_connection()
    columns = list(Item.model_fields)
    
    query = f"""
        SELECT *
        FROM fm
    """
    
    # Validate categories if provide

    if categories:     
        categories_placeholder = ', '.join('?' * len(categories))
        query += f" WHERE category IN ({categories_placeholder})"

        
    query += f"ORDER BY time {order} OFFSET {(page-1)*count} LIMIT {count}"
    
    if categories:
        result = conn.execute(query, categories).fetchall()
    else:
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
    detail["comments"] = pickle.loads(base64.b64decode(detail["comments"].encode('utf-8')))
    return detail
    
# @hotdeal.get('/')

@hotdeal.get('/search', tags=['hotdeal'], response_model= List[Item])
async def search(p: SearchParameters = Depends()):
    
    conn = db.get_connection()
    
    page = p.page
    count = p.count
    search_mode = p.search_mode
    search_query = p.search_query
    order = p.order
    
    
    columns = list(Item.model_fields)
    
    if search_mode == 'title_content':     
        query = f"""
            SELECT DISTINCT fm.*
            FROM fm
            WHERE fm.url IN (
                SELECT url
                FROM fm_detail
                WHERE article LIKE '%{search_query}%'
                UNION
                SELECT url
                FROM fm_detail
                WHERE title LIKE '%{search_query}%'
            )
        """             
    elif search_mode == 'title':
        query = f"""
            SELECT DISTINCT *
            FROM fm
            WHERE title LIKE '%{search_query}%'
        """
        
    query += f"ORDER BY time {order} OFFSET {(page-1)*count} LIMIT {count}"
    
    result = conn.execute(query).fetchall()
    search_items: List[Item] = [Item(**dict(zip(columns,item))) for item in result]
    return search_items