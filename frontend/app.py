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

# get rid of auto side nav bar created by streamlit
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Classwork Chatbot")
st.write("Welcome! Please log in to continue.")

# session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# login inputs
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# login button logic
if st.button("Login"):
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

# logout
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()
