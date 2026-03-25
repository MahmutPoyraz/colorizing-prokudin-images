import numpy as np
import matplotlib.pyplot as plt
from enhancement import crop_borders
from utils import load_image, split_image
from alignment import align_channel
import os
import cv2
proje_raporu=[]  

def ensure_3_channels(image):
    if image.ndim == 3 and image.shape[2] == 4:
        return image[:, :, :3]
    return image

def process_single_image(filepath, filename, results_dir):
    
    print(f"\n--> Uzerinde Calisiliyor: {filename}")
    try:
        img = load_image(filepath)
        b, g, r = split_image(img)
    except Exception as e:
        print(f"ERROR: {filename} okunamadı. Nedeni???: {e}")
        return
    # Gorsel-1  Hizalanma Yapilmamis Hali 3 channelli bir yapi transparencyi dahil etmiyoruz.
    naive_img = cv2.merge([b, g, r])
    # Eğer resim 0-1 arasındaysa 0-255 yapmamız lazım (3.Haftanın dersinde işlemiştik)
    if naive_img.max() <= 1.0:
        naive_img = (naive_img * 255).astype(np.uint8)
        
    cv2.imwrite(os.path.join(results_dir, filename + "_unaligned.jpg"), naive_img)
    #Hesaplama
    shift_g, _ = align_channel(b, g, search_range=15, metric='ssd')
    shift_r, _ = align_channel(b, r, search_range=15, metric='ssd')
    # Hizalama
    g_aligned = np.roll(g, shift=shift_g, axis=(0, 1))
    r_aligned = np.roll(r, shift=shift_r, axis=(0, 1))
    aligned_img = cv2.merge([b, g_aligned, r_aligned])
    if aligned_img.max() <= 1.0:
        aligned_img = (aligned_img * 255).astype(np.uint8)

    cv2.imwrite(os.path.join(results_dir, filename + "_aligned.jpg"), aligned_img)
    
    # Gorsel-3   Nihai Hali

    # Kenar Kirpma Islemi
    final_img = crop_borders(aligned_img, percent=0.07)
    cv2.imwrite(os.path.join(results_dir, filename + "_enhanced.jpg"), final_img)
    print(f"   -> Kaydedildi: {filename} (G:{shift_g}, R:{shift_r})")
    proje_raporu.append({
        "isim": filename,
        "g_vec": shift_g,
        "r_vec": shift_r
    })
    # Istenilen Gorsel Bicimini olusturma
    fig, axes = plt.subplots(3, 1, figsize=(8, 18))

    # Hizalanmamis Resim
    axes[0].imshow(np.clip(naive_img, 0, 1))
    axes[0].set_title(f"1. Hizalanmamis", fontsize=12, color='red')
    axes[0].axis('off')

    # 2. Hizalanmis resim
    axes[1].imshow(np.clip(aligned_img, 0, 1))
    axes[1].set_title(f"2. Hizalanmis (G:{shift_g}, R:{shift_r})", fontsize=12, color='blue')
    axes[1].axis('off')

    # 3. ulasilan son foto 
    axes[2].imshow(np.clip(final_img, 0, 1))
    axes[2].set_title(f"3. Nihai Sonuc", fontsize=12, color='green')
    axes[2].axis('off')

    plt.tight_layout()

    print(f"    Islem Tamamlandi!!!! Tesekkurler:)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    results_dir = os.path.join(current_dir, '..', 'results')

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    if not os.path.exists(data_dir):
        print("Dikkat!!! 'data' klasörü bulunamadı!")
    else:
        valid_extensions = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')
        image_files = [f for f in os.listdir(data_dir) if f.lower().endswith(valid_extensions)]
        if not image_files:
            print("UYARI: 'data' klasöründe resim bulunamadı!")
            print("Istenilen resimleri data klasorune atip tekrar deneyin.")
        else:
            print(f"Toplam {len(image_files)} tane gorsel bulundu. Program Basliyor!!!")
            for img_file in image_files:
                full_path = os.path.join(data_dir, img_file)
                process_single_image(full_path, img_file, results_dir)
            print("\n\nPROGRAM BASARILI BIR SEKILDE SONLANDI\nRENKLI RESIMLER 'results' KLASORUNDE\n")
            print("IYI CALISMALAR\n\n\n")



# --- PROGRAM SONU RAPOR TABLOSU ---
print("\n" + "="*75)
print(f"{'ALIGNMENT VALUES':^75}")
print("="*75)
print(f"{'Image Name':<25} | {'Green Vector':<20} | {'Red Vector':<20}")
print("-" * 75)

for veri in proje_raporu:
    # HATA BURADAYDI: 'g_shift' yerine 'g_vec' yazman lazımdı.
    # Çünkü yukarıda sözlüğe 'g_vec' adıyla kaydettik.
    g_str = str(veri['g_vec'])
    r_str = str(veri['r_vec'])
    
    print(f"{veri['isim']:<25} | {g_str:<20} | {r_str:<20}")

print("-" * 75)
print(f"Toplam İşlenen Görsel: {len(proje_raporu)}")
print("="*75)