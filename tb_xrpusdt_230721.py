from types import new_class
import bybit
import pandas as pd
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
import collections
from collections import Counter
from urllib.request import urlopen
from urllib.error import HTTPError

client = bybit.bybit(test=False, api_key="HlCqvTfGuZ87KwwAz3", api_secret="wjPZzFU8Irznbb2uzhH6Srd1Ddly5XRGXgof")
apiKey='HlCqvTfGuZ87KwwAz3'
apisecret='wjPZzFU8Irznbb2uzhH6Srd1Ddly5XRGXgof'
session = HTTP(
    endpoint='https://api.bybit.com',
    api_key="HlCqvTfGuZ87KwwAz3",
    api_secret="wjPZzFU8Irznbb2uzhH6Srd1Ddly5XRGXgof")


le_2=3
le_3=3
le_4=3
h1=0.067
h2=0.067
h3=0.067
h4=0.067
h5=0.067
h6=0.067
h7=0.067
h8=0.067
h9=0.067
h10=0.067  
l1=0.067
l2=0.067
l3=0.067
l4=0.067
l5=0.067
l6=0.067
l7=0.067
l8=0.067
l9=0.067
l10=0.067

pename=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
for y in pename:
    globals()['e_e_%s' % y] = 0
    globals()['p_p_%s' % y] = 0
size_abs=0
buy_close2=0
sell_close2=0
now_close=0
size1=0
size2=0
size3=0
size4=0
buy_size_e=0
sell_size_e=0
my_stop=0
my_rev=0
my_tep1=0
my_usdt_d=0
rat_1=3500
ssall = 100
lev1=1
udt=0
sell_en = 0

num=1

now_close_9 = 0.78 #기준자산의 현재가
price_s=0

while True:
    try:

        ticker="XRPUSDT"
        sosu=4
        ticker2="XRPUSD"
        ticker2_1="XRP"
        
        # 분봉가저오기
        now = datetime.utcnow()
        time_d = int(now.day) #날짜 카운트
        time_h = int(now.hour) #시간 카운트
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
        average20 = float(round(average,sosu))

        bb_u_5=round(float(average20 + std*2),sosu)
        bb_l_5=round(float(average20 - std*2),sosu)

         # 5분초단위=300, 20개 가저오기, interval="5" =5분봉
        since_5 = unixtime - 300*20
        response_5=session.query_kline(symbol=ticker,interval="5",**{'from':since_5})['result']
        df_2 = pd.DataFrame(response_5)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_5 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_5_20 = float(round(average_5,sosu))

        bb_u=round(float(average_5_20 + std_1*2),sosu)
        bb_l=round(float(average_5_20 - std_1*2),sosu)

         # 30분초단위=1800, 20개 가저오기, interval="30" =30분봉
        since_30 = unixtime - 1800*20
        response_30=session.query_kline(symbol=ticker,interval="30",**{'from':since_30})['result']
        df_2 = pd.DataFrame(response_30)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_30 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_30_20 = float(round(average_30,sosu))

        bb_u_30=round(float(average_30_20 + std_1*2),sosu)
        bb_l_30=round(float(average_30_20 - std_1*2),sosu)

        # 60분초단위=3600, 20개 가저오기, interval="60" =60분봉
        since_60 = unixtime - 3600*20
        response_60=session.query_kline(symbol=ticker,interval="60",**{'from':since_60})['result']
        df_2 = pd.DataFrame(response_60)
        df_3=df_2['close'].astype(float)#문자열 숫자열로변환

        average_60 = numpy.mean(df_3)
        std_1=numpy.std(df_3)
        average_60_20 = float(round(average_60,sosu))

        bb_u_60=round(float(average_60_20 + std_1*le_2),sosu)
        bb_l_60=round(float(average_60_20 - std_1*le_2),sosu)
        
        
        
        #현재가조회(USDT)- 60분봉 조회
        now_close_1_60 = client.LinearKline.LinearKline_get(symbol=ticker, interval="60", **{'from':unixtime-7200}).result()
        now_close_60 = round(float(now_close_1_60[0]["result"][-1]["close"]),sosu)

        now_open_60 = round(float(now_close_1_60[0]["result"][-2]["open"]),4) #전봉의 시가
        now_low_60 = round(float(now_close_1_60[0]["result"][-2]["low"]),4)   #전봉의 저가
        now_high_60 = round(float(now_close_1_60[0]["result"][-2]["high"]),4) #전봉의 고가
        h_close_60 = round(float(now_close_1_60[0]["result"][-2]["close"]),4) #전봉의 종가

        print(now_open_60, "전봉의 시가")
        print(now_low_60, "전봉의 저가")
        print(now_high_60, "전봉의 고가")
        print(h_close_60, "전봉의 종가")
        
     

        

        # 내 포지션 정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()
        
        
        
        buy_size = int(my_infor[0]["result"][0]["size"])
        sell_size = int(abs(my_infor[0]["result"][1]["size"]))
        my_leverage = int(abs(my_infor[0]["result"][0]["leverage"]))
        print(buy_size,"공매수수량")
        print(sell_size,"공매도수량")
        print(my_leverage,"레버리지")

        # #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),sosu)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),sosu)



        

        # #각 포지션 청산가격
        # buy_liq_price=round(float(my_infor[0]["result"][0]["liq_price"]),2)
        # sell_liq_price=round(float(my_infor[0]["result"][1]["liq_price"]),2)            
        
        # 내 활성주문 가저오기
        my_query= client.LinearOrder.LinearOrder_query(symbol=ticker).result()
        # 활성주문중 청산주문골라내기
        count_1 = my_query[0]["result"]
        re_len = len(count_1)

        #매수주문 내역받아오기 , chr = 문자열로 변환
        for n in range(0, re_len):
            globals()['cls_%s' % n] = Counter({(count_1[n]["side"])+chr((count_1[n]["reduce_only"])):(count_1[n]["qty"])})

        #에러 나는 매수주문내역 더미 만들어주기 
        for n in range(re_len, 100):
            globals()['cls_%s' % n] = Counter({'Buy\x00':0})

        #buy주문, sell주문 수량합계 계산하기
        cls_sum=[cls_0+cls_1+cls_2+cls_3+cls_4+cls_5+cls_6+cls_7+cls_8+cls_9+cls_10+cls_11+cls_12+cls_13+cls_14+cls_15+cls_16+cls_17+cls_18+cls_19+cls_20+cls_21+cls_22+cls_23+cls_24+cls_25+cls_26+cls_27+cls_28+cls_29+cls_30+cls_31+cls_32
        +cls_33+cls_34+cls_35+cls_36+cls_37+cls_38+cls_39+cls_40+cls_41+cls_42+cls_43+cls_44+cls_45+cls_46+cls_47+cls_48+cls_49+cls_50+cls_51+cls_52+cls_53+cls_54+cls_55+cls_56+cls_57+cls_58+cls_59+cls_60+cls_61+cls_62+cls_63+cls_64+cls_65+cls_66
        +cls_67+cls_68+cls_69+cls_70+cls_71+cls_72+cls_73+cls_74+cls_75+cls_76+cls_77+cls_78+cls_79+cls_80+cls_81+cls_82+cls_83+cls_84+cls_85+cls_86+cls_87+cls_88+cls_89+cls_90+cls_91+cls_92+cls_93+cls_94+cls_95+cls_96+cls_97+cls_98+cls_99]
        
        #'Buy\x00': 공매수주문수량, 'Sell\x00' :공매도주문수량 , 'Buy\x01' :공매도청산주문수량, 'Sell\x01' :공매수청산주문수량
        buy_cls=cls_sum[0]['Buy\x00']  #buy수량합계
        sell_cls=cls_sum[0]['Sell\x00'] #sell수량합계

        buy_close=cls_sum[0]['Sell\x01']  #공매수청산주문수량
        sell_close=cls_sum[0]['Buy\x01']  #공매도청산주문수량


       #========================================각 포지션별 주문 갯수 구하기=========================================================================
        #매수주문 내역받아오기 , chr = 문자열로 변환
        for n in range(0, re_len):
            globals()['lens_%s' % n] = Counter({(count_1[n]["side"])+chr((count_1[n]["reduce_only"])):1})

        #에러 나는 매수주문내역 더미 만들어주기 
        for n in range(re_len, 100):
            globals()['lens_%s' % n] = Counter({'Buy\x00':0})

        #buy주문, sell주문 수량합계 계산하기
        len_sum=[lens_0+lens_1+lens_2+lens_3+lens_4+lens_5+lens_6+lens_7+lens_8+lens_9+lens_10+lens_11+lens_12+lens_13+lens_14+lens_15+lens_16+lens_17+lens_18+lens_19+lens_20+lens_21+lens_22+lens_23+lens_24+lens_25+lens_26+lens_27+lens_28+lens_29+lens_30+lens_31+lens_32
        +lens_33+lens_34+lens_35+lens_36+lens_37+lens_38+lens_39+lens_40+lens_41+lens_42+lens_43+lens_44+lens_45+lens_46+lens_47+lens_48+lens_49+lens_50+lens_51+lens_52+lens_53+lens_54+lens_55+lens_56+lens_57+lens_58+lens_59+lens_60]
        
        #'Buy\x00': 공매수주문수량, 'Sell\x00' :공매도주문수량 , 'Buy\x01' :공매도청산주문수량, 'Sell\x01' :공매수청산주문수량
        # 각 주문 갯수 계산
        buy_len=len_sum[0]['Buy\x00'] #buy수량합계
        sell_len=len_sum[0]['Sell\x00'] #sell수량합계

        buy_close_len=len_sum[0]['Sell\x01'] #공매수청산주문수량
        sell_close_len=len_sum[0]['Buy\x01']  #공매도청산주문수량
        #=================================================================================================================

                
        # #자산조회(usdt마켓)
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))
        print(my_usdt,"usdt총자산")
          # 내자산가저오기(usd마켓)
        myxrp=session.get_wallet_balance(coin=ticker2_1)
        my_usd= float(myxrp["result"][ticker2_1]['equity']) #총자본XRP
        print(my_usd ,'총자본XRPUSD' )
        
       

        # #아침 9시 총자산정산
        # if time_h == 0 and time_m ==0 and (time_s ==0 or time_s ==1 or time_s ==2 or time_s ==3 or time_s ==4 or time_s ==5):
        #     udt = 0
        # else:
        #     pass

        # if udt == 0 and buy_size == 0 and sell_size == 0 and my_usdt_d != my_usdt or my_usdt_d == 0:
        #     my_usdt_d = my_usdt
        #     udt = 1
        # else:
        #     pass



        if 50 >= my_leverage >45: # 1/10
            le_1 = 50
        elif 45 >= my_leverage > 40: # 1/15
            le_1 = 45
        elif 40 >= my_leverage > 35: # 1/20
            le_1 = 40
        elif 35 >= my_leverage > 30: # 1/25
            le_1 = 35
        elif 30 >= my_leverage > 25: # 1/30
            le_1 = 30
        elif my_leverage < 30: # 1/35
            le_1 = 25
        else:
            pass

        qty_40=my_usdt/(60-le_1)


        le_2 = round((le_1-my_leverage),1)

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

        


        #현재가조회(USDT)
        now_close_1 = client.LinearKline.LinearKline_get(symbol=ticker, interval="1", **{'from':unixtime-120}).result()
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),sosu)
        print(now_close,"xrpusdt현재가")


        #usd -> xrp수량으로 환산
        my_usd_sell=round((my_usd/now_close),0)


        # # 위험수량 결정 자본금의 7배 이상  (xrp단위수량)   
        # gty_d = round((my_usdt/now_close)*15,0)

        # # 기본 수량 계산 - 반대포지션이 이수량되면 두배매수
        gty_c = round((my_usdt/now_close)*1,0)

        # 양매수 기준수량 (xrp단위수량)
        gty_b = round((my_usdt/now_close)*5,0)

        # buy_size_d = round(buy_size-abs(sell_size),0)
        # sell_size_d = round(abs(sell_size)-buy_size,0)
        # size_abs = round(abs( sell_size-buy_size),0)

        # usdt -> xrp수량으로 환산
        qty_10=round(qty_40/now_close,0)


        # 주문취소하기(1시간마다 주문리셋)
        if time_m ==0 and (time_s ==0 or time_s ==1 or time_s ==2 or time_s==3 ) and sell_len != 0  and my_leverage !=50 and my_leverage !=40 :
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소
        else:
            pass
        
        
        # usd수량 만큼 공매도수량매수(양매수표지션유지)
        if my_usd > my_usdt and gty_c > sell_size and bb_u_60-0.0001 <= now_close and  my_leverage !=50 and my_leverage !=40:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=sell_size-my_usd_sell ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
       

        # #======================공매도주문하기===================================================================================================
        if sell_len == 0 and bb_u_60-0.0001 <= now_close and gty_c <= sell_size < gty_b and  my_leverage !=50 and my_leverage !=40:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.003)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.007)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.012)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.018)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.025)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.033)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.042)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.052)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.063)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.075)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.088)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.102)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.116)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.130)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_10 ,price =round((now_close*(1.144)),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            
        else:
            pass

        # 청산하기
        #청산을 위해서 내 기준 usdt계산
        if sell_size <= my_usd_sell:
            price_s=my_usdt #총자산USDt 저장
            now_close_9 = now_close
        else:
            pass

        if price_s * 1.01 < my_usdt:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=sell_size-my_usd_sell,price =now_close ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            
        else:
            pass
        
            
    

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