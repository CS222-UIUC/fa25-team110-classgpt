import PyPDF2
from docx import Document

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        return f"Error: {str(e)}"

def get_file_type(filename):
    ext = filename.lower().split('.')[-1]
    return 'pdf' if ext == 'pdf' else 'docx' if ext in ['docx', 'doc'] else None

def extract_text(file_path, file_type):
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type == 'docx':
        return extract_text_from_docx(file_path)
    return "Unsupported file type"