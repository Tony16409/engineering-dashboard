import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة إدارة المشاريع الهندسية", page_icon="🏗️", layout="wide")

# --- كود CSS لتنسيق واجهة الدخول والخلفية ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f4f6f9;
}
.login-card {
    background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("https://images.unsplash.com/photo-1581094264568-6190d67d0736?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    max-width: 450px;
    margin: 12vh auto;
    text-align: center;
    color: white;
}
.login-card h2, .login-card p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --- إدارة حالة تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- شاشة تسجيل الدخول ---
if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h2>🏗️ تسجيل الدخول</h2>", unsafe_allow_html=True)
        st.markdown("<p>منصة إدارة المشاريع الهندسية</p>", unsafe_allow_html=True)
        
        username = st.text_input("👤 اسم المستخدم")
        password = st.text_input("🔑 كلمة المرور", type="password")
        
        st.write("")
        if st.button("🚪 الدخول للمنصة", type="primary", use_container_width=True):
            if username == "admin" and password == "1234":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.stop()

# =================================================================
# --- لوحة التحكم الرئيسية (تظهر بكامل الشاشة بعد تسجيل الدخول) ---
# =================================================================

st.markdown('<h1 style="text-align: center; color: #333; background: #fff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">📂 لوحة تحكم إدارة الملفات والمشاريع الهندسية 📂</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; color: #555;">أهلاً بك يا باشمهندس أنطونيوس | التاريخ: {datetime.now().strftime("%Y-%m-%d")}</p>', unsafe_allow_html=True)
st.markdown("---")

if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state["authenticated"] = False
    st.rerun()

# --- تهيئة قائمة الملفات في الذاكرة ---
if "files_list" not in st.session_state:
    st.session_state["files_list"] = []

# --- قسم رفع الملفات ---
st.subheader("📤 رفع مستند أو مخطط جديد")
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("اختر ملف (Excel, PDF, CAD، أو مستند نصي)", type=["xlsx", "pdf", "txt", "csv", "dwg", "dxf", "jpg", "png"])

with col2:
    note = st.text_input("📝 ملاحظات على الملف (اختياري)", key="file_note")

if st.button("💾 حفظ ورفع الملف", type="primary"):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_size_kb = len(file_bytes) / 1024
        file_size_str = f"{file_size_kb / 1024:.1f} MB" if file_size_kb > 1024 else f"{file_size_kb:.1f} KB"
        file_ext = uploaded_file.name.split('.')[-1].upper()
        
        new_file_data = {
            "name": uploaded_file.name,
            "type": file_ext,
            "size": file_size_str,
            "note": note if note else "بدون ملاحظات",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "data": file_bytes
        }
        st.session_state["files_list"].insert(0, new_file_data)
        st.success(f"✅ تم رفع الملف بنجاح وإضافته للجدول: {uploaded_file.name}")
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")
# --- سجل الملفات والمقاييس (جدول مرتب بأعمدة مستقلة لـ "فتح بالمتصفح" و "تحميل") ---
st.subheader("📋 سجل الملفات والمقاييس المرفوعة والمرقمة")

if not st.session_state["files_list"]:
    st.info("ℹ️ لم يتم رفع أي ملفات حتى الآن. قم برفع ملف أعلاه.")
else:
    # رأس الجدول الاحترافي
    header_cols = st.columns([0.6, 2.5, 0.9, 1.1, 1.8, 1.2, 1.2])
    header_cols[0].markdown("م")
    header_cols[1].markdown("اسم الملف")
    header_cols[2].markdown("النوع")
    header_cols[3].markdown("الحجم")
    header_cols[4].markdown("الملاحظات")
    header_cols[5].markdown("🌐 فتح بالمتصفح")
    header_cols[6].markdown("💾 تحميل")
    st.markdown("---")

    # عرض الصفوف مرقمة
    for idx, file_info in enumerate(st.session_state["files_list"]):
        row_cols = st.columns([0.6, 2.5, 0.9, 1.1, 1.8, 1.2, 1.2])
        
        row_cols[0].markdown(f"{idx + 1}")
        row_cols[1].markdown(f"{file_info['name']}")
        row_cols[2].markdown(f"{file_info['type']}")
        row_cols[3].markdown(f"{file_info['size']}")
        row_cols[4].markdown(f"{file_info['note']}")
        
        # زرار الفتح بمتصفح كروم في خانة مستقلة
        with row_cols[5]:
            b64 = base64.b64encode(file_info["data"]).decode('utf-8')
            file_ext = file_info['name'].split('.')[-1].lower()
            mime_map = {
                'pdf': 'application/pdf',
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'txt': 'text/plain'
            }
            mime_type = mime_map.get(file_ext, 'application/octet-stream')
            open_link = f'<a href="data:{mime_type};base64,{b64}" target="_blank" style="padding:6px 12px; background-color:#1976D2; color:white; border-radius:5px; text-decoration:none; font-size:14px;">🌐 فتح بمتصفح</a>'
            st.markdown(open_link, unsafe_allow_html=True)
            
        # زرار التحميل في خانة مستقلة
        with row_cols[6]:
            st.download_button(
                label="📥 تحميل",
                data=file_info["data"],
                file_name=file_info["name"],
                key=f"download_btn_{idx}"
            )
            
        st.markdown("---")

st.markdown('<p style="text-align: center; color: #777;">منصة إدارة المشاريع الهندسية - تصميم وتنفيذ أنطونيوس © 2026</p>', unsafe_allow_html=True)
