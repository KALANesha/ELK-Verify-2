import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS

# 1. Page Config
st.set_page_config(page_title="ELK Verify | Global", page_icon="🛡️", layout="centered")

# 2. Language Dictionary (භාෂා එකතු කිරීම)
languages = {
    "English": {
        "title": "🛡️ ELK Verify",
        "subtitle": "Global Digital Integrity Standard",
        "upload_label": "Upload Image for Verification",
        "button": "RUN VERIFICATION",
        "report": "Analysis Report",
        "status": "Checking through ELK Network...",
        "meta_ok": "Metadata Found",
        "meta_error": "No Metadata: Possible AI or Stripped Image",
        "edit_warn": "Warning: Software editing detected!",
        "res_low": "Warning: Low resolution. Possible screenshot.",
        "res_ok": "Resolution quality is satisfactory."
    },
    "සිංහල": {
        "title": "🛡️ ELK Verify",
        "subtitle": "ELK Verification Network - ගෝලීය සත්‍යාපන ප්‍රමිතිය",
        "upload_label": "පරීක්ෂා කිරීමට අවශ්‍ය ඡායාරූපය ඇතුළත් කරන්න",
        "button": "පරීක්ෂාව ආරම්භ කරන්න",
        "report": "පරීක්ෂණ වාර්තාව",
        "status": "ELK Network හරහා පරීක්ෂා කරමින් පවතී...",
        "meta_ok": "Metadata හමු විය",
        "meta_error": "Metadata නැත: AI මගින් කළ එකක් විය හැක",
        "edit_warn": "අනතුරු ඇඟවීම: මෘදුකාංග මගින් සංස්කරණය කර ඇත!",
        "res_low": "අනතුරු ඇඟවීම: Resolution මදියි. මෙය Screenshot එකක් විය හැක.",
        "res_ok": "Resolution ගුණාත්මකභාවය සතුටුදායකයි."
    },
    "中文 (Chinese)": {
        "title": "🛡️ ELK Verify",
        "subtitle": "全球数字诚信标准",
        "upload_label": "上传图片进行验证",
        "button": "开始验证",
        "report": "分析报告",
        "status": "正在通过 ELK 网络检查...",
        "meta_ok": "找到元数据",
        "meta_error": "无元数据：可能是人工智能生成",
        "edit_warn": "警告：检测到软件编辑！",
        "res_low": "警告：分辨率低。可能是截图。",
        "res_ok": "分辨率质量令人满意。"
    }
}

# 3. Sidebar Language Selector (භාෂාව තෝරන බටන් එක)
st.sidebar.title("Settings")
selected_lang = st.sidebar.selectbox("Select Language / භාෂාව තෝරන්න", list(languages.keys()))
text = languages[selected_lang]

# --- UI Branding ---
st.markdown(f"<h1 style='text-align: center; color: #004aad;'>{text['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>{text['subtitle']}</b></p>", unsafe_allow_html=True)
st.write("---")

# 4. Main App Logic
uploaded_file = st.file_uploader(text['upload_label'], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)

    if st.button(text['button']):
        st.write(f"### 🔍 {text['report']}")
        
        with st.status(text['status']) as status:
            # Metadata Analysis
            exif_data = img._getexif()
            if exif_data:
                st.success(f"✅ {text['meta_ok']}")
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "Software":
                        st.warning(text['edit_warn'])
            else:
                st.error(f"❌ {text['meta_error']}")

            # Resolution Analysis
            w, h = img.size
            if w < 1000 or h < 1000:
                st.warning(text['res_low'])
            else:
                st.success(f"✅ {text['res_ok']}")
            
            status.update(label="Complete!", state="complete")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 10px;'>© 2026 ELK Verification Network</p>", unsafe_allow_html=True)