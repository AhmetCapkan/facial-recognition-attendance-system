import sys
import os
import shutil
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from kayit_formu import Ui_MainWindow  # Güncellenmiş arayüz dosyası

class KayıtArayüz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.photo_path = None

        self.ui.btnLoadPhoto.clicked.connect(self.fotograf_yukle)
        self.ui.btn.clicked.connect(self.kayit_ekle)

    def fotograf_yukle(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "Image Files (*.jpg *.png *.jpeg *.bmp)")
        if file_path:
            self.photo_path = file_path
            pixmap = QPixmap(file_path)
            self.ui.label_5.setPixmap(pixmap.scaled(self.ui.label_5.size()))

    def kayit_ekle(self):
        adsoyad = self.ui.lineAdSoyad.text().strip()
        numara = self.ui.lineNumara.text().strip()
        bolum = self.ui.lineBolum.text().strip()

        if not adsoyad or not numara or not bolum or not self.photo_path:
            QMessageBox.warning(self, "Eksik Bilgi", "Lütfen tüm alanları doldurun ve fotoğraf yükleyin.")
            return

        try:
            os.makedirs("Photos", exist_ok=True)
            yeni_foto_yolu = os.path.join("Photos", f"{numara}.jpg").replace("\\","/")
            shutil.copy(self.photo_path, yeni_foto_yolu)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Fotoğraf kaydedilirken hata oluştu:\n{e}")
            return

        try:
            conn = pyodbc.connect("Driver={SQL Server};Server=CAPKAN\SQLEXPRESS;Database=StudentsFace;Trusted_Connection=yes;")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Students (StudentID, Name, Major, PhotoPath)
                VALUES (?, ?, ?, ?)
            """, numara, adsoyad, bolum, yeni_foto_yolu)

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Kayıt başarıyla eklendi.")
            self.temizle()

        except Exception as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Kayıt eklenirken hata oluştu:\n{e}")

    def temizle(self):
        self.ui.lineAdSoyad.clear()
        self.ui.lineNumara.clear()
        self.ui.lineBolum.clear()
        self.ui.label_5.clear()
        self.photo_path = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = KayıtArayüz()
    pencere.show()
    sys.exit(app.exec_())
