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


class TrigonometricLevelling(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()


    def interface(self):
        for m in get_monitors():
            continue
        grid = QGridLayout()

        GoBack = QPushButton('Menu')
        grid.addWidget(GoBack, 0, 0)




        # First row
        StationPoint = QLineEdit()
        StationPoint.setPlaceholderText('Station point number')
        grid.addWidget(StationPoint, 1, 0)

        StationPointHeight = QLineEdit()
        StationPointHeight.setPlaceholderText('Station point height [m]')
        grid.addWidget(StationPointHeight, 1, 1)

        InstrumentHeight = QLineEdit()
        InstrumentHeight.setPlaceholderText('Instrument height [m]')
        grid.addWidget(InstrumentHeight, 1, 2)

        PrismHeight = QLineEdit()
        PrismHeight.setPlaceholderText('Prism height [m]')
        grid.addWidget(PrismHeight, 1, 3)

        CalculateButton = QPushButton('Calculate')
        grid.addWidget(CalculateButton,3,3)
        addNewRowButton = QPushButton('Add row')
        grid.addWidget(addNewRowButton, 3,0)

        table = QTableWidget()
        table.setColumnCount(4)
        tableWidth = table.width()
        table.setColumnWidth(0, 220)
        table.setColumnWidth(1, 220)
        table.setColumnWidth(2, 220)
        table.setColumnWidth(3, 220)

        def addRow():
            rowCount = table.rowCount()
            table.insertRow(rowCount)

            columnCount = table.columnCount()
            for row in range(table.rowCount()):
                item = QTableWidgetItem()
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
                table.setItem(row, columnCount-1, item)

        addNewRowButton.clicked.connect(addRow)

        table.setHorizontalHeaderLabels(['Point number', 'Vertical Angle', 'Horizontal distance', 'Point Height'])
        grid.addWidget(table, 2, 0, 1, 4)



        def Calculate():
            table_data = []
            StH = float(StationPointHeight.text())
            InstH = float(InstrumentHeight.text())
            PrismH = float(PrismHeight.text())


            for row in range(table.rowCount()):
                row_data = []
                for column in range(table.columnCount()):
                    item = table.item(row,column)
                    if item is not None:
                        cell_value = item.text()
                        row_data.append(cell_value)
                    else:
                        QMessageBox.warning(None, 'Empty Cell','Cells cannot be empty')
                        return
                table_data.append(row_data)
                if len(row_data) >= 3:
                    V = float(row_data[1])
                    Hd = float(row_data[2])
                    Hp = StH + InstH + (Hd * np.cos(np.radians(V))) - PrismH
                    Hp = round(Hp, 3)

                    item = QTableWidgetItem(f'{str(Hp)}m')
                    table.setItem(row, 3, item)


        CalculateButton.clicked.connect(Calculate)

        self.setLayout(grid)
        width = 1000
        height = 800
        self.setGeometry(int(m.width / 2 - width / 2), int(m.height / 2 - height / 2), width, height)
        self.setWindowIcon(QIcon('kalkulator.png'))
        self.setWindowTitle("Geometric Levelling")
        self.show()
