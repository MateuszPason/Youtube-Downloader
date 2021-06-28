from pytube import YouTube
from moviepy.editor import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import time


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
            selected_format = self.format.currentText()
            user_link = self.source.text()
            yt = YouTube(user_link)
            folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

            # Print information about video
            self.length.setText('Duration: ' + time.strftime('%H:%M:%S', time.gmtime(yt.length)))
            self.title.setText(yt.title)

            if selected_format == 'MP3':
                self.download(folder_path, yt)
                self.convert(folder_path, yt)
            else:
                self.download(folder_path, yt)
        except:
            print('invalid link')

    def download(self, folder_path, yt):
        to_download = yt.streams.get_highest_resolution()
        VideoFileClip(to_download.download(folder_path + '/'))

    def convert(self, folder_path, yt):
        video_to_convert = VideoFileClip(folder_path + '/' + delete_illegal_chars(yt.title) + '.mp4')
        video_to_convert.audio.write_audiofile(os.path.join(folder_path + '/' + delete_illegal_chars(yt.title) +
                                                            '.mp3'))
        # Delete video after conversion
        video_to_convert.close()
        path_to_delete_file = folder_path + '/' + delete_illegal_chars(yt.title) + '.mp4'
        os.remove(path_to_delete_file)


def main():
    app = QApplication(sys.argv)
    main_window = DownloadingComponent()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
