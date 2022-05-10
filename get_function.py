from jqdata import finance
import datetime
from datetime import timedelta
from jqdata import *
import pandas as pd
import numpy as np


# 获取指定日期成立满1年且未退市的偏股混合基金
def get_fund_code(tradeDate, stock_rate_min=0, stock_rate_max=100):
    start_date=datetime.datetime.strptime(tradeDate,'%Y-%m-%d')-timedelta(days=365)
    start_date=start_date.strftime('%Y-%m-%d')
    report_date=get_report_date(tradeDate)
    codes=list(finance.run_query(query(finance.FUND_MAIN_INFO.main_code).filter(
            finance.FUND_MAIN_INFO.operate_mode_id.in_(["401001","401006"]),                #开放式&LOF
            finance.FUND_MAIN_INFO.underlying_asset_type_id.in_(["402001","402004"]),       #股基&混基
            finance.FUND_MAIN_INFO.invest_style_id.in_(["005001","005005"]),                #股基+偏股混合基
            finance.FUND_MAIN_INFO.start_date < start_date).filter(
            (finance.FUND_MAIN_INFO.end_date > tradeDate) |
            (finance.FUND_MAIN_INFO.end_date == None)))['main_code'].values)
    # 限制股票占比高于70%
    codes=list(finance.run_query(query(finance.FUND_PORTFOLIO.code).filter(
        finance.FUND_PORTFOLIO.code.in_(codes), 
        finance.FUND_PORTFOLIO.stock_rate >= stock_rate_min,
        finance.FUND_PORTFOLIO.stock_rate <= stock_rate_max,
        finance.FUND_PORTFOLIO.period_end==report_date))['code'].values)
    return codes

# 分组函数，按当期净资产从小到大分为N组
def group_by_net_asset(reportDate,code,groupCount):
    data=get_net_asset(reportDate,code)                         #获取净资产值
    data.sort_values(by='total_tna',ascending=True,inplace=True)#从小到大排序
    data['group']=data.rank(ascending=True).astype(int)         #获得排序叙述
    each_count=int(len(data)/groupCount)                        #计算每组个数
    data['group']=(data['group'] / each_count + 1).astype(int)  #按序数计算分组值
    data.loc[(data['group']>=groupCount+1),'group']=groupCount  #最后剩下的部分归于最大组
    return data

# 分组函数，按当期总资产从小到大分为N组
def group_by_total_asset(reportDate,code,groupCount):
    data=get_total_asset(reportDate,code)                           #获取净资产值
    data.sort_values(by='total_asset',ascending=True,inplace=True)  #从小到大排序
    data['group']=data.rank(ascending=True).astype(int)             #获得排序叙述
    each_count=int(len(data)/groupCount)                            #计算每组个数
    data['group']=(data['group'] / each_count + 1).astype(int)      #按序数计算分组值
    data.loc[(data['group']>=groupCount+1),'group']=groupCount      #最后剩下的部分归于最大组
    return data

# 分组函数，按当期股票资产从小到大分为N组
def group_by_stock_asset(reportDate,code,groupCount):
    data=get_stock_asset(reportDate,code)                           #获取净资产值
    data.sort_values(by='stock_value',ascending=True,inplace=True)  #从小到大排序
    data['group']=data.rank(ascending=True).astype(int)             #获得排序叙述
    each_count=int(len(data)/groupCount)                            #计算每组个数
    data['group']=(data['group'] / each_count + 1).astype(int)      #按序数计算分组值
    data.loc[(data['group']>=groupCount + 1),'group']=groupCount    #最后剩下的部分归于最大组
    return data

#获取净资产规模
def get_net_asset(reportDate,code):
    data = finance.run_query(query(
        finance.FUND_FIN_INDICATOR.code,
        finance.FUND_FIN_INDICATOR.total_tna
    ).filter(
        finance.FUND_FIN_INDICATOR.code.in_(code), 
        finance.FUND_FIN_INDICATOR.period_end==reportDate,
        finance.FUND_FIN_INDICATOR.total_tna > 0))
    data.set_index('code',inplace=True)
    data=data[~np.isinf(data)]
    data.dropna(inplace=True)
    print("%s：获取到%s只基金规模" % (reportDate, len(data)))
    return data

#获取总资产规模
def get_total_asset(reportDate,code):
    data = finance.run_query(query(
        finance.FUND_PORTFOLIO.code,
        finance.FUND_PORTFOLIO.total_asset
    ).filter(
        finance.FUND_PORTFOLIO.code.in_(code), 
        finance.FUND_PORTFOLIO.period_end==reportDate,
        finance.FUND_PORTFOLIO.total_asset > 0))
    data.set_index('code',inplace=True)
    data=data[~np.isinf(data)]
    data.dropna(inplace=True)
    print("%s：获取到%s只基金规模" % (reportDate, len(data)))
    return data

#获取股票资产规模
def get_stock_asset(reportDate,code):
    data = finance.run_query(query(
        finance.FUND_PORTFOLIO.code,
        finance.FUND_PORTFOLIO.stock_value
    ).filter(
        finance.FUND_PORTFOLIO.code.in_(code), 
        finance.FUND_PORTFOLIO.period_end==reportDate,
        finance.FUND_PORTFOLIO.stock_value > 0))
    data.set_index('code',inplace=True)
    data=data[~np.isinf(data)]
    data.dropna(inplace=True)
    print("%s：获取到%s只基金规模" % (reportDate, len(data)))
    return data

# 计算季度收益
def cal_rtn(start_date,end_date,code):
    #上季度复权累积净值。使用复权累积净值是认为基金分红又全部投入该基金
    pre_data=finance.run_query(query(finance.FUND_NET_VALUE.code,
                                 finance.FUND_NET_VALUE.refactor_net_value
                                ).filter(finance.FUND_NET_VALUE.code.in_(code))
                                        .filter(finance.FUND_NET_VALUE.day==start_date))
    pre_data.set_index('code',inplace=True)
    pre_data=pre_data[pre_data>0].dropna()
    #当前季度复权累积净值
    data=finance.run_query(query(finance.FUND_NET_VALUE.code,
                                 finance.FUND_NET_VALUE.refactor_net_value
                                ).filter(finance.FUND_NET_VALUE.code.in_(code))
                                        .filter(finance.FUND_NET_VALUE.day==end_date))
    data.set_index('code',inplace=True)
    data=data[data>0].dropna()
    #计算净值涨幅
    result=(data/pre_data).dropna()-1
    return result

# 获取每月最后一个交易日
def get_month_end(trade_day):
    cal=[]
    for i in range(len(trade_day)-1):
        if trade_day[i].month!=trade_day[i+1].month:
            cal.append(trade_day[i])
    return cal

# 计算当前日期的上一个报表日
def get_report_date(tradeDate):
    if isinstance(tradeDate, str):
        tradeDate=datetime.datetime.strptime(tradeDate,"%Y-%m-%d")
    year=tradeDate.year
    month=tradeDate.month
    report_month=(month-1) //3*3
    if report_month==0:
        report_month=12
        year=year-1
    day=30
    if report_month in [3,12]:
        day=31
    report_date=str(year)+'-'+str(report_month).rjust(2,'0')+'-'+str(day)
    return report_date