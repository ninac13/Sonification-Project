from flask import Blueprint, render_template_string, request, redirect, url_for

bp = Blueprint('participant_info', __name__, url_prefix='/participant_info')

# inline HTML + JS + CSS
_FORM_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to our DNA Analysis Study!</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #eef2f7;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    .card {
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.1);
      padding: 2rem;
      max-width: 480px;
      width: 100%;
      animation: fadeIn 0.6s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    h1 {
      margin-bottom: 1rem;
      font-size: 1.75rem;
      color: #333;
      text-align: center;
    }
    label {
      display: block;
      margin-top: 1rem;
      font-weight: 500;
      color: #555;
    }
    input, select {
      width: 100%;
      padding: 0.75rem;
      margin-top: 0.5rem;
      border: 1px solid #ccd0d5;
      border-radius: 6px;
      font-size: 1rem;
      transition: border-color 0.2s;
    }
    input:focus, select:focus {
      outline: none;
      border-color: #6c8efb;
      box-shadow: 0 0 0 3px rgba(108,142,251,0.2);
    }
    .btn-primary {
      display: block;
      width: 100%;
      padding: 0.75rem;
      margin-top: 1.5rem;
      background: #6c8efb;
      color: #fff;
      font-size: 1rem;
      font-weight: 600;
      text-align: center;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      transition: background 0.2s;
    }
    .btn-primary:hover {
      background: #5a7ddb;
    }
    /* modal styles */
    .modal-backdrop {
      display: none;
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0,0,0,0.6);
      justify-content: center;
      align-items: center;
    }
    .modal {
      background: #fff;
      padding: 1.5rem;
      border-radius: 8px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.2);
      max-width: 400px;
      width: 90%;
      text-align: center;
      animation: popIn 0.3s ease-out;
    }
    @keyframes popIn {
      from { transform: scale(0.95); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }
    .modal h2 {
      margin-top: 0;
      color: #333;
    }
    .modal p {
      color: #555;
      margin: 1rem 0;
    }
    .modal .btn {
      padding: 0.75rem 1.25rem;
      border: none;
      border-radius: 6px;
      font-size: 0.9rem;
      cursor: pointer;
      margin: 0.5rem;
    }
    .btn-confirm {
      background: #77DD77;
    }
    .btn-cancel {
      background: #FF6961;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Welcome to our DNA Analysis Study!</h1>
    <form id="participantForm" method="post">
      <label for="participant_number">Your Participant #</label>
      <input type="text" id="participant_number" name="participant_number" placeholder="e.g. 1" required>

      <label for="age">Your Age</label>
      <input type="number" id="age" name="age" placeholder="e.g. 13" required>

      <label for="day">Today's Date</label>
      <input type="date" id="day" name="day" required>
      
      <label for="type">Are you a student or teacher?</label>
      <select id="type" name="type" required>
        <option value="" disabled selected>Select...</option>
        <option value="student">Student</option>
        <option value="teacher">Teacher</option>
      </select>

      <label for="group">Group</label>
      <select id="group" name="group" required>
        <option value="" disabled selected>Select group...</option>
        <option value="sonification">Sonification</option>
        <option value="visual">Visual</option>
      </select>

      <button type="button" id="submitBtn" class="btn-primary">Submit</button>
    </form>
  </div>

  <div class="modal-backdrop" id="confirmBackdrop">
    <div class="modal">
      <h2>Please confirm your info</h2>
      <p>Make sure the following information is correct:</p>
      <ul style="text-align:left; padding-left:1.2rem;">
        <li><strong>Participant #:</strong> <span id="confirmParticipant"></span></li>
        <li><strong>Age:</strong> <span id="confirmAge"></span></li>
        <li><strong>Date:</strong> <span id="confirmDay"></span></li>
        <li><strong>Type:</strong> <span id="confirmType"></span></li>
        <li><strong>Group:</strong> <span id="confirmGroup"></span></li>
      </ul>
      <button id="yesBtn" class="btn btn-confirm">Yes, it&#39;s correct</button>
      <button id="noBtn" class="btn btn-cancel">No, let me edit</button>
    </div>
  </div>

  <script>
    const form = document.getElementById('participantForm');
    const submitBtn = document.getElementById('submitBtn');
    const backdrop = document.getElementById('confirmBackdrop');
    const yesBtn = document.getElementById('yesBtn');
    const noBtn = document.getElementById('noBtn');
    const fields = {
      participant: document.getElementById('participant_number'),
      age: document.getElementById('age'),
      day: document.getElementById('day'),
      type: document.getElementById('type'),
      group: document.getElementById('group')
    };
    const confirmSpans = {
      participant: document.getElementById('confirmParticipant'),
      age: document.getElementById('confirmAge'),
      day: document.getElementById('confirmDay'),
      type: document.getElementById('confirmType'),
      group: document.getElementById('confirmGroup')
    };

    submitBtn.addEventListener('click', () => {
      confirmSpans.participant.textContent = fields.participant.value;
      confirmSpans.age.textContent = fields.age.value;
      confirmSpans.day.textContent = fields.day.value;
      confirmSpans.type.textContent = fields.type.value.charAt(0).toUpperCase() + fields.type.value.slice(1);
      confirmSpans.group.textContent = fields.group.value.charAt(0).toUpperCase() + fields.group.value.slice(1);
      backdrop.style.display = 'flex';
    });

    yesBtn.addEventListener('click', () => {
      backdrop.style.display = 'none';
      form.submit();
    });

    noBtn.addEventListener('click', () => {
      backdrop.style.display = 'none';
    });
  </script>
</body>
</html>
"""

@bp.route('/', methods=['GET', 'POST'])
def participant_info():
    if request.method == 'POST':
        participant_number = request.form['participant_number']
        age                = request.form['age']
        day                = request.form['day']
        p_type             = request.form['type']
        group              = request.form['group']

        print(f"Participant: {participant_number}, Age: {age}, Date: {day}, Type: {p_type}, Group: {group}")

        if group == 'sonification':
            return redirect(url_for('sonify.index', participant=participant_number))
        elif group == 'visual':
            return redirect(url_for('visual.index', participant=participant_number))
        else:
            return redirect(url_for('participant_info.participant_info'))

    return render_template_string(_FORM_HTML)
