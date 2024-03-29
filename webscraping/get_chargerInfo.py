import requests
import time
import bs4
import sqlite3
import time
import pandas as pd


conn= sqlite3.connect("/Users/damon/Documents/codestate_project/project6/DB.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS chargers;")

#데이터 저장할 테이블 생성
cur.execute("""CREATE TABLE chargers (
    statId VARCHAR,
    statNm VARCHAR,
    chgerId VARCHAR,
    chgerType INTEGER,
    addr VARCHAR,
    location VARCHAR,
    lat VARCHAR,
    lng VARCHAR,
    useTime VARCHAR,
    busiId VARCHAR,
    bnm VARCHAR,
    busiNm VARCHAR,
    busiCall INTEGER,
    stat INTEGER,
    statUpdDt INTEGER,
    lastTsdt INTEGER,
    lastTedt INTEGER,
    nowTsdt INTEGER,
    powerType VARCHAR,
    output INTEGER,
    method VARCHAR,
    zcode INTEGER,
    zscode INTEGER,
    kind VARCHAR,
    kindDetail VARCHAR,
    parkingFree VARCHAR,
    note VARCHAR,
    limitYn VARCHAR,
    limitDetail VARCHAR,
    delYn VARCHAR,
    delDetail VARCHAR);""")

for i in range(1,21):
    url = 'http://apis.data.go.kr/B552584/EvCharger/getChargerInfo'
    params ={'serviceKey' : '서비스키 입력하기',
            'pageNo' : {i},
            'numOfRows' : '9200',
            'period' : '5'}
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
    result = result.drop_duplicates()

    #데이터 베이스에 저장
    result.to_sql(name='chargers', con=conn, if_exists='append',index=False)  

conn.commit()
conn.close()
