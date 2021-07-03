from pytube import YouTube, exceptions
from moviepy.video.io.VideoFileClip import VideoFileClip
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import time
import pytube
import os
import sys


def delete_illegal_chars(filename):
    illegal_chars = [':', '/', '*', '"', '<', '>', '|', '.', '\'']
    for i in illegal_chars:
        filename = filename.replace(i, '')
    return filename


class DownloadingComponent(QDialog):
    def __init__(self):
        super(DownloadingComponent, self).__init__()
        self.ui = loadUi("interface/mainWindow.ui", self)
        self.pushButton.clicked.connect(self.choose_dir_and_download)

    def choose_dir_and_download(self):
        try:
            user_link = self.source.text()
            yt = YouTube(user_link)
            file_type = self.file_type.currentText()

            # Inform about that file is downloading
            self.completed_info.setText('')
            self.length.setText('')
            self.title_and_download_info.setText('Downloading...')

            folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

            if file_type == 'MP3':
                to_download = yt.streams.filter(only_audio=True).first()
                out_file = to_download.download(output_path=folder_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
            else:
                # if resolution 1080p is available download it, otherwise download the highest available resolution
                if yt.streams.get_by_itag(137) is not None:
                    to_download_video = yt.streams.get_by_itag(137)
                else:
                    to_download_video = yt.streams.get_highest_resolution()
                VideoFileClip(to_download_video.download(folder_path + '/'))

            # Print information about downloaded file
            self.completed_info.setText('Completed: ')
            self.length.setText('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(yt.length)))
            self.title_and_download_info.setText(yt.title)

        except pytube.exceptions.RegexMatchError:
            self.title_and_download_info.setText('Invalid link')


def main():
    app = QApplication(sys.argv)
    main_window = DownloadingComponent()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
