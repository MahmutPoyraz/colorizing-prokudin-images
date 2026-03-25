import numpy as np
import cv2

def load_image(filepath):
    # Normalizasyon 
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Yukleme Basarisiz: {filepath}")
    # 0-255 arasi degerleri 0-1 arasina getir dersin 3. hafta konusunda gormustuk.
    img_float = img.astype(np.float32) / 255.0
    return img_float
def split_image(image):
    height, width = image.shape
    third_height = height // 3
    b_channel = image[0:third_height, :]               # Blue Channel
    g_channel = image[third_height:2*third_height, :]  # Green Chanel
    r_channel = image[2*third_height:3*third_height, :] # Red Cahannel
    return b_channel, g_channel, r_channel