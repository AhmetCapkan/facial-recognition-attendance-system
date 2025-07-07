import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from delete_update import Ui_MainWindow  # Qt Designer'dan pyuic5 ile çevrilmiş arayüz

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Veritabanı bağlantısı
        self.conn = pyodbc.connect(
            'Driver={SQL Server};Server=CAPKAN\SQLEXPRESS;Database=StudentsFace;Trusted_Connection=yes;'
        )
        self.cursor = self.conn.cursor()

        # Signal-slot bağlantıları
    #    self.ui.btnKaydet.clicked.connect(self.kaydet)
        self.ui.btnGuncelle.clicked.connect(self.guncelle)
        self.ui.btnSil.clicked.connect(self.sil)
        self.ui.tableWidget.cellClicked.connect(self.kayit_secildi)

        # İlk veri yüklemesi
        self.load_data()

    def load_data(self):
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Numara", "Ad Soyad", "Bölüm"])
        self.ui.tableWidget.setRowCount(0)  # Tabloyu temizle
        self.cursor.execute("SELECT StudentID, Name, Major FROM Students")
        for row_data in self.cursor.fetchall():
            row = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row)
            for col, data in enumerate(row_data):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(data)))

    def kaydet(self):
        ad = self.ui.lineAdSoyad.text()
        numara = self.ui.lineNumara.text()
        bolum = self.ui.lineBolum.text()

        if not (ad and numara and bolum):
            print("Tüm alanları doldurun!")
            return

        try:
            self.cursor.execute(
                "INSERT INTO Students (AdSoyad, Numara, Bolum) VALUES (?, ?, ?)",
                (ad, numara, bolum)
            )
            self.conn.commit()
            self.load_data()
            print("Kayıt eklendi.")
        except Exception as e:
            print("Hata:", e)

    def kayit_secildi(self, row, column):
        self.ui.lineAdSoyad.setText(self.ui.tableWidget.item(row, 1).text())
        self.ui.lineNumara.setText(self.ui.tableWidget.item(row, 0).text())
        self.ui.lineBolum.setText(self.ui.tableWidget.item(row, 2).text())
        self.seciliSatir = row
        self.seciliNumara = self.ui.tableWidget.item(row, 0).text()  # Numara ile güncelleme/silme yapılacak

    def guncelle(self):
        if not hasattr(self, 'seciliSatir'):
            QMessageBox.warning(self,"Uyarı","Lütfen güncellenecek kaydı seçiniz.")
            return

        ad = self.ui.lineAdSoyad.text()
        numara = self.ui.lineNumara.text()
        bolum = self.ui.lineBolum.text()

        eski_numara = self.seciliNumara

        try:
            self.cursor.execute(
                "UPDATE Students SET Name=?, Major=? WHERE StudentID=?",
                (ad,  bolum, numara)
            )
            self.conn.commit()
            self.load_data()
            QMessageBox.information(self,"Başarılı","Kayıt başarı ile güncellendi.")
        except Exception as e:
            print("Hata:", e)

    def sil(self):
        if not hasattr(self, 'seciliSatir'):
            QMessageBox.warning(self,"Uyarı","Lütfen silinecek kaydı seçiniz.")
            return

        try:
            self.cursor.execute(
                "DELETE FROM Students WHERE StudentID=?",
                (self.seciliNumara,)
            )
            self.conn.commit()
            self.load_data()
            QMessageBox.information(self,"Başarılı","Kayıt başarı ile silindi.")
            # LineEdit temizle
            self.ui.lineAdSoyad.clear()
            self.ui.lineNumara.clear()
            self.ui.lineBolum.clear()
            self.seciliSatir = None
        except Exception as e:
            print("Hata:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
