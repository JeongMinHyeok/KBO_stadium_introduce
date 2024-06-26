# 한국 야구장 소개 홈페이지 제작

<h2>현재 진행 상황</h2>

<details>
<summary>6월 21일</summary>

- 대략적인 구조 html 파일로 구현
    - 메인, 뉴스, 야구장소개, 티켓페이지
    - 이미지 및 폰트 등 static 연결

- fastapi 및 DB 연결, 필요 라이브러리 설치
    - requirements.txt
    - mongodb 사용 결정

</details>

<details>
<summary>6월 24일</summary>

- 네이버 API 이용 뉴스 크롤러 제작
    - '야구' 키워드를 가진 스포츠 뉴스만 수집하도록('link' 칼럼 내 문자열이용)
    - mongodb 및 뉴스 DB에 들어갈 칼럼 별 유형 설정

- news.html 수정
    - 날짜 별로 뉴스가 노출되는 형식으로 변경
    - 더보기 버튼 추가, 클릭 시 리스트 연장되어 노출

</details>

<details>
<summary>6월 26일</summary>

- 크롤러 정상 작동 확인
- apscheduler 이용 자동으로 주기적 크롤러 실행 로직 제작
- mongodb 연결 및 저장 확인
- 데이터 중복 저장 방지 로직 제작 및 작동 확인
- news.html에 mongodb에 저장된 뉴스 리스트 노출되도록 연결
- news.html에서 받은 날짜를 DB의 pubDate 항목과 비교해 해당 날짜에 맞는 뉴스 Read
- title에 포함된 html 태그 제거 후 노출되도록 필터 제작 ('&quot;' 태그 처리 필요)

- news.html 수정
    - 뉴스 제목과 날짜만 표시되도록 수정
    - 수집된 뉴스 없을 경우 문구 노출
    - 하단 날짜 별 내비게이터 클릭 시 새로고침해 백엔드 상 함수 실행되도록 설정
    - title 노출 및 해당 글자 클릭 시 네이버 링크로 접속되도록 설정

- 추후 개발 방향
    - 정렬 필터 임시 제거, 더보기 버튼 유지에 대한 의견 정리 필요
    - 크롤러 작동 주기 고민
    - 메인화면에 뉴스 노출 방식 기획 필요

</details>
