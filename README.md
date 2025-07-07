# facial-recognition-attendance-system
Yüz tanımalı yoklama sistemi kullanıcının eklediği yüzleri ekleyerek yoklama alacaktır . Daha sonra ilk tanındığı kısımı giriş saati ikinci tanınan kısmı ise çıkış saati olarak excel dosyasına kaydedecektir. 

1. Ms SQL'de yeni bir database oluşturun (benimkinin adı StudentsFace karışıklık olmaması için bunu kullanabilirsiniz)

2. EncodeGenerator.py'de 11. Satırdaki, main.py'de 14. satırdaki Server ismini bilgisayarınızın adıyla değiştirin

3. StudentsFace database'i içerisine new query açıp 

CREATE TABLE Students (
    StudentID BIGINT PRIMARY KEY,  -- Use BIGINT instead of INT
    Name NVARCHAR(100),
    Major NVARCHAR(100),
    PhotoPath NVARCHAR(255)
); 

yazıp çalıştırın

4. Öğrenci isimlerini girmek için query açıp en alta eklediğim listeyi yazın. Arayüzdende ekleyebilirsini<

5. Öncelikle EncodeGenerator.py'yi çalıştırın, encoding bittikten sonra main.py'yi çalıştırın

Herkesin olduğu SQL kodu:
Arayüzden Ekleme silme güncelleme işlemlerini yapabilirsiniz.
INSERT INTO Students (StudentID, Name, Major, PhotoPath)
VALUES
('Numara', 'İsim', 'Bölüm', 'Fotoğraf Yolu'),

Bu kısımları ekleme güncelleme silme işlemlerini arayüz kısmından yapabilirsiniz. 

6. Projeyi çalıştırdıktan sonra sağ tarafta isim soyisim bölüm ve numara çıkacaktır tanınan kişinin ve Hoş geldin 'İsmi' şeklinde seslenip giriş saati kaydedilecektir.


7. Daha sonra projede tanınan kişi birdaha tanınınca Güle Güle 'isim' şeklinde çıkış saati kaydedilecektir.


8. Ve Yoklama işlemleri bitince 'q' tuşuna basarak yoklamayı bitirip hazır excel dosyasını proje klasöründen alabilirsiniz

