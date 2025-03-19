import csv
import random
import datetime
from enum import Enum

class ResultEnum(Enum):
    HOME_WIN = '1'
    DRAW = 'X'
    AWAY_WIN = '2'
    PENDING = '?'

# Lista di squadre di calcio
teams = [
    ('Juventus', 'Roma'),
    ('Milan', 'Inter'),
    ('Napoli', 'Lazio'),
    ('Fiorentina', 'Atalanta'),
    ('Bologna', 'Sampdoria'),
    ('Torino', 'Cagliari'),
    ('Sassuolo', 'Empoli'),
    ('Parma', 'Verona'),
    ('Udinese', 'Salernitana'),
    ('Monza', 'Spezia'),
    ('Barcelona', 'Real Madrid'),
    ('Atlético Madrid', 'Sevilla'),
    ('Valencia', 'Villarreal'),
    ('Chelsea', 'Liverpool'),
    ('Manchester United', 'Manchester City'),
    ('Arsenal', 'Tottenham'),
    ('Bayern Munich', 'Borussia Dortmund'),
    ('RB Leipzig', 'Wolfsburg'),
    ('Paris Saint-Germain', 'Marseille'),
    ('Lyon', 'Lille'),
    ('AC Milan', 'Juventus'),
    ('Roma', 'Napoli'),
    ('Barcelona', 'Atletico Madrid'),
    ('Tottenham', 'West Ham United'),
    ('Bayer Leverkusen', 'Bayern Munich'),
    ('Everton', 'Newcastle United'),
    ('Lazio', 'Fiorentina'),
    ('PSG', 'Lyon'),
    ('Manchester City', 'Chelsea'),
    ('Real Madrid', 'Valencia'),
    ('Borussia Monchengladbach', 'Eintracht Frankfurt'),
    ('Leeds United', 'Aston Villa'),
    ('VfB Stuttgart', 'Borussia Dortmund'),
    ('Marseille', 'Nice'),
    ('AC Milan', 'Napoli'),
    ('Celtic', 'Rangers'),
    ('Lazio', 'Inter'),
    ('Real Sociedad', 'Athletic Bilbao'),
    ('Sevilla', 'Real Betis'),
    ('Benfica', 'Portimonense'),
    ('Boca Juniors', 'River Plate'),
    ('Flamengo', 'Vasco da Gama'),
    ('Palmeiras', 'Corinthians'),
    ('Fluminense', 'Sao Paulo'),
    ('São Paulo', 'Internacional'),
    ('Vélez Sarsfield', 'Boca Juniors'),
    ('Santos', 'Gremio'),
    ('Corinthians', 'Flamengo'),
    ('Persebaya', 'Arema FC'),
    ('FC Porto', 'Sporting CP'),
    ('Maritimo', 'Boavista'),
    ('Corinthians', 'Fluminense'),
    ('Hellas Verona', 'Torino'),
    ('Rangers', 'Aberdeen'),
    ('Villarreal', 'Real Betis'),
    ('Palmeiras', 'São Paulo')
]

def generate_csv(filename, num_matches):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['team_home', 'team_away', 'date', 'odds1', 'oddsX', 'odds2', 'result']) 
        
        for _ in range(num_matches):
            team_home, team_away = random.choice(teams)

            # Impostiamo casualmente se la data sarà futura o passata
            is_past_game = random.random() < 0.5  

            if is_past_game:
                date = (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))).date()
                result = random.choice([ResultEnum.HOME_WIN.value, ResultEnum.DRAW.value, ResultEnum.AWAY_WIN.value])
            else:
                date = (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).date()
                result = ResultEnum.PENDING.value 

            odds1 = round(random.uniform(1.5, 3.5), 2)
            oddsX = round(random.uniform(2.5, 3.5), 2)
            odds2 = round(random.uniform(1.5, 3.5), 2)
            
            writer.writerow([team_home, team_away, date, odds1, oddsX, odds2, result])

generate_csv('football_matches.csv', num_matches=20000)
