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
    {"name": "경산초등학교", "url": "https://school.gyo6.net/gyeongsanes/na/ntt/selectNttList.do?mi=133988&bbsId=56143"},
    {"name": "경산동부초등학교", "url": "https://school.gyo6.net/ksdongbues/na/ntt/selectNttList.do?mi=151714&bbsId=55643"},
    {"name": "경산서부초등학교", "url": "https://school.gyo6.net/gssb/na/ntt/selectNttList.do?mi=130197&bbsId=55692"},
    {"name": "경산중앙초등학교", "url": "https://school.gyo6.net/gsja/na/ntt/selectNttList.do?mi=129869&bbsId=23189"},
    {"name": "경산압량초등학교", "url": "https://school.gyo6.net/ar/na/ntt/selectNttList.do?mi=104846&bbsId=28021"},
    {"name": "경산계당초등학교", "url": "https://school.gyo6.net/kyedang/na/ntt/selectNttList.do?mi=152585&bbsId=55365"},
    {"name": "경산금락초등학교", "url": "https://school.gyo6.net/gumrak/na/ntt/selectNttList.do?mi=132275&bbsId=55415"},
    {"name": "경산남산초등학교", "url": "https://school.gyo6.net/kns/na/ntt/selectNttList.do?mi=151120&bbsId=55466"},
    {"name": "경산남성초등학교", "url": "https://school.gyo6.net/namseong/na/ntt/selectNttList.do?mi=158049&bbsId=38284"},
    {"name": "경산남천초등학교", "url": "https://school.gyo6.net/n1000es/na/ntt/selectNttList.do?mi=156878&bbsId=55531"},
    {"name": "경산다문초등학교", "url": "https://school.gyo6.net/damun/na/ntt/selectNttList.do?mi=114537&bbsId=23302"},
    {"name": "경산대동초등학교", "url": "https://school.gyo6.net/gsdaedonges/na/ntt/selectNttList.do?mi=129645&bbsId=25827"},
    {"name": "경산봉황초등학교", "url": "https://school.gyo6.net/bonghwang-ks/na/ntt/selectNttList.do?mi=106505&bbsId=55744"},
    {"name": "경산부림초등학교", "url": "https://school.gyo6.net/burymes/na/ntt/selectNttList.do?mi=107919&bbsId=24996"},
    {"name": "경산사동초등학교", "url": "https://school.gyo6.net/ksd/na/ntt/selectNttList.do?mi=151625&bbsId=23438"},
    {"name": "경산삼성현초등학교", "url": "https://school.gyo6.net/gbssh/na/ntt/selectNttList.do?mi=122493&bbsId=27925"},
    {"name": "경산성암초등학교", "url": "https://school.gyo6.net/seongam/na/ntt/selectNttList.do?mi=174273&bbsId=11032"},
    {"name": "경산옥곡초등학교", "url": "https://school.gyo6.net/gsokes/na/ntt/selectNttList.do?mi=130047&bbsId=66851"},
    {"name": "경산와촌초등학교", "url": "https://school.gyo6.net/wachon/na/ntt/selectNttList.do?mi=185091&bbsId=55801"},
    {"name": "경산용성초등학교", "url": "https://school.gyo6.net/yongseong/na/ntt/selectNttList.do?mi=195992&bbsId=15961"},
    {"name": "경산임당초등학교", "url": "https://school.gyo6.net/imdang/na/ntt/selectNttList.do?mi=142096&bbsId=35546"},
    {"name": "경산자인초등학교", "url": "https://school.gyo6.net/jain/na/ntt/selectNttList.do?mi=143894&bbsId=25470"},
    {"name": "경산장산초등학교", "url": "https://school.gyo6.net/jsan/na/ntt/selectNttList.do?mi=147546&bbsId=117116"},
    {"name": "경산정평초등학교", "url": "https://school.gyo6.net/jeongpyeong/na/ntt/selectNttList.do?mi=145540&bbsId=66962"},
    {"name": "경산진량초등학교", "url": "https://school.gyo6.net/jillyang/na/ntt/selectNttList.do?mi=147308&bbsId=55939"},
    {"name": "경산청천초등학교", "url": "https://school.gyo6.net/cheongcheon/na/ntt/selectNttList.do?mi=109536&bbsId=56078"},
    {"name": "경산평산초등학교", "url": "https://school.gyo6.net/psps/na/ntt/selectNttList.do?mi=167690&bbsId=12484"},
    {"name": "경산하양초등학교", "url": "https://school.gyo6.net/hayanges/na/ntt/selectNttList.do?mi=136232&bbsId=37121"},
    {"name": "경산현흥초등학교", "url": "https://school.gyo6.net/hhes/na/ntt/selectNttList.do?mi=137345&bbsId=56254"},
]

