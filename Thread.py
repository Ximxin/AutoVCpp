import sys
import os
import zipfile
import time
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import QThread, pyqtSignal


class Thread(QThread):
    EmptyOption = pyqtSignal()
    UnzipFile = pyqtSignal()
    Installing = pyqtSignal()
    InstallFinish = pyqtSignal()

    def __init__(self, array):
        super(Thread, self).__init__()
        self.array = array

    def run(self):
        while True:
            self.i = 0
            for key in self.array:
                if self.array[key]:
                    self.i = 1
                    break
            if self.i == 0:
                self.EmptyOption.emit()
                return
            break
        self.UnzipFile.emit()
        unzip = zipfile.ZipFile('VisualCpp/VCpp.zip')
        unzip.extractall('VisualCpp')
        self.Installing.emit()
        os.chdir('VisualCpp')
        for key in self.array:
            if self.array[key]:
                if key == 'vc2008_x86.exe' or key == 'vc2008_x64.exe' or key == 'vc2010_x86.exe' \
                        or key == 'vc2010_x64.exe':
                    install = '/q'
                else:
                    install = 'install /quiet'
                os.popen(key + ' ' + install)
            time.sleep(1)
        self.InstallFinish.emit()