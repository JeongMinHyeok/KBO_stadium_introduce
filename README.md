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

<details>
<summary>7월 1일</summary>

- KBO 홈페이지에서 경기 일정 크롤러 제작
    - 하루에 3번 이하로 크롤링할 것 같아 비동기 사용하지 않음
    - 초기 기획은 request 사용하는 것이었으나, 월별 일정도 수집해야 해 편의상 selenium 사용
    - 월별 크롤러 제작 완료(3~11월 수집속도 약 20초)
    - DB 연결 및 저장 확인

- 경기 일정 크롤러 작동 함수 scheduler에 추가

- '&quot;' html 라이브러리 불러와 처리
- 더보기 버튼 임시 제거 (추후 하루 동안의 뉴스 수집량 파악한 뒤 기능 활용예정)

- 추후 개발 방향
    - 경기 일정 ticket.html에 노출되도록 코드 수정
        - ticket.html UI/UX 수정 필요 (월 별로 일정 노출되도록)
    - 홈 경기 별 티켓예매 페이지에 연결되도록 설정

</details>

<details>
<summary>7월 4일</summary>

- 경기 일정 크롤러 수정
    - text를 df로 만드는 대신 table 세부 항목까지 크롤링하여 데이터가 없는 상황 고려
    - 코드 최적화, 크롤링 시간 단축

- DB 저장 코드 수정
    - 리스트 정의하는 순서 수정하여 3월~11월 모든 데이터 DB에 저장하도록 수정

- ticket.html 수정
    - 첫 진입시 현재 날짜 파악하여 해당 월 노출되도록 설정
    - 경기 일정 노출위해 서버에서 데이터 불러오도록 설정
    - Dropdown으로 월 설정 시 해당 월 데이터만 불러오도록 수정
    - 날짜 별로 묶어서 경기일정 테이블 노출되도록 설정

- 추후 개발 방향
    - 홈 경기 별 티켓예매 페이지에 연결되도록 설정

</details>

<details>
<summary>7월 5일</summary>

- 홈 경기 별 티켓예매 페이지에 연결되도록 설정
    - 티켓예매 칼럼 추가
    - 티켓예매 링크 연결 버튼 추가
    - 경기 별 홈구장 파악할 수 있도록 DB에 해당 칼럼 추가
    - 홈구장에 해당하는 예매 링크로 연결하도록 설정

</details>
