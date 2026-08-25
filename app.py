import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Al-Farida Group", page_icon="🏗️", layout="wide")

# --- كود CSS لتخلي الصورة خلفية لجزء تسجيل الدخول (Card) ---
st.markdown("""
<style>
/* خلفية الصفحة العامة لون هادئ */
[data-testid="stAppViewContainer"] {
    background-color: #f4f6f9;
}
/* تنسيق كارد تسجيل الدخول وتثبيت صورتك الخلفية جواها */
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
        st.markdown("<h2>🏗️ Log in</h2>", unsafe_allow_html=True)
        st.markdown("<p>Al-Farida Group</p>", unsafe_allow_html=True)
        
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

st.subheader("📤 رفع مستند أو مخطط جديد")
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("اختر ملف (Excel, PDF, CAD، أو مستند نصي)", type=["xlsx", "pdf", "txt", "csv", "dwg", "dxf", "jpg", "png"])

with col2:
    note = st.text_input("📝 ملاحظات على الملف (اختياري)")

if st.button("💾 حفظ ورفع الملف", type="primary"):
    if uploaded_file is not None:
        st.success(f"✅ تم رفع الملف بنجاح: {uploaded_file.name}")
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")
st.subheader("📋 سجل الملفات والمقاييس المرفوعة")

data = {
    "اسم الملف": ["مشروع_فيلا_الرياض_واجهة.dwg", "جدول_كميات_مول_جدة.xlsx", "تقرير_تربة_مشروع_القاهرة.pdf", "مخطط_كهرباء_فيلا.pdf"],
    "النوع": ["CAD", "Excel", "PDF", "PDF"],
    "الحجم": ["15.2 MB", "1.2 MB", "500 KB", "2.8 MB"],
    "الملاحظات": ["معتمد من الاستشاري", "نسخة أولية للمراجعة", "مختوم وموقع", ""],
    "تاريخ الرفع": ["2024-08-25", "2024-08-24", "2024-08-23", "2024-08-22"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align: center; color: #777;">منصة إدارة المشاريع الهندسية - تصميم وتنفيذ مهندس أنطونيوس © 2026</p>', unsafe_allow_html=True)
