# -*- coding: utf-8 -*-
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import webbrowser
import math
import os
import screen_brightness_control as sbc

# Yapılandırma
KENAR_BOSLUK = 10
YAZI_BOYUTU = 1
YAZI_KALINLIGI = 1
EL_YON_RENGI = (88, 205, 54)
MODEL_YOLU = 'hand_landmarker.task'

def koordinat_getir(noktalar, indeks, yukseklik, genislik):
    """Normalleştirilmiş nokta koordinatlarını piksel koordinatlarına dönüştür."""
    nokta = noktalar[indeks]
    return int(nokta.x * genislik), int(nokta.y * yukseklik)

def mesafe_hesapla(nokta1, nokta2):
    """İki nokta (x, y) arasındaki Öklid mesafesini hesapla."""
    return math.sqrt((nokta2[0] - nokta1[0])**2 + (nokta2[1] - nokta1[1])**2)

def el_noktalarini_ciz(goruntu_rgb, algilama_sonucu):
    """El noktalarını işle, parmakları say, parlaklığı kontrol et ve görüntüyü işaretle."""
    el_noktalar_listesi = algilama_sonucu.hand_landmarks
    el_yon_listesi = algilama_sonucu.handedness
    isaretli_goruntu = np.copy(goruntu_rgb)
    yukseklik, genislik, _ = isaretli_goruntu.shape

    # Google hareketi için statik değişken başlat
    if not hasattr(el_noktalarini_ciz, "google_acildi"):
        el_noktalarini_ciz.google_acildi = False

    for idx in range(len(el_noktalar_listesi)):
        el_noktalar = el_noktalar_listesi[idx]
        el_yonu = el_yon_listesi[idx][0].category_name
        parmaklar = []

        # Avuç yönü kontrolü (avuç yukarı mı, elin arkası mı)
        y_merkez = koordinat_getir(el_noktalar, 0, yukseklik, genislik)[1]
        y_orta = koordinat_getir(el_noktalar, 12, yukseklik, genislik)[1]
        avuc_yukari = y_orta < y_merkez  # True: avuç yukarı, False: elin arkası

        # Parmak algılama (işaret, orta, yüzük, serçe)
        kontrol_noktalar = [(8, 6), (12, 10), (16, 14), (20, 18)]
        for ucu, eklem in kontrol_noktalar:
            y_ucu = koordinat_getir(el_noktalar, ucu, yukseklik, genislik)[1]
            y_eklem = koordinat_getir(el_noktalar, eklem, yukseklik, genislik)[1]
            if avuc_yukari:
                parmaklar.append(1 if y_ucu < y_eklem else 0)  # Avuç yukarı: uç eklemden yüksekse kaldırılmış
            else:
                parmaklar.append(1 if y_ucu > y_eklem else 0)  # Elin arkası: uç eklemden düşükse kaldırılmış

        # Başparmak algılama
        x_basparmak, y_basparmak = koordinat_getir(el_noktalar, 4, yukseklik, genislik)
        x_eklem, y_eklem = koordinat_getir(el_noktalar, 2, yukseklik, genislik)
        if avuc_yukari:
            if el_yonu == "Right":
                parmaklar.append(1 if x_basparmak > x_eklem else 0)
            else:
                parmaklar.append(1 if x_basparmak < x_eklem else 0)
        else:
            if el_yonu == "Right":
                parmaklar.append(1 if x_basparmak < x_eklem else 0)
            else:
                parmaklar.append(1 if x_basparmak > x_eklem else 0)

        # Parmak sayımı
        if not avuc_yukari:
            toplam = 5 - sum(parmaklar)  # Elin arkası: 5’ten başla, katlanmış parmaklar için azalt
        else:
            toplam = sum(parmaklar)  # Avuç yukarı: 0’dan başla, kaldırılmış parmaklar için artır

        # Google hareketi
        if toplam == 3 and not el_noktalarini_ciz.google_acildi:
            webbrowser.open("https://www.google.com")
            el_noktalarini_ciz.google_acildi = True
        elif toplam != 3:
            el_noktalarini_ciz.google_acildi = False

        # Parlaklık kontrolü (çakışmayı önlemek için sadece ilk el)
        if idx == 0:
            basparmak_konum = koordinat_getir(el_noktalar, 4, yukseklik, genislik)
            isaret_konum = koordinat_getir(el_noktalar, 8, yukseklik, genislik)
            mesafe = mesafe_hesapla(basparmak_konum, isaret_konum)
            
            # Mesafeyi normalleştir (50-300 piksel, 0-100 parlaklık aralığına eşle)
            min_mesafe = 50
            max_mesafe = 300
            normal_mesafe = max(0, min(1, (mesafe - min_mesafe) / (max_mesafe - min_mesafe)))
            parlaklik = int(normal_mesafe * 100)
            
            # Parlaklığı ayarla
            try:
                sbc.set_brightness(parlaklik)
                print(f"Parlaklık {parlaklik}% olarak ayarlandı.")
            except Exception as e:
                print(f"Parlaklık kontrol hatası: {e}. Platform uyumluluğunu veya izinleri kontrol edin.")

            # Parlaklık seviyesini göster
            parlaklik_metni = f"Parlaklık: {parlaklik}%"
            print(f"Ekrana yazdırılan metin: {parlaklik_metni}")  # Hata ayıklamak için
            cv2.putText(isaretli_goruntu, parlaklik_metni, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Parmak sayısını çiz
        x1, y1 = koordinat_getir(el_noktalar, 8, yukseklik, genislik)
        isaretli_goruntu = cv2.putText(isaretli_goruntu, str(toplam), (x1, y1),
                                      cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 4)
        isaretli_goruntu = cv2.circle(isaretli_goruntu, (x1, y1), 9, (255, 255, 0), 5)

        # El noktalarını çiz
        el_noktalar_proto = landmark_pb2.NormalizedLandmarkList()
        el_noktalar_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=nokta.x, y=nokta.y, z=nokta.z)
            for nokta in el_noktalar
        ])

        mp.solutions.drawing_utils.draw_landmarks(
            isaretli_goruntu,
            el_noktalar_proto,
            mp.solutions.hands.HAND_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            mp.solutions.drawing_styles.get_default_hand_connections_style())

        # El yönünü yaz
        x_koordinatlar = [nokta.x for nokta in el_noktalar]
        y_koordinatlar = [nokta.y for nokta in el_noktalar]
        yazi_x = int(min(x_koordinatlar) * genislik)
        yazi_y = max(KENAR_BOSLUK, int(min(y_koordinatlar) * yukseklik) - KENAR_BOSLUK)
        cv2.putText(isaretli_goruntu, f"{el_yonu}", (yazi_x, yazi_y),
                    cv2.FONT_HERSHEY_DUPLEX, YAZI_BOYUTU, EL_YON_RENGI,
                    YAZI_KALINLIGI, cv2.LINE_AA)

    return isaretli_goruntu

