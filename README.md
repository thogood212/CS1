# 카셰어링 전기차 충전소 검색 프로젝트
![1](https://user-images.githubusercontent.com/87019897/175301077-a3444f28-d353-4f45-92ea-776f648168a2.png)

## ✔️ 개요

- 카셰어링 서비스 사용 시 **전기차 충전소에 대한 편의 개선을 위해 출발지와 목적지 사이의 전기차 충전소의 위치와 상세정보를 전달**해주는 어플리케이션 구현이 목표입니다.
- 데이터 출처 : 공공데이터 API를 활용하여 카셰어링 차고지 정보, 전기차 충전소 현황, 주소 기반 좌표 검색 데이터 수집하고 관계형 DB(Sqlite3)에 저장

## ✔️ 주제 선정 이유

![2](https://user-images.githubusercontent.com/87019897/175301119-9cbecb67-ec33-4b5e-abb7-703dedb9faf8.png)

- 전기차에 대한 관심이 많아지고 있지만 접하기 어려운 부분이 있습니다. 그러나 전기차를 가장 쉽고 빠르게 접해볼 수 있는 기회로 카셰어링 서비스가 있습니다.
- 그러나 자주 전기차를 사용하는 이용객이 아니라면 전기차 충전소의 위치 및 사용법에 대한 정보가 부족하기 때문에 카셰어링 어플에서 해당 서비스를 같이 제공할 경우 편의성이 늘어나 이용률이 높아질 것이라고 가정하였습니다.
- 또한 해당 프로젝트를 통해 이전 직무에서 쌓았던 물류 지식과 관심을 충족할 수 있다고 생각하여 GIS 정보를 사용하게 되었습니다.

## ✔️ 프로젝트 프로세스

![3](https://user-images.githubusercontent.com/87019897/175301150-89ae3233-7ef7-41d2-bf32-fa5f9f1e7f28.png)

## ✔️ **데이터 수집 및 분석**

![4](https://user-images.githubusercontent.com/87019897/175301170-e519c07b-c07f-4a39-b09e-dd1f90cac1b7.png)
![5](https://user-images.githubusercontent.com/87019897/175301178-255262b0-d421-43a2-8a5c-59322a12d0dc.png)

- 공공데이터 API를 활용하여 카셰어링 차고지 정보, 전기차 충전소 현황, 주소 기반 좌표 검색 데이터 수집하고 관계형 DB(Sqlite3)에 저장
- Folium 라이브러리를 사용하여 GIS 지도 데이터를 시각화 하여 활용
- 출발지(도시명,지역구) 입력을 통해 카셰어링 차고지 정보를 전달하여 선택할 수 있게 구현, 목적지(도시명, 지역구, 도로명) 입력을 통해 실시간으로 주소 기반 좌표 검색값을 전달하도록 구현
- 출발지와 목적지의 정보가 모두 입력된 경우, 출발지와 목적지 사이의 중간 지점을 설정, 해당 지점으로부터 10km이내의 전기차 충전소에 대한 정보를 지도를 통해 시각화 하여 확인 할 수 있도록 구현
- 최종적으로 지도에 출발지와 목적지가 표시되고 현재 시간에 맞게 이용가능한 충전소와 불가능한 충전소가 마커의 색깔로 구분되고 마커를 클릭 시에는 충전소 이름, 장소, 전화번호를 확인할 수 있도록 구현

## ✔️ 프로젝트 결과

- 출발지와 목적지를 설정하여 중간 지점에 위치한 전기차 충전소의 정보(이름,위치,전화번호, 사용시간 등)을 확인 할 수 있게 구현되었습니다.
- 사용불가한 시간대에 검색을 한 경우, 빨간색 표시로 표기되고 사용가능한 시간대인 경우, 초록색 표시로 표기됩니다.
![6](https://user-images.githubusercontent.com/87019897/175301198-9dc95407-0763-4c11-a007-6ab702beb74a.png)
![7](https://user-images.githubusercontent.com/87019897/175301214-a9fd40ae-4ee0-43cf-bd22-ccb19bd9a2e6.png)
![8](https://user-images.githubusercontent.com/87019897/175301223-ddcbbd32-464d-441c-be40-67fa7ff9eb3c.png)
![9](https://user-images.githubusercontent.com/87019897/175301240-913dad18-a316-4681-ad84-9207d1760c2c.png)


## ✔️ 프로젝트 REVIEW

아쉬운 점

- 출발지와 목적지의 네비게이션 경로에 맞춘 충전소 추천 시스템이었다면 더욱더 효용성이 증가했을 것이다.
- 웹에서 구현한 어플레케이션의 속도가 빠르지 않아 실생활에서 사용하기 부적합하다.
- 카카오, 네이버 네비게이션 API를 활용하여 좀더 정확한 충전소 위치 및 기준을 세울 수도 있겠다는 아쉬움이 들었습니다.

![10](https://user-images.githubusercontent.com/87019897/175301327-6b24efa4-cbed-4e35-bb9a-819cf0569eb9.png)

---
# 22.12.30일 업데이트

## ✔️ 업데이트 사항

- 출발지(카셰어링 대차지)를 사용하지 않고 사용자의 출발지에 맞춰서 충전소 길찾기가 가능하도록 업데이트 ( 카카오 로컬 API 사용 )
![스크린샷 2022-12-30 오후 4 51 13](https://user-images.githubusercontent.com/87019897/210047309-b3968f01-7ba2-43a5-8aa3-b3b72bb041b7.png)
  
- 카카오 api를 활용한 다중목적지 검색 기능을 활용함으로써 절대적 거리가 가깝더라도 도로상황상 실질적 거리가 멀어지는 것에 대해서 대응이 가능.
![스크린샷 2022-12-30 오후 4 53 50](https://user-images.githubusercontent.com/87019897/210047497-c20bccdc-358d-4b04-8c0e-69b0d4ba4037.png)
(하행선(목포방향) 휴게소를 출발지로 지정할 시에 상행선(서울방향) 휴게소의 충전소 순위가 뒤로 물러나게 됩니다.)

- 사용자가 설정한 범위 내에 사용가능한 전기차 충전소를 보여주기 및 목적지까지의 경로 요약정보(시간,거리) 전달
![스크린샷 2022-12-30 오후 4 56 20](https://user-images.githubusercontent.com/87019897/210047698-dafef86c-5b47-4341-8321-ba63b228cd43.png)


