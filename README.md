# 📶 Wi-Fi Signal Heatmap Generator

> Ev veya ofis ortamındaki Wi-Fi sinyal kalitesini analiz ederek, bağlantı sorunlarını (ölü bölgeleri) tespit eden ve görselleştiren bir Python aracı.

## 🎯 Projenin Amacı
İnternet bağlantı sorunlarını "tahmin etmek" yerine, **veri mühendisliği** yöntemleriyle analiz etmek. Bu araç, donanımdan (NIC) alınan **RSSI (Received Signal Strength Indicator)** verilerini işleyerek mekanın sinyal haritasını çıkarır.

## 🚀 Özellikler
* **Gerçek Zamanlı Veri:** Windows `netsh` komutlarıyla donanımdan anlık sinyal gücü çekimi.
* **Veri Toplama:** Kullanıcının kroki üzerinde tıkladığı noktalardan veri toplama.
* **Matematiksel Modelleme:** Toplanan veriler arasındaki boşlukları **Linear Interpolation** yöntemiyle doldurma.
* **Görselleştirme:** Matplotlib ve Seaborn benzeri renkli **Isı Haritası (Heatmap)** çıktısı.

## 🛠️ Kullanılan Teknolojiler
* **Python 3.x**
* **Pandas & NumPy:** Veri manipülasyonu için.
* **Matplotlib:** Görselleştirme ve arayüz için.
* **SciPy:** İnterpolasyon (GridData) algoritmaları için.
* **Subprocess:** İşletim sistemi komutlarını yönetmek için.

## 💻 Nasıl Çalıştırılır?

1. Projeyi indirin:
```bash
git clone [https://github.com/mehmet3mn/wifi-signal-heatmap](https://github.com/mehmet3mn/wifi-signal-heatmap)

2. Gerekli kütüphaneleri kurun:
pip install -r requirements.txt

3. Kendi evinizin krokisini kroki.png adıyla klasöre atın.

4. Uygulamayı başlatın:
python wifi_map.py