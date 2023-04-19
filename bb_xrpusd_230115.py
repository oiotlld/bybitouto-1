from types import new_class
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


client = bybit.bybit(test=False, api_key="5d0T7NvHkIVts3JK8m", api_secret="KDO3t4Vz9xfQZ14v9aduwEgT4FmasJUHRbW9")
apiKey='5d0T7NvHkIVts3JK8m'
apisecret='KDO3t4Vz9xfQZ14v9aduwEgT4FmasJUHRbW9'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="5d0T7NvHkIVts3JK8m",
    api_secret="KDO3t4Vz9xfQZ14v9aduwEgT4FmasJUHRbW9")

le_2=3
le_3=3
le_4=3
price_s=0
   
while True:
    try:

        ticker="XRPUSD"
        ticker_1="XRP"
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

        bb_u_5=round(float(average20 + std*2),sosu)
        bb_l_5=round(float(average20 - std*2),sosu)
        

        #  5분초단위=300, 20개 가저오기, interval="5" =5분봉
        since_5 = unixtime - 300*20
        response_5=session.query_kline(symbol=ticker,interval="5",**{'from':since_5})['result']
        df_2 = pd.DataFrame(response_5)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_5 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_5_20 = float(round(average_5,sosu))

        bb_u=round(float(average_5_20 + std_1*2),sosu)
        bb_l=round(float(average_5_20 - std_1*2),sosu)

        # 60분초단위=3600, 20개 가저오기, interval="60" =60분봉
        since_60 = unixtime - 3600*20
        response_60=session.query_kline(symbol=ticker,interval="60",**{'from':since_60})['result']
        df_2 = pd.DataFrame(response_60)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_60 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_60_20 = float(round(average_60,sosu))

        bb_u_60=round(float(average_60_20 + std_1*(le_3)),sosu)
        bb_l_60=round(float(average_60_20 - std_1*(le_4)),sosu)

        
        # # # 내 포지션 정보가저오기
        my_infor=session.my_position(symbol=ticker)
        print(my_infor)        
        
        # 내포지션 가저오기 양매수안됨 
        size = int(my_infor["result"]["size"])
        side = my_infor["result"]["side"]
        entry_price = float(my_infor["result"]["entry_price"])
        leverage = int(my_infor["result"]["leverage"])
        # print(entry_price)
        # 내자산가저오기
        myxrp=session.get_wallet_balance(coin=ticker_1)
        my_equity= float(myxrp["result"][ticker_1]['equity'])
        print(my_equity)

        # 현재가가저오기
        now_close=session.orderbook(symbol=ticker)
        now_close_1=float(now_close["result"][1]["price"])
        # 자산/현재가
        if (my_equity*now_close_1) < 20000:
            my_qty=(my_equity*now_close_1)
        elif (my_equity*now_close_1) >= 20000:
            my_qty=20000

        if 50 >= leverage >45:
            le_1 = 50
        elif 45 >= leverage > 40:
            le_1 = 45
        elif 40 >= leverage > 35:
            le_1 = 40
        elif 35 >= leverage > 30:
            le_1 = 35
        elif 30 >= leverage > 25:
            le_1 = 30
        elif leverage < 30:
            le_1 = 25
        else:
            pass

        qty_40=my_qty/(65-le_1)


        le_2 = round((le_1-leverage),1)

        if le_2 == 1:
            le_3= 2.5
            le_4= 3
        elif le_2 == 2:
            le_3= 3
            le_4= 2.5
        elif le_2 == 3:
            le_3= 2.5
            le_4= 2.5
        elif le_2 == 4:
            le_3= 3
            le_4= 3
        else:
            le_3= 3
            le_4= 3
            



        # 주문내역 받아보기
        my_data_1=session.get_active_order(symbol=ticker,order_status="New")
        my_data_2=my_data_1["result"]["data"]
        my_date_len=len(my_data_2)#주문수량 
        my_date_4=[]
        for g in range(0, my_date_len):
            my_data_3=int(my_data_1["result"]["data"][g]["leaves_qty"])
            my_date_4.append(0)

        
        if entry_price == 0:
            en_p = now_close_1
        else:
            en_p = entry_price
        
        # 주문하기
        if time_m ==0 and (time_s ==0 or time_s ==1 or time_s ==2 ) and my_date_len != 0  and leverage !=50:
            print(session.cancel_all_active_orders(symbol=ticker))
        else:
            pass
        # 공매수
        if my_date_len == 0  and size == 0 and bb_l_60 >= now_close_1 and size<my_qty*5 and en_p >= now_close_1 and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1-(0.0001)),4),qty=qty_40,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9971)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9942)),4),qty=qty_40*1.44,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9912)),4),qty=qty_40*1.73,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9882)),4),qty=qty_40*2.07,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9853)),4),qty=qty_40*2.49,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9823)),4),qty=qty_40*2.99,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9774)),4),qty=qty_40*3.58,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9725)),4),qty=qty_40*4.30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9676)),4),qty=qty_40*5.16,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9627)),4),qty=qty_40*6.19,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9578)),4),qty=qty_40*7.43,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9589)),4),qty=qty_40*8.92,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9482)),4),qty=qty_40*10.70,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9436)),4),qty=qty_40*12.84,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9389)),4),qty=qty_40*15.41,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9533)),4),qty=qty_40*18.49,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9504)),4),qty=qty_40*22.19,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9475)),4),qty=qty_40*26.62,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9446)),4),qty=qty_40*31.95,time_in_force="GoodTillCancel"))
        
        elif my_date_len == 0 and size > 0 and now_close_1 < bb_l_60+(bb_l_60*0.01) and side=="Buy" and size<my_qty*5  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1-(now_close_1*0.01)),4),qty=size*0.3,time_in_force="GoodTillCancel"))


        else:
            pass    

        # 공매도
        if my_date_len == 0 and size == 0  and round((bb_u_60*(1)),4) <= now_close_1  and size<my_qty*6 and en_p <= now_close_1  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1-(0.0000)),4),qty=qty_40,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0029)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0058)),4),qty=qty_40*1.44,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0088)),4),qty=qty_40*1.73,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0117)),4),qty=qty_40*2.07,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0147)),4),qty=qty_40*2.49,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0177)),4),qty=qty_40*2.99,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0226)),4),qty=qty_40*3.58,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0275)),4),qty=qty_40*4.30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0324)),4),qty=qty_40*5.16,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0373)),4),qty=qty_40*6.19,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0422)),4),qty=qty_40*7.43,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0471)),4),qty=qty_40*8.92,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0518)),4),qty=qty_40*10.70,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0564)),4),qty=qty_40*12.84,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0611)),4),qty=qty_40*15.41,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0467)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0496)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0525)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
            # print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0554)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
        
        elif my_date_len == 0 and size > 0 and now_close_1 > bb_u_60-(bb_u_60*0.01) and side=="Sell" and size<my_qty*6  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1+(now_close_1*0.01)),4),qty=size*0.3,time_in_force="GoodTillCancel"))


        else:
            pass    


        # 청산하기
        if side=="Sell" and entry_price*0.99 > now_close_1 and size <= my_qty*1  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.992 > now_close_1  and my_qty*1 < size <= my_qty*2  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*1,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.994 > now_close_1  and my_qty*2 < size <= my_qty*3  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*2,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.995 > now_close_1  and my_qty*3 < size <= my_qty*4  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*3,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.996 > now_close_1  and my_qty*4 < size <= my_qty*5  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*4,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.997 > now_close_1  and my_qty*5 < size  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*5,0),time_in_force="GoodTillCancel"))
        

        elif side=="Buy" and entry_price*1.01 < now_close_1 and size <= my_qty*1  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size,time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.007 < now_close_1  and my_qty*1 < size <= my_qty*2  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*1,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.006 < now_close_1  and my_qty*2 < size <= my_qty*3  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*2,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.005 < now_close_1  and my_qty*3 < size <= my_qty*4  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*3,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.004 < now_close_1  and my_qty*4 < size <= my_qty*5  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*4,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.003 < now_close_1  and my_qty*5 < size  and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*5,0),time_in_force="GoodTillCancel"))

        else:
            pass


        print(bb_l_60,"볼린저하단(3)")
        print(size,"size")
        print(side,"side")
        print(my_date_len,"주문수량")
        print(my_qty,"총자산")
        print(qty_40,"초기투입액")
        print(65-le_1,"투입배율")
        print(leverage,"레버리지")
        print(le_2,"레버리지번호")
        print(le_3,"공매도편차")
        print(le_4,"공매수편차")
        # =============================================================btc펀딩비 전략=========================================================
        ticker_p="ETHUSD"
        ticker_p_1="ETH"

        # 분봉가저오기
        # 60분초단위=3600, 20개 가저오기, interval="60" =60분봉
        since_60 = unixtime - 3600*20
        response_60_eth=session.query_kline(symbol=ticker_p,interval="60",**{'from':since_60})['result']
        df_2_eth = pd.DataFrame(response_60_eth)
        df_3_eth = df_2_eth['close'].astype(float)#문자열 숫자열로변환

        average_60_eth = numpy.mean(df_3_eth)
        std_1=numpy.std(df_3_eth)
        average_60_20_eth = float(round(average_60_eth,sosu))

        bb_u_60_eth=round(float(average_60_20_eth + std_1*3),sosu)
        bb_l_60_eth=round(float(average_60_20_eth - std_1*3),sosu)


        # # #각 포지션 평균단가 가저오기
        # # # 내 포지션 정보가저오기
        my_infor_btc=session.my_position(symbol=ticker_p)
        # print(my_infor_btc)      
        leverage_btc = int(my_infor_btc["result"]["leverage"])  
        
        # 내포지션 가저오기 양매수안됨 
        size_btc = int(my_infor_btc["result"]["size"])
        position_value = int(my_infor_btc["result"]["position_value"])
        side_btc = my_infor_btc["result"]["side"]
        entry_price_btc = float(my_infor_btc["result"]["entry_price"])
        # print(entry_price)
        # 내자산가저오기
        myxrp_btc=session.get_wallet_balance(coin=ticker_p_1)
        my_equity_btc= float(myxrp_btc["result"][ticker_p_1]['equity'])
        

        # 현재가가저오기
        now_close_btc=session.orderbook(symbol=ticker_p)
        now_close_1_btc=float(now_close_btc["result"][1]["price"])
        # 자산/현재가
        my_qty_1_btc=round(my_equity_btc*now_close_1_btc,0)
        qty_40_eth=my_qty_1_btc/100

        # 주문내역 받아보기
        my_data_1_btc=session.get_active_order(symbol=ticker_p,order_status="New")
        my_data_2_btc=my_data_1_btc["result"]["data"]
        my_date_len_btc=len(my_data_2_btc)#주문수량 
        my_date_4_btc=[]
        for g in range(0, my_date_len_btc):
            my_data_3=int(my_data_1_btc["result"]["data"][g]["leaves_qty"])
            my_date_4_btc.append(0)

        
        if entry_price_btc == 0:
            en_p_btc = now_close_1_btc
        else:
            en_p_btc = entry_price_btc
        
        
        if 50 >= leverage_btc >40:
            le_btc = 40
        elif 40 >= leverage_btc > 30:
            le_btc = 30
        elif 30 >= leverage_btc > 20:
            le_btc = 20
        elif 20 >= leverage_btc > 10:
            le_btc = 10
        elif 10 >= leverage_btc > 1:
            le_btc = 0
        else:
            pass

        le_8=leverage_btc-le_btc
        
       
        # 공매도 - 보유btc가 보유 공매도의 가격보다 5usd차이 보다 크면 그차익만큼 공매도를 해라 = 레버리지1배 유지 펀팅피 재투자
        if my_equity_btc > price_s and round(my_equity_btc - price_s,0) > round(price_s*0.003,0) and bb_u_60_eth < now_close_1_btc and size_btc != 0 and my_qty_1_btc > size_btc  and leverage_btc !=50:
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Market",price=round((now_close_1_btc+(0.0002)),2),qty=round(my_qty_1_btc - size_btc ,0),time_in_force="GoodTillCancel"))
            price_s=round(my_equity_btc,0)
        else:
            pass



        if round(price_s*1.01,0) < round(my_equity_btc,0) and average_60_20_eth > now_close_1_btc and size_btc != 0 and my_qty_1_btc < size_btc  and leverage_btc !=50:
            print(session.place_active_order(symbol=ticker_p,side="Buy",order_type="Market",price=round((now_close_1_btc+(0.0002)),2),qty=round(size_btc - my_qty_1_btc,0),time_in_force="GoodTillCancel"))
            price_s=round(my_equity_btc,0)

        elif round(price_s*1.05,0) < round(my_equity_btc,0) and size_btc != 0 and my_qty_1_btc < size_btc  and leverage_btc !=50:
            print(session.place_active_order(symbol=ticker_p,side="Buy",order_type="Market",price=round((now_close_1_btc+(0.0002)),2),qty=round(size_btc - my_qty_1_btc,0),time_in_force="GoodTillCancel"))
            price_s=round(my_equity_btc,0)
        else:
            pass


        # 공매도
        if time_m ==0 and (time_s ==0 or time_s ==1 or time_s ==2 ) and leverage_btc !=50:
            print(session.cancel_all_active_orders(symbol=ticker_p))
        else:
            pass
        if bb_u_60_eth < now_close_1_btc  and size_btc < my_qty_1_btc*le_8  and size_btc != 0 and leverage_btc !=50:
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.000)),4),qty=qty_40_eth,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.005)),4),qty=qty_40_eth*1.2,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.010)),4),qty=qty_40_eth*1.69,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.015)),4),qty=qty_40_eth*2.22,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.020)),4),qty=qty_40_eth*2.86,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.025)),4),qty=qty_40_eth*3.71,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.030)),4),qty=qty_40_eth*4.83,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.035)),4),qty=qty_40_eth*6.27,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.040)),4),qty=qty_40_eth*8.16,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.045)),4),qty=qty_40_eth*10.6,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.050)),4),qty=qty_40_eth*13.79,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.055)),4),qty=qty_40_eth*17.92,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.060)),4),qty=qty_40_eth*23.30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.065)),4),qty=qty_40_eth*30.29,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker_p,side="Sell",order_type="Limit",price=round((now_close_1_btc*(1.070)),4),qty=qty_40_eth*39.37,time_in_force="GoodTillCancel"))

        # =============================================================btc펀딩비 전략=========================================================

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