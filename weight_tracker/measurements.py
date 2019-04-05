from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from weight_tracker.auth import login_required
from weight_tracker.db import get_db

bp = Blueprint('measurements', __name__)

@bp.route('/')
def index():
    db = get_db()
    if g.user:
        measurements = db.execute(
            'SELECT id, recorded, weight FROM weight_record'
            ' WHERE author_id = ?'
            ' ORDER BY recorded DESC', (g.user['id'], )
        ).fetchall()
    else:
        measurements = []
    return render_template('measurements/index.html', measurements=measurements)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        weight = request.form['weight']
        error = None

        if not weight:
            error = "Weight is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO weight_record (weight, author_id)'
                ' VALUES (?, ?)', (weight, g.user['id'])
            )
            db.commit()
            return redirect(url_for('measurements.index'))

    return render_template('measurements/create.html')

def get_measurement(id, check_author=True):
    measurement = get_db().execute(
        # TODO: Is this join really necessary?
        'SELECT id, recorded, weight, author_id FROM weight_record'
        ' WHERE id = ?',
        (id, )
    ).fetchone()

    if measurement is None:
        abort(404, "Measurement id {0} doesn't exist.".format(id))

    if check_author and measurement['author_id'] != g.user['id']:
        abort(403)

    return measurement

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    measurement = get_measurement(id)

    if request.method == "POST":
        weight = request.form['weight']
        error = None

        if not weight:
            error = "Weight is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE weight_record SET weight = ?'
                ' WHERE id = ?',
                (weight, id)
            )
            db.commit()
            return redirect(url_for('measurements.index'))

    return render_template('measurements/update.html', measurement=measurement)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_measurement(id)
    db = get_db()
    db.execute('DELETE FROM weight_record WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('measurements.index'))
