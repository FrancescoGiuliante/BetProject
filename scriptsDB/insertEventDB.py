import csv
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

def load_csv_to_db(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        
        for row in reader:
            team_home = row[0]
            team_away = row[1]
            date_str = row[2]
            odds1 = row[3]
            oddsX = row[4]
            odds2 = row[5]
            result = row[6]
            
            date = datetime.strptime(date_str, "%Y-%m-%d").date() 
           
            
            query = """
                INSERT INTO bet_event (team_home, team_away, date, odds1, "oddsX", odds2, result)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            cur.execute(query, (team_home, team_away, date, odds1, oddsX, odds2, result))

    conn.commit()

d1 = datetime.now()
load_csv_to_db('football_matches.csv')
d2 = datetime.now()

cur.close()
conn.close()

print(f"Tempo impiegato: {d2 - d1}")
