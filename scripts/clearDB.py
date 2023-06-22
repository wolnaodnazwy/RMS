import argparse
import psycopg2

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

def clear_database():
    conn = psycopg2.connect(
        host='127.0.0.1',
        port='5432',
        dbname='student02db',
        user='student02',
        password='852BSW529qfdpxGRP'
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('--table', help='Usuń zawartość tabeli')
    parser.add_argument('--all', action='store_true', help='Usuń wszystkie tabele')
    args = parser.parse_args()

    if args.table:
        clear_table(conn, args.table)
    elif args.all:
        clear_all_tables(conn)
    else:
        print('Nie podano żadnej opcji. Użyj --table lub --all.')

    conn.close()

if __name__ == '__main__':
    clear_database()