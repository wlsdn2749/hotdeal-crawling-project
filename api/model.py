from pydantic import BaseModel

class Item(BaseModel):
    recommend: int
    title: str
    comment: int
    shoppingmall: str
    price: str
    deliveryfee: str
    category: str
    time: str
    author: str