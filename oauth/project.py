from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User
from flask import session as login_session
from flask_oauth import OAuth
import random
import string
import json
from urllib import urlopen
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from google.oauth2 import id_token
from google.auth.transport import requests
import httplib2
from flask import make_response
import requests
from datetime import datetime

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


APPLICATION_NAME = "oauth-test"
# user login status


def signin_required(func):
    """
    A decorator to confirm a user is signed in or redirect as needed.
    """
    def check_signin():
        # Redirect to login if user not logged in, else execute func.
        if login_session.has_key('username'):
            return func()
        else:
            return redirect(url_for('showSignin'))
    return check_signin

# google
GOOGLE_CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
GOOGLE_CLIENT_SECRET = json.loads(open('client_secrets.json', 'r').read())['web']['client_secret']
FACEBOOK_ID = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
FACEBOOK_SECRET = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']


# signin
@app.route('/signin')
def showSignin():
    return render_template('signin.html')


# after signed in
@app.route('/in')
@signin_required
def showUser():
    userId = login_session['user_id']
    userName = login_session['username']
    accessToken = login_session['access_token']
    email = login_session['email']
    provider = login_session['provider']
    providerId = login_session['provider_id']
    return render_template('in.html', userId=userId, userName = userName, accessToken=accessToken,
                           email=email, provider=provider, providerId=providerId)


# google connect
@app.route('/gsignin', methods=['POST'])
def gconnect():
    # Obtain authorization code
    request_data = request.get_json()
    if 'id_token' in request_data:
        token = request_data['id_token']
    else:
        makeResponse('no id_token', 401)
    try:
        verify_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='
        response = urlopen(verify_url+token)
        idinfo = json.loads(response.read())
        # verify the issuer
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        userid = idinfo['sub']
        # Verify app info
        if idinfo['aud'] != GOOGLE_CLIENT_ID:
            raise ValueError("The token ID does'nt match the apps's")
    except ValueError:
        # Invalid token
        pass
    # Store the access token in the session for later use.
    login_session['access_token'] = token
    login_session['provider_id'] = userid
    login_session['username'] = idinfo['name']
    login_session['email'] = idinfo['email']
    login_session['provider'] = 'google'
    # check if user exists, if it doesn't make a new one
    user_id = getUserID(idinfo["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    message = 'Success'
    print 'done! logged in with gaccount'
    return message


# Google disconnect 
def gsignout():
    # Only disconnect a connected user.
    print login_session['access_token']


# Disconnect based on provider
@app.route('/signout')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gsignout()
        if login_session['provider'] == 'facebook':
            fbsignout()
            del login_session['picture']
        del login_session['access_token']
        del login_session['provider_id']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']
        flash("You have been logged out.")
        return redirect(url_for('showSignin'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showUser'))


# Facebook
@app.route('/fbsignin', methods=['POST'])
def fbsignin():
    access_token = request.data
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (FACEBOOK_ID, FACEBOOK_SECRET, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['access_token'] = token
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['provider_id'] = data["id"]
    login_session['user_id'] = getSessionId(login_session)
    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    output = 'success'
    return output


def fbsignout():
    facebook_id = login_session['provider_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# User Helper Functions
def createUser(login_session):
    ''' register the user and return the user id'''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], provider=login_session['provider'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getSessionId(login_session):
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    return user_id


def makeResponse(message, status_code):
    response = make_response(json.dumps(message), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