def ana_fonksiyon():
    """El takibi ve hareket kontrolünü çalıştıran ana fonksiyon."""
    # Model dosyasını doğrula
    if not os.path.exists(MODEL_YOLU):
        print(f"Hata: Model dosyası {MODEL_YOLU} bulunamadı. MediaPipe web sitesinden indirin.")
        return

    # Dedektörü başlat
    try:
        temel_secenekler = python.BaseOptions(model_asset_path=MODEL_YOLU)
        secenekler = vision.HandLandmarkerOptions(base_options=temel_secenekler, num_hands=2)
        dedektor = vision.HandLandmarker.create_from_options(secenekler)
    except Exception as e:
        print(f"ElDedektörü başlatma hatası: {e}")
        return

    # Kamerayı başlat
    kamera = cv2.VideoCapture(0)
    if not kamera.isOpened():
        print("Hata: Kamera açılamadı. Kameranın bağlı olduğunu ve izinlerin verildiğini kontrol edin.")
        return

    print("El takibi başlatılıyor. Çıkmak için 'q' veya 'Q' tuşuna basın.")
    while kamera.isOpened():
        basari, kare = kamera.read()
        if not basari:
            print("Uyarı: Kameradan kare okunamadı.")
            continue

        kare_rgb = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
        mp_goruntu = mp.Image(image_format=mp.ImageFormat.SRGB, data=kare_rgb)
        try:
            algilama_sonucu = dedektor.detect(mp_goruntu)
        except Exception as e:
            print(f"Algılama sırasında hata: {e}")
            continue

        isaretli_goruntu = el_noktalarini_ciz(mp_goruntu.numpy_view(), algilama_sonucu)
        cv2.imshow("El Takibi", cv2.cvtColor(isaretli_goruntu, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(1) & 0xFF in [ord('q'), ord('Q')]:
            print("Programdan çıkılıyor.")
            break

    kamera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ana_fonksiyon()