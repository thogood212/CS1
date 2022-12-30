def chger_code(code):
    chgerType = {'1':'DC차데모','2':'AC완속','3':'DC차데모+AC3상',
             '4':'DC콤보','5':'DC차데모+DC콤보','6':'DC차데모+AC3상+DC콤보',
             '7':'AC3상','89':'H2'}
    return chgerType[str(code)]

def detail_code(code):
    kindDetail = {
    'A001': '관공서','A002': '주민센터','A003': '공공기관','A004': '지자체시설',
    'B001': '공영주차장','B002': '공원주차장','B003': '환승주차장','B004': '일반주차장',
    'C001': '고속도로 휴게소','C002': '지방도로 휴게소','C003': '쉼터',
    'D001': '공원','D002': '전시관','D003': '민속마을','D004': '생태공원','D005': '홍보관','D006': '관광안내소',
    'D007': '관광지','D008': '박물관','D009': '유적지',
    'E001': '마트(쇼핑몰)','E002': '백화점','E003': '숙박시설','E004': '골프장(CC)','E005': '카페','E006': '음식점',
    'E007': '주유소','E008': '영화관','F001': '서비스센터','F002': '정비소',
    'G001': '군부대','G002': '야영장','G003': '공중전화부스','G004': '기타','G005': '오피스텔','G006': '단독주택',
    'H001': '아파트','H002': '빌라','H003': '사업장(사옥)','H004': '기숙사','H005': '연립주택',
    'I001': '병원','I002': '종교시설','I003': '보건소','I004': '경찰서','I005': '도서관','I006': '복지관','I007': '수련원','I008': '금융기관',
    'J001': '학교','J002': '교육원','J003': '학원','J004': '공연장','J005': '관람장','J006': '동식물원','J007': '경기장','':'기타'}  
    return kindDetail[code]

#마커 세부사항 설정 함수
def make_marker(num, data):
    data = data.loc[num]
    string = ''
    for i in range(1,8):
      if data[f'chgerType_{i}'] != 0:
          string += f'{chger_code(i)} : {data[f"chgerType_{i}"]}개</br>'
    return string

def make_dest(departure, dataframe):
    destination = {}
    dest_list=[]
    destination['origin'] = {'x': departure[1], 'y':departure[0]}
    for i in range(len(dataframe)):
        dest_dict={}
        dest_dict['x']=str(dataframe.loc[i,'lng'])
        dest_dict['y']=str(dataframe.loc[i,'lat'])
        dest_dict['key']=f'{i}'
        dest_list.append(dest_dict)
    destination['destinations'] = dest_list
    destination['radius'] = 10000
    return destination

def check_result(df):
    for i in range(len(df)):
        if df.loc[i,'result_msg'] == '길찾기 실패':
            df = df.drop(index=i, axis=0)
    df = df.sort_values(by=["limitYn",'duration'], ascending=[True, True])
    df = df.reset_index(drop=True)
    for i in range(len(df)):
        df.loc[i,'index'] = int(i)+1
    df['index'] = df['index'].apply(lambda x: int(x))
    df['location'] = df['location'].apply(lambda x: '' if x =='null' else x)
    df['key'] = df['key'].apply(lambda x : int(x)+1)
    return df