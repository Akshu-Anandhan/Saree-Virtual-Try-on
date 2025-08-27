import streamlit as st
from PIL import Image, ImageEnhance
import numpy as np
from segmentation import segment_person, estimate_pose_keypoints
from vto_core import generate_tryon, FabricParams
from recommend import suggest_blouse_styles, suggest_jewellery, look_bundle_cards
from utils_color import extract_palette, describe_palette

st.set_page_config(page_title="Virtual Saree Try-On", layout="wide")
st.title("👗 Virtual Saree Try-On")

# Upload user photo
user_photo = st.file_uploader("📸 Upload your full-body photo", type=["jpg", "jpeg", "png"])
saree_img = st.file_uploader("📷 Upload saree image (flat or draped)", type=["jpg","jpeg","png"])

# Saree fabric options
saree_type = st.selectbox(
    "🧵 Choose a saree fabric",
    ["Cotton", "Silk", "Organza", "Georgette", "Chiffon", "Crepe", "Banarasi", "Kanjivaram"]
)

occasion = st.selectbox("Occasion", ["Daily wear","Office","Festive","Wedding guest","Bridal","Party"])

transparency = st.slider("Sheerness", 0.0, 0.7, 0.15, 0.05)
gloss = st.slider("Silk shine", 0.0, 1.0, 0.45, 0.05)
wrinkle = st.slider("Wrinkle scale", 0.0, 1.0, 0.25, 0.05)

if user_photo:
    img = Image.open(user_photo).convert("RGB")
    st.image(img, caption="Uploaded photo", use_column_width=True)
else:
    st.info("Upload your photo to see the try-on preview.")

if user_photo and saree_img:
    saree = Image.open(saree_img).convert("RGB")
    st.image(saree, caption="Saree image (catalog)", use_column_width=True)

    with st.spinner("Segmenting & generating try-on..."):
        mask = segment_person(img)
        keypoints = estimate_pose_keypoints(img)
        fab = FabricParams.from_ui(saree_type, transparency=transparency, gloss=gloss, wrinkle=wrinkle)
        palette = extract_palette(saree, n_colors=6)
        st.caption(describe_palette(palette))
        tryon, quality = generate_tryon(img, mask, keypoints, saree, fab)
        st.image(tryon, caption=f"Try-On • Confidence {int(quality*100)}%", use_column_width=True)

    st.markdown("### Blouse Suggestions")
    blouse_rec = suggest_blouse_styles(saree_type, palette, occasion)
    for s in blouse_rec:
        st.markdown(f"- **{s['name']}** — {s['why']}")

    st.markdown("### Jewellery Suggestions")
    jewels = suggest_jewellery(palette, occasion, saree_type)
    for j in jewels:
        st.markdown(f"- **{j['name']}** — {j['why']}")

    st.markdown("### Complete the Look")
    st.write(look_bundle_cards(blouse_rec, jewels))
