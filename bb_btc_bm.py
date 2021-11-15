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

        now_open = round(float(now_close_1[0]["result"][-1]["open"]),sosu)
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
        size_abs = abs( sell_size-buy_size)

        #현재가의 0.1%~0.3%분할 청산_지정가주문시
       
        buy_j3 = round(buy_entry_price*0.003,0)
        buy_j2 = round(buy_entry_price*0.002,0)
        buy_j1 = round(buy_entry_price*0.001,0)
        
        sell_j3 = round(sell_entry_price*0.003,0)
        sell_j2 = round(sell_entry_price*0.002,0)
        sell_j1 = round(sell_entry_price*0.001,0)

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
        
        # # 평단의 격차가벌어젓을때 손실없이 수량을 털기위해 많은쪽 포지션의 수량을 절반만 적용한 수익을 구해 수익구간에서 청산
        
        ccc=0.5
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
    
        if time_m==0 or time_m==2 or time_m==4 or time_m==6 or time_m==8 or time_m==10 or time_m==12 or time_m==14 or time_m==16 or time_m==18 or time_m==20 or time_m==22 or time_m==24 or time_m==26 or time_m==28 or time_m==29 or time_m==31 or time_m==33 or time_m==35 or time_m==37 or time_m==39 or time_m==41 or time_m==43 or time_m==45 or time_m==47 or time_m==49 or time_m==51 or time_m==53 or time_m==55 or time_m==57 or time_m==59:
            time_2m=time_m*0
        else:
            time_2m=time_m

        #자본금 대비 투입량 증가 기본자본금 5000USDT를 기준으로 투입자본금늘어나는 만큼 투입수량에 + 더해주는방법

        # if my_usdt > 5000:
        #     rb=(round((my_usdt / 5000),)-1)*0.001
        # elif my_usdt <= 5000:
        #     rb=0
        # else:
        #     pass
              

        if now_close < average20 and now_open > average20 : # 현재가가 볼린전 중단(20일이평선)을 하향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

        
            if buy_size < gty_d:
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.001 ,price =a-(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.001 ,price =a-(50) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.002 ,price =a-(110) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.004 ,price =a-(180) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.008 ,price =a-(260) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.008 ,price =a-(350) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.016 ,price =a-(450) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.016 ,price =a-(560) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.017 ,price =a-(680) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.018 ,price =a-(810) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.019 ,price =a-(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.020 ,price =a-(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.030 ,price =a-(1260) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.040 ,price =a-(1430) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.050 ,price =a-(1610) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.060 ,price =a-(1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.110 ,price =a-(2040) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.190 ,price =a-(2330) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.350 ,price =a-(3210) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.055 ,price =a-(900) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.058 ,price =a-(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.061 ,price =a-(1000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.064 ,price =a-(1050) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.067 ,price =a-(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.070 ,price =a-(1150) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.073 ,price =a-(1200) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=0.100 ,price =a-(2000) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())


           

            else:
                pass
        else:
            pass

        if now_close > average20 and now_open < average20 : # 현재가가 볼린전 중단(20일이평선)을 상향 돌파시
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

         
            if sell_size < gty_d:
               
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.001 ,price =a_1+(0) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.001 ,price =a_1+(50) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.002 ,price =a_1+(110) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.004 ,price =a_1+(180) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.008 ,price =a_1+(260) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.008 ,price =a_1+(350) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.016 ,price =a_1+(450) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.016 ,price =a_1+(560) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.017 ,price =a_1+(680) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.018 ,price =a_1+(810) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.019 ,price =a_1+(950) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.020 ,price =a_1+(1100) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.030 ,price =a_1+(1260) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.040 ,price =a_1+(1430) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.050 ,price =a_1+(1610) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.060 ,price =a_1+(1800) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.110 ,price =a_1+(2040) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.190 ,price =a_1+(2330) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=0.350 ,price =a_1+(3210) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            else:
                pass

            #지정가 청산주문
        else:
            pass

        




        #  시장가 청산하기    sell_j3=0.3% 수익이나면 청산
        if now_close >= buy_entry_price+buy_j1:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=buy_size-sell_size,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        else:
            pass

        if now_close <= sell_entry_price-sell_j1:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=sell_size-buy_size,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
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
        print(time_m)
        print(time_2m)
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