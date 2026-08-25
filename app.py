import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="منصة إدارة المشاريع الهندسية", page_icon="🏗️", layout="wide")

# شاشة تسجيل الدخول البسيطة
st.sidebar.title("🔐 تسجيل الدخول")
username = st.sidebar.text_input("اسم المستخدم")
password = st.sidebar.text_input("كلمة المرور", type="password")

if username == "admin" and password == "1234":
    st.sidebar.success("تم تسجيل الدخول بنجاح!")
    
    st.title("🏗️ لوحة تحكم إدارة الملفات والمشاريع الهندسية")
    st.write(f"أهلاً بك يا باشمهندس أنطونيوس | التاريخ: {datetime.now().strftime('%Y-%m-%d')}")
    
    # قسم رفع الملفات
    st.markdown("---")
    st.subheader("📁 رفع مستند أو مخطط جديد")
    uploaded_file = st.file_uploader("اختر ملف (Excel, PDF, CAD, أو مستند نصي)", type=["xlsx", "pdf", "txt", "csv"])
    note = st.text_input("ملاحظات على الملف")
    
    if st.button("حفظ ورفع الملف"):
        if uploaded_file is not None:
            st.success(f"تم رفع الملف '{uploaded_file.name}' بنجاح وتوثيق الملاحظات!")
        else:
            st.warning("الرجاء اختيار ملف أولاً قبل الرفع.")
            
    # جدول عرض الملفات
    st.markdown("---")
    st.subheader("📊 سجل الملفات والمقايسات المرفوعة")
    
    data = {
        "اسم الملف": ["مقايسة خرسانات العاصمة.xlsx", "مخطط محطة الرفع الرئيسية.pdf", "حصر أطوال الحديد.xlsx"],
        "تاريخ الرفع": ["2026-08-24", "2026-08-25", "2026-08-25"],
        "الحالة": ["مراجعة نهائية", "قيد الدراسة", "معتمد"],
        "الملاحظات": ["تم مطابقة الكميات", "يحتاج تنسيق مع الاستشاري", "مطابق للمواصفات"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

else:
    st.title("🏗️ منصة إدارة المشاريع الهندسية الخاصة")
    st.info("الرجاء إدخال اسم المستخدم وكلمة المرور من القائمة الجانبية للدخول.")
    st.text("بيانات التجربة:\nاسم المستخدم: admin\nكلمة المرور: 1234")