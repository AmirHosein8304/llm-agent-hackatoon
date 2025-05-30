import os
from docx import Document
import PyPDF2
import sqlite3

def initialize_db(name):
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO contracts (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def read_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def read_pdf(path):
    text = ""
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def read_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])


def file_exists_in_db(name):
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM contracts WHERE name = ?", (name,))
    except:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
        cursor.execute("SELECT 1 FROM contracts WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def file_reader(path):
    if not os.path.exists(path):
        print("File not found!")
        return None

    ext = os.path.splitext(path)[1].lower()
    name = os.path.basename(os.path.splitext(path)[0]).lower()

    if not file_exists_in_db(name):
        initialize_db(name)

    if ext == '.txt':
        return read_txt(path)
    elif ext == '.pdf':
        return read_pdf(path)
    elif ext == '.docx':
        return read_docx(path)
    else:
        print(f"Unsupported file extension: {ext}")
        return None


if __name__ == "__main__":
    path = "contract1.pdf"  # Make sure this is in the same directory or provide full path
    try:
        content = file_reader(path)
        if content:
            print("File content preview:\n", content[:1000])
        else:
            print("No content extracted.")
    except Exception as e:
        print("Error:", e)
