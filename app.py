mport os
from datetime import datetime
import pandas as pd
import streamlit as st

# إعدادات صفحة المنصة
st.set_page_config(
    page_title="Al-Farida Company Management", page_icon="🏗️", layout="wide"
)

# إنشاء مجلد حفظ الملفات إذا لم يكن موجوداً
UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
  os.makedirs(UPLOAD_DIR)

# ملف قاعدة البيانات الوهمية (CSV) لتخزين سجل الملفات
DB_FILE = "files_db.csv"
if not os.path.exists(DB_FILE):
  df_init = pd.DataFrame(
      columns=["name", "type", "size", "note", "date", "path"]
  )
  df_init.to_csv(DB_FILE, index=False)

# تهيئة متغير الـ uploader key لتصفير خانة الرفع أوتوماتيكياً
if "uploader_key" not in st.session_state:
  st.session_state["uploader_key"] = 0

# حالة تسجيل الدخول
if "authenticated" not in st.session_state:
  st.session_state["authenticated"] = False

# ------------------------- واجهة تسجيل الدخول -------------------------
if not st.session_state["authenticated"]:
  # تصميم الـ CSS لصفحة الدخول
  st.markdown(
      """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        .login-box {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            padding: 30px 25px;
            border-radius: 18px;
            max-width: 450px;
            margin: 80px auto;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        </style>
    """,
      unsafe_allow_html=True,
  )

  st.markdown("<div class='login-box'>", unsafe_allow_html=True)

  with st.form("login_form"):
    st.markdown(
        "<h2 style='text-align: center; color: white;'>🏗️ Welcome Back</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #94a3b8;'>Engineering"
        " Projects Management Platform</p>",
        unsafe_allow_html=True,
    )

    username = st.text_input("👤 Username", key="login_user")
    password = st.text_input("🔑 Password", type="password", key="login_pass")

    st.write("")
    submit_button = st.form_submit_button(
        "🚪 Login to Platform", use_container_width=True
    )

    if submit_button:
      if username == "admin" and password == "1234":
        st.session_state["authenticated"] = True
        st.rerun()
      else:
        st.error("❌ Invalid Username or Password.")

  st.markdown("</div>", unsafe_allow_html=True)

