import urllib.request # 웹(API) 요청을 보내기 위한 라이브러리
import json           # JSON 데이터 처리를 위한 라이브러리
import datetime       # 현재 날짜 및 시간 처리를 위한 라이브러리
import asyncio        # 비동기 실행을 위한 라이브러리
from telegram import Bot # 텔레그램 봇 기능을 사용하기 위한 라이브러리

telegram_id = '8566822956' # 텔레그램 사용자(chat) ID
my_token = '8622003880:AAEZtYyVyJgWHvwO80K6ZSZihh_LkG4X1rU' # BotFather에서 발급받은 텔레그램 봇 토큰
api_key = 'd48240c3013a6a01eaac201e986231b9' # OpenWeatherMap API 키


bot = Bot(token=my_token) # 발급받은 토큰을 이용하여 텔레그램 봇 객체 생성

ALERT_HOURS = [7, 10, 13, 16, 19, 22]    # 정각 기준으로 날씨 정보를 전송할 시간 목록                         
ALERT_TIMES = ["11:30", "11:31"]    # 추가적으로 지정한 알림 시간 목록                                      

def getWeather(): 
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"   # OpenWeatherMap API 요청 URL 생성

    with urllib.request.urlopen(url) as r:  # API 서버에 요청을 보내고 응답 데이터 수신
        data = json.loads(r.read())   # 응답 데이터를 JSON 형식으로 변환

    text = ""  # 텔레그램으로 전송할 문자열 초기화
    for i in range(8):  # 8개의 예보 데이터 반복 처리
        item = data['list'][i]  # i번째 예보 데이터 추출
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)   # UTC 시간을 한국 시간(KST)으로 변환 후 두 자리 문자열로 저장
        temp = item['main']['temp'] # 기온 정보 추출
        humi = item['main']['humidity'] # 습도 정보 추출
        desc = item['weather'][0]['description'] # 날씨 상태 정보 추출
        text += f"({hour}h {temp}C {humi}% {desc})\n" # 추출한 데이터를 문자열 형태로 추가

    return text   # 완성된 날씨 정보 문자열 반환

async def main(): # 비동기 메인 함수
    try:
        while True:  # 프로그램을 계속 실행하기 위한 무한 반복문
            now = datetime.datetime.now() # 현재 시간 가져오기
            hm = now.strftime('%H:%M')    # 현재 시간을 시:분 형식 문자열로 저장                               

            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0   # 정각 알림 시간 조건 확인
            is_alert_time = hm in ALERT_TIMES and now.second == 0         # 지정한 특정 시간 조건 확인                      

            if is_alert_hour or is_alert_time:  # 두 조건 중 하나라도 만족하면 실행
                msg = getWeather()   # 날씨 정보 가져오기
                print(msg) # 터미널에 날씨 정보 출력
                await bot.send_message(chat_id=telegram_id, text=msg)    # 텔레그램으로 메시지 전송

            await asyncio.sleep(1) #1초 대기후 반복

    except KeyboardInterrupt: # Ctrl + C 입력 시 프로그램 종료
        pass

asyncio.run(main()) # 비동기 메인 함수 실행