# AI Classwork Chatbot

## Project Overview

ClassGPT is a Python-based, full-stack web application designed to help students and professors interact with class materials more effectively and with more integrity with an AI powered academic chatbot. The platform allows professors to upload course materials such as lecture slides, study guides, practice quizzes, etc. and students can then use the chatbot interface to ask questions and recieve contextual answers that are derived from the material provided by the professor. 

ClassGPT enhances learning by allowing students to clarify concepts at anytime while maintaining academic integrity through instructor oversight. Unlike general chatbots, ClassGPT ensures that all information is course-specific (ex. all formulas/content are taught the way the professor teaches in class), approved by the professor, and securely managed.

---

## Technical Architecture

The system is organized into three main layers:

### 1. Frontend (Streamlit)

* Built using **Streamlit** in Python
* Provides the user interface for:

  * Login and authentication
  * Role-based navigation (student vs. professor)
  * Chat interaction with the AI
* Uses the `requests` library to communicate with the backend via HTTP and JSON

### 2. Backend (Django)

* Built using **Django**
* Handles:

  * User authentication and authorization
  * API routing and request handling
  * Chat logic and communication with the AI layer
* Exposes REST-style endpoints (e.g., `/api/auth/login/`)
* Acts as the central controller between the frontend and the AI model

### 3. AI Layer (Ollama)

* Uses **Ollama** to run a local large language model (e.g., Mistral or LLaMA)
* Receives prompts from the Django backend
* Generates AI responses and returns them to the backend
* Enables local, private, and cost-free AI inference

### Architecture Flow

1. User interacts with the Streamlit frontend
2. Streamlit sends requests to the Django backend
3. Django authenticates the user and processes the request
4. Django forwards prompts to Ollama
5. Ollama generates a response
6. The response is returned through Django to Streamlit and displayed to the user

---

## Installation & Reproducibility Instructions

### Prerequisites

* Python 3.10 or higher
* pip
* Git
* Ollama installed locally

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd classwork_chatbot
```

### Step 2: Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Ollama

Install Ollama from [https://ollama.com](https://ollama.com) and pull a model:

```bash
ollama pull mistral
ollama run mistral
```

Ensure Ollama is running in the background.

### Step 5: Run the Django Backend

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

The backend will run at `http://127.0.0.1:8000`.

### Step 6: Run the Streamlit Frontend

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

The Streamlit app will open in your browser.

---

## Group Members and Roles

* **Julia** – Backend Team - Integrated the Ollama chatbot and implemented course material parsing
* **Stephanie** – Backend Team - Built test users, created test cases, and Django API setup
* **Jenna** – Frontend Team - Created the login page frontend and implemented UI improvements
* **Samika** – Frontend Team - Developed the Streamlit interface and implemented UI improvements
* **Entire Team** - All members contributed to testing, debugging, and integration between the frontend and backend

---

## Notes / Future Work

* This project is designed to run locally for development and demonstration purposes.
* The modular architecture allows easy extension, such as adding logging, chat history, or new AI models.
* We plan for future enhancements which include: 
1. Professor dashboard with analytics to track student engagement and common question areas
2. OAuth for Student/Professor login
3. Document summarization for uploaded materials
4. Fine tune chatbot to allow professor to omit certain things from answers 
