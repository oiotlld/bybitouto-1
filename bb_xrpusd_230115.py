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

        bb_u_60=round(float(average_60_20 + std_1*3),sosu)
        bb_l_60=round(float(average_60_20 - std_1*3),sosu)

        
        # # # 내 포지션 정보가저오기
        my_infor=session.my_position(symbol=ticker)
        print(my_infor)        
        
        # 내포지션 가저오기 양매수안됨 
        size = int(my_infor["result"]["size"])
        side = my_infor["result"]["side"]
        entry_price = float(my_infor["result"]["entry_price"])
        # print(entry_price)
        # 내자산가저오기
        myxrp=session.get_wallet_balance(coin=ticker_1)
        my_equity= float(myxrp["result"][ticker_1]['equity'])

        # 현재가가저오기
        now_close=session.orderbook(symbol=ticker)
        now_close_1=float(now_close["result"][1]["price"])
        # 자산/현재가
        my_qty=my_equity*now_close_1

        # 주문내역 받아보기
        my_data_1=session.get_active_order(symbol=ticker,order_status="New")
        my_data_2=my_data_1["result"]["data"]
        my_date_len=len(my_data_2)#주문수량 
        my_date_4=[]
        for g in range(0, my_date_len):
            my_data_3=int(my_data_1["result"]["data"][g]["leaves_qty"])
            my_date_4.append(0)
        
        # 주문하기
        if time_m ==0 and (time_s ==0 or time_s ==1):
            print(session.cancel_all_active_orders(symbol=ticker))
        else:
            pass
        # 공매수
        if my_date_len == 0 and size == 0 and bb_l_60 >= now_close_1 and size<my_qty*5:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1-(0.0002)),4),qty=my_qty/4,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9971)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9942)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9912)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9883)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9854)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9825)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9796)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9767)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9737)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9708)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9679)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9650)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9621)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9592)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9562)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9533)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9504)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9475)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.9446)),4),qty=my_qty/30,time_in_force="GoodTillCancel"))
        
        elif my_date_len == 0 and size > 0 and now_close_1 < bb_l_60+(bb_l_60*0.01) and side=="Buy" and size<my_qty*5:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1-(now_close_1*0.01)),4),qty=size*0.3,time_in_force="GoodTillCancel"))


        else:
            pass    

        # 공매도
        if my_date_len == 0  and size == 0 and bb_u_60 <= now_close_1  and size<my_qty*6 :
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1+(0.0002)),4),qty=my_qty/4,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0029)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0058)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0088)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0117)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0146)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0175)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0204)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0233)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0263)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0292)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0321)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0350)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0379)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0408)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0438)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0467)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0496)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0525)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.0554)),4),qty=my_qty/20,time_in_force="GoodTillCancel"))
        
        elif my_date_len == 0 and size > 0 and now_close_1 > bb_u_60-(bb_u_60*0.01) and side=="Sell" and size<my_qty*6:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1+(now_close_1*0.01)),4),qty=size*0.3,time_in_force="GoodTillCancel"))


        else:
            pass    


        # 청산하기
        if side=="Sell" and entry_price*0.99 > now_close_1 and size <= my_qty*1 :
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.995 > now_close_1  and my_qty*1 < size <= my_qty*2 :
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*1,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.997 > now_close_1  and my_qty*2 < size <= my_qty*5 :
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*2,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and entry_price*0.997 > now_close_1  and my_qty*5 < size :
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*2,0),time_in_force="GoodTillCancel"))
        

        elif side=="Buy" and entry_price*1.01 < now_close_1 and size <= my_qty*1 :
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size,time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.005 < now_close_1  and my_qty*1 < size <= my_qty*2 :
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*1,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.003 > now_close_1  and my_qty*2 < size <= my_qty*5 :
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*2,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.003 > now_close_1  and my_qty*5 < size :
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*2,0),time_in_force="GoodTillCancel"))

        else:
            pass


        print(bb_l_60,"볼린저하단(3)")
        print(size,"size")
        print(side,"side")
        print(my_date_len,"주문수량")
        print(my_qty,"총자산")
        
        # # #각 포지션 평균단가 가저오기
        # buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),sosu)
        # sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),sosu)

         
        #  # 내 활성주문 가저오기
        
        
        # print(bb_l_60-(bb_l_60*0.01))
        # print("실행중")


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