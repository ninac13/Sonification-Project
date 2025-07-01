# THIS WILL BE THE SAME SCREEN THAT SHOWS UP FOR BOTH VISUAL AND SONIFIED PARTICIPANTS
from flask import Blueprint, render_template_string, url_for

bp = Blueprint("finished_view", __name__, url_prefix="/finished")

@bp.route("/", methods=("GET",))
def index():
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>All Done!</title>
  <style>
    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f0f4f8;
      color: #333;
    }
    .card {
      background: #fff;
      padding: 40px 50px;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.1);
      text-align: center;
      max-width: 600px;
      width: 90%;
    }
    h1 {
      font-size: 2.5rem;
      color: #007BFF;
      margin-bottom: 20px;
    }
    p {
      font-size: 1.1rem;
      line-height: 1.6;
      margin-bottom: 30px;
    }
    .button {
      display: inline-block;
      padding: 14px 28px;
      font-size: 1rem;
      color: #fff;
      background: #007BFF;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      text-decoration: none;
      transition: background 0.2s, transform 0.1s;
    }
    .button:hover {
      background: #0056b3;
      transform: translateY(-2px);
    }
    .button + .button {
      margin-left: 12px;
      background: #6c757d;
    }
    .button + .button:hover {
      background: #5a6268;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>All Done!</h1>
    <p>You've completed the final trial.</p>
    <p>Thank you for participating in our study!</p>
    <p><strong>DO NOT EXIT</strong> your screen yet.</p>
    <p>Please show this finished screen to either Lea or Nina. When you have done so, you are free to exit this program and leave!</p>
  </div>
</body>
</html>
    """)
