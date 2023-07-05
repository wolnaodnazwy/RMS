import argparse
from connection import get_database_connection

def clear_table(conn, table_name):
    cursor = conn.cursor()

    # Usuwanie wszystkich danych z tabeli
    cursor.execute(f'DELETE FROM {table_name};')

    conn.commit()
    cursor.close()

def clear_all_tables(conn):
    cursor = conn.cursor()

    # Pobieranie nazw wszystkich tabel
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cursor.fetchall()

    # Usuwanie wszystkich danych z każdej tabeli
    for table in tables:
        cursor.execute(f'DELETE FROM {table[0]};')

    conn.commit()
    cursor.close()

def clear_database(conn):
    cursor = conn.cursor()

    # Pobieranie nazw wszystkich tabel
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    tables = cursor.fetchall()

    # Usuwanie wszystkich tabel
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS {table[0]} CASCADE;')

    conn.commit()
    cursor.close()

def clear():
    # Uzyskanie połączenia do bazy danych
    conn = get_database_connection()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--table', help='Usuń zawartość tabeli')
    parser.add_argument('--all', action='store_true', help='Usuń dane ze wszystkich tabeli')
    parser.add_argument('--drop', action='store_true', help='Usuń wszystkie tabele (całkowicie)')
    args = parser.parse_args()

    if args.table:
        clear_table(conn, args.table)
    elif args.all:
        clear_all_tables(conn) 
    elif args.drop:
        clear_database(conn)
    else:
        print('Nie podano żadnej opcji. Użyj --table [nazwa_tabeli], --all lub --drop.')

    conn.close()

if __name__ == '__main__':
    clear()