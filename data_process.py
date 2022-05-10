#In[]
from get_function import *
from jqdata import finance
import datetime
from datetime import timedelta
from jqdata import *
import pandas as pd
import numpy as np
# 净资产分组
start_date='2012-04-29'
end_date='2022-04-29'
trade_days=get_trade_days(start_date,end_date)
month_end=get_month_end(trade_days)
groupCount=10

result={}
# 第一次分组
report_date=get_report_date(month_end[0])#获取上一报表日
group_data=group_by_net_asset(report_date,code,groupCount)
for i in range(1,len(month_end)-1):
    start_date=month_end[i-1].strftime('%Y-%m-%d')
    end_date=month_end[i].strftime('%Y-%m-%d')
    code=get_fund_code(start_date)
    #计算本月累积净值涨幅
    rtn=cal_rtn(start_date,end_date,code)
    #融合净值涨幅与分组
    data=pd.merge(group_data,rtn,left_index=True,right_index=True)
    #计算每组涨幅均值
    mean=data[['refactor_net_value','group']].groupby('group').mean()['refactor_net_value'].to_dict()
    #记录当前月份每组涨幅
    result[end_date]=mean
    #在报表月份下一月重新分组
    if month_end[i].month in [4,10]:
        report_date=get_report_date(month_end[i])#获取上一报表日
        group_data=group_by_net_asset(report_date,code,groupCount)

result = (pd.DataFrame(result).T+1).cumprod()#计算累计净值

# 展示最近一期各分组规模细节
group_data.pivot_table(index="group",aggfunc=[len, min, np.mean, max])

#In[]
print(result.tail(1).values.max() / result.tail(1).values.min())
result.tail(1)
result.tail(1).plot(kind='bar')
result.plot(figsize=[15,10])

#In[]
# 总资产分组
result={}
# 第一次分组
report_date=get_report_date(month_end[0])#获取上一报表日
group_data=group_by_total_asset(report_date,code,groupCount)
for i in range(1,len(month_end)-1):
    start_date=month_end[i-1].strftime('%Y-%m-%d')
    end_date=month_end[i].strftime('%Y-%m-%d')
    code=get_fund_code(start_date)
    #计算本月累积净值涨幅
    rtn=cal_rtn(start_date,end_date,code)
    #融合净值涨幅与分组
    data=pd.merge(group_data,rtn,left_index=True,right_index=True)
    #计算每组涨幅均值
    mean=data[['refactor_net_value','group']].groupby('group').mean()['refactor_net_value'].to_dict()
    #记录当前月份每组涨幅
    result[end_date]=mean
    #在报表月份下一月重新分组
    if month_end[i].month in [4,10]:
        report_date=get_report_date(month_end[i])#获取上一报表日
        group_data=group_by_total_asset(report_date,code,groupCount)

result = (pd.DataFrame(result).T+1).cumprod()#计算累计净值

# 展示最近一期各分组规模细节
group_data.pivot_table(index="group",aggfunc=[len, min, np.mean, max])

#In[]
print(result.tail(1).values.max() / result.tail(1).values.min())
result.tail(1)
result.tail(1).plot(kind='bar')

#In[]
# 股票资产分组
result={}
# 第一次分组
report_date=get_report_date(month_end[0])#获取上一报表日
group_data=group_by_stock_asset(report_date,code,groupCount)
for i in range(1,len(month_end)-1):
    start_date=month_end[i-1].strftime('%Y-%m-%d')
    end_date=month_end[i].strftime('%Y-%m-%d')
    code=get_fund_code(start_date)
    #计算本月累积净值涨幅
    rtn=cal_rtn(start_date,end_date,code)
    #融合净值涨幅与分组
    data=pd.merge(group_data,rtn,left_index=True,right_index=True)
    #计算每组涨幅均值
    mean=data[['refactor_net_value','group']].groupby('group').mean()['refactor_net_value'].to_dict()
    #记录当前月份每组涨幅
    result[end_date]=mean
    #在报表月份下一月重新分组
    if month_end[i].month in [4,10]:
        report_date=get_report_date(month_end[i])#获取上一报表日
        group_data=group_by_stock_asset(report_date,code,groupCount)

result = (pd.DataFrame(result).T+1).cumprod()#计算累计净值

# 展示最近一期各分组规模细节
group_data.pivot_table(index="group",aggfunc=[len, min, np.mean, max])

#In[]
print(result.tail(1).values.max() / result.tail(1).values.min())
result.tail(1)
result.tail(1).plot(kind='bar')

#In[]
tradeDate='2022-04-29'
print(
    len(get_fund_code(tradeDate, stock_rate_min=0, stock_rate_max=30)), 
    len(get_fund_code(tradeDate, stock_rate_min=30, stock_rate_max=70)), 
    len(get_fund_code(tradeDate, stock_rate_min=70, stock_rate_max=100)))