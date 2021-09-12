import bybit
import pandas as pd 
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
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
        
        # 분봉가저오기
        now = datetime.utcnow()
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

        # 내주문정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()

        buy_size = float(my_infor[0]["result"][0]["size"])
        sell_size = float(my_infor[0]["result"][1]["size"])

        #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),4)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),4)

        #각 포지션 청산가격
        buy_liq_price=round(float(my_infor[0]["result"][0]["liq_price"]),4)
        sell_liq_price=round(float(my_infor[0]["result"][1]["liq_price"]),4)            
        
       

        
        # #자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))


        #현재가조회(USDT)
        now_close = client.LinearKline.LinearKline_get(symbol=ticker, interval="w", **{'from':1581231260}).result()
        now_close = round(float(now_close[0]["result"][-1]["close"]),4)

        

        # 진입가격 결정, 
        
        if 300 > my_usdt:
            now_qty20 = 1 
        elif 300 < my_usdt:
            now_qty20 = round((my_usdt*now_close)/50,0)
        else:
            pass

               
                
        # 모든주문취소
        print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result())

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

    
       
        # print(bb_u)
        # print(bb_l)
        #매수매도주문 Buy 첫글자"B"는 대문자여야함
        if bb_l < now_close < bb_u:
            qty_l=[2,4,8,16,32,64,128,128,128,128,128,256]
            price_l=[0,0.0001,0.0002,0.0004,0.0006,0.0008,0.001,0.0014,0.0018,0.0022,0.0026,0.0041]

            for z, x in zip(qty_l, price_l):
                if now_close <= average20:
                    print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                elif now_close >= average20:
                    print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                else:
                    pass
        elif bb_l >= now_close or now_close >= bb_u:
            qty_l=[2,4,8,16,32,64,128,128,128,128,128,256,256,512,512,1024,1024]
            price_l=[0,0.0001,0.0002,0.0004,0.0006,0.0008,0.001,0.0014,0.0018,0.0022,0.0026,0.0041,0.0051,0.0069,0.0081,0.0102,0.0116]

            for z, x in zip(qty_l, price_l):
                if now_close <= average20:
                    print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a-x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                elif now_close >= average20:
                    print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=now_qty20*z,price =a_1+x ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                else:
                    pass
        else:
                    pass
       
            

              
         #청산하기 2~3틱먹기
        if buy_entry_price < now_close:
            buy_j=round(now_close+0.0002,4)
        else:
            buy_j=round(buy_entry_price+0.0003,4)
        
        if sell_entry_price > now_close:
            sell_j=round(now_close-0.0002,4)
        else:
            sell_j=round(sell_entry_price-0.0003,4)
                
        
                    
        if buy_size != 0 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size,price = buy_j ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass
        
   
        if sell_size != 0 :
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size,price = sell_j ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass

        
        
        print(buy_size)
        print(sell_size)
        print(buy_entry_price)
        print(sell_entry_price)
        print(buy_j)
        print(sell_j)
        print(now_close)
        print(a)
        print(a_1)
        print(now_qty20)
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

        
    time.sleep(30)

