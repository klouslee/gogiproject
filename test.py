from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import time

driver = webdriver.Chrome('D:/finalproject/chromedriver.exe')

url_base='https://www.google.com/maps/search/'

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route("/")
def home():
    return render_template('sample1.html', subject="이건 테스트")

@app.route('/search', methods=['POST'])
def write_review():
    search_full = request.form['search']
    search_keyword = request.form['search_key']
    url = url_base+search_full
    driver.get(url)
    go_back = "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/button/span"

    return jsonify({'result': 'success', 'msg': '서칭 성공적!'})



if __name__=="__main__":
    app.run()
