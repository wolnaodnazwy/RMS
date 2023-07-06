import pandas as pd
import os.path
import re

def validate_date_format(date):
    # Sprawdzanie poprawności formatu daty
    pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
    if re.match(pattern, date):
        return True
    else:
        print("Błędny format daty. Poprawny format: yyyy-mm-dd")
        return False
    
def validate_enum_value(enum_type, value):
    # Sprawdzanie poprawności wartości enum
    enum_values = [val.lower() for val in enum_type]
    value_lower = value.lower()
    if value_lower in enum_values:
        return True
    else:
        print(f"Błędna wartość. Dostępne opcje: {', '.join(enum_values)}. Wprowadzona wartość: {value}")
        return False

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
            purchase_date = input("Podaj datę zakupu urządzenia (yyyy-mm-dd): ")
            warranty = input("Czy urządzenie posiada gwarancję?: ")
            # Walidacja typu urządzenia
            while not validate_enum_value(['Laptop', 'Drukarka', 'Smartphone', 'Fax', 'Komputer stacjonarny', 'Tablet', 'Router', 'Skaner', 'Projektor', 'Serwer'], device_type):
                device_type = input("Podaj typ urządzenia: ")
            # Walidacja informacji o gwarancji
            while not validate_enum_value(['Tak', 'Nie'], warranty):
                warranty = input("Czy urządzenie posiada gwarancję?: ")
            # Walidacja daty zakupu
            while not validate_date_format(purchase_date):
                purchase_date = input("Podaj datę zakupu urządzenia (yyyy-mm-dd): ")
            # Dodawanie informacji do zbioru danych
            equipment_data.append({
                'Typ urządzenia': device_type.capitalize(),
                'Numer seryjny': serial_number,
                'Lokalizacja': location.capitalize(),
                'Data zakupu': purchase_date,
                'Gwarancja': warranty.capitalize()
            })
        
            # Dodawanie informacji o przeglądzie
            service_date = input("Podaj datę przeglądu (yyyy-mm-dd): ")
            service_result = input("Podaj wynik przeglądu: ")
            # Walidacja wyniku przeglądu
            while not validate_enum_value(['Pozytywny', 'Negatywny', 'Wstrzymany'], service_result):
                service_result = input("Podaj wynik przeglądu: ")
            # Walidacja daty przeglądu
            while not validate_date_format(service_date):
                service_date = input("Podaj datę przeglądu (yyyy-mm-dd): ")
            # Dodawanie informacji do zbioru danych
            service_data.append({
                'Numer seryjny': serial_number,
                'Data przeglądu': service_date,
                'Wynik przeglądu': service_result.capitalize()
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

if __name__ == '__main__':
    main()