import requests
from bs4 import BeautifulSoup
import os
import datetime
import pytz
import time # [추가] 시간 조절을 위한 도구

# 깃허브 금고에서 꺼내쓰기
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

# ==========================================
# [설정] 감시할 게시판 목록 (여기에 30개를 다 넣으세요)
# 형식: {"name": "게시판이름", "url": "주소"},
# ==========================================
TARGET_BOARDS = [
    {"name": "경산초등학교", "url": "https://school.gyo6.net/gyeongsanes/na/ntt/selectNttList.do?mi=133988&bbsId=56143"},
    {"name": "경산동부초등학교", "url": "https://school.gyo6.net/ksdongbues/na/ntt/selectNttList.do?mi=151714&bbsId=55643"},
    {"name": "경산서부초등학교", "url": "https://school.gyo6.net/gssb/na/ntt/selectNttList.do?mi=130197&bbsId=55692"},
    {"name": "경산중앙초등학교", "url": "https://school.gyo6.net/gsja/na/ntt/selectNttList.do?mi=129869&bbsId=23189"},
    {"name": "경산압량초등학교", "url": "https://school.gyo6.net/ar/na/ntt/selectNttList.do?mi=104846&bbsId=28021"},
    {"name": "경산계당초등학교", "url": "https://school.gyo6.net/kyedang/na/ntt/selectNttList.do?mi=152585&bbsId=55365"},
    {"name": "경산금락초등학교", "url": "https://school.gyo6.net/gumrak/na/ntt/selectNttList.do?mi=132275&bbsId=55415"},
    {"name": "경산남산초등학교", "url": "https://school.gyo6.net/kns/na/ntt/selectNttList.do?mi=151120&bbsId=55466"},
    {"name": "경산남성초등학교", "url": "https://school.gyo6.net/namseong/na/ntt/selectNttList.do?mi=158049&bbsId=38284"},
    {"name": "경산남천초등학교", "url": "https://school.gyo6.net/n1000es/na/ntt/selectNttList.do?mi=156878&bbsId=55531"},
    {"name": "경산다문초등학교", "url": "https://school.gyo6.net/damun/na/ntt/selectNttList.do?mi=114537&bbsId=23302"},
    {"name": "경산대동초등학교", "url": "https://school.gyo6.net/gsdaedonges/na/ntt/selectNttList.do?mi=129645&bbsId=25827"},
    {"name": "경산봉황초등학교", "url": "https://school.gyo6.net/bonghwang-ks/na/ntt/selectNttList.do?mi=106505&bbsId=55744"},
    {"name": "경산부림초등학교", "url": "https://school.gyo6.net/burymes/na/ntt/selectNttList.do?mi=107919&bbsId=24996"},
    {"name": "경산사동초등학교", "url": "https://school.gyo6.net/ksd/na/ntt/selectNttList.do?mi=151625&bbsId=23438"},
    {"name": "경산삼성현초등학교", "url": "https://school.gyo6.net/gbssh/na/ntt/selectNttList.do?mi=122493&bbsId=27925"},
    {"name": "경산성암초등학교", "url": "https://school.gyo6.net/seongam/na/ntt/selectNttList.do?mi=174273&bbsId=11032"},
    {"name": "경산옥곡초등학교", "url": "https://school.gyo6.net/gsokes/na/ntt/selectNttList.do?mi=130047&bbsId=66851"},
    {"name": "경산와촌초등학교", "url": "https://school.gyo6.net/wachon/na/ntt/selectNttList.do?mi=185091&bbsId=55801"},
    {"name": "경산용성초등학교", "url": "https://school.gyo6.net/yongseong/na/ntt/selectNttList.do?mi=195992&bbsId=15961"},
    {"name": "경산임당초등학교", "url": "https://school.gyo6.net/imdang/na/ntt/selectNttList.do?mi=142096&bbsId=35546"},
    {"name": "경산자인초등학교", "url": "https://school.gyo6.net/jain/na/ntt/selectNttList.do?mi=143894&bbsId=25470"},
    {"name": "경산장산초등학교", "url": "https://school.gyo6.net/jsan/na/ntt/selectNttList.do?mi=147546&bbsId=117116"},
    {"name": "경산정평초등학교", "url": "https://school.gyo6.net/jeongpyeong/na/ntt/selectNttList.do?mi=145540&bbsId=66962"},
    {"name": "경산진량초등학교", "url": "https://school.gyo6.net/jillyang/na/ntt/selectNttList.do?mi=147308&bbsId=55939"},
    {"name": "경산청천초등학교", "url": "https://school.gyo6.net/cheongcheon/na/ntt/selectNttList.do?mi=109536&bbsId=56078"},
    {"name": "경산평산초등학교", "url": "https://school.gyo6.net/psps/na/ntt/selectNttList.do?mi=167690&bbsId=12484"},
    {"name": "경산하양초등학교", "url": "https://school.gyo6.net/hayanges/na/ntt/selectNttList.do?mi=136232&bbsId=37121"},
    {"name": "경산현흥초등학교", "url": "https://school.gyo6.net/hhes/na/ntt/selectNttList.do?mi=137345&bbsId=56254"},    
    # ... 이런 식으로 콤마(,) 찍고 계속 추가하시면 됩니다 ...
]
# ==========================================

