import requests
from bs4 import BeautifulSoup
import os
import datetime
import pytz

# 깃허브 금고에서 꺼내쓰기 (수정하지 마세요)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# 감시할 게시판 목록
TARGET_BOARDS = [
    {
        "name": "경산초등학교",
        "url": "https://school.gyo6.net/gyeongsanes/na/ntt/selectNttList.do?mi=133988&bbsId=56143"
    },
    {
        "name": "경산동부초등학교",
        "url": "https://school.gyo6.net/ksdongbues/na/ntt/selectNttList.do?mi=151714&bbsId=55643"
    },
    {
        "name": "경산서부초등학교",
        "url": "https://school.gyo6.net/gssb/na/ntt/selectNttList.do?mi=130197&bbsId=55692"
    },
    {
        "name": "경산중앙초등학교",
        "url": "https://school.gyo6.net/gsja/na/ntt/selectNttList.do?mi=129869&bbsId=23189"
    },
    {
        "name": "경산압량초등학교",
        "url": "https://school.gyo6.net/ar/na/ntt/selectNttList.do?mi=104846&bbsId=28021"
    },
    {
        "name": "경산계당초등학교",
        "url": "https://school.gyo6.net/kyedang/na/ntt/selectNttList.do?mi=152585&bbsId=55365"
    },
    {
        "name": "경산금락초등학교",
        "url": "https://school.gyo6.net/gumrak/na/ntt/selectNttList.do?mi=132275&bbsId=55415"
    },
    {
        "name": "경산남산초등학교",
        "url": "https://school.gyo6.net/kns/na/ntt/selectNttList.do?mi=151120&bbsId=55466"
    },
    {
        "name": "경산남성초등학교",
        "url": "https://school.gyo6.net/namseong/na/ntt/selectNttList.do?mi=158049&bbsId=38284"
    },
    {
        "name": "경산남천초등학교",
        "url": "https://school.gyo6.net/n1000es/na/ntt/selectNttList.do?mi=156878&bbsId=55531"
    },
    {
        "name": "경산다문초등학교",
        "url": "https://school.gyo6.net/damun/na/ntt/selectNttList.do?mi=114537&bbsId=23302"
    },
    {
        "name": "경산대동초등학교",
        "url": "https://school.gyo6.net/gsdaedonges/na/ntt/selectNttList.do?mi=129645&bbsId=25827"
    },
    {
        "name": "경산봉황초등학교",
        "url": "https://school.gyo6.net/bonghwang-ks/na/ntt/selectNttList.do?mi=106505&bbsId=55744"
    },
    {
        "name": "경산부림초등학교",
        "url": "https://school.gyo6.net/burymes/na/ntt/selectNttList.do?mi=107919&bbsId=24996"
    },
    {
        "name": "경산사동초등학교",
        "url": "https://school.gyo6.net/ksd/na/ntt/selectNttList.do?mi=151625&bbsId=23438"
    },
    {
        "name": "경산삼성현초등학교",
        "url": "https://school.gyo6.net/gbssh/na/ntt/selectNttList.do?mi=122493&bbsId=27925"
    },
    {
        "name": "경산성암초등학교",
        "url": "https://school.gyo6.net/seongam/na/ntt/selectNttList.do?mi=174273&bbsId=11032"
    },
    {
        "name": "경산옥곡초등학교",
        "url": "https://school.gyo6.net/gsokes/na/ntt/selectNttList.do?mi=130047&bbsId=66851"
    },
    {
        "name": "경산와촌초등학교",
        "url": "https://school.gyo6.net/wachon/na/ntt/selectNttList.do?mi=185091&bbsId=55801"
    },
    {
        "name": "경산용성초등학교",
        "url": "https://school.gyo6.net/yongseong/na/ntt/selectNttList.do?mi=195992&bbsId=15961"
    },
    {
        "name": "경산임당초등학교",
        "url": "https://school.gyo6.net/imdang/na/ntt/selectNttList.do?mi=142096&bbsId=35546"
    },
    {
        "name": "경산자인초등학교",
        "url": "https://school.gyo6.net/jain/na/ntt/selectNttList.do?mi=143894&bbsId=25470"
    },
    {
        "name": "경산장산초등학교",
        "url": "https://school.gyo6.net/jsan/na/ntt/selectNttList.do?mi=147546&bbsId=117116"
    },
    {
        "name": "경산정평초등학교",
        "url": "https://school.gyo6.net/jeongpyeong/na/ntt/selectNttList.do?mi=145540&bbsId=66962"
    },
    {
        "name": "경산진량초등학교",
        "url": "https://school.gyo6.net/jillyang/na/ntt/selectNttList.do?mi=147308&bbsId=55939"
    },
    {
        "name": "경산청천초등학교",
        "url": "https://school.gyo6.net/cheongcheon/na/ntt/selectNttList.do?mi=109536&bbsId=56078"
    },
    {
        "name": "경산평산초등학교",
        "url": "https://school.gyo6.net/psps/na/ntt/selectNttList.do?mi=167690&bbsId=12484"
    },
    {
        "name": "경산하양초등학교",
        "url": "https://school.gyo6.net/hayanges/na/ntt/selectNttList.do?mi=136232&bbsId=37121"
    },
    {
        "name": "경산현흥초등학교",
        "url": "https://school.gyo6.net/hhes/na/ntt/selectNttList.do?mi=137345&bbsId=56254"
    }
]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={'chat_id': CHAT_ID, 'text': text})

def check_school_notice():
    # 1. 오늘 날짜 구하기 (한국 시간 기준)
    korea_timezone = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(korea_timezone).strftime("%Y.%m.%d")
    
    print(f"📅 기준 날짜: {today} (오늘 올라온 글만 찾습니다)")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    found_count = 0

    for board in TARGET_BOARDS:
        try:
            response = requests.get(board["url"], headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.select('tbody tr')
            
            for row in rows:
                # 제목과 날짜를 가져옵니다.
                # 보통 학교 홈페이지는 날짜가 4번째나 5번째 칸에 있습니다.
                cols = row.select('td')
                if len(cols) > 3:
                    title = cols[1].get_text().strip() # 제목 (보통 2번째)
                    date = cols[4].get_text().strip()  # 날짜 (보통 5번째)
                    
                    # 날짜 형식이 다를 경우를 대비해 단순 포함 여부 확인
                    # "오늘 날짜가 포함되어 있고" AND "키워드가 있으면"
                    if today in date or date in today:
                        if "늘봄" in title or "방과후" in title:
                            print(f"✨ 발견! [{board['name']}] {title}")
                            msg = f"🔔 [{board['name']}] 오늘자 새 글!\n\n제목: {title}\n날짜: {date}\n\n바로가기: {board['url']}"
                            send_telegram_message(msg)
                            found_count += 1
                            
        except Exception as e:
            print(f"에러 발생: {e}")

    if found_count == 0:
        print("✅ 오늘 올라온 관련 공지는 없습니다.")

if __name__ == "__main__":
    check_school_notice()
