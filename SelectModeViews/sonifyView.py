from flask import Blueprint, render_template_string, url_for

bp = Blueprint("sonify", __name__, url_prefix="/sonification")

@bp.route("/")
def index():
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sonified Analysis Group</title>
  <style>
    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      min-height: 100vh;
      margin: 0;
      padding-top: 40px;
    }
    .container {
      width: 80%;
      max-width: 600px;
      text-align: center;
      background: #fff;
      padding: 40px 60px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }
    h1 {
      margin-bottom: 24px;
      font-size: 28px;
      color: #333;
    }
    p {
      color: #555;
      margin-bottom: 16px;
    }
    .button {
      display: inline-block;
      margin-top: 16px;
      padding: 12px 24px;
      font-size: 16px;
      color: #fff;
      background-color: #007BFF;
      border: none;
      border-radius: 4px;
      text-decoration: none;
      transition: background-color .2s ease-in-out;
    }
    .button:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>
  <!-- Welcome Card -->
  <div class="container">
    <h1>Welcome to the Sonified Analysis Group!</h1>
    <p>If you selected the wrong mode, click below to return:</p>
    <a href="{{ url_for('index') }}" class="button">← Back to Mode Selection</a>
  </div>

  <!-- Demo Placeholder Card -->
  <div class="container">
    <h1>SONIFIED DEMONSTRATION ACTIVITY
                                  Read below before you begin</h1>
    <p> There are two DNA sequences that will be playing simultaneously. They will sound identical (You will hear one musical note playing at a time until you hear the mutation.) The mutation will sound like two distinct notes. Once you hear the mutation click the button to mark on the audio file that you have found the mutation. You can rewind the audio player by clicking on the point you want to rehear or dragging the playhead to where you want to rehear. For those who are on laptop can also use your spacebar to play or pause the audio. </p>
    <a href="{{ url_for('sonify_demo.index') }}" class="button">
      START DEMO ACTIVITY
    </a>
  </div>
</body>
</html>
    """)