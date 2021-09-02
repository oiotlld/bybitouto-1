import bybit
import pandas as pd 
from pybit import HTTP
import time
from datetime import datetime
import calendar
import numpy
from urllib.request import urlopen
from urllib.error import HTTPError

client = bybit.bybit(test=False, api_key="8PolF3iULIcIQdDUPS", api_secret="cvdty5N2XgvRsAQccbW61jziXti2Yxlj7xEz")
apiKey='8PolF3iULIcIQdDUPS'
apisecret='cvdty5N2XgvRsAQccbW61jziXti2Yxlj7xEz'
# session = HTTP(
#     endpoint='https://api.bybit.com', 
#     api_key="8PolF3iULIcIQdDUPS",
#     api_secret="cvdty5N2XgvRsAQccbW61jziXti2Yxlj7xEz")
    

    
num=1

while True:
    try:
        # 분봉가저오기
        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())
        # 300초단위로 20번 === 5분봉, 20개봉 가저오기
        since = unixtime - 60*20
        response=client.LinearKline.LinearKline_get(symbol="BTCUSDT", interval="1", **{'from':since}).result()
        
        close_0= float(response[0]["result"][0]["close"])
        close_1= float(response[0]["result"][1]["close"])
        close_2= float(response[0]["result"][2]["close"])
        close_3= float(response[0]["result"][3]["close"])
        close_4= float(response[0]["result"][4]["close"])
        close_5= float(response[0]["result"][5]["close"])
        close_6= float(response[0]["result"][6]["close"])
        close_7= float(response[0]["result"][7]["close"])
        close_8= float(response[0]["result"][8]["close"])
        close_9= float(response[0]["result"][9]["close"])
        close_10= float(response[0]["result"][10]["close"])
        close_11= float(response[0]["result"][11]["close"])
        close_12= float(response[0]["result"][12]["close"])
        close_13= float(response[0]["result"][13]["close"])
        close_14= float(response[0]["result"][14]["close"])
        close_15= float(response[0]["result"][15]["close"])
        close_16= float(response[0]["result"][16]["close"])
        close_17= float(response[0]["result"][17]["close"])
        close_18= float(response[0]["result"][18]["close"])
        close_19= float(response[0]["result"][19]["close"])
        
        close_list = (close_0,close_1,close_2,close_3,close_4,close_5,close_6,close_7,close_8,close_9,close_10,close_11,close_12,close_13,close_14,close_15,close_16,close_17,close_18,close_19)
        average = numpy.mean(close_list)
        std = numpy.std(close_list)
        bb_u=average + std*2
        bb_l=average - std*2

        # 내주문정보가저오기
        my_infor=client.LinearPositions.LinearPositions_myPosition(symbol="BTCUSDT").result()

        buy_size = float(my_infor[0]["result"][0]["size"])
        sell_size = float(my_infor[0]["result"][1]["size"])

        #각 포지션 평균단가 가저오기
        buy_entry_price = round(float(my_infor[0]["result"][0]["entry_price"]),2)
        sell_entry_price = round(float(my_infor[0]["result"][1]["entry_price"]),2)

        # print(bb_u)
        # print(bb_l)
        # print(buy_entry_price)
        # print(sell_size)
        # print(sell_entry_price)

        
        #자산조회
        my_equity = client.Wallet.Wallet_getBalance(coin="USDT").result()
        my_usdt = float((my_equity[0]["result"]["USDT"]["equity"]))

        #현재가조회
        now_btc = client.Market.Market_orderbook(symbol="BTCUSD").result()
        now_price = float(now_btc[0]["result"][0]["price"])
        #현재가조회(USDT)
        now_close = client.LinearKline.LinearKline_get(symbol="BTCUSDT", interval="w", **{'from':1581231260}).result()
        now_close = float(now_close[0]["result"][-1]["close"])

        

        # 진입가격 결정, 매수매도 평단가가 볼리저 상하단을 이탈하면 진입수량 2배, 평단가가 현재가와 1%이상 벌어지면 3배 진입
        now_qty = round(my_usdt/now_price,2)
        now_qty20 = now_qty/20

        if bb_u < buy_entry_price  > 0 and buy_entry_price*1.01 < now_close:
            my_qty_buy = now_qty20*3        
        elif bb_u < buy_entry_price  > 0:
            my_qty_buy = now_qty20*2
        else:
            my_qty_buy = now_qty20

        if bb_l > sell_entry_price > 0 and sell_entry_price*0.99 > now_close:
            my_qty_sell = now_qty20*3
        elif bb_l > sell_entry_price > 0:
            my_qty_sell = now_qty20*2    
        else:
            my_qty_sell = now_qty20
        
                
        # # 모든주문취소
        print(client.LinearOrder.LinearOrder_cancelAll(symbol="BTCUSDT").result())

        # # 매수 현재가
        # # 현재가가 볼린저 상하단에 있을때 매수매도신호가 들어가면 볼린저 상단부터 현재가까지 시장가로 채결되는것을 방지하기위해 현재가가 볼린저상하단이탈한상태에서는 현재가를 기준으로 매수매도 주문을 넣는다
        if bb_l > now_close:
            a = now_close
        else:
            a = round(float(bb_l), 2)

        #매도 현재가
        if bb_u < now_close:
            a_1 = now_close
        else:
            a_1 = round(float(bb_u), 2)

        b = a - 10 
        c = a - 40 
        d = a - 60 
        e = a - 80 
        f = a - 100 
        g = a - 120 
        h = a - 150 
        i = a - 200 
        j = a - 250 
        k = a - 300 
        l = a - 500 
        n = a - 1000 
        m = a - 1500 
        o = a - 2000 
        p = a - 2500 
        q = a - 3000

        b_1 = (a_1 + 10)
        c_1 = (a_1 + 40)
        d_1 = (a_1 + 60)
        e_1 = (a_1 + 80)
        f_1 = (a_1 + 100)
        g_1 = (a_1 + 120)
        h_1 = (a_1 + 150)
        i_1 = (a_1 + 200)
        j_1 = (a_1 + 250)
        k_1 = (a_1 + 300)
        l_1 = (a_1 + 500)
        n_1 = (a_1 + 1000)
        m_1 = (a_1 + 1500)
        o_1 = (a_1 + 2000)
        p_1 = (a_1 + 2500)
        q_1 = (a_1 + 3000)

        # print(bb_u)
        # print(bb_l)
        # # # # #매수주문 Buy 첫글자"B"는 대문자여야함
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (b) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (c) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (d) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (e) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (f) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (g) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (h) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (i) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (j) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (k) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy,price = (l) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy*10,price = (n) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy*10,price = (m) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy*20,price = (o) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy*25,price = (p) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=my_qty_buy*30,price = (q) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

        # #매도주문하기 포스트온니없음
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (b_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (c_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (d_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (e_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (f_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (g_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (h_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (i_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (j_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (k_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell,price = (l_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell*10,price = (n_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell*10,price = (m_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell*20,price = (o_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell*25,price = (p_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
        print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=my_qty_sell*30,price = (q_1) ,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())

        
        # #청산하기
        my_clearing = buy_size * sell_size
        qty_c = abs(buy_size - sell_size)
        if my_clearing == 0:
            qty_clearing=0
            
        elif buy_size >= sell_size:
            qty_clearing = round(buy_size - qty_c,3)
            print("공매수가많을때")
            print(qty_clearing)
        elif buy_size <= sell_size:
            qty_clearing = round(sell_size - qty_c,3)   
            print("공매도가많을때")
            print(qty_clearing)
        else:
            pass
        # 양매수 포지션 청산, qty_clearing:양매수청산수량, now_qty:투자금(비트로환산한값),now_close:현재가,buy_entry_price:매수평단,sell_entry_price:매도평단
        
        if qty_clearing > now_qty and my_clearing !=0 and buy_entry_price < now_close < sell_entry_price and buy_entry_price+50 < sell_entry_price-50:   
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Market",qty=qty_clearing,price = sell_entry_price-10,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Market",qty=qty_clearing,price = buy_entry_price-10,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())    
            print("매도청산신호")
        else:
            print("매도청산신호없음")
        

            
        # 매수수량이 자산의 5배보다 크면 평균단가에 보유물량 절반을 지정가로 청산주문
        if buy_size > now_qty*5:
            print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=round(buy_size/2,3),price = buy_entry_price ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass
        
        # 매도수량이 자산의 5배보다 크면 평균단가에 보유물량 절반을 지정가로 청산주문
        if sell_size > now_qty*5:
            print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="BTCUSDT",order_type="Limit",qty=round(sell_size/2,3),price = sell_entry_price ,time_in_force="GoodTillCancel",reduce_only=True, close_on_trigger=False).result())
        else:
            pass
        
        print(now_qty)
        print(now_close)
        print(buy_size)
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
    except Exception as erro2: 
        print(erro2)
    pass

        
    time.sleep(30)

