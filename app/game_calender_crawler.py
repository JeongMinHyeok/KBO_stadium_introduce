from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd

class GameCalCrawler:

    url = "https://www.koreabaseball.com/Schedule/Schedule.aspx"

    def crawling(self, month):
        # selenium 업데이트로 인해 이제 크롬드라이버가 필요없다!
        options = Options()

        options.add_argument("--headless")
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)

        select = Select(driver.find_element(By.ID, "ddlMonth"))
        select.select_by_value(month)
        table = driver.find_element(By.CLASS_NAME, "tbl-type06")
        thead = table.find_element(By.TAG_NAME, "thead") # 테이블 칼럼 부분
        header = thead.text.split() # df에 칼럼으로 쓸 부분 미리 빼놓음
        tbody = table.find_element(By.TAG_NAME, "tbody") # 경기 일정이 있는 부분
        rows = tbody.find_elements(By.TAG_NAME, "tr") # 각 라인 별 데이터 추출
        if len(rows) == 1:
            return '0'

        lines = []
        for value in rows: # 라인 별로 반복문 돌며 데이터 추출
            body = value.find_elements(By.TAG_NAME, "td")
            schedule_list = []
            for b in body:
                schedule_list.append(b.text) # 칼럼 별 데이터들 라인 별로 리스트에 저장
            lines.append(schedule_list) # 각 라인 별 데이터를 한번 더 리스트에 저장

        # 날짜 데이터가 없는 라인을 위해 데이터 핸들링
        data = []
        game_day = None

        for line in lines:
            if line[0].endswith(')'): # 날짜 칼럼 데이터 위치에 ')'로 끝날 경우 날짜 데이터가 있다고 판단
                game_day = line[0] # 해당 날짜 변수에 저장 후 data list에 바로 추가
                data.append(line)
            else:
                line.insert(0, game_day) # 날짜 데이터가 없을 경우 위에서 저장한 날짜 데이터 첫 번째 순서에 추가
                data.append(line)

        df = pd.DataFrame(data, columns=header) # json으로 저장해주기 위해 데이터프레임 생성
        df = df.replace('','-')
        df.to_json('./app/game_schedule/{0}m_calender.json'.format(month), force_ascii = False, orient='records', indent=4)

        driver.quit()

        return '1'

if __name__ == "__main__":
    crawler = GameCalCrawler()
    df = crawler.crawling('07')
    # print(df)