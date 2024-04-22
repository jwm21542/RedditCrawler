# RedditCrawler
### Because Reddit API is so difficult to acquire, I created a Reddit web crawler/scraper using Selenium to pull comments and comment info from specified subreddits.

### Required Libaries:
- Selenium
- Webdriver Manager
- user_agent

```
pip install webdriver-manager
pip install -U selenium
pip install -U user_agent
```
### Usage:
You can use either the Jupyter notebook file or run the py file from the terminal. To run the py file you will need to update the PATH variable.

The list of subreddits you want to scrape is stored to and called from the SubredditList.xlsx file. You can add or remove from the list as you need to. 

Currently we can only scrape from the last hour, day, week, year, and alltime of the subreddit due to how Reddit website is configured. Change the following line according to how long of a timeframe you require :
```
subreddit_url = f'{sub}/top/?t=week'
```
Instead of 'week' here, put 'hour', 'day', 'year', or 'all'.

### Using ChromeDriver: 
Make sure you have downloaded the latest ChromeDriver file, which you can find [here](https://chromedriver.chromium.org/getting-started), make sure to get the correct one for your OS and Chrome version. It may be necessary to update your Chrome as well.

On line 48, 90 of py file you will see the following line : 
```
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
```

This is to create a driver instance in **Linux**. You will have to change this line if your OS is NOT linux. 

For example, this would be what you would change it to in **Windows**:
```
# Specify the path to the ChromeDriver executable if not added to PATH
chrome_driver_path = 'path/to/chromedriver.exe'

# Create ChromeDriver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)
```

# 레딧 크롤러
### 레딧 API를 획득하기가 매우 어려워서, 지정된 서브레딧에서 댓글 및 댓글 정보를 가져오기 위해 Selenium을 사용한 레딧 웹 크롤러/스크래퍼를 만들었습니다.

### 필요한 라이브러리:
- Selenium
- Webdriver Manager
- user_agent

```
pip install webdriver-manager
pip install -U selenium
pip install -U user_agent
```
### 사용법:
주피터 노트북 파일을 사용하거나 터미널에서 py 파일을 실행할 수 있습니다. py 파일을 실행하려면 PATH 변수를 업데이트해야 합니다.

스크랩하려는 서브레딧 목록은 SubredditList.xlsx 파일에 저장되고 호출됩니다. 필요에 따라 목록을 추가하거나 제거할 수 있습니다.

현재 Reddit 웹사이트의 구성에 따라 마지막 1시간, 1일, 1주, 1년, 그리고 영원히(subreddit의 모든 시간)에서만 스크랩할 수 있습니다. 필요한 시간 범위에 따라 다음 줄을 변경하세요: 
```
subreddit_url = f'{sub}/top/?t=week'
```
여기서 'week' 대신에 'hour', 'day', 'year', 또는 'all'을 넣으세요.


### ChromeDriver 사용전: 
최신 ChromeDriver 파일을 다운로드했는지 확인하십시오. 여기에서 찾을 수 있습니다. 사용 중인 OS 및 Chrome 버전에 맞는 것을 가져오십시오. Chrome을 업데이트해야 할 수도 있습니다.

py 파일의 48, 90번째 줄에서 다음 줄을 볼 수 있습니다:
```
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
```

이것은 **리눅스**에서 드라이버 인스턴스를 만드는 것입니다. 사용 중인 OS가 리눅스가 아닌 경우 이 줄을 변경해야 합니다.

예를 들어, **윈도우**에서는 다음과 같이 변경해야 합니다:
```
# Specify the path to the ChromeDriver executable if not added to PATH
chrome_driver_path = 'path/to/chromedriver.exe'

# Create ChromeDriver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)
```
