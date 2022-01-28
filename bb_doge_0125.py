
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


client = bybit.bybit(test=False, api_key="EAhsvXoYCBu6xNzQ3Z", api_secret="AHp8h2D3xIQfOSGEokLJxQxsMFPA1clF7xQI")
apiKey='EAhsvXoYCBu6xNzQ3Z'
apisecret='AHp8h2D3xIQfOSGEokLJxQxsMFPA1clF7xQI'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="EAhsvXoYCBu6xNzQ3Z",
    api_secret="AHp8h2D3xIQfOSGEokLJxQxsMFPA1clF7xQI")

   
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
        bb_cc = float(round((bb_u-bb_l)/bb_u,2))
       
        # print(bb_u)
        # print(bb_l)
        #매수매도주문 Buy 첫글자"B"는 대문자여야함


         # 진입가격 결정, 
        
        if 500 > my_usdt:
            now_qty20 = 0 
        elif 500 < my_usdt < 10000:
            now_qty20 = (my_usdt/now_close)/1000
        elif 10000 < my_usdt:
            now_qty20 = (my_usdt/now_close)/1000
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
        yj1 = float(round(now_close *0.008,sosu))

        #청산가격 계산 현재가의 0.15% 
        buy_j3 = float(round(now_close *0.003,sosu))

        #평단가격과 1.1%이격 가격
        buy_entry_1 =float(round(buy_entry_price -(buy_entry_price *0.011),sosu))
        sell_entry_1 = float(round(sell_entry_price+(sell_entry_price *0.011),sosu))


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
        e_39=round(2200*(now_qty20),4)

        p_1=0
        p_2=0.0007
        p_3=0.0013
        p_4=0.002
        p_5=0.0027
        p_6=0.0034
        p_7=0.0047
        p_8=0.0061
        p_9=0.0074
        p_10=0.0087
        p_11=0.0101
        p_12=0.0121
        p_13=0.0141
        p_14=0.0162
        p_15=0.0182
        p_16=0.0202
        p_17=0.0229
        p_18=0.0256
        p_19=0.0283
        p_20=0.031
        p_21=0.0336
        p_22=0.037
        p_23=0.0404
        p_24=0.0437
        p_25=0.0471
        p_26=0.0505
        p_27=0.0538
        p_28=0.0572
        p_29=0.0606
        p_30=0.0639
        p_31=0.068
        p_32=0.0727
        p_33=0.0781
        p_34=0.0841
        p_35=0.0908
        p_36=0.0983
        p_37=0.1063
        p_38=0.1151
        p_39=0.1306







       

    
        #주문하기    
        if now_close <= average_5_20-0.0004 and count_side != "Buy" and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31) : # 현재가가 볼린전 중단(20일이평선)을 하향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소


                   
            
            qty_l=[e_1,e_2,e_3,e_4,e_5,e_6,e_7,e_8,e_9,e_10,e_11,e_12,e_13,e_14,e_15,e_16,e_17,e_18,e_19,e_20,e_21,e_22,e_23,e_24,e_25,e_26,e_27,e_28,e_29,e_30,e_31,e_32,e_33,e_34,e_35,e_36,e_37,e_38,e_39]
            price_l=[p_1,p_2,p_3,p_4,p_5,p_6,p_7,p_8,p_9,p_10,p_11,p_12,p_13,p_14,p_15,p_16,p_17,p_18,p_19,p_20,p_21,p_22,p_23,p_24,p_25,p_26,p_27,p_28,p_29,p_30,p_31,p_32,p_33,p_34,p_35,p_36,p_37,p_38,p_39]
            for z, x in zip(qty_l, price_l):
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=z,price =round(bb_l-(x*now_close),4) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            
            
        else:
            pass
        
        if now_close > average_5_20+0.0004 and count_side != "Sell" and (time_s == 0 or time_s == 1 or time_s == 30 or time_s == 31) : # 현재가가 볼린전 중단(20일이평선)을 상향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

         
           
            
            qty_l=[e_1,e_2,e_3,e_4,e_5,e_6,e_7,e_8,e_9,e_10,e_11,e_12,e_13,e_14,e_15,e_16,e_17,e_18,e_19,e_20,e_21,e_22,e_23,e_24,e_25,e_26,e_27,e_28,e_29,e_30,e_31,e_32,e_33,e_34,e_35,e_36,e_37,e_38,e_39]
            price_l=[p_1,p_2,p_3,p_4,p_5,p_6,p_7,p_8,p_9,p_10,p_11,p_12,p_13,p_14,p_15,p_16,p_17,p_18,p_19,p_20,p_21,p_22,p_23,p_24,p_25,p_26,p_27,p_28,p_29,p_30,p_31,p_32,p_33,p_34,p_35,p_36,p_37,p_38,p_39]
            for z, x in zip(qty_l, price_l):
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=z,price =round(bb_u+(x*now_close),4) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            
            
        else:
            pass

       



        #지정가 청산주문
        if buy_size_d > 0:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_entry_price+buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass
        if sell_size_d > 0:
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
        if close_all_3 > 0.004 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=close_b_1,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass

        if close_all_3 > 0.004 :
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