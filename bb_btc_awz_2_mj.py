import bybit
import pandas as pd 
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
from urllib.request import urlopen
from urllib.error import HTTPError

client = bybit.bybit(test=False, api_key="vd4durU82SHhr0qQ49", api_secret="t2064yhJfopfqXRVRYwV7mXT12jhYE5CrgAl")
apiKey='vd4durU82SHhr0qQ49'
apisecret='t2064yhJfopfqXRVRYwV7mXT12jhYE5CrgAl'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="vd4durU82SHhr0qQ49",
    api_secret="t2064yhJfopfqXRVRYwV7mXT12jhYE5CrgAl")

   
num=1

while True:
    try:

        ticker="BTCUSDT"

        #소주점 맞추기
        sosu=1
        
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

        

        # 내 포지션 정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()

        buy_size = float(my_infor[0]["result"][0]["size"])
        sell_size = float(my_infor[0]["result"][1]["size"])

        #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),sosu)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),sosu)


        #각 포지션 청산가격
        buy_liq_price=round(float(my_infor[0]["result"][0]["liq_price"]),sosu)
        sell_liq_price=round(float(my_infor[0]["result"][1]["liq_price"]),sosu)            
        
       
        

        
        # #자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))


        #현재가조회(USDT)
        now_close_1 = client.LinearKline.LinearKline_get(symbol=ticker, interval="1", **{'from':unixtime-120}).result()
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),sosu)

        now_low = round(float(now_close_1[0]["result"][-2]["low"]),sosu)
        now_high = round(float(now_close_1[0]["result"][-2]["high"]),sosu)

        
        

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
        bb_cc = round((bb_u-bb_l)/bb_u,sosu)
       
        # print(bb_u)
        # print(bb_l)
        #매수매도주문 Buy 첫글자"B"는 대문자여야함


        

        # 위험수량 결정 자본금의 10배 이상      
        gty_d = round((my_usdt/now_close)*10,0)

        # 기본 수량 계산 - 반대포지션이 이수량되면 두배매수
        # gty_c = round((my_usdt/now_close)*3,0)

        # buy_size_d = buy_size-sell_size
        # sell_size_d = sell_size-buy_size


        
         #현재가의 0.2% 수익
        jjjj=round(now_close*0.002,sosu)
                
        #자본금 대비 투입량 증가 기본자본금 5000USDT를 기준으로 투입자본금늘어나는 만큼 투입수량에 + 더해주는방법

        if my_usdt > 5000:
            rb=(round((my_usdt / 5000),)-1)*0.001
        elif my_usdt <= 5000:
            rb=0
        else:
            pass

        if time_s == 2 or time_s==3 and (gty_d > buy_size and gty_d > sell_size): # 초단위 카운팅 0 = 1분,  공매수 공매도 둘중하나라도 위험수량에 도달하면 매수주문 안들어감
            # print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

            if now_close < average20:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002+rb ,price =a-(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1260) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1320) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1380) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1440) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a-(1500) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004+rb ,price =a-(1560) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.006+rb ,price =a-(1620) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.009+rb ,price =a-(1680) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.013+rb ,price =a-(1740) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.018+rb ,price =a-(1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.024+rb ,price =a-(1870) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.031+rb ,price =a-(1940) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.039+rb ,price =a-(2010) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.048+rb ,price =a-(2080) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.058+rb ,price =a-(2150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.068+rb ,price =a-(2220) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.088+rb ,price =a-(2290) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.128+rb ,price =a-(2360) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.208+rb ,price =a-(2430) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                
               
            
            elif now_close > average20:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002+rb ,price =a_1+(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1260) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1320) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1380) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1440) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003+rb ,price =a_1+(1500) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004+rb ,price =a_1+(1560) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.006+rb ,price =a_1+(1620) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.009+rb ,price =a_1+(1680) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.013+rb ,price =a_1+(1740) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.018+rb ,price =a_1+(1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.024+rb ,price =a_1+(1870) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.031+rb ,price =a_1+(1940) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.039+rb ,price =a_1+(2010) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.048+rb ,price =a_1+(2080) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.058+rb ,price =a_1+(2150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.068+rb ,price =a_1+(2220) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.088+rb ,price =a_1+(2290) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.128+rb ,price =a_1+(2360) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.208+rb ,price =a_1+(2430) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                
            else:
                pass
        else:
            pass



        

        #  #시장가 청산하기    
        # if now_close >= buy_entry_price+jjjj:
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Market",qty=buy_size,price = buy_entry_price+jjjj,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass
        
        # if now_close <= sell_entry_price-jjjj:
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Market",qty=sell_size,price = sell_entry_price-jjjj,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass

                      
        
        print(buy_size)
        print(sell_size)
        print(buy_entry_price)
        print(sell_entry_price)
        print(now_close)
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