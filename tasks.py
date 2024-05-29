import os
import requests
import datetime

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
from amocrm_datas import sorted_datas
from convert_to_png_analytics import plot_chart

load_dotenv()

app = Celery(
    'tasks',
    broker='redis://redis_najot:6379',
    backend='redis://redis_najot:6379'
)

app.conf.beat_schedule = {
    'send_message': {
        'task': 'tasks.send_message_to_user',
        'schedule': crontab(hour=14, minute=18)
    }
}

MBI_CHAT_ID = os.environ.get('MBI_CHAT_ID')
SHER_CHAT_ID = os.environ.get('SHER_CHAT_ID')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
NAJOT_NUR_CHAT_ID = os.environ.get('NAJOT_NUR_CHAT_ID')
NAJOT_NUR_CHAT_ID_2 = os.environ.get('NAJOT_NUR_CHAT_ID_2')

chat_ids = [int(MBI_CHAT_ID), int(SHER_CHAT_ID), int(NAJOT_NUR_CHAT_ID_2), int(NAJOT_NUR_CHAT_ID)]


def seconds_to_hms(seconds):
    td = datetime.timedelta(seconds=seconds)
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = td.seconds % 60
    return f"{hours:02d}", f"{minutes:02d}", f"{seconds:02d}"


@app.task()
def send_message_to_user():
    bot_calls = sorted_datas()
    plot_chart(bot_calls)
    today = (datetime.datetime.today() - datetime.timedelta(days=1)).date()
    message = f"""Xodimlarning {today} kungi hisoboti\n\n"""
    for val in bot_calls:
        hours, minutes, seconds = seconds_to_hms(val['all_duration'])
        successful_calls = val['success']
        unsuccessful_calls = val['no_success']
        qarz_calls = 50 - val['all_calls'] if val['all_calls'] <= 50 else 0
        all_calls = val['all_calls']
        call_in = val['call_in']
        call_out = val['call_out']
        f_money = val.get('balance', 0.0)
        money = f"{f_money:,.0f}".replace(',', '.')
        message += f"""👤 *{val['name']}*:\n  📞Barcha qong'iroqlar: {all_calls}\n  ☎️Davomiyligi: {hours}:{minutes}:{seconds}\n  ✅Ko'tarilgan qo'ngiroqlar: {successful_calls}\n  🔔Kiruvchi qo'ngiroqlar: {call_in}\n  🔕Chiquvchi qo'ngiroqlar: {call_out}\n  🚫Ko'tarilmagan qong'iroqlar: {unsuccessful_calls}\n  💣Qarz qo'ng'iroqlar: {qarz_calls}\n  💰Kirim: {money}\n\n"""

    url = f'https://api.telegram.org/bot{BOT_TOKEN}'
    for chat_id in chat_ids:
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        requests.post(url + '/sendMessage', data)
        with open('calls_chart.png', 'rb') as photo:
            requests.post(url + '/sendPhoto', data={'chat_id': chat_id}, files={'photo': photo})
    return True
