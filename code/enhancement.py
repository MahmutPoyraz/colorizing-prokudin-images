import numpy as np
#Iyilestirme
def crop_borders(image, percent=0.1):
    h, w, _ = image.shape
    crop_h = int(h * percent)
    crop_w = int(w * percent)
    cropped_img = image[crop_h:-crop_h, crop_w:-crop_w]
    return cropped_img