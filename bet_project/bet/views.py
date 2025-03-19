from django.shortcuts import render, redirect
import psycopg2
from .forms import LoginForm, UserRegistrationForm, CredentialForm
from .models import Bet, BetSlip, BetStatusEnum, BetUserStatusEnum, Credential, ResultEnum, User, Event
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from decimal import Decimal
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render
from decimal import Decimal
from .models import Event, Bet, ResultEnum


def home(request):
    events = Event.objects.filter(result='?') 
    bets = request.session.get('bets', [])
    user_id = request.session.get('user_id') 
    user = None
    if user_id:
        user = User.objects.get(id=user_id) 
    if request.method == 'POST':
        if 'remove_bet' in request.POST:
            remove_index = int(request.POST['remove_bet'])
            del bets[remove_index]
            request.session['bets'] = bets
        else:
            event_id = request.POST.get('event_id')
            bet_type = request.POST.get('bet_type')

            event = Event.objects.get(id=event_id)
            
            if bet_type == 'home':
                result = ResultEnum.HOME_WIN.value
            elif bet_type == 'draw':
                result = ResultEnum.DRAW.value
            elif bet_type == 'away':
                result = ResultEnum.AWAY_WIN.value
            
            bets.append({
                'event_id': int(event_id),
                'result': result,
                'selected': True
            })
            
            request.session['bets'] = bets

    detailed_bets = []
    for bet in bets:
        event = Event.objects.get(id=bet['event_id'])
        detailed_bets.append({
            'event': event,
            'result': bet['result'],
            'selected': bet['selected']
        })
    
    return render(request, 'bet/home.html', {'events': events, 'bets': detailed_bets, 'user': user})


def play_bet(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  

    user = User.objects.get(id=user_id)

    # Caso quando l'utente sta confermando la scommessa (POST con 'confirm_bet')
    if request.method == 'POST' and 'confirm_bet' in request.POST:
        bets_data = request.session.get('bets', [])
        stake = Decimal(request.POST.get('stake', '0.00'))

        if not bets_data:
            return HttpResponse("Nessuna scommessa selezionata.")

        total_odds = Decimal('1.00')
        # Calcoliamo le odds totali
        for bet_data in bets_data:
            event = Event.objects.get(id=bet_data['event_id'])
            if bet_data['result'] == ResultEnum.HOME_WIN.value:
                total_odds *= Decimal(event.odds1)
            elif bet_data['result'] == ResultEnum.DRAW.value:
                total_odds *= Decimal(event.oddsX)
            elif bet_data['result'] == ResultEnum.AWAY_WIN.value:
                total_odds *= Decimal(event.odds2)

        # Calcoliamo la potenziale vincita
        potential_win = stake * total_odds

        try:
            # Creiamo la BetSlip
            bet_slip = BetSlip.objects.create(
                user=user,
                stake=stake,
                status=BetUserStatusEnum.PENDING.value,
                potential_win=potential_win  # Assegniamo il valore calcolato a 'potential_win'
            )

            # Creiamo le bet associate alla betslip
            for bet_data in bets_data:
                event = Event.objects.get(id=bet_data['event_id'])
                bet = Bet.objects.create(
                    event=event,
                    result=bet_data['result'],
                    stake=stake,
                    status=BetStatusEnum.PENDING.value,
                    betslip=bet_slip  # Associare la bet alla betslip
                )
                bet_slip.bets.add(bet)  # Aggiungi la bet alla betslip tramite il ManyToMany

            # Rimuoviamo le scommesse dalla sessione
            del request.session['bets']
            return redirect('bet_success')

        except Exception as e:
            if "Insufficient credit to place the bet" in str(e):
                return redirect('bet_failure')
            else:
                return HttpResponse(f"Errore inaspettato: {e}")

    # Caso quando l'utente sta visualizzando la conferma della scommessa (POST senza 'confirm_bet')
    elif request.method == 'POST':
        bets_data = request.session.get('bets', [])
        stake = Decimal(request.POST.get('stake', '0.00'))

        if not bets_data:
            return HttpResponse("Nessuna scommessa selezionata.")

        total_odds = Decimal('1.00')
        for bet_data in bets_data:
            event = Event.objects.get(id=bet_data['event_id'])
            if bet_data['result'] == ResultEnum.HOME_WIN.value:
                total_odds *= Decimal(event.odds1)
            elif bet_data['result'] == ResultEnum.DRAW.value:
                total_odds *= Decimal(event.oddsX)
            elif bet_data['result'] == ResultEnum.AWAY_WIN.value:
                total_odds *= Decimal(event.odds2)

        possible_winnings = round(stake * total_odds, 2)

        return render(request, 'bet/confirm_bet.html', {
            'bets': bets_data,
            'possible_winnings': possible_winnings,
            'stake': stake,
            'user': user
        })

    else:
        return HttpResponse("Metodo non permesso.")



def bet_success(request):
    return render(request, 'bet/bet_success.html')

def bet_failure(request):
    return render(request, 'bet/bet_failure.html')
    

def login(request):
    if request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                credential = Credential.objects.get(email=email)
                if check_password(password, credential.password):
                    request.session['user_id'] = credential.user.id
                    return redirect('home')
                else:
                    form.add_error(None, "Credenziali non valide.")
            except Credential.DoesNotExist:
                form.add_error(None, "Credenziali non valide.")
    else:
        form = LoginForm()
    return render(request, 'bet/login.html', {'form': form})


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('login')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        credential_form = CredentialForm(request.POST)

        if user_form.is_valid() and credential_form.is_valid():
            user = user_form.save()
            password = credential_form.cleaned_data.get('password')
            hashed_password = make_password(password)

            credential = credential_form.save(commit=False)
            credential.user = user
            credential.password = hashed_password
            credential.save()

            return redirect('home')

    else:
        user_form = UserRegistrationForm()
        credential_form = CredentialForm()

    return render(request, 'bet/register.html', {
        'user_form': user_form,
        'credential_form': credential_form
    })


DATABASE_SETTINGS = {
    'NAME': 'betproject',
    'USER': 'postgres',
    'PASSWORD': 'Gheddafi22',
    'HOST': 'localhost',
    'PORT': '5432',
}

def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    try:
        conn = psycopg2.connect(
            dbname=DATABASE_SETTINGS['NAME'],
            user=DATABASE_SETTINGS['USER'],
            password=DATABASE_SETTINGS['PASSWORD'],
            host=DATABASE_SETTINGS['HOST'],
            port=DATABASE_SETTINGS['PORT']
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM betslip_details WHERE user_id = %s;
        """, (user.id,))
        betslips = cursor.fetchall()

        cursor.execute("""
            SELECT * FROM event_bet_summary;
        """)
        event_summary = cursor.fetchall()

        conn.close()
    except Exception as e:
        return render(request, 'bet/error.html', {'error': str(e)})

    return render(request, 'bet/profile.html', {'user': user, 'betslips': betslips, 'event_summary': event_summary})