from flask import Blueprint, render_template_string, request, url_for

bp = Blueprint("sonify_demo_results", __name__, url_prefix="/sonify/demo/results")

@bp.route("", methods=["GET"])
def show_results():
    elapsed_ms   = request.args.get("t", type=int, default=0)
    used_markers = request.args.get("m", type=int, default=0)
    accuracy     = request.args.get("acc", type=int, default=0)  # markers within ±2s of 11s
    participant  = request.args.get("p", "Unknown")


    # Format time: MM:SS:MS
    minutes = elapsed_ms // 60000
    seconds = (elapsed_ms % 60000) // 1000
    millis  = elapsed_ms % 1000
    formatted = f"{minutes:02d}:{seconds:02d}:{millis:03d}"

    misplaced = used_markers - accuracy

    return render_template_string ("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sonification Demo Results</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #eef2f7;
      color: #333;
      margin: 0;
      padding: 2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1.5rem;
    }
    .card {
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      padding: 2rem;
      text-align: center;
      max-width: 600px;
      width: 100%;
    }
    h1 {
      font-size: 1.75rem;
      margin-bottom: 1rem;
      color: #007BFF;
    }
    .time {
      font-family: 'Courier New', Courier, monospace;
      font-size: 2rem;
      color: #0056b3;
      margin-bottom: 0.5rem;
    }
    p {
      font-size: 1rem;
      margin: 0.5rem 0;
    }
    a.button {
      display: inline-block;
      padding: 0.75rem 1.5rem;
      background: #007BFF;
      color: #fff;
      text-decoration: none;
      border-radius: 6px;
      font-weight: 500;
      transition: background 0.2s;
    }
    a.button:hover {
      background: #0056b3;
    }
  </style>
</head>
<body>
  <!-- Card 1: Time & Marker Summary -->
  <div class="card">
    <h1>Sonification Demo Results:</h1>
    <p class="time">Time Taken: {{ formatted }}</p>
    <p>(Minutes : Seconds : Milliseconds)</p>
    {% if used_markers == 1 %}
      <p class="time">You used 1 marker.</p>
    {% else %}
      <p class="time">You used <strong>{{ used_markers }}</strong> markers.</p>
    {% endif %}
    <p class="time">
      Mutations found: <strong>{{ accuracy }}/1</strong>
    </p>
    <p class="time">Misplaced markers: <strong>{{ misplaced }}/{{used_markers}}</strong></p>
  </div>

  <!-- Card 2: Guidance -->
  <div class="card">
    <h2>Please read before moving on to Trial 1:</h2>
    <p>These results are <strong>ONLY</strong> shown for the demonstration activity so you know what to look for when analyzing DNA sequences in the actual trials.</p></br>
    <p>Following completion of each respective trial, <strong>results will not be shown</strong> and each trial will be directly followed by the next.</p>
  </div>

  <!-- Card 3: Navigation -->
  <div class="card">
    <a href="{{ url_for('sonify_trial1.index') }}?p={{ participant }}" class="button">
    Proceed to Trial 1 →
    </a>

  </div>
</body>
</html>
""",
    formatted=formatted,
    used_markers=used_markers,
    accuracy=accuracy,
    misplaced=misplaced,
    participant=participant

)

