import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import subprocess
import re
import pandas as pd
import numpy as np
from scipy.interpolate import griddata


def get_wifi_signal():
    try:
        
        output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('utf-8', errors='ignore')
        
        
        match = re.search(r"Signal\s*:\s*(\d+)%", output)
        if match:
            return int(match.group(1)) 
        else:
            return 0
    except:
        return 0


image_path = 'kroki.png' 
data = [] 


fig, ax = plt.subplots(figsize=(10, 6))
img = mpimg.imread(image_path)
ax.imshow(img)
plt.title("Haritada bulunduğunuz yere TIKLAYIN (Çıkmak için 'q' basın)")

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        
        x, y = event.xdata, event.ydata
        
        
        signal = get_wifi_signal()
        print(f"Konum: ({int(x)}, {int(y)}) -> Sinyal: %{signal}")
        
        
        data.append([x, y, signal])
        
        
        color = 'red' if signal < 50 else 'yellow' if signal < 75 else 'green'
        ax.plot(x, y, 'o', color=color, markersize=10, markeredgecolor='black')
        plt.draw()


cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()


if len(data) > 3: 
    df = pd.DataFrame(data, columns=['x', 'y', 'signal'])
    
    
    x = df['x']
    y = df['y']
    z = df['signal']
    
    
    xi = np.linspace(x.min(), x.max(), 100)
    yi = np.linspace(y.min(), y.max(), 100)
    xi, yi = np.meshgrid(xi, yi)
    
    
    zi = griddata((x, y), z, (xi, yi), method='linear')
    
    
    plt.figure(figsize=(10, 6))
    plt.imshow(img, extent=[0, img.shape[1], img.shape[0], 0], alpha=0.5) 
    plt.contourf(xi, yi, zi, levels=15, cmap='RdYlGn', alpha=0.7) 
    plt.colorbar(label='Wi-Fi Sinyal Gücü (%)')
    plt.scatter(x, y, c='black', s=20) 
    plt.title("Evin Wi-Fi Kapsama Haritası")
    plt.gca().invert_yaxis() 
    plt.show()
else:

    print("Yeterli veri toplanmadı.")
