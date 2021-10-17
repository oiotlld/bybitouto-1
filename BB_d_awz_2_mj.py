import bybit
import pandas as pd 
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
from urllib.request import urlopen
from urllib.error import HTTPError

client = bybit.bybit(test=False, api_key="lBJLenoK4dz8bqoBCH", api_secret="qsjRwMsqd1psIWxO9sotKyc8tC9q40NWEzIi")
apiKey='lBJLenoK4dz8bqoBCH'
apisecret='qsjRwMsqd1psIWxO9sotKyc8tC9q40NWEzIi'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="lBJLenoK4dz8bqoBCH",
    api_secret="qsjRwMsqd1psIWxO9sotKyc8tC9q40NWEzIi")

   
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

        

        # 내 포지션 정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()

        buy_size = float(my_infor[0]["result"][0]["size"])
        sell_size = float(my_infor[0]["result"][1]["size"])

        #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),4)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),4)


        #각 포지션 청산가격
        buy_liq_price=round(float(my_infor[0]["result"][0]["liq_price"]),4)
        sell_liq_price=round(float(my_infor[0]["result"][1]["liq_price"]),4)            
        
        # 내 활성주문 가저오기
        my_query= client.LinearOrder.LinearOrder_query(symbol=ticker).result()
        # # 활성주문중 청산주문골라내기
        re_len = len(my_query[0]["result"])
        if re_len >= 1 :
            query_1 = float(my_query[0]["result"][0]["reduce_only"])
        else:
            query_1 = 3
        if query_1 == 1 :
            query_3 = [my_query[0]["result"][0]["order_id"],my_query[0]["result"][0]["side"]]
        else:
            query_3 = 0

        if re_len >= 2 :
            query_2 = float(my_query[0]["result"][1]["reduce_only"])
        else:
            query_2 = 3
        if query_2 == 1 :
            query_4 = [my_query[0]["result"][1]["order_id"],my_query[0]["result"][1]["side"]]
        else:
            query_4 = 0



        if re_len >= 3 :
            query_5 = float(my_query[0]["result"][2]["reduce_only"])
        else:
            query_5 = 3
        if query_5 == 1 :
            query_6 = [my_query[0]["result"][2]["order_id"],my_query[0]["result"][2]["side"]]
        else:
            query_6 = 0

        if re_len >= 4 :
            query_7 = float(my_query[0]["result"][3]["reduce_only"])
        else:
            query_7 = 3
        if query_7 == 1 :
            query_8 = [my_query[0]["result"][3]["order_id"],my_query[0]["result"][3]["side"]]
        else:
            query_8 = 0

        if re_len >= 5 :
            query_9 = float(my_query[0]["result"][4]["reduce_only"])
        else:
            query_9 = 3
        if query_9 == 1 :
            query_10 = [my_query[0]["result"][4]["order_id"],my_query[0]["result"][4]["side"]]
        else:
            query_10 = 0

        if re_len >= 6 :
            query_11 = float(my_query[0]["result"][5]["reduce_only"])
        else:
            query_11 = 3
        if query_11 == 1 :
            query_12 = [my_query[0]["result"][5]["order_id"],my_query[0]["result"][5]["side"]]
        else:
            query_12 = 0

        

        
        # #자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))


        #현재가조회(USDT)
        now_close_1 = client.LinearKline.LinearKline_get(symbol=ticker, interval="1", **{'from':unixtime-120}).result()
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),4)

        now_low = round(float(now_close_1[0]["result"][-2]["low"]),4)
        now_high = round(float(now_close_1[0]["result"][-2]["high"]),4)

        #전봉의 볼리저상하단 이격 차이
        bb_low = round(bb_l - now_low,4)
        bb_high = round(now_high - bb_u,4)

        #평단과 현재가의 차이
        if buy_entry_price != 0:
            buy_geb =abs(round((buy_entry_price-now_close)/buy_entry_price,4))
        else:
            buy_geb = 0
        if sell_entry_price !=0:
            sell_geb = abs(round((sell_entry_price-now_close)/sell_entry_price,4))
        else:
            sell_geb = 0
       

        # # 매수 현재가
        # # 현재가가 볼린저 상하단에 있을때 매수매도신호가 들어가면 볼린저 상단부터 현재가까지 시장가로 채결되는것을 방지하기위해 현재가가 볼린저상하단이탈한상태에서는 현재가를 기준으로 매수매도 주문을 넣는다
        if bb_l > now_close:
            a = now_close
        else:
            a = bb_l

        #매도 현재가
        if bb_u < now_close:
            a_1 = now_close
        else:
            a_1 = bb_u


        #볼린저 상하단 격차
        bb_cc = round((bb_u-bb_l)/bb_u,4)
       
        # print(bb_u)
        # print(bb_l)
        #매수매도주문 Buy 첫글자"B"는 대문자여야함


         # 진입가격 결정, 
        
        if 300 > my_usdt:
            now_qty20 = 1 
        elif 300 < my_usdt and buy_geb < 0.03 and sell_geb < 0.03:
            now_qty20 = round((my_usdt*now_close)/80,0)
        elif 300 < my_usdt and (buy_geb > 0.03 or sell_geb > 0.03) :
            now_qty20 = round((my_usdt*now_close)/50,0)
        else:
            pass

        # 위험수량 결정 자본금의 5배 이상      
        gty_d = round((my_usdt/now_close)*5,0)

        # 기본 수량 계산
        gty_c = round((my_usdt/now_close)/10,0)

        buy_size_d = buy_size-sell_size
        sell_size_d = sell_size-buy_size
        
         #청산하기 2~3틱먹기
                       
        if buy_entry_price != 0 and buy_entry_price < now_close:
            buy_j=round(now_close+0.0002,4)
        else:
            buy_j=round(buy_entry_price+0.0003,4)
        
        if sell_entry_price != 0 and sell_entry_price > now_close:
            sell_j=round(now_close-0.0002,4)
        else:
            sell_j=round(sell_entry_price-0.0003,4)

        #매도 3분할매도
        sell_size_4 = round(sell_size/4,0)
        buy_size_4 = round(buy_size/4,0)

        

        if time_s == 0 or time_s==1: # 초단위 카운팅 0 = 1분
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

            if bb_l < now_close < bb_u:
                qty_l=[1,2,4,8,16,32,64,128,229,330,431,532,756]
                price_l=[-0.0001,0,0.0001,0.0002,0.0004,0.0006,0.0008,0.001,0.0014,0.0018,0.0022,0.0026,0.0041]

                for z, x in zip(qty_l, price_l):
                    if now_close <= average20 and buy_size < gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and sell_size < gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*2 > buy_size > gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+1),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*2 >sell_size > gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+1),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*4 > buy_size > gty_c*2:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+2),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*4 >sell_size > gty_c*2:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+2),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*8 > buy_size > gty_c*4:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+3),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*8 >sell_size > gty_c*4:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+3),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*16 > buy_size > gty_c*8:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+4),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*16 >sell_size > gty_c*8:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+4),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*32 > buy_size > gty_c*16:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+5),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*32 >sell_size > gty_c*16:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+5),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and  buy_size > gty_c*32:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+6),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and sell_size > gty_c*32:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+6),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

            elif bb_l >= now_close or now_close >= bb_u or bb_cc > 0.05 :
                qty_l=[1,2,4,8,16,32,64,128,229,330,431,532,756,1056,1356,1656,1956,2256]
                price_l=[-0.0001,0,0.0001,0.0002,0.0004,0.0006,0.0008,0.001,0.0014,0.0018,0.0022,0.0026,0.0041,0.0051,0.0069,0.0081,0.0102,0.0116]

                for z, x in zip(qty_l, price_l):
                    if now_close <= average20 and buy_size < gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and sell_size < gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*2 > buy_size > gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+1),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*2 >sell_size > gty_c:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+1),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*4 > buy_size > gty_c*2:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+2),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*4 >sell_size > gty_c*2:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+2),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*8 > buy_size > gty_c*4:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+3),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*8 >sell_size > gty_c*4:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+3),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*16 > buy_size > gty_c*8:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+4),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*16 >sell_size > gty_c*8:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+4),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and gty_c*32 > buy_size > gty_c*16:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+5),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and gty_c*32 >sell_size > gty_c*16:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+5),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass

                    if now_close <= average20 and  buy_size > gty_c*32:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*(z+6),price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    elif now_close >= average20 and sell_size > gty_c*32:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*(z+6),price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass
            else:
                pass
            
              
            #청산주문 
            
            if buy_size != 0 and buy_geb < 0.03 and buy_size < gty_d :
                pp=[0,0.0001,0.0002,0.0003]
                for m in pp:
                    print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size_4,price = buy_j+m ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                
            else:
                pass

            if sell_size != 0 and sell_geb < 0.03 and sell_size < gty_d:
                pp=[0,0.0001,0.0002,0.0003]
                for m in pp:
                    print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size_4,price = sell_j-m ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                
            else:
                pass
            #손절하기
            if (round(abs(0.0020/now_close),4) < buy_geb or round(abs(0.0042/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002,0.0021,0.0022,0.0023,0.0024,0.0025,0.0026,0.0027,0.0028,0.0029,0.003,0.0031,0.0032,0.0033,0.0034,0.0035,0.0036,0.0037,0.0038,0.0039,0.004]
            elif (round(abs(0.0020/now_close),4) < buy_geb or round(abs(0.0037/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002,0.0021,0.0022,0.0023,0.0024,0.0025,0.0026,0.0027,0.0028,0.0029,0.003,0.0031,0.0032,0.0033,0.0034,0.0035]
            elif (round(abs(0.0020/now_close),4) < buy_geb or round(abs(0.0032/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002,0.0021,0.0022,0.0023,0.0024,0.0025,0.0026,0.0027,0.0028,0.0029,0.003]
            elif (round(abs(0.0020/now_close),4) < buy_geb or round(abs(0.0027/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002,0.0021,0.0022,0.0023,0.0024,0.0025]
            elif (round(abs(0.0020/now_close),4) < buy_geb or round(abs(0.0022/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016,0.0017,0.0018,0.0019,0.002]
            elif (round(abs(0.0016/now_close),4) < buy_geb or round(abs(0.0018/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012,0.0013,0.0014,0.0015,0.0016]                
            elif (round(abs(0.0012/now_close),4) < buy_geb or round(abs(0.0014/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001,0.0011,0.0012] 
            elif (round(abs(0.0009/now_close),4) < buy_geb or round(abs(0.0009/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009]
            elif (round(abs(0.0005/now_close),4) < buy_geb or round(abs(0.0005/now_close),4) <sell_geb) and (sell_size_d > gty_d or buy_size_d >= gty_d):
                price_2=[0.0001,0.0002,0.0003,0.0004,0.0005]
            else:
                price_2=[-0.0003]
            if buy_size != 0 and buy_geb < 0.03 and buy_size_d >= gty_d:
                for n in price_2:
                    print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size/40,price = buy_entry_price - n ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            else:
                pass

            if sell_size != 0 and sell_geb < 0.03 and sell_size_d >= gty_d:
                for m in price_2:
                    print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size/40,price = sell_entry_price + m ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            else:
                pass

            #순환매 전봉이 현재볼린저가격의 이탈하면 볼린저 2틱에 익절주문을 건다,(매수평단과 무관하게 순환매하기위해 주문)
            if buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0116:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*3000,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

            elif buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0081:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*1800,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

            elif buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0069:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*1200,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

            elif buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0041:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*700,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0022:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*500,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0014:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*250,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0008:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*60,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif buy_size_d >= gty_d  and buy_geb > 0.03 and bb_low > 0.0004:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*15,price = bb_l+0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            
            else:
                pass



            if sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0116:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*3000,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

            elif sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0081:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*1800,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

            elif sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0069:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*1200,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

            elif sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0041:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*700,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0022:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*500,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0014:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*250,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0008:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*60,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            elif sell_size_d >= gty_d  and sell_geb > 0.03 and bb_high > 0.0004:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*15,price = bb_u-0.0002 ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

            
            else:
                pass
            
            
        else:
            pass

    
        #청산 주문 취소하기
        # if query_1 == 1:
        #     my_id1 = query_3[0]
        # else:
        #     my_id1 = 0

        # if query_2 == 1:
        #     my_id2 = query_4[0]
        # else:
        #     my_id2 = 0
        
        # if query_5 == 1:
        #     my_id3 = query_6[0]
        # else:
        #     my_id3 = 0

        # if query_7 == 1:
        #     my_id4 = query_8[0]
        # else:
        #     my_id4 = 0
        
        # if query_9 == 1:
        #     my_id5 = query_10[0]
        # else:
        #     my_id5 = 0
        
        # if query_11 == 1:
        #     my_id6 = query_12[0]
        # else:
        #     my_id6 = 0


            
        if (time_s == 12 or time_s == 22  or time_s == 32  or time_s == 42  or time_s == 52  ) and (buy_size < gty_d and sell_size < gty_d) and (buy_size != 0 or sell_size != 0) and buy_geb < 0.03: # 초단위 카운팅 0 = 1분
            
            #청산주문취소하기
            # if my_id1 != 0:
            #     print(client.LinearOrder.LinearOrder_cancel(symbol=ticker, order_id=my_id1).result())
            # else:
            #     pass
            # if my_id2 != 0:
            #     print(client.LinearOrder.LinearOrder_cancel(symbol=ticker, order_id=my_id2).result())
            # else:
            #     pass
            # if my_id3 != 0:
            #     print(client.LinearOrder.LinearOrder_cancel(symbol=ticker, order_id=my_id3).result())
            # else:
            #     pass
            # if my_id4 != 0:
            #     print(client.LinearOrder.LinearOrder_cancel(symbol=ticker, order_id=my_id4).result())
            # else:
            #     pass
            # if my_id5 != 0:
            #     print(client.LinearOrder.LinearOrder_cancel(symbol=ticker, order_id=my_id5).result())
            # else:
            #     pass
            # if my_id6 != 0:
            #     print(client.LinearOrder.LinearOrder_cancel(symbol=ticker, order_id=my_id6).result())
            # else:
            #     pass


            
            #청산하기 2~3틱먹기
            pp=[0,0.0001,0.0002,0.0003]
            for m in pp:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size/10,price = buy_j+m ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size/10,price = sell_j-m ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass

       
        
        print(buy_size)
        print(sell_size)
        print(buy_entry_price)
        print(sell_entry_price)
        print(now_close)
        print(buy_geb)
        print(sell_geb)
        print(gty_d)
        print(time_s)
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