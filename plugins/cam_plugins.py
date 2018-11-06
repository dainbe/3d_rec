#coding:utf-8
from slackbot.bot import respond_to, listen_to
from slacker import Slacker
import datetime
import os
import sys
sys.path.append('../')
from movie_rec import Movie
from slackbot_settings import API_TOKEN

bot_status_file='/home/pi/3d_rec/bot_status.txt'

token = API_TOKEN
slacker = Slacker(token)
movie=Movie()

c_name='チャンネル名'

@listen_to(u'(調子|ちょうし)+.*(どう)+')
@respond_to(u'(調子|ちょうし)+.*(どう)+')
def check_order(message,*something):
    userID = message.channel._client.users[message.body['user']][u'id']

    dt = datetime.datetime.now()
    dt_str = dt.strftime("%Y/%m/%d %H:%M:%S")

    message.reply('撮影します。')

    f_name=movie.get_movie()
    message.reply('こんな感じです。')
    slacker.files.upload(f_name, channels=[c_name], title='{}'.format(dt_str))

    os.remove(f_name)

@respond_to('起動+(.*)')
def bot_active(message,something):
    now=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    with open(bot_status_file, 'r') as f:
        for row in f:
            hoge=int(row.strip())
            bot_status=hoge
    if bot_status == 0:
        with open(bot_status_file,'w') as f:
            f.write('1')
        movie.start()
        message.reply('起動しました。\n{}\n1時間ごとに送信します。'.format(now))

    else:
        message.reply('既に起動しています。')

@respond_to('停止+(.*)')
def bot_deactive(message,something):
    now=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    with open(bot_status_file,'r') as f:
        for row in f:
            hoge=int(row.strip())
            bot_status=hoge
    if bot_status == 1:
        with open(bot_status_file,'w') as f:
            f.write('0')
        movie.stop()
        message.reply('{}\n停止しました。'.format(now))

    else:
        message.reply('既に停止しています。')
