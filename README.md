# KBO_stadium_introduce
한국 야구장 소개 홈페이지 제작

<h2>현재 진행 상황</h2>
<h3>6월 21일</h3>

- 대략적인 구조 html 파일로 구현
    - 메인, 뉴스, 야구장소개, 티켓페이지
    - 이미지 및 폰트 등 static 연결

- fastapi 및 DB 연결, 필요 라이브러리 설치
    - requirements.txt
    - mongodb 사용 결정

<h3>6월 24일</h3>

- 네이버 API 이용 뉴스 크롤러 제작
    - '야구' 키워드를 가진 스포츠 뉴스만 수집하도록('link' 칼럼 내 문자열이용)
    - mongodb 및 뉴스 DB에 들어갈 칼럼 별 유형 설정

- news.html 수정
    - 날짜 별로 뉴스가 노출되는 형식으로 변경
    - 더보기 버튼 추가, 클릭 시 리스트 연장되어 노출

<h3>6월 25일</h3>

- mongodb 연결 및 저장 확인 예정
- news.html에 mongodb에 저장된 뉴스 리스트 노출되도록 연결
