# Trial1Views/sonifyTrial1.py
from flask import Blueprint, render_template_string, url_for

bp = Blueprint("sonify_trial1", __name__, url_prefix="/sonification/trial1")

@bp.route("/")
def index():
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sonified Trial 1</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      min-height: 100vh;
      margin: 0;
      padding-top: 40px;
    }
    .container {
      background: #fff;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      text-align: center;
      max-width: 600px;
      width: 90%;
      margin-bottom: 20px;
    }
    h1 { margin-bottom: 24px; color: #333; }
    p  { color: #555; margin-bottom: 16px; }
    .button {
      display: inline-block;
      padding: 12px 24px;
      font-size: 16px;
      color: #fff;
      background: #007BFF;
      border: none;
      border-radius: 4px;
      text-decoration: none;
      transition: background .2s;
      margin: 8px;
    }
    .button:hover { background: #0056b3; }
  </style>
</head>
<body>
  <!-- Trial 1 Content -->
  <div class="container">
    <h1>Sonified Trial 1</h1>
    <p>This is where your first trial’s interface will go.</p>
  </div>

  <!-- Ready for Trial 2 -->
  <div class="container">
    <h1>Ready to Move to Trial 2?</h1>
    <p>When you’re set, click below to begin Trial 2.</p>
    <a href="{{ url_for('sonify_trial2.index') }}" class="button">
      Go to Sonification Trial 2 →
    </a>
  </div>
</body>
</html>
    """)