import pickle
import base64

from fastapi import APIRouter, Depends, Query, HTTPException, Response
from typing import Optional, List, Annotated, Literal
from pydantic import Field, field_validator, BaseModel, ValidationInfo
from app.database import db
from app.utils import load_valid_categories
from app.model import Item, HotdealItemDetail

hotdeal = APIRouter(prefix='/hotdeal')

VALID_CATEGORIES = load_valid_categories("./app/static/categories_fm.txt")
VALID_SITES = db.available_sites

class ItemList(BaseModel):
    '''
        각 page는 count만큼의 Item을 보여줌
        categories 필터를 추가함, 기본값은 모든 카테고리
    '''
    page: int = Field(Query(1, ge=1, description='Page number'))
    count: int = Field(Query(20, description='Number of items per page'))
    categories: List[str] = Field(Query([], description='List of categories'))
    sites: List[str] = Field(Query([], description='List of site'))
    order: str = Field(Query('desc', description='time order of items'))
    
    @field_validator('categories', 'order')
    @classmethod
    def check_attrs(cls, v, info: ValidationInfo):
        
        if info.field_name == 'sites':
            if not v:
                return None
            
            invalid_sites = [site for site in v if site not in VALID_SITES]
            
            if invalid_sites:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid sites: {', '.join(invalid_sites)}. Valid categories are: {', '.join(VALID_SITES)}"
                )
            
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
async def read_items(response: Response, itemlist: ItemList = Depends()):
    
    categories = itemlist.categories
    page = itemlist.page
    count = itemlist.count
    order = itemlist.order
    sites = itemlist.sites
    
    conn = db.get_connection()
    columns = list(Item.model_fields)
    
    query = f"""
        SELECT *
        FROM merged
    """

    page_query = f"""
        SELECT COUNT(*)
        FROM merged
    """
    
    optional_query = []
    query_parameters = []
    
    if categories:     
        categories_placeholder = ', '.join('?' * len(categories))
        categories_query = f"category IN ({categories_placeholder})"
        optional_query.append(categories_query)
        query_parameters.extend(categories)
        
    if sites:
        sites_placeholder = ', '.join('?' * len(sites))
        sites_query = f"site IN ({sites_placeholder})"
        optional_query.append(sites_query)
        query_parameters.extend(sites)
        
    if optional_query:
        query += " WHERE " + " AND ".join(optional_query)
        page_query += " WHERE " + " AND ".join(optional_query)
    
    query += f"ORDER BY time {order} OFFSET {(page-1)*count} LIMIT {count}"
    
    result = conn.execute(query, query_parameters).fetchall()

    if not result:
        raise HTTPException(status_code=400, detail="결과가 없습니다.")
    items: List[Item] = [Item(**dict(zip(columns,item))) for item in result]
    
    response.headers["X-Total-Count"] = str(conn.execute(page_query, query_parameters).fetchone()[0])
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
    
    if not result:
        raise HTTPException(status_code=404, detail="상세 페이지가 없습니다.")
    
    detail: HotdealItemDetail = dict(zip(colmuns, result))
    detail["comments"] = pickle.loads(base64.b64decode(detail["comments"].encode('utf-8')))
    return detail

@hotdeal.get('/search', tags=['hotdeal'], response_model= List[Item])
async def search(response: Response, p: SearchParameters = Depends()):
    
    conn = db.get_connection()
    
    page = p.page
    count = p.count
    search_mode = p.search_mode
    search_query = p.search_query
    order = p.order
    
    columns = list(Item.model_fields)
    
    if search_mode == 'title_content':     
        query = f"""
            SELECT DISTINCT merged.*
            FROM merged
            WHERE merged.url IN (
                SELECT url
                FROM merged_detail
                WHERE article LIKE '%{search_query}%'
                UNION
                SELECT url
                FROM merged
                WHERE title LIKE '%{search_query}%'
            )
        """
        
        count_query = f"""
            SELECT DISTINCT COUNT(merged.*)
            FROM merged
            WHERE merged.url IN (
                SELECT url
                FROM merged_detail
                WHERE article LIKE '%{search_query}%'
                UNION
                SELECT url
                FROM merged
                WHERE title LIKE '%{search_query}%'
            )
        """
        
    elif search_mode == 'title':
        query = f"""
            SELECT DISTINCT *
            FROM merged
            WHERE title LIKE '%{search_query}%'
        """
        
        count_query = f"""
            SELECT DISTINCT COUNT(*)
            FROM merged
            WHERE title LIKE '%{search_query}%'
        """
        
    query += f"ORDER BY time {order} OFFSET {(page-1)*count} LIMIT {count}"
    
    result = conn.execute(query).fetchall()
    search_items: List[Item] = [Item(**dict(zip(columns,item))) for item in result]
    
    response.headers["X-Total-Count"] = str(conn.execute(count_query).fetchone()[0])
    return search_items