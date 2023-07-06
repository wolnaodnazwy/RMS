import subprocess

def print_menu():
    print("1. Wprowadź dane")
    print("2. Zaimportuj dane do SQLite")
    print("3. Zaimportuj dane do PostgreSQL")
    print("4. Utwórz strukturę bazy danych")
    print("5. Wstaw dane testowe")
    print("6. Wyczyść tabelę")
    print("7. Wyczyść wszystkie tabele lub baze danych")
    print("8. Filtruj dane i twórz raporty")
    print("9. Stwórz podsumowanie danych")
    print("10. Wyjdź z programu")

def execute_script(script):
    subprocess.run(['python', script])

def main():
    while True:
        print_menu()
        choice = input("Wybierz opcję (1-10): ")

        if choice == '1':
            execute_script('data.py')
        elif choice == '2':
            execute_script('dataToDB.py')
        elif choice == '3':
            execute_script('importToPostgres.py')
        elif choice == '4':
            execute_script('createStructure.py')
        elif choice == '5':
            execute_script('testData.py')
        elif choice == '6':
            param = input("Podaj nazwe tabeli ")
            subprocess.run(['python', 'clearDB.py', '--table', param])
        elif choice == '7':
            param = input("Podaj parametr (--all, --drop) ")
            subprocess.run(['python', 'clearDB.py', param])
        elif choice == '8':
            execute_script('filter.py')
        elif choice == '9':
            execute_script('summary.py')
        elif choice == '10':
            print("Zamykanie programu...")
            break
        else:
            print("Nieprawidłowy wybór. Wybierz opcję od 1 do 10.")

if __name__ == '__main__':
    main()