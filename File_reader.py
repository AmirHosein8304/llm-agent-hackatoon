import os
from typing import Optional
from docx import Document
import PyPDF2


def read_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def read_pdf(file_path: str) -> str:
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def read_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def file_reader(file_path: str) -> Optional[str]:
    """
    Universal file reader that extracts text from .txt, .pdf, or .docx files.
    """
    if not os.path.exists(file_path):
        print("File not found!")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.txt':
        return read_txt(file_path)
    elif ext == '.pdf':
        return read_pdf(file_path)
    elif ext == '.docx':
        return read_docx(file_path)
    else:
        print(f"Unsupported file extension: {ext}")

if __name__ == "__main__":
    path = "IDA_Star.pdf" 
    try:
        content = file_reader(path)
        print("File content preview:\n", content[:1000])  
    except Exception as e:
        print("Error:", e)
