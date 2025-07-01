from flask import Blueprint, render_template_string, url_for

bp = Blueprint("sonify_demo", __name__, url_prefix="/sonification/demo")

@bp.route("/")
def index():
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sonified Demo Activity</title>
  <style>
    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      padding: 20px;
    }
    .container {
      width: 100%;
      max-width: 600px;
      text-align: center;
      background: #fff;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }
    h1 {
      margin-bottom: 24px;
      font-size: 24px;
      color: #333;
    }
    p {
      color: #555;
      margin-bottom: 16px;
    }
    .button {
      display: inline-block;
      margin-top: 20px;
      padding: 10px 20px;
      font-size: 16px;
      color: #fff;
      background: #007BFF;
      border: none;
      border-radius: 4px;
      text-decoration: none;
      transition: background-color .2s ease-in-out;
    }
    .button:hover {
      background: #0056b3;
    }
  </style>
</head>
<body>
  <!-- Sonified Demo Content Card -->
  <div class="container">
    <h1>Click below to Begin your Demo</h1>
    <p>There are two DNA sequneces that will be playing simultaneously. They will sound identical (You will hear one musical note playing at a time until you hear the mutation.) The mutation will sound like two distinct notes. Once you hear the mutation click the button to mark on the audio file that you have found the mutation. </p>
    <audio controls>
  <source src="{{ url_for('static', filename='demo_sonification.wav') }}" type="audio/wav">
  Your browser does not support the audio element.
</audio>
  </div>

  <!-- Finished with Demo Card -->
  <div class="container">
    <h1>Finished with Demo?</h1>
    <p>When you’re ready, continue to the first trial:</p>
    <a href="{{ url_for('sonify_trial1.index') }}" class="button">
      Go to Sonification Trial 1
    </a>
  </div>
</body>
</html>
    """)