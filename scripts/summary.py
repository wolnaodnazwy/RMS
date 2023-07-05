import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import json
import base64
import os

def generate_summary_report():
    # Otwarcie pliku JSON i odczytanie danych połączenia
    with open('database_creds.json') as json_file:
        connection_data = json.load(json_file)

    # Tworzenie URI połączenia na podstawie danych z pliku JSON
    connection_uri = f"postgresql://{connection_data['user_name']}:{connection_data['password']}@{connection_data['host_name']}:{connection_data['port_number']}/{connection_data['db_name']}"

    # Pobieranie danych z bazy danych
    data_query = "SELECT * FROM public.data"
    service_query = "SELECT * FROM public.service"
    
    engine = create_engine(connection_uri)
    data_df = pd.read_sql_query(data_query, engine)
    service_df = pd.read_sql_query(service_query, engine)

    # Podsumowanie danych
    total_devices = len(data_df)
    total_services = len(service_df)
    average_devices_per_location = data_df['lokalizacja'].value_counts().mean()

    # Podsumowanie przeglądów
    positive_services = service_df[service_df['wynik_przegladu'] == 'Pozytywny']
    negative_services = service_df[service_df['wynik_przegladu'] == 'Negatywny']
    suspended_services = service_df[service_df['wynik_przegladu'] == 'Wstrzymany']

    total_percentage = 100
    positive_percentage = len(positive_services) / total_services * 100
    negative_percentage = len(negative_services) / total_services * 100
    suspended_percentage = len(suspended_services) / total_services * 100

    # Generowanie wykresu
    device_counts = data_df['typ_urzadzenia'].value_counts()
    device_counts.plot(kind='bar', figsize=(8, 6))
    plt.title('Liczba urządzeń według typu')
    plt.xlabel('Typ urządzenia')
    plt.ylabel('Liczba')
    plt.savefig('results/wykres.png')  # Zapisanie wykresu jako pliku PNG

    # Wyświetlanie podsumowania
    print(f"Podsumowanie danych:")
    print(f"Całkowita liczba urządzeń: {total_devices}")
    print(f"Całkowita liczba przeglądów: {total_services}")
    print(f"Średnia liczba urządzeń na lokalizację: {average_devices_per_location:.2f}")
    print(f"Procent przeglądów pozytywnych: {positive_percentage:.2f}%")
    print(f"Procent przeglądów negatywnych: {negative_percentage:.2f}%")
    print(f"Procent przeglądów wstrzymanych: {suspended_percentage:.2f}%")

    # Tworzenie folderu "results", jeśli nie istnieje
    if not os.path.exists('results'):
        os.makedirs('results')

    # Zapisanie danych do pliku CSV wraz z załączonym plikiem obrazu
    summary_data = {
        'Całkowita liczba urządzeń': [total_devices],
        'Całkowita liczba przeglądów': [total_services],
        'Średnia liczba urządzeń na lokalizację': [average_devices_per_location],
        'Procent przeglądów pozytywnych': [positive_percentage],
        'Procent przeglądów negatywnych': [negative_percentage],
        'Procent przeglądów wstrzymanych': [suspended_percentage]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv('results/podsumowanie.csv', index=False)

    # Dodanie pliku obrazu jako załącznik do pliku CSV
    with open('results/wykres.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    summary_df['Wykres'] = encoded_image

# Wywołanie funkcji generującej raport
generate_summary_report()