def send_telegram_message(text):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.get(url, params={'chat_id': CHAT_ID, 'text': text})
    except:
        pass

def check_school_notice():
    korea_timezone = pytz.timezone('Asia/Seoul')
    today = datetime.datetime.now(korea_timezone).strftime("%Y.%m.%d")
    
    print(f"📅 기준 날짜: {today}")
    print(f"총 {len(TARGET_BOARDS)}개의 게시판을 검사합니다.")
    print("------------------------------------------------")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    found_count = 0

    # enumerate를 쓰면 순번(i)을 알 수 있습니다.
    for i, board in enumerate(TARGET_BOARDS):
        # 진행 상황 표시 (예: [1/30] 공지사항 확인 중...)
        print(f"[{i+1}/{len(TARGET_BOARDS)}] {board['name']} 확인 중...", end=" ")
        
        try:
            response = requests.get(board['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.select('tbody tr')
            
            board_found = False # 이 게시판에서 찾았는지 여부
            
            for row in rows:
                cols = row.select('td')
                if len(cols) > 4:
                    title = cols[1].get_text().strip()
                    date = cols[4].get_text().strip()
                    
                    if today in date or date in today:
                        if "늘봄" in title or "방과후" in title "외부강사" in title:
                            print(f"\n   >>> ✨ 발견! {title}")
                            msg = f"🔔 [{board['name']}] 오늘자 새 글!\n\n제목: {title}\n날짜: {date}\n\n바로가기: {board['url']}"
                            send_telegram_message(msg)
                            found_count += 1
                            board_found = True
            
            if not board_found:
                print("완료")
                
        except Exception as e:
            print(f"\n   >>> ⚠️ 에러: {e}")

        # [중요] 학교 서버 보호를 위해 1초 쉽니다.
        time.sleep(1) 

    print("------------------------------------------------")
    print(f"✅ 검사 종료. 총 {found_count}개의 알림을 보냈습니다.")

if __name__ == "__main__":
    check_school_notice()
