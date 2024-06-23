import data_loading as rdata
import datas
from datas import Data
import features
import datetime
import pandas as pd
from features.feature import Feature

def main():
    month_num=6
    stock_id=1101
    file_path='data.csv'

    month_datas=pd.DataFrame()
    #檢查是否檔案下載了
    if rdata.Check_Data_Csv():
        print("csv 已經存在")
        month_datas = pd.read_csv(file_path)
    else:
        print("下載檔案")
        month_datas:pd.DataFrame=rdata.Get_N_Month_Data(month_num=month_num,stock_id=stock_id)
        #將該網站的日期從str -> datetime
        month_datas['日期'] = month_datas['日期'].apply(datas.parse_custom_date)

    window=20
    sma:pd.Series = Feature().Calculate_Moving_Average(data=month_datas, window=window)
    month_datas['sma']=sma

    rsi:pd.Series= Feature().Calculate_Rsi(data=month_datas,window=window)
    month_datas['rsi']=rsi

    num_std=2
    month_datas:pd.DataFrame=Feature().Calculate_Bollinger_Bands(data=month_datas,window=window,num_std=num_std)

    print(month_datas)

    # 將 month_datas 寫入 data.csv
    month_datas.to_csv('data.csv', index=False)
    
if __name__ =="__main__":
    main()