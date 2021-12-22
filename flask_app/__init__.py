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
from math import sin, cos, atan2, sqrt, degrees, radians, pi
from geopy.distance import great_circle as distance
from geopy.point import Point
import requests
import bs4
from math import sin, cos, atan2, sqrt, degrees, radians, pi
import sqlite3

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/select',methods = ['POST', 'GET'])
def carshare_info():
    if request.method == 'POST':
        addr1 = request.form['City']
        addr2 = request.form['District']
        url = 'http://openapi.tago.go.kr/openapi/service/CarSharingInfoService/getCarZoneListByAddr'
        params ={'serviceKey' : 'uq85vB0CVxMjRW8l/pz9IpBuoHGnXu5kw2tDlcjZZ7p8FI4eKWy85qTNK2rcfISJRZQFVabvDSEq3iEhe4cOFQ==',
                'pageNo' : 1,
                'numOfRows' : '100',
                'zoneAddr' : f'{addr1}'+' '+f'{addr2}'}
        response = requests.get(url, params=params).text.encode('utf-8')

        xmlobj = bs4.BeautifulSoup(response, 'lxml-xml')
        rows = xmlobj.findAll('item')

        rowList = []
        nameList = []
        columnList = []

        rowsLen = len(rows)
        for i in range(0, rowsLen):
            columns = rows[i].find_all()
            
            columnsLen = len(columns)
            for j in range(0, columnsLen):
                # 첫 번째 행 데이터 값 수집 시에만 컬럼 값을 저장한다. (어차피 rows[0], rows[1], ... 모두 컬럼헤더는 동일한 값을 가지기 때문에 매번 반복할 필요가 없다.)
                if i == 0:
                    nameList.append(columns[j].name)
                # 컬럼값은 모든 행의 값을 저장해야한다.    
                eachColumn = columns[j].text
                columnList.append(eachColumn)
            rowList.append(columnList)
            columnList = []    # 다음 row의 값을 넣기 위해 비워준다. (매우 중요!!)
        
        result = pd.DataFrame(rowList, columns=nameList)
        return render_template('select.html',tables=rowList)

def geocording(address):
    #address= request.form['destination']
    address = address.replace('지하 ', '') # 도로명주소에 '지하'가 포함되는 경우 API에서 에러가 발생하는 것을 처리합니다.
    apiKey = '9C86074F-229A-3625-86F6-0EAB6B8038A9'
    r = requests.get('http://apis.vworld.kr/new2coord.do?q=' + address + '&apiKey=' + apiKey + \
            '&domain=http://map.vworld.kr/&output=json').text
    data = json.loads(r)
    if 'result' in data:
        return (-1, -1)
    x, y = data['EPSG_4326_Y'], data['EPSG_4326_X']
    x=float(x)
    y=float(y)
    return x,y

def midpoint():
    if request.method == 'POST':
        a= Point(latitude=request.form['lat'], longitude=request.form['lon'])
        (x,y) = geocording(request.form['destination'])
        b= Point(latitude=x, longitude=y)
        a_lat, a_lon = radians(a.latitude), radians(a.longitude)
        b_lat, b_lon = radians(b.latitude), radians(b.longitude)
        delta_lon = b_lon - a_lon
        B_x = cos(b_lat) * cos(delta_lon)
        B_y = cos(b_lat) * sin(delta_lon)
        mid_lat = atan2(
            sin(a_lat) + sin(b_lat),
            sqrt(((cos(a_lat) + B_x)**2 + B_y**2))
        )
        mid_lon = a_lon + atan2(B_y, cos(a_lat) + B_x)
        # Normalise
        mid_lon = (mid_lon + 3*pi) % (2*pi) - pi
        midpoint=Point(latitude=degrees(mid_lat), longitude=degrees(mid_lon))
        
        return midpoint






