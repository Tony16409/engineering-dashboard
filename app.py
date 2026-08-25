import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة إدارة المشاريع الهندسية", page_icon="🏗️", layout="wide")

# --- إنشاء مجلد حفظ الملفات وقاعدة البيانات لو مش موجودين ---
UPLOAD_DIR = "uploaded_files"
DB_FILE = "files_db.csv"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

if not os.path.exists(DB_FILE):
    df_init = pd.DataFrame(columns=["name", "type", "size", "note", "date", "path"])
    df_init.to_csv(DB_FILE, index=False)

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

# --- قسم رفع الملفات ---
st.subheader("📤 رفع مستند أو مخطط جديد")
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("اختر ملف (Excel, PDF, CAD، أو مستند نصي)", type=["xlsx", "pdf", "txt", "csv", "dwg", "dxf", "jpg", "png"])

with col2:
    note = st.text_input("📝 ملاحظات على الملف (اختياري)", key="file_note")

if st.button("💾 حفظ ورفع الملف", type="primary"):
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        file_size_kb = uploaded_file.size / 1024
        file_size_str = f"{file_size_kb / 1024:.1f} MB" if file_size_kb > 1024 else f"{file_size_kb:.1f} KB"
        file_ext = uploaded_file.name.split('.')[-1].upper()
        
        df = pd.read_csv(DB_FILE)
        new_row = pd.DataFrame([{
            "name": uploaded_file.name,
            "type": file_ext,
            "size": file_size_str,
            "note": note if note else "بدون ملاحظات",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "path": file_path
        }])
        
        df = pd.concat([new_row, df], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        
        st.success(f"✅ تم حفظ الملف بشكل دائم ورفعه بنجاح: {uploaded_file.name}")
        st.rerun()
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")

# --- سجل الملفات والمقاييس ---
st.subheader("📋 سجل الملفات والمقاييس المرفوعة والمرقمة (حفظ دائم)")

df_files = pd.read_csv(DB_FILE)

if df_files.empty:
    st.info("ℹ️ لم يتم رفع أي ملفات حتى الآن. قم برفع ملف أعلاه.")
else:
    header_cols = st.columns([0.5, 2.6, 0.9, 1.0, 2.0, 1.2, 1.2])
    header_cols[0].markdown("م")
    header_cols[1].markdown("اسم الملف")
    header_cols[2].markdown("النوع")
    header_cols[3].markdown("الحجم")
    header_cols[4].markdown("الملاحظات")
    header_cols[5].markdown("🌐 عرض مباشر")
    header_cols[6].markdown("💾 تحميل")
    st.markdown("---")

    for idx, row in df_files.iterrows():
        row_cols = st.columns([0.5, 2.6, 0.9, 1.0, 2.0, 1.2, 1.2])
        
        row_cols[0].markdown(f"{idx + 1}")
        row_cols[1].markdown(f"{row['name']}")
        row_cols[2].markdown(f"{row['type']}")
        row_cols[3].markdown(f"{row['size']}")
        row_cols[4].markdown(f"{row['note']}")
        
        with row_cols[5]:
            if st.button("🌐 عرض", key=f"view_btn_{idx}", use_container_width=True):
                st.session_state[f"show_file_{idx}"] = not st.session_state.get(f"show_file_{idx}", False)

        with row_cols[6]:
            if os.path.exists(row['path']):
                with open(row['path'], "rb") as file_to_download:
                    st.download_button(
                        label="📥 تحميل",
                        data=file_to_download,
                        file_name=row['name'],
                        key=f"download_btn_{idx}",
                        use_container_width=True
                    )
            else:
                st.error("مفقود")
        
        if st.session_state.get(f"show_file_{idx}", False):
            st.info(f"📄 معاينة الملف: {row['name']}")
            if os.path.exists(row['path']):
                file_ext = row['name'].split('.')[-1].lower()
                if file_ext == 'pdf':
                    with open(row['path'], "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0" width="100%" height="600px" style="border:1px solid #ccc; border-radius:8px;"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                elif file_ext in ['jpg', 'jpeg', 'png']:
                    st.image(row['path'], caption=row['name'], use_container_width=True)
                elif file_ext in ['xlsx', 'csv']:
                    df_view = pd.read_excel(row['path']) if file_ext == 'xlsx' else pd.read_csv(row['path'])
                    st.dataframe(df_view, use_container_width=True)
                elif file_ext == 'txt':
                    with open(row['path'], "r", encoding="utf-8", errors="ignore") as tf:
                        st.text_area("محتوى الملف:", tf.read(), height=250)
                else:
                    st.warning("⚠️ عذراً، هذا الامتداد غير معمول له معاينة مباشرة. يمكنك تحميله بالضغط على زر تحميل.")
            else:
                st.error("⚠️ الملف غير موجود على الخادم.")
            
        st.markdown("---")

st.markdown('<p style="text-align: center; color: #777;">منصة إدارة المشاريع الهندسية - تصميم وتنفيذ أنطونيوس © 2026</p>', unsafe_allow_html=True)
