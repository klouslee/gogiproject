from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


# client = MongoClient('mongodb://sampleID:samplePW@12.34.56.78', 27017)
client = MongoClient('localhost', 27017)
db = client.dbsparta

where = ''
def get_region_store(region):
    gogilist = []
    goginame = []
    style= list(db.ShopInfo.find({},{'_id':0}))
    for k in style:
        t=list(k.values())
        p=list(k.keys())

        if t[0][0]['지역'] == region:
            gogilist.append(t)
            goginame.append(p)
    return gogilist, goginame

def get_store_pic(name,region):
    store = list(db.PicStar.find({},{'_id':0}))
    i=0

    for k in store:
        if(k['이미지'][1]['가게이름']==name and k['이미지'][0]['지역']==region):
            return k['이미지'][2]['이미지'],k['이미지'][3]['별점']
        i += 1

def get_comment(name,region):
    comments = list(db.ShopComments.find({},{'_id':0}))
    high_comment=[]
    low_comment = []
    lowstar=6
    highstar=0
    for k in comments:
        t = list(k.values())
        p = list(k.keys())
        if p[0]==name and t[1]==region:
            comment_list = t[0]
            if len(comment_list)<2:
                return "없음","없음"
            for o in comment_list:
                if float(o['별점'])>highstar:
                    highstar = float(o['별점'])
                if float(o['별점'])<lowstar:
                    lowstar = float(o['별점'])
            for o in comment_list:
                if (float(o['별점']) == highstar):
                    if len(high_comment)!=3:
                        high_comment.append(o['이름'])
                        high_comment.append(o['별점'])
                        high_comment.append(o['코멘트'])


                if (float(o['별점']) == lowstar):
                    if len(low_comment)!=3:
                        low_comment.append(o['이름'])
                        low_comment.append(o['별점'])
                        low_comment.append(o['코멘트'])
                print(high_comment,low_comment)
            return(high_comment,low_comment)
        else:
            return "없음", "없음"

def get_specific_data(region,store,type):
    search_key = region
    store_num = store
    storelist, storename = get_region_store(search_key)
    store_name = ''.join(storename[store_num-1])
    k=storelist[store_num-1][0]
    infolist=[]
    for i in k:
        infolist.append(list(i.keys())[0])
    if type in infolist:
        pos = infolist.index(type)
        return storelist[store_num-1][0][pos][type]
    else:
        return "정보없음"



# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('gogi.html')

@app.route('/searchregion', methods=['POST'])
def region():
    search_key = request.form['search_key']
    regions=list(db.region.find({'state':search_key},{'_id':0,'state':0,'shop_num':0}))
    k=len(regions)
    data=""
    for state in regions:
        data=data+"""
        <a href="#" style="margin-bottom:3px" onclick ="getdata(\'"""+str(state['region'])+"""\')" class="btn-gradient blue mini">"""+state['region']+"""</a>
        """


    return jsonify({'result': 'success', 'data': data})

@app.route('/search', methods=['POST'])
def post():
    search_key = request.form['search']
    totaldata = ''
    storelist, storename = get_region_store(search_key)
    global where
    where = storelist[0][0][0]['지역']
    i = 1

    for k in range(0, len(storelist)):
        store_name = ''.join(storename[k])
        store_region = get_specific_data(search_key,k+1,'지역')
        store_img, store_star = get_store_pic(store_name, store_region)

        store_intro = get_specific_data(search_key,k+1,'매장소개')

        store_type = get_specific_data(search_key,k+1,'업종')[7:]
        data = """    <div class="shoplist""" + str(i) + """\" style="width: 1000px; height: auto; margin-top: 10px; overflow: hidden;"><hr style="border: solid 1px rgb(138, 138, 138); ">
          </hr>
          <div class="shoppic" style="margin-top: 20px;">
            <img src=\""""+store_img+"""\" alt="My Image" width=200px height=180px>
          </div>
          <div class="shopinfo" style="height: 190px; width: 760px; ">
            <h2 style='margin: 4px 0 1px 3px; color:crimson'>"""+store_star+"""</h2>
            <h2 style='margin: 4px 0 1px 3px;'>　""" + store_name + """</h2>
            <h4 style='margin-top: 50px; margin-left:10px'>#""" + store_region + """ #""" + store_type + """</h4>
            <h5 style='width:90%'>""" + store_intro + """</h5>
            <button style='float:right; vertical-align:bottom' onclick="getinfo("""+str(i)+""")">더보기 ⇓</button>
          </div>
      </div>
    """
        totaldata += data

        i += 1
        if i > 10:
            break;
    return jsonify({'result': 'success','msg':'가져오는데 성공','data':totaldata})