@app.route('/result',methods = ['POST'])
# def geocording():
#     if request.method == 'POST':
#         address= request.form['destination']
#         address = address.replace('지하 ', '') # 도로명주소에 '지하'가 포함되는 경우 API에서 에러가 발생하는 것을 처리합니다.
#         apiKey = '9C86074F-229A-3625-86F6-0EAB6B8038A9'
#         r = requests.get('http://apis.vworld.kr/new2coord.do?q=' + address + '&apiKey=' + apiKey + \
#                 '&domain=http://map.vworld.kr/&output=json').text
#         data = json.loads(r)
#         if 'result' in data:
#             return (-1, -1)
#         x, y = data['EPSG_4326_Y'], data['EPSG_4326_X']
#         #dest=Point(latitude=x, longitude=y)
#         return render_template('result.html',data=(x,y))

# def midpoint():
#     if request.method == 'POST':
#         a= Point(latitude=request.form['lat'], longitude=request.form['lon'])
#         (x,y) = geocording(request.form['destination'])
#         b= Point(latitude=x, longitude=y)
#         a_lat, a_lon = radians(a.latitude), radians(a.longitude)
#         b_lat, b_lon = radians(b.latitude), radians(b.longitude)
#         delta_lon = b_lon - a_lon
#         B_x = cos(b_lat) * cos(delta_lon)
#         B_y = cos(b_lat) * sin(delta_lon)
#         mid_lat = atan2(
#             sin(a_lat) + sin(b_lat),
#             sqrt(((cos(a_lat) + B_x)**2 + B_y**2))
#         )
#         mid_lon = a_lon + atan2(B_y, cos(a_lat) + B_x)
#         # Normalise
#         mid_lon = (mid_lon + 3*pi) % (2*pi) - pi
#         midpoint=Point(latitude=degrees(mid_lat), longitude=degrees(mid_lon))
        
#         return render_template('result.html',data=(degrees(mid_lat),degrees(mid_lon)))

