from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bleach import clean
from datetime import datetime
import html
import json
from pathlib import Path
from app.models import mongodb
from app.models.news import NewsModel
from app.models.calender import CalenderModel
from app.news_crawler import NaverNewsScraper
from app.game_calender_crawler import GameCalCrawler

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="야구장 소개 홈페이지", version="0.0.1")

scheduler = AsyncIOScheduler()

# 정적 파일 경로 설정
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "야구장 소개 홈페이지"},
    )

@app.get("/stadium", response_class=HTMLResponse)
async def stadium(request: Request):
    return templates.TemplateResponse(
        "./stadium.html",
        {"request": request, "title": "야구장 소개 홈페이지: 야구장 소개"},
    )

@app.get("/news/{date}", response_class=HTMLResponse)
async def news(request: Request, date: str):
    # DB 형식에 맞게 date 변환
    date_object = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date_object.strftime('%a, %d %b %Y')
    if await mongodb.engine.find_one(NewsModel, NewsModel.pubDate == formatted_date):
        news = await mongodb.engine.find(NewsModel, NewsModel.pubDate == formatted_date)
        for article in news:
            clean_title = clean(article.title, tags=[], attributes={}, strip=True)
            article.title = html.unescape(clean_title)
        return templates.TemplateResponse(
            "news.html",
            {"request": request, "title": "야구장 소개 홈페이지: 뉴스", "news": news, "current_date": date}
        )

    else:
        return templates.TemplateResponse(
            "news.html",
            {"request": request, "title": "야구장 소개 홈페이지: 뉴스", "current_date": date}
    )

@app.get("/ticket/{month}", response_class=HTMLResponse)
async def stadium(request: Request, month: str):
    if await mongodb.engine.find_one(CalenderModel, CalenderModel.date.startswith(month)):
        print(CalenderModel.date)
    return templates.TemplateResponse(
        "./ticket.html",
        {"request": request, "month": month, "title": "야구장 소개 홈페이지: 경기 일정 및 티켓 예매"},
    )

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
    for month in month_list:
        game_cal = game_calender_crawler.crawling(month)
        if game_cal == '0': # 데이터가 없는 경우 다음 달로 이동
            continue
        with open('./app/game_schedule/{0}m_calender.json'.format(month), 'r') as f: # json 파일 읽기
            game_cal = json.load(f)
        game_list = []
        for game in game_cal:
            calender_model = CalenderModel(
                    date= game['날짜'],
                    time= game['시간'],
                    game= game['경기'],
                    tv= game['TV'],
                    stadium= game['구장'],
                    note= game['비고']
            )
            game_list.append(calender_model)

    await mongodb.engine.save_all(game_list)
    print('경기 일정 DB 저장 완료', datetime.now())



# 일정 시간마다 collect_and_store_data 함수 실행
scheduler.add_job(collect_news_data, IntervalTrigger(seconds=1800))  # 30분마다 실행
scheduler.add_job(collect_game_calender, IntervalTrigger(seconds=36000)) # 하루에 두 번정도 수집할 생각
scheduler.start()


@app.on_event("startup")  # 앱이 실행될 때 아래 함수 실행됨
def on_app_start():
    """before app starts"""
    mongodb.connect()
    if not scheduler.running:
        scheduler.start()


@app.on_event("shutdown")  # 앱이 종료될 때 아래 함수 실행됨
def on_app_shutdown():
    print("bye")
    """after app shutdown"""
    scheduler.shutdown()
    mongodb.close()
