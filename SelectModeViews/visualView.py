from flask import Blueprint, render_template_string, request, url_for

bp = Blueprint("visual", __name__, url_prefix="/visual")

@bp.route("/")
def index():
    participant = request.args.get("participant", None)
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Visual Analysis Group</title>
  <style>
    body {
      margin-top: 2.5rem; /* increased top spacing */
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #e0e7ff;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }
    .participant-badge {
      margin-top: 0.5rem;
      background: #6366f1;
      color: #fff;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-weight: 500;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
      display: inline-block;
    }
    main {
      flex: 1;
      width: 100%;
      max-width: 640px;
      padding: 2rem 1rem;
      box-sizing: border-box;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      margin-bottom: 1.5rem;
      padding: 2rem;
      text-align: center;
    }
    .card h2 {
      margin-top: 0;
      color: #4f46e5;
      font-size: 1.5rem;
    }
    .card p {
      color: #4b5563;
      line-height: 1.6;
      margin: 1rem 0;
    }
    .button {
      display: inline-block;
      margin-top: 1rem;
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      font-weight: 600;
      color: #fff;
      background: #4f46e5;
      border: none;
      border-radius: 8px;
      text-decoration: none;
      transition: background 0.2s;
    }
    .button:hover {
      background: #4338ca;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Visual Analysis Group</h1>
    {% if participant %}
      <div class="participant-badge">Participant {{ participant }}</div>
    {% endif %}
  </div>
  <main>
    <div class="card">
      <h2>Demonstration Activity</h2>
      <p><strong>Ready to begin? Click below to start the guided demo.</strong></p>
      <a href="{{ url_for('visual_demo.index') }}?participant={{ participant }}" class="button">Start Demo &rarr;</a>
    </div>
  </main>
</body>
</html>
    """, participant=participant)
