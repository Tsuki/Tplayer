from __future__ import unicode_literals
import os
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        print("debug: " + msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


class Download():
    filename = ""

    def my_hook(self):
        if self['status'] == 'finished':
            print('Done downloading, now converting ...')
            print(self["filename"])
            filename = os.path.splitext(self["filename"])[0] + '.mp3'

    ydl_opts = {
        'format': '140/139',
        'nooverwrites': True,
        'postprocessors': [
            # {'key': 'FFmpegExtractAudio',
            #   'preferredcodec': 'mp3',
            #   'preferredquality': '320'}
            # ,{'key': 'EmbedThumbnail',
            #    'already_have_thumbnail': False}
            {'key': 'MetadataFromTitle',
             'titleformat': '%(title)s'}
            # ,{'key': 'FFmpegMetadata'}
        ],
        'outtmpl': 'mp3/%(id)s.%(ext)s',
        'forcefilename': True,
        'forcethumbnail': True,
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }

    def download(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            infodict = ydl.extract_info(url)
        return infodict
