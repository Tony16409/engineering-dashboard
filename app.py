[25/08/2026 04:17 ص] Eng.ToNy 👷‍♂️♥: import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="منصة إدارة المشاريع الهندسية", page_icon="🏗️", layout="wide")

# --- كود CSS لتصميم الخلفية الهندسية وتوسيط واجهة الدخول ---
login_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1920&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
/* توسيط الكارد الأبيض */
.login-card {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 40px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    max-width: 400px;
    margin: auto;
    margin-top: 10vh; /* ينزله شوية عن التايتل */
}
/* توسيط التايتل داخل الكارد */
.login-title {
    text-align: center;
    color: #333;
    margin-bottom: 25px;
}
</style>
"""

# --- دالة التحقق من كلمة المرور ---
def check_password():
    """يُرجع True إذا تم إدخال كلمة المرور الصحيحة."""

    # إنشاء حاوية (Container) لتوسيط العناصر في الشريط الجانبي
    with st.sidebar:
        st.markdown(login_css, unsafe_allow_html=True) # تحميل الـ CSS الخاص بالخلفية

        # --- واجهة تسجيل الدخول في نص الشاشة ---
        # نستخدم st.empty() عشان لما ندخل، المحتوى ده يختفي ويظهر محتوى المنصة
        login_container = st.empty()
        
        with login_container.container():
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown('<h1 class="login-title">🏗️ تسجيل الدخول</h1>', unsafe_allow_html=True)
            
            username_input = st.text_input("👤 اسم المستخدم", key="login_user")
            password_input = st.text_input("🔑 كلمة المرور", type="password", key="login_pass")
            
            # مسافة صغيرة
            st.write("")
            
            # زرار "الدخول"
            login_button = st.button("🚪 الدخول", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if login_button:
                if username_input == "admin" and password_input == "1234":
                    st.session_state["password_correct"] = True
                    login_container.empty() # إخفاء واجهة الدخول
                    st.rerun() # إعادة تحميل الصفحة لإظهار محتوى المنصة
                else:
                    st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة.")
                    st.session_state["password_correct"] = False
            
            # منع الوصول لباقي الكود إذا لم يتم تسجيل الدخول
            if "password_correct" not in st.session_state or not st.session_state["password_correct"]:
                st.stop()

# تشغيل دالة التحقق من كلمة المرور
check_password()


# =================================================================
# --- محتوى المنصة (يظهر فقط بعد تسجيل الدخول الناجح) ---
# =================================================================

# --- ترويسة اللوحة ---
st.markdown('<h1 style="text-align: center; color: #333;">📂 لوحة تحكم إدارة الملفات والمشاريع الهندسية 📂</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align: center; color: #666;">أهلاً بك يا باشمهندس أنطونيوس | التاريخ: {datetime.now().strftime("%Y-%m-%d")}</p>', unsafe_allow_html=True)
st.markdown("---")

# --- قسم رفع الملفات ---
st.subheader("📤 رفع مستند أو مخطط جديد")
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("اختر ملف (Excel, PDF, CAD، أو مستند نصي)", type=["xlsx", "pdf", "txt", "csv", "dwg", "dxf", "jpg", "png"])

with col2:
    note = st.text_input("📝 ملاحظات على الملف (اختياري)")

# زر حفظ الملف
if st.button("💾 حفظ ورفع الملف", type="primary"):
    if uploaded_file is not None:
        st.success(f"✅ تم رفع الملف بنجاح: {uploaded_file.name}")
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")

# --- سجل الملفات والمقاييس المرفوعة ---
st.subheader("📋 سجل الملفات والمقاييس المرفوعة")
[25/08/2026 04:17 ص] Eng.ToNy 👷‍♂️♥: # بيانات وهمية مؤقتة
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
st.markdown('<p style="text-align: center; color: #888;">منصة إدارة المشاريع الهندسية - تصميم وتنفيذ أنطونيوس © 2024</p>', unsafe_allow_html=True)
