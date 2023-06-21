import pandas as pd
import os.path
from sqlalchemy import create_engine
import subprocess

def collect_data():
    # Zbieranie danych z różnych źródeł
    equipment_data = []
    service_data = []
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
            # Dodawanie informacji do zbioru danych
            equipment_data.append({
                'Typ urządzenia': device_type,
                'Numer seryjny': serial_number,
                'Lokalizacja': location,
                'Data zakupu': purchase_date,
                'Gwarancja': warranty
            })
        
             # Dodawanie informacji o przeglądzie
            service_date = input("Podaj datę przeglądu: ")
            service_result = input("Podaj wynik przeglądu: ")
            # Dodawanie informacji do zbioru danych
            service_data.append({
                'Numer seryjny': serial_number,
                'Data przeglądu': service_date,
                'Wynik przeglądu': service_result
            })
        else: 
             print(f"Błędna odpowiedź! Proszę wybrać 'Tak' lub 'Nie'.")
    

    # Zwracanie zebranych danych jako obiekt DataFrame z biblioteki pandas
    equipment_df = pd.DataFrame(equipment_data)
    service_df = pd.DataFrame(service_data)
    return equipment_df, service_df

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

def main():
    # Główna funkcja programu
    equipment_data, service_data = collect_data()
    export_to_csv(equipment_data, 'results/data.csv')
    export_to_csv(service_data, 'results/service.csv')
    
    # Uruchomienie drugiego skryptu
    subprocess.run(['python', 'dataToDB.py'])

if __name__ == '__main__':
    main()
