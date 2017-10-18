from flask import Flask, render_template, request, make_response
from flask import session as login_session
import random
import string
import httplib2
import json
from datetime import datetime


app = Flask(__name__)

# Create anti-forgery state token
@app.route('/login-test')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    # state = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    login_session['state'] = state
    return render_template('login-test.html', STATE=state)


@app.route('/connect-test', methods=['POST'])
def fbconnect():
    state_original = login_session['state']
    state_sent = request.args.get('state') 
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter. It should be %s, but you sent %s'
                   % (state_original, state_sent)), 401)
        response.headers['Content-Type'] = 'application/json'
    else:
        response = 'success' 
    return response

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

