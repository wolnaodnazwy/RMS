import simplejson
import psycopg2

def get_database_connection():
    """
    Ustanawia połączenie z bazą danych PostgreSQL.

    Ładuje dane uwierzytelniające z pliku "database_creds.json"
    i używa ich do połączenia się z bazą danych PostgreSQL.

    :return: połączenie do bazy danych
    :rtype: psycopg2.extensions.connection
    """
    with open("database_creds.json") as db_con_file:
        creds = simplejson.loads(db_con_file.read())
    
    conn = psycopg2.connect(
        host=creds['host_name'],
        user=creds['user_name'],
        dbname=creds['db_name'],
        password=creds['password'],
        port=creds['port_number']
    )

    return conn