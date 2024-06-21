from pydantic import BaseModel,RootModel,Field
from datetime import datetime

class StockData(BaseModel):
    date:str=Field(alias="日期")
    trading_volume:str=Field(alias="成交股數")
    turnover:str=Field(alias="成交金額")
    open_price:float=Field(alias="開盤價")
    high_price:float=Field(alias="最高價")
    low_price:float=Field(alias="最低價")
    close_price:float=Field(alias="收盤價")
    change:float=Field(alias="漲跌價差")
    transactions:str=Field(alias="成交筆數")

class Data(RootModel):
    root:list[StockData]
