import pandas as pd
import os.path
from sqlalchemy import create_engine

def collect_data():
    # Zbieranie danych z różnych źródeł
    data = []
    # Logika zbierania danych
    
    while True:
        choice = input("Czy chcesz dodać informacje o sprzęcie? (Tak/Nie): ")
        if choice.lower() == 'nie':
            break
        elif choice.lower() == 'tak':
            # Dodawanie informacji o sprzęcie
            device_type = input("Podaj typ urządzenia: ")
            serial_number = input("Podaj numer seryjny urządzenia: ")
            location = input("Podaj lokalizację urządzenia: ")
            purchase_date = input("Podaj datę zakupu urządzenia: ")
            warranty = input("Podaj informację o gwarancji urządzenia: ")
            maintenance_schedule = input("Podaj plan przeglądów i konserwacji urządzenia: ")
            # Dodawanie informacji do zbioru danych
            data.append({
            'Typ urządzenia': device_type,
            'Numer seryjny': serial_number,
            'Lokalizacja': location,
            'Data zakupu': purchase_date,
            'Gwarancja': warranty,
            'Plan przeglądów i konserwacji': maintenance_schedule
            })
        else: 
             print(f"Błędna odpowiedź! Proszę wybrać 'Tak' lub 'Nie'.")
    

    # Zwracanie zebranych danych jako obiekt DataFrame z biblioteki pandas
    df = pd.DataFrame(data)
    return df

def export_to_csv(dataframe, filename):
    if os.path.isfile(filename):
        # Jeśli plik istnieje, odczytaj istniejący plik CSV
        existing_data = pd.read_csv(filename)
        # Połącz istniejące dane z nowymi danymi
        updated_data = pd.concat([existing_data, dataframe], ignore_index=True)
        # Zapisz zaktualizowane dane do pliku CSV bez nagłówków
        updated_data.to_csv(filename, index=False)
        print(f"Dane zostały zaktualizowane w pliku {filename}.")
    else:
        # Jeśli plik nie istnieje, utwórz nowy plik CSV
        dataframe.to_csv(filename, index=False)
        print(f"Nowy plik {filename} został utworzony.")
    
#def export_to_database(dataframe, database_name, table_name):
    # Eksportowanie danych do bazy danych SQLite
 #   engine = create_engine(f'sqlite:///{database_name}')
  #  dataframe.to_sql(table_name, con=engine, if_exists='replace', index=False)
   # print(f"Dane zostały wyeksportowane do tabeli {table_name} w bazie danych {database_name}.")

def main():
    # Główna funkcja programu
    data = collect_data()
    export_to_csv(data, 'dane.csv')
  #  export_to_database(data, 'dane.db', 'tabela_danych')

if __name__ == '__main__':
    main()
