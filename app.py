import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# إعدادات الصفحة
st.set_page_config(page_title="منصة إدارة المشاريع الهندسية", layout="wide")

st.title("🏗️ منصة إدارة المشاريع الهندسية")
st.markdown("---")

# تهيئة الذاكرة المؤقتة للملفات
if "files_list" not in st.session_state:
    st.session_state["files_list"] = []

# --- قسم رفع الملفات ---
st.subheader("📁 رفع ملف جديد أو مقايسة")
uploaded_file = st.file_uploader("اختر ملف (PDF, صور, أو مستندات)", type=["pdf", "png", "jpg", "jpeg", "txt", "csv", "xlsx"])
note_input = st.text_input("ملاحظات على الملف:", placeholder="اكتب ملاحظة أو وصف للملف هنا...")

if st.button("💾 حفظ الملف وإضافته للسجل"):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_size_kb = len(file_bytes) / 1024
        size_str = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.2f} MB"
        
        file_info = {
            "name": uploaded_file.name,
            "type": uploaded_file.type.split('/')[-1].upper() if '/' in uploaded_file.type else uploaded_file.type,
            "size": size_str,
            "note": note_input if note_input else "بدون ملاحظات",
            "data": file_bytes
        }
        st.session_state["files_list"].append(file_info)
        st.success(f"✅ تم رفع الملف بنجاح: {uploaded_file.name}")
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")

# --- سجل الملفات والمقاييس ---
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
    header_cols[5].markdown("👁️ فتح بالمنصة")
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
        
        with row_cols[5]:
            if st.button("👁️ فتح بالمنصة", key=f"view_btn_{idx}"):
                st.session_state["active_view"] = idx
                
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
        
        if file_ext == 'pdf':
            base64_pdf = base64.b64encode(selected_file["data"]).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        elif file_ext in ['png', 'jpg', 'jpeg']:
            st.image(selected_file["data"], caption=selected_file['name'], use_column_width=True)
            elif file_ext in ['txt', 'csv']:
            text_content = selected_file["data"].decode('utf-8')
            st.text_area("محتوى الملف:", text_content, height=300)
        else:
            st.info(f"📁 نوع الملف ({file_ext}) جاهز للتحميل المباشر.")
            
        if st.button("❌ إغلاق المعاينة"):
            del st.session_state["active_view"]
            st.rerun()

st.markdown('<p style="text-align: center; color: #777;">منصة إدارة المشاريع الهندسية - تصميم وتنفيذ أنطونيوس © 2026</p>', unsafe_allow_html=True)
