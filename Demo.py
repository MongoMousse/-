import tushare as ts
import schedule as schedule



def get_now_jiage(code):
   df = ts.get_realtime_quotes(code)[['name','price','pre_close','date','time']]
   return df

def do_programe(code):
    if pd_ztjytime()==False: #判断是否在暂停交易的时间范围内
        info=get_now_jiage(code) #调用方法获取当前的DataFrame
        now_jiage=float(info['price'][0]) #获取现价
        name=info['name'][0] #获取证券名称
        pre_close=float(info['pre_close'][0]) #获取昨日收盘价
        riqi=info['date'][0] #获取现价对应的日期
        sj=info['time'][0] #获取价格对应的时间
        now_zdie=round((now_jiage-pre_close)/pre_close*100,2) #计算现在的涨跌幅
        all_zdie=round((now_jiage-cbj)/cbj*100,2)  #计算股票持有期间内总的涨跌幅，其中cbj为购买时候的成本价，需要约定全局变量
        now_shizhi=round(shuliang*now_jiage,2) #计算股票现在的市值，其中shuliang为购买股票的数量，需要约定为全局变量
        ykui=round(now_shizhi-cbj*shuliang,2)  #计算股票现在总的盈亏
        if (abs(now_zdie)>=3 and abs(now_zdie)<3.09) or (abs(now_zdie)>=6  and abs(now_zdie)<6.05)  or (abs(now_zdie)>=9 and  abs(now_zdie)<9.1) : #判断现在的涨跌幅是否在目标范围内
            email_comment = []
            email_comment.append('<html>')
            email_comment.append('<b><p><h3><font size="2" color="black">您好：</font></h4></p></b>')
            email_comment.append('<p><font size="2" color="#000000">根据设置参数，现将监控到'+name+'('+str(code)+')的证券价格异动消息汇报如下：</font></p>')
            email_comment.append('<table border="1px" cellspacing="0px"   width="600" bgcolor=' + color_bg_fg + ' style="border-collapse:collapse">')

            email_comment.append('<tr>')
            email_comment.append('<td align="center"><b>序号</b></td>')
            email_comment.append('<td align="center"><b>购买单价</b></td>')
            email_comment.append('<td align="center"><b>持股数</b></td>')
            email_comment.append('<td align="center"><b>现价</b></td>')
            email_comment.append('<td align="center"><b>现涨跌幅</b></td>')
            email_comment.append('<td align="center"><b>总涨跌幅</b></td>')
            email_comment.append('<td align="center"><b>现市值</b></td>')
            email_comment.append('<td align="center"><b>盈亏额</b></td>')
            email_comment.append('<td align="center"><b>异动时间</b></td>')
            email_comment.append('</tr>')

            email_comment.append('<tr>')
            email_comment.append('<td align="center">'+str(1)+'</td>')
            email_comment.append('<td align="center">'+str(cbj) + '</td>')
            email_comment.append('<td align="center">' + str(shuliang) + '</td>')
            email_comment.append('<td align="center">' + str(now_jiage) +'</td>')
            email_comment.append('<td align="center">' + str(now_zdie) + '%</td>')
            email_comment.append('<td align="center">' + str(all_zdie) + '%</td>')
            email_comment.append('<td align="center">' + str(now_shizhi) + '元</td>')
            email_comment.append('<td align="center">' + str(ykui) + '元</td>')
            email_comment.append('<td align="center">' + str(riqi) +' '+str(sj) +'</td>')
            email_comment.append('</tr>')
            email_comment.append('</table>')
            email_comment.append('<p><font size="2" color="black">祝：股市天天红，日日发大财！</font></p>')
            email_comment.append('</html>')
            send_msg = '\n'.join(email_comment)
            send_Email(email_add[0], send_msg)


def run():
    while True:
        do_programe('600905')
        now_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d1 = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 15:00:00', '%Y-%m-%d %H:%M:%S')
        delta = d2 - d1
        if delta.total_seconds()<=0:
          sys.exit()
        time.sleep(1)

if __name__ == '__main__':
    schedule.every().day.at("09:30").do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)