import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname="betproject", 
    user="postgres",  
    password="Gheddafi22",  
    host="localhost",  
    port="5432" 
)

cur = conn.cursor()

def delete_all_events():
    delete_query = "DELETE FROM bet_event;"
    cur.execute(delete_query)
    conn.commit()

d1 = datetime.now()
delete_all_events()
d2 = datetime.now()

cur.close()
conn.close()

print(f"Tempo impiegato per cancellare tutte le righe: {d2 - d1}")