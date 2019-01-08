from flask import Flask, jsonify
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import urllib.parse as urlparse
from urllib.parse import urlencode
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'

@app.route('/')
def home():
    session['redirect_uri'] = request.args.get('redirect_uri')
    session['state'] = request.args.get('state')
    return render_template('login.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    return redirect(session['redirect_uri']+'#state='+session['state']+'&access_token='+request.form['password']
    +"*"+request.form['username']+'&token_type=Bearer', code = 303)
 
def process_redirect_url(redirect_url, new_entries):
    url_parts = list(urlparse.urlparse(redirect_url))
    queries = dict(urlparse.parse_qsl(url_parts[4]))
    queries.update(new_entries)
    url_parts[4] = urlencode(queries)
    url = urlparse.urlunparse(url_parts)
    return url

if __name__ == "__main__":
    app.run(debug=True)
