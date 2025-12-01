import streamlit as st
import requests

st.set_page_config(page_title="Professor Page", page_icon="📚")
st.title("Professor Upload Page")

# Check authentication
if not st.session_state.get("logged_in") or st.session_state.get("role") != "Professor":
    st.error("Access denied. Please log in as a Professor.")
    st.stop()

# API base URL
API_BASE = "http://localhost:8000/api/auth"

st.subheader("Upload Course Materials")

# File uploader
uploaded_files = st.file_uploader(
    "Upload your lecture slides or assignments (PDF, DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# Course name input (optional)
course_name = st.text_input("Course Name (optional)", placeholder="e.g., CS 225")

# Upload button
if st.button("Upload Files") and uploaded_files:
    for file in uploaded_files:
        # Prepare the file for upload
        files = {"file": (file.name, file, file.type)}
        data = {"course_name": course_name} if course_name else {}
        
        try:
            # Send POST request to backend
            response = requests.post(
                f"{API_BASE}/upload/",
                files=files,
                data=data,
                # Add authentication if you have session tokens
                # headers={"Authorization": f"Bearer {st.session_state.get('token')}"}
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success(f"✅ Uploaded: {file.name}")
                st.json(result)
            else:
                st.error(f"❌ Failed to upload {file.name}: {response.json().get('error', 'Unknown error')}")
        
        except Exception as e:
            st.error(f"❌ Error uploading {file.name}: {str(e)}")

elif uploaded_files:
    st.info("👆 Click 'Upload Files' to send files to backend")
else:
    st.warning("No files selected yet.")

# Display uploaded files
st.subheader("Your Uploaded Files")

try:
    response = requests.get(f"{API_BASE}/files/")
    
    if response.status_code == 200:
        files_data = response.json()
        files = files_data.get("files", [])
        
        if files:
            for file in files:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📄 {file['filename']}")
                with col2:
                    st.write(f"Type: {file['file_type']}")
                with col3:
                    if st.button("Delete", key=f"del_{file['id']}"):
                        del_response = requests.delete(f"{API_BASE}/files/{file['id']}/delete/")
                        if del_response.status_code == 200:
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("No files uploaded yet.")
    else:
        st.error("Could not fetch files")
        
except Exception as e:
    st.error(f"Error loading files: {str(e)}")

# Logout button
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("app.py")