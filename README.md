# AI Classwork Chatbot

## Project Overview

The AI Classwork Chatbot is a Python-based, full-stack web application designed to assist students and professors with class-related questions through an interactive AI-powered chat interface. The system supports user authentication, role-based access, and AI-generated responses, all while running locally for privacy and ease of development.

This project combines a lightweight frontend, a robust backend, and a locally hosted large language model to create a modular and extensible educational tool.

---

## Presentation Summary / Introduction

Our project demonstrates how modern AI tools can be integrated into a traditional web architecture to enhance learning experiences. We built a chatbot that allows authenticated students and professors to interact with an AI model in a controlled academic setting. By separating the frontend, backend, and AI layers, we ensure clarity of design, security, and maintainability.

The chatbot is powered by a locally hosted large language model using Ollama, which avoids reliance on cloud APIs and provides greater control over data and behavior. This architecture reflects real-world software engineering practices and highlights how AI systems can be responsibly integrated into educational applications.

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

* **Julia** – Backend development, Chatbot logic, Ollama integration
* **Stephanie** – System testing, Backend development, Django API setup
* **Jenna** – Frontend development, login and authentication system
* **Samika** – Backend/Frontend development, system integration

---

## Notes

* This project is designed to run locally for development and demonstration purposes.
* The modular architecture allows easy extension, such as adding logging, chat history, or new AI models.
