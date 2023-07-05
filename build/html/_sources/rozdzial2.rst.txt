===============
Rozdział 2
===============

Stworzona aplikacja umożliwia zarządzanie bazą danych, która zajmuje się obsługą serwisową dla wskazanego budynku. Baza zawiera dane odnośnie dostepnego sprzętu oraz w którym pomieszczeniu jest zainstalowany. Można nazwać ją jako inwentaryzację sprzętową. 

Instrukcja części klienckiej
--------------------------------

Dane w bazie są zbierane w dwóch tabelach. Pierwsza tabela posiada kolumny takie jak: Typ urządzenia, Numer seryjny, Lokalizacja, Data zakupu, Gwarancja.
W drugiej tabeli zbierane są dane odnośnie przeglądów. Zawiera kolumny: Numer seryjny, Data przeglądu, Wynik przeglądu.
Numer seryjny sprzętu jest kluczem głównym dla tej bazy.
Obsługa serwisowa urządzeń części klienckiej odbywa się za pomocą konsoli. Uruchamiamy aplikację za pomocą pliku menagement.py.
Oto opis każdej opcji menu wraz z odpowiadającymi im plikami:

1. Wprowadź dane:
------------------------------------
Ta opcja pozwala na wprowadzenie danych do programu. Po uruchomieniu zadaje pytanie czy użytkownik chce dodać nowe dane. Po twierdzącej odpowiedzi, wprowadzamy dane: 
-"Podaj typ urządzenia: "
-"Podaj numer seryjny urządzenia: "
-"Podaj lokalizację urządzenia: "
-"Podaj datę zakupu urządzenia (yyyy-mm-dd): "
-"Czy urządzenie posiada gwarancję?: "
-"Podaj datę przeglądu (yyyy-mm-dd): "
-"Podaj wynik przeglądu: "

Odpowiada za to plik: (data.py)

2.Zaimportuj dane do SQLite:
-------------------------------------------
Ta opcja odpowiada za importowanie danych wprowadzonych z pliku .csv do bazy danych SQLite. Plik dataToDB.py zawiera skrypt, który wykonuje operacje związane z importem danych i zapisuje je w bazie danych SQLite.

Odpowiada za to plik: (dataToDB.py)

3.Zaimportuj dane do PostgreSQL:
------------------------------------------------------
Ta opcja służy do importowania danych z bazy danych utworzonych w SQLite do bazy danych PostgreSQL. Skrypt importToPostgres.py zajmuje się operacjami związanymi z importem danych i zapisuje je w bazie danych PostgreSQL.

Odpowiada za to plik: (importToPostgres.py)

Dokładne omówienie importowania z SQLite do PostgreSQL zostanie przedstawione w rozdziale 3.

4.Utwórz strukturę bazy danych:
-----------------------------------------------------
Ta opcja odpowiada za utworzenie struktury bazy danych. Skrypt createStructure.py zawiera definicje tabel, relacji i innych obiektów bazy danych, które są potrzebne do prawidłowego funkcjonowania programu.

Odpowiada za to plik: (createStructure.py)

5. Wstaw dane testowe:
---------------------------------------
Ta opcja służy do wstawienia danych testowych do bazy danych. Plik testData.py zawiera skrypt, który posiada przykładowe dane testowe i wprowadza je do bazy danych.

Odpowiada za to plik: (testData.py)

6.Wyczyść tabelę:
----------------------------------
Ta opcja umożliwia wyczyszczenie zawartości wybranej tabeli w bazie danych. Użytkownik zostanie poproszony o podanie nazwy tabeli, a następnie skrypt clearDB.py wykonuje operacje usuwania danych z tej tabeli.

Odpowiada za to plik: (clearDB.py)

7. Wyczyść wszystkie tabele lub bazę danych:
------------------------------------------------------------
Ta opcja pozwala na wyczyszczenie wszystkich tabel w bazie danych lub całej bazy danych. Użytkownik zostanie poproszony o podanie odpowiedniego parametru (--all lub --drop), a następnie skrypt clearDB.py wykonuje odpowiednie operacje czyszczenia.

Odpowiada za to plik: (clearDB.py)

8. Filtruj dane i twórz raporty:
------------------------------------------
Opcja implementuje filtrowanie danych i tworzenie raportów na podstawie określonych kryteriów.

Odpowiadają za to pliki: (raportGenerator.py oraz filter.py)

9. Stwórz podsumowanie danych: 
---------------------------------------------
Agreguje dane i tworzy podsumowanie na podstawie określonych parametrów.

Odpowiada za to plik: (summary.py)

10. Wyjdź z programu:
--------------------------
Opcja kończy działanie programu i zamyka go.


Omówienie importu danych z pliku data.py do SQLite:
------------------------------------------------------------
1.Wczytanie danych o sprzęcie i przeglądach z plików CSV przy użyciu biblioteki pandas.
2.Nawiązanie połączenia z bazą danych PostgreSQL poprzez wywołanie funkcji get_database_connection.
3.Wywołanie funkcji create_table w celu utworzenia wymaganych tabel w bazie danych.
4.Przekształcenie danych o sprzęcie i przeglądach z obiektów DataFrame na listy krotek.
5.Wywołanie funkcji insert_equipment_data w celu wstawienia danych o sprzęcie do tabeli "data" w bazie danych.
6.Wywołanie funkcji insert_service_data w celu wstawienia danych o przeglądach do tabeli "service" w bazie danych.
7.Zatwierdzenie zmian w bazie danych poprzez wywołanie metody commit.
8.Zamknięcie połączenia z bazą danych poprzez wywołanie metod close na obiektach kursora i połączenia.


# Sprawdzanie poprawności formatu daty

    def validate_date_format(date): 
     pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
    if re.match(pattern, date):
        return True
    else:
        print("Błędny format daty. Poprawny format: yyyy-mm-dd")
        return False
# Sprawdzanie poprawności wartości enum

    def validate_enum_value(enum_type, value):
    enum_values = [val.lower() for val in enum_type]
    value_lower = value.lower()
    if value_lower in enum_values:
        return True
    else:
        print(f"Błędna wartość. Dostępne opcje: {', '.join(enum_values)}. Wprowadzona wartość: {value}")
        return False
        
 # Zbieranie danych z różnych źródeł
 
    def collect_data():
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

