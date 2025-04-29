OĞULCAN ESENDİR
2023688031

El Hareketi ile Parlaklık Kontrolü ve Google Açma
Bu proje, MediaPipe kullanarak el hareketlerini algılar, parmak sayısını hesaplar, ekran parlaklığını kontrol eder ve belirli bir hareketle Google’ı açar. Görüntü işleme teknikleriyle el takibi yaparak kullanıcı dostu bir arayüz sunar.
Özellikler

Parmak Sayımı:
Avuç yukarı: Kaldırılan parmak sayısını 0’dan başlayarak sayar.


Parlaklık Kontrolü: Başparmak ve işaret parmağı arasındaki mesafeye göre ekran parlaklığını ayarlar (0-100%).
Google Hareketi: Üç parmak gösterildiğinde Google ana sayfasını tarayıcıda açar.
Görsel Geri Bildirim: Ekranda parmak sayısı, el yönü (sağ/sol) ve parlaklık yüzdesi gösterilir.

Gereksinimler

Python 3.6+
Kütüphaneler:
mediapipe
opencv-python
screen-brightness-control
numpy


Model Dosyası: MediaPipe Hand Landmarker modeli (hand_landmarker.task)
Webcam: El takibi için bir kamera

Kurulum

Python’u Yükleyin:

Python 3.6 veya üstü bir sürümün yüklü olduğundan emin olun:python --version




Gerekli Kütüphaneleri Yükleyin:

Terminalde aşağıdaki komutu çalıştırın:pip install mediapipe opencv-python screen-brightness-control numpy




Model Dosyasını İndirin:

MediaPipe’in Hand Landmarker modelini indirin (hand_landmarker.task).
Dosyayı proje dizinine (kod dosyasının yanına) yerleştirin.


Kod Dosyasını Hazırlayın:

ogulcan_esendir_goruntuisleme_vize.py dosyasını bir metin editöründe (ör. VS Code) açın.
Dosyanın UTF-8 kodlamasıyla kaydedildiğinden emin olun (Türkçe karakterler için).



Kullanım

Kodu Çalıştırın:

Terminalde veya VS Code’da aşağıdaki komutu çalıştırın:python ogulcan_esendir_goruntuisleme_vize.py


Program, kamerayı açar ve el takibine başlar.


Hareketleri Kullanın:

Parmak Sayımı:
Avucunuzu kameraya gösterin: Kaldırdığınız parmaklar sayılır (0-5).
Elinizin arkasını gösterin: Katlanmayan parmaklar 5’ten başlayarak sayılır.


Parlaklık Kontrolü:
Başparmak ve işaret parmağınızı yaklaştırıp uzaklaştırarak ekran parlaklığını ayarlayın.
Parlaklık yüzdesi ekranın sol üst köşesinde gösterilir (Parlaklık: X%).


Google Açma:
Üç parmak gösterin; Google ana sayfası varsayılan tarayıcıda açılır.




Çıkış:

Programdan çıkmak için q veya Q tuşuna basın.



Notlar

Platform Uyumluluğu:
Windows/macOS: Parlaklık kontrolü genellikle sorunsuz çalışır.
Linux: xrandr veya brightnessctl gibi araçlar gerekebilir:sudo apt-get install x11-xserver-utils brightnessctl


Parlaklık kontrolü için kullanıcıyı video grubuna ekleyin:sudo usermod -aG video $USER

Çıkış yapıp tekrar giriş yapın.




Hata Ayıklama:
Kamera açılmazsa, bağlı olduğundan ve izinlerin verildiğinden emin olun.
Model dosyası eksikse, hata mesajı görüntülenir; dosyayı doğru konuma yerleştirin.
Parlaklık kontrolü başarısız olursa, terminaldeki hata mesajını kontrol edin.


Türkçe Karakterler:
Kod, UTF-8 kodlamasıyla çalışır. VS Code’da dosyanın UTF-8 ile kaydedildiğinden emin olun.
Ekran metni (Parlaklık: X%) doğru Türkçe karakterlerle görüntülenir.



Lisans
Bu proje, eğitim amaçlı geliştirilmiştir ve kişisel kullanım için ücretsizdir. Ticari kullanım veya dağıtım için izin gerekmez.
