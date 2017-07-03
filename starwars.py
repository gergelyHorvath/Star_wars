import data_manager
import requests
import json
import os
from flask import Flask, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = '1p2o3I5j R,.cZ5!Q91%A $X'


@app.before_request
def guest_session():
    try:
        session['username']
    except KeyError:
        session['username'] = ''


@app.route('/')
def index():
    return redirect('/swplanets?page=1')


@app.route('/swplanets', methods=['GET', 'POST'])
def listpage():
    page = request.args['page']
    req = requests.get('http://swapi.co/api/planets?page={}'.format(page))
    data = json.loads(req.text)['results']
    relevant_data = [{
        'name': planet['name'],
        'diameter': planet['diameter'] + (' km' if planet['diameter'] != 'unknown' else ''),
        'climate': planet['climate'],
        'terrain': planet['terrain'],
        'surface_water': planet['surface_water'] + (' %' if planet['surface_water'] != 'unknown' else ''),
        'population': planet['population'] + (' people' if planet['population'] != 'unknown' else ''),
        'residents': planet['residents']
    } for planet in data]
    return render_template('listpage.html', planets=relevant_data, page=int(page))


@app.route('/login')
def login_render():
    returned = True if request.args['mode'] == 'incorrect' else False
    return render_template('login.html', returned=returned, task='login')


@app.route('/login_check', methods=['POST'])
def login_check():
    users = data_manager.get_users()
    for user in users:
        if user[1] == request.form['username'] and check_password_hash(user[2], request.form['password']):
            session['username'] = request.form['username']
            session['user_id'] = user[0]
            return redirect('/')
    return redirect('/login?mode=incorrect')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect('/')


@app.route('/register')
def register():
    returned = True if request.args['mode'] == 'incorrect' else False
    return render_template('login.html', returned=returned, task='register')


@app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    password = generate_password_hash(request.form['password'], 'sha256')
    users = data_manager.get_users()
    usernames = [u[1] for u in users]
    if username in usernames:
        return redirect('/register?mode=incorrect')
    else:
        data_manager.add_user(username, password)
        return redirect('/')


if __name__ == ('__main__'):
    app.run()
