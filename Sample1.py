from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db =client.dbsparta
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
            return(high_comment,low_comment)




totaldata = ''
storelist, storename = get_region_store('강남역')
i=1
for k in range(0,len(storelist)):
    store_name = ''.join(storename[k])
    store_region = storelist[k][0][0]['지역']
    store_img, store_star = get_store_pic(store_name,store_region)
    store_intro = storelist[k][0][2]['매장소개']
    store_type = storelist[k][0][1]['업종'][7:]
    store_phone = storelist[k][0][3]['전화번호']
    store_address = storelist[k][0][4]['주소']
    store_worktime = storelist[k][0][5]['영업시간']
    store_menu = storelist[k][0][6]['대표메뉴']

    if store_star!="평가중":
        store_meatpoint = str(int(float(store_star) * 20))
    else:
        store_meatpoint = "평가중"
    high_comment, low_comment = get_comment(store_name,store_region)
    data1 = """<div class="Sepecific" id="specific"""+str(i)+"""\" style="width: 1000px; height: auto; margin-top:0px; display: none;">
        </div>"""
    data2 = """<hr style="border: solid 1px rgb(138, 138, 138); "></hr>
        <div class="address">
          <h4>주소</h4>
          <h4 style="font-weight:unset">"""+store_address+"""</h4></div>"""

    data3 = """<div class="workTime">"""
    if len(store_worktime)>0:
        data3+="<h4>영업시간</h4>"
        for time in range(0,len(store_worktime)):
            a = store_worktime[time].keys()
            b = store_worktime[time].values()
            data3=data3+"<h4 style=\"font-weight:unset\">"+list(a)[0]+" : "+list(b)[0]+"</h4>"
    data3+="</div>"

    data4= """<div class="menu" style="width:1000px; height:auto; margin:0 0 0 0;">"""
    if len(store_menu)>0:
        data4+="""<h4 style="width:500px; height:auto; margin:0 0 0 5px;">대표메뉴</h4>
          <div style="width:250px; margin-top:0px;">"""
        for menu in range(0,len(store_menu)):
            a = store_menu[menu].keys()
            data4= data4+"""<h4 style="font-weight:unset">"""+list(a)[0]+""" : </h4>"""
        data4+="""</div>
          <div style="width:720px; margin-top:0px;">"""
        for menu in range(0,len(store_menu)):
            b = store_menu[menu].values()
            data4=data4+"""<h4 style="font-weight:unset">"""+list(b)[0]+"""</h4>"""
        data4+="""</div>
        </div>"""

    if int(store_meatpoint)<50:
        meat_pic="https://previews.123rf.com/images/makc76/makc761701/makc76170100058/69648578-piece-of-meat-vector-icon-beef-steak-icon-vector-illustration.jpg"
    else:
        meat_pic="https://cdn2.iconfinder.com/data/icons/steak-cartoon-2/512/g27867-512.png"

    data5="""<div class="comment" style="margin : 0 0 0 0">
          <h4 style="width:500px; height:auto; margin:0 0 0 5px;">MEAT 지수</h4>
          <div style="width:400; height:110px">
            <img
              src=\""""+meat_pic+"""\"
              alt="My Image" width=100px style="float:left">
            <h1 style="float:left; font-size:80px; margin: 0 600px 0 0 ">&nbsp;"""+store_meatpoint+"""%</h1>
            <hr width=650px; style="float: left; border: solid 1px rgb(138, 138, 138); margin: 10px 0 0 0;">
            </hr>"""
    if high_comment == "없음":
        data5+="</div>"
    else:
        data5= data5+"""<div class="good" style="height: auto; margin: 0 0 0 0;float: left;">
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
              <h3 style="margin: 20px 10px 10px 10px; float:left; width:230px">"""+high_comment[0]+"""</h1> 
              <h2 style="margin: 14px 10px 0 0px; float:right; height:45px;">"""+high_comment[1]+"""</h2>
              <div>
                <h6>"""+high_comment[2]+"""</h5>
              </div>
            </div>
          </div>

          <div style="border-left:2px solid rgb(138, 138, 138); width:5px; height: 300px;float:left;"></div>

          <div class="bad" style="height: auto; margin: 0 0 0 0;float: left;">
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
              <h3 style="margin: 20px 10px 10px 10px; float:left; width:230px">"""+low_comment[0]+"""</h1> 
              <h2 style="margin: 14px 10px 0 0px; float:right; height:45px;">"""+low_comment[1]+"""</h2>
              <div>
                <h6>"""+low_comment[2]+"""</h5>
              </div>
            </div>
          </div>
        </div>"""
    i+=1
    if i>2:
        break;