import numpy as np
from PIL import Image
import mediapipe as mp

mp_selfie = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)
mp_pose = mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1)

def _pil_to_np(img):
    return np.array(img)

def segment_person(img_pil):
    img = _pil_to_np(img_pil)
    results = mp_selfie.process(img)
    mask = (results.segmentation_mask > 0.5).astype("uint8") * 255
    return mask

def estimate_pose_keypoints(img_pil):
    img = _pil_to_np(img_pil)
    results = mp_pose.process(img)
    h, w, _ = img.shape
    kps = {}
    if results.pose_landmarks:
        for i, lm in enumerate(results.pose_landmarks.landmark):
            kps[i] = (int(lm.x * w), int(lm.y * h), lm.visibility)
    return kps
