import pandas as pd

def calculate_bollinger_bands(data: pd.DataFrame, window=20, num_std=2)->pd.DataFrame:
    # 計算移動平均線
    data['MA'] = data['收盤價'].rolling(window=window).mean()
    
    # 計算標準差
    data['std_dev'] = data['收盤價'].rolling(window=window).std()
    
    # 計算布林通道的上限線和下限線
    data['UpperBand'] = data['MA'] + num_std * data['std_dev']
    data['LowerBand'] = data['MA'] - num_std * data['std_dev']
    
    return data
