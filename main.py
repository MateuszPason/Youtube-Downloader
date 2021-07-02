from pytube import YouTube, exceptions
from moviepy.editor import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import time
import pytube
import os


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

            # Inform about that file is downloading
            self.completed_info.setText('')
            self.length.setText('')
            self.title_and_download_info.setText('Downloading')

            folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

            to_download = yt.streams.get_highest_resolution()
            VideoFileClip(to_download.download(folder_path + '/'))

            video_to_convert = VideoFileClip(folder_path + '/' + delete_illegal_chars(yt.title) + '.mp4')
            video_to_convert.audio.write_audiofile(os.path.join(folder_path + '/' + delete_illegal_chars(yt.title) +
                                                                '.mp3'))

            # Print information about downloaded file
            self.completed_info.setText('Completed: ')
            self.length.setText('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(yt.length)))
            self.title_and_download_info.setText(yt.title)

            self.delete_file(video_to_convert, folder_path, yt)
        except pytube.exceptions.RegexMatchError:
            self.title_and_download_info.setText('Invalid link')

    def delete_file(self, file_to_delete, path, yt):
        file_to_delete.close()
        os.remove(path + '/' + delete_illegal_chars(yt.title) + '.mp4')


def main():
    app = QApplication(sys.argv)
    main_window = DownloadingComponent()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
