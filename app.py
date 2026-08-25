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

# --- كود CSS لتنسيق الواجهة وخلفية هندسية احترافية مع تكبير العنوان العلوي ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
}
/* تنسيق المستطيل العلوي لكلمة Al-Farida Group بحجم كبير وفخم */
.brand-box {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 22px 30px;
    border-radius: 18px;
    max-width: 500px;
    margin: 25px auto 20px auto;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.brand-text {
    color: #ffffff;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-shadow: 0 2px 10px rgba(255, 255, 255, 0.2);
}
.login-container {
    max-width: 500px;
    margin: 0 auto;
    color: white;
}
.login-container label {
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
        # مستطيل العنوان العلوي بخط كبير وفخم
        st.markdown('<div class="brand-box"><p class="brand-text">Al-Farida Group</p></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # استخدام st.form لدعم الضغط على زر Enter لتسجيل الدخول مباشرة
        with st.form("login_form"):
            st.markdown("<h2 style='text-align: center; color: white;'>🏗️ تسجيل الدخول</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8;'>منصة إدارة المشاريع الهندسية</p>", unsafe_allow_html=True)
            
            username = st.text_input("👤 اسم المستخدم", key="login_user")
            password = st.text_input("🔑 كلمة المرور", type="password", key="login_pass")
            
            st.write("")
            submit_button = st.form_submit_button("🚪 الدخول للمنصة", use_container_width=True)
            
            if submit_button:
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
    uploaded_file = st.file_uploader("اختر ملف (Excel, Word, PDF, CAD، أو مستند نصي)", type=["xlsx", "docx", "pdf", "txt", "csv", "dwg", "dxf", "jpg", "png"])

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
    header_cols = st.columns([0.4, 2.3, 0.8, 0.9, 1.8, 1.1, 1.1, 1.1])
    header_cols[0].markdown("*م*")
    header_cols[1].markdown("*اسم الملف*")
    header_cols[2].markdown("*النوع*")
    header_cols[3].markdown("*الحجم*")
    header_cols[4].markdown("*الملاحظات*")
    header_cols[5].markdown("*🌐 فتح*")
    header_cols[6].markdown("*💾 تحميل*")
    header_cols[7].markdown("*🗑️ حذف*")
    st.markdown("---")

    for idx, row in df_files.iterrows():
        row_cols = st.columns([0.4, 2.3, 0.8, 0.9, 1.8, 1.1, 1.1, 1.1])
        
        row_cols[0].markdown(f"*{idx + 1}*")
        row_cols[1].markdown(f"{row['name']}")
        row_cols[2].markdown(f"{row['type']}")
        row_cols[3].markdown(f"{row['size']}")
        row_cols[4].markdown(f"{row['note']}")
        
        # 1. زرار الفتح
        with row_cols[5]:
            if os.path.exists(str(row['path'])):
                with open(row['path'], "rb") as f:
                    file_bytes = f.read()
                b64_data = base64.b64encode(file_bytes).decode('utf-8')
                mime_type = "application/pdf" if row['type'] == "PDF" else "application/octet-stream"
                
                open_link = f'''
                <a href="data:{mime_type};base64,{b64_data}" target="_blank" style="
                    display: inline-block;
                    background-color: #ff4b4b;
                    color: white;
                    padding: 5px 8px;
                    border-radius: 4px;
                    text-decoration: none;
                    text-align: center;
                    font-size: 13px;
                    font-weight: 500;
                    width: 100%;
                ">فتح</a>
                '''
                st.markdown(open_link, unsafe_allow_html=True)
            else:
                st.error("مفقود")

        # 2. زرار التحميل
        with row_cols[6]:
            if os.path.exists(str(row['path'])):
                with open(row['path'], "rb") as file_to_download:
                    st.download_button(
                        label="تحميل",
                        data=file_to_download,
                        file_name=row['name'],
                        key=f"download_btn_{idx}",
                        use_container_width=True
                    )
            else:
                st.error("مفقود")

        # 3. زرار الحذف
        with row_cols[7]:
            if st.button("🗑️ حذف", key=f"delete_btn_{idx}", use_container_width=True):
                if os.path.exists(str(row['path'])):
                    try:
                        os.remove(row['path'])
                    except Exception:
                        pass
                
                df_files = df_files.drop(idx)
                df_files.to_csv(DB_FILE, index=False)
                st.success(f"تم حذف الملف {row['name']} بنجاح!")
                st.rerun()
            
        st.markdown("---")

st.markdown('<p style="text-align: center; color: #777;">منصة إدارة المشاريع الهندسية - تصميم وتنفيذ أنطونيوس © 2026</p>', unsafe_allow_html=True)
