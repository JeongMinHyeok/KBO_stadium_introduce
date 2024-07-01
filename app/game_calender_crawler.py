from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pathlib import Path
import pandas as pd

class GameCalCrawler:

    BASE_DIR = Path(__file__).resolve()
    print(BASE_DIR)

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
        schedule = table.text

        lines = schedule.strip().split('\n')
        if lines[1] == '데이터가 없습니다.': # 해당 월 경기 데이터가 없을 경우
            return '0'
        header = lines[0].split()
        rows = []

        for line in lines[1:]:
            if line.split()[0].endswith(')'): # '날짜' 칼럼 데이터 위치에 ')'로 끝날경우 날짜 데이터로 판단
                date = line.split(' ')[0] # 해당 날짜 저장(아래 데이터에 추가 위함)
                rows.append(line.split(' '))
            else:
                temp = line.split() # 임시 리스트에 저장한 뒤
                temp.insert(0, date) # 위에서 저장한 날짜 데이터 맨 앞에 추가
                rows.append(temp)

        rows.insert(0, header)

        df = pd.DataFrame(rows)
        df = df.rename(columns=df.iloc[0]) # 첫 번째 행을 칼럼명으로 지정
        df = df.drop(df.index[0])
        if df['하이라이트'][1] != '하이라이트':
            df['라디오'] = df['TV']
            df['TV'] = df['하이라이트']
        df = df.fillna('-')
        df = df.drop(['게임센터', '하이라이트', '구장',], axis=1)
        df.rename(columns = {"라디오":"구장"}, inplace=True)

        df.to_json('./app/game_schedule/{0}m_calender.json'.format(month), force_ascii = False, orient='records', indent=4)

        driver.quit()

        return '1'

if __name__ == "__main__":
    crawler = GameCalCrawler()
    df = crawler.crawling('07')
    # print(df)