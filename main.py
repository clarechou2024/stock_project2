import data_loading as rdata
import datas
from datas import Data
import datetime
import pandas as pd

def main():
    month_num=6
    stock_id=1101

    month_datas:pd.DataFrame=rdata.Get_N_Month_Data(month_num=month_num,stock_id=stock_id)
    month_datas['日期'] = month_datas['日期'].apply(datas.parse_custom_date)

    data_list:list=rdata.Get_Data_Dict(month_datas)
    data:Data=Data.model_validate(data_list)
    stock_datas:list[dict]=data.model_dump()


    
if __name__ =="__main__":
    main()