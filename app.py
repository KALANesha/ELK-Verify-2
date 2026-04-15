import streamlit as st
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="ELK Verify | Global Network", page_icon="🛡️", layout="centered")

# Custom CSS for Professional Branding
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .verdict-box { padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px; margin-top: 20px; }
    .real { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .fake { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Advanced ELA Analysis Function
def perform_ela(image, quality=90):
    original = image.convert('RGB')
    original.save("temp_resaved.jpg", 'JPEG', quality=quality)
    resaved = Image.open("temp_resaved.jpg")
    diff = ImageChops.difference(original, resaved)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0: max_diff = 1
    scale = 255.0 / max_diff
    diff = ImageEnhance.Brightness(diff).enhance(scale)
    return diff

# 3. Multi-language Support
languages = {
    "English": {
        "title": "🛡️ ELK Verify",
        "subtitle": "Global Truth Verification Network",
        "upload": "Upload Image",
        "btn": "CHECK NOW",
        "meta_title": "📸 Metadata Analysis",
        "ela_title": "🔍 Digital Artifact Analysis (ELA)",
        "verdict": "Final Verdict",
        "real_msg": "Likely Original Camera Image",
        "fake_msg": "Likely AI Generated or Modified",
        "reason": "Reasoning"
    },
    "සිංහල": {
        "title": "🛡️ ELK Verify",
        "subtitle": "ELK සත්‍යාපන ජාලය",
        "upload": "ඡායාරූපය ඇතුළත් කරන්න",
        "btn": "පරීක්ෂා කරන්න",
        "meta_title": "📸 Metadata පරීක්ෂාව",
        "ela_title": "🔍 ඩිජිටල් ව්‍යුහය පරීක්ෂාව (ELA)",
        "verdict": "අවසාන නිගමනය",
        "real_msg": "කැමරාවකින් ගත් සැබෑ ඡායාරූපයක් විය හැක",
        "fake_msg": "AI මගින් කළ හෝ වෙනස් කළ එකක් විය හැක",
        "reason": "හේතුව"
    }
}

# Language Selector
sel_lang = st.sidebar.selectbox("Language / භාෂාව", list(languages.keys()))
t = languages[sel_lang]

# 4. UI Layout
st.markdown(f"<h1 style='text-align: center;'>{t['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t['subtitle']}</p>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader(t['upload'], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Target Image", use_container_width=True)

    if st.button(t['btn']):
        st.write("---")
        
        # --- Metadata Logic ---
        st.subheader(t['meta_title'])
        exif = img._getexif()
        has_meta = False
        is_edited = False
        
        if exif:
            has_meta = True
            m_data = []
            for tag, val in exif.items():
                tag_name = TAGS.get(tag, tag)
                m_data.append({"Property": tag_name, "Value": str(val)})
                if tag_name == "Software": is_edited = True
            st.table(pd.DataFrame(m_data).head(10))
        else:
            st.warning("No Metadata found.")

        # --- ELA Logic ---
        st.subheader(t['ela_title'])
        ela_img = perform_ela(img)
        st.image(ela_img, caption="Error Level Analysis Map", use_container_width=True)
        st.info("Tip: Uniform noise = Real | Bright spots = Edited")

        # --- Final Verdict Logic ---
        st.subheader(f"🚩 {t['verdict']}")
        
        # නිගමනය තීරණය කිරීම
        if not has_meta or is_edited:
            st.markdown(f"<div class='verdict-box fake'>❌ {t['fake_msg']}</div>", unsafe_allow_html=True)
            reason_text = "Metadata missing or software traces found." if sel_lang=="English" else "Metadata නොමැති වීම හෝ මෘදුකාංග සලකුණු හමු වීම."
        else:
            st.markdown(f"<div class='verdict-box real'>✅ {t['real_msg']}</div>", unsafe_allow_html=True)
            reason_text = "Valid Camera Metadata present." if sel_lang=="English" else "නිවැරදි කැමරා දත්ත පවතී."
            
        st.write(f"**{t['reason']}:** {reason_text}")

st.write("---")
st.caption("© 2026 ELK Verification Network | Global Integrity Standard")