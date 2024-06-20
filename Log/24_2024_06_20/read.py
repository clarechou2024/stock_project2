import requests
import datetime as dt # 時間套件
import pandas as pd
from dateutil.relativedelta import relativedelta

stock_id = '1101'

month_num=6
# 當日時間
date_now = dt.datetime.now()

# 建立日期串列
date_list = [(date_now - relativedelta(months=i)).replace(day=1).\
             strftime('%Y%m%d') for i in range(month_num)]
date_list.reverse()

data:dict={}

# 使用迴圈抓取連續月份資料
for date in date_list:
    url = f'https://www.twse.com.tw/rwd/zh/afterTrading/\
        STOCK_DAY?date={date}&stockNo={stock_id}'
    try:
        json_data = requests.get(url).json()

        df = pd.DataFrame(data=json_data['data'],
                        columns=json_data['fields'])
    except Exception as e:
        print(f"無法取得{date}的資料, 可能資料量不足.")
    
    
