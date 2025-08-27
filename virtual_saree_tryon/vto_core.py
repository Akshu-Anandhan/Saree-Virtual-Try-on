import numpy as np
import cv2
from PIL import Image

def pil_to_np(img):
    return np.array(img)

class FabricParams:
    def __init__(self, stiffness: float, specular: float, roughness: float, transparency: float, wrinkle: float):
        self.stiffness = stiffness
        self.specular = specular
        self.roughness = roughness
        self.transparency = transparency
        self.wrinkle = wrinkle

    @staticmethod
    def from_ui(fabric_type: str, transparency: float, gloss: float, wrinkle: float):
        base = {
            "Silk":      dict(stiff=0.35, spec=0.8, rough=0.2),
            "Cotton":    dict(stiff=0.55, spec=0.2, rough=0.7),
            "Organza":   dict(stiff=0.65, spec=0.6, rough=0.3),
            "Linen":     dict(stiff=0.6,  spec=0.25, rough=0.6),
            "Chiffon":   dict(stiff=0.25, spec=0.5, rough=0.4),
            "Georgette": dict(stiff=0.4,  spec=0.4, rough=0.5),
            "Banarasi":  dict(stiff=0.5,  spec=0.7, rough=0.35),
            "Kanjivaram':dict(stiff=0.55, spec=0.75,rough=0.35),
        }.get(fabric_type, dict(stiff=0.5, spec=0.4, rough=0.5))
        return FabricParams(base["stiff"], gloss, base["rough"], transparency, wrinkle)

def generate_tryon(user_img_pil, person_mask_u8, keypoints, saree_img_pil, fab: FabricParams):
    bg = pil_to_np(user_img_pil)
    h, w = bg.shape[:2]
    saree = pil_to_np(saree_img_pil)
    saree = cv2.resize(saree, (min(700, saree.shape[1]), int(saree.shape[0]*min(700, saree.shape[1])/saree.shape[1])))
    # Place saree as overlay on torso area (simplified demo)
    y, x = h//4, w//4
    overlay = np.zeros_like(bg)
    sh, sw = saree.shape[:2]
    overlay[y:y+sh, x:x+sw] = saree
    mask = (overlay.sum(axis=2) > 0).astype("uint8")*255
    comp = bg.copy()
    comp[mask>0] = overlay[mask>0]
    quality = 0.85
    return comp, quality
