from types import new_class
import bybit
import pandas as pd
from pybit.inverse_perpetual import HTTP as InversePerpetualHTTP
import time
from datetime import datetime
import calendar
import numpy
import collections
from urllib.request import urlopen
from urllib.error import HTTPError

client = bybit.bybit(test=False, api_key="mykey", api_secret="mysecret")
apiKey='mykey'
apisecret='mysecret'
session = usdt_perpetualHTTP(
    endpoint='https://api.bybit.com',
    api_key="mykey",
    api_secret="mysecret")



le_2=3
le_3=3
le_4=3
price_s=3295 #총자본USD= 추가로자본투입할때 계산해서 그시점의 나의 원금을 넣어줘야함(다시돌릴때)
now_close_9 = 0.4738 #기준자산의 현재가
sizecount=0
dc=0
dc_1=0
dc_2=0
dc_3=0
dc_4=0
dt=0
dt_1=0
dt_2=0
dt_3=0
dt_4=0
low_6=0
open_5_1=0
open_60_1=0
low_60_1=100
high_60_1 =0
now_close_2=0
now_close_3=0
now_close_4=0
abu=0
abu_1=0
abu_2=0
abu_3=0
abu_4=0
abu_5=0
abu_6=0
abu_7=0
abu_8=0
abu_9=0
abu_10=0
abu_11=0
abu_12=0
abu_13=0
abl=0
abl_1=0
abl_2=0
abl_3=0
abl_4=0
abl_5=0
abl_6=0
abl_7=0
abl_8=0
abl_9=0
abl_10=0
abl_11=0
abl_12=0
abl_13=0
size_1=0


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

        since_6 = unixtime - 300
        response_6=session.query_kline(symbol=ticker,interval="5",**{'from':since_6})['result']
        df_4 = pd.DataFrame(response_6)
        df_5=df_4['low'].astype(float)#문자열 숫자열로변환
        low_5=numpy.mean(df_5)
        df_5=df_4["open"].astype(float)
        open_5=round(numpy.mean(df_5),4)
        print(open_5, "open_5=5분봉시작가")
        print(low_5, "low_5=5분봉최저가")


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

        bb_u_60_1=round(float(average_60_20 + std_1*(2)),sosu)
        bb_l_60_1=round(float(average_60_20 - std_1*(2)),sosu)

        bb_u_60_2=round(float(average_60_20 + std_1*(3)),sosu)
        bb_l_60_2=round(float(average_60_20 - std_1*(3)),sosu)

        since_60 = unixtime - 3600
        response_60=session.query_kline(symbol=ticker,interval="60",**{'from':since_60})['result']
        df_2 = pd.DataFrame(response_60)
        df_3 = df_2['open'].astype(float)
        open_60=numpy.mean(df_3)
        print(open_60, '1시간봉시작가')

        # 240분초단위=14400, 20개 가저오기, interval="240" =240분봉
        since_240 = unixtime - 14400*20
        print(open_5, "5분봉시작가")
        print(low_5, "5분봉최저가")


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

        bb_u_60_1=round(float(average_60_20 + std_1*(2)),sosu)
        bb_l_60_1=round(float(average_60_20 - std_1*(2)),sosu)

        bb_u_60_2=round(float(average_60_20 + std_1*(3)),sosu)
        bb_l_60_2=round(float(average_60_20 - std_1*(3)),sosu)

        since_60 = unixtime - 3600
        response_60=session.query_kline(symbol=ticker,interval="60",**{'from':since_60})['result']
        df_2 = pd.DataFrame(response_60)
        df_3 = df_2['open'].astype(float)
        open_60=numpy.mean(df_3)
        print(open_60, 'open_60=1시간봉시작가')

        df_4 = pd.DataFrame(response_60)
        df_5=df_4['low'].astype(float)#문자열 숫자열로변환
        low_60=numpy.mean(df_5)
        print(low_60, "low_60=60분봉최저가")
        df_6=df_4['high'].astype(float)#문자열 숫자열로변환
        high_60=numpy.mean(df_6)
        print(high_60, "high_60=60분봉최고가")

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

        #5분초단위=300, 20개 가저오기, interval="5" =5분봉
        since_5 = unixtime - 300*2
        response_5=session.query_kline(symbol=ticker,interval="5",**{'from':since_5})['result']
        df_2 = pd.DataFrame(response_5)
        df_3=df_2['low'].astype(float)#문자열 숫자열로변환

        low_7 = numpy.min(df_3)

        # # # 내 포지션 정보가저오기
        my_infor=session.my_position(symbol=ticker)
        #print(my_infor)        

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

        bb_cha=round((bb_u_60_2-now_close_1)/now_close_1,2)
        print(bb_cha,"bb_cha=볼린저하단과 현재가차이")



        # 주문내역 받아보기
        my_data_1=session.get_active_order(symbol=ticker,order_status="New")
        my_data_2=my_data_1["result"]["data"]
        my_date_len=len(my_data_2)#주문수량 
        my_date_4=[]
        for g in range(0, my_date_len):
            my_data_3=int(my_data_1["result"]["data"][g]["leaves_qty"])
            my_date_4.append(0)

        abu_13=average_60_20
        abl_13=average_60_20
        # 주문취소하기(1시간마다 주문리셋)
        if  open_60_1 != open_60  or (time_m ==0 and time_s ==0) and leverage !=50  :
            # print(session.cancel_all_active_orders(symbol=ticker)) #모든주문취소
            open_60_1 = open_60
            dt=0
            low_60_1=low_60
            now_close_2=0
            now_close_3=0
            now_close_4=0
            abu_1=abu_2
            abu_2=abu_3
            abu_3=abu_4
            abu_4=abu_5
            abu_5=abu_6
            abu_6=abu_7
            abu_7=abu_8
            abu_8=abu_9
            abu_9=abu_10
            abu_10=abu_11
            abu_11=abu_12
            abu_12=abu_13
            abl_1=abl_2
            abl_2=abl_3
            abl_3=abl_4
            abl_4=abl_5
            abl_5=abl_6
            abl_6=abl_7
            abl_7=abl_8
            abl_8=abl_9
            abl_10=abl_11
            abl_11=abl_12
            abl_12=abl_13            
        else:
            pass

        # 변수들의 리스트 (예를 들어, 변수1, 변수2, 변수3, ...)
        variables_1 = [abu_1, abu_2, abu_3, abu_4, abu_5, abu_6, abu_7, abu_8, abu_9, abu_10, abu_11, abu_12]
        variables_2 = [abl_1, abl_2, abl_3, abl_4, abl_5, abl_6, abl_7, abl_8, abl_9, abl_10, abl_11, abl_12]

        # 0이 아닌 값을 가진 변수들의 리스트 생성
        non_zero_values_1 = [x for x in variables_1 if x != 0]
        # 0이 아닌 값들의 평균 계산
        if non_zero_values_1:
             abu= sum(non_zero_values_1) / len(non_zero_values_1)
        else:
            abu = bb_u_60_2  # 0이 아닌 값이 없을 경우 
        
        non_zero_values_2 = [x for x in variables_2 if x != 0]
        # 0이 아닌 값들의 평균 계산
        if non_zero_values_2:
             abl= sum(non_zero_values_2) / len(non_zero_values_2)
        else:
            abl = bb_l_60_2  # 0이 아닌 값이 없을 경우
    

        #투입수량결정(보유금액의 1/20)
        qty_40=my_qty/20

        if low_60_1 > low_60 and now_close_1 < bb_l_60_2 and size < my_qty*5 and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1-(0.0001)),4),qty=qty_40*(1+(dt*0.2)),time_in_force="GoodTillCancel"))
            low_60_1=low_60-(low_60*0.003)
            dt=dt+1
            dt_1=1
        
        # elif dt <= 4 and low_60_1 > low_60 and now_close_1 < bb_l_60_2 and size < my_qty*5 and leverage !=50:
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1-(0.0001)),4),qty=qty_40*1.44,time_in_force="GoodTillCancel"))
        #     low_60_1=low_60
        #     dt=dt+1
        #     dt_1=1
        
        # elif dt <= 6 and low_60_1 > low_60 and now_close_1 < bb_l_60_2 and size < my_qty*5 and leverage !=50:
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1-(0.0001)),4),qty=qty_40*2.07,time_in_force="GoodTillCancel"))
        #     low_60_1=low_60
        #     dt=dt+1
        #     dt_1=1
        
        # elif dt <= 8 and low_60_1 > low_60 and now_close_1 < bb_l_60_2 and size < my_qty*5 and leverage !=50:
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1-(0.0001)),4),qty=qty_40*2.99,time_in_force="GoodTillCancel"))
        #     low_60_1=low_60
        #     dt=dt+1
        #     dt_1=1
        
        # elif dt > 8 and low_60_1 > low_60 and now_close_1 < bb_l_60_2 and size < my_qty*5 and leverage !=50:
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1-(0.0001)),4),qty=qty_40*4.30,time_in_force="GoodTillCancel"))
        #     low_60_1=low_60
        #     dt=dt+1
        #     dt_1=1
        else:
            pass

        # #주문하기
        # # 공매수
        # if bb_l_60_2 >= now_close_1 and size<my_qty*2  and leverage !=50:
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Market",price=round((now_close_1-(0.0001)),4),qty=qty_40,time_in_force="GoodTillCancel"))
        
        # elif my_date_len == 0  and bb_l_60_2 +0.0001 >= now_close_1 and size<my_qty*5  and bb_cha > 0.07 and leverage !=50:
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.997)),4),qty=qty_40*1.2,time_in_force="GoodTillCancel"))
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.993)),4),qty=qty_40*1.44,time_in_force="GoodTillCancel"))
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.988)),4),qty=qty_40*1.73,time_in_force="GoodTillCancel"))
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.982)),4),qty=qty_40*2.07,time_in_force="GoodTillCancel"))
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.974)),4),qty=qty_40*2.49,time_in_force="GoodTillCancel"))
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.965)),4),qty=qty_40*2.99,time_in_force="GoodTillCancel"))
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.953)),4),qty=qty_40*3.58,time_in_force="GoodTillCancel"))
        #     print(session.place_active_order(symbol=ticker,side="Buy",order_type="Limit",price=round((now_close_1*(0.939)),4),qty=qty_40*4.30,time_in_force="GoodTillCancel"))
        # else:
        #     pass

        #청산신호 볼린저 상향돌파
        if size!=0 and bb_l_60_2 < now_close_1 and now_close_2 < now_close_1:
            now_close_2 = now_close_1
            dt_2=dt_2+1
        elif size!=0 and average_60_20 < now_close_1 and now_close_3 < now_close_1 :
            now_close_3 = now_close_1
            dt_3=dt_3+1
        elif size!=0 and bb_u_60_2 < now_close_1 and now_close_4 < now_close_1 :
            now_close_4 = now_close_1
            dt_4=dt_4+1
        else:
            pass

        #청산신호 볼린저 상단돌파해서 급등할때 최대수익구간구하기
        if size!=0 and bb_u_60_2 < now_close_1 and high_60_1 != high_60:
            high_60_1 = high_60
            dc=dc+1
            size_1=round(size/65,0)
        else:
            pass

        

        #공매수청산
        if  side=="Buy" and entry_price*1.02 < now_close_1 and bb_l_60_2 > now_close_1 and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size,time_in_force="GoodTillCancel"))
        elif dt_2>1  and side=="Buy" and entry_price*1.01 < now_close_1 and bb_l_60_2 > now_close_1 and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size,time_in_force="GoodTillCancel"))
            dt_2=0
        elif dt_3>1 and side=="Buy" and entry_price*1.005 < now_close_1 and average_60_20 > now_close_1 and abu > average_60_20 and abl > average_60_20 and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size,time_in_force="GoodTillCancel"))
            dt_3==0
        elif dt_4>1 and side=="Buy" and entry_price*1.003 < now_close_1 and bb_u_60_2 > now_close_1 and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size,time_in_force="GoodTillCancel"))
            dt_4=0
        elif dt_4>1 and side=="Buy" and entry_price*1.003 < now_close_1 and dc>2 and dc_1 < now_close_1 and leverage !=50:
            print(session.place_active_order(symbol=ticker,side="Sell",order_type="Market",price=round((now_close_1+(now_close_1*0.01)),4),qty=size_1*dc,time_in_force="GoodTillCancel"))
            dc_1=now_close_1
        
        else:
            pass
        if size==0:
            dc=0
            dt_2=0
            dt_3=0
            dt_4=0
        else:
            pass

        print(leverage,"레버리지")
        print(le_2,"레버리지번호")
        print(le_3,"공매도편차")
        print(le_4,"공매수편차")
        print(price_s,"기준금액")
        print(price_s*1.01,"기준금액1%수익시")
        print(my_qty,"총자산")
        print(dc, "dc=청산신호")
        print(open_60 ,'1시간봉 시가')
        print(open_60_1 ,'1시간봉 시가교체시기')
        print(open_5 ,'5분봉시가')
        print(open_5_1 , '5분봉시가교체')
        print(size , '공매도수량')
        print("=====================================================================================================================================")


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