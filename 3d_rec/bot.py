# coding: utf-8
from slacker import Slacker
from slackbot.bot import Bot
from slackbot.settings import API_TOKEN

bot_status_file='/home/pi/3d_rec/bot_status.txt'

# API token
token = API_TOKEN

# 投稿するチャンネル名
c_name = 'チャンネル名'

# 投稿
slacker = Slacker(token)

try:
    with open(bot_status_file,'x') as f:
        f.write('0')
except FileExistsError:
    pass

try:
    with open(bot_status_file,'x'):
        pass
except FileExistsError:
    pass


def main():
    bot = Bot()
    try:
        slacker.chat.post_message(c_name, '起動しました', as_user=True)
        # botを起動する
        bot.run()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print('start slackbot')
    main()
