import streamlit as st
import requests

st.set_page_config(page_title="Professor Page", page_icon="📚")
st.title("Professor Upload Page")

# delete side nav bar created by streamlit
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("logged_in") or st.session_state.get("role") != "Professor":
    st.error("Access denied. Please log in as a Professor.")
    st.stop()

API_BASE = "http://localhost:8000/api/auth"

st.subheader("Upload Course Materials")

uploaded_files = st.file_uploader(
    "Upload your lecture slides or assignments (PDF, DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

course_name = st.text_input("Course Name (optional)", placeholder="e.g., CS 225")

if st.button("Upload Files") and uploaded_files:
    for file in uploaded_files:
        files = {"file": (file.name, file, file.type)}
        data = {"course_name": course_name} if course_name else {}
        
        try:
            response = requests.post(f"{API_BASE}/upload/", files=files, data=data)
            
            if response.status_code == 200:
                st.success(f"✅ Uploaded: {file.name}")
            else:
                st.error(f"❌ Failed: {response.json().get('error')}")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif uploaded_files:
    st.info("👆 Click 'Upload Files'")
else:
    st.warning("No files selected.")

st.subheader("Your Uploaded Files")

try:
    response = requests.get(f"{API_BASE}/files/")
    
    if response.status_code == 200:
        files = response.json().get("files", [])
        
        if files:
            for file in files:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📄 {file['filename']}")
                with col2:
                    st.write(f"{file['file_type']}")
                with col3:
                    if st.button("Delete", key=f"del_{file['id']}"):
                        requests.delete(f"{API_BASE}/files/{file['id']}/delete/")
                        st.rerun()
        else:
            st.info("No files.")
except:
    pass

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("app.py")
