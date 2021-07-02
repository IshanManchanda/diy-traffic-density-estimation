import sys
from PyQt5.QtWidgets import *
from detection.Detection import getOutput
from image_processing.video_write import transformVideo
from simulator import simulateSignal
from image_processing.final_plot import performPlot


class window(QWidget):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        self.fullLayout = QVBoxLayout(self)
        self.resize(600, 200)
        self.browseButton = QPushButton("Browse")
        self.labelBrowse = QLabel("Select input video file for correction: ")
        self.textBrowse = QLineEdit()
        self.textBrowse.setReadOnly(True)
        self.browseButton.clicked.connect(self.getVideoFile)
        self.filename = ['', '']
        self.browseLayout = QHBoxLayout()
        self.browseLayout.addWidget(self.labelBrowse)
        self.browseLayout.addWidget(self.textBrowse)
        self.browseLayout.addWidget(self.browseButton)
        self.angleCorrectionButton = QPushButton('Perform correction')
        self.angleCorrectionButton.clicked.connect(self.angleCorrection)
        self.browseLayout.addWidget(self.angleCorrectionButton)
        self.fullLayout.addLayout(self.browseLayout)

        self.browse1Button = QPushButton("Browse")
        self.label1Browse = QLabel("Select corrected video file: ")
        self.text1Browse = QLineEdit()
        self.text1Browse.setReadOnly(True)
        self.browse1Button.clicked.connect(self.getCorrectedVideoFile)
        self.filename1 = ['', '']
        self.browse1Layout = QHBoxLayout()
        self.browse1Layout.addWidget(self.label1Browse)
        self.browse1Layout.addWidget(self.text1Browse)
        self.browse1Layout.addWidget(self.browse1Button)
        self.outputButton = QPushButton('View output')
        self.outputButton.clicked.connect(self.output)
        self.browse1Layout.addWidget(self.outputButton)
        self.fullLayout.addLayout(self.browse1Layout)

        self.browse2Button = QPushButton("Browse")
        self.label2Browse = QLabel("Select input file: ")
        self.text2Browse = QLineEdit()
        self.text2Browse.setReadOnly(True)
        self.browse2Button.clicked.connect(self.getInputData)
        self.filename2 = ['', '']
        self.browse2Layout = QHBoxLayout()
        self.browse2Layout.addWidget(self.label2Browse)
        self.browse2Layout.addWidget(self.text2Browse)
        self.browse2Layout.addWidget(self.browse2Button)
        self.simulateButton = QPushButton('Simulate')
        self.simulateButton.clicked.connect(self.simulate)
        self.browse2Layout.addWidget(self.simulateButton)
        self.fullLayout.addLayout(self.browse2Layout)
        self.plotButton = QPushButton('Display plot')
        self.plotButton.clicked.connect(self.displayPlot)
        self.fullLayout.addWidget(self.plotButton)

    def getVideoFile(self):
        self.filename = QFileDialog.getOpenFileName(self, "Select video", filter="Video Files (*.avi *.mp4)")
        self.textBrowse.setText(self.filename[0])

    def getCorrectedVideoFile(self):
        self.filename1 = QFileDialog.getOpenFileName(self, "Select corrected video", filter="Video Files (*.avi *.mp4)")
        self.text1Browse.setText(self.filename1[0])

    def getInputData(self):
        self.filename2 = QFileDialog.getOpenFileName(self, "Select input file", filter="Text File (*.txt)")
        self.text2Browse.setText(self.filename2[0])

    def angleCorrection(self):
        if not self.filename[0]:
            errorBox = QMessageBox()
            errorBox.setText("Choose a file")
            errorBox.setIcon(QMessageBox.Critical)
            errorBox.setStandardButtons(QMessageBox.Ok)
            errorBox.exec_()
        else:
            retCode = transformVideo(self.filename[0])
            if retCode:
                msgBox = QMessageBox()
                msgBox.setText("Video successfully transformed")
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()

    def output(self):
        if not self.filename1[0]:
            errorBox = QMessageBox()
            errorBox.setText("Choose a file")
            errorBox.setIcon(QMessageBox.Critical)
            errorBox.setStandardButtons(QMessageBox.Ok)
            errorBox.exec_()
        else:
            retCode = getOutput(self.filename1[0])
            if retCode:
                msgBox = QMessageBox()
                msgBox.setText("Video successfully analyzed")
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()

    def simulate(self):
        if not self.filename2[0]:
            errorBox = QMessageBox()
            errorBox.setText("Choose a file")
            errorBox.setIcon(QMessageBox.Critical)
            errorBox.setStandardButtons(QMessageBox.Ok)
            errorBox.exec_()
        else:
            retCode = simulateSignal(self.filename2[0])
            if retCode:
                msgBox = QMessageBox()
                msgBox.setText("Simulation completed!")
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec_()

    def displayPlot(self):
        performPlot()


def main():
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
