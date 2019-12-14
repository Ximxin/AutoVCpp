import sys
import os
import ctypes

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from AutoVCpp_UI import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from Thread import Thread


class Change_UI(Ui_MainWindow):

    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.ExecuteObject = [self.vc2015to19x86, self.vc2015to19x64, self.vc2013x86, self.vc2013x64, self.vc2012x86,
                              self.vc2012x64, self.vc2010x86, self.vc2010x64, self.vc2008x86, self.vc2008x64]
        self.SelectAll.stateChanged.connect(self.SelectAllOption)
        self.Install.clicked.connect(self.InstallAllOptioned)

    def InstallAllOptioned(self):
        self.Install.setDisabled(True)
        self.InstallThread = Thread({'vc2015-2019_x86.exe': self.vc2015to19x86.isChecked(),
                                     'vc2015-2019_x64.exe': self.vc2015to19x64.isChecked(),
                                     'vc2013_x86.exe': self.vc2013x86.isChecked(),
                                     'vc2013_x64.exe': self.vc2013x64.isChecked(),
                                     'vc2012_x86.exe': self.vc2012x86.isChecked(),
                                     'vc2012_x64.exe': self.vc2012x64.isChecked(),
                                     'vc2010_x86.exe': self.vc2010x86.isChecked(),
                                     'vc2010_x64.exe': self.vc2010x64.isChecked(),
                                     'vc2008_x86.exe': self.vc2008x86.isChecked(),
                                     'vc2008_x64.exe': self.vc2008x64.isChecked()})
        self.InstallThread.EmptyOption.connect(self.EmptyOptionTip)
        self.InstallThread.UnzipFile.connect(self.UnzipFileTip)
        self.InstallThread.Installing.connect(self.InstallingTip)
        self.InstallThread.InstallFinish.connect(self.InstallFinishTip)
        self.InstallThread.start()

    def EmptyOptionTip(self):
        self.InstallTip.setText("你还未选择组件...")
        self.Install.setDisabled(False)

    def UnzipFileTip(self):
        self.InstallTip.setText("正在解压文件...")

    def InstallingTip(self):
        self.InstallTip.setText("正在安装程序，请耐心等待...")

    def InstallFinishTip(self):
        self.InstallTip.setText("安装完成...")
        self.Install.setDisabled(False)

    def SelectAllOption(self):
        if self.SelectAll.isChecked():
            for i in self.ExecuteObject:
                i.setChecked(True)
        else:
            for i in self.ExecuteObject:
                i.setChecked(False)


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    if isAdmin():
        app = QApplication(sys.argv)
        Main = QMainWindow()
        UI = Change_UI(Main)
        Main.setWindowIcon(QIcon("images/favicon.ico"))
        Main.show()
        sys.exit(app.exec_())
    else:
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, __file__, None, 1)
