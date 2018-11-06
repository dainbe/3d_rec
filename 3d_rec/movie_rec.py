#coding:utf-8
import threading
import time
import picamera
import datetime
import subprocess
import os.path
import time
import sys

FILEPATH = '/home/pi/3d_rec/'

class Movie():
    def __init__(self):
        self.switch_event = threading.Event() #停止させるかのフラグ

    def start(self):
        #スレッドの作成と開始
        self.thread = threading.Thread(target = self.time_rec)
        self.thread.start()
        print('start')

    def stop(self):
        """スレッドを停止させる"""
        self.switch_event.clear()
        self.thread.join()    #スレッドが停止するのを待つ
        print('stop')

    def get_movie(self,rec_time=10):
        dt = datetime.datetime.now()
        dt_str = dt.strftime("%Y-%m-%d_%H:%M:%S")
        instantfile = FILEPATH + "instant.h264"
        filename=dt_str+'.mp4'

        with picamera.PiCamera() as camera:
            camera.hflip = True
            camera.vflip = True
            camera.resolution = (1024,768)
            camera.brightness = 70
            camera.start_recording(instantfile)
            time.sleep(rec_time)
            camera.stop_recording()

        command = "MP4Box -add instant.h264 {}".format(filename)

        #h264をmp4に変換
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))

        return filename

    def time_rec(self,recdelta=1):
        now=datetime.datetime.now()
        check_time=now + datetime.timedelta(hours=recdelta)

        while True:

            #現在時間の更新
            now= datetime.datetime.now()
            if now.hour == check_time.hour:
                time_stamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                #撮影して返り値としてmp4のファイル名
                f_name=self.get_movie()

                #ファイルのアップロード
                slacker.chat.post_message(c_name, '{}現在こんな感じです。'.format(time_stamp), as_user=True)
                slacker.files.upload(f_name, channels=[c_name], title='{}'.format(time_stamp))

                #1時間後に設定
                check_time=now + datetime.timedelta(hours=1)

                #ファイル削除
                os.remove(f_name)

            time.sleep(10)
