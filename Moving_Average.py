import pandas as pd

def Calculate_Moving_Average(data: pd.DataFrame, window: int = 5) -> pd.Series:
    # 将日期列转换为日期时间格式
    # 按日期排序（如果未排序的话）
    data = data.sort_values(by='日期')

    # 计算收盘价的移动平均
    sma = data['收盤價'].rolling(window=window).mean()

    return sma