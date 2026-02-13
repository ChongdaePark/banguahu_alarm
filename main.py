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

def send_telegram_message(text):
    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': text}
    try:
        requests.get(send_url, params=params)
    except:
        print("메시지 전송 실패 (인터넷 문제일 수 있습니다)")

def check_school_notice():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🔍 모든 게시판을 검사합니다...")

    headers = {'User-Agent': 'Mozilla/5.0'}

    # 설정한 게시판 목록을 하나씩 돌면서 검사
    for board in TARGET_BOARDS:
        board_name = board["name"]
        url = board["url"]

        # 게시판마다 기억해야 할 파일이 다르므로 파일명을 다르게 만듭니다.
        # 예: sent_logs_공지사항.txt, sent_logs_가정통신문.txt
        log_filename = f"sent_logs_{board_name}.txt"

        # 기록 불러오기
        sent_list = []
        if os.path.exists(log_filename):
            with open(log_filename, "r", encoding="utf-8") as f:
                sent_list = f.read().splitlines()

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.select('tbody tr')

            new_finds_count = 0

            for row in rows:
                link = row.select_one('a')
                if link:
                    title = link.get_text().strip()

                    # 키워드 검사
                    if "늘봄" in title or "방과후" in title or "외부강사" in title:
                        if title not in sent_list:
                            # 찾았다!
                            print(f"✨ [{board_name}] 새로운 글 발견: {title}")

                            message = f"🔔 [{board_name} 알림]\n\n{title}\n\n바로가기: {url}"
                            send_telegram_message(message)

                            sent_list.append(title)
                            new_finds_count += 1

            # 파일 업데이트
            with open(log_filename, "w", encoding="utf-8") as f:
                for item in sent_list:
                    f.write(item + "\n")

            if new_finds_count == 0:
                print(f"   - {board_name}: 새로운 관련 글 없음")

        except Exception as e:
            print(f"⚠️ {board_name} 접속 중 오류 발생: {e}")

    print("✅ 전체 검사 완료. 다음 9시까지 대기합니다.\n")
