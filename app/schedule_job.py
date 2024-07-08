from datetime import datetime
import json
from app.models import mongodb
from app.models.news import NewsModel
from app.models.calender import CalenderModel
from app.news_crawler import NaverNewsScraper
from app.game_calender_crawler import GameCalCrawler

async def collect_news_data():
    keyword = "야구" # 야구가 포함된 뉴스만 크롤링
    naver_news_scraper = NaverNewsScraper()
    news = await naver_news_scraper.search(keyword, 10)
    news_list = []
    for n in news:
        # 중복 확인, 중복 데이터일 경우 저장 리스트에 포함하지 않음
        if await mongodb.engine.find_one(NewsModel, NewsModel.link == n["link"]):
            continue
        news_model = NewsModel(
            title= n["title"],
            originallink= n["originallink"],
            link= n["link"],
            description= n["description"],
            pubDate= n["pubDate"] # 'pubDate': 'Wed, 26 Jun 2024'
        )
        news_list.append(news_model)

    # 수집한 데이터가 있을 경우 DB에 저장
    if news_list != []:
        await mongodb.engine.save_all(news_list)
        print('뉴스 데이터 {}건 DB 저장 완료'.format(len(news_list)), datetime.now())

async def collect_game_calender():
    month_list = ['03', '04', '05', '06', '07', '08', '09', '10', '11'] # 월별 경기일정 수집을 위한 dropdown 선택 코드
    await mongodb.engine.remove(CalenderModel)
    game_calender_crawler = GameCalCrawler()
    game_list = []
    for month in month_list:
        game_cal = game_calender_crawler.crawling(month)
        if game_cal == '0': # 데이터가 없는 경우 다음 달로 이동
            continue
        with open('./app/game_schedule/{0}m_calender.json'.format(month), 'r') as f: # json 파일 읽기
            game_cal = json.load(f)
        for game in game_cal:
            calender_model = CalenderModel(
                    month= game['날짜'][:2],
                    date= game['날짜'],
                    time= game['시간'],
                    game= game['경기'],
                    tv= game['TV'],
                    stadium= game['구장'],
                    note= game['비고'],
                    home_team= game['경기'][-2:]
            )
            game_list.append(calender_model)

    await mongodb.engine.save_all(game_list)
    print('경기 일정 DB 저장 완료', datetime.now())