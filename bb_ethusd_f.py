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
from collections import Counter
import math


client = bybit.bybit(test=False, api_key="EAhsvXoYCBu6xNzQ3Z", api_secret="AHp8h2D3xIQfOSGEokLJxQxsMFPA1clF7xQI")
apiKey='EAhsvXoYCBu6xNzQ3Z'
apisecret='AHp8h2D3xIQfOSGEokLJxQxsMFPA1clF7xQI'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="EAhsvXoYCBu6xNzQ3Z",
    api_secret="AHp8h2D3xIQfOSGEokLJxQxsMFPA1clF7xQI")


sell_close=0
sell_e=0
sell_e2=0
sell_size_2=0
price_limit=0
num=1

while True:
    try:

        ticker="ETHUSD"
        
        # 분봉가저오기
        now = datetime.utcnow()
        time_s = int(now.second) #초 카운트
        time_m = int(now.minute) #분 카운트
        unixtime = calendar.timegm(now.utctimetuple())
        # 1분초단위=60, 20개 가저오기, interval="1" =1분봉
        since = unixtime - 60*20
        response=session.query_kline(symbol=ticker,interval="1",**{'from':since})['result']
        df = pd.DataFrame(response)
        df_1=df['close'].astype(float)#문자열 숫자열로변환
        

        average = numpy.mean(df_1)
        std=numpy.std(df_1)
        average20 = float(round(average,2))

        bb_u=round(float(average20 + std*2),2)
        bb_l=round(float(average20 - std*2),2)

         # 1시간초단위=3600, 20개 가저오기, interval="60" =1시간
        since_60 = unixtime - 3600*20
        response_60=session.query_kline(symbol=ticker,interval="60",**{'from':since_60})['result']
        df_2 = pd.DataFrame(response_60)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_60 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_60_20 = float(round(average_60,2))

        bb_u_60=round(float(average_60_20 + std_1*2),2)
        bb_l_60=round(float(average_60_20 - std_1*2),2)

        

        # # 내 포지션 정보가저오기
        my_infor=client.Positions.Positions_myPosition(symbol=ticker).result()
        
        # buy_size = float(my_infor[1]["result"]["size"])
     
        sell_size = float(my_infor[0]["result"]["size"])
        # print(buy_size)
        # print(sell_size)
        

        # # #각 포지션 평균단가 가저오기
        # buy_entry_price = round(float(my_infor[0]["result"]["entry_price"]),0)
        sell_entry_price = round(float(my_infor[0]["result"]["entry_price"]),2)
        # print(sell_entry_price)

        

        
        
        # # # 내 활성주문 가저오기
        # my_query= client.Order.Order_getOrders(symbol=ticker,order_status="New").result()
        
        # # # 활성주문중 청산주문골라내기
        # count_1 = my_query[0]["result"]
        # re_len = len(count_1)

        # if re_len ==0:
        #     count_side = 0
        # else:
        #     count_side = count_1[-1]["side"]

        
        # print(count_side)
        # # print(re_len)

        
        # # #자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="ETH").result()
        my_eth = float((my_equity[0]["result"]["ETH"]["equity"]))
        
        


        # #현재가조회(USDT)
        now_close_1 = client.Kline.Kline_get(symbol=ticker, interval="1", **{'from':unixtime-60}).result()
        # print(now_close_1)
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),2)
        now_open = round(float(now_close_1[0]["result"][-1]["open"]),2)
        now_high = round(float(now_close_1[0]["result"][-1]["high"]),2)

        oh=(now_high-now_open)/now_open

        # print(now_close)
        # print(now_open)
        # print(now_high)


        #평단과 현재가의 이격비율
        if  sell_entry_price !=0 :
            sell_entry_1 = round((sell_entry_price -now_close)/now_close,4)

        else:
            sell_entry_1 =0
        
        #이더 usd 환산가격
        my_ethusd = round(my_eth * now_close,0)
        # print(my_ethusd)

        # #현재가의 1%
        yj1 = round(now_close *0.005,1)
        yj2 = round(now_close *0.0005,1)

        
        if time_s == 0:
            print(client.Order.Order_cancelAll(symbol=ticker).result())#모드주문취소
        

        #매수주문 넣기

        if now_close >= (bb_u_60+(yj1+yj1)) and time_s == 0 and my_ethusd*5 > sell_size and sell_entry_1 > 0:
            
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd,0) ,price =round(now_close + yj1,0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*1)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*2)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*3)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*4)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*5)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*6)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*7)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*8)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*9)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*10)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*11)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*12)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*13)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*14)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.1,0) ,price =round(now_close + (yj1+(yj2*15)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.2,0) ,price =round(now_close + (yj1+(yj2*16)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.2,0) ,price =round(now_close + (yj1+(yj2*17)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.2,0) ,price =round(now_close + (yj1+(yj2*18)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.2,0) ,price =round(now_close + (yj1+(yj2*19)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.2,0) ,price =round(now_close + (yj1+(yj2*20)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.2,0) ,price =round(now_close + (yj1+(yj2*21)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.2,0) ,price =round(now_close + (yj1+(yj2*22)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.3,0) ,price =round(now_close + (yj1+(yj2*23)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.4,0) ,price =round(now_close + (yj1+(yj2*24)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd*0.4,0) ,price =round(now_close + (yj1+(yj2*25)),0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            

        else:
            pass

        if  (my_ethusd-sell_size) > 0 and time_s == 0:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(my_ethusd-sell_size,0) ,price =round(now_close +0.1,0),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        else:
            pass

        if sell_size > my_ethusd:
            sell_size_d = sell_size - my_ethusd
        else:
            sell_size_d = 0
        
        #청산주문가 산정
        if now_close >= (bb_u_60+(yj1)) and oh > 0.005:
            price_limit=bb_u_60
        else:
            price_limit=0



        #지정가청산주문 
        if sell_size_d > 0 and time_s == 0 and price_limit != 0:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(sell_size_d,0),price = price_limit+yj1,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            
        else:
            pass
        
        print("현재초             :",time_s)
        print("현재가             :",now_close)
        print("볼린저상단         :",bb_u_60)
        print("보유이더량         :",my_eth)
        print("보유이더usd환산가격:",my_ethusd)
        print("보유수량          :",sell_size)
        print("1배초과보유수량    :",sell_size_d)
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