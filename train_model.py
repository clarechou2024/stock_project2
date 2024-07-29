from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression

def Decision_tree_Regressor(test_size,data,feature):
    
    tdf = pd.DataFrame()
    tdf['Target'] = data['CloseY']

    x = data[feature].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=39830)

    dec = DecisionTreeRegressor(random_state=39830)
    dec.fit(x_train, y_train)

    # 在测试集上评估模型
    y_pred = dec.predict(x_test)
    mse = round(mean_squared_error(y_test, y_pred),4)
    r2 = round(r2_score(y_test, y_pred),4)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_last_predict = dec.predict((x_last_predict))

    return mse,r2,round(y_last_predict[0],4)

def Linear_regression(test_size,data,feature):
    tdf = pd.DataFrame()
    tdf['Target'] = data['CloseY']

    x = data[feature].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=test_size,random_state=39830)
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    # print('權重值：{}'.format(lr.coef_))
    # print('偏置值：{}'.format(lr.intercept_))

    y_predict = std_y.inverse_transform(lr.predict(x_test))
    y_test=std_y.inverse_transform(y_test)

    mse = round(mean_squared_error(y_test, y_predict),4)
    r2 = round(r2_score(y_test, y_predict),4)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_last_predict = lr.predict((x_last_predict))


    return mse,r2,round(y_last_predict[0][0],4)

def Decision_tree_Classifier(test_size,data,feature):
    
    tdf = pd.DataFrame()
    tdf['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 'Buy', 'Sell')

    x = data[feature].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=39830)

    dec = DecisionTreeClassifier(random_state=39830)
    dec.fit(x_train, y_train)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_pred = dec.predict(x_last_predict)
    score = dec.score(x_test, y_test)

    return score,y_pred[0]

def Logisticregression(test_size,data,feature):
    tdf= pd.DataFrame()

    tdf['Target'] = np.where(data['CloseY'].diff() > 0, 'Buy', 'Sell')

    x = data[feature].values  # 假設需要排除第一列（日期）和最後兩列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作為目標變量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=test_size,random_state=39830)
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    estimator = LogisticRegression()
    estimator.fit(x_train, y_train)
    score = estimator.score(x_test, y_test)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_pred = estimator.predict(x_last_predict)
    
    return score,y_pred[0]
