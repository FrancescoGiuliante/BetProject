from enum import Enum
from django.db import models

# Enum per i risultati
class ResultEnum(Enum):
    HOME_WIN = '1'
    DRAW = 'X'
    AWAY_WIN = '2'
    PENDING = '?'

# Enum per lo stato delle scommesse
class BetUserStatusEnum(Enum):
    PENDING = 'pending'
    WON = 'won'
    LOST = 'lost'

# Enum per lo stato delle scommesse
class BetStatusEnum(Enum):
    PENDING = 'pending'
    CONCLUDED = 'concluded'

# Modello per l'utente
class User(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_stake = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_winnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} {self.lastname}"
    
    def add_credit(self, amount):
        self.credit += amount
        self.save()

# Modello per le credenziali
class Credential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"Credential for {self.user.name} {self.user.lastname}"

# Modello per gli eventi
class Event(models.Model):
    team_home = models.CharField(max_length=100)
    team_away = models.CharField(max_length=100)
    date = models.DateField()
    odds1 = models.DecimalField(max_digits=5, decimal_places=2)
    oddsX = models.DecimalField(max_digits=5, decimal_places=2)
    odds2 = models.DecimalField(max_digits=5, decimal_places=2)
    result = models.CharField(
        max_length=1,
        choices=[(tag, tag.value) for tag in ResultEnum],
        default=ResultEnum.PENDING.value
    )

    def __str__(self):
        return f"{self.team_home} vs {self.team_away} on {self.date}"

# Modello per le scommesse
class Bet(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  
    result = models.CharField(
        max_length=1,
        choices=[(tag, tag.value) for tag in ResultEnum],  
    )
    stake = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(
        max_length=10,
        choices=[(tag, tag.value) for tag in BetUserStatusEnum],
        default=BetUserStatusEnum.PENDING.value  
    )

    def __str__(self):
        return f"Bet on {self.event} - Predicted: {self.result} - Stake: {self.stake}€ - Status: {self.status}"

# Modello per la schedina
class BetSlip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    stake = models.DecimalField(max_digits=10, decimal_places=2)
    potential_win = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bets = models.ManyToManyField(Bet) 
    status = models.CharField(
        max_length=7,
        choices=[(tag, tag.value) for tag in BetUserStatusEnum],
        default=BetUserStatusEnum.PENDING.value  
    )

    def __str__(self):
        return f"BetSlip for {self.user.name} {self.user.lastname} - Status: {self.status} - Total Stake: {self.total_stake}€"
