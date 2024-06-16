from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from datetime import datetime

class Item(BaseModel):
    site: str
    url: str
    recommend: int
    title: str
    comment: int
    shoppingmall: str
    price: str
    deliveryfee: str
    category: str
    time: datetime
    author: str
    
class HotdealItemDetail(BaseModel):
    site: str
    url: str
    title: str
    date: str
    author: str
    views: int
    likes: int
    comment_count: int
    related_url: str
    shoppingmall: str
    product_name: str
    price: str
    deliveryfee: str
    article: Optional[str] = None
    comments: List[Dict[str, Union[str, int, List]]] = None