import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('station', __name__, url_prefix='/station')

@bp.route('/station')
def station():
    login_required()
    db = get_db()
    station = db.execute(
            'SELECT * FROM station ORDER BY stop_order'
        ).fetchone()
    
    return render_template('station/station.html')

@bp.route('/create', methods=('GET', 'POST'))
def create():
    login_required()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        s_name = request.form['s_name']
        s_address=request.form['latitude']
        s_address=request.form['longitude']
        s_address=request.form['s_address']
        stop_order=request.form['stop_order']
        stop_kids=request.form['stop_kids']
        error = None

        # URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address={}'
        # response = requests.get(URL)
        # data = response.json()
        # latitude = data['results'][0]['geometry']['location']['lat']
        # longitude = data['results'][0]['geometry']['location']['lng']

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO station (s_name, latitude, longitude, s_address, stop_order, stop_kids)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (s_name, latitude, longitude, s_address, stop_order, stop_kids)
            )
            db.commit()
            return redirect(url_for('station.station'))

    return render_template('station/create.html')

def login_required():
        if g.user is None:
            return redirect(url_for('auth.login'))