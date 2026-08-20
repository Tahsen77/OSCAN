import streamlit as st
from supabase import create_client

# إعدادات الاتصال بـ Supabase
SUPABASE_URL = "https://cgzenucjljpwslwuttjz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNnemVudWNqbGpwd3Nsd3V0dGp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcxNjQ0NjEsImV4cCI6MjEwMjc0MDQ2MX0.cck74uVjeRnZE_u5upT2K4-5T4yHyfIAtfL0fYCOVyM"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

st.title("📦 OSCAN - Barcode Scanner")

# التقاط صورة من الكاميرا
img_buffer = st.camera_input("Take a photo / Scan product")

# إدخال الاسم
product_name = st.text_input("Product Name", placeholder="Enter product name...")

# حفظ البيانات
if st.button("Save to Supabase", type="primary"):
    if not product_name:
        st.warning("Please enter a product name!")
    else:
        try:
            data = {"barcode": "123456789", "name": product_name}
            supabase.table("products").insert(data).execute()
            st.success("Saved Successfully to Supabase!")
        except Exception as e:
            st.error(f"Error: {e}")
