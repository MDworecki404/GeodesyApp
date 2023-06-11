import subprocess
import sys

from PyQt5 import Qt, QtCore
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
    QGridLayout, QTableWidget, QToolBar, QTableWidgetItem, QMessageBox,
)
from PyQt5.QtGui import QIcon
from screeninfo import get_monitors
import numpy as np


class PolarMethod(QWidget):

    def __init__(self):
        super().__init__()

        self.interface()

    def OpenMenu(self):
        subprocess.Popen([sys.executable, "./main.py"])
        self.close()

    def interface(self):
        for m in get_monitors():
            continue
        grid = QGridLayout()

        GoBack = QPushButton('Menu')
        grid.addWidget(GoBack, 0, 0)
        GoBack.clicked.connect(self.OpenMenu)

        StationPoint = QLineEdit()
        StationPoint.setPlaceholderText('Station point')
        grid.addWidget(StationPoint, 1, 0)

        StationX = QLineEdit()
        StationX.setPlaceholderText('X coordinate of the station [m]')
        grid.addWidget(StationX, 1, 1)

        StationY = QLineEdit()
        StationY.setPlaceholderText('Y coordinate of the station [m]')
        grid.addWidget(StationY, 1, 2)

        ReferencePoint1 = QLineEdit()
        ReferencePoint1.setPlaceholderText('First reference point')
        grid.addWidget(ReferencePoint1, 2, 0)

        ReferencePoint1X = QLineEdit()
        ReferencePoint1X.setPlaceholderText('X coordinate of first reference point')
        grid.addWidget(ReferencePoint1X, 2, 1)

        ReferencePoint1Y = QLineEdit()
        ReferencePoint1Y.setPlaceholderText('Y coordinate of first reference point')
        grid.addWidget(ReferencePoint1Y, 2, 2)

        ReferencePoint1Hz = QLineEdit()
        ReferencePoint1Hz.setPlaceholderText('Horizontal angle from station to first reference point')
        grid.addWidget(ReferencePoint1Hz, 2, 3)

        ReferencePoint1Hd = QLineEdit()
        ReferencePoint1Hd.setPlaceholderText('Horizontal distance from station to first reference point')
        grid.addWidget(ReferencePoint1Hd, 2, 4)

        ReferencePoint2 = QLineEdit()
        ReferencePoint2.setPlaceholderText('Second reference point')
        grid.addWidget(ReferencePoint2, 3, 0)

        ReferencePoint2X = QLineEdit()
        ReferencePoint2X.setPlaceholderText('X coordinate of second reference point')
        grid.addWidget(ReferencePoint2X, 3, 1)

        ReferencePoint2Y = QLineEdit()
        ReferencePoint2Y.setPlaceholderText('Y coordinate of second reference point')
        grid.addWidget(ReferencePoint2Y, 3, 2)

        ReferencePoint2Hz = QLineEdit()
        ReferencePoint2Hz.setPlaceholderText('Horizontal angle from station to second reference point')
        grid.addWidget(ReferencePoint2Hz, 3, 3)

        ReferencePoint2Hd = QLineEdit()
        ReferencePoint2Hd.setPlaceholderText('Horizontal distance from station to second reference point')
        grid.addWidget(ReferencePoint2Hd, 3, 4)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setColumnWidth(0, 220)
        table.setColumnWidth(1, 220)
        table.setColumnWidth(2, 220)
        table.setColumnWidth(3, 220)
        table.setColumnWidth(4, 220)
        table.setColumnWidth(5, 220)

        table.setHorizontalHeaderLabels(['Point number', 'Horizontal Angle', 'Horizontal distance', 'Xp', 'Yp'])
        grid.addWidget(table, 4, 0, 1, 5)

        CalculateButton = QPushButton('Calculate')
        grid.addWidget(CalculateButton, 5, 4)
        addNewRowButton = QPushButton('Add row')
        grid.addWidget(addNewRowButton, 5, 0)
        removeRowButton = QPushButton('Remove row')
        grid.addWidget(removeRowButton, 5, 1)

        def addRow():
            rowCount = table.rowCount()
            table.insertRow(rowCount)

            columnCount = table.columnCount()
            for row in range(table.rowCount()):
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)

                item2 = QTableWidgetItem()
                item2.setFlags(item2.flags() & ~QtCore.Qt.ItemIsEditable)
                item2.setFlags(item2.flags() & ~QtCore.Qt.ItemIsSelectable)

                table.setItem(row, columnCount - 1, item)
                table.setItem(row, columnCount - 2, item2)

        addNewRowButton.clicked.connect(addRow)

        def removeRow():
            rowCount = table.rowCount()
            if rowCount > 0:
                table.removeRow(rowCount - 1)

        removeRowButton.clicked.connect(removeRow)

        def Calculate():
            table_data = []

            for row in range(table.rowCount()):
                row_data = []
                for column in range(table.columnCount()):
                    item = table.item(row, column)
                    if item is not None:
                        cell_value = item.text()
                        row_data.append(cell_value)
                    else:
                        QMessageBox.warning(None, 'Empty Cell', 'Cells cannot be empty')
                        return
                table_data.append(row_data)
                if len(row_data) >= 3:
                    StX = float(StationX.text())
                    StY = float(StationY.text())
                    Ref1X = float(ReferencePoint1X.text())
                    Ref1Y = float(ReferencePoint1Y.text())
                    Ref1Hz = float(ReferencePoint1Hz.text())
                    Ref1Hd = float(ReferencePoint1Hd.text())
                    Ref2X = float(ReferencePoint2X.text())
                    Ref2Y = float(ReferencePoint2Y.text())
                    Ref2Hz = float(ReferencePoint2Hz.text())
                    Ref2Hd = float(ReferencePoint2Hd.text())

                    PHz = float(row_data[1])
                    PHd = float(row_data[2])

                    Azimuth_St_Ref1 = np.arctan((Ref1Y - StY) / (Ref1X - StX))
                    Azimuth_St_Ref1 = Azimuth_St_Ref1 * 180 / np.pi
                    Azimuth_St_Ref1 = abs(Azimuth_St_Ref1 * 400 / 360)

                    if (Ref1Y - StY) >= 0 and (Ref1X - StX) >= 0:
                        Azimuth_St_Ref1 = Azimuth_St_Ref1
                    elif (Ref1Y - StY) >= 0 and (Ref1X - StX) <= 0:
                        Azimuth_St_Ref1 = 200 - Azimuth_St_Ref1
                    elif (Ref1Y - StY) <= 0 and (Ref1X - StX) <= 0:
                        Azimuth_St_Ref1 = 200 + Azimuth_St_Ref1
                    elif (Ref1Y - StY) <= 0 and (Ref1X - StX) >= 0:
                        Azimuth_St_Ref1 = 400 - Azimuth_St_Ref1

                    Azimuth_St_Ref2 = np.arctan((Ref2Y - StY) / (Ref2X - StX))
                    Azimuth_St_Ref2 = Azimuth_St_Ref2 * 180 / np.pi
                    Azimuth_St_Ref2 = abs(Azimuth_St_Ref2 * 400 / 360)

                    if (Ref2Y - StY) >= 0 and (Ref2X - StX) >= 0:
                        Azimuth_St_Ref2 = Azimuth_St_Ref2
                    elif (Ref2Y - StY) >= 0 and (Ref2X - StX) <= 0:
                        Azimuth_St_Ref2 = 200 - Azimuth_St_Ref2
                    elif (Ref2Y - StY) <= 0 and (Ref2X - StX) <= 0:
                        Azimuth_St_Ref2 = 200 + Azimuth_St_Ref2
                    elif (Ref2Y - StY) <= 0 and (Ref2X - StX) >= 0:
                        Azimuth_St_Ref2 = 400 - Azimuth_St_Ref2

                    Azimuth0_St_Ref1 = Azimuth_St_Ref1 - Ref1Hz
                    Azimuth0_St_Ref2 = Azimuth_St_Ref2 - Ref2Hz

                    Azimuth0_St_P = (Azimuth_St_Ref2 + Azimuth0_St_Ref2) / 2 + PHz
                    Azimuth0_St_P = (Azimuth0_St_P * 360 / 400) * np.pi / 180

                    Xp = StX + PHd * np.cos(Azimuth0_St_P)
                    Yp = StY + PHd * np.sin(Azimuth0_St_P)

                    item = QTableWidgetItem(f'{str(Xp)}m')
                    table.setItem(row, 3, item)
                    item2 = QTableWidgetItem(f'{str(Yp)}m')
                    table.setItem(row, 4, item2)

        CalculateButton.clicked.connect(Calculate)

        self.setLayout(grid)
        width = 1200
        height = 800
        self.setGeometry(int(m.width / 2 - width / 2), int(m.height / 2 - height / 2), width, height)
        self.setWindowTitle("Polar method")
        self.show()
