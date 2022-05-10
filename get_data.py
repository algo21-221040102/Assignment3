#In[]
from jqdata import finance
code = list(finance.run_query(query(finance.FUND_MAIN_INFO).filter(
        finance.FUND_MAIN_INFO.start_date <= '2021-04-30',
        finance.FUND_MAIN_INFO.end_date == None,
        finance.FUND_MAIN_INFO.operate_mode_id.in_(["401001","401006"]),            #开放式&LOF
        finance.FUND_MAIN_INFO.underlying_asset_type_id.in_(["402001","402004"]),   #股基&混基
        finance.FUND_MAIN_INFO.invest_style_id.in_(["005001","005005"])             #股基+偏股混合基
        ))['main_code'].values)
len(code)

#In[]
# 按净资产规模分布
data = finance.run_query(query(finance.FUND_FIN_INDICATOR.total_tna)
                  .filter(finance.FUND_FIN_INDICATOR.code.in_(code))
                  .filter(finance.FUND_FIN_INDICATOR.period_end=='2022-03-31')
                  .filter(finance.FUND_FIN_INDICATOR.total_tna > 0))                #保留净资产大于0的基金
print(len(data))
print(np.mean(data), np.median(data))
log10(data).hist(bins=100)

#In[]
# 按总资产规模分布
data = finance.run_query(query(finance.FUND_PORTFOLIO.total_asset)
                  .filter(finance.FUND_PORTFOLIO.code.in_(code))
                  .filter(finance.FUND_PORTFOLIO.period_end=='2022-03-31')
                  .filter(finance.FUND_PORTFOLIO.total_asset > 0))                  #保留资产大于0的基金
print(len(data))
print(np.mean(data), np.median(data))
log10(data).hist(bins=100)

#In[]
# 按股票类资产规模分布
data = finance.run_query(query(finance.FUND_PORTFOLIO.stock_value)
                  .filter(finance.FUND_PORTFOLIO.code.in_(code))
                  .filter(finance.FUND_PORTFOLIO.period_end=='2022-03-31')
                  .filter(finance.FUND_PORTFOLIO.stock_value > 0))                  #保留资产大于0的基金
print(len(data))
print(np.mean(data), np.median(data))
log10(data).hist(bins=100)