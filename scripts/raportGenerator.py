import csv
import os
from connection import get_database_connection

def generate_report(table_name, column_name, filter_value=None, filename='report.csv'):
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
        filename_with_extension = f"{filename}.csv"
        results_dir = "results"

        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        file_path = os.path.join(results_dir, filename_with_extension)

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([column[0] for column in cursor.description])
            writer.writerows(rows)

        print(f"Raport został utworzony i zapisany w pliku {filename_with_extension}.")
    else:
        print(f"Brak wyników filtrowania w tabeli '{table_name}', dla kolumny '{column_name}'.")

    cursor.close()
    conn.close()
