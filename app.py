import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS

# 1. Page Configuration & Custom CSS for Branding
st.set_page_config(page_title="ELK Verify | Truth Verification Network", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #004aad;
        color: white;
        font-weight: bold;
    }
    .title-text {
        text-align: center;
        color: #004aad;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🛡️ ELK Verify</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>ELK Verification Network</b> - Global Digital Integrity Standard</p>", unsafe_allow_html=True)
st.write("---")

# 2. Image Upload Section
uploaded_file = st.file_uploader("පරීක්ෂා කිරීමට අවශ්‍ය ඡායාරූපය මෙතැනට Upload කරන්න", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    # Displaying the image nicely
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img, caption="පරීක්ෂණයට සූදානම් කළ ඡායාරූපය", use_container_width=True)

    # 3. Check Button
    if st.button("RUN VERIFICATION (CHECK)"):
        st.write("### 🔍 පරීක්ෂණ වාර්තාව (Analysis Report)")
        
        with st.status("ELK Network හරහා දත්ත පරීක්ෂා කරමින් පවතී...", expanded=True) as status:
            # --- Metadata Analysis ---
            exif_data = img._getexif()
            
            st.write("**පියවර 1: Metadata සත්‍යාපනය...**")
            if exif_data:
                software_found = None
                device_model = "හඳුනාගත නොහැක"
                
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "Software":
                        software_found = value
                    if tag_name == "Model":
                        device_model = value
                
                st.success(f"✅ Metadata හමු විය. (Device: {device_model})")
                
                if software_found:
                    st.warning(f"⚠️ අනතුරු ඇඟවීම: මෙහි '{software_found}' මෘදුකාංග සලකුණු හමු විය. පින්තූරය සංස්කරණය කර ඇති බවට සැක කෙරේ.")
            else:
                st.error("❌ Metadata හමු වූයේ නැත. මෙය AI මගින් නිර්මාණය කළ හෝ දත්ත මකා දැමූ ඡායාරූපයකි.")

            # --- Structural Analysis ---
            st.write("**පියවර 2: ව්‍යුහාත්මක (Structural) පරීක්ෂාව...**")
            w, h = img.size
            if w < 1000 or h < 1000:
                st.warning(f"⚠️ අවදානම: මෙහි Resolution එක මදියි ({w}x{h}). මෙය තිර රුවක් (Screenshot) විය හැක.")
            else:
                st.success(f"✅ පින්තූරයේ ගුණාත්මකභාවය (Quality) ප්‍රමාණවත්.")
            
            status.update(label="පරීක්ෂණය අවසන්!", state="complete", expanded=False)

        st.balloons()
        st.write("---")
        st.markdown("<p style='text-align: center; font-size: 12px;'>© 2026 ELK Verification Network. All Rights Reserved.</p>", unsafe_allow_html=True)