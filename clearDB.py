import argparse
from connection import get_database_connection

def clear_table(conn, table_name):
    """
    Usuwa wszystkie dane z określonej tabeli w bazie danych.

    :param conn: połączenie do bazy danych
    :type conn: psycopg2.extensions.connection
    :param table_name: nazwa tabeli do wyczyszczenia
    :type table_name: str
    """
    cursor = conn.cursor()

    # Usuwanie wszystkich danych z tabeli
    cursor.execute(f'DELETE FROM {table_name};')

    conn.commit()
    cursor.close()

def clear_all_tables(conn):
    """
    Usuwa wszystkie dane ze wszystkich tabel w bazie danych.

    :param conn: połączenie do bazy danych
    :type conn: psycopg2.extensions.connection
    """
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
     """
    Usuwa wszystkie tabele w bazie danych.

    :param conn: połączenie do bazy danych
    :type conn: psycopg2.extensions.connection
    """
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
     """
    Czyści zawartość tabeli lub usuwa tabele w bazie danych.

    Umożliwia wyczyszczenie pojedynczej tabeli, wszystkich tabel
    lub całkowite usunięcie wszystkich tabel w bazie danych.

    Opcje:
    --table [nazwa_tabeli]: Usuń zawartość określonej tabeli.
    --all: Usuń dane ze wszystkich tabel.
    --drop: Usuń wszystkie tabele (całkowicie).
    """
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