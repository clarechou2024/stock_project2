import pandas as pd

def calculate_rsi(data:pd.DataFrame, window=14)->pd.Series:
    """
    Calculate RSI (Relative Strength Index) for given data.
    
    Parameters:
    - data: pandas DataFrame with 'Close' prices.
    - window: RSI window period (default is 14).
    
    Returns:
    - pandas Series with RSI values.
    """

    delta = pd.Series(data['收盤價'].astype(float).values).diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

