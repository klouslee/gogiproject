from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from multiprocessing import Pool

from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import google_module


startime = time.time()
def get_gogi_data(t):
    url='https://www.google.com/maps/search/수지구+고기집'
    option1 = webdriver.ChromeOptions()
    option1.add_argument('headless')
    option1.add_argument('window-size=1920x1080')
    option1.add_argument("disable-gqu")

    driver = webdriver.Chrome('D:/finalproject/chromedriver.exe', options=option1)
    client = MongoClient('localhost', 27017)
    db = client.dbsparta
    driver.get(url)
    WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/h3/span")
            )
        )#페이지 로딩 기다리기(특정 div 나올 때 까지)



    go_back = "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/button/span"

    for k in range(t, 39, 8):
        find_front = "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[1]/div["

        find_full = find_front + str(k) + "]"

        driver.find_element_by_xpath(find_full).click()
        WebDriverWait(driver, 3).until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/h1")
            )
        )

        gogi_name = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/h1").text
        gogi_position = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[10]/div/div[1]/span[3]/span[3]").text

        gogi_phone_div=None
        gogi_phones=None
        gogi_phone=None
        try:
            gogi_phone_div = driver.find_element_by_class_name("section-info-speak-numeral")
            gogi_phones = gogi_phone_div.find_elements_by_class_name("widget-pane-link")
            gogi_phone = google_module.get_gogi_phone(gogi_phones)

        except:
            gogi_phone = '정보없음'

        gogi_work_div = None
        gogi_work = None
        gogi_work1 = None
        gogi_work2 = None
        try:
            gogi_work_div = driver.find_element_by_class_name("section-open-hours")
            gogi_work1 = gogi_work_div.find_elements_by_class_name("section-info-red")
            gogi_work2 = gogi_work_div.find_elements_by_class_name("section-info-text")

            gogi_work1, gogi_work2 = google_module.get_gogi_work(gogi_work1, gogi_work2)
        except:
            gogi_work1 = '정보없음'
            gogi_work2 = ''

        dataset = {'store_name': str(gogi_name),
           'store_position': str(gogi_position),
           'store_phone': str(gogi_phone),
           'store_work' : str(gogi_work1)+str(gogi_work2)}
        db.stores.insert_one(dataset)

        driver.find_element_by_xpath(go_back).click()
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, find_full)
            )
        )
if __name__ == '__main__' :
    num_list = [1, 3, 5, 7]

    pool = Pool(processes=4)
    pool.map(get_gogi_data, num_list)

    print(time.time()-startime)
