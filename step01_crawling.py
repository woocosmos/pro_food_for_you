import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import math

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('../../chromedriver', options=options)
url = 'https://www.yogiyo.co.kr/mobile/#/'
driver.get(url)

# 검색입력필드와 검색버튼 가져오기
input_field = driver.find_element_by_xpath('//*[@id="search"]/div/form/input')
search_btn = driver.find_element_by_xpath('//*[@id="button_search_address"]/button[2]')
# 입력필드에 주소 입력
edu_place = '서울 중구 삼일대로2길 70'
# 입력 필드 초기화
input_field.clear()
# 입력 필드에 값 입력
input_field.send_keys(edu_place)

# search_btn.click()
# select search option
input_field.send_keys(Keys.RETURN) # Keys.RETURN = ENTER / 텍스트창에서 key를 보내야 한다
time.sleep(3)
driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[2]/div/select/option[4]').click()
time.sleep(3)

# 데이터 저장 리스트
popular_store_title = []
popular_menu_title = []
popular_menu_img = []

review_store_title = []
review_reviews = []

info_store_title = []
info_store_operation_hours = []
into_address = []
info_min_order_amount = []

# 시작 지점(1321번째 리스트)으로 이동
# for i in range(1,23):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(1)

for a in range(1,13):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

print('지금부터 시작')


for r in range(12, 23):
    # 업체 상세 페이지로 진입
    for u in range(60 * (r - 1) + 1, 60 * r + 1):
        try:
            store_xpath = '//*[@id="content"]/div/div[5]/div/div/div[{}]'.format(u)
            driver.find_element_by_xpath(store_xpath).click()
            print('store', u)
            # 업체 상세 페이지로 진입
            time.sleep(2)

            store_review_count = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span')
            review_count = int(store_review_count.text)

            if review_count == 0:
                print('리뷰가 0개, drop')
                driver.back()
                time.sleep(2)
            else:
                # 0. 스토어 이름 지정
                store_name = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/span').text
                # 1. 메뉴탭 : 인기 메뉴 가져오기
                try:
                    for i in range(1, 3):  # range 값 수정 시 가져올 수 있는 메뉴 개수 변경
                        xpath_title = '//*[@id="menu"]/div/div[2]/div[2]/div/ul/li[{}]/table/tbody/tr/td[1]/div[2]'.format(i)
                        xpath_img = '//*[@id="menu"]/div/div[2]/div[2]/div/ul/li[{}]/table/tbody/tr/td[2]/div'.format(i)
                        menu_title_obj = driver.find_element_by_xpath(xpath_title)
                        menu_img_obj = driver.find_element_by_xpath(xpath_img)

                        menu_title = menu_title_obj.text
                        menu_img = menu_img_obj.get_attribute('style').split(' url("')[1].replace('"),', '')

                        popular_store_title.append(store_name)
                        popular_menu_title.append(menu_title)
                        popular_menu_img.append(menu_img)
                except:
                    print('no more than 2 menu')
                print('end save popular menu')

                # 2. 정보탭 : 업체 정보 가져오기
                store_info_tab = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[3]/a')
                store_info_tab.click()
                time.sleep(2)

                try:
                    # 정보 가져오기
                    operation_hours = driver.find_element_by_xpath('//*[@id="info"]/div[2]/p[1]/span').text
                    address = driver.find_element_by_xpath('//*[@id="info"]/div[2]/p[3]/span').text
                    min_order_amount = driver.find_element_by_xpath('//*[@id="info"]/div[3]/p[1]/span').text
                    # 최소가격 숫자로 변경
                    min_order_amount = min_order_amount.replace(',', '')
                    min_order_amount = int(min_order_amount.replace('원', ''))

                    info_store_title.append(store_name)
                    info_store_operation_hours.append(operation_hours)
                    into_address.append(address)
                    info_min_order_amount.append(min_order_amount)
                except:
                    print("정보가 없습니다")

                print('end save store info')

                # 3. 리뷰탭 : 리뷰 긁어오기
                store_review_tab = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a')
                store_review_tab.click()

                if review_count >= 100:
                    review_count = 100

                click_count = review_count // 10
                print('클릭 수 : ', click_count)
                print('리뷰 개수 : ', review_count)

                try:
                    if click_count != 0:
                        for i in range(1, click_count + 1):
                            time.sleep(3)
                            btn_more = driver.find_element_by_class_name('btn-more')
                            btn_more.click()
                            print('더보기 클릭 : ', i)
                except:
                    print('end_of_page(더보기 없다)')

                # 리뷰 가져오기
                for j in range(2, review_count+1):
                    review_obj = driver.find_element_by_xpath('//*[@id="review"]/li[{}]/p'.format(j))
                    review = review_obj.text
                    review_store_title.append(store_name)
                    review_reviews.append(review)
                print('end save store review')

                time.sleep(2)
                driver.back()
                time.sleep(2)

            while (len(driver.find_elements_by_xpath('//*[@id="content"]/div/div[5]/div/div/div')) <= u):
                print(len(driver.find_elements_by_xpath('//*[@id="content"]/div/div[5]/div/div/div')))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
        except:
            print('end of list')
            break

time.sleep(3)
df_popular = pd.DataFrame({'title':popular_store_title, 'menu':popular_menu_title,'menu_img':popular_menu_img})
df_review = pd.DataFrame({'title':review_store_title, 'review':review_reviews})
df_info = pd.DataFrame({'title':info_store_title, 'hour':info_store_operation_hours,
                        'min_order':info_min_order_amount, 'address':into_address})

df_popular.to_csv('./yoggiyo_popular_menu.csv')
df_review.to_csv('./yoggiyo_review.csv')
df_info.to_csv('./yoggiyo_store.csv')