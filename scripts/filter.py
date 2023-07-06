from connection import get_database_connection
from raportGenerator import generate_report
from datetime import date

def check_enum_type_exists(conn, enum_type_name):
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_type WHERE typname = %s)", (enum_type_name,))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists


def get_available_tables():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    cursor.close()
    conn.close()
    return table_names


def get_table_columns(table_name):
    conn = get_database_connection()
    cursor = conn.cursor()

    # Sprawdzanie, czy tabela istnieje
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        print(f"Tabela '{table_name}' nie istnieje.")
        return []

    # Pobieranie dostępnych kolumn w tabeli
    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
    columns = cursor.fetchall()
    column_names = [column[0] for column in columns]

    cursor.close()
    conn.close()

    return column_names


def get_column_values(table_name, column_name):
    conn = get_database_connection()
    cursor = conn.cursor()

    # Sprawdzanie, czy tabela istnieje
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        print(f"Tabela '{table_name}' nie istnieje.")
        return []

    # Sprawdzanie, czy kolumna istnieje w tabeli
    cursor.execute(
        f"SELECT EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = %s AND column_name = %s)",
        (table_name, column_name))
    column_exists = cursor.fetchone()[0]

    if not column_exists:
        print(f"Kolumna '{column_name}' nie istnieje w tabeli '{table_name}'.")
        return []

    # Pobieranie unikalnych wartości w kolumnie
    cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name}")
    values = cursor.fetchall()
    column_values = [value[0] for value in values]

    cursor.close()
    conn.close()

    return column_values


def filter_table_by_column(table_name, column_name, filter_value=None):
    conn = get_database_connection()
    cursor = conn.cursor()

    # Sprawdzanie, czy tabela istnieje
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        print(f"Tabela '{table_name}' nie istnieje.")
        return

    # Sprawdzanie, czy kolumna istnieje w tabeli
    cursor.execute(
        f"SELECT EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = %s AND column_name = %s)",
        (table_name, column_name))
    column_exists = cursor.fetchone()[0]

    if not column_exists:
        print(f"Kolumna '{column_name}' nie istnieje w tabeli '{table_name}'.")
        return

    # Filtrowanie danych
    if filter_value is None:
        cursor.execute(f"SELECT * FROM {table_name}")
    else:
        cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = %s", (filter_value,))

    rows = cursor.fetchall()

    if rows:
        print(f"Wyniki filtrowania w tabeli '{table_name}', dla kolumny '{column_name}':")
        for row in rows:
            formatted_row = [str(value) if isinstance(value, date) else value for value in row]
            print(formatted_row)
    else:
        print(f"Brak wyników filtrowania w tabeli '{table_name}', dla kolumny '{column_name}'.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    while True:
        available_tables = get_available_tables()
        print("Dostępne tabele:")
        for index, table in enumerate(available_tables, start=1):
            print(f"{index}. {table}")

        table_index = input("Wybierz numer tabeli (lub wpisz 'exit' aby zakończyć): ")

        if table_index.lower() == 'exit':
            break

        try:
            table_index = int(table_index) - 1
            if table_index < -1 or table_index >= len(available_tables):
                raise ValueError
        except ValueError:
            print("Nieprawidłowy numer tabeli.")
            continue

        table_name = available_tables[table_index]

        columns = get_table_columns(table_name)

        if not columns:
            print(f"Tabela '{table_name}' nie istnieje lub nie ma dostępnych kolumn.")
            continue

        print("Dostępne kolumny:")
        for index, column in enumerate(columns, start=1):
            print(f"{index}. {column}")

        column_index = input("Wybierz numer kolumny (lub wpisz 'exit' aby zakończyć): ")
        
        if column_index.lower() == 'exit':
            break

        try:
            column_index = int(column_index) - 1
            if column_index < -1 or column_index >= len(columns):
                raise ValueError
        except ValueError:
            print("Nieprawidłowy numer kolumny.")
            continue

        selected_column = columns[column_index]

        column_values = get_column_values(table_name, selected_column)

        if not column_values:
            print(f"Kolumna '{selected_column}' nie istnieje w tabeli '{table_name}' lub nie ma dostępnych wartości.")
            continue

        print("Dostępne wartości:")
        print("0. Brak filtracji")
        for index, value in enumerate(column_values, start=1):
            print(f"{index}. {value}")

        value_index = input("Wybierz numer wartości (lub wpisz 'exit' aby zakończyć): ")
        
        if value_index.lower() == 'exit':
            break

        try:
            value_index = int(value_index) - 1
            if value_index < -1 or value_index >= len(column_values):
                raise ValueError
        except ValueError:
            print("Nieprawidłowy numer wartości.")
            continue

        if value_index == -1:
            filter_table_by_column(table_name, selected_column)
            if input("Czy chcesz utworzyć raport z przefiltrowanych danych? (Tak/Nie): ").lower() != 'tak':
                continue
            else:
                filename = input("Podaj nazwę pliku CSV dla raportu: ")
                generate_report(table_name, selected_column, filter_value=None, filename=filename)
                
        else:
            selected_value = column_values[value_index]
            filter_table_by_column(table_name, selected_column, selected_value)
            if input("Czy chcesz utworzyć raport z przefiltrowanych danych? (Tak/Nie): ").lower() != 'tak':
                continue
            else:
                filename = input("Podaj nazwę pliku CSV dla raportu: ")
                generate_report(table_name, selected_column, filter_value=selected_value, filename=filename)