@app.route('/searchinfo', methods=['POST'])
def postinfo():
    search_key = where
    store_num = int(request.form['storenum'])

    storelist, storename = get_region_store(search_key)
    store_name = ''.join(storename[store_num-1])
    get_specific_data(search_key,store_num,'지역')
    store_region = get_specific_data(search_key,store_num,'지역')
    store_img, store_star = get_store_pic(store_name, store_region)
    store_address = get_specific_data(search_key,store_num,'주소')
    store_worktime = get_specific_data(search_key,store_num,'영업시간')
    store_menu = get_specific_data(search_key,store_num,'대표메뉴')
    store_phone = get_specific_data(search_key,store_num,'전화번호')

    if store_star != "평가중":
        store_meatpoint = str(int(float(store_star) * 20))
    else:
        store_meatpoint = "평가중"
    high_comment, low_comment = get_comment(store_name, store_region)

    data1 = """<div class="Sepecific" id="specific""" + str(store_num) + """\" style="width: 1000px; height: auto; margin-top:0px; display:block;">
        </div>"""
    data2 = """<hr style="border: solid 1px rgb(138, 138, 138); "></hr>
        <div class="address">
          <h3>주소</h3>
          <h3 style="font-weight:unset">""" + store_address + """</h3></div>"""

    data3 = """<div class="workTime">"""
    if len(store_worktime) > 0:
        data3 += "<h3>영업시간</h3>"
        for time in range(0, len(store_worktime)):
            a = store_worktime[time].keys()
            b = store_worktime[time].values()
            data3 = data3 + "<h3 style=\"font-weight:unset\">" + list(a)[0] + " : " + list(b)[0] + "</h4>"
    data3 += "</div>"

    data4 = """<div class="menu" style="width:1000px; height:auto; margin:0 0 0 0;">"""
    if len(store_menu) > 0:
        data4 += """<h3 style="width:500px; height:auto; margin:0 0 0 5px;">대표메뉴</h3>
          <div style="width:250px; height:auto; margin-top:0px;">"""
        for menu in range(0, len(store_menu)):
            a = store_menu[menu].keys()
            data4 = data4 + """<h3 style="font-weight:unset">""" + list(a)[0] + """ : </h3>"""
        data4 += """</div>
          <div style="width:720px; margin-top:0px;">"""
        for menu in range(0, len(store_menu)):
            b = store_menu[menu].values()
            data4 = data4 + """<h3 style="font-weight:unset">""" + list(b)[0] + """</h3>"""
        data4 += """</div><h3>"""+store_phone+"""</h3>
        </div>"""
    if store_meatpoint!='평가중':
        if int(store_meatpoint) < 50:
            meat_pic = "https://previews.123rf.com/images/makc76/makc761701/makc76170100058/69648578-piece-of-meat-vector-icon-beef-steak-icon-vector-illustration.jpg"
        else:
            meat_pic = "https://cdn2.iconfinder.com/data/icons/steak-cartoon-2/512/g27867-512.png"
    else:
        meat_pic = "https://www.sgu.ac.kr/_res/sgu_mobile/img/common/prepare.jpg"



    data5 = """<div class="comment" style="margin : 0 0 0 0; height:450px">
          <h3 style="width:500px; height:auto; margin:0 0 0 5px;">MEAT 지수</h3>
          <div style="width:400; height:110px; position: relative;">
            <img
              src=\"""" + meat_pic + """\"
              alt="My Image" width=100px style="float:left">
            <h1 style="float:left; font-size:80px; margin: 0 600px 0 0 ">&nbsp;""" + store_meatpoint + """%</h1>
            <hr width=650px; style="float: left; border: solid 1px rgb(138, 138, 138); margin: 10px 0 0 0;">
            </hr>"""
    if high_comment == "없음":
        data5 += "</div>"
    else:
        data5 = data5 + """<div class="good" style="height: auto; margin: 0 0 0 0;float: right; position: absolute; top:120px;">
            <div style="width: 300px; height: 60px;">
              <div style=" max-width:60px; overflow: hidden; float: left; margin: 0 0 0 0;">
                <img
                  src="https://previews.123rf.com/images/09910190/099101901711/09910190171100062/90461006-good-and-bad-signs-set-social-media-gesture-like-finger-thumb-up-and-down-vector-illustration-flat-s.jpg"
                  alt="C:/Users/klous/OneDrive/Desktop/sign/bad.png" width=100px
                  style="max-width:initial; float: left; margin: 0px 10px 0px 10px; overflow: hidden; ">
              </div>
              <div style=" margin:15px 0 0 0; width: 180px; float: left ">
                <h1 style=" margin:0 0 0 10px;">좋아요!</h1>
              </div>
            </div>
            <hr width=300px; style="float: left; border: solid 1px rgb(138, 138, 138); margin: 10px 0 0 0;">
            <div class="goodComment1" style="width:300px">
              <h3 style="margin: 20px 10px 10px 10px; float:left; width:230px">""" + high_comment[0] + """</h1> 
              <h2 style="margin: 14px 10px 0 0px; float:right; height:45px;">""" + high_comment[1] + """</h2>
              <div>
                <h5>""" + high_comment[2] + """</h5>
              </div>
            </div>
          </div>

          <div style="border-left:2px solid rgb(138, 138, 138); width:5px; height: 300px;float:left; position: absolute; left:320px; top:120px;"></div>

          <div class="bad" style="height: auto; margin: 0 0 0 0;float: left; position:absolute; left:340px; top:120px;">
            <div style="width: 300px; height: 60px;">
              <div style=" max-width:60px; overflow: hidden; float: left; margin: 0 0 0 0;">
                <img
                  src="https://previews.123rf.com/images/09910190/099101901711/09910190171100062/90461006-good-and-bad-signs-set-social-media-gesture-like-finger-thumb-up-and-down-vector-illustration-flat-s.jpg"
                  alt="C:/Users/klous/OneDrive/Desktop/sign/bad.png" width=100px
                  style="max-width:initial; float: left;  margin: 0px 10px 0px -80%; overflow: hidden; ">
              </div>
              <div style=" margin:15px 0 0 0; width: 180px; float: left ">
                <h1 style=" margin:0 0 0 0px;">모르겠어요!</h1>
              </div>
            </div>
            <hr width=300px; style="float: left; border: solid 1px rgb(138, 138, 138); margin: 10px 0 0 0;">
            <div class="goodComment1" style="width:300px">
              <h3 style="margin: 20px 10px 10px 10px; float:left; width:230px">""" + low_comment[0] + """</h1> 
              <h2 style="margin: 14px 10px 0 0px; float:right; height:45px;">""" + low_comment[1] + """</h2>
              <div>
                <h5>""" + low_comment[2] + """</h5>
              </div>
            </div>
          </div>
        </div>"""


    return jsonify({'result': 'success', 'region': search_key,'data1': data1,'data2':data2,'data3':data3,'data4':data4,'data5':data5})



if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
