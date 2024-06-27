import os
import requests
import datetime as dt # 時間套件
import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta

def Check_Data_Csv():
    if os.path.exists("data.csv"):
        print("檔案存在")
        return True
    else:
        return False

def Get_N_Month_Data(month_num:int,stock_id:int) ->pd.DataFrame:
    ticker = f'{stock_id}.TW'  # 這裡使用蘋果公司（AAPL）作為例子
    start_date = '2008-01-01'
    end_date = '2023-12-31'
    data = yf.download(ticker, start=start_date, end=end_date)
# # 當日時間
#     date_now = dt.datetime.now()

#     # 建立日期串列
#     date_list = [(date_now - relativedelta(months=i)).replace(day=1).\
#                 strftime('%Y%m%d') for i in range(month_num)]
#     date_list.reverse()

#     # 用於存儲每個月的數據
#     all_data = []

#     # 使用迴圈抓取連續月份資料
#     for date in date_list:
#         url = f'https://www.twse.com.tw/rwd/zh/afterTrading/\
#             STOCK_DAY?date={date}&stockNo={stock_id}'
#         try:
#             json_data = requests.get(url).json()

#             df = pd.DataFrame(data=json_data['data'],
#                             columns=json_data['fields'])
        
#             all_data.append(df)

#         except Exception as e:
#             print(f"無法取得{date}的資料, 可能資料量不足.")

#     # 合併所有月份的數據
#     if all_data:
#         final_df = pd.concat(all_data, ignore_index=True)
#     else:
#         final_df = pd.DataFrame()

    return data
    
def Get_Data_Dict(data:pd.DataFrame)->dict:
    
    try:
        if not data.empty: 
            columns_list = data.columns.tolist()
            datas_list = data.values.tolist()

            final_dict_list = []
            for row in datas_list:
                row_dict = {columns_list[i]: row[i] for i in range(len(columns_list))}
                final_dict_list.append(row_dict)
        
            return final_dict_list
        else:
            print("資料遺失或空白 DataFrame")
            return {}
    except Exception as e:
        print(f"發生錯誤: {str(e)}")
        return {}
    

    
