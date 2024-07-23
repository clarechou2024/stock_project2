import tkinter as tk 
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.messagebox as msgbox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.feature_selection import SelectKBest,f_regression
import seaborn as sns
import numpy as np
import features
from features.feature import Feature
import pandas as pd
import matplotlib.ticker as  mticker
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class Window(tk.Tk):
    def __init__(self,theme:str=None,**kwargs):
        super().__init__(**kwargs)
        self.title("Test")

        #定義style的名稱
        style = ttk.Style()
        style.configure('Top.TFrame')
        style.configure('Top.TLabel',font=('Helvetica',25,'bold'))

        title_frame = ttk.Frame(self,style='Top.TFrame',borderwidth=2,relief='groove')
        ttk.Label(title_frame,text='Stock Forecast',style='Top.TLabel').pack(expand=True,fill='y')
        title_frame.pack(ipadx=100,ipady=10,padx=10,pady=10)

        center_frame  = ttk.Frame(borderwidth=2,relief='groove')
        ttk.Label(center_frame,text='請選擇技術圖',font=('Arial',20,'bold'),foreground='#000').pack(expand=True,fill='y')
        center_frame.pack(fill=tk.BOTH,expand=1,padx=100,pady=50)

        ttk.Button(self,text="Quit",command=self.destroy).pack(side='bottom')
        
      

#按鈕
        func_frame = title_frame = ttk.Frame(self,style='Top.TFrame',borderwidth=1)
        ttk.Label(func_frame,text="請選擇技術圖",font=('Arial',20,'bold'),foreground='#ADD').pack(expand=True,fill='y')
        ttk.Button(center_frame,text='5MA',command=self.click1).pack(side='left',expand=True)
        center_frame.pack(pady=10)
        ttk.Button(center_frame,text='20MA',command=self.click2).pack(side='left',expand=True)
        center_frame.pack(pady=10)
        ttk.Button(center_frame,text='60MA',command=self.click3).pack(side='left',expand=True)
        center_frame.pack(pady=10)


        ttk.Button(center_frame,text='線性回歸',command=self.Linear_regression).pack(side='left',expand=True)
        center_frame.pack(pady=10) 
        ttk.Button(center_frame,text='邏輯回歸',command=self.Logisticregression).pack(side='left',expand=True)
        center_frame.pack(pady=10)


        self.func_frame2  = ttk.Frame(self,borderwidth=1,relief='groove')
        self.func_frame2.pack(pady=10)

        

    def click1(self):
    
        sol=['sma']

        window=5
        original_datas=pd.DataFrame()

        original_datas = pd.read_csv("data.csv")
        original_datas = Feature().Calculate_Moving_Average(data=original_datas, window=window)
        
        self._stock_data=original_datas

        self.distplot_features(0, sol)



    def click2(self):

        sol=['sma']

        window=20
        original_datas=pd.DataFrame()

        original_datas = pd.read_csv("data.csv")
        original_datas = Feature().Calculate_Moving_Average(data=original_datas, window=window)

        self._stock_data=original_datas

        self.distplot_features(0, sol)

        

    def click3(self):
        sol=['sma']

        window=60
        original_datas=pd.DataFrame()

        original_datas = pd.read_csv("data.csv")
        original_datas = Feature().Calculate_Moving_Average(data=original_datas, window=window)

        self._stock_data=original_datas

        self.distplot_features(0, sol)

        

     # 定義自訂圖形函式
    def get_selected_features(self):

            alpha=float(self.alpha_combobox.get())

            data_x = self._stock_data.iloc[:, :-1]
            data_y = self._stock_data.iloc[:, -1]
            n = 16
            chi = SelectKBest(f_regression, k=n)
            arrchi = chi.fit_transform(data_x, data_y)
            score = np.round(chi.scores_,4)
            selected_scores = score[np.abs(score) > alpha]
            scoresort = np.argsort(selected_scores)
            scoresort = np.flipud(scoresort)
            col = self._stock_data.columns

            return col[scoresort]
    
    def clean_right(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    
    #畫常態圖
    def distplot_features(self,index,selected_features):

        for i, fea in enumerate(selected_features):
            fig, ax = plt.subplots(figsize=(6, 4))
            #     # Assuming ax is your subplot axis
            # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 设置日期格式
            # ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # 自动设置日期刻度间隔
            ax.plot(self._stock_data['Date'], self._stock_data['sma'], label='SMA')  # Plot SMA data
            ax.set_xlabel('Date')
            ax.set_ylabel('SMA')
            ax.set_title(fea)
            #x軸處理
            # tick_spacing = ax.set_xlabel['Date'].size/12
            # ax.xaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))

            # canvas = FigureCanvasTkAgg(fig, master=self.func_frame2)
            # canvas.draw()
            # canvas.get_tk_widget().grid(row=index, column=i, sticky="nsew")

             # 調整 X 軸刻度間距
            ax.xaxis.set_major_locator(mticker.AutoLocator())  # 自動設置刻度間距

            canvas = FigureCanvasTkAgg(fig, master=self.func_frame2)
            canvas.draw()
            canvas.get_tk_widget().grid(row=index, column=i, sticky="nsew")
    #=========================================================
    def feature_score(self,data,frame):

        df = data.iloc[:, :-1]
        target = data.iloc[:, -1]

        n = 5
        chi = SelectKBest(f_regression, k=16)
        chi.fit(df, target)

        score = abs(chi.scores_)
        scoresort = np.argsort(score)
        scoresort = np.flipud(scoresort)

        for idx in scoresort[:n]:
            feature = col[idx]
            correlation = score[idx]
            print("", "end", values=[feature, correlation])

        return list(col[scoresort[:n]])

    #=========================================================            
    #(回歸)線性回歸
    def Linear_regression(self):
        top_window = tk.Toplevel(self)
        top_window.title("線性回歸")
        top_window.geometry("600x500")

        # 创建文本框用于显示结果
        output_text = tk.Text(top_window, height=150, width=70)
        output_text.pack(pady=20)


    #讀取和處理數據
        data =pd.read_csv('data.csv')
        last_row = pd.DataFrame(data.tail(1))

        tdf = pd.DataFrame()
        tdf['Target'] = data['Close']

        f =['Open','High','Low','Adj Close','EMA12']

        # f= feature_score(data)
        last_row_y=last_row['Close']
        last_row_x=last_row[f]
        x = data[f].values  # 排除第一列（日期）和最后两列（Target和Close）
        y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    #數據預處理和分割
        x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.4,random_state=39830)
    #特徵和目標變量的標準化
        std_x = StandardScaler()
        x_train = std_x.fit_transform(x_train)
        x_test = std_x.transform(x_test)
        std_y = StandardScaler()
        y_train = std_y.fit_transform(y_train.reshape(-1, 1))
        y_test = std_y.transform(y_test.reshape(-1, 1))
    #建構和訓練線性回歸模型
        lr = LinearRegression()
        lr.fit(x_train, y_train)
        # print('權重值：{}'.format(lr.coef_))
        # print('偏置值：{}'.format(lr.intercept_))
    
    # #模型評估和預測
    #     y_predict = std_y.inverse_transform(lr.predict(x_test))
    #     y_real = std_y.inverse_transform(y_test)
    #     for i in range(50):
    #         print('預測值：{}，真實值：{}'.format(y_predict[i], y_real[i]))

    #     merror = mean_squared_error(y_real, y_predict)
    #     print('平均方差：{}'.format(merror))

    # 将输出结果插入到文本框中
        output_text.insert(tk.END, '權重值：{}\n'.format(lr.coef_))
        output_text.insert(tk.END, '偏置值：{}\n\n'.format(lr.intercept_))

        y_predict = std_y.inverse_transform(lr.predict(x_test))
        y_real = std_y.inverse_transform(y_test)

        output_text.insert(tk.END, '部分預測值與真實值對比：\n')
        # for i in range(min(50, len(y_predict))):
        #     output_text.insert(tk.END, '預測值：{:.2f}，真實值：{:.2f}\n'.format(y_predict[i][0], y_real[i][0]))

        y_last_row_predict = lr.predict(last_row_x.values.reshape(1, -1))[0][0]  # 提取单个预测值
        y_last_row_predict = pd.Series(y_last_row_predict)

        # output_text.insert(tk.END, '預測值：{:.2f}，真實值：{:.2f}\n'.format(y_last_row_predict, last_row_y))
    

        merror = mean_squared_error(y_real, y_predict)
        output_text.insert(tk.END, '\n平均方差：{:.2f}\n'.format(merror))

            

    #(分類)邏輯回歸
    def Logisticregression(self):
        top_window = tk.Toplevel(self)
        top_window.title("邏輯回歸")
        top_window.geometry("600x500")

    # 创建文本框用于显示结果
        output_text = tk.Text(top_window, height=20, width=70)
        output_text.pack(pady=20)

        data =pd.read_csv('data.csv')
        tdf= pd.DataFrame()

        tdf['Target'] = np.where(data['Close'].diff() > 0, 'Buy', 'Sell')

        x = data.iloc[:, 1:-1].values  # 假設需要排除第一列（日期）和最後兩列（Target和Close）
        y = tdf['Target'].values  # 使用 'Target' 作為目標變量

        x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.4,random_state=39830)
        transfer = StandardScaler()
        x_train = transfer.fit_transform(x_train)
        x_test = transfer.transform(x_test)
        estimator = LogisticRegression()
        estimator.fit(x_train, y_train)
        score = estimator.score(x_test, y_test)
        # print("Logistic 準確率：{}".format(score))
        output_text.insert(tk.END,"Logistic 準確率：{}".format(score))
        


def main():
    def on_closing():
        window.destroy()
        window.quit()

    window = Window(theme='arc')
    window.protocol("WM_DELETE_WINDOW",on_closing)
    window.mainloop()

if __name__=="__main__":
    main()