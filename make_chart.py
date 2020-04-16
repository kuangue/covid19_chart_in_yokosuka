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

def line_chart(lst):
    df = lst[0].sort_values('患者確定日')
    for idx, row in df.iterrows():
        df.at[idx, '患者確定日']=pd.to_datetime("2020年"+row['患者確定日'], format='%Y年%m月%d日')

    chart=df.groupby('患者確定日').size()

    # join
    full_date=get_datelist()
    for idx, val in full_date.iteritems():
        if idx in chart:
            full_date[idx]=chart[idx]

    df_full_date=pd.DataFrame({'新規感染者数':full_date})
    df_full_date['感染者総数']=0

    # sum
    psum = 0
    for idx,item in df_full_date.iterrows():
        psum=psum+df_full_date.at[idx, '新規感染者数']
        df_full_date.at[idx, '感染者総数']=psum

    tdy=dd.today().strftime('%Y-%m-%d')

    # describe chart
    ax = df_full_date.plot(title='新規感染者数(横須賀市)'+tdy)
    ax.set_xlabel('日付')
    ax.set_ylabel('染者数')
    fig = ax.get_figure()
    fig.savefig('chart_of_covid19_in_yokosuka.png')

def pie_chart_age(lst):
    df = lst[0]
    filtered_df=df.query('年代 != "-"')
    grouped_se = filtered_df.groupby('年代').size()
    print(type(grouped_se))
    ax = grouped_se.plot(kind='pie', title='年代別円グラフ@横須賀市')
    ax.set_xlabel('')
    ax.set_ylabel('')
    fig = ax.get_figure()
    fig.savefig('pie_chart_of_age_in_yokosuka.png')

if __name__=='__main__':
    lst = pd.read_html('https://www.city.yokosuka.kanagawa.jp/3130/hasseijoukyou.html', flavor='bs4')

    line_chart(lst)
    pie_chart_age(lst)
