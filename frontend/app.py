import streamlit as st
import requests

# backend API
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Classwork Chatbot", page_icon="🤖")

# css to change only the text color in input boxes
st.markdown("""
<style>
input, textarea {
    color: #EFEFEF !important;
}
</style>
""", unsafe_allow_html=True)

# delete side nav bar created by streamlit
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Classwork Chatbot")

# session states - check if logged in
if "api_session" not in st.session_state:
    st.session_state.api_session = requests.Session()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

#not logged in
if not st.session_state.logged_in:
    st.write("Welcome! Please log in to continue.")
    # login inputs
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    # login button logic
    with col1:
        if st.button("Login", type="primary", use_container_width=True):
            if username and password:
                try:
                    response = requests.post(
                        f"{API_BASE}/api/auth/login/",
                        json={"username": username, "password": password},
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.role = data["user_type"].capitalize()
                        st.success(f"Welcome, {data['username']}! Redirecting to your {data['user_type']} page...")

                        # redirect to right page
                        if data["user_type"].lower() == "professor":
                            st.switch_page("pages/professor.py")
                        elif data["user_type"].lower() == "student":
                            st.switch_page("pages/student.py")
                        else:
                            st.warning("Unknown role")
                    else:
                        st.error("Invalid username or password.")
                except requests.exceptions.ConnectionError:
                    st.error("Backend not running. Start Django first.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Enter both username and password.")
    with col2:
        if st.button("Sign Up", use_container_width=True):
            st.switch_page("pages/signup.py")

else:
    st.success(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Go to Dashboard"):
            if st.session_state.role.lower() == "professor":
                st.switch_page("pages/professor.py")
            else:
                st.switch_page("pages/student.py")
    
    with col2:
        if st.button("Logout"):
            # logout
            try:
                st.session_state.api_session.post(f"{API_BASE}/logout/", timeout=5)
            except:
                pass
            
            # clear session
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.username = None
            st.session_state.api_session = requests.Session()
            st.rerun()
