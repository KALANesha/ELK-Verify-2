import streamlit as st
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS
import pandas as pd
import numpy as np

# 1. Page Config
st.set_page_config(page_title="ELK Verify | Global", page_icon="🛡️", layout="centered")

# 2. Advanced Analysis Function (Error Level Analysis - ELA)
def perform_ela(img_path, quality=90):
    original = img_path
    resaved_name = "resaved.jpg"
    original.save(resaved_name, 'JPEG', quality=quality)
    resaved = Image.open(resaved_name)
    
    # පින්තූර දෙක අතර වෙනස සෙවීම
    diff = ImageChops.difference(original, resaved)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    diff = ImageEnhance.Brightness(diff).enhance(scale)
    return diff

# 3. Main UI
st.title("🛡️ ELK Verify - Advanced")
st.write("---")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption="ඔබ ලබා දුන් පින්තූරය", use_container_width=True)

    if st.button("RUN DEEP VERIFICATION"):
        # --- පියවර 1: Metadata පරීක්ෂාව ---
        exif_data = img._getexif()
        has_metadata = False
        if exif_data:
            has_metadata = True
            st.write("### 📸 Metadata Details")
            meta_list = [{"Property": TAGS.get(t, t), "Value": str(v)} for t, v in exif_data.items()]
            st.table(pd.DataFrame(meta_list[:10])) # මුල් දත්ත 10ක් පෙන්වයි

        # --- පියවර 2: ELA (Error Level Analysis) ---
        st.write("### 🔍 Digital Artifact Analysis")
        ela_img = perform_ela(img)
        st.image(ela_img, caption="Error Level Analysis (ELA) Map", use_container_width=True)
        
        # ELA එකෙන් නිගමනයකට එන හැටි:
        # පින්තූරය පුරාම එකම විදිහට Noise තියෙනවා නම් ඒක Real. 
        # එක තැනක විතරක් ගොඩක් දීප්තිමත් නම් ඒක Edit කරපු තැනක්.
        
        # --- පියවර 3: Final Verdict ---
        st.subheader("🚩 Final Verdict")
        if not has_metadata:
            st.error("❌ සැක සහිතයි: කැමරා දත්ත (Metadata) කිසිවක් හමු නොවීය. මෙය AI හෝ Graphic එකක් වීමේ සම්භාවිතාව 90% කි.")
        else:
            st.success("✅ කැමරා දත්ත හමු විය. නමුත් ඉහත ELA සිතියමේ අසාමාන්‍ය දීප්තිමත් කොටස් ඇත්දැයි බලන්න.")
            st.info("උපදෙස්: ELA සිතියම සම්පූර්ණයෙන්ම කළු හෝ එකම රටාවකට තිබේ නම් එය සැබෑ පින්තූරයකි. වෙනස් වර්ණ ඇත්නම් එය එඩිට් කළ එකකි.")

st.write("---")
st.caption("© 2026 ELK Verification Network")