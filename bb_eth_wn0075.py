import bybit
import pandas as pd 
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
import collections
from urllib.request import urlopen
from urllib.error import HTTPError


client = bybit.bybit(test=False, api_key="NWnSrOPiVJZ1wEIbMw", api_secret="dihn6uASHn9s2BSuV6DAJPgP65st1PQaFJks")
apiKey='NWnSrOPiVJZ1wEIbMw'
apisecret='dihn6uASHn9s2BSuV6DAJPgP65st1PQaFJks'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="NWnSrOPiVJZ1wEIbMw",
    api_secret="dihn6uASHn9s2BSuV6DAJPgP65st1PQaFJks")

   
num=1

while True:
    try:

        ticker="ETHUSDT"
        
        # 분봉가저오기
        now = datetime.utcnow()
        time_s = int(now.second) #초 카운트
        time_m = int(now.minute) #분 카운트
        unixtime = calendar.timegm(now.utctimetuple())
        # 1시간초단위=60, 20개 가저오기, interval="1" =1분봉
        since = unixtime - 60*20
        response=session.query_kline(symbol=ticker,interval="1",**{'from':since})['result']
        df = pd.DataFrame(response)
        df_1=df['close'].astype(float)#문자열 숫자열로변환

        average = numpy.mean(df_1)
        std=numpy.std(df_1)
        average20 = float(round(average,2))

        bb_u=round(float(average20 + std*2),0)
        bb_l=round(float(average20 - std*2),0)

         # 5분초단위=300, 20개 가저오기, interval="5" =5분봉
        since_5 = unixtime - 300*20
        response_5=session.query_kline(symbol=ticker,interval="5",**{'from':since_5})['result']
        df_2 = pd.DataFrame(response_5)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_5 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_5_20 = float(round(average_5,2))

        bb_u_5=round(float(average_5_20 + std_1*2),1)
        bb_l_5=round(float(average_5_20 - std_1*2),1)


        # 내 포지션 정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()

        
        buy_size = float(my_infor[0]["result"][0]["size"])
        sell_size = float(my_infor[0]["result"][1]["size"])

        # #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),0)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),0)


        # #각 포지션 청산가격
        # buy_liq_price=round(float(my_infor[0]["result"][0]["liq_price"]),2)
        # sell_liq_price=round(float(my_infor[0]["result"][1]["liq_price"]),2)            
        
        # 내 활성주문 가저오기
        my_query= client.LinearOrder.LinearOrder_query(symbol=ticker).result()
        # 활성주문중 청산주문골라내기
        count_1 = my_query[0]["result"]
        re_len = len(count_1)

        if re_len ==0:
            count_side = 0
        else:
            count_side = count_1[-1]["side"]

        
        print(count_side)
        print(re_len)

        
        # #자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))


        #현재가조회(USDT)
        now_close_1 = client.LinearKline.LinearKline_get(symbol=ticker, interval="1", **{'from':unixtime-120}).result()
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),4)

        # now_open_1 = round(float(now_close_1[0]["result"][-1]["open"]),2) #전봉의 시가
        # now_open = round(float(now_close_1[0]["result"][-2]["open"]),2) #전봉의 시가
        # now_low = round(float(now_close_1[0]["result"][-2]["low"]),2)   #전봉의 저가
        # now_high = round(float(now_close_1[0]["result"][-2]["high"]),2) #전봉의 고가
        # h_close = round(float(now_close_1[0]["result"][-2]["close"]),2) #전봉의 종가

        # #전봉의 볼리저상하단 이격 차이
        # bb_low = round(bb_l - now_low,2)
        # bb_high = round(now_high - bb_u,2)

        # #평단과 현재가의 차이
        # if buy_entry_price != 0:
        #     buy_geb =abs(round((buy_entry_price-now_close)/buy_entry_price,2))
        # else:
        #     buy_geb = 0
        # if sell_entry_price !=0:
        #     sell_geb = abs(round((sell_entry_price-now_close)/sell_entry_price,2))
        # else:
        #     sell_geb = 0
       

        # # 매수 현재가
        # # 현재가가 볼린저 상하단에 있을때 매수매도신호가 들어가면 볼린저 상단부터 현재가까지 시장가로 채결되는것을 방지하기위해 현재가가 볼린저상하단이탈한상태에서는 현재가를 기준으로 매수매도 주문을 넣는다
        # if bb_l > now_close:
        #     a = now_close
        # else:
        #     a = bb_l

        # #매도 현재가
        # if bb_u < now_close:
        #     a_1 = now_close
        # else:
        #     a_1 = bb_u


        #볼린저 상하단 격차
        bb_cc = round((bb_u-bb_l)/bb_u,2)
       
        # print(bb_u)
        # print(bb_l)
        #매수매도주문 Buy 첫글자"B"는 대문자여야함


         # 진입가격 결정, 
        
        if 500 > my_usdt:
            now_qty20 = 0 
        elif 500 < my_usdt < 10000:
            now_qty20 = (my_usdt/now_close)/3.5
        elif 10000 < my_usdt:
            now_qty20 = (11000/now_close)/3.5
        else:
            pass

        # 위험수량 결정 자본금의 7배 이상      
        gty_d = round((my_usdt/now_close)*3,0)

        # 기본 수량 계산 - 반대포지션이 이수량되면 두배매수
        gty_c = round((my_usdt/now_close)*3,0)

        buy_size_d = buy_size-sell_size
        sell_size_d = sell_size-buy_size
        size_abs = abs( sell_size-buy_size)

        #현재가의 1%
        yj1 = round(now_close *0.008,0)

        #청산가격 계산 현재가의 0.15% 
        buy_j3 = round(now_close *0.002,0)

        # #투입간격
        # qty_1 = 0
        # qty_2=1.00
        # qty_3=2.35

        # # qty_4=4.05
        # qty_4=4

        # qty_5=6.10
        # qty_6=8.50
        # qty_7=11.25
        # qty_8=14.35

        # # qty_9=17.80
        # qty_9=18

        # qty_10=21.60
        # qty_11=25.75
        # qty_12=30.25
        # qty_13=35.10

        # # qty_14=40.30
        # qty_14=40

        # qty_15=45.85
        # qty_16=51.75
        # qty_17=58.00
        # qty_18=64.60

        # # qty_19=71.55
        # qty_19=71

        # qty_20=78.85
        # qty_21=86.50
        # qty_22=94.50
        # qty_23=102.85

        # # qty_24=111.55
        # qty_24=111

        # qty_25=120.60
        # qty_26=130.00
        # qty_27=139.75
        # qty_28=149.85

        # # qty_29=160.30
        # qty_29=160

        # qty_30=171.10
        # qty_31=182.25
        # qty_32=193.75
        # # qty_33=205.60
        # # qty_34=217.80

        

        # #투입수량
        # price_1=round(0.03*(now_qty20),2)
        # price_2=round(0.03*(now_qty20),2)
        # price_3=round(0.03*(now_qty20),2)
        # price_4=round(0.03*(now_qty20),2)
        # price_5=round(0.03*(now_qty20),2)
        # price_6=round(0.03*(now_qty20),2)
        # price_7=round(0.04*(now_qty20),2)
        # price_8=round(0.04*(now_qty20),2)
        # price_9=round(0.04*(now_qty20),2)
        # price_10=round(0.04*(now_qty20),2)
        # price_11=round(0.06*(now_qty20),2)
        # price_12=round(0.06*(now_qty20),2)
        # price_13=round(0.06*(now_qty20),2)
        # price_14=round(0.06*(now_qty20),2)
        # price_15=round(0.07*(now_qty20),2)
        # price_16=round(0.07*(now_qty20),2)
        # price_17=round(0.07*(now_qty20),2)
        # price_18=round(0.07*(now_qty20),2)
        # price_19=round(0.09*(now_qty20),2)
        # price_20=round(0.09*(now_qty20),2)
        # price_21=round(0.13*(now_qty20),2)
        # price_22=round(0.13*(now_qty20),2)
        # price_23=round(0.19*(now_qty20),2)
        # price_24=round(0.19*(now_qty20),2)
        # price_25=round(0.28*(now_qty20),2)
        # price_26=round(0.28*(now_qty20),2)
        # price_27=round(0.42*(now_qty20),2)
        # price_28=round(0.42*(now_qty20),2)
        # price_29=round(0.61*(now_qty20),2)
        # price_30=round(0.79*(now_qty20),2)
        # price_31=round(1.03*(now_qty20),2)
        # price_32=round(1.33*(now_qty20),2)
        # # price_33=round(1.74*(now_qty20),2)
        # # price_34=round(2.25*(now_qty20),2)


        

        qty_1= 0
        qty_2=round(0.0007168459*now_close,0)
        qty_3=round(0.0014336918*now_close,0)
        qty_4=round(0.0021505376*now_close,0)
        qty_5=round(0.0028673835*now_close,0)
        qty_6=round(0.0035842294*now_close,0)
        qty_7=round(0.0043010753*now_close,0)
        qty_8=round(0.0050179211*now_close,0)
        qty_9=round(0.005734767*now_close,0)
        qty_10=round(0.0064516129*now_close,0)
        qty_11=round(0.0078853047*now_close,0)
        qty_12=round(0.0093189964*now_close,0)
        qty_13=round(0.0107526882*now_close,0)
        qty_14=round(0.0121863799*now_close,0)
        qty_15=round(0.0136200717*now_close,0)
        qty_16=round(0.0150537634*now_close,0)
        qty_17=round(0.0164874552*now_close,0)
        qty_18=round(0.017921147*now_close,0)
        qty_19=round(0.0193548387*now_close,0)
        qty_20=round(0.0207885305*now_close,0)
        qty_21=round(0.0229390681*now_close,0)
        qty_22=round(0.0250896057*now_close,0)
        qty_23=round(0.0272401434*now_close,0)
        qty_24=round(0.029390681*now_close,0)
        qty_25=round(0.0315412186*now_close,0)
        qty_26=round(0.0336917563*now_close,0)
        qty_27=round(0.0358422939*now_close,0)
        qty_28=round(0.0379928315*now_close,0)
        qty_29=round(0.0401433692*now_close,0)
        qty_30=round(0.0422939068*now_close,0)
        qty_31=round(0.0451612903*now_close,0)
        qty_32=round(0.0516129032*now_close,0)
        qty_33=round(0.0616487455*now_close,0)
        qty_34=round(0.0752688172*now_close,0)


        price_1=round(0.03*(now_qty20),2)
        price_2=round(0.03*(now_qty20),2)
        price_3=round(0.03*(now_qty20),2)
        price_4=round(0.03*(now_qty20),2)
        price_5=round(0.03*(now_qty20),2)
        price_6=round(0.03*(now_qty20),2)
        price_7=round(0.03*(now_qty20),2)
        price_8=round(0.03*(now_qty20),2)
        price_9=round(0.03*(now_qty20),2)
        price_10=round(0.03*(now_qty20),2)
        price_11=round(0.04*(now_qty20),2)
        price_12=round(0.04*(now_qty20),2)
        price_13=round(0.04*(now_qty20),2)
        price_14=round(0.04*(now_qty20),2)
        price_15=round(0.04*(now_qty20),2)
        price_16=round(0.04*(now_qty20),2)
        price_17=round(0.05*(now_qty20),2)
        price_18=round(0.06*(now_qty20),2)
        price_19=round(0.13*(now_qty20),2)
        price_20=round(0.15*(now_qty20),2)
        price_21=round(0.2*(now_qty20),2)
        price_22=round(0.25*(now_qty20),2)
        price_23=round(0.33*(now_qty20),2)
        price_24=round(0.42*(now_qty20),2)
        price_25=round(0.55*(now_qty20),2)
        price_26=round(0.65*(now_qty20),2)
        price_27=round(0.82*(now_qty20),2)
        price_28=round(0.98*(now_qty20),2)
        price_29=round(1.25*(now_qty20),2)
        price_30=round(1.6*(now_qty20),2)
        price_31=round(2.07*(now_qty20),2)
        price_32=round(2.66*(now_qty20),2)
        price_33=round(3.44*(now_qty20),2)
        price_34=round(4.46*(now_qty20),2)







        if now_close <= average_5_20 and count_side != "Buy" and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31) : # 현재가가 볼린전 중단(20일이평선)을 하향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소


                   
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_1,price =bb_l-(qty_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_2,price =bb_l-(qty_2) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_3,price =bb_l-(qty_3) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_4,price =bb_l-(qty_4) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_5,price =bb_l-(qty_5) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_6,price =bb_l-(qty_6) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_7,price =bb_l-(qty_7) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_8,price =bb_l-(qty_8),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_9,price =bb_l-(qty_9),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_10,price =bb_l-(qty_10),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_11,price =bb_l-(qty_11),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_12,price =bb_l-(qty_12) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_13,price =bb_l-(qty_13) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_14,price =bb_l-(qty_14) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_15,price =bb_l-(qty_15) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_16,price =bb_l-(qty_16) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_17,price =bb_l-(qty_17) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_18,price =bb_l-(qty_18) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_19,price =bb_l-(qty_19) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_20,price =bb_l-(qty_20),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_21,price =bb_l-(qty_21),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_22,price =bb_l-(qty_22) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_23,price =bb_l-(qty_23) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_24,price =bb_l-(qty_24) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_25,price =bb_l-(qty_25) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_26,price =bb_l-(qty_26) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_27,price =bb_l-(qty_27) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_28,price =bb_l-(qty_28) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_29,price =bb_l-(qty_29) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_30,price =bb_l-(qty_30) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_31,price =bb_l-(qty_31) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_32,price =bb_l-(qty_32) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_33,price =bb_l-(qty_33) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=price_34,price =bb_l-(qty_34) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
           
        else:
            pass
        
        if now_close > average_5_20 and count_side != "Sell" and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31) : # 현재가가 볼린전 중단(20일이평선)을 상향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

         
           
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_1,price =bb_u+(qty_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_2,price =bb_u+(qty_2) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_3,price =bb_u+(qty_3) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_4,price =bb_u+(qty_4) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_5,price =bb_u+(qty_5) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_6,price =bb_u+(qty_6) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_7,price =bb_u+(qty_7) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_8,price =bb_u+(qty_8),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_9,price =bb_u+(qty_9),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_10,price =bb_u+(qty_10),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_11,price =bb_u+(qty_11),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_12,price =bb_u+(qty_12) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_13,price =bb_u+(qty_13) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_14,price =bb_u+(qty_14) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_15,price =bb_u+(qty_15) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_16,price =bb_u+(qty_16) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_17,price =bb_u+(qty_17) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_18,price =bb_u+(qty_18) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_19,price =bb_u+(qty_19) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_20,price =bb_u+(qty_20),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_21,price =bb_u+(qty_21),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_22,price =bb_u+(qty_22) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_23,price =bb_u+(qty_23) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_24,price =bb_u+(qty_24) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_25,price =bb_u+(qty_25) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_26,price =bb_u+(qty_26) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_27,price =bb_u+(qty_27) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_28,price =bb_u+(qty_28) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_29,price =bb_u+(qty_29) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_30,price =bb_u+(qty_30) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_31,price =bb_u+(qty_31) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_32,price =bb_u+(qty_32) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_33,price =bb_u+(qty_33) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=price_34,price =bb_u+(qty_34) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            
            
            
            
           

            
        else:
            pass

        #볼린저 1%이탈시 초당 0.01이더 매수

        # if bb_l-yj1 > now_close :
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.01,price =now_close+1 ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        # else:
        #     pass
        # if bb_u+yj1 < now_close :
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.01,price =now_close-1 ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        # else:
        #     pass
      




        #지정가 청산주문
        if buy_size != 0:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass
        if sell_size != 0:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_entry_price-buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass

        # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_entry_price-buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
    


       
        
        print(buy_size)
        print(sell_size)
        print(buy_entry_price)
        print(sell_entry_price)
        # print(buy_geb)
        # print(sell_geb)
        # print(gty_d)
        # print(gty_c)
        # print(my_usdt)
        # print(now_close)
        print(time_s)
        # print(close_all_3)
        # print(close_b_1)
        # print(close_s_1)
        # print(my_query)
        print(buy_j3)
        # print(now_close)
        # print(a)
        # print(a_1)
        print("실행중")

    except HTTPError as erro:
        print(erro)
    except ZeroDivisionError as erro1:
        print(erro1)
    except ValueError as erro3:
        print(erro3)
    except IndexError as erro4:
        print(erro4)
    except NameError as erro5:
        print(erro5)
    except KeyError as erro6:
        print(erro6)
    except TypeError as erro7:
        print(erro7)
    except Exception as erro2: 
        print(erro2)
    pass

        
    time.sleep(1)