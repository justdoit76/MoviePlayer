from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QObject, QUrl, pyqtSignal

class Media(QObject):

    dc_signal = pyqtSignal(int)
    pc_signal = pyqtSignal(int)

    def __init__(self, w):
        super().__init__()
        self.parent = w

        self.mp = QMediaPlayer()
        self.ao = QAudioOutput()
        self.ao.setVolume(0.5)
        self.pl = []

        self.mp.setAudioOutput(self.ao)
        self.mp.setVideoOutput(w.vw)

        # signals
        self.mp.durationChanged.connect(self.onDC)
        self.mp.positionChanged.connect(self.onPC)

        # emit signals to widget        
        self.dc_signal.connect(self.parent.onDC)
        self.pc_signal.connect(self.parent.onPC)

    def addMedia(self, files):
        for file in files:            
            url = QUrl.fromLocalFile(file)
            self.pl.append(url)

    def delMedia(self, row):
        del(self.pl[row])        

    def playMedia(self, idx=0):        
        if self.pl:
            if self.mp.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
                self.mp.setSource( self.pl[idx] )
            elif self.mp.playbackState() == QMediaPlayer.PlaybackState.PausedState:
                pass
            self.mp.play()

    def stopMedia(self):
        self.mp.stop()

    def pauseMedia(self):
        self.mp.pause()

    def ffMedia(self, idx=0):
        self.stopMedia()
        self.playMedia(idx)

    def prevMedia(self, idx=0):
        self.stopMedia()
        self.playMedia(idx)

    def volumeMedia(self, vol):
        self.ao.setVolume(vol/100)

    def onDC(self, t):        
        self.dc_signal.emit(t)
        
    def onPC(self, pos):        
        self.pc_signal.emit(pos)