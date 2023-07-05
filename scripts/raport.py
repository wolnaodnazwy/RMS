import json
import pandas as pd
from sqlalchemy import create_engine
from connection import get_database_connection

def get_device_counts():
    # Uzyskanie połączenia do bazy danych
    conn = get_database_connection()

    # Odczytanie informacji dostępowych z pliku JSON
    with open('database_creds.json') as file:
        credentials = json.load(file)

    # Tworzenie URL-a dla połączenia z bazą danych PostgreSQL
    db_url = f"postgresql+psycopg2://{credentials['user_name']}:{credentials['password']}@{credentials['host_name']}:{credentials['port_number']}/{credentials['db_name']}"

    # Utworzenie obiektu Engine SQLAlchemy
    engine = create_engine(db_url, creator=lambda: conn)

    # Pobranie liczby urządzeń dla każdego typu
    query = "SELECT Typ_urzadzenia, COUNT(*) AS Liczba_urzadzen FROM data GROUP BY Typ_urzadzenia;"
    device_counts = pd.read_sql_query(query, engine)

    # Zamknięcie połączenia
    conn.close()

    # Zwrócenie podsumowania
    return device_counts

def get_service_results():
    # Uzyskanie połączenia do bazy danych
    conn = get_database_connection()

    # Odczytanie informacji dostępowych z pliku JSON
    with open('database_creds.json') as file:
        credentials = json.load(file)

    # Tworzenie URL-a dla połączenia z bazą danych PostgreSQL
    db_url = f"postgresql+psycopg2://{credentials['user_name']}:{credentials['password']}@{credentials['host_name']}:{credentials['port_number']}/{credentials['db_name']}"

    # Utworzenie obiektu Engine SQLAlchemy
    engine = create_engine(db_url, creator=lambda: conn)

    # Pobranie liczby wyników przeglądu dla każdego typu
    query = "SELECT Wynik_przegladu, COUNT(*) AS Liczba_wynikow FROM service GROUP BY Wynik_przegladu;"
    service_results = pd.read_sql_query(query, engine)

    # Zamknięcie połączenia
    conn.close()

    # Zwrócenie podsumowania
    return service_results

if __name__ == '__main__':
    # Przykład użycia funkcji
    device_counts = get_device_counts()
    print("Podsumowanie urządzeń:")
    print(device_counts)

    service_results = get_service_results()
    print("Podsumowanie wyników przeglądu:")
    print(service_results)
