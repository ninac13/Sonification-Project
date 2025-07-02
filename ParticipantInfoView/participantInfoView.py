from flask import Blueprint, render_template, request, redirect, url_for, session

bp = Blueprint('participant_info_bp', __name__)

@bp.route('/', methods=['GET', 'POST'])
def participant_info():
    if request.method == 'POST':
        session['participant_number'] = request.form['participant_number']
        session['age'] = request.form['age']
        session['experimental_day'] = request.form['experimental_day']
        session['group'] = request.form['group']
        return redirect(url_for('sonify_bp.index'))  # Or 'visual_bp.index' if that's the next view

    return render_template('participant_info.html')