else:
  # ------------------------- لوحة التحكم الرئيسية للمنصة -------------------------
  st.markdown(
      """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        .brand-box {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            padding: 22px 20px;
            border-radius: 18px;
            max-width: 550px;
            margin: 25px auto 15px auto;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        .brand-text {
            color: #ffffff;
            font-size: 38px !important;
            font-weight: 900;
            letter-spacing: 1px;
            margin: 0;
            line-height: 1.1;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-shadow: 0 3px 15px rgba(255, 255, 255, 0.3);
        }
        </style>
    """,
      unsafe_allow_html=True,
  )

  # الهيدر الاحترافي للشركة
  st.markdown(
      """
        <div class="brand-box">
            <h1 class="brand-text">📂 Welcome to our company Al-Farida 📁</h1>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # زر تسجيل الخروج في الجانب
  col_logout1, col_logout2 = st.columns([8, 1])
  with col_logout2:
    if st.button("🚪 Logout"):
      st.session_state["authenticated"] = False
      st.rerun()

  st.write("---")

  # قسم رفع الملفات
  st.markdown(
      "### 📤 Upload New File (Excel, Word, PDF, CAD, Images)"
  )

  col1, col2 = st.columns([2, 1])
  with col1:
    # استخدام الـ dynamic key لتصفير الخانة أوتوماتيكياً بعد الحفظ
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=[
            "xlsx",
            "docx",
            "pdf",
            "txt",
            "csv",
            "dwg",
            "dxf",
            "jpg",
            "png",
        ],
        key=f"file_uploader_{st.session_state['uploader_key']}",
        label_visibility="collapsed",
    )

  with col2:
    note = st.text_input("📝 Notes on file (Optional)", key="file_note")

  st.write("")
  if st.button("📤 Upload File & Save", type="primary"):
    if uploaded_file is not None:
      # حفظ الملف في المجلد
      file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
      with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

      # حساب حجم الملف وتنسيقه
      file_size_kb = uploaded_file.size / 1024
      file_size_str = (
          f"{file_size_kb / 1024:.1f} MB"
          if file_size_kb > 1024
          else f"{file_size_kb:.1f} KB"
      )
      file_ext = uploaded_file.name.split(".")[-1].upper()

      # قراءة قاعدة البيانات وتحديثها
      df = pd.read_csv(DB_FILE)
      new_row = pd.DataFrame([{
          "name": uploaded_file.name,
          "type": file_ext,
          "size": file_size_str,
          "note": note if note else "No notes",
          "date": datetime.now().strftime("%Y-%m-%d"),
          "path": file_path,
      }])

      df = pd.concat([new_row, df], ignore_index=True)
      df.to_csv(DB_FILE, index=False)

      # تصفير خانة الرفع أوتوماتيكياً دون الحاجة لضغط علامة الـ X أو إعادة تحميل ظاهرة
      st.session_state["uploader_key"] += 1
      st.success("✅ File uploaded and saved successfully!")
      st.rerun()
    else:
      st.warning("⚠️ Please select a file to upload first.")

  st.write("---")

  # ------------------------- جدول عرض الملفات المحفوظة -------------------------
  st.markdown("### 🗂️ Uploaded Files & Quantities Record")

  df_records = pd.read_csv(DB_FILE)

  if df_records.empty:
    st.info("ℹ️ No files uploaded yet.")
  else:
    # رأس جدول الأعمدة بالإنجليزية
    header_cols = st.columns([0.5, 3, 1, 1, 2.5, 1, 1, 1])
    headers = ["#", "File Name", "Type", "Size", "Notes", "Open", "Download", "Delete"]
    for col, h in zip(header_cols, headers):
      col.markdown(f"*{h}*")

    st.markdown("---")

    # عرض الصفوف ديناميكياً مع أدوات التحكم
    for idx, row in df_records.iterrows():
      r_cols = st.columns([0.5, 3, 1, 1, 2.5, 1, 1, 1])

      r_cols[0].write(f"{idx + 1}")
      r_cols[1].write(f"{row['name']}")
      r_cols[2].write(f"{row['type']}")
      r_cols[3].write(f"{row['size']}")
      r_cols[4].write(f"{row['note']}")

      # زرار فتح الملف
      if os.path.exists(row["path"]):
        with open(row["path"], "rb") as file_data:
          r_cols[5].download_button(
              "🌐 Open",
              data=file_data,
              file_name=row["name"],
              mime="application/octet-stream",
              key=f"open_{idx}",
          )
      else:
        r_cols[5].write("Missing")

      # زرار تحميل الملف
      if os.path.exists(row["path"]):
        with open(row["path"], "rb") as file_data:
          r_cols[6].download_button(
              "📥 Download",
              data=file_data,
              file_name=row["name"],
              mime="application/octet-stream",
              key=f"download_{idx}",
          )
      else:
        r_cols[6].write("Missing")

      # زرار حذف الملف من الجدول والمجلد
      if r_cols[7].button("🗑️ Delete", key=f"del_{idx}"):
        if os.path.exists(row["path"]):
          try:
            os.remove(row["path"])
          except:
            pass
        df_records = df_records.drop(idx)
        df_records.to_csv(DB_FILE, index=False)
        st.rerun()

  # الفوتر الهندسي للمنصة
  st.markdown("---")
  st.markdown(
      "<p style='text-align: center; color: #64748b; font-size: 14px;'>Engineering"
      " Projects Management Platform - Designed & Developed by Antonious"
      f" Adel © {datetime.now().year}</p>",
      unsafe_allow_html=True,
  )
