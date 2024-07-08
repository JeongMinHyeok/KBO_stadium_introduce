from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bleach import clean
from datetime import datetime
import html
from pathlib import Path
from pydantic import BaseModel
from app.models import mongodb
from app.models.news import NewsModel
from app.models.calender import CalenderModel
from app.models.notice import NoticeModel
from app.schedule_job import collect_news_data, collect_game_calender

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="야구장 소개 홈페이지", version="0.0.1")

scheduler = AsyncIOScheduler()

# 정적 파일 경로 설정
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "야구장 소개 홈페이지"},
    )

@app.get("/stadium", response_class=HTMLResponse)
async def stadium(request: Request):
    return templates.TemplateResponse(
        "stadium.html",
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
async def ticket(request: Request, month: str):
    if await mongodb.engine.find_one(CalenderModel, CalenderModel.month == month):
        schedule_data = {}
        ticket_url = {'키움': 'https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07001&TeamCode=PB003',
                      '두산': 'https://ticket.interpark.com/Contents/Sports/GoodsInfo?SportsCode=07001&TeamCode=PB004',
                      'LG': 'https://www.ticketlink.co.kr/sports/baseball/59#reservation',
                      'KT': 'https://www.ticketlink.co.kr/sports/baseball/62#reservation',
                      'SG': 'https://www.ticketlink.co.kr/sports/baseball/476#reservation',
                      'IA': 'https://www.ticketlink.co.kr/sports/baseball/58#reservation',
                      '삼성': 'https://www.ticketlink.co.kr/sports/baseball/57#reservation',
                      '한화': 'https://www.ticketlink.co.kr/sports/baseball/63#reservation',
                      '롯데': 'https://www.giantsclub.com/html/?pcode=339',
                      'NC': 'https://ticket.ncdinos.com/login'}
        schedules = await mongodb.engine.find(CalenderModel, CalenderModel.month == month)
        for schedule in schedules:
            if schedule.date not in schedule_data:
                schedule_data[schedule.date] = []

            game_info = {
                'time': schedule.time,
                'game': schedule.game,
                'tv': schedule.tv,
                'stadium': schedule.stadium,
                'note': schedule.note,
                'ticket': ticket_url[schedule.home_team]
            }
            schedule_data[schedule.date].append(game_info)

        return templates.TemplateResponse(
            "ticket.html",
            {"request": request, "schedule": schedule_data, "month": month, "title": "야구장 소개 홈페이지: 경기 일정 및 티켓 예매"},
        )
    
    else:
        return templates.TemplateResponse(
            "ticket.html",
            {"request": request, "month": month, "title": "야구장 소개 홈페이지: 경기 일정 및 티켓 예매"},
        )

class PostCreate(BaseModel):
    title: str
    content: str

@app.get("/community", response_class=HTMLResponse)
async def community(request: Request):
    posts = await mongodb.engine.find(NoticeModel)
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "posts": posts, "title": "야구장 소개 홈페이지"},
    )

@app.get("/community/read/{post_id}", response_class=HTMLResponse)
async def notice_read(request: Request, post_id: str):
    post = await mongodb.engine.find_one(NoticeModel, NoticeModel.id == post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "post": post, "title": "야구장 소개 홈페이지"}
    )

@app.get("/community/create", response_class=HTMLResponse)
async def get_create_page(request: Request):
    return templates.TemplateResponse(
        "create.html",
        {"request": request, "title": "게시글 작성"}
    )

@app.post("/community/create", response_class=HTMLResponse)
async def notice_create(request: Request, title: str = Form(...), content: str = Form(...)):
    new_post = NoticeModel(title=title, content=content)
    await mongodb.engine.save(new_post)
    posts = await mongodb.engine.find(NoticeModel)
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "posts": posts, "title": "야구장 소개 홈페이지"},
    )

@app.put("/community/read/{post_id}")
async def notice_update(request: Request, post_id: str, post: PostCreate):
    existing_post = await mongodb.engine.find_one(NoticeModel, NoticeModel.id == post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.updated_at = datetime.now()
    await mongodb.engine.save(existing_post)
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "existing_post": existing_post, "title": "야구장 소개 홈페이지"},
    )

@app.delete("/community/read/{post_id}")
async def notice_delete(request: Request, post_id: str):
    post = await mongodb.engine.find_one(NoticeModel, NoticeModel.id == post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await mongodb.engine.delete(post)
    return templates.TemplateResponse(
        "community.html",
        {"request": request, "title": "야구장 소개 홈페이지"}
    )



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
