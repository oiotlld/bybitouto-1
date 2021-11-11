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
        gty_d = round((my_usdt/now_close)*5,3)

        # 기본 수량 계산 - 반대포지션이 이수량되면 두배매수
        gty_c = round((my_usdt/now_close)*3.5,3)

        buy_size_d = buy_size-sell_size
        sell_size_d = sell_size-buy_size
        

        #현재가의 0.1%~0.3%분할 청산_지정가주문시
       
        buy_j3 = round(buy_entry_price*0.003,0)
        buy_j2 = round(buy_entry_price*0.002,0)
        buy_j1 = round(buy_entry_price*0.001,0)
        
        sell_j3 = round(sell_entry_price*0.003,0)
        sell_j2 = round(sell_entry_price*0.002,0)
        sell_j1 = round(sell_entry_price*0.001,0)

        #양매수시 청산주문 계산
        #수익율 계산 close_sb_3:수익율

        # if buy_size < sell_size and buy_size != 0 and sell_size != 0:
        #     close_all_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*buy_size #수익금액 계산식
        #     close_all_2 = (buy_entry_price*buy_size) + (sell_entry_price*buy_size)#투입금액 계산식
        #     close_all_3 = close_all_1 / close_all_2 #수익률 계산식
        #     close_b = buy_size
        #     close_s = buy_size
        
        # elif buy_size >= sell_size and buy_size != 0 and sell_size != 0:
        #     close_all_1 = (now_close - buy_entry_price)*sell_size +  ( sell_entry_price - now_close)*sell_size
        #     close_all_2 = (buy_entry_price*sell_size) + (sell_entry_price*sell_size)
        #     close_all_3 = round(close_all_1 / close_all_2,3) #수익률 계산식
        #     close_b = sell_size
        #     close_s = sell_size

        # else:
        #     close_all_3=0
        
        # # 평단의 격차가벌어젓을때 손실없이 수량을 털기위해 많은쪽 포지션의 수량을 절반만 적용한 수익을 구해 수익구간에서 청산
        
        ccc=0.8
        if round((buy_size/ccc),3) < sell_size:
            c1 = round((buy_size/ccc),3)
        elif round((buy_size/ccc),3) >= sell_size:
            c1 = sell_size
        else:
            c1=0

        if round((sell_size/ccc),3) < buy_size:
            c2 = round((sell_size/ccc),3)
        elif round((sell_size/ccc),3) >= buy_size:
            c2 = sell_size
        else:
            c2=0
    
        if buy_size < sell_size and buy_size != 0 and sell_size != 0 :
            close_haf_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*c1
            close_haf_2 = (buy_entry_price*buy_size) + (sell_entry_price*c1)
            close_haf_3 = round(close_haf_1 / close_haf_2,3) #수익률 계산식
            close_b = buy_size
            close_s = c1
        
        elif buy_size >= sell_size and buy_size != 0 and sell_size != 0:
            close_haf_1 = (now_close - buy_entry_price)*c2 +  (sell_entry_price - now_close)*sell_size
            close_haf_2 = (buy_entry_price*c2) + (sell_entry_price*sell_size)
            close_haf_3 = round(close_haf_1 / close_haf_2,3) #수익률 계산식
            close_b = c2
            close_s = sell_size

        else:
            close_haf_3=0
    


        #자본금 대비 투입량 증가 기본자본금 5000USDT를 기준으로 투입자본금늘어나는 만큼 투입수량에 + 더해주는방법

        # if my_usdt > 5000:
        #     rb=(round((my_usdt / 5000),)-1)*0.001
        # elif my_usdt <= 5000:
        #     rb=0
        # else:
        #     pass
              

        if time_s == 0 or time_s==1 : # 초단위 카운팅 0 = 1분,  공매수 공매도 둘중하나라도 위험수량에 도달하면 매수주문 안들어감
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

        
            if now_close < average20 and sell_size_d < 0.1 and buy_size < gty_d:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.001 ,price =a-(10) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.001 ,price =a-(50) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004 ,price =a-(250) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004 ,price =a-(300) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.006 ,price =a-(350) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.009 ,price =a-(400) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.020 ,price =a-(450) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.050 ,price =a-(500) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.100 ,price =a-(700) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.150 ,price =a-(850) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.400 ,price =a-(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.043 ,price =a-(700) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.046 ,price =a-(750) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.049 ,price =a-(800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.052 ,price =a-(850) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.055 ,price =a-(900) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.058 ,price =a-(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.061 ,price =a-(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.064 ,price =a-(1050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.067 ,price =a-(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.070 ,price =a-(1150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.073 ,price =a-(1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.100 ,price =a-(2000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())


            elif now_close > average20 and buy_size_d < 0.1 and sell_size < gty_d:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.001 ,price =a_1+(10) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.001 ,price =a_1+(50) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004 ,price =a_1+(250) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004 ,price =a_1+(300) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.006 ,price =a_1+(350) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.009 ,price =a_1+(400) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.020 ,price =a_1+(450) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.050 ,price =a_1+(500) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.100 ,price =a_1+(700) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.150 ,price =a_1+(850) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.400 ,price =a_1+(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.043 ,price =a_1+(700) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.046 ,price =a_1+(750) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.049 ,price =a_1+(800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.052 ,price =a_1+(850) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.055 ,price =a_1+(900) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.058 ,price =a_1+(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.061 ,price =a_1+(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.064 ,price =a_1+(1050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.067 ,price =a_1+(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.070 ,price =a_1+(1150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.073 ,price =a_1+(1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.100 ,price =a_1+(2000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

            else:
                pass


            if now_close < average20 and sell_size_d >= 0.1  and buy_size < gty_d:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(10) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(30) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003 ,price =a-(60) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003 ,price =a-(100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.003 ,price =a-(150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004 ,price =a-(210) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004 ,price =a-(270) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004 ,price =a-(330) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004 ,price =a-(390) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.005 ,price =a-(450) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.005 ,price =a-(510) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.005 ,price =a-(570) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.005 ,price =a-(630) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.043 ,price =a-(700) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.046 ,price =a-(750) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.049 ,price =a-(800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.052 ,price =a-(850) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.055 ,price =a-(900) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.058 ,price =a-(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.061 ,price =a-(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.064 ,price =a-(1050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.067 ,price =a-(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.070 ,price =a-(1150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.073 ,price =a-(1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.100 ,price =a-(2000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())


            elif now_close > average20 and buy_size_d >= 0.1  and sell_size < gty_d:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(10) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(30) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003 ,price =a_1+(60) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003 ,price =a_1+(100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.003 ,price =a_1+(150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004 ,price =a_1+(210) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004 ,price =a_1+(270) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004 ,price =a_1+(330) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004 ,price =a_1+(390) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.005 ,price =a_1+(450) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.005 ,price =a_1+(510) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.005 ,price =a_1+(570) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.005 ,price =a_1+(630) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.043 ,price =a_1+(700) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.046 ,price =a_1+(750) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.049 ,price =a_1+(800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.052 ,price =a_1+(850) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.055 ,price =a_1+(900) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.058 ,price =a_1+(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.061 ,price =a_1+(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.064 ,price =a_1+(1050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.067 ,price =a_1+(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.070 ,price =a_1+(1150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.073 ,price =a_1+(1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.100 ,price =a_1+(2000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

            else:
                pass

            #지정가 청산주문

            if sell_size < 0.05:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=round(buy_size/3,3),price = buy_entry_price+buy_j1,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=round(buy_size/3,3),price = buy_entry_price+buy_j2,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=round(buy_size-(round(buy_size/3,3)+round(buy_size/3,3)),3),price = buy_entry_price+buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            else:
                pass

            if buy_size < 0.05:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=round(sell_size/3,3),price = sell_entry_price-sell_j1,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=round(sell_size/3,3),price = sell_entry_price-sell_j2,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=round(sell_size-(round(sell_size/3,3)+round(sell_size/3,3)),3),price = sell_entry_price-sell_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            else:
                pass

            if sell_size >= 0.05:
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=round(buy_size_d/3,3),price = buy_entry_price+buy_j1,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=round(buy_size_d/3,3),price = buy_entry_price+buy_j2,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=round(buy_size_d-(round(buy_size_d/3,3)+round(buy_size_d/3,3)),3),price = buy_entry_price+buy_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            else:
                pass

            if buy_size >= 0.05:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=round(sell_size_d/3,3),price = sell_entry_price-sell_j1,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=round(sell_size_d/3,3),price = sell_entry_price-sell_j2,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=round(sell_size_d-(round(sell_size_d/3,3)+round(sell_size_d/3,3)),3),price = sell_entry_price-sell_j3,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            else:
                pass
        else:
            pass





         #시장가 청산하기    
        # if now_close >= buy_entry_price+buy_j3+10:
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Market",qty=buy_size-sell_size,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass

        # if now_close <= sell_entry_price-sell_j3-10:
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Market",qty=sell_size-buy_size,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        # else:
        #     pass


         #양매수 시장가 청산하기    
        if close_haf_3 > 0.003:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Market",qty=close_b,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass

        if close_haf_3 > 0.003:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Market",qty=close_s,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass



       
                      
        
        print(buy_size)
        print(sell_size)
        print(buy_entry_price)
        print(sell_entry_price)
        print(now_close)
        print(gty_d)
        print(time_s)
        # print(close_haf_1)
        # print(close_haf_2)
        print(close_haf_3)
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