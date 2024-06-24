from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.models import mongodb
from app.models.news import NewsModel
from app.news_crawler import NaverNewsScraper

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="야구장 소개 홈페이지", version="0.0.1")

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

@app.get("/news", response_class=HTMLResponse)
async def stadium(request: Request):
    return templates.TemplateResponse(
        "./news.html",
        {"request": request, "title": "야구장 소개 홈페이지: 뉴스"},
    )

@app.get("/ticket", response_class=HTMLResponse)
async def stadium(request: Request):
    return templates.TemplateResponse(
        "./ticket.html",
        {"request": request, "title": "야구장 소개 홈페이지: 경기 일정 및 티켓 예매"},
    )


# @app.get("/search", response_class=HTMLResponse)
# async def search(request: Request, q: str):
#     # 1. 쿼리에서 검색어 추출
#     keyword = q
#     # 예외처리
#     # 검색어가 없을 경우 사용자에게 검색 요구
#     if not keyword:
#         return templates.TemplateResponse(
#             "./index.html",
#             {"request": request, "title": "콜렉터 북북이"},
#         )
#     # 해당 검색어에 대한 수집 데이터가 이미 DB에 있다면 해당 데이터를 return
#     if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
#         books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
#         return templates.TemplateResponse(
#             "./index.html",
#             {"request": request, "title": "콜렉터 북북이", "books": books},
#         )
#     # 2. 데이터 수집기로 해당 검색어에 대한 데이터 수집
#     naver_book_scraper = NaverBookScraper()
#     books = await naver_book_scraper.search(keyword, 10)
#     book_models = []
#     for book in books:
#         book_model = BookModel(
#             keyword=keyword,
#             publisher=book["publisher"],
#             price=book["discount"],
#             image=book["image"],
#         )
#         book_models.append(book_model)

#     # 3. 수집한 데이터를 DB에 저장
#     await mongodb.engine.save_all(book_models)  # save_all: asyncio의 gather와 같은 기능

#     return templates.TemplateResponse(
#         request=request,
#         context={"title": "콜렉터스 북북이", "keyword": q},
#         name="index.html",
#     )


# @app.on_event("startup")  # 앱이 실행될 때 아래 함수 실행됨
# def on_app_start():
#     """before app starts"""
#     mongodb.connect()


# @app.on_event("shutdown")  # 앱이 종료될 때 아래 함수 실행됨
# def on_app_shutdown():
#     print("bye")
#     """after app shutdown"""
#     mongodb.close()
