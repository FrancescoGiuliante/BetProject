import psycopg2
from datetime import datetime, date

DATABASE_SETTINGS = {
    'NAME': 'betproject',
    'USER': 'postgres',
    'PASSWORD': 'Gheddafi22',
    'HOST': 'localhost',
    'PORT': '5432'
}

def reset_future_event_results():
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_SETTINGS['NAME'],
            user=DATABASE_SETTINGS['USER'],
            password=DATABASE_SETTINGS['PASSWORD'],
            host=DATABASE_SETTINGS['HOST'],
            port=DATABASE_SETTINGS['PORT']
        )
        cur = conn.cursor()

        today = date.today()
        today_str = today.strftime('%Y-%m-%d')  

        # Seleziona gli eventi con data maggiore o uguale a oggi
        select_query = "SELECT id FROM bet_event WHERE date >= %s"
        cur.execute(select_query, (today_str,))
        events = cur.fetchall()

        # Aggiorna il risultato di ogni evento a '?'
        for event in events:
            event_id = event[0]
            update_query = "UPDATE bet_event SET result = '?' WHERE id = %s"
            cur.execute(update_query, (event_id,))

        conn.commit()
        print("Risultati degli eventi futuri reimpostati con successo!")

    except Exception as e:
        print(f"Errore durante la reimpostazione dei risultati: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    reset_future_event_results()