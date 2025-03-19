import psycopg2
import random
from datetime import datetime

conn = psycopg2.connect(
    dbname="betproject", 
    user="postgres",  
    password="Gheddafi22",  
    host="localhost",  
    port="5432" 
)

cur = conn.cursor()

def update_pending_results():
    query = "SELECT id, result FROM bet_event WHERE result = '?'"
    cur.execute(query)
    
    events = cur.fetchall()
    
    updated_count = 0 
    
    for event in events:
        event_id = event[0]
        new_result = random.choice(['1', 'X', '2'])
        
        update_query = """
            UPDATE bet_event 
            SET result = %s 
            WHERE id = %s;
        """
        cur.execute(update_query, (new_result, event_id))
        
        updated_count += 1 

    conn.commit()
    return updated_count

d1 = datetime.now()
updated_events = update_pending_results()
d2 = datetime.now()

cur.close()
conn.close()

print(f"Tempo impiegato per aggiornare: {d2 - d1}")
print(f"Partite trovate e aggiornate: {updated_events}")
