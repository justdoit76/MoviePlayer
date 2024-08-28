from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.uic import loadUi
from multimedia import Media
import sys

class Window(QWidget):

    def __init__(self):
        super().__init__()
        loadUi('form.ui', self)        
        self.setWindowTitle('Ocean Coding School')

        self.media = Media(self)
        self.dial.setRange(0,100)
        self.dial.setValue(50)

        self.playtime = ''

        # signals
        self.pb_add.clicked.connect(self.onAdd)
        self.pb_del.clicked.connect(self.onDel)
        
        self.pb_play.clicked.connect(self.onPlay)
        self.pb_stop.clicked.connect(self.onStop)
        self.pb_pau.clicked.connect(self.onPause)
        self.pb_ff.clicked.connect(self.onFF)
        self.pb_prev.clicked.connect(self.onPrev)

        self.dial.valueChanged.connect(self.onDial)
        self.lw.itemDoubleClicked.connect(self.onDbClick)

    def onAdd(self):
        path = QFileDialog.getOpenFileNames(self, '', '', '(Media Files (*.mp3 *.mp4 *.mkv *.avi *.mov)')
        cnt = self.lw.count()

        for file in path[0]:
            lst = file.split('/')
            self.lw.addItem(lst[-1])

        self.media.addMedia(path[0])            

        if cnt==0:
            self.lw.setCurrentRow(0)

    def onDel(self):
        row = self.lw.currentRow()
        self.lw.takeItem(row)
        self.media.delMedia(row)

    def onPlay(self):
        row = self.lw.currentRow()
        self.media.playMedia(row)

    def onStop(self):
        self.media.stopMedia()

    def onPause(self):
        self.media.pauseMedia()

    def onFF(self):
        row = self.lw.currentRow()+1
        if row==self.lw.count():
            row = 0
        self.lw.setCurrentRow(row)
        self.media.ffMedia(row)

    def onPrev(self):
        row = self.lw.currentRow()-1
        if row<0:
            row = self.lw.count()-1
        self.lw.setCurrentRow(row)
        self.media.prevMedia(row)

    def onDial(self):
        val = self.dial.value()
        self.media.volumeMedia(val)

    def onDbClick(self, item):
        self.onPlay()

    def onDC(self, t):        
        self.hsld.setRange(0, t)
        h, m, s = self.hmsFromSecond(t//1000)
        self.playtime = f'{h:02}:{m:02}:{s:02}'

    def onPC(self, pos):
        self.hsld.setValue(pos)        
        h, m, s = self.hmsFromSecond(pos//1000)
        currtime = f'{h:02}:{m:02}:{s:02}'
        self.lb.setText(f'{currtime} / {self.playtime}')        

    def hmsFromSecond(self, sec):
        h = sec//3600
        m = (sec%3600)//60
        s = (sec%3600)%60
        return h, m, s

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())