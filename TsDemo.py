import tushare as ts

df = ts.get_realtime_quotes("515180")[['name', 'price', 'pre_close', 'date', 'time']]

print(df)
