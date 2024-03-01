"""
@author: Ulas Sahillioglu
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys
from os import path
from PyQt5.uic import loadUiType
from conv import currency_converter

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons(self)
        self.exchange_rate = currency_converter()
        self.lineEdit = [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
        ]

    def Handel_Buttons(self, parent):
        self.btnCalculate.clicked.connect(self.calculate)
        self.btnClear.clicked.connect(self.clear)

    def clear(self):
        for line in self.lineEdit:
            eval(f"self.lineEdit{line}.clear()")

    def calculate(self):
        quantities = [
            "10",
            "25",
            "50",
            "100",
            "250",
            "500",
            "1000",
            "2500",
            "5000",
            "10000",
            "25000",
            "50000",
            "100000",
            "250000",
            "500000",
        ]

        main_list = []
        website = self.boxWebsite.currentText()
        sm = self.boxSM.currentText()
        product = self.boxProduct.currentText()
        quality = self.boxQuality.currentText()
        country = self.boxCountry.currentText()
        provider = self.lineProvider.text()

        self.tablePrice.setRowCount(0)
        self.tablePrice.setColumnCount(10)  # Set to the number of columns in your data

        for index, quantity in enumerate(quantities):

            try:
                line_edit = self.findChild(QLineEdit, f"lineEdit{index+1}")
                our_price = float(line_edit.text())
                srv_price = float(self.lineSrvPrice.text())
                cost = round((int(quantity) * srv_price / 1000), 5)
                print(f"cost: {cost:.6f}")
                percentage = format((cost * 100) / our_price, ".3f")

                print("percentage", percentage)
                main_list.append(
                    [
                        website,
                        sm,
                        product,
                        country,
                        quality,
                        provider,
                        quantity,
                        str(our_price),
                        f"{cost:.5f}",
                        percentage,
                    ]
                )

            except Exception as e:
                print(e)

        for row_number, row_data in enumerate(main_list):
            self.tablePrice.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tablePrice.setItem(
                    row_number, column_number, QTableWidgetItem(str(data))
                )


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
