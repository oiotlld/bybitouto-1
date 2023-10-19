from types import new_class
import bybit
import pandas as pd
from pybit.usdt_perpetual import HTTP as usdt_perpetualHTTP
import time
from datetime import datetime
import calendar
import numpy
import collections
from collections import Counter
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
my_usdt=700
rat_1=3500
ssall = 100
lev1=1
udt=0
sell_en = 0

num=1

now_close_9 = 0.55 #기준자산의 현재가
price_s=0
dc=0
dc_1=0
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

        bb_u_60=round(float(average_60_20 + std_1*3),sosu)
        bb_l_60=round(float(average_60_20 - std_1*3),sosu)
        print(bb_u_60,"bb_u_60=60분봉볼리저상단")
        
        
        
        
        #현재가조회(USDT)- 60분봉 조회
        now_close_1_60 = client.LinearKline.LinearKline_get(symbol=ticker, interval="60", **{'from':unixtime-7200}).result()
        now_close_60 = round(float(now_close_1_60[0]["result"][-1]["close"]),sosu)
        high_60 = round(float(now_close_1_60[0]["result"][-1]["high"]),sosu)
        low_60 = round(float(now_close_1_60[0]["result"][-1]["low"]),sosu)

        now_open_60 = round(float(now_close_1_60[0]["result"][-2]["open"]),4) #전봉의 시가
        now_low_60 = round(float(now_close_1_60[0]["result"][-2]["low"]),4)   #전봉의 저가
        now_high_60 = round(float(now_close_1_60[0]["result"][-2]["high"]),4) #전봉의 고가
        h_close_60 = round(float(now_close_1_60[0]["result"][-2]["close"]),4) #전봉의 종가

        print(now_open_60, "전봉의 시가")
        print(now_low_60, "전봉의 저가")
        print(now_high_60, "전봉의 고가")
        print(h_close_60, "전봉의 종가============")
        print(high_60, "high_60현재봉의고가")
        print(low_60, "low_60현재봉의고가")
        
             

        # 내 포지션 정보가저오기
        my_infor=session.my_position(category="inverse", symbol=ticker,)
        # print(my_infor)


        
        
        
        buy_position = my_infor['result'][0]
        sell_position = my_infor['result'][1]
        buy_size = int(buy_position['size'])
        sell_size = int(abs(sell_position['size']))
        my_leverage = int(abs(buy_position['leverage']))
        print(buy_size,"공매수수량")
        print(sell_size,"공매도수량")
        print(my_leverage,"레버리지")

        # #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(buy_position["entry_price"]),sosu)
        sell_entry_price = round(float(sell_position["entry_price"]),sosu)
        print(buy_entry_price,"buy평균단가")
        print(sell_entry_price,"sell평균단가")

        

        # #각 포지션 청산가격
        # buy_liq_price=round(float(my_infor[0]["result"][0]["liq_price"]),2)
        # sell_liq_price=round(float(my_infor[0]["result"][1]["liq_price"]),2)            
        
        # 내 활성주문 가저오기
        my_query= client.LinearOrder.LinearOrder_query(symbol=ticker).result()
        # 활성주문중 청산주문골라내기
        count_1 = my_query[0]["result"]
        re_len = len(count_1)
        print(re_len,'================주문수량===========')

    #     #매수주문 내역받아오기 , chr = 문자열로 변환
    #     for n in range(0, re_len):
    #         globals()['cls_%s' % n] = Counter({(count_1[n]["side"])+chr((count_1[n]["reduce_only"])):(count_1[n]["qty"])})

    #     #에러 나는 매수주문내역 더미 만들어주기 
    #     for n in range(re_len, 100):
    #         globals()['cls_%s' % n] = Counter({'Buy\x00':0})

    #     #buy주문, sell주문 수량합계 계산하기
    #     cls_sum=[cls_0+cls_1+cls_2+cls_3+cls_4+cls_5+cls_6+cls_7+cls_8+cls_9+cls_10+cls_11+cls_12+cls_13+cls_14+cls_15+cls_16+cls_17+cls_18+cls_19+cls_20+cls_21+cls_22+cls_23+cls_24+cls_25+cls_26+cls_27+cls_28+cls_29+cls_30+cls_31+cls_32
    #     +cls_33+cls_34+cls_35+cls_36+cls_37+cls_38+cls_39+cls_40+cls_41+cls_42+cls_43+cls_44+cls_45+cls_46+cls_47+cls_48+cls_49+cls_50+cls_51+cls_52+cls_53+cls_54+cls_55+cls_56+cls_57+cls_58+cls_59+cls_60+cls_61+cls_62+cls_63+cls_64+cls_65+cls_66
    #     +cls_67+cls_68+cls_69+cls_70+cls_71+cls_72+cls_73+cls_74+cls_75+cls_76+cls_77+cls_78+cls_79+cls_80+cls_81+cls_82+cls_83+cls_84+cls_85+cls_86+cls_87+cls_88+cls_89+cls_90+cls_91+cls_92+cls_93+cls_94+cls_95+cls_96+cls_97+cls_98+cls_99]
        
    #     #'Buy\x00': 공매수주문수량, 'Sell\x00' :공매도주문수량 , 'Buy\x01' :공매도청산주문수량, 'Sell\x01' :공매수청산주문수량
    #     buy_cls=cls_sum[0]['Buy\x00']  #buy수량합계
    #     sell_cls=cls_sum[0]['Sell\x00'] #sell수량합계

    #     buy_close=cls_sum[0]['Sell\x01']  #공매수청산주문수량
    #     sell_close=cls_sum[0]['Buy\x01']  #공매도청산주문수량


    #    #========================================각 포지션별 주문 갯수 구하기=========================================================================
    #     #매수주문 내역받아오기 , chr = 문자열로 변환
    #     for n in range(0, re_len):
    #         globals()['lens_%s' % n] = Counter({(count_1[n]["side"])+chr((count_1[n]["reduce_only"])):1})

    #     #에러 나는 매수주문내역 더미 만들어주기 
    #     for n in range(re_len, 100):
    #         globals()['lens_%s' % n] = Counter({'Buy\x00':0})

    #     #buy주문, sell주문 수량합계 계산하기
    #     len_sum=[lens_0+lens_1+lens_2+lens_3+lens_4+lens_5+lens_6+lens_7+lens_8+lens_9+lens_10+lens_11+lens_12+lens_13+lens_14+lens_15+lens_16+lens_17+lens_18+lens_19+lens_20+lens_21+lens_22+lens_23+lens_24+lens_25+lens_26+lens_27+lens_28+lens_29+lens_30+lens_31+lens_32
    #     +lens_33+lens_34+lens_35+lens_36+lens_37+lens_38+lens_39+lens_40+lens_41+lens_42+lens_43+lens_44+lens_45+lens_46+lens_47+lens_48+lens_49+lens_50+lens_51+lens_52+lens_53+lens_54+lens_55+lens_56+lens_57+lens_58+lens_59+lens_60]
        
    #     #'Buy\x00': 공매수주문수량, 'Sell\x00' :공매도주문수량 , 'Buy\x01' :공매도청산주문수량, 'Sell\x01' :공매수청산주문수량
    #     # 각 주문 갯수 계산
    #     buy_len=len_sum[0]['Buy\x00'] #buy수량합계
    #     sell_len=len_sum[0]['Sell\x00'] #sell수량합계
    #     print(sell_len, "숏주문수량")

    #     buy_close_len=len_sum[0]['Sell\x01'] #공매수청산주문수량
    #     sell_close_len=len_sum[0]['Buy\x01']  #공매도청산주문수량
    #     #=================================================================================================================

                
        #자산조회(usdt마켓)
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))
        print(my_usdt,"my_usdt=보유usdt금액")
        
        
        # 내자산가저오기(usd마켓)
        myxrp=session.get_wallet_balance(coin=ticker2_1)
        my_usd= float(myxrp["result"][ticker2_1]['equity']) #총자본XRP
        print(my_usd ,'my_usd=usd마켓에서의XRP갯수' )
        
       

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
        print(now_close,"now_close=xrpusdt현재가")

        bb_cha=round((now_close-bb_l_60)/now_close,2)
        print(bb_cha,"bb_cha=볼린저하단과 현재가차이")
        

        #usdt -> xrp수량으로 환산
        my_usdt_xrp=round((my_usdt/now_close),0)
        print(my_usdt_xrp,"my_usdt_xrp= usdt-> xrp환산")


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
        if time_m ==0 and (time_s ==0 or time_s ==1 or time_s ==2 or time_s==3 ) and re_len != 0  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result(),"모든주문취소") # 모든주문취소
            dt=0
            high_60_1 = high_60
            now_close_2=0
            now_close_3=0
            now_close_4=0
        else:
            pass
        abu_13=average_60_20
        abl_13=average_60_20
        if  open_60_1 != now_open_60  and my_leverage !=50  :
            open_60_1 = now_open_60
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
            abu = bb_u_60  # 0이 아닌 값이 없을 경우 
        
        non_zero_values_2 = [x for x in variables_2 if x != 0]
        # 0이 아닌 값들의 평균 계산
        if non_zero_values_2:
             abl= sum(non_zero_values_2) / len(non_zero_values_2)
        else:
            abl = bb_l_60  # 0이 아닌 값이 없을 경우
        
        # usd수량 만큼 공매도수량매수(양매수표지션유지)
        if my_usd > sell_size  and bb_u_60-0.0001 <= now_close and  my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=round(my_usd,0)-sell_size ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result(),"1배유지숏주문")

        else:
            pass
       
        

        #======================공매도주문하기===================================================================================================
        if dt < 1 and high_60_1 < high_60 and bb_u_60 <= now_close and gty_c <= sell_size < gty_b  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=qty_10 ,price =round((now_close*(1.000)),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            high_60_1 = high_60
            dt=dt+1
            dt_1=1
        elif dt <= 4 and high_60_1 < high_60 and bb_u_60 <= now_close and gty_c <= sell_size < gty_b  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=qty_10*1.2 ,price =round((now_close*(1.000)),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            high_60_1 = high_60
            dt=dt+1
            dt_1=1
        elif dt <= 6 and high_60_1 < high_60 and bb_u_60 <= now_close and gty_c <= sell_size < gty_b  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=qty_10*2.07 ,price =round((now_close*(1.000)),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            high_60_1 = high_60
            dt=dt+1
            dt_1=1
        elif dt <= 8 and high_60_1 < high_60 and bb_u_60 <= now_close and gty_c <= sell_size < gty_b  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=qty_10*2.99 ,price =round((now_close*(1.000)),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            high_60_1 = high_60
            dt=dt+1
            dt_1=1
        elif dt > 8 and high_60_1 < high_60 and bb_u_60 <= now_close and gty_c <= sell_size < gty_b  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=qty_10*4.30 ,price =round((now_close*(1.000)),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            high_60_1 = high_60
            dt=dt+1
            dt_1=1
        else:
            pass

        # 청산하기
        #청산을 위해서 내 기준 usdt계산
        if sell_size <= my_usd:
            price_s=my_usdt #총자산USDt 저장
            now_close_9 = now_close
        else:
            pass

        #청산신호 볼린저 하향돌파
        if sell_size>my_usd and bb_u_60 > now_close and now_close_2 > now_close:
            now_close_2 = now_close
            dt_2=dt_2+1
        elif sell_size>my_usd and average_60_20 > now_close and now_close_3 > now_close:
            now_close_3 = now_close
            dt_3=dt_3+1
        elif sell_size>my_usd and bb_l_60 > now_close and now_close_4 > now_close:
            now_close_4 = now_close
            dt_4=dt_4+1
        else:
            pass

        #청산신호 볼린저 상단돌파해서 급등할때 최대수익구간구하기
        if sell_size>my_usd and bb_l_60 > now_close and low_60_1 > low_60:
            low_60_1=low_60
            dc=dc+1
            size_1=round((sell_size-my_usd)/65,0)
        else:
            pass
        
        if dt_4>1 and price_s * 1.003 < my_usdt and bb_l_60 < now_close  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=(sell_size-my_usd),price =now_close ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result(),'볼린저하단이탈시청산주문')    
        elif dt_3>1 and price_s * 1.005 < my_usdt and average_60_20 < now_close and abu < average_60_20 and abl < average_60_20 and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=(sell_size-my_usd),price =now_close ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result(),'볼린저중단이탈시청산주문')    
        elif dt_2>1 and price_s * 1.01 < my_usdt and bb_u_60 < now_close  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=(sell_size-my_usd),price =now_close ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result(),'볼린저상단이탈시청산주문')    
        elif price_s * 1.02 < my_usdt and bb_u_60 < now_close  and my_leverage !=50 :
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=(sell_size-my_usd),price =now_close ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result(),'볼린저하단에서청산주문')    
        else:
            pass
        
        if price_s*1.003 < my_usdt and dc>2 and sell_size > my_usd and bb_l_60 > now_close and dc_1 > now_close_1 and my_leverage !=50:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=size_1*dc,price =now_close ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result(),'usd자산과비교청산')
            dc_1=now_close
        else:
            pass

        if sell_size <= my_usd:
            dc=0
            dt_2=0
            dt_3=0
            dt_4=0
        else:
            pass


        print(dt,'dt=볼린저상단돌파누적신호')
        print(dt_2,'dt_2=1볼린저상단하양돌파')
        print(dt_3,'dt_3=1볼린저중단하양돌파')
        print(dt_4,'dt_4=1볼린저하단하양돌파')

    

        print("실행중=======================================================================================================")

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