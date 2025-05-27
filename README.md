# IoT Tabanlı Sensör Verisi Toplama ve AWS MQTT ile Buluta Aktarma

Bu proje, Raspberry Pi üzerinde çalışan bir Python uygulaması ile çevresel (DHT11) ve elektriksel (PZEM-004T) sensörlerden veri toplamayı, bu verileri yerel InfluxDB'ye kaydetmeyi, Grafana ile görselleştirmeyi ve aynı zamanda AWS IoT Core üzerinden MQTT protokolü ile buluta aktarmayı amaçlamaktadır.

## Kullanılan Teknolojiler

- **Raspberry Pi** (Veri işleme ve yönlendirme)
- **DHT11** (Sıcaklık ve nem sensörü)
- **PZEM-004T** (Gerilim, akım, enerji, güç faktörü vs.)
- **Python** (Veri okuma ve gönderme)
- **InfluxDB** (Zaman serisi veri tabanı)
- **Grafana** (Veri görselleştirme)
- **MQTT (Paho + Mosquitto)** (Yerel mesajlaşma)
- **AWS IoT Core** (Bulut tabanlı veri gönderimi)
- **Graphviz / Sistem Şeması** (Proje görselleştirme)

## Sistem Mimarisi

Aşağıdaki şema, veri kaynaklarından başlayıp AWS bulutuna kadar olan tüm süreci görsel olarak açıklamaktadır:

![Sistem Mimarisi](bulutbilişim-proje.jpeg)

##  Dosya Açıklamaları

| Dosya Adı          | Açıklama |
|--------------------|----------|
| `example2.py`      | DHT11 sensöründen sıcaklık ve nem ölçümü alır ve InfluxDB + AWS MQTT'ye gönderir. |
| `okuyucu.py`       | PZEM-004T modülü üzerinden enerji verilerini okur ve benzer şekilde gönderir. |
| `requirements.txt` | Projeyi çalıştırmak için gerekli Python kütüphaneleri. |
| `bulutbilişim-proje.jpeg` | Proje sistem mimarisi. |

##  Kurulum

1. Gerekli Python kütüphanelerini yükleyin:
```bash
pip install -r requirements.txt
```

2. Sensörleri bağlayın ve uygun portları kontrol edin.

3. AWS sertifikalarınızı `/home/raspberry/certs/` klasörüne yerleştirin.

4. Uygulamayı çalıştırın:
```bash
python3 example2.py     # DHT11 için
python3 okuyucu.py      # PZEM-004T için
```

##  Örnek Veri Akışı

- Sensörlerden alınan veri, InfluxDB’ye yazılır.
- Grafana panelinden bu veriler izlenebilir.
- AWS IoT Core üzerinden MQTT ile bulut entegrasyonu sağlanır.
- Uyarı sistemi için eşik değer kontrolü yapılabilir.

## Güvenlik Notu

AWS IoT sertifikalarınızı `.gitignore` ile gizlediğinizden emin olun. Örnek:
```bash
/certs/
*.pem
*.key
```

##  Lisans

MIT Lisansı. Detaylar için `LICENSE` dosyasını inceleyin.
