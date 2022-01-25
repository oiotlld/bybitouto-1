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

        ticker="DOGEUSDT"
        sosu=4
        
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
        average20 = float(round(average,sosu))

        bb_u=round(float(average20 + std*2),sosu)
        bb_l=round(float(average20 - std*2),sosu)

         # 5분초단위=300, 20개 가저오기, interval="5" =5분봉
        since_5 = unixtime - 300*20
        response_5=session.query_kline(symbol=ticker,interval="5",**{'from':since_5})['result']
        df_2 = pd.DataFrame(response_5)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_5 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_5_20 = float(round(average_5,sosu))

        bb_u_5=round(float(average_5_20 + std_1*2),sosu)
        bb_l_5=round(float(average_5_20 - std_1*2),sosu)


        # 내 포지션 정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()

        
        buy_size = float(my_infor[0]["result"][0]["size"])
        sell_size = float(my_infor[0]["result"][1]["size"])

        # #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),sosu)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),sosu)


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
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),sosu)

        


        #볼린저 상하단 격차
        bb_cc = round((bb_u-bb_l)/bb_u,2)
       
        # print(bb_u)
        # print(bb_l)
        #매수매도주문 Buy 첫글자"B"는 대문자여야함


         # 진입가격 결정, 
        
        if 500 > my_usdt:
            now_qty20 = 0 
        elif 500 < my_usdt < 10000:
            now_qty20 = (my_usdt/now_close)/3600
        elif 10000 < my_usdt:
            now_qty20 = (my_usdt/now_close)/3600
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
        yj1 = round(now_close *0.008,sosu)

        #청산가격 계산 현재가의 0.15% 
        buy_j3 = round(now_close *0.002,sosu)

        #평단가격과 1.1%이격 가격
        buy_entry_1 = round(buy_entry_price -(buy_entry_price *0.011),sosu)
        sell_entry_1 = round(sell_entry_price+(sell_entry_price *0.011),sosu)


        #구간별 주문수량계산
        e_1=round(1*(now_qty20),4)
        e_2=round(6*(now_qty20),4)
        e_3=round(11*(now_qty20),4)
        e_4=round(16*(now_qty20),4)
        e_5=round(21*(now_qty20),4)
        e_6=round(26*(now_qty20),4)
        e_7=round(31*(now_qty20),4)
        e_8=round(36*(now_qty20),4)
        e_9=round(41*(now_qty20),4)
        e_10=round(46*(now_qty20),4)
        e_11=round(51*(now_qty20),4)
        e_12=round(56*(now_qty20),4)
        e_13=round(61*(now_qty20),4)
        e_14=round(76*(now_qty20),4)
        e_15=round(91*(now_qty20),4)
        e_16=round(106*(now_qty20),4)
        e_17=round(121*(now_qty20),4)
        e_18=round(136*(now_qty20),4)
        e_19=round(151*(now_qty20),4)
        e_20=round(166*(now_qty20),4)
        e_21=round(181*(now_qty20),4)
        e_22=round(196*(now_qty20),4)
        e_23=round(211*(now_qty20),4)
        e_24=round(251*(now_qty20),4)
        e_25=round(291*(now_qty20),4)
        e_26=round(331*(now_qty20),4)
        e_27=round(371*(now_qty20),4)
        e_28=round(431*(now_qty20),4)
        e_29=round(491*(now_qty20),4)
        e_30=round(551*(now_qty20),4)
        e_31=round(611*(now_qty20),4)
        e_32=round(671*(now_qty20),4)
        e_33=round(751*(now_qty20),4)
        e_34=round(831*(now_qty20),4)
        e_35=round(911*(now_qty20),4)
        e_36=round(991*(now_qty20),4)
        e_37=round(1071*(now_qty20),4)
        e_38=round(1151*(now_qty20),4)




       

    
        #주문하기    
        if now_close <= average_5_20 and count_side != "Buy" and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31) : # 현재가가 볼린전 중단(20일이평선)을 하향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소


                   
            
            qty_l=[e_1,e_2,e_3,e_4,e_5,e_6,e_7,e_8,e_9,e_10,e_11,e_12,e_13,e_14,e_15,e_16,e_17,e_18,e_19,e_20,e_21,e_22,e_23,e_24,e_25,e_26,e_27,e_28,e_29,e_30,e_31,e_32,e_33,e_34,e_35,e_36,e_37,e_38]
            price_l=[0,0.0001,0.0002,0.0003,0.0004,0.0005,0.0007,0.0009,0.0011,0.0013,0.0015,0.0018,0.0021,0.0024,0.0027,0.003,0.0034,0.0038,0.0042,0.0046,0.005,0.0055,0.006,0.0065,0.007,0.0075,0.008,0.0085,0.009,0.0095,0.0101,0.0108,0.0116,0.0125,0.0135,0.0146,0.0158,0.0171
]
            for z, x in zip(qty_l, price_l):
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=z,price =bb_l-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            
            
        else:
            pass
        
        if now_close > average_5_20 and count_side != "Sell" and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31) : # 현재가가 볼린전 중단(20일이평선)을 상향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

         
           
            
            qty_l=[e_1,e_2,e_3,e_4,e_5,e_6,e_7,e_8,e_9,e_10,e_11,e_12,e_13,e_14,e_15,e_16,e_17,e_18,e_19,e_20,e_21,e_22,e_23,e_24,e_25,e_26,e_27,e_28,e_29,e_30,e_31,e_32,e_33,e_34,e_35,e_36,e_37,e_38]
            price_l=[0,0.0001,0.0002,0.0003,0.0004,0.0005,0.0007,0.0009,0.0011,0.0013,0.0015,0.0018,0.0021,0.0024,0.0027,0.003,0.0034,0.0038,0.0042,0.0046,0.005,0.0055,0.006,0.0065,0.007,0.0075,0.008,0.0085,0.009,0.0095,0.0101,0.0108,0.0116,0.0125,0.0135,0.0146,0.0158,0.0171]
            for z, x in zip(qty_l, price_l):
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=z,price =bb_u+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            
            
        else:
            pass

       



        #지정가 청산주문
        if buy_size > 0:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass
        if sell_size > 0:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_entry_price-buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass

        
         #양매수시 청산주문 계산
        #수익율 계산 close_sb_3:수익율

        if buy_size < sell_size and buy_size != 0 and sell_size != 0:
            close_all_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*buy_size #수익금액 계산식
            close_all_2 = (buy_entry_price*buy_size) + (sell_entry_price*buy_size)#투입금액 계산식
            close_all_3 = close_all_1 / close_all_2 #수익률 계산식
            close_b_1 = buy_size
            close_s_1 = buy_size
        
        elif buy_size >= sell_size and buy_size != 0 and sell_size != 0:
            close_all_1 = (now_close - buy_entry_price)*sell_size +  ( sell_entry_price - now_close)*sell_size
            close_all_2 = (buy_entry_price*sell_size) + (sell_entry_price*sell_size)
            close_all_3 = round(close_all_1 / close_all_2,3) #수익률 계산식
            close_b_1 = sell_size
            close_s_1 = sell_size

        else:
            close_all_3=0

         #양매수 시장가 청산하기    0.01= 1%수익
        if close_all_3 > 0.003 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=close_b_1,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass

        if close_all_3 > 0.003 :
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=close_s_1,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass    
        
        print(buy_size)
        print(sell_size)
        print(buy_entry_price)
        print(sell_entry_price)
        # print(buy_geb)
        # print(sell_geb)
        print(now_qty20)
        # print(gty_c)
        # print(my_usdt)
        # print(now_close)
        print(time_s)
        print(close_all_3)
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