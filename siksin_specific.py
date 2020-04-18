from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys

import time

url = 'https://www.siksinhot.com/taste'
driver = webdriver.Chrome('D:/finalproject/chromedriver.exe')
client = MongoClient('localhost',27017)
db = client.dbsparta
driver.get(url)
driver.implicitly_wait(1)

driver.find_element_by_xpath('/html/body/div/div/div/div[3]/div/div/div/div[1]/div[1]/div/div/a').click()
#먼저 맛집 지역 클릭


def next_low_region(end_num):
    low_text_front = '/html/body/div/div/div/div[3]/div/div/div/div['
    middle_num = 9
    low_text_middle = ']/div[2]/div[2]/div/div/div[2]/ul/li['
    low_text_end = ']/a'
    try:
        driver.find_element_by_class_name("area_recommand_tag")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_gray01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white02")
    except:
        middle_num -= 1
    return low_text_front+str(middle_num)+low_text_middle+str(end_num)+low_text_end

def next_high_region(end_num):
    high_text_front = '/html/body/div/div/div/div[3]/div/div/div/div['
    middle_num = 9
    high_text_middle = ']/div[2]/div[2]/div/div/div[1]/ul/li['
    high_text_end = ']/a'
    try:
        driver.find_element_by_class_name("area_recommand_tag")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_gray01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white01")
    except:
        middle_num -= 1
    try:
        driver.find_element_by_class_name("sub_cont_white02")
    except:
        middle_num -= 1
    return high_text_front+str(middle_num)+high_text_middle+str(end_num)+high_text_end

def get_shop_data():
    gogi_upper_front = "/html/body/div/div/div/div[3]/div/div/div/div[5]/div[1]/div/div[1]/div[1]/div["
    gogi_upper_back_name = ']/h4'

    gogi_info1 = ['매장소개', '전화번호', '주소']
    gogi_shop_data = []
    gogi_shop_data.append({'업종': driver.find_element_by_xpath(
        "/html/body/div/div/div/div[3]/div/div/div/div[5]/div[1]/div/div[1]/div[1]/p").text})
    for gogi_upper_num in range(1, 8):
        try:
            info = driver.find_element_by_xpath(gogi_upper_front + str(gogi_upper_num) + gogi_upper_back_name).text
        except:
            break
        if info == gogi_info1[0]:
            gogi_shop_data.append(
                {'매장소개': driver.find_element_by_xpath(gogi_upper_front + str(gogi_upper_num) + ']/p').text})
        elif info == gogi_info1[1]:
            gogi_shop_data.append(
                {'전화번호': driver.find_element_by_xpath(gogi_upper_front + str(gogi_upper_num) + ']/p/a/span').text})
        elif info == gogi_info1[2]:
            gogi_shop_data.append(
                {'주소': driver.find_element_by_xpath(gogi_upper_front + str(gogi_upper_num) + ']/p/a[1]').text})

    shop_work_front = "/html/body/div/div/div/div[3]/div/div/div/div[5]/div[1]/div/div[1]/ul/li["
    shop_work_day = "]/span"
    shop_work_time = "]/em/label"
    worktime_list = []
    for work in range(1, 10):
        try:
            workday = driver.find_element_by_xpath(shop_work_front + str(work) + shop_work_day).text
            worktime = driver.find_element_by_xpath(shop_work_front + str(work) + shop_work_time).text
        except:
            break
        worktime_list.append({workday: worktime})
    gogi_shop_data.append({"영업시간":worktime_list})

    gogi_down_front = "/html/body/div/div/div/div[3]/div/div/div/div[5]/div[1]/div/div[1]/div["
    gogi_down_back = ']/h4'
    down_infolist = ['편의/시설 정보','대표메뉴','음료/주류']
    shop_menu_info=[]
    for div_num in range(1,11):
        try:
            shop_inner_info = driver.find_element_by_xpath(gogi_down_front+str(div_num)+gogi_down_back).text
        except:
            shop_inner_info = ''
            pass
        if shop_inner_info == down_infolist[1]:
            for menu in range (1,10):
                try:
                    menu_name = driver.find_element_by_xpath(gogi_down_front+str(div_num)+"]/ul/li["+str(menu)+"]/span").text
                    menu_name = menu_name.replace(".",",")
                except:
                    break
                gogi_price = ''
                for price in range (1,3):
                    try:
                        menu_price = driver.find_element_by_xpath(gogi_down_front+str(div_num)+"]/ul/li["+str(menu)+"]/p/span/em/label["+str(price)+"]").text
                    except:
                        break
                    gogi_price +=menu_price
                shop_menu_info.append({menu_name : gogi_price})
    gogi_shop_data.append({"대표메뉴":shop_menu_info})
    return gogi_shop_data

count1=0
count2=0





for k in range(3,18):
    print(k,'번째 지역 서치')

    #나온 목록에서 국내지역중 하나 클릭
    driver.find_element_by_xpath(next_high_region(k)).click()



    end_num = 2
    if count1 == 0:
        count1 += 1
        end_num = 69
        ##중간에 터지면 지역번호 지정 ㄱㄱ
    while True:
        print(end_num, '번째 세부지역 서치')

        try:
            state = driver.find_element_by_xpath(next_low_region(end_num)).text
        except:
            print('터짐')
            break
        region_data = state.split(' ')

        driver.find_element_by_xpath(next_low_region(end_num)).click()
        end_num += 1

        driver.find_element_by_xpath('/html/body/div/div/div/div[3]/div/div/div/div[1]/div[2]/div/ul/li[6]/a').send_keys(Keys.ENTER)

        shop_table = driver.find_element_by_id('tabMove1')
        while True:
            try:
                shop_table.find_element_by_class_name('btn_sMore').click()
            except:
                break
        shop_number=1
        if count2==0 :
            count2+=1
            shop_number=31
            #이건 샵번호 지정하자 중간에 터졌을 경우
        while True:
            shop_name_front = '/html/body/div/div/div/div[3]/div/div/div/div[6]/div/ul/li['
            shop_name_back = ']/div/a/div/div'
            shop_name_text = '/strong'
            shop_name_full = shop_name_front+str(shop_number)+shop_name_back
            try:
                shop_name=driver.find_element_by_xpath(shop_name_full+shop_name_text).text


                shop_name = shop_name.replace(".", ",") #가게제목. 있을경우 ,로 바꿔줌

                print(shop_name)

            except:
                driver.find_element_by_xpath(
                    '/html/body/div/div/div/div[3]/div/div/div/div[1]/div[1]/div/div/a').click()
                break

            driver.find_element_by_xpath(shop_name_front+str(shop_number)+']/div/a').send_keys(Keys.ENTER)

            shop_information = []
            shop_information.append({'지역':region_data[0]})

            shop_end_data = get_shop_data()
            for k in shop_end_data:
                shop_information.append(k)
            total_information = {shop_name : shop_information}
            db.ShopInfo.insert_one(total_information)


            driver.back()

            shop_number += 1




