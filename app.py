from flask import Flask, request, url_for, session, redirect, render_template
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import pandas as pd
import numpy as np
 
 
app = Flask(__name__)
 
 
# create more permanent cookies (not super sensitive information)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
 
@app.route("/")
def index():
   return render_template("landing.html")
 

@app.route("/login")
def login():
   oauth = configure_oauth()
   auth_url = oauth.get_authorize_url()
   return redirect(auth_url)


@app.route("/redirect")
def redirected():
    oauth = configure_oauth()
    session.clear()
    # use access code to get access token
    code = request.args.get("code")
    token = oauth.get_access_token(code)
    # set token in session
    session[0] = token
    return redirect(url_for('getHistory',  _external=True))
 

@app.route("/history")
def getHistory():
    # access user's data
    token = get_token()
    spotify = spotipy.Spotify(auth=token['access_token'])
    # long term calculation
    long_term_tracks = spotify.current_user_top_tracks(limit=50, time_range="long_term")['items']
    average_valence_long = calculate_average_valence(long_term_tracks)
    # medium term calculation
    medium_term_tracks = spotify.current_user_top_tracks(limit=50, time_range="medium_term")['items']
    average_valence_medium = calculate_average_valence(medium_term_tracks)
    # short term calculation
    short_term_tracks = spotify.current_user_top_tracks(limit=50, time_range="short_term")['items']
    average_valence_short = calculate_average_valence(short_term_tracks)
    # calculate happiness percentages
    happiness_percentage_long = str(round(average_valence_long * 100))
    happiness_percentage_medium = str(round(average_valence_medium * 100))
    happiness_percentage_short = str(round(average_valence_short * 100))
    # calculate percent change in happiness index
    series_long = pd.Series([int(happiness_percentage_long), int(happiness_percentage_short)])
    pct_change_long = series_long.pct_change()
    pct_change_rounded = round(pct_change_long[1], 2)
    # calculate top 5 happy songs all-time and current
    top5_long = top_five_generator(long_term_tracks)
    top5_short = top_five_generator(short_term_tracks)
    # calculate top 5 sad songs all-time and current
    top5_long_sad = top_five_generator_sad(long_term_tracks)
    top5_short_sad = top_five_generator_sad(short_term_tracks)

    return render_template("results.html", long=happiness_percentage_long, medium=happiness_percentage_medium, short=happiness_percentage_short, pct_change_rounded=pct_change_rounded, happytop5a=top5_long, happytop5c=top5_short, sadtop5a=top5_long_sad, sadtop5c=top5_short_sad)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index', _external=True))


def get_token():
    token = session[0]
    # make sure access token is active
    if not token:
        return redirect(url_for('login', _external=True))
    current_time = int(time.time())
    expiration = token['expires_at'] - current_time < 60
    # get refresh token when expired
    if (expiration):
        oauth = configure_oauth()
        token = oauth.refresh_access_token(token['refresh_token'])
    return token
    
 
def configure_oauth():
   return SpotifyOAuth (
       client_id="b29fa8d32fe84c9ab17824fcbc95252c",
       client_secret="7d224df0518d442380093e3316aff493",
       redirect_uri=url_for('redirected', _external=True),
       scope="user-top-read"
   )


def calculate_average_valence(term_valence):
    token = get_token()
    spotify = spotipy.Spotify(auth=token['access_token'])
    # initialize variables
    valence = 0
    counter = 0
    total_track_valence = 0
    # find valence for each song and create average
    for item in term_valence:
        track = item['id']
        track_features = spotify.audio_features(tracks=track)
        intermediary = track_features[0]
        valence = intermediary['valence']
        total_track_valence += valence
        counter += 1
    # calculate final average valence and return
    average_valence = total_track_valence / counter
    return average_valence


def top_five_generator(tracks):
    # initialize variables and get access from API
    token = get_token()
    spotify = spotipy.Spotify(auth=token['access_token'])
    valence = 0
    rank1, rank2, rank3, rank4, rank5 = 0, 0, 0, 0, 0
    rank1_id, rank2_id, rank3_id, rank4_id, rank5_id = 0, 0, 0, 0, 0
    # set and fill ranks by traversing API outputs
    for item in tracks:
        track = item['id']
        track_features = spotify.audio_features(tracks=track)
        intermediary = track_features[0]
        valence = intermediary['valence']
        if (valence > rank1):
            rank1 = valence
            rank1_id = track
            continue
        elif (valence > rank2):
            rank2 = valence
            rank2_id = track
            continue
        elif (valence > rank3):
            rank3 = valence
            rank3_id = track
            continue
        elif (valence > rank4):
            rank4 = valence
            rank4_id = track
            continue
        elif (valence > rank5):
            rank5 = valence
            rank5_id = track
            continue
    # get each rank's information
    number1 = song_puller(rank1_id)
    number2 = song_puller(rank2_id)
    number3 = song_puller(rank3_id)
    number4 = song_puller(rank4_id)
    number5 = song_puller(rank5_id)

    number1a = artist_puller(rank1_id)
    number2a = artist_puller(rank2_id)
    number3a = artist_puller(rank3_id)
    number4a = artist_puller(rank4_id)
    number5a = artist_puller(rank5_id)
    # return value in list
    top5_list = [number1, number2, number3, number4, number5, number1a, number2a, number3a, number4a, number5a]
    
    return top5_list


def top_five_generator_sad(tracks):
    token = get_token()
    spotify = spotipy.Spotify(auth=token['access_token'])
    valence = 0
    rank1, rank2, rank3, rank4, rank5 = 1, 1, 1, 1, 1
    rank1_id, rank2_id, rank3_id, rank4_id, rank5_id = 0, 0, 0, 0, 0
    for item in tracks:
        track = item['id']
        track_features = spotify.audio_features(tracks=track)
        intermediary = track_features[0]
        valence = intermediary['valence']
        if (valence < rank5):
            rank5 = valence
            rank5_id = track
            continue
        elif (valence < rank4):
            rank4 = valence
            rank4_id = track
            continue
        elif (valence < rank3):
            rank3 = valence
            rank3_id = track
            continue
        elif (valence < rank2):
            rank2 = valence
            rank2_id = track
            continue
        elif (valence < rank1):
            rank1 = valence
            rank1_id = track
            continue
    # get each rank's information
    number1 = song_puller(rank1_id)
    number2 = song_puller(rank2_id)
    number3 = song_puller(rank3_id)
    number4 = song_puller(rank4_id)
    number5 = song_puller(rank5_id)

    number1a = artist_puller(rank1_id)
    number2a = artist_puller(rank2_id)
    number3a = artist_puller(rank3_id)
    number4a = artist_puller(rank4_id)
    number5a = artist_puller(rank5_id)

    top5_list = [number1, number2, number3, number4, number5, number1a, number2a, number3a, number4a, number5a]
    
    return top5_list


def song_puller(id):
    token = get_token()
    spotify = spotipy.Spotify(auth=token['access_token'])
    song_title = spotify.track(id)['name']
    return song_title


def artist_puller(id):
    token = get_token()
    spotify = spotipy.Spotify(auth=token['access_token'])
    artist2 = spotify.track(id)['artists']
    artist1 = artist2[0]
    artist = artist1["name"]
    return artist