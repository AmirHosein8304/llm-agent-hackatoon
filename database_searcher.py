import sqlite3

def data_base_searcher():
    conn = sqlite3.connect('contracts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM contracts")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

if __name__ == "__main__":
    results = data_base_searcher()
    print(results)