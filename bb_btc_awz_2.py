import bybit
import pandas as pd 
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
from urllib.request import urlopen
from urllib.error import HTTPError

client = bybit.bybit(test=False, api_key="FPkbvpdvFPvRXwrwZn", api_secret="RW96PrpqqOBok5wrDQZvUp2kVWvjGfYLkixQ")
apiKey='FPkbvpdvFPvRXwrwZn'
apisecret='RW96PrpqqOBok5wrDQZvUp2kVWvjGfYLkixQ'
session = HTTP(
    endpoint='https://api.bybit.com', 
    api_key="FPkbvpdvFPvRXwrwZn",
    api_secret="RW96PrpqqOBok5wrDQZvUp2kVWvjGfYLkixQ")

   
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
        
              

        if time_s == 0 or time_s==1 and (gty_d > buy_size and gty_d > sell_size): # 초단위 카운팅 0 = 1분,  공매수 공매도 둘중하나라도 위험수량에 도달하면 매수주문 안들어감
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

            if now_close < average20:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*0+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*1+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*2+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*3+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*4+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*5+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*6+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*7+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*8+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*9+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*10+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*11+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*12+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*13+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*14+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*15+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*16+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*17+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*18+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*19+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
               
            
            elif now_close > average20:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*0+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*1+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*2+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*3+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*4+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*5+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*6+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*7+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*8+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*9+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*10+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*11+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*12+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*13+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*14+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*15+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*16+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*17+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*18+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*19+1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            else:
                pass
        else:
            pass



        if time_s == 3 or time_s==4 and (gty_d > buy_size and gty_d > sell_size): # 초단위 카운팅 0 = 1분,  공매수 공매도 둘중하나라도 위험수량에 도달하면 매수주문 안들어감

            if now_close < average20:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*0+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*1+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*2+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*3+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*4+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*5+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*6+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*7+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*8+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*9+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*10+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*11+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*12+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*13+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*14+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*15+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*16+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*17+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*18+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30*19+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
               
            
            elif now_close > average20:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*0+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*1+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*2+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*3+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*4+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*5+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*6+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*7+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*8+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*9+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*10+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*11+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*12+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*13+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*14+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*15+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*16+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*17+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*18+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30*19+1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            else:
                pass

        
        else:
            pass


         #시장가 청산하기    
        
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Market",qty=buy_size,price = sell_entry_price*1.002,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Market",qty=sell_size,price = buy_entry_price*0.998,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    

       
                      
        
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