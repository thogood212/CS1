from flask import Flask
from flask import Flask, render_template
from flask import request
import pandas as pd
from bs4 import BeautifulSoup as bs
import numpy as np
from datetime import datetime, timedelta
import folium, json, sys, io
from folium import plugins
from folium.plugins import MarkerCluster
from geopy.distance import great_circle as geodistance
from geopy.point import Point
import requests
import bs4
import sqlite3
import module

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/select',methods = ['POST', 'GET'])
def geocording():
    if request.method == 'POST':
        #키워드를 통한 상세 주소 좌표 표기
        addr = request.form['address']
        url = f"http://dapi.kakao.com/v2/local/search/keyword"
        header = {'Authorization': 'KakaoAK 318f960d88d8869efe28e323c646cad5', 
                "Content-Type" : "application/json"}

        queryString = {'query' : addr}
        response = requests.get(url, headers=header, params=queryString)
        search = response.json()        

        nameList = ['place_name','category_group_name','road_address_name','place_url','x','y']
        result = pd.DataFrame(search['documents'], columns=nameList)
        return render_template('select.html',tables=search['documents'])


@app.route('/result',methods = ['POST'])
def find_charger():
    if request.method == 'POST':
        depart_lat=float(request.form['y'])
        depart_lng=float(request.form['x'])
        p_departure= Point(latitude=depart_lat, longitude=depart_lng)

        count=0 # 충전소가 없을 시를 확인하기 위한 변수
        #출발지 10km안에 있는 충전소 지도에 보여주기
        conn = sqlite3.connect("/Users/damon/Documents/codestate_project/project6/DB/DB.db", isolation_level=None)
        cur = conn.cursor()
        query = cur.execute("SELECT * From chargers2")
        cols = [column[0] for column in query.description]
        charger_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        charger_result[['lat','lng']]=charger_result[['lat','lng']].apply(pd.to_numeric)

        charger_result = charger_result[(charger_result['lat']<=depart_lat+0.1) & (charger_result['lat']>=depart_lat-0.1) & (charger_result['lng']<=depart_lng+0.15) & (charger_result['lng']>=depart_lng-0.15)]
        charger_result= charger_result.reset_index(drop = True)
        charger_result['ex_distance']=1e9

        for i,geo in enumerate(zip(charger_result.lat,charger_result.lng)):  
            lat, lng = geo
            p= Point(latitude=lat, longitude=lng)
            charger_result.loc[i,'ex_distance']=float(geodistance(p_departure, p).km)
        charger_result = charger_result.sort_values('ex_distance')

        #5km 미만 충전소가 10개 미만이면 10km 미만 충전소까지 확인
        if len(charger_result[charger_result['ex_distance']<=5]) < 10:
            DB_result = charger_result[charger_result['ex_distance']<=10][:30].reset_index(drop = True)
        else:
            DB_result = charger_result[charger_result['ex_distance']<=5][:30].reset_index(drop = True)
        #코드를 읽기 쉽게 변환
        DB_result['chgerType'] = DB_result['chgerType'].apply(lambda x: module.chger_code(x))
        DB_result['kindDetail'] = DB_result['kindDetail'].apply(lambda x: module.detail_code(x))

        url = "https://apis-navi.kakaomobility.com/v1/destinations/directions"

        #다중 목적지 카카오내비 api
        header = {'Authorization': 'KakaoAK 318f960d88d8869efe28e323c646cad5', "Content-Type" : "application/json"}

        destination = module.make_dest(p_departure,DB_result)
        response = requests.post(url, headers=header, json=destination)
        multi_destination = response.json()

        #dataframe화
        route = pd.DataFrame(multi_destination['routes'])
        route['distance']=route['summary'].apply(lambda x: x['distance'])
        route['duration']=route['summary'].apply(lambda x: x['duration'])
        route = route.drop(columns=['result_code','summary'])
        DB_result = pd.merge(DB_result,route, left_index=True,right_index=True)
        colortype = {'Y':'#DC0000', 'N':'#00ABDC'}
        abletype = {'Y':'<font style="color:red" size="4"> 사용불가 </font> ', 'N':'<font style="color:green" size="4"> 사용가능 </font>'}
        abletype2 = {'Y':' 사용불가 ', 'N':' 사용가능 '}
        parking = {'Y':'주차 무료', 'N':'주차 유료 및 제한'}
        DB_result=module.check_result(DB_result)

        map=folium.Map([depart_lat,depart_lng],zoom_start=16)
        distribution_map=plugins.MarkerCluster(maxClusterRadius=10).add_to(map)
        str_tag = '<strong><font style="color:blue" size="4">'

        #출발지 표시
        folium.Marker(location=[depart_lat,depart_lng],icon=folium.Icon(color = 'blue', icon = 'car',prefix='fa'),tooltip='출발지').add_to(distribution_map)

        for i in range(len(DB_result)):
            count+=1

            makerDetail = module.make_marker(i, DB_result)
            lat = DB_result.loc[i,'lat']
            lng = DB_result.loc[i,'lng']
            num = DB_result.loc[i,'key']
            name = DB_result.loc[i,'statNm']
            p= Point(latitude=lat, longitude=lng)
            usetime = DB_result.loc[i,'useTime']
            kindDetail = DB_result.loc[i,'kindDetail']
            parkingFree = DB_result.loc[i,'parkingFree']
            limitDetail = DB_result.loc[i,'limitDetail']
            addr = DB_result.loc[i,'addr']
            location = DB_result.loc[i,'location']
            total_chger_num = DB_result.loc[i,'total_chger_num']
            distance = DB_result.loc[i,'distance']
            duration = DB_result.loc[i,'duration']
            
            # 목록 클릭시 id로 넘겨주기 위해 설정
            html = folium.Html(f"""
                <div id={num} class="d-flex w-100 justify-content-between">
                  <h5 class="mb-1">{num}. {name}</h5>
                  <small>{abletype2[DB_result.loc[i,'limitYn']]}</small>
                </div>
                <p class="mb-1">{addr}{location}</p>
                """, script=True)
            popup = folium.Popup(html, max_width=2650)
            
            icon_number = plugins.BeautifyIcon(
                border_color= colortype[DB_result.loc[i,'limitYn']],
                text_color= colortype[DB_result.loc[i,'limitYn']],
                icon_shape = 'marker',
                number=str(num))

            #marker 입력
            folium.Marker(location=[lat,lng],
            icon = icon_number,
            tooltip=str_tag + str(num) +'.'+name + '</font></strong>'
            + ' (이용시간 : ' + str(usetime) + ')</br>'
            + '<strong><font style="color:blue" size="2">'+'목적지 거리 :' + str(distance/1000) +'km'+'</br>'
            + '예상 소요 시간 :' + str(duration//60) +'분' +str(duration%60)+'초' +'</font></strong>' +'</br>'
            +'충전소 위치 구분 :'+str(kindDetail) +'</br>'
            +'충전소 상세 위치:'+str(location) +'</br>'
            +'주차장 이용 :'+str(parking[f'{parkingFree}'])+'</br>'
            +'충전기 총 '+ str(total_chger_num)+'개'+'</br>'
            + makerDetail
            + '주소 :' + str(addr)+'</br>'
            + abletype[DB_result.loc[i,'limitYn']]
            + ' ' + str(limitDetail)).add_to(distribution_map)
        
        DB_result['limitYn'] = DB_result['limitYn'].apply(lambda x: abletype2[x])
        result_json = DB_result.to_json(orient = 'records',force_ascii=False)
        result_json = json.loads(result_json)

        if count ==0:
            answer = '전기차 렌트를 추천하지 않습니다. 이용 반경 10km내에 충전소가 없습니다.'
            return render_template('result.html',data=answer,tables=result_json)          
        else:
            map.add_child(distribution_map)
            map.save('/Users/damon/Documents/codestate_project/project6/flask_app_update/templates/map.html')
            answer=f'이동 경로에서 {count}개의 충전소가 검색되었습니다.'
            return render_template('result.html',data=answer,tables=result_json)

if __name__ == '__main__':
    app.run(debug=True)

