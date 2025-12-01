import streamlit as st
import requests

st.set_page_config(page_title="Student Page", page_icon="💬")

# css to change only the text color in input boxes
st.markdown("""
<style>
input, textarea {
    color: #EFEFEF !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Student Chatbot Page")

if not st.session_state.get("logged_in") or st.session_state.get("role") != "Student":
    st.error("Access denied. Please log in as a Student.")
    st.stop()

user_question = st.text_input("Ask the chatbot a question:")

if st.button("Ask"):
    if user_question:
        st.write(f"🤖 Bot: Great question about '{user_question}'! (Backend coming soon)")
    else:
        st.warning("Please enter a question first.")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.switch_page("app.py")