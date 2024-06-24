from pydantic import BaseModel
from typing import Optional, List, Dict, Union
from datetime import datetime

class Item(BaseModel):
    site: Optional[Union[str, int]]
    url: Optional[Union[str, int]]
    recommend: Optional[Union[str, int]]
    title: Optional[Union[str, int]]
    comment: Optional[Union[str, int]]
    shoppingmall: Optional[Union[str, int]]
    price: Optional[Union[str, int]]
    deliveryfee: Optional[Union[str, int]]
    category: Optional[Union[str, int]]
    time: datetime
    author: Optional[Union[str, int]]
    views: Optional[Union[str, int]]
    
class HotdealItemDetail(BaseModel):
    site: str
    url: str
    title: str
    date: datetime
    author: str
    views: Optional[Union[str, int]]
    likes: Optional[Union[str, int]]
    comment_count: Optional[Union[str, int]]
    related_url: str
    shoppingmall: str
    product_name: str
    price: str
    deliveryfee: str
    article: Optional[str] = None
    comments: List[Dict[str, Union[str, int, List]]] = None