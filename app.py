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
# --- لوحة التحكم الرئيسية ---
# =================================================================

st.markdown('<h1 style="text-align: center; color: #333; background: #fff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">📂 لوحة تحكم إدارة الملفات والمشاريع الهندسية 📂</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; color: #555;">أهلاً بك يا باشمهندس أنطونيوس | التاريخ: {datetime.now().strftime("%Y-%m-%d")}</p>', unsafe_allow_html=True)
st.markdown("---")

if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state["authenticated"] = False
    st.rerun()

# --- تهيئة قائمة الملفات في الذاكرة مع حفظ محتوى الملف نفسه للفتح والتحميل ---
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
        file_size_kb = uploaded_file.size / 1024
        file_size_str = f"{file_size_kb / 1024:.1f} MB" if file_size_kb > 1024 else f"{file_size_kb:.1f} KB"
        file_ext = uploaded_file.name.split('.')[-1].upper()
        
        # حفظ بيانات الملف ومحتواه الفعلي عشان نقدر نفتحه ونتحكم فيه
        new_file_data = {
            "name": uploaded_file.name,
            "type": file_ext,
            "size": file_size_str,
            "note": note if note else "بدون ملاحظات",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "data": uploaded_file.getvalue() # الاحتفاظ بمحتوى الملف البايتس
        }
        st.session_state["files_list"].insert(0, new_file_data)
        st.success(f"✅ تم رفع الملف بنجاح: {uploaded_file.name}")
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")
# زرار الفتح والمعاينة مباشرة جوه المنصة
        with row_cols[5]:
            if st.button("👁️ فتح بالمنصة", key=f"view_btn_{idx}"):
                st.session_state["active_view"] = idx
                
        # زرار التحميل في خانة لوحده جنبه
        with row_cols[6]:
            st.download_button(
                label="📥 تحميل",
                data=file_info["data"],
                file_name=file_info["name"],
                key=f"download_btn_{idx}"
            )
            
        st.markdown("---")

# --- معاينة الملف المختار جوه المنصة مباشرة ---
if "active_view" in st.session_state:
    idx = st.session_state["active_view"]
    if idx < len(st.session_state["files_list"]):
        selected_file = st.session_state["files_list"][idx]
        st.markdown(f"### 🔍 معاينة الملف: {selected_file['name']}")
        
        file_ext = selected_file['name'].split('.')[-1].lower()
        
        # لو الملف PDF نعرضه مباشرة جوه المنصة بشاشة واضحة
        if file_ext == 'pdf':
            base64_pdf = base64.b64encode(selected_file["data"]).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
        # لو صورة نعرضها مباشرة
        elif file_ext in ['png', 'jpg', 'jpeg']:
            st.image(selected_file["data"], caption=selected_file['name'], use_column_width=True)
            
        # لو ملف نصي أو كود نعرضه
        elif file_ext in ['txt', 'csv']:
            text_content = selected_file["data"].decode('utf-8')
            st.text_area("محتوى الملف:", text_content, height=300)
            
        else:
            st.info(f"📁 نوع الملف ({file_ext}) جاهز للتحميل المباشر.")
            
        if st.button("❌ إغلاق المعاينة"):
            del st.session_state["active_view"]
            st.rerun()
