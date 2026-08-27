import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Al-Farida Company Management 📐", page_icon="🏗️", layout="wide")

# --- إعداد الاتصال بجوجل شيت وجوجل درايف أوتوماتيكياً ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1kG0V8iqNv4nCVDSYA-nRL_K5UCYpTbLGa5vh4Ip8ug0/edit?usp=sharing"

@st.cache_resource
def get_gcp_clients():
    try:
        if "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
            
            # عميل جوجل شيت
            gc = gspread.authorize(creds)
            sheet = gc.open_by_url(SHEET_URL).worksheet("Sheet1")
            
            # عميل جوجل درايف
            drive_service = build('drive', 'v3', credentials=creds)
            
            return sheet, drive_service
    except Exception as e:
        st.error(f"خطأ في الاتصال بخدمات جوجل: {e}")
        return None, None
    return None, None

def upload_to_drive(uploaded_file, drive_service):
    try:
        file_metadata = {'name': uploaded_file.name}
        media = MediaIoBaseUpload(
            io.BytesIO(uploaded_file.getbuffer()),
            mimetype=uploaded_file.type,
            resumable=True
        )
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink, webContentLink'
        ).execute()
        
        # منح صلاحية القراءة للجميع برابط مباشر
        file_id = file.get('id')
        drive_service.permissions().create(
            fileId=file_id,
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()
        
        return file.get('webViewLink'), file.get('webContentLink')
    except Exception as e:
        st.error(f"خطأ أثناء الرفع إلى جوجل درايف: {e}")
        return None, None

def load_data_from_sheet():
    sheet, _ = get_gcp_clients()
    if sheet:
        try:
            data = sheet.get_all_records()
            df = pd.DataFrame(data)
            if not df.empty:
                return df
        except Exception:
            pass
    return pd.DataFrame(columns=["name", "type", "size", "note", "date", "path"])

def save_row_to_sheet(row_dict):
    sheet, _ = get_gcp_clients()
    if sheet:
        try:
            sheet.append_row([
                row_dict["name"],
                row_dict["type"],
                row_dict["size"],
                row_dict["note"],
                row_dict["date"],
                row_dict["path"]
            ])
        except Exception as e:
            st.error(f"خطأ في حفظ البيانات في الشيت: {e}")

def delete_row_from_sheet(index_to_delete):
    sheet, _ = get_gcp_clients()
    if sheet:
        try:
            sheet.delete_rows(index_to_delete + 2)
        except Exception:
            pass

# --- كود CSS لتنسيق الواجهة وخلفية هندسية احترافية ---
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
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
.login-container {
    max-width: 550px;
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
        st.markdown('<div class="brand-box"><p class="brand-text">Al-Farida Group</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("<h2 style='text-align: center; color: white;'>🏗️ Log in to Al-Farida Group</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8;'>Al-Farida Company Management 📐</p>", unsafe_allow_html=True)
            
            username = st.text_input("👤 Username", key="login_user")
            password = st.text_input("🔑 password", type="password", key="login_pass")
            
            st.write("")
            submit_button = st.form_submit_button("🚪 Log in", use_container_width=True)
            
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

st.markdown('<h1 style="text-align: center; color: #333; background: #fff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">📂 Welcome to our company Al-Farida 📂</h1>', unsafe_allow_html=True)
st.markdown("---")

if st.sidebar.button("🔒 Log out"):
    st.session_state["authenticated"] = False
    st.rerun()

# --- قسم رفع الملفات ---
st.subheader("📤 Upload a new document or plan (Google Drive Synced)")
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Select the file (Excel, Word, PDF, CAD، أو مستند نصي)", type=["xlsx", "docx", "pdf", "txt", "csv", "dwg", "dxf", "jpg", "png"])

with col2:
    note = st.text_input("📝 Notes on the file", key="file_note")

if st.button("💾 Upload to Drive & Save", type="primary"):
    if uploaded_file is not None:
        with st.spinner("جاري رفع الملف إلى Google Drive وحفظ البيانات..."):
            _, drive_service = get_gcp_clients()
            if drive_service:
                view_link, download_link = upload_to_drive(uploaded_file, drive_service)
                
                if view_link:
                    file_size_kb = uploaded_file.size / 1024
                    file_size_str = f"{file_size_kb / 1024:.1f} MB" if file_size_kb > 1024 else f"{file_size_kb:.1f} KB"
                    file_ext = uploaded_file.name.split('.')[-1].upper()
                    
                    row_data = {
                        "name": uploaded_file.name,
                        "type": file_ext,
                        "size": file_size_str,
                        "note": note if note else "No notes",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "path": view_link # نحفظ رابط الدريف السحابي المباشر
                    }
                    
                    save_row_to_sheet(row_data)
                    st.success(f"✅ تم رفع الملف إلى جوجل درايف وحفظه بنجاح: {uploaded_file.name}")
                    st.rerun()
                else:
                    st.error("❌ فشل رفع الملف إلى جوجل درايف.")
            else:
                st.error("❌ تعذر الاتصال بخدمة Google Drive.")
    else:
        st.warning("⚠️ يرجى اختيار ملف أولاً.")

st.markdown("---")

# --- سجل الملفات والمقاييس ---
st.subheader("📋 Uploaded Files & Quantities Record (Google Drive & Sheets Synced)")

df_files = load_data_from_sheet()

if df_files.empty:
    st.info("ℹ️ لم يتم العثور على سجلات حتى الآن.")
else:
    header_cols = st.columns([0.4, 2.3, 0.8, 0.9, 1.8, 1.1, 1.1, 1.1])
    header_cols[0].markdown("No")
    header_cols[1].markdown("File Name")
    header_cols[2].markdown("Type")
    header_cols[3].markdown("Size")
    header_cols[4].markdown("Notes")
    header_cols[5].markdown("🌐 Open")
    header_cols[6].markdown("💾 Download")
    header_cols[7].markdown("🗑️ Delete")
    st.markdown("---")

    for idx, row in df_files.iterrows():
        row_cols = st.columns([0.4, 2.3, 0.8, 0.9, 1.8, 1.1, 1.1, 1.1])
        
        row_cols[0].markdown(f"{idx + 1}")
        row_cols[1].markdown(f"{row['name']}")
        row_cols[2].markdown(f"{row['type']}")
        row_cols[3].markdown(f"{row['size']}")
        row_cols[4].markdown(f"{row['note']}")
        
        link_val = str(row['path'])
        
        # زر Open السحابي
        with row_cols[5]:
            if link_val and link_val.startswith("http"):
                open_link = f'''
                <a href="{link_val}" target="_blank" style="
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
                ">Open</a>
                '''
                st.markdown(open_link, unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:gray;'>غير متاح</span>", unsafe_allow_html=True)

        # زر Download السحابي
        with row_cols[6]:
            if link_val and link_val.startswith("http"):
                # تحويل رابط التصفح لرابط تحميل مباشر من جوجل درايف
                download_url = link_val.replace("view?usp=drivesdk", "uc?export=download&id=").replace("file/d/", "uc?id=").split("/view")[0]
                if "uc?export=download" not in download_url and "id=" in link_val:
                    # استخراج الـ file_id لو الرابط بالشكل القياسي
                    try:
                        file_id = link_val.split('/d/')[1].split('/')[0]
                        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    except:
                        download_url = link_val
                
                dl_btn = f'''
                <a href="{download_url}" target="_blank" style="
                    display: inline-block;
                    background-color: #2563eb;
                    color: white;
                    padding: 5px 8px;
                    border-radius: 4px;
                    text-decoration: none;
                    text-align: center;
                    font-size: 13px;
                    font-weight: 500;
                    width: 100%;
                ">Download</a>
                '''
                st.markdown(dl_btn, unsafe_allow_html=True)
            else:
                st.write("-")

        # زر الحذف
        with row_cols[7]:
            if st.button("🗑️ Delete", key=f"delete_btn_{idx}", use_container_width=True):
                delete_row_from_sheet(idx)
                st.success("تم حذف السجل بنجاح!")
                st.rerun()
            
        st.markdown("---")

st.markdown('<p style="text-align: center; color: #777;">منصة إدارة شركة الفريدة - تصميم وتنفيذ مهندس أنطونيوس عادل © 2026</p>', unsafe_allow_html=True)
