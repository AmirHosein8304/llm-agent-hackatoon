import os
from typing import Optional
from docx import Document
import PyPDF2
import sqlite3

def initialize_db(name,file_path):
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            file_path TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO contracts (name, file_path) VALUES (?, ?)", 
                   (name, file_path))
    conn.commit()
    conn.close()



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


def file_exists_in_db(name: str) -> bool:
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM contracts WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def file_reader(file_path: str) -> Optional[str]:
    """
    Universal file reader that extracts text from .txt, .pdf, or .docx files.
    Also checks if the file is already in the database, and inserts it if not.
    """
    if not os.path.exists(file_path):
        print("File not found!")
        return None

    ext = os.path.splitext(file_path)[1].lower()
    name = os.path.basename(os.path.splitext(file_path)[0]).lower()  # only filename without extension

    # Add to DB only if not already there
    if not file_exists_in_db(name):
        initialize_db(name, file_path)

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
