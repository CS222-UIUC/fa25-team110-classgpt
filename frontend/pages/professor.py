import streamlit as st

st.set_page_config(page_title="Professor Page", page_icon="📚")

#change colors of file uploader
st.markdown("""
<style>
[data-testid="stFileUploader"] > div {
  background: var(--secondary-background-color) !important;
  border: 1px dashed var(--primary-color) !important;
  border-radius: 14px;
  padding: 1rem;
}
[data-testid="stFileUploader"] label {
  color: var(--text-color) !important;
  font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("Professor Upload Page")

if not st.session_state.get("logged_in") or st.session_state.get("role") != "Professor":
    st.error("Access denied. Please log in as a Professor.")
    st.stop()

uploaded_files = st.file_uploader(
    "Upload your lecture slides or assignments (PDF, PPTX, DOCX)",
    type=["pdf", "pptx", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        st.success(f"Uploaded: {file.name}")
else:
    st.warning("No files uploaded yet.")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("app.py")