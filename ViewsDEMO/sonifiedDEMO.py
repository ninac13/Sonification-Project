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

    .audio-wrapper {
      position: relative;
      width: 100%;
      margin-top: 20px;
    }

    #customAudioControls {
      width: 100%;
    }

    #progressContainer {
      position: relative;
      width: 100%;
      height: 20px;
      background: #ddd;
      margin-top: 10px;
      border-radius: 4px;
      overflow: hidden;
    }

    #progressBar {
      height: 100%;
      width: 0;
      background: #007BFF;
    }

    #markerOverlay {
      position: absolute;
      top: -30px;
      left: 0;
      height: 20px;
      width: 100%;
      pointer-events: none;
    }

    .marker {
      position: absolute;
      color: red;
      font-size: 24px;
      transform: translateX(-50%);
    }

    #markerButton {
      background-color: red;
      color: white;
      border: none;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      font-weight: bold;
      font-size: 14px;
      cursor: pointer;
      margin-top: 20px;
    }

    .speed-controls {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: 10px;
    }

    .speed-controls label {
      margin-right: 10px;
    }

    .speed-controls input[type=range] {
      width: 150px;
      margin: 0 10px;
    }
  </style>
</head>
<body>

  <div class="container">
    <h1>Click below to Begin your Demo</h1>
    <p>There are two DNA sequences that will be playing simultaneously. They will sound identical (You will hear one musical note playing at a time until you hear the mutation.) The mutation will sound like two distinct notes. Once you hear the mutation click the button to mark on the audio file that you have found the mutation.</p>

    <div class="audio-wrapper">
      <audio id="dnaAudio">
        <source src="{{ url_for('static', filename='demo_sonification.wav') }}" type="audio/wav">
        Your browser does not support the audio element.
      </audio>

      <!-- Custom controls -->
      <div id="customAudioControls">
        <button onclick="togglePlay()">▶️/⏸️</button>
        <div id="progressContainer" onclick="seek(event)">
          <div id="progressBar"></div>
          <div id="markerOverlay"></div>
        </div>
      </div>
    </div>

    <!-- Marker Controls -->
    <button id="markerButton" title="Click to drop marker">10</button>
    <span id="markerLabel">/10 markers left</span>

    <!-- Speed Controls -->
    <div class="speed-controls">
      <label for="playbackRate">Speed:</label>
      <input type="range" id="playbackRate" min="0.5" max="2" step="0.1" value="1">
      <span id="rateDisplay">1x</span>
    </div>
  </div>

  <!-- Finished with Demo Card -->
  <div class="container">
    <h1>Finished with Demo?</h1>
    <p>When you’re ready, continue to the first trial:</p>
    <a href="{{ url_for('sonify_trial1.index') }}" class="button">
      Go to Sonification Trial 1
    </a>
  </div>

<script>
  const audio = document.getElementById("dnaAudio");
  const progressContainer = document.getElementById("progressContainer");
  const progressBar = document.getElementById("progressBar");
  const markerOverlay = document.getElementById("markerOverlay");
  const markerButton = document.getElementById("markerButton");
  const markerLabel = document.getElementById("markerLabel");

  const maxMarkers = 10;
  let remainingMarkers = maxMarkers;

  function togglePlay() {
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  }

  function seek(e) {
    const rect = progressContainer.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = x / rect.width;
    audio.currentTime = percentage * audio.duration;
  }

  audio.addEventListener("timeupdate", () => {
    const percentage = audio.currentTime / audio.duration;
    progressBar.style.width = percentage * 100 + "%";
  });

  markerButton.addEventListener("click", () => {
    if (remainingMarkers <= 0 || audio.paused || audio.currentTime === 0) return;

    const percentage = audio.currentTime / audio.duration;
    const markerX = percentage * progressContainer.offsetWidth;

    const marker = document.createElement("div");
    marker.classList.add("marker");
    marker.textContent = "↓";
    marker.style.left = markerX + "px";

    markerOverlay.appendChild(marker);

    remainingMarkers--;
    markerButton.textContent = remainingMarkers;
    markerLabel.textContent = "/10 markers left";
  });

  // Speed control
  const slider = document.getElementById("playbackRate");
  const rateDisplay = document.getElementById("rateDisplay");

  slider.addEventListener("input", function () {
    const rate = parseFloat(this.value);
    audio.playbackRate = rate;
    rateDisplay.textContent = `${rate.toFixed(1)}x`;
  });
</script>

</body>
</html>
""")

