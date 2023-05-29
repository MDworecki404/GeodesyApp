from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QStackedWidget
)
from PyQt5.uic.properties import QtCore
from PyQt5.QtCore import Qt
from screeninfo import get_monitors

from methods.TrigonometricLevelling import TrigonometricLevelling
from methods.PolarMethod import PolarMethod



class Menu(QWidget):

    def __init__(self):
        super().__init__()

        self.interface()

    def OpenGeometricLevelling(self, checked):
        self.hide()
        self.w = TrigonometricLevelling()
        self.w.show()

    def OpenPolarMethod(self, checked):
        self.hide()
        self.w = PolarMethod()
        self.w.show()

    def interface(self):

        for m in get_monitors():
            continue
        grid = QGridLayout()

        GeometricLevellingButton = QPushButton("Trigonometric Levelling")
        grid.addWidget(GeometricLevellingButton,0,0)
        GeometricLevellingButton.clicked.connect(self.OpenGeometricLevelling)

        PolarMethodButton = QPushButton("Polar method")
        grid.addWidget(PolarMethodButton, 0, 1)
        PolarMethodButton.clicked.connect(self.OpenPolarMethod)



        self.setLayout(grid)
        width = 800
        height = 600
        self.setGeometry(int(m.width/2-width/2), int(m.height/2-height/2),width, height)
        self.setWindowTitle("GeodesyApp")
        self.show()

if __name__ == '__main__':
    import sys

app = QApplication(sys.argv)
okno = Menu()
sys.exit(app.exec_())
