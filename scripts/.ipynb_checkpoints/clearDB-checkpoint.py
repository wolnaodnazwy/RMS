import sqlite3

def clear_database():
    conn = sqlite3.connect('results/rms.db')
    cursor = conn.cursor()

    # Usuwanie wszystkich danych z tabeli 'dane'
    cursor.execute('DELETE FROM dane;')

    # Usuwanie wszystkich danych z tabeli 'service'
    cursor.execute('DELETE FROM service;')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    clear_database()