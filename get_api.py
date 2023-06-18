import json
import os
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "steamnotes.settings")
django.setup()
from django.db import connection
from applist.models import Rank, App

# db 테이블 초기화
with connection.cursor() as cursor:
    cursor.execute("DELETE FROM rank")
    cursor.execute("DELETE FROM app")

# api 불러오기
applist = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/').json()
ranks = requests.get('https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/').json()

# 불러온 데이터를 DB에 저장
# 게임 목록 테이블 생성
app = [App(id=data['appid'], name=data['name']) for data in applist['applist']['apps']]
App.objects.bulk_create(app)

# 순위 테이블 생성
for rank in ranks['response']['ranks']:
    Rank.objects.create(
        rank=rank['rank'],
        app_id=rank['appid'],
        last_week_rank=rank['last_week_rank'],
        peak_in_game=rank['peak_in_game']
    )

print('Data Saved')
