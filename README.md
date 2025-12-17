ClassGPT : AI Study Assistant 

(a) Project Summary & Introduction
ClassGPT is an AI powered academic chatbot designed to help students and professors interact with class materials more effectively and with more integrity. The platform allows professors to upload course materials such as lecture slides, study guides, practice quizzes, etc. and students can then use the chatbot interface to ask questions and recieve contextual answers that are derived from the material provided by the professor. 

ClassGPT enhances learning by allowing students to clarify concepts at anytime while maintaining academic integrity through instructor oversight. Unlike general chatbots, ClassGPT ensures that all information is course-specific (ex. all formulas/content are taught the way the professor teaches in class), approved by the professor, and securely managed. 

(b) Technical Architecture
The system follows a 2 part architecture using a Django API Backend and a Streamlit Frontend. 
Frontend (Streamlit)
- Handles user login and role-based access
- Provides chat interface for students
- Communicates with backend via REST API calls

Backend (Django + Django REST Framework)
- Authentication and user roles (Student / Professor)
- APIs for login, registration, and AI chat
- Database storing users, uploaded course files, and chat history
- Role-based access ensuring professors manage and control materials

(c) Installation Instructions 
1. Clone the Repository 

2. Create and activate the Virtual Environment 
python3 -m venv venv
source venv/bin/activate #Mac/Linux
venv\Scripts\activate #Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Backend
python manage.py migrate
python manage.py runserver

5. Run the Frontend
In a new terminal window: 
cd frontend
streamlit run app.py

(d) Group Members & Roles 

Samika Karumuri: Frontend Team - Developed the Streamlit interface and implemented UI improvements
Jenna Rentz: Frontend Team - Created the login page frontend and implemented UI improvements
Julia Szendela: Backend Team - Integrated the Ollama chatbot and implemented course material parsing
Stephanie Kirova: Backend Team - Built test users, created test cases, and supported integration
Entire Team: All members contributed to testing, debugging, and integration between the frontend and backend

(e) Future Work
We plan for future enhancements which include: 
- Professor dashboard with analytics to track student engagement and common question areas
- OAuth for Student/Professor login
- Document summarization for uploaded materials
- Fine tune chatbot to allow professor to omit certain things from answers 

