import bybit
import pandas as pd 
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
from urllib.request import urlopen
from urllib.error import HTTPError

client = bybit.bybit(test=False, api_key="KiJb87bD3cl4X4bnM9", api_secret="xfg0sAko83iPfMUNVdXeAYY862bU827v34cY")
apiKey='KiJb87bD3cl4X4bnM9'
apisecret='xfg0sAko83iPfMUNVdXeAYY862bU827v34cY'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="KiJb87bD3cl4X4bnM9",
    api_secret="xfg0sAko83iPfMUNVdXeAYY862bU827v34cY")

   
num=1

while True:
    try:

        ticker="DOGEUSDT"
        
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
        average20 = float(round(average,4))

        bb_u=round(float(average20 + std*2),4)
        bb_l=round(float(average20 - std*2),4)

        # 5분초단위=300, 20개 가저오기, interval="5" =5분봉
        since_5 = unixtime - 300*20
        response_5=session.query_kline(symbol=ticker,interval="5",**{'from':since_5})['result']
        df_2 = pd.DataFrame(response_5)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_5 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_5_20 = float(round(average_5,4))

        bb_u_5=round(float(average_5_20 + std_1*2),4)
        bb_l_5=round(float(average_5_20 - std_1*2),4)


        # 내 포지션 정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()

        buy_size = float(my_infor[0]["result"][0]["size"])
        sell_size = float(my_infor[0]["result"][1]["size"])

        # 각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),4)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),4)


        # 각 포지션 청산가격
        buy_liq_price=round(float(my_infor[0]["result"][0]["liq_price"]),4)
        sell_liq_price=round(float(my_infor[0]["result"][1]["liq_price"]),4)            
        
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

        # query_1 = float(my_query[0]["result"][0]["reduce_only"])   #첫주문이(마지막에들어간주문) 청산주문인지 확인 청산주문이면 1 아니면 0
        # query_2 = float(my_query[0]["result"][-1]["reduce_only"])   #마지막주문(첫번째로 들어간주문)청산주문인지 확인 청산주문이면 1 아니면 0
        # query_3 = my_query[0]["result"][0]["side"]                 #buy인지 sell 인지 확인
        
        
        # if re_len >= 1 :
        #     query_1 = float(my_query[0]["result"][0]["reduce_only"])
        # else:
        #     query_1 = 3
        # if query_1 == 1 :
        #     query_3 = [my_query[0]["result"][0]["order_id"],my_query[0]["result"][0]["side"]]
        # else:
        #     query_3 = 0

        # if re_len >= 2 :
        #     query_2 = float(my_query[0]["result"][1]["reduce_only"])
        # else:
        #     query_2 = 3
        # if query_2 == 1 :
        #     query_4 = [my_query[0]["result"][1]["order_id"],my_query[0]["result"][1]["side"]]
        # else:
        #     query_4 = 0



        # if re_len >= 3 :
        #     query_5 = float(my_query[0]["result"][2]["reduce_only"])
        # else:
        #     query_5 = 3
        # if query_5 == 1 :
        #     query_6 = [my_query[0]["result"][2]["order_id"],my_query[0]["result"][2]["side"]]
        # else:
        #     query_6 = 0

        # if re_len >= 4 :
        #     query_7 = float(my_query[0]["result"][3]["reduce_only"])
        # else:
        #     query_7 = 3
        # if query_7 == 1 :
        #     query_8 = [my_query[0]["result"][3]["order_id"],my_query[0]["result"][3]["side"]]
        # else:
        #     query_8 = 0

        # if re_len >= 5 :
        #     query_9 = float(my_query[0]["result"][4]["reduce_only"])
        # else:
        #     query_9 = 3
        # if query_9 == 1 :
        #     query_10 = [my_query[0]["result"][4]["order_id"],my_query[0]["result"][4]["side"]]
        # else:
        #     query_10 = 0

        # if re_len >= 6 :
        #     query_11 = float(my_query[0]["result"][5]["reduce_only"])
        # else:
        #     query_11 = 3
        # if query_11 == 1 :
        #     query_12 = [my_query[0]["result"][5]["order_id"],my_query[0]["result"][5]["side"]]
        # else:
        #     query_12 = 0

        

        
        # 자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))


        # 현재가조회(USDT)
        now_close_1 = client.LinearKline.LinearKline_get(symbol=ticker, interval="1", **{'from':unixtime-120}).result()
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),4)

        now_open_1 = round(float(now_close_1[0]["result"][-1]["open"]),4) #전봉의 시가
        now_open = round(float(now_close_1[0]["result"][-2]["open"]),4) #전봉의 시가
        now_low = round(float(now_close_1[0]["result"][-2]["low"]),4)   #전봉의 저가
        now_high = round(float(now_close_1[0]["result"][-2]["high"]),4) #전봉의 고가
        h_close = round(float(now_close_1[0]["result"][-2]["close"]),4) #전봉의 종가

        # 전봉의 볼리저상하단 이격 차이
        bb_low = round(bb_l - now_low,4)
        bb_high = round(now_high - bb_u,4)

        # 평단과 현재가의 차이
        if buy_entry_price != 0:
            buy_geb =abs(round((buy_entry_price-now_close)/buy_entry_price,4))
        else:
            buy_geb = 0
        if sell_entry_price !=0:
            sell_geb = abs(round((sell_entry_price-now_close)/sell_entry_price,4))
        else:
            sell_geb = 0
       

        # 매수 현재가
        # 현재가가 볼린저 상하단에 있을때 매수매도신호가 들어가면 볼린저 상단부터 현재가까지 시장가로 채결되는것을 방지하기위해 현재가가 볼린저상하단이탈한상태에서는 현재가를 기준으로 매수매도 주문을 넣는다
        if bb_l > now_close:
            a = now_close
        else:
            a = bb_l

        # 매도 현재가
        if bb_u < now_close:
            a_1 = now_close
        else:
            a_1 = bb_u


        # 볼린저 상하단 격차
        bb_cc = round((bb_u-bb_l)/bb_u,4)
       
        # print(bb_u)
        # print(bb_l)
        # 매수매도주문 Buy 첫글자"B"는 대문자여야함


        # 진입가격 결정, 
        # 공매수 주문 비율조정
        if 500 > my_usdt:
            now_qty20 = 0 
        elif 500 < my_usdt < 10000:
            now_qty20 = (10000/now_close)/100000
        elif 10000 < my_usdt:
            now_qty20 = (10000/now_close)/100000
        else:
            pass
        
        # 공매도 주문 비율조정
        if 500 > my_usdt:
            now_qty20_1 = 0 
        elif 500 < my_usdt < 10000:
            now_qty20_1 = (10000/now_close)/100000
        elif 10000 < my_usdt:
            now_qty20_1 = (10000/now_close)/100000
        else:
            pass
       

        # 위험수량 결정 자본금의 7배 이상      
        gty_d = round((my_usdt/now_close)*3,0)

        # 기본 수량 계산 - 반대포지션이 이수량되면 두배매수
        gty_c = round((my_usdt/now_close)*3,0)

        buy_size_d = buy_size-sell_size
        sell_size_d = sell_size-buy_size
        size_abs = abs( sell_size-buy_size)

        # 양매수시 청산주문 계산
        # 수익율 계산 close_sb_3:수익율

        if buy_size < sell_size and buy_size != 0 and sell_size != 0:
            close_all_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*buy_size #수익금액 계산식
            close_all_2 = (buy_entry_price*buy_size) + (sell_entry_price*buy_size)#투입금액 계산식
            close_all_3 = close_all_1 / close_all_2 #수익률 계산식
            close_b_1 = buy_size
            close_s_1 = buy_size
        
        elif buy_size >= sell_size and buy_size != 0 and sell_size != 0:
            close_all_1 = (now_close - buy_entry_price)*sell_size +  ( sell_entry_price - now_close)*sell_size
            close_all_2 = (buy_entry_price*sell_size) + (sell_entry_price*sell_size)
            close_all_3 = close_all_1 / close_all_2 #수익률 계산식
            close_b_1 = sell_size
            close_s_1 = sell_size

        else:
            close_all_3=0
            close_b_1 = 0
            close_s_1 = 0
        
        # 평단의 격차가벌어젓을때 손실없이 수량을 털기위해 많은쪽 포지션의 수량을 절반만 적용한 수익을 구해 수익구간에서 청산
        
        ccc=1
        if round((buy_size/ccc),3) < sell_size:
            c1 = round((buy_size/ccc),3)
        elif round((buy_size/ccc),3) >= sell_size:
            c1 = sell_size
        else:
            c1=0

        if round((sell_size/ccc),3) < buy_size:
            c2 = round((sell_size/ccc),3)
        elif round((sell_size/ccc),3) >= buy_size:
            c2 = sell_size
        else:
            c2=0
    
        if buy_size < sell_size and buy_size != 0 and sell_size != 0 :
            close_haf_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*c1
            close_haf_2 = (buy_entry_price*buy_size) + (sell_entry_price*c1)
            close_haf_3 = close_haf_1 / close_haf_2 #수익률 계산식
            close_b = buy_size
            close_s = c1
        
        elif buy_size >= sell_size and buy_size != 0 and sell_size != 0:
            close_haf_1 = (now_close - buy_entry_price)*c2 +  (sell_entry_price - now_close)*sell_size
            close_haf_2 = (buy_entry_price*c2) + (sell_entry_price*sell_size)
            close_haf_3 = close_haf_1 / close_haf_2 #수익률 계산식
            close_b = c2
            close_s = sell_size

        else:
            close_haf_3=0
            close_b = 0
            close_s = 0        
        #청산하기 2~3틱먹기
                       
        if buy_entry_price != 0 and buy_entry_price < now_close and buy_entry_price+0.0008 > now_close:
            buy_j=round(now_close+0.0003,4)
        elif buy_entry_price != 0 and buy_entry_price+0.0008 <= now_close:
            buy_j=round(now_close+0.0002,4)
        else:
            buy_j=round(buy_entry_price+0.0003,4)
        
        if sell_entry_price != 0 and sell_entry_price > now_close and sell_entry_price-0.0008 < now_close:
            sell_j=round(now_close-0.0003,4)
        elif sell_entry_price != 0 and sell_entry_price-0.0008 >= now_close :
            sell_j=round(now_close-0.0002,4)
        else:
            sell_j=round(sell_entry_price-0.0003,4)
        
        

        #매도 3분할매도
        sell_size_4 = round(sell_size_d/4,0)
        buy_size_4 = round(buy_size_d/4,0)

        if now_close <= average_5_20 and count_side != "Buy" and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31): # 현재가가 볼린전 중단(20일이평선)을 하향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소


        
            
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(50*(now_qty20),0),price =a-(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(50*(now_qty20),0),price =a-(0.0001) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(100*(now_qty20),0),price =a-(0.0002) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(100*(now_qty20),0),price =a-(0.0003) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(150*(now_qty20),0),price =a-(0.0004) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(150*(now_qty20),0),price =a-(0.0005) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(200*(now_qty20),0),price =a-(0.0006) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(200*(now_qty20),0),price =a-(0.0007) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(400*(now_qty20),0),price =a-(0.0008) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(400*(now_qty20),0),price =a-(0.0009) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(400*(now_qty20),0),price =a-(0.0011) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(500*(now_qty20),0),price =a-(0.0013) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(500*(now_qty20),0),price =a-(0.0015) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(600*(now_qty20),0),price =a-(0.0017) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(600*(now_qty20),0),price =a-(0.0019) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(700*(now_qty20),0),price =a-(0.0021) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(700*(now_qty20),0),price =a-(0.0023) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(800*(now_qty20),0),price =a-(0.0025) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(800*(now_qty20),0),price =a-(0.0027) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(1500*(now_qty20),0),price =a-(0.0029) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(1500*(now_qty20),0),price =a-(0.0032) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(2000*(now_qty20),0),price =a-(0.0035) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(2000*(now_qty20),0),price =a-(0.0038) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(2000*(now_qty20),0),price =a-(0.0041) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(3000*(now_qty20),0),price =a-(0.0044) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(4000*(now_qty20),0),price =a-(0.0047) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(5000*(now_qty20),0),price =a-(0.0050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(5000*(now_qty20),0),price =a-(0.0053) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(6000*(now_qty20),0),price =a-(0.0056) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(7000*(now_qty20),0),price =a-(0.0059) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(12000*(now_qty20),0),price =a-(0.0063) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(15000*(now_qty20),0),price =a-(0.0072) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(20000*(now_qty20),0),price =a-(0.0086) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(25000*(now_qty20),0),price =a-(0.0105) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(31000*(now_qty20),0),price =a-(0.0129) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(43000*(now_qty20),0),price =a-(0.0155) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832,price =a-(0.0192) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832,price =a-(0.0231) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832,price =a-(0.0275) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())


            #청산주문
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_entry_price-0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
           

           
        else:
            pass
        
        if now_close > average_5_20 and count_side != "Sell"  and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31): # 현재가가 볼린전 중단(20일이평선)을 상향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

         
           
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(50*(now_qty20_1),0),price =a_1+(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(50*(now_qty20_1),0),price =a_1+(0.0001) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(100*(now_qty20_1),0),price =a_1+(0.0002) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(100*(now_qty20_1),0),price =a_1+(0.0003) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(150*(now_qty20_1),0),price =a_1+(0.0004) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(150*(now_qty20_1),0),price =a_1+(0.0005) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(200*(now_qty20_1),0),price =a_1+(0.0006) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(200*(now_qty20_1),0),price =a_1+(0.0007) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(400*(now_qty20_1),0),price =a_1+(0.0008) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(400*(now_qty20_1),0),price =a_1+(0.0009) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(400*(now_qty20_1),0),price =a_1+(0.0011) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(500*(now_qty20_1),0),price =a_1+(0.0013) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(500*(now_qty20_1),0),price =a_1+(0.0015) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(600*(now_qty20_1),0),price =a_1+(0.0017) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(600*(now_qty20_1),0),price =a_1+(0.0019) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(700*(now_qty20_1),0),price =a_1+(0.0021) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(700*(now_qty20_1),0),price =a_1+(0.0023) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(800*(now_qty20_1),0),price =a_1+(0.0025) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(800*(now_qty20_1),0),price =a_1+(0.0027) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(1500*(now_qty20_1),0),price =a_1+(0.0029) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(1500*(now_qty20_1),0),price =a_1+(0.0032) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(2000*(now_qty20_1),0),price =a_1+(0.0035) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(2000*(now_qty20_1),0),price =a_1+(0.0038) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(2000*(now_qty20_1),0),price =a_1+(0.0041) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(3000*(now_qty20_1),0),price =a_1+(0.0044) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(4000*(now_qty20_1),0),price =a_1+(0.0047) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(5000*(now_qty20_1),0),price =a_1+(0.0050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(5000*(now_qty20_1),0),price =a_1+(0.0053) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(6000*(now_qty20_1),0),price =a_1+(0.0056) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(7000*(now_qty20_1),0),price =a_1+(0.0059) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(12000*(now_qty20_1),0),price =a_1+(0.0063) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(15000*(now_qty20_1),0),price =a_1+(0.0072) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(20000*(now_qty20_1),0),price =a_1+(0.0086) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(25000*(now_qty20_1),0),price =a_1+(0.0105) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(31000*(now_qty20_1),0),price =a_1+(0.0129) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(43000*(now_qty20_1),0),price =a_1+(0.0155) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832,price =a_1+(0.0192) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832,price =a_1+(0.0231) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832,price =a_1+(0.0275) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

            # 청산주문
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_entry_price-0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
           

            
        else:
            pass

        

        ########################################################################################################################

        # if re_len==0 and buy_size >= gty_d  : # 공매수 매수수량이 레버1배이상 일때 주문이 없으면 공매수주문을넣는다
            


        
            
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=2*(now_qty20),price =a-(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=2*(now_qty20),price =a-(0.0001) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=4*(now_qty20),price =a-(0.0002) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=4*(now_qty20),price =a-(0.0003) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=8*(now_qty20),price =a-(0.0004) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=8*(now_qty20),price =a-(0.0005) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=16*(now_qty20),price =a-(0.0006) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=16*(now_qty20),price =a-(0.0007),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=32*(now_qty20),price =a-(0.0008),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=32*(now_qty20),price =a-(0.0009),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=64*(now_qty20),price =a-(0.0011),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=64*(now_qty20),price =a-(0.0013) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=128*(now_qty20),price =a-(0.0015) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=128*(now_qty20),price =a-(0.0017) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=256*(now_qty20),price =a-(0.0019) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=256*(now_qty20),price =a-(0.0021) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=512*(now_qty20),price =a-(0.0023) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=512*(now_qty20),price =a-(0.0025) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=768*(now_qty20),price =a-(0.0027) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=768*(now_qty20),price =a-(0.0029),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=1152*(now_qty20),price =a-(0.0032),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=1152*(now_qty20),price =a-(0.0035) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=1728*(now_qty20),price =a-(0.0038) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=1728*(now_qty20),price =a-(0.0041) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=2592*(now_qty20),price =a-(0.0044) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=2592*(now_qty20),price =a-(0.0047) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=3888*(now_qty20),price =a-(0.0050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=3888*(now_qty20),price =a-(0.0053) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0056) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0059) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0063) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0072) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0086) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0105) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0129) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0158) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0192) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0231) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a-(0.0275) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())


        #     #청산주문
        #     # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        
        #     # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_entry_price-0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
           

           
        # else:
        #     pass
        
        # if re_len==0 and sell_size >= gty_d  :  # 공매도 매수수량이 레버1배이상 일때 주문이 없으면 공매도주문을넣는다
            

         
           
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=2*(now_qty20),price =a_1+(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=2*(now_qty20),price =a_1+(0.0001) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=4*(now_qty20),price =a_1+(0.0002) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=4*(now_qty20),price =a_1+(0.0003) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=8*(now_qty20),price =a_1+(0.0004) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=8*(now_qty20),price =a_1+(0.0005) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=16*(now_qty20),price =a_1+(0.0006) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=16*(now_qty20),price =a_1+(0.0007),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=32*(now_qty20),price =a_1+(0.0008),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=32*(now_qty20),price =a_1+(0.0009),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=64*(now_qty20),price =a_1+(0.0011),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=64*(now_qty20),price =a_1+(0.0013) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=128*(now_qty20),price =a_1+(0.0015) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=128*(now_qty20),price =a_1+(0.0017) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=256*(now_qty20),price =a_1+(0.0019) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=256*(now_qty20),price =a_1+(0.0021) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=512*(now_qty20),price =a_1+(0.0023) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=512*(now_qty20),price =a_1+(0.0025) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=768*(now_qty20),price =a_1+(0.0027) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=768*(now_qty20),price =a_1+(0.0029),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=1152*(now_qty20),price =a_1+(0.0032),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=1152*(now_qty20),price =a_1+(0.0035) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=1728*(now_qty20),price =a_1+(0.0038) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=1728*(now_qty20),price =a_1+(0.0041) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=2592*(now_qty20),price =a_1+(0.0044) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=2592*(now_qty20),price =a_1+(0.0047) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=3888*(now_qty20),price =a_1+(0.0050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=3888*(now_qty20),price =a_1+(0.0053) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0056) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0059) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0063) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0072) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0086) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0105) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0129) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0158) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0192) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0231) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        #     # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=5832*(now_qty20),price =a_1+(0.0275) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

        #     #청산주문
        #     # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        
        #     # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_entry_price-0.0003,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
           

            
        # else:
        #     pass

        ########################################################################################################################





        # 지정가 청산주문
        if (time_s == 2 or time_s==10 or time_s==20 or time_s==30 or time_s==40 or time_s==50)  :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size_4,price = buy_entry_price+0.0005,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size_4,price = sell_entry_price-0.0005,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass
    


        
        # 시장가 청산하기 5틱 수익이나면 청산
        if now_close >= buy_entry_price+0.0002 and 0 < buy_size > gty_d:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=round(buy_size/2,0) ,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass
        
        if now_close <= sell_entry_price-0.0002 and 0 < sell_size >gty_d:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=round(sell_size/2,0) ,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass
        
        if now_close >= buy_entry_price+0.0008 and 0 < buy_size <= gty_d:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=buy_size ,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass
        
        if now_close <= sell_entry_price-0.0008 and 0 < sell_size <= gty_d:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=sell_size,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass

        # 볼린저를 이탈하면 수익율을 적당히 낮은수준에서 청산한다
        # if now_close >= buy_entry_price+0.0004 and 0 < buy_size <= gty_d and bb_u >= now_close:
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=buy_size ,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass
        
        # if now_close <= sell_entry_price-0.0004 and 0 < sell_size <= gty_d and bb_l <= now_close:
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=sell_size,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass
        
        #  #양매수 시장가 청산하기    
        # if close_all_3 >= 0.003 and buy_size <= gty_c and sell_size <= gty_c  :
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=close_b_1,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=close_s_1,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass
        # if close_all_3 >= 0.001 and buy_size > gty_c or sell_size > gty_c  :
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=close_b_1,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=close_s_1,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass

       
        
        # print(buy_size)
        # print(sell_size)
        # print(buy_entry_price)
        # print(sell_entry_price)
        # print(buy_geb)
        # print(sell_geb)
        print(gty_d)
        print(now)
        # print(gty_c)
        # print(my_usdt)
        # print(now_close)
        # print(time_s)
        # print(close_all_3)
        # print(close_b_1)
        # print(close_s_1)
        # print(my_query)
        # print(query_1)
        # print(now_close)
        # print(average20)
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