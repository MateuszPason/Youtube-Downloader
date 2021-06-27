from pytube import YouTube
from moviepy.editor import *
import time

user_link = input('Provide video link: ')
yt = YouTube(user_link)

print('Information about video:')
print('Author: ', yt.author)
print('Title: ', yt.title)
print('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(yt.length)))

to_download = yt.streams.get_highest_resolution()

video_to_convert = VideoFileClip(to_download.download('D:/'))
video_to_convert.audio.write_audiofile(os.path.join('D:/' + yt.title + '.mp3'))

# Delete file to convert
video_to_convert.close()
path_to_delete_file = 'D:/' + yt.title.replace('.', '') + '.mp4'
os.remove(path_to_delete_file)
