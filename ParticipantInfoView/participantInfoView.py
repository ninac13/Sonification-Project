from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint('participant_info', __name__, url_prefix='/participant_info')

@bp.route('/', methods=['GET', 'POST'])
def participant_info():
    print("Rendering participant_info.html...")  # ✅ Add this line here

    if request.method == 'POST':
        participant_number = request.form.get('participant_number')
        age = request.form.get('age')
        day = request.form.get('day')
        group = request.form.get('group')
        print(f"Participant: {participant_number}, Age: {age}, Day: {day}, Group: {group}")
        return redirect(url_for('visual.index'))  # Or whatever route is next

    return render_template('participant_info.html')






