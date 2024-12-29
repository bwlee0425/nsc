import os
import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window()

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 2. 조회 항목 초기화 (체크되어 있는 항목 체크 해제)

checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면?
        checkbox.click() # 클릭 (체크 해제)

# 3. 조회 항목 설정 (원하는 항목)
#items_to_select = ['영업이익', '자산총계', '매출액']
items_to_select = ['시가', '고가', '저가']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모엘리먼트 찾기
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text) # 이름 확인
    if label.text in items_to_select: # 선택항목
        checkbox.click() # 체크

# 4. 적용하기 버튼 클릭
# 적용하기 href 를 XPath 로 카피 후
# btn_apply = browser.find_element(By, XPATH, '//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]')
# 또는
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40): # 1 이상 40 미만 페이지 반복
    # 사전 작업 : 페이지 이동
    browser.get(url +str(idx)) # http://naver.com....& page=2

    # 5. 데이터 추출
    html_string = browser.page_source
    html_io = StringIO(html_string) # browser.page_source 에서 가져온 html 문자열을 StringIO 로 감싸기
    # 이것때문에 : 보시는 경고는 pandas.read_html 함수를 사용할 때 리터럴 HTML 문자열을 직접 전달하는 것이 더 이상 권장되지 않으며, 향후 버전에서 제거될 것이라는 내용을 담고 있습니다. 따라서 HTML 문자열을 StringIO 객체로 감싸서 사용하는 것이 필요합니다.
    #df = pd.read_html(html_io)
    # len(df)
    # df[0]
    # df[1]
    # df[2]
    df = pd.read_html(html_io)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0: # 더 이상 가져올 데이터가 없으면?
        break

    # 6. 파일 저장
    f_name = 'sise.csv'
    if os.path.exists(f_name): # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없다면? 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit() # 브라우저 종료