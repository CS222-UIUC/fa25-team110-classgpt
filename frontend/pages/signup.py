import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sign Up", page_icon="📝")

st.markdown("""
<style>
input, textarea {
    color: #EFEFEF !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("Create Account")

if "api_session" not in st.session_state:
    st.session_state.api_session = requests.Session()

# select role
user_type = st.selectbox(
    "I am a:",
    ["student", "professor"],
    format_func=lambda x: x.capitalize()
)

# inputs
username = st.text_input("Username*")
email = st.text_input("Email*")
password = st.text_input("Password* (min 8 characters)", type="password")
password_confirm = st.text_input("Confirm Password*", type="password")

# button
if st.button("Sign Up"):
    if not all([username, email, password, password_confirm]):
        st.error("Please fill in all required fields")
    elif password != password_confirm:
        st.error("Passwords do not match")
    elif len(password) < 8:
        st.error("Password must be at least 8 characters long")
    else:
        data = {
            "username": username,
            "email": email,
            "password": password,
            "user_type": user_type,
        }
        
        # api request
        try:
            response = st.session_state.api_session.post(
                f"{API_BASE}/api/auth/register/",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                st.success(f"Account created successfully! Welcome, {username}!")
                
                # store login info
                st.session_state.logged_in = True
                st.session_state.role = user_type.capitalize()
                st.session_state.username = username
                
                if user_type == "professor":
                    st.switch_page("pages/professor.py")
                else:
                    st.switch_page("pages/student.py")
            else:
                st.error(f"Registration failed (Status: {response.status_code})")
                st.code(response.text[:1000])  

                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", "Unknown error")
                    st.error(f"Error details: {error_msg}")
                except:
                    pass
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Please ensure Django server is running on port 8000.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# go to login
st.markdown("---")
st.write("Already have an account?")
if st.button("Go to Login", use_container_width=True):
    st.switch_page("app.py")