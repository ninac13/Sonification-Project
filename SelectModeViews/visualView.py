from flask import Blueprint, render_template_string, url_for

bp = Blueprint("visual", __name__, url_prefix="/visual")

@bp.route("/")
def index():
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Visual Analysis Group</title>
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
    <h1>Welcome to the Visual Analysis Group!</h1>
    <p>If you selected the wrong mode, click below to return:</p>
    <a href="{{ url_for('index') }}" class="button">← Back to Mode Selection</a>
  </div>

  <!-- Demo Placeholder Card -->
  <div class="container">
    <h1>DEMO ACTIVITY UNDER HERE</h1>
    <p>Ready to begin?</p>
<a href="{{ url_for('visual_demo.index') }}" class="button">
  START DEMO ACTIVITY
</a>  
  </div>

</body>
</html>
    """)