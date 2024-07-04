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
from conv import currency_converter, currency_converter_to_real,currency_converter_to_real_from_try

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    DEFAULT_HEADERS = ["Site", "Sosyal Medya", "Ürün", "Ülke", "Kalite", "Tedarikçi", "Adet", "Fiyat", "Maliyet", "Maliyet Oranı"]
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons(self)
        self.exchange_rate = currency_converter()
        self.exchange_rate_real = currency_converter_to_real()
        self.exchange_rate_real_from_try = currency_converter_to_real_from_try()
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
        
        self.headers_modified = False
        header = self.tablePrice.horizontalHeader()
        header.setStyleSheet("QHeaderView::section { background-color: #3f57cc; }")
        
    def Handel_Buttons(self, parent):
        self.btnCalculate.clicked.connect(self.calculate)
        self.btnAutoCalc.clicked.connect(self.calculate_auto)
        self.btnMontlyCalc.clicked.connect(self.calculate_monthly_price)
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
        quantities_comments = ["10", "20", "30", "40", "50", "100","250","500"]

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
        self.headers_modified = True

        for index, quantity in enumerate(quantities):
            try:
                line_edit_name = f"comment{index+1}" if product.lower() == "comments" else f"lineEdit{index+1}"
                line_edit = self.findChild(QLineEdit, line_edit_name)
                our_price = float(line_edit.text())

                if website.lower() == "it":
                    auto_price = our_price * 4
                    auto_price_with_scraper = auto_price + self.tr_scraper
                else:
                    auto_price = round(our_price * 2.25, 3)
                    auto_price_with_scraper = auto_price + self.en_scraper

                if website.lower() == "pop":
                    if chosen_currency == "USD":
                        our_price = round(float(line_edit.text()) * self.exchange_rate_real, 2)
                        srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real

                    else:
                        our_price = round(float(line_edit.text()) * self.exchange_rate_real_from_try, 2)
                        srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real_from_try

                elif website.lower() == "it" and chosen_currency == "USD":
                    srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate
                    
                elif website.lower() == "if" and chosen_currency == "TRY":
                    srv_price = float(self.lineSrvPrice.text()) / self.exchange_rate
                else:
                    srv_price = float(self.lineSrvPrice.text())

                cost = round((int(quantity) * srv_price / 1000), 5)
                percentage = format(((cost * 100) / auto_price) * 5, ".3f")
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
        if self.headers_modified:
            self.tablePrice.setColumnCount(len(self.DEFAULT_HEADERS))  # Ensure the column count matches the headers
            self.tablePrice.setHorizontalHeaderLabels(self.DEFAULT_HEADERS)
            self.headers_modified = False  # Reset the flag

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
        quantities_comments = ["10", "20", "30", "40", "50", "100", "250", "500"]

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
        # self.tablePrice.setColumnCount(10)  # Set to the number of columns in your data

        for index, quantity in enumerate(quantities):
            if len(quantities) <= 8:
                try:
                    line_edit = self.findChild(QLineEdit, f"comment{index+1}")
                    if website.lower() == "pop":
                        if chosen_currency == "USD":
                            our_price = round(float(line_edit.text()) * self.exchange_rate_real, 2)
                            srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real
                        else:
                            our_price = round(float(line_edit.text()) * self.exchange_rate_real_from_try, 2)
                            srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real_from_try
                        
                    elif website.lower() == 'it' and chosen_currency == "USD":
                        our_price = round(float(line_edit.text()), 2)
                        srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate

                    elif website.lower() == "if" and chosen_currency == "TRY":
                        our_price = round(float(line_edit.text()), 2)
                        srv_price = float(self.lineSrvPrice.text()) / self.exchange_rate
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
                    if website.lower() == "pop":
                        if chosen_currency == "USD":
                            our_price = round(float(line_edit.text()) * self.exchange_rate_real, 2)
                            srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real
                        else:
                            our_price = round(float(line_edit.text()) * self.exchange_rate_real_from_try, 2)
                            srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real_from_try

                    elif website.lower() == 'it' and chosen_currency == "USD":
                        our_price = round(float(line_edit.text()), 2)
                        srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate

                    elif website.lower() == "if" and chosen_currency == "TRY":
                        our_price = round(float(line_edit.text()), 2)
                        srv_price = float(self.lineSrvPrice.text()) / self.exchange_rate

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

    def calculate_monthly_price(self):
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
        quantities_comments = ["10", "20", "30", "40", "50", "100","250","500"]

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

        headers = ["Website", "Aylık Fiyat", "Provider", "Miktar", "Fiyat", "Aylık Maliyet", "Aylık Yüzde Maliyet"]
        self.tablePrice.setRowCount(0)
        self.tablePrice.setColumnCount(len(headers))
        self.tablePrice.setHorizontalHeaderLabels(headers)
        self.headers_modified = True

        for index, quantity in enumerate(quantities):
            try:
                line_edit_name = f"comment{index+1}" if product.lower() == "comments" else f"lineEdit{index+1}"
                line_edit = self.findChild(QLineEdit, line_edit_name)
                our_price = float(line_edit.text())

                
                monthly_price = round(our_price * 30,3)
                
                if website.lower() == "pop":
                    if chosen_currency == "USD":
                        our_price = round(float(line_edit.text()) * self.exchange_rate_real, 2)
                        srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real
                        monthly_price = round(our_price * 30,3)

                    else:
                        our_price = round(float(line_edit.text()) * self.exchange_rate_real_from_try, 2)
                        srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate_real_from_try
                        monthly_price = round(our_price * 30,3)

                elif website.lower() == "it" and chosen_currency == "USD":
                    srv_price = float(self.lineSrvPrice.text()) * self.exchange_rate
                    
                elif website.lower() == "if" and chosen_currency == "TRY":
                    srv_price = float(self.lineSrvPrice.text()) / self.exchange_rate
                else:
                    srv_price = float(self.lineSrvPrice.text())

                cost = round((int(quantity) * srv_price / 1000), 5)
                percentage = format((cost / monthly_price)*100*30, ".3f")
                

                main_list.append(
                    [
                        website,
                        monthly_price,
                        provider,
                        quantity,
                        str(our_price),
                        f"{cost:.5f}",
                        '% ' + percentage,
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

