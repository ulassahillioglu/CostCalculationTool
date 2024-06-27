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
from conv import currency_converter, currency_converter_to_real

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons(self)
        self.exchange_rate = currency_converter()
        self.exchange_rate_real = currency_converter_to_real()
        self.tr_scraper = 10.0
        self.en_scraper = 0.50
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
        
        header = self.tablePrice.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #3f57cc; }")
        
    def Handel_Buttons(self, parent):
        self.btnCalculate.clicked.connect(self.calculate)
        self.btnAutoCalc.clicked.connect(self.calculate_auto)
        self.btnClear.clicked.connect(self.clear)

    def clear(self):
        website = self.boxWebsite.currentText()
        product = self.boxProduct.currentText()
        
        if product.lower() == "comments":
            quantities_comments = ["10", "20", "30", "40", "50", "100"]
            for index in range(len(quantities_comments)):
                line_edit = self.findChild(QLineEdit, f"comment{index+1}")
                if line_edit:
                    line_edit.clear()
        else:
            quantities = [
                "10", "25", "50", "100", "250", "500", "1000", 
                "2500", "5000", "10000", "25000", "50000", 
                "100000", "250000", "500000"
            ]
            for index in range(len(quantities)):
                line_edit = self.findChild(QLineEdit, f"lineEdit{index+1}")
                if line_edit:
                    line_edit.clear()


    def calculate_auto(self):
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
        quantities_comments = ["10", "20", "30", "40", "50", "100"]

        main_list = []
        website = self.boxWebsite.currentText()
        sm = self.boxSM.currentText()
        product = self.boxProduct.currentText()
        quality = self.boxQuality.currentText()
        country = self.boxCountry.currentText()
        provider = self.lineProvider.text()

        if self.radioBtnUsd.isChecked():
            chosen_currency = "USD"
        elif self.radioBtnTry.isChecked():
            chosen_currency = "TRY"

        if product.lower() == "comments":
            quantities = quantities_comments

        self.tablePrice.setRowCount(0)
        self.tablePrice.setColumnCount(9)
        headers = ["Website", "Oto Fiyat", "Oto Fiyat (Scraper)", "Provider", "Miktar", "Fiyat", "Oto Maliyet", "Oto Yüzde", "Oto Yüzde (Scraper)"]
        self.tablePrice.setHorizontalHeaderLabels(headers)

        for index, quantity in enumerate(quantities):
            try:
                line_edit_name = f"comment{index+1}" if product.lower() == "comments" else f"lineEdit{index+1}"
                line_edit = self.findChild(QLineEdit, line_edit_name)
                our_price = float(line_edit.text())

                if website.lower() == "instatakipci":
                    auto_price = our_price * 4
                    auto_price_with_scraper = auto_price + self.tr_scraper
                else:
                    auto_price = round(our_price * 2.25, 3)
                    auto_price_with_scraper = auto_price + self.en_scraper

                if website.lower() == "instatakipci" and chosen_currency == "USD":
                    srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate
                else:
                    srv_price = float(self.lineSrvPrice.text())

                cost = round((int(quantity) * srv_price / 1000), 5)
                percentage = format((cost * 100) / auto_price, ".3f")
                percentage_with_scraper = format((cost * 100 / auto_price_with_scraper) * 5, ".3f")

                main_list.append(
                    [
                        website,
                        auto_price,
                        auto_price_with_scraper,
                        provider,
                        quantity,
                        str(our_price),
                        f"{cost:.5f}",
                        percentage,
                        percentage_with_scraper,
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
        quantities_comments = ["10","20","30","40","50","100"]

        main_list = []
        website = self.boxWebsite.currentText()
        sm = self.boxSM.currentText()
        product = self.boxProduct.currentText()
        quality = self.boxQuality.currentText()
        country = self.boxCountry.currentText()
        provider = self.lineProvider.text()

        if self.radioBtnUsd.isChecked():
            chosen_currency = "USD"
        elif self.radioBtnTry.isChecked():
            chosen_currency = "TRY"
        
        if product.lower() == "comments":
            quantities = quantities_comments

        self.tablePrice.setRowCount(0)
        self.tablePrice.setColumnCount(10)  # Set to the number of columns in your data

        for index, quantity in enumerate(quantities):
            if len(quantities)<=6:
                try:
                    line_edit = self.findChild(QLineEdit, f"comment{index+1}")
                    if website.lower() == "popularos":
                        our_price = round(float(line_edit.text())*self.exchange_rate_real,2)
                        srv_price = float(self.lineSrvPrice.text())*self.exchange_rate_real

                    elif website.lower()=='instatakipci' and chosen_currency == "USD":
                        our_price = round(float(line_edit.text()),2)
                        srv_price = float(self.lineSrvPrice.text())*self.exchange_rate

                    elif website.lower()=="instafollowers" and chosen_currency == "TRY":
                        our_price = round(float(line_edit.text()),2)
                        srv_price = float(self.lineSrvPrice.text())/self.exchange_rate
                    else:
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
            else:
                try:
                    line_edit = self.findChild(QLineEdit, f"lineEdit{index+1}")
                    if website.lower() == "popularos":
                        our_price = round(float(line_edit.text())*self.exchange_rate_real,2)
                        srv_price = float(self.lineSrvPrice.text())*self.exchange_rate_real

                    elif website.lower()=='instatakipci' and chosen_currency == "USD":
                        our_price = round(float(line_edit.text()),2)
                        srv_price = float(self.lineSrvPrice.text())*self.exchange_rate
                    
                    elif website.lower()=="instafollowers" and chosen_currency == "TRY":
                        our_price = round(float(line_edit.text()),2)
                        srv_price = float(self.lineSrvPrice.text())/self.exchange_rate

                    else:
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
