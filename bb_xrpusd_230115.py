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
price_s=2290 #총자본USD= 추가로자본투입할때 계산해서 그시점의 나의 원금을 넣어줘야함(다시돌릴때)
now_close_9 = 0.4479 #기준자산의 현재가
   
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

        # 240분초단위=14400, 20개 가저오기, interval="240" =240분봉
        since_240 = unixtime - 14400*20
        response_240=session.query_kline(symbol=ticker,interval="240",**{'from':since_240})['result']
        df_2 = pd.DataFrame(response_240)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_240 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_240_20 = float(round(average_240,sosu))

        bb_u_240=round(float(average_240_20 + std_1*2),sosu)
        bb_l_240=round(float(average_240_20 - std_1*2),sosu)

        print(bb_u_240, "240분봉")   
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
        my_equity= float(myxrp["result"][ticker_1]['equity']) #총자본XRP
        print(my_equity ,'총자본XRP' )

        # 현재가가저오기
        now_close=session.orderbook(symbol=ticker)
        now_close_1=float(now_close["result"][1]["price"])
        
        # 자산/현재가(usd)
        my_qty=round((my_equity*now_close_1),0)
        

        if 50 >= leverage >45: # 1/10
            le_1 = 50
        elif 45 >= leverage > 40: # 1/15
            le_1 = 45
        elif 40 >= leverage > 35: # 1/20
            le_1 = 40
        elif 35 >= leverage > 30: # 1/25
            le_1 = 35
        elif 30 >= leverage > 25: # 1/30
            le_1 = 30
        elif leverage < 30: # 1/35
            le_1 = 25
        else:
            pass

        qty_40=my_qty/(60-le_1)


        le_2 = round((le_1-leverage),1)

        if le_2 == 1: #49,44,39,34
            le_3= 2.5
            le_4= 3
        elif le_2 == 2: #48,43,38,33
            le_3= 3
            le_4= 2.5
        elif le_2 == 3: #47,42,37,32
            le_3= 2.5
            le_4= 2.5
        elif le_2 == 4: #46,41,36,31
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
        
        #레버리지 40으로 설정시 나의 자본원금을 계산(청산의 기준이되는 가격)
        if leverage == 40:
            price_s=round(my_equity*now_close_9,0) #총자산USD 저장, 저장시 추가투입액을반영햇을때도수익구간의 기준금액을 계산하기위해 now_close_9적용(추가투입액넣어도됨)
            
        else:
            pass

        


        # 주문취소하기(1시간마다 주문리셋)
        if time_m ==0 and (time_s ==0 or time_s ==1 or time_s ==2 ) and my_date_len != 0  and leverage !=50 and leverage !=40:
            print(session.cancel_all_active_orders(symbol=ticker))
        else:
            pass
        #주문하기
        # 공매수
        if my_date_len == 0  and size == 0 and bb_l_60 >= now_close_1 and size<my_qty*5 and en_p >= now_close_1 and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1-(0.0001)),4),qty=qty_40,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.997)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.993)),4),qty=qty_40*1.44,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.988)),4),qty=qty_40*1.73,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.982)),4),qty=qty_40*2.07,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.975)),4),qty=qty_40*2.49,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.967)),4),qty=qty_40*2.99,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.958)),4),qty=qty_40*3.58,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.948)),4),qty=qty_40*4.30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.937)),4),qty=qty_40*5.16,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.925)),4),qty=qty_40*6.19,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.912)),4),qty=qty_40*7.43,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.898)),4),qty=qty_40*8.92,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.884)),4),qty=qty_40*10.70,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.870)),4),qty=qty_40*12.84,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.856)),4),qty=qty_40*15.34,time_in_force="GoodTillCancel"))
               
        elif my_date_len == 0 and size > 0 and now_close_1 < bb_l_60+(bb_l_60*0.01) and side=="Buy" and size<my_qty*5  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1-(now_close_1*0.01)),4),qty=size*0.3,time_in_force="GoodTillCancel"))


        else:
            pass

        #공매수청산
        if side=="Buy" and entry_price*1.01 < now_close_1 and size <= my_qty*1  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size,time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.007 < now_close_1  and my_qty*1 < size <= my_qty*2  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*1,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.006 < now_close_1  and my_qty*2 < size <= my_qty*3  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*2,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.005 < now_close_1  and my_qty*3 < size <= my_qty*4  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*3,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.004 < now_close_1  and my_qty*4 < size <= my_qty*5  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*4,0),time_in_force="GoodTillCancel"))
        elif side=="Buy" and entry_price*1.003 < now_close_1  and my_qty*5 < size  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=round(size-my_qty*5,0),time_in_force="GoodTillCancel"))

        else:
            pass

        # 공매도
        if my_date_len == 0 and side=="Sell" and size < my_qty  and round((bb_u_60*(1)),4) <= now_close_1  and size<my_qty*5 and en_p <= now_close_1  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1-(0.0000)),4),qty=qty_40,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.003)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.007)),4),qty=qty_40*1.44,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.012)),4),qty=qty_40*1.73,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.018)),4),qty=qty_40*2.07,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.025)),4),qty=qty_40*2.49,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.033)),4),qty=qty_40*2.99,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.042)),4),qty=qty_40*3.58,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.052)),4),qty=qty_40*4.30,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.063)),4),qty=qty_40*5.16,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.075)),4),qty=qty_40*6.19,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.088)),4),qty=qty_40*7.43,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.102)),4),qty=qty_40*8.92,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.116)),4),qty=qty_40*10.70,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.130)),4),qty=qty_40*12.84,time_in_force="GoodTillCancel"))
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Limit",price=round((now_close_1*(1.144)),4),qty=qty_40*15.34,time_in_force="GoodTillCancel"))
        
        elif my_qty > size > my_qty*0.84 and side=="Sell" and bb_u_60 <= now_close_1 and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(0.0002)),2),qty=round(my_qty - size ,0),time_in_force="GoodTillCancel"))
            price_s=round(my_equity*now_close_1,0) #총자산USD 저장
            now_close_9 = now_close_1

        else:
            pass    


        # 청산하기(공매도 청산)
        if side=="Sell" and entry_price*0.95 > now_close_1 and bb_l_60*1.001 > now_close_1 and size <= my_qty  and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=now_close_1,qty=round(size,0),time_in_force="GoodTillCancel"))
        elif side=="Sell" and my_qty*2 > size > my_qty*1 and price_s*1.01 <= my_qty and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=now_close_1,qty=size-my_qty,time_in_force="GoodTillCancel"))
            price_s=round(my_equity*now_close_1,0) #총자산USD 저장
            now_close_9 = now_close_1
        elif side=="Sell" and my_qty*3 > size > my_qty*2 and price_s*1.007 <= my_qty and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=now_close_1,qty=(size-my_qty)-my_qty,time_in_force="GoodTillCancel"))
        elif side=="Sell" and my_qty*4 > size > my_qty*3 and price_s*1.005 <= my_qty and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=now_close_1,qty=(size-my_qty)-my_qty*2,time_in_force="GoodTillCancel"))
        elif side=="Sell" and my_qty*5 > size > my_qty*4 and price_s*1.004 <= my_qty and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=now_close_1,qty=(size-my_qty)-my_qty*3,time_in_force="GoodTillCancel"))
        elif side=="Sell" and size > my_qty*5 and price_s*1.003 <= my_qty and leverage !=50 and leverage !=40:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=now_close_1,qty=(size-my_qty)-my_qty*4,time_in_force="GoodTillCancel"))

        else:
            pass

        

        

        


        print(bb_l_60,"볼린저하단(3)")
        print(size,"size")
        print(side,"side")
        print(my_date_len,"주문수량")
        print(qty_40,"초기투입액")
        print(60-le_1,"투입배율")
        print(leverage,"레버리지")
        print(le_2,"레버리지번호")
        print(le_3,"공매도편차")
        print(le_4,"공매수편차")
        print(price_s,"기준금액")
        print(price_s*1.01,"기준금액1%수익시")
        print(my_qty,"총자산")
       

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