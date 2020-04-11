from bs4 import BeautifulSoup
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import japanize_matplotlib
from datetime import datetime as dt
from datetime import date as dd
from datetime import timedelta

def get_datelist():
    strdt = dt.strptime("2020-03-01", '%Y-%m-%d')
    enddt = dt.today()

    days_num = (enddt - strdt).days + 1

    datelist = []
    zeros = [0] * days_num
    for i in range(days_num):
        datelist.append(strdt + timedelta(days=i))

    full_date = pd.Series(zeros, datelist)

    return full_date


if __name__=='__main__':
    lst = pd.read_html('https://www.city.yokosuka.kanagawa.jp/3130/hasseijoukyou.html', flavor='bs4')

    df = lst[0].sort_values('患者確定日')
    for idx, row in df.iterrows():
        df.at[idx, '患者確定日']=pd.to_datetime("2020年"+row['患者確定日'], format='%Y年%m月%d日')

    chart=df.groupby('患者確定日').size()

    # join
    full_date=get_datelist()
    for idx, val in full_date.iteritems():
        if idx in chart:
            full_date[idx]=chart[idx]

    df_full_date=pd.DataFrame({'each':full_date})
    df_full_date['sum']=0

    psum = 0
    for idx,item in df_full_date.iterrows():
        psum=psum+df_full_date.at[idx, 'each']
        df_full_date.at[idx, 'sum']=psum


    plt.plot(df_full_date)
    tdy=dd.today().strftime('%Y-%m-%d')
    plt.title('新規感染者数(横須賀市)'+tdy)
    plt.xlabel('日付')
    plt.ylabel('新規感染者数')
    plt.gcf().autofmt_xdate()
    plt.savefig('chart_of_covid19_in_yokosuka.png')
