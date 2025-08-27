import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

def extract_palette(img_pil: Image.Image, n_colors=6):
    arr = np.array(img_pil).reshape(-1,3).astype("float32")
    idx = np.random.choice(arr.shape[0], size=min(2000, arr.shape[0]), replace=False)
    km = KMeans(n_clusters=n_colors, n_init="auto", random_state=42).fit(arr[idx])
    centers = km.cluster_centers_.astype("uint8")
    return [tuple(map(int,c)) for c in centers]

def describe_palette(palette):
    return f"Detected colors: {palette[:4]}"
