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

num=1

while True:
    try:

        ticker="DOGEUSDT"
        sosu=4
        
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

        bb_u_60=round(float(average_60_20 + std_1*2),sosu)
        bb_l_60=round(float(average_60_20 - std_1*2),sosu)
        
        
        #현재가조회(USDT)- 60분봉 조회
        now_close_1_60 = client.LinearKline.LinearKline_get(symbol=ticker, interval="60", **{'from':unixtime-7200}).result()
        now_close_60 = round(float(now_close_1_60[0]["result"][-1]["close"]),sosu)

        now_open_60 = round(float(now_close_1_60[0]["result"][-2]["open"]),4) #전봉의 시가
        now_low_60 = round(float(now_close_1_60[0]["result"][-2]["low"]),4)   #전봉의 저가
        now_high_60 = round(float(now_close_1_60[0]["result"][-2]["high"]),4) #전봉의 고가
        h_close_60 = round(float(now_close_1_60[0]["result"][-2]["close"]),4) #전봉의 종가


        #60분봉 종가 기록
        if (time_m == 0 and time_s == 0) and h10 < now_high_60 and bb_u_60 < now_high_60:
            h1=h2
            h2=h3
            h3=h4
            h4=h5
            h5=h6
            h6=h7
            h7=h8
            h8=h9
            h9=h10
            h10=now_high_60
        
        elif (time_m == 0 and time_s == 0) and h10 > now_low_60  and bb_l_60 > now_low_60:
            l1=l2
            l2=l3
            l3=l4
            l4=l5
            l5=l6
            l6=l7
            l7=l8
            l8=l9
            l9=l10
            l10=now_low_60
        else:
            pass

        list_h=(h1,h2,h3,h4,h5,h6,h7,h8,h9,h10)
        list_l=(l1,l2,l3,l4,l5,l6,l7,l8,l9,l10)
        max_h=max(list_h)
        min_l=min(list_l)

        
        # 내 포지션 정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol=ticker).result()

        
        
        buy_size = int(my_infor[0]["result"][0]["size"])
        sell_size = int(abs(my_infor[0]["result"][1]["size"]))
        my_leverage = int(abs(my_infor[0]["result"][0]["leverage"]))
        

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

                
        # #자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))
        
        #아침 9시 총자산정산
        if time_h == 0 and buy_size == 0 and sell_size == 0 and my_usdt_d != my_usdt or my_usdt_d == 0:
            my_usdt_d = my_usdt
        else:
            pass
        


        #현재가조회(USDT)
        now_close_1 = client.LinearKline.LinearKline_get(symbol=ticker, interval="1", **{'from':unixtime-120}).result()
        now_close = round(float(now_close_1[0]["result"][-1]["close"]),sosu)

        # 위험수량 결정 자본금의 7배 이상      
        gty_d = round((my_usdt/now_close)*15,0)

        # 기본 수량 계산 - 반대포지션이 이수량되면 두배매수
        gty_c = round((my_usdt/now_close)*1,0)

        # 양매수 기준수량
        gty_b = round((my_usdt/now_close)*5,0)

        buy_size_d = round(buy_size-abs(sell_size),0)
        sell_size_d = round(abs(sell_size)-buy_size,0)
        size_abs = round(abs( sell_size-buy_size),0)


        #볼린저 상하단 격차
        bb_cc = float(round((bb_u-bb_l)/bb_u,2))

         #평단가격과 현재가와의 이격
        buy_entry_1 = 0
        sell_entry_1 = 0
        if buy_entry_price !=0 :
            buy_entry_1 =abs(round((buy_entry_price -now_close)/now_close,sosu))
        else:
            buy_entry_1 = 0
            
        if  sell_entry_price !=0 :
            sell_entry_1 = abs(round((sell_entry_price -now_close)/now_close,sosu))

        else:
            sell_entry_1 =0
        
        #볼린저상하단 보다 공매수공매도 평단이 위아래에았을때 대체, 평단과의 이격 1%이상 날때 볼린저 한틱 아래에서 매수시작
        # if bb_u <= sell_entry_price and sell_entry_price != 0 :
        #     bb_u = sell_entry_price
        # else:
        #     bb_u = bb_u

        # if bb_l >= buy_entry_price and buy_entry_price != 0 :
        #     bb_l = buy_entry_price
        # else:
        #     bb_l = bb_l
        
        
        
        
        #현재 수익율
        if (my_usdt-my_usdt_d)!=0:
            day_b=float((my_usdt-my_usdt_d)/my_usdt)
        else:
            day_b = 0 
        
        # 보유수량없는 시간에 수익율 계산됨
        if buy_size ==0 and sell_size == 0 and my_rev != day_b:
            my_rev = day_b
        else:
            pass
        #하루수익률이 1%를 넘으면 넘는 비율만큼 투자금비중을 줄인다
        lev1 = 50-my_leverage
        
        if my_rev < 0.005:
            rat_1=(3500*lev1)
        elif 0.005 < my_rev < 0.01:
            rat_1=(4000*lev1)
        elif my_rev > 0.01:
            rat_1=(my_rev*600000*lev1)
        else:
            rat_1=(3500*lev1)
        
        # 진입가격 결정,  (my_usdt/now_close)/4000
        
        if 500 > my_usdt:
            now_qty20 = 1 
        elif 500 < my_usdt < 10000:
            now_qty20 = (my_usdt/now_close)/rat_1
        elif 10000 < my_usdt:
            now_qty20 = (my_usdt/now_close)/rat_1
        else:
            pass
        #주문리셋 하는 수량단위
        if math.floor(now_qty20) < 1:
            ssall = 100
        elif math.floor(now_qty20) > 1:
            ssall=math.floor(now_qty20)*100

        

        

        

        #청산가격 계산 현재가의 0.15% 
        buy_j3 = round(now_close*0.005,4)
        #청산가격 수익율
        buy_j4 = round(now_close*0.01,4)
        #1%
        buy_j5 = round(now_close*0.01,4)

       
        

        # 평단 이격에 따라 매수량증가, math.floor():반내림, math.ceil:반올림
        if bb_u_30 < now_close or now_close< bb_l_30:
            fft=10000
        else:
            fft=1500

        if 0 < buy_entry_1 <= 0.005 :
            qb1=4.5
        elif 0.005 < buy_entry_1 <= 0.015:
            qb1=math.floor(buy_entry_1*1500)
        elif 0.015 < buy_entry_1 :
            qb1=buy_entry_1*fft
        else:
            qb1=4.5
        if 0 < sell_entry_1 <= 0.005 :
            ql1=4.5
        elif 0.005 < sell_entry_1 <= 0.015:
            ql1=math.floor(sell_entry_1*1500)
        elif 0.015 < sell_entry_1 :
            ql1=sell_entry_1*fft
        else:
            ql1=4.5

        #수량증가에따른 매수량 증가

        if size_abs < 300:
            qa=1
        elif size_abs >= 300:
            qa=1
        else:
            qa=1
        buy_stop =0
        sell_stop=0
        # 평단이 현재가와 수량이gty_c(1배레버수량)이상이면서 0.0002 이내로 들어와있으면 주문을 넣치않음
        if buy_entry_1 < (0.0001/now_close) and buy_entry_1 !=0 and gty_c*0.25 < buy_size:
            buy_stop=1
        elif buy_entry_1 < (0.0002/now_close) and buy_entry_1 !=0 and gty_c*0.5 < buy_size:
            buy_stop=1
        elif buy_entry_1 < (0.0003/now_close) and buy_entry_1 !=0 and gty_c*1 < buy_size:
            buy_stop=1
        elif buy_entry_1 < (0.0007/now_close) and buy_entry_1 !=0 and gty_c*10 < buy_size:
            buy_stop=1
        
        else:
            buy_stop=0
        if sell_entry_1 < (0.0001/now_close) and sell_entry_1 !=0 and gty_c*0.25 < sell_size:
            sell_stop=1
        elif sell_entry_1 < (0.0002/now_close) and sell_entry_1 !=0 and gty_c*0.5 < sell_size:
            sell_stop=1
        elif sell_entry_1 < (0.0003/now_close) and sell_entry_1 !=0 and gty_c*1 < sell_size:
            sell_stop=1
        elif sell_entry_1 < (0.0007/now_close) and sell_entry_1 !=0 and gty_c*10 < sell_size:
            sell_stop=1
        
        else:
            sell_stop=0
        buy_stop2 =0
        sell_stop2=0
        # # 양매수상태가 됏을때 그시점에서 1% 정도 등락이 생긴이후 부터 매수 시작 
        if buy_size > gty_b and sell_size > gty_b and size_abs==0  and buy_entry_1 < 0.01 :
            buy_stop2=1
        else:
            buy_stop2=0

        if buy_size > gty_b and sell_size > gty_b and size_abs==0  and sell_entry_1 < 0.01 :
            sell_stop2=1
        else:
            sell_stop2=0

        
         
        for i in range(0, 59):
            if time_s == i and my_leverage != 50 and my_stop==0:
                
                #주문하기    
                #공매수 주문
                for g in range(0, 100):
                    if now_close == round((bb_l) -(g*0.0001),4) and buy_size_d < gty_d and bb_l > now_close and buy_stop !=1 and sell_stop2 !=1 and (buy_entry_price > now_close or buy_entry_price == 0) and bb_l_60 > now_close:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=round(((g*qb1)+qa)*now_qty20,0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    #  현재가가 볼린저라인에 걸리면 1배레버리지 수량만큼사질때까지 주문넣어라
                    elif now_close == round((bb_l) -(g*0.0001),4) and buy_size_d < gty_d and bb_l == now_close and buy_size_d < gty_c and buy_stop !=1 and sell_stop2 !=1 and (buy_entry_price > now_close or buy_entry_price == 0) and bb_l_60 > now_close:
                        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=round(((g*qb1)+qa)*now_qty20,0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass
            
                

            
                    
                    
                
                
                #공매도 주문
                for g in range(0, 100):
                    if now_close == round((bb_u) +(g*0.0001),4) and sell_size_d < gty_d and bb_u < now_close and sell_stop !=1 and buy_stop2 !=1 and sell_entry_price < now_close and bb_u_60 < now_close:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=round(((g*ql1)+qa)*now_qty20,0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    #  현재가가 볼린저라인에 걸리면 1배레버리지 수량만큼사질때까지 주문넣어라
                    elif now_close == round((bb_u) +(g*0.0001),4) and sell_size_d < gty_d and bb_u == now_close and sell_size_d < gty_c and sell_stop !=1 and buy_stop2 !=1 and sell_entry_price < now_close and bb_u_60 < now_close:
                        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=round(((g*ql1)+qa)*now_qty20,0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
                    else:
                        pass
                    

               
 

            else:
                pass
            
            
        
            
            
                
        buy_size_d = round(buy_size-abs(sell_size),0)
        sell_size_d = round(abs(sell_size)-buy_size,0)
        size_abs = round(abs( sell_size-buy_size),0)
        if buy_size_d < 0:
            buy_size_d = 0
        else:
            buy_size_d = round(buy_size-abs(sell_size),0)
        
        if sell_size_d < 0:
            sell_size_d = 0
        else:
            sell_size_d = round(abs(sell_size)-buy_size,0)

        if sell_size > gty_c*5 and buy_size > gty_c*5 and size_abs < (gty_c/20):
            buy_size_e = round(sell_size*0.1,0)
            sell_size_e = round(buy_size*0.1,0)
        else:
            buy_size_e = 0
            sell_size_e = 0


        if buy_entry_price >= sell_entry_price :
            buy_ent = buy_entry_price
        elif buy_entry_price < sell_entry_price :
            buy_ent = sell_entry_price
        else:
            pass
        if sell_entry_price >= buy_entry_price :
            sell_ent = buy_entry_price
        elif buy_entry_price < sell_entry_price :
            sell_ent = sell_entry_price
        else:
            pass
        
        #5분 단위구분
        if time_m == 5 or time_m == 10 or time_m == 15  or time_m == 20 or time_m == 25 or time_m == 30 or time_m == 35 or time_m == 40 or time_m == 45 or time_m == 50 or time_m == 55 or time_m == 60:
            time_5m = 1
        else:
            time_5m = 0 

        #지정가 청산주문
        if time_m == 0 and (time_s == 0 or time_s == 1  or re_len > 99) and my_leverage != 50 and my_stop==0:
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소
        else:
            pass
        # if (buy_close_len > 1 or sell_close_len > 1) and (math.ceil(buy_size/100) == math.ceil(sell_size/100)) and my_leverage != 50 and my_stop==0:
        #     print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소
        # else:
        #     pass

        
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

        buy_close2=cls_sum[0]['Sell\x01']  #공매수청산주문수량
        sell_close2=cls_sum[0]['Buy\x01']  #공매도청산주문수량

        #매수수량이 1배~5배 사이면 매수량기준으로 매수수량 산정 햇으나 넘많이사지는거같아 1배의 반 적용 대신 투입비율(now_qty20)을 곱해줌
        if gty_c*5 > buy_size > gty_c:
            gty_buy= gty_c/2
        else:
            gty_buy= gty_c/2
        if gty_c*5 > sell_size > gty_c:
            gty_sell= gty_c/2
        else:
            gty_sell= gty_c/2


        # #1시간봉기준 볼린저이탈 이탈(4틱) 지정가매수주문넣기
        # if (bb_l > now_close ) and  buy_cls < 11 and buy_size ==0   and my_leverage != 50  and my_stop==0:
        #     print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소
        # else:
        #     pass
        # if (bb_u < now_close ) and  sell_cls < 11 and sell_size ==0   and my_leverage != 50  and my_stop==0:
        #     print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소
        # else:
        #     pass

        if buy_cls == 0  and my_leverage != 50  and my_stop==0 and buy_size < (gty_c*15) and bb_l_60 > now_close:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(1000,0),price =round(now_close-(0.0005),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(2000,0),price =round(now_close-(0.0006),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(3000,0),price =round(now_close-(0.0007),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(4000,0),price =round(now_close-(0.0009),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(gty_buy/10*now_qty20,0),price =round(now_close-(buy_j5+0.0004),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(gty_buy/10*now_qty20,0),price =round(now_close-(buy_j5+0.0005),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(gty_buy/10*now_qty20,0),price =round(now_close-(buy_j5+0.0006),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(gty_buy/9*now_qty20,0),price =round(now_close-(buy_j5+0.0008),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(gty_buy/8*now_qty20,0),price =round(now_close-(buy_j5+0.0015),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(gty_buy/7*now_qty20,0),price =round(now_close-(buy_j5+0.0020),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round(gty_buy/6*now_qty20,0),price =round(now_close-(buy_j5+0.0025),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

            

        elif sell_cls == 0  and my_leverage != 50 and my_stop==0 and sell_size < (gty_c*15) and bb_u_60 < now_close:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(1000,0),price =round(now_close+(0.0005),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(2000,0),price =round(now_close+(0.0006),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(3000,0),price =round(now_close+(0.0007),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(4000,0),price =round(now_close+(0.0009),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(gty_sell/10*now_qty20,0),price =round(now_close+(buy_j5+0.0004),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(gty_sell/10*now_qty20,0),price =round(now_close+(buy_j5+0.0005),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(gty_sell/10*now_qty20,0),price =round(now_close+(buy_j5+0.0006),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(gty_sell/9*now_qty20,0),price =round(now_close+(buy_j5+0.0008),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(gty_sell/8*now_qty20,0),price =round(now_close+(buy_j5+0.0015),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(gty_sell/7*now_qty20,0),price =round(now_close+(buy_j5+0.0020),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round(gty_sell/6*now_qty20,0),price =round(now_close+(buy_j5+0.0025),4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        else:
            pass
        
        #지정가 청산주문
        if buy_size_d < gty_c and math.ceil((buy_size_d)/ssall) != math.ceil(buy_close2/ssall) and buy_size > sell_size and my_leverage != 50 and my_stop==0 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=buy_size_d-buy_close2,price = round(buy_entry_price+buy_j4,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        
        elif buy_size_d >= gty_c and buy_size > sell_size and my_leverage != 50 and my_stop==0 and buy_entry_price < now_close and sell_cls==0 and math.ceil((buy_size_d)/ssall) != math.ceil(buy_close2/ssall):
                     
           
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d)/10,0) ,price =round(now_close+0.0000,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0001,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0002,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0003,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0004,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0005,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0006,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0007,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0008,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0009,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size_d-buy_close2)/10,0) ,price =round(now_close+0.0010,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        
        
        else:
            pass

        if sell_size_d < gty_c  and math.ceil((sell_size_d)/ssall) != math.ceil(sell_close2/ssall)  and buy_size < sell_size  and my_leverage != 50 and my_stop==0:                
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=sell_size_d-sell_close2,price = round(sell_entry_price-buy_j4,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
        
       
        elif sell_size_d >= gty_c  and buy_size < sell_size and my_leverage != 50 and my_stop==0 and sell_entry_price > now_close and buy_cls==0 and math.ceil((sell_size_d)/ssall) != math.ceil(sell_close2/ssall)  : 
            

            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d)/10,0) ,price =round(now_close-0.0000,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0001,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0002,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0003,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0004,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0005,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0006,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0007,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0008,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0009,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size_d-sell_close2)/10,0) ,price =round(now_close-0.0010,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

        
                
        else:
            pass

        if buy_size ==0 and sell_size == 0:
             my_stop=0
        else:
            pass

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

        buy_close2=cls_sum[0]['Sell\x01']  #공매수청산주문수량
        sell_close2=cls_sum[0]['Buy\x01']  #공매도청산주문수량
        

        
    # 수량이 차면 양매수를 걸어라
        if buy_size_d > gty_c*2 and my_leverage != 50 and my_stop==0:
             # 1배이상 싸이면 반대포지션을 지정가로 양매수 걸어라 초당1배수량제외한 나머지 차이의 20분에1을 걸어라
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=round((buy_size_d)/20,0) ,price =round(now_close+0.0001,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
           
         
        elif sell_size_d > gty_c*2 and my_leverage != 50 and my_stop==0:
            # 1배이상 싸이면 반대포지션을 지정가로 양매수 걸어라 초당1배수량제외한 나머지 차이의 20분에1을 걸어라
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=round((sell_size_d)/20,0) ,price =round(now_close+0.0001,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
     

        else:
            pass

        

        # 매수수량이 25배 이상이면 양매수를 걸고 모든 매매를 멈춰라
        if buy_size > gty_c*15 and buy_size > sell_size and my_leverage != 50 and my_stop==0:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=round((buy_size-sell_size),0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=round((gty_c/2),0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            my_stop=1
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소

            
              
        else:
            pass
        if sell_size > gty_c*15 and buy_size < sell_size and my_leverage != 50 and my_stop==0:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=round((sell_size-buy_size),0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            # print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=round((gty_c/2),0) ,price =now_close,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
            my_stop=1
            print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소
        else:
            pass

        # #양매수후 떨어지는 방향의 포지션에 0.5배(gty_c/2) 매수를 걸은것 수익나서 수익이 +-0 되는가격에 양매수주문넣기
        # if my_stop==1 and sell_size > buy_size and buy_close == 0:
        #     close_a_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*sell_size #수익금액 계산식
        #     close_a_1_b0 = 
            
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((sell_size-buy_size),0),price = round(buy_entry_price+buy_j4,4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
            
 



        #  #15배 양매도 시 모든주문 스탑후 양매도 단계별 청산주문넣기
        # if my_stop==1 and bb_u_30 > now_close > bb_l_30 and time_s == 0 :
        #     print(client.LinearOrder.LinearOrder_cancelAll(symbol=ticker).result()) # 모든주문취소
        # else:
        #     pass
        # if  my_stop==1 and bb_u_30 < now_close and buy_close==0:
            
            
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*3.0),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*3.2),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*3.4),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*3.6),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*3.8),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*4.0),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*4.2),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*4.4),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*4.6),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=round((buy_size)/100,0) ,price =round(now_close+(buy_j5*4.8),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())


            
        # else:
        #     pass

        # if  my_stop==1 and bb_l_30 > now_close and buy_close==0:
            
            
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*3.0),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*3.2),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*3.4),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*3.6),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*3.8),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*4.0),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*4.2),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*4.4),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*4.6),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=round((sell_size)/100,0) ,price =round(now_close-(buy_j5*4.8),4),time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())

                
        # else:
        #     pass




         #양매수시 청산주문 계산(같은수량팔았을때 수익률)
        #수익율 계산 close_sb_3:수익율

        if buy_size < sell_size and buy_size != 0 and sell_size != 0:
            close_all_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*buy_size #수익금액 계산식
            close_all_2 = (buy_entry_price*buy_size) + (sell_entry_price*buy_size)#투입금액 계산식
            close_all_3 = round(close_all_1 / close_all_2,5) #수익률 계산식
            close_b_1 = buy_size
            close_s_1 = buy_size
        
        elif buy_size >= sell_size and buy_size != 0 and sell_size != 0:
            close_all_1 = ((now_close - buy_entry_price)*sell_size) +  (( sell_entry_price - now_close)*sell_size)
            close_all_2 = (buy_entry_price*sell_size) + (sell_entry_price*sell_size)
            close_all_3 = round(close_all_1 / close_all_2,5) #수익률 계산식
            close_b_1 = sell_size
            close_s_1 = sell_size

        else:
            close_all_3=0
            close_s_1 = 0
            close_b_1 = 0

        #양매수시 청산주문 계산(모두 팔았을때 수익률)
        #수익율 계산 close_sb_3:수익율

        if buy_size != 0 and sell_size != 0 and (buy_size+sell_size)>(gty_c/5):
            close_a_1 = (now_close - buy_entry_price)*buy_size +  (sell_entry_price - now_close)*sell_size #수익금액 계산식
            close_a_2 = (buy_entry_price*buy_size) + (sell_entry_price*sell_size)#투입금액 계산식
            close_a_3 = round(close_a_1 / close_a_2,5) #수익률 계산식
            close_b_2 = buy_size
            close_s_2 = sell_size
        
        else:
            close_a_3=0
            close_s_2 = 0
            close_b_2 = 0

        #=================같은수량 동시청산시 수익나는 시점에 청산=============
         #양매수 시장가 청산하기    0.01= 1%수익
        if close_all_3 >= 0.005 and buy_size != 0 and sell_size != 0 and my_leverage != 50 and my_stop==0:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=close_b_1,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=close_s_1,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            if close_b_1 > gty_c:
                my_tep1=1
            else:
                pass
        else:
            pass
        #==============================================================

        # =================모든수량 동시청산시 수익나는 시점에 청산후 리셋=============
        #  양매수 시장가 청산하기    0.01= 1%수익
        if close_a_3 >= 0.005 and buy_size != 0 and sell_size != 0 and my_leverage != 50 :
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=close_b_2,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=close_s_2,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            my_stop=0
            
        else:
            pass
        #==============================================================

        # #=================한쪽포지션만 남았을때 수익나면 수익실현후 리셋=============================================
        # if buy_size > 0 and sell_size == 0 and round(buy_entry_price+buy_j3,4) <= now_close and my_leverage != 50 and my_stop==0 and my_tep1==0:
        #     print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Market",qty=buy_size,price = buy_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
           
        # else:
        #     pass
        
        # if buy_size ==0  and sell_size > 0  and round(sell_entry_price-buy_j3,4) >= now_close and my_leverage != 50 and my_stop==0 and my_tep1==0:
        #     print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Market",qty=sell_size,price = sell_entry_price,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            
        # else:
        #     pass
        #==============================================================

        #분봉 지정가매수주문넣기
        
        # #==============================================================================30분봉 기준 지정가 넣기==================================================
        # #현재가의 1%, 0.5%
        # yj1 = float(round(now_close *0.01,sosu))
        # yj05 = float(round(now_close *0.006,sosu))
        
        # #현재가 3틱위아래에서 주문시 j05(0.6%)이격을유지하기위한 매수수량구하기
        # du_1=((((now_close+0.0001)-sell_entry_price)-yj1)/(now_close+0.0001))*100
        # dl_1=((((now_close-0.0001)-buy_entry_price)-yj1)/(now_close-0.0001))*100
        # if du_1 < 0:
        #     du_1 = 0
        # else:
        #     du_1=((((now_close+0.0001)-sell_entry_price)-yj1)/(now_close+0.0001))*100
        # if dl_1 < 0:
        #     dl_1 = 0
        # else:
        #     dl_1=((((now_close-0.0001)-buy_entry_price)-yj1)/(now_close-0.0001))*100

        # #한틱 이격 줄이기위한 수량구하기
        # teg_1 = (0.0001/now_close)*100
        # #6틱 이격 줄이기위한 수량구하기
        # teg_2 = (0.0006/now_close)*100

        # #공매도수량
        # qty_0=round(sell_size_d*du_1,0)
        # #공매수수량
        # qty_10=round(buy_size_d*dl_1,0)
        

        # # 30분봉 1%이상 이탈시 0.6%이격을 유지하기 위한 지정가매수주문넣기
        # if now_close >= round(bb_u_30+yj1,4) and sell_cls == 0 and qty_0 != 0 and sell_entry_1 > 0.015:
        #    print(client.LinearOrder.LinearOrder_new(side="Sell",symbol=ticker,order_type="Limit",qty=qty_0,price = round(now_close+0.0001,4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        # else:
        #    pass
        
        # if now_close <= round(bb_l_30-yj1,4) and buy_cls == 0 and qty_10 != 0 and buy_entry_1 > 0.015:
        #    print(client.LinearOrder.LinearOrder_new(side="Buy",symbol=ticker,order_type="Limit",qty=qty_10,price = round(now_close-0.0001,4),time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        # else:
        #    pass
        #  # ===========================================================================================================================================================
        
          
        print("시간초            :",time_s)
        print("레버리지            :",my_leverage)
        print("볼린저상단        :",bb_u)
        print("볼린저하단        :",bb_l)
        print("현재가            :",now_close)
        print("모두팔때수익률     :",close_a_3)
        print("동수량팔때수익률   :",close_all_3)
        print("초기수량          :",round(((1*qb1)+qa)*now_qty20,0))
        print("투입비율          :",now_qty20)
        print("양매수발동수량     :",gty_b)
        print("1배수량           :",gty_c)
        print("15배수량           :",gty_c*15)
        print("buy평단이격       :",buy_entry_1)
        print("sell평단이격      :",sell_entry_1)
        print("공매수수량        :",buy_size)
        print("공매도수량        :",sell_size)
        print("공매수청산주문수량 :",buy_close)
        print("양매수스탑 1이면스탑 :",my_stop)
        print("동시청산후 털기   :",my_tep1)
        # print("오늘수익율        :",day_b)
        print("9시or초기정산금        :",my_usdt_d)
        
        print(h1,h2,h3,h4,h5,h6,h7,h8,h9,h10)
        print(l1,l2,l3,l4,l5,l6,l7,l8,l9,l10)
        print(max_h)
        print(min_l)

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