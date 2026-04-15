import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="ELK Verify | Global", page_icon="🛡️", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    .report-box { padding: 20px; border-radius: 10px; margin: 10px 0; }
    .status-real { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .status-fake { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
    """, unsafe_allow_html=True)

# 2. Language Dictionary
languages = {
    "English": {
        "title": "🛡️ ELK Verify",
        "subtitle": "ELK Verification Network",
        "upload_label": "Upload Image",
        "button": "RUN VERIFICATION",
        "verdict": "Final Verdict",
        "is_ai": "Likely AI Generated / Manipulated",
        "is_real": "Likely Original Camera Image",
        "details": "Technical Details"
    },
    "සිංහල": {
        "title": "🛡️ ELK Verify",
        "subtitle": "ELK සත්‍යාපන ජාලය",
        "upload_label": "ඡායාරූපය ඇතුළත් කරන්න",
        "button": "පරීක්ෂාව ආරම්භ කරන්න",
        "verdict": "අවසාන නිගමනය",
        "is_ai": "AI මගින් කළ හෝ වෙනස් කළ එකක් විය හැක",
        "is_real": "කැමරාවකින් ගත් සැබෑ ඡායාරූපයක් විය හැක",
        "details": "තාක්ෂණික දත්ත"
    }
}

selected_lang = st.sidebar.selectbox("Language", list(languages.keys()))
text = languages[selected_lang]

st.markdown(f"<h1 style='text-align: center;'>{text['title']}</h1>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.file_uploader(text['upload_label'], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)

    if st.button(text['button']):
        st.subheader(f"🔍 {text['details']}")
        
        exif_data = img._getexif()
        metadata_list = []
        is_suspicious = False
        
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                metadata_list.append({"Property": tag_name, "Value": str(value)})
                if tag_name == "Software":
                    is_suspicious = True
            
            # Metadata වගුවක් ලෙස පෙන්වීම
            df = pd.DataFrame(metadata_list)
            st.table(df)
        else:
            st.error("No Metadata found in this image.")
            is_suspicious = True

        # අවසාන නිගමනය (Final Verdict)
        st.write(f"### 🚩 {text['verdict']}")
        if is_suspicious:
            st.markdown(f"<div class='report-box status-fake'>❌ <b>{text['is_ai']}</b></div>", unsafe_allow_html=True)
            st.info("හේතුව: Metadata නොමැති වීම හෝ මෘදුකාංග සලකුණු හමු වීම.")
        else:
            st.markdown(f"<div class='report-box status-real'>✅ <b>{text['is_real']}</b></div>", unsafe_allow_html=True)
            st.info("හේතුව: කැමරා දත්ත (EXIF) නිවැරදිව පවතී.")

st.write("---")
st.caption("© 2026 ELK Verification Network")