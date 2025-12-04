import streamlit as st
import requests

st.set_page_config(page_title="Student Page", page_icon="📖")

# css to change only the text color in input boxes
st.markdown("""
<style>
input, textarea {
    color: #EFEFEF !important;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Study Assistant")

if not st.session_state.get("logged_in") or st.session_state.get("role") != "Student":
    st.error("Access denied. Please log in as a Student.")
    st.stop()

API_BASE = "http://localhost:8000/api/auth"

# Get available files
try:
    response = requests.get(f"{API_BASE}/files/")
    files = response.json().get("files", []) if response.status_code == 200 else []
except:
    files = []

# File selector
if files:
    file_options = {f['id']: f['filename'] for f in files}
    selected_file = st.selectbox(
        "Select course material", 
        options=[None] + list(file_options.keys()), 
        format_func=lambda x: "All materials" if x is None else file_options.get(x, "")
    )
else:
    selected_file = None
    st.info("No course materials uploaded yet.")

# Clear chat button
col1, col2 = st.columns([4, 1])
with col2:
    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat interface
st.subheader("Ask Questions")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question about the course material..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build chat history for context
                chat_history = [{"role": msg["role"], "content": msg["content"]} 
                                for msg in st.session_state.messages[-10:]]  # Last 10 messages
                
                data = {
                    "question": prompt,
                    "chat_history": chat_history
                }
                if selected_file:
                    data["file_id"] = selected_file
                
                response = requests.post(f"{API_BASE}/chat/", json=data)
                
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("Failed to get response")
            except Exception as e:
                st.error(f"Error: {str(e)}")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("app.py")