def find_charger():
    if request.method == 'POST':
        a= Point(latitude=float(request.form['lat']), longitude=float(request.form['lon']))
        (x,y) = geocording(request.form['destination'])
        b= Point(latitude=x, longitude=y)

        min_lat=min(a.latitude,b.latitude) #좌표값 비교를 위해 최대.최소값 나눠주기
        min_lng=min(a.longitude,b.longitude)
        max_lat=max(a.latitude,b.latitude)
        max_lng=max(a.longitude,b.longitude)
        count=0 # 충전소가 없을 시를 확인하기 위한 변수
        #출발지와 목적지 사이의 직선에 11km안에 있는 충전소 지도에 보여주기
        conn = sqlite3.connect("/Users/damon/Documents/codestate_project/project6/Data.db", isolation_level=None)
        cur = conn.cursor()
        query = cur.execute("SELECT * From chargers")
        cols = [column[0] for column in query.description]
        charger_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        charger_result[['lat','lng']]=charger_result[['lat','lng']].apply(pd.to_numeric)
        Lat = charger_result.lat.mean()
        Long = charger_result.lng.mean()
        map=folium.Map([Lat,Long],zoom_start=16)
        distribution_map=plugins.MarkerCluster().add_to(map)
        str_tag = '<strong><font style="color:blue" size="4">'
        #출발지 표시
        folium.Marker(location=[a.latitude,a.longitude],icon=folium.Icon(color = 'blue', icon = 'car',prefix='fa'),tooltip='출발지').add_to(distribution_map)
        #도착지 표시
        folium.Marker(location=[b.latitude,b.longitude],icon=folium.Icon(color = 'blue', icon = 'map-pin',prefix='fa'),tooltip='목적지').add_to(distribution_map)
        
        for lat,lon,label,usetime,num in zip(charger_result.lat,charger_result.lng,charger_result['statNm'],charger_result['useTime'],charger_result['busiCall']):
            # Lat = charger_result.lat.mean()
            # Long = charger_result.lng.mean()
            # map=folium.Map([Lat,Long],zoom_start=16)
            # distribution_map=plugins.MarkerCluster().add_to(map)
            # str_tag = '<strong><font style="color:blue" size="4">'
            # #출발지 표시
            # folium.Marker(location=[a.latitude,a.longitude],icon=folium.Icon(color = 'blue', icon = 'car',prefix='fa'),tooltip='출발지').add_to(distribution_map)
            # #도착지 표시
            # folium.Marker(location=[b.latitude,b.longitude],icon=folium.Icon(color = 'blue', icon = 'map-pin',prefix='fa'),tooltip='목적지').add_to(distribution_map)
            
            if lat >= min_lat-0.1 and lat <= max_lat+0.1 and lon >= min_lng-0.1 and lon <= max_lng+0.1:
                p= Point(latitude=lat, longitude=lon)
                if distance(midpoint(), p)<= 11:
                    count += 1
                    # map=folium.Map([Lat,Long],zoom_start=16)
                    # distribution_map=plugins.MarkerCluster().add_to(map)
                    #str_tag = '<strong><font style="color:blue" size="4">'
                    #출발지 표시
                    #folium.Marker(location=[a.latitude,a.longitude],icon=folium.Icon(color = 'blue', icon = 'car',prefix='fa'),tooltip='출발지').add_to(distribution_map)
                    #도착지 표시
                    #folium.Marker(location=[b.latitude,b.longitude],icon=folium.Icon(color = 'blue', icon = 'map-pin',prefix='fa'),tooltip='목적지').add_to(distribution_map)
                    try :
                        if usetime[:2] == '24' or usetime == '':
                            folium.Marker(location=[lat,lon],icon=folium.Icon(color = 'green', icon = 'bolt',prefix='fa'),tooltip=str_tag + label + '</font></strong>' + ' (' \
                                + str(usetime) + ')</br>'+'Tel:'+ str(num)+'</br>'+'사용가능').add_to(distribution_map)
                        elif int(usetime.split('~')[0][:2]) <= datetime.now().hour+9 or int(usetime.split('~')[1][:2]) >= datetime.now().hour+9:
                            folium.Marker(location=[lat,lon],icon=folium.Icon(color = 'red', icon = 'bolt',prefix='fa'),tooltip=str_tag + label + '</font></strong>' + ' (' \
                                + str(usetime) + ')</br>'+'Tel:'+ str(num)+'</br>'+'영업시간을 확인해주세요').add_to(distribution_map)
                        else :
                            folium.Marker(location=[lat,lon],icon=folium.Icon(color = 'red', icon = 'bolt',prefix='fa'),tooltip=str_tag + label + '</font></strong>' + ' (' \
                                + str(usetime) + ')</br>' + 'Tel:'+str(num)+'</br>'+'사용불가').add_to(distribution_map)
                        #map.add_child(distribution_map)
                    except:
                        folium.Marker(location=[lat,lon],icon=folium.Icon(color = 'red', icon = 'bolt',prefix='fa'),tooltip=str_tag + label + '</font></strong>' + ' (' \
                                + str(usetime) + ')</br>'+'Tel:'+ str(num)+'</br>'+'영업시간을 확인해주세요').add_to(distribution_map)
                        #map.add_child(distribution_map)

        if count ==0:
            answer = '전기차 렌트를 추천하지 않습니다. 이용 반경 10km내에 충전소가 없습니다.'
            return render_template('result.html',data=answer)          
        else:
        # data = io.BytesIO()
        # map.save(data, close_file = False)
            map.add_child(distribution_map)
            map.save('/Users/damon/Documents/codestate_project/project6/flask_app/templates/map.html')
            answer=f'이동 경로에서 {count}개의 충전소가 검색되었습니다.'
            # map._repr_html_()
            return render_template('result.html',data=answer)

if __name__ == '__main__':
    app.run(debug=True)