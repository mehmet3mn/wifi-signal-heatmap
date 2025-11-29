import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import subprocess
import re
import pandas as pd
import numpy as np
from scipy.interpolate import griddata

# --- 1. FONKSİYON: Wi-Fi Sinyal Gücünü Çek ---
def get_wifi_signal():
    try:
        # Windows terminaline 'netsh wlan show interfaces' komutunu gönderiyoruz
        output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('utf-8', errors='ignore')
        
        # Çıktının içinden "Signal" yazan satırı Regex ile buluyoruz
        match = re.search(r"Signal\s*:\s*(\d+)%", output)
        if match:
            return int(match.group(1)) # Örn: 85 döner
        else:
            return 0
    except:
        return 0

# --- 2. AYARLAR ---
image_path = 'kroki.png' # Buraya kendi kroki resminin adını yaz
data = [] # Verileri burada tutacağız: [x, y, signal]

# --- 3. İNTERAKTİF HARİTA ---
fig, ax = plt.subplots(figsize=(10, 6))
img = mpimg.imread(image_path)
ax.imshow(img)
plt.title("Haritada bulunduğunuz yere TIKLAYIN (Çıkmak için 'q' basın)")

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        # 1. Tıklanan koordinatı al
        x, y = event.xdata, event.ydata
        
        # 2. O anki Wi-Fi sinyalini ölç
        signal = get_wifi_signal()
        print(f"Konum: ({int(x)}, {int(y)}) -> Sinyal: %{signal}")
        
        # 3. Listeye ekle ve ekrana nokta koy
        data.append([x, y, signal])
        
        # Renk skalası: Kötü (Kırmızı) -> İyi (Yeşil)
        color = 'red' if signal < 50 else 'yellow' if signal < 75 else 'green'
        ax.plot(x, y, 'o', color=color, markersize=10, markeredgecolor='black')
        plt.draw()

# Tıklama olayını bağla
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

# --- 4. VERİYİ KAYDET VE GÖRSELLEŞTİR (HEATMAP) ---
if len(data) > 3: # En az 3 nokta lazım
    df = pd.DataFrame(data, columns=['x', 'y', 'signal'])
    
    # Grid oluştur (Matematiksel Doldurma)
    x = df['x']
    y = df['y']
    z = df['signal']
    
    # Harita boyutlarına göre ızgara yarat
    xi = np.linspace(x.min(), x.max(), 100)
    yi = np.linspace(y.min(), y.max(), 100)
    xi, yi = np.meshgrid(xi, yi)
    
    # Boşlukları doldur (Linear Interpolation)
    zi = griddata((x, y), z, (xi, yi), method='linear')
    
    # Sonucu çiz
    plt.figure(figsize=(10, 6))
    plt.imshow(img, extent=[0, img.shape[1], img.shape[0], 0], alpha=0.5) # Altta kroki flu görünsün
    plt.contourf(xi, yi, zi, levels=15, cmap='RdYlGn', alpha=0.7) # Üstte renkli heatmap
    plt.colorbar(label='Wi-Fi Sinyal Gücü (%)')
    plt.scatter(x, y, c='black', s=20) # Tıkladığın noktalar
    plt.title("Evin Wi-Fi Kapsama Haritası")
    plt.gca().invert_yaxis() # Koordinat düzeltmesi
    plt.show()
else:
    print("Yeterli veri toplanmadı.")