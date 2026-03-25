import numpy as np

def ssd_metric(img1, img2):
    if img1.shape != img2.shape:
        raise ValueError("Boyut Hatasi")
    diff = img1 - img2
    ssd = np.sum(diff ** 2) 
    return ssd
def ncc_metric(img1, img2):
    if img1.shape != img2.shape:
        raise ValueError("Boyut Hatasi")
    img1_norm = (img1 - np.mean(img1)) / (np.std(img1) + 1e-10)
    img2_norm = (img2 - np.mean(img2)) / (np.std(img2) + 1e-10)
   
    ncc = np.sum(img1_norm * img2_norm)
    return ncc
def align_channel(base_channel, align_channel, search_range=15, metric='ssd'):
    best_score = float('inf') if metric == 'ssd' else -1
    best_shift = (0, 0)
    
    # Kirpma islemine giriyoruz
    h, w = base_channel.shape
    crop_h, crop_w = h // 5, w // 5
    base_cropped = base_channel[crop_h:-crop_h, crop_w:-crop_w]
    for dy in range(-search_range, search_range + 1):
        for dx in range(-search_range, search_range + 1):
            shifted = np.roll(align_channel, shift=(dy, dx), axis=(0, 1))
            shifted_cropped = shifted[crop_h:-crop_h, crop_w:-crop_w]
            if metric == 'ssd':
                score = ssd_metric(base_cropped, shifted_cropped)
                if score < best_score: 
                    best_score = score
                    best_shift = (dy, dx)
            elif metric == 'ncc':
                score = ncc_metric(base_cropped, shifted_cropped)
                if score > best_score:  
                    best_score = score
                    best_shift = (dy, dx)
                    
    return best_shift, best_score