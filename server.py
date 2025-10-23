import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    email = request.form.get('email', '')
    email = email.strip()
    club = next((c for c in clubs if c.get('email', '').strip() == email), None)
    if not email or not club:
        flash("Sorry, that email was not found, please try again.")
        return render_template('index.html')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    
    competition_date = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("This competition has already taken place, booking is not allowed.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    MAX_BOOKING = 12
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    places = request.form.get('places')
    if not places:
        flash("Please enter a number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # même si on a vérifié dans le formulaire sur le HTML avec un input de type "number",
    # on doit quand même gérer le cas où un utilisateur malveillant envoie une valeur non numérique
    # en modifiant via les outils de développement du navigateur. 
    try:
        placesRequired = int(places)
    except ValueError:
        flash("Invalid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    club_points = int(club['points'])

    if placesRequired <= 0:
        flash("Invalid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > club_points:
        flash("Cannot book more places than club points.")
        return render_template('welcome.html', club=club, competitions=competitions) 


    if placesRequired > MAX_BOOKING:
        flash(f"Cannot book more than {MAX_BOOKING} places for this competition.")
        return render_template('welcome.html', club=club, competitions=competitions)   

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = club_points - placesRequired
    flash('Great - booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))