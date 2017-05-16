from __future__ import unicode_literals
import os
from pathlib import Path
import youtube_dl
class MyLogger(object):
    def debug(self, msg):
        print("debug: "+msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Download():
    filename = ""
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
            print(d["filename"])
            filename = os.path.splitext(d["filename"])[0]+'.mp3'

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'forcefilename' : True,
        'forcethumbnail' : True,
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    def download(self,url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.extract_info(url)
            print (filename)
        # return filename;
down = Download()
down.download('ioBQzIsgddI')
