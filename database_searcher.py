import sqlite3

def data_base_searcher() -> list[str]:
    """
    Returns a list of all file paths stored in the contracts database.
    """
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM contracts")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results
