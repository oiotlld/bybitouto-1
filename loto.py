from playwright.sync_api import Playwright, sync_playwright
import schedule
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

# 동행복권 아이디와 패스워드를 설정
USER_ID = 'oiotlld'
USER_PW = 'dldnska0075!'

# 구매 개수를 설정
COUNT = 5

while True:
    now = datetime.utcnow()
    time_d = int(now.day) #날짜 카운트
    time_h = int(now.hour) #시간 카운트
    time_s = int(now.second) #초 카운트
    time_m = int(now.minute) #분 카운트

    if (time_d == 7 or time_d == 14 or time_d == 21 or time_d == 28) and time_h==0 and time_m==0 and time_s==0 :
        def run(playwright: Playwright) -> None:

            # chrome 브라우저를 실행
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()

            # Open new page
            page = context.new_page()

            # Go to https://dhlottery.co.kr/user.do?method=login
            page.goto("https://dhlottery.co.kr/user.do?method=login")

            # Click [placeholder="아이디"]
            page.click("[placeholder=\"아이디\"]")

            # Fill [placeholder="아이디"]
            page.fill("[placeholder=\"아이디\"]", USER_ID)

            # Press Tab
            page.press("[placeholder=\"아이디\"]", "Tab")

            # Fill [placeholder="비밀번호"]
            page.fill("[placeholder=\"비밀번호\"]", USER_PW)

            # Press Tab
            page.press("[placeholder=\"비밀번호\"]", "Tab")

            # Press Enter
            # with page.expect_navigation(url="https://ol.dhlottery.co.kr/olotto/game/game645.do"):
            with page.expect_navigation():
                page.press("form[name=\"jform\"] >> text=로그인", "Enter")

            page.goto(url="https://ol.dhlottery.co.kr/olotto/game/game645.do")

            # ---------------------------------------------
            # 사용자 지정 번호 입력 
            # 여기서는 9와 25를 입력하고 나머지는 자동선택함
            # ---------------------------------------------

            # Click label:has-text("2")
            page.click("label:has-text(\"9\")")

            # Click label:has-text("24")
            page.click("label:has-text(\"25\")")

            # 나머지 숫자는 자동 선택함
            # Click text=자동선택
            page.click("text=자동선택")

            # 구매할 개수를 선택
            # Select 5
            page.select_option("select", str(COUNT))

            # Click text=확인
            page.click("text=확인")

            # Click input:has-text("구매하기")
            page.click("input:has-text(\"구매하기\")")

            time.sleep(2)
            # Click text=확인 취소 >> input[type="button"]   
            page.click("text=확인 취소 >> input[type=\"button\"]")

            # Click input[name="closeLayer"]
            page.click("input[name=\"closeLayer\"]")
            # assert page.url == "https://el.dhlottery.co.kr/game/TotalGame.jsp?LottoId=LO40"

            # ---------------------
            context.close()
            browser.close()


        with sync_playwright() as playwright:
            run(playwright)

    time.sleep(1)
