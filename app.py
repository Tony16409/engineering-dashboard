import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة إدارة المشاريع الهندسية", page_icon="🏗️", layout="wide")

# --- كود CSS للخلفية (الصورة الجديدة) والتصميم ---
st.markdown("""
<style>
/* تعيين الصورة الجديدة كخلفية للصفحة */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1581094264568-6190d67d0736?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
/* تأثير تعتيم بسيط للصورة عشان الكلام يظهر بوضوح */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4); /* لون أسود شفاف بنسبة 40% */
    z-index: -1;
}
/* تنسيق كارد تسجيل الدخول */
.login-card {
    background-color: rgba(255, 255, 255, 0.9); /* خلفية بيضاء شبه شفافة */
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    max-width: 420px;
    margin: 15vh auto; /* توسيط رأسي وأفقي */
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- إدارة حالة تسجيل الدخول ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- شاشة تسجيل الدخول (تظهر لو لم يتم الدخول بعد) ---
if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1, 2, 1]) # عمل أعمدة لتوسيط الكارد
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h2>🏗️ تسجيل الدخول</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666;'>منصة إدارة المشاريع الهندسية</p>", unsafe_allow_html=True)
        
        # --- مدخلات اسم المستخدم وكلمة المرور ---
        username = st.text_input("👤 اسم المستخدم")
        password = st.text_input("🔑 كلمة المرور", type="password")
        
        st.write("")
        # --- زرار الدخول ---
        if st.button("🚪 الدخول للمنصة", type="primary", use_container_width=True):
            # التحقق من كلمة المرور
            if username == "admin" and password == "1234":
                st.session_state["authenticated"] = True
                st.rerun() # إعادة تحميل الصفحة للدخول
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.stop() # منع تنفيذ باقي الكود لحد ما يتم تسجيل الدخول

# =================================================================
# --- لوحة التحكم الرئيسية (تظهر بكامل الشاشة بعد تسجيل الدخول) ---
# =================================================================

# عنوان اللوحة
st.markdown('<h1 style="text-align: center; color: #333; background: rgba(255, 255, 255, 0.7); padding: 15px; border-radius: 10px;">📂 لوحة تحكم إدارة الملفات والمشاريع الهندسية 📂</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; color: #555; background: rgba(255, 255, 255, 0.7); padding: 5px; border-radius: 5px;">أهلاً بك يا باشمهندس أنطونيوس | التاريخ: {datetime.now().strftime("%Y-%m-%d")}</p>', unsafe_allow_html=True)
st.markdown("---")

# زر تسجيل الخروج في الشريط الجانبي
if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state["authenticated"] = False
    st.rerun()

# --- قسم رفع الملفات ---
st.subheader("📤 رفع مستند أو مخطط جديد")
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("اختر ملف (Excel, PDF, CAD، أو مستند نصي)", type=["xlsx", "pdf", "txt", "csv", "dwg", "dxf", "jpg", "png"])

with col2:
    note = st.text_input("📝 ملاحظات على الملف (اختياري)")

# زر حفظ ورفع الملف
if st.button("💾 حفظ ورفع الملف", type="primary"):
    if uploaded_file is not None:
        st.success(f"✅ تم رفع الملف بنجاح: {uploaded_file.name}")
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")

# --- سجل الملفات والمقاييس المرفوعة ---
st.subheader("📋 سجل الملفات والمقاييس المرفوعة")
# بيانات وهمية مؤقتة (للتجربة)
data = {
    "اسم الملف": ["مشروع_فيلا_الرياض_واجهة.dwg", "جدول_كميات_مول_جدة.xlsx", "تقرير_تربة_مشروع_القاهرة.pdf", "مخطط_كهرباء_فيلا.pdf"],
    "النوع": ["CAD", "Excel", "PDF", "PDF"],
    "الحجم": ["15.2 MB", "1.2 MB", "500 KB", "2.8 MB"],
    "الملاحظات": ["معتمد من الاستشاري", "نسخة أولية للمراجعة", "مختوم وموقع", ""],
    "تاريخ الرفع": ["2024-08-25", "2024-08-24", "2024-08-23", "2024-08-22"]
}
df = pd.DataFrame(data)

# عرض الجدول
st.dataframe(df, use_container_width=True)

# تذييل الصفحة
st.markdown("---")
st.markdown('<p style="text-align: center; color: #555;">منصة إدارة المشاريع الهندسية - تصميم وتنفيذ أنطونيوس © 2026</p>', unsafe_allow_html=True)
