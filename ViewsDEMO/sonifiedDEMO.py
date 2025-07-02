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
      margin-bottom: 16px;
      font-size: 34px;
      color: #111;
    }
    p {
      color: #666;
      font-size: 18px;
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

    .audio-controls {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: 20px;
      justify-content: center;
    }

    .audio-controls button {
      font-size: 18px;
      padding: 10px 20px;
      border: none;
      background: #ccc;
      cursor: pointer;
      border-radius: 5px;
    }

    #progressBarContainer {
      position: relative;
      width: 100%;
      height: 20px;
      background: #ccc;
      border-radius: 5px;
      margin-top: 10px;
      overflow: hidden;
      cursor: pointer;
    }

    #progressBar {
      position: absolute;
      height: 100%;
      background: #007BFF;
      width: 0%;
    }

    .marker-bar {
      position: absolute;
      top: 0;
      height: 100%;
      width: 2px;
      background: red;
    }

    #markerButton {
      background-color: red;
      color: white;
      border: none;
      border-radius: 50%;
      width: 60px;
      height: 60px;
      font-weight: bold;
      font-size: 20px;
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
    <h1>Click 'Play' below to begin your Demo</h1>
    <p> When you hear a mutation (two notes playing at the same time) click the red button in order to mark where you have heard the mutation. Afterwards, click submit to see if you are correct!</p>

    <div class="audio-controls">
      <button id="playButton">Play</button>
      <span id="timeDisplay">0:00 / 0:00</span>
    </div>

    <div id="progressBarContainer">
      <div id="progressBar"></div>
      <div id="markerContainer"></div>
    </div>

    <!-- Marker Controls -->
    <button id="markerButton">10</button>
    <span id="markerLabel">/10 markers left</span>

    <!-- Speed Controls -->
    <div class="speed-controls">
      <label for="playbackRate">Speed:</label>
      <input type="range" id="playbackRate" min="0.5" max="2" step="0.1" value="1">
      <span id="rateDisplay">1x</span>
    </div>

    <audio id="dnaAudio" hidden>
      <source src="{{ url_for('static', filename='demo_sonification.wav') }}" type="audio/wav">
      Your browser does not support the audio element.
    </audio>
  </div>

  <div class="container">
    <h1>Finished with Demo?</h1>
    <p>When you’re ready, continue to the first trial:</p>
    <a href="{{ url_for('sonify_trial1.index') }}" class="button">
      Go to Sonification Trial 1
    </a>
  </div>

<script>
  const audio = document.getElementById("dnaAudio");
  const playButton = document.getElementById("playButton");
  const timeDisplay = document.getElementById("timeDisplay");
  const progressBar = document.getElementById("progressBar");
  const markerButton = document.getElementById("markerButton");
  const markerLabel = document.getElementById("markerLabel");
  const markerContainer = document.getElementById("markerContainer");
  const progressBarContainer = document.getElementById("progressBarContainer");

  const maxMarkers = 10;
  let remainingMarkers = maxMarkers;

  // Play/Pause functionality
  playButton.addEventListener("click", () => {
    if (audio.paused) {
      audio.play();
      playButton.textContent = "Pause";
    } else {
      audio.pause();
      playButton.textContent = "Play";
    }
  });

  // Update time and progress bar
  audio.addEventListener("timeupdate", () => {
    const current = audio.currentTime;
    const duration = audio.duration;
    if (!isNaN(duration)) {
      timeDisplay.textContent = `${formatTime(current)} / ${formatTime(duration)}`;
      const percent = (current / duration) * 100;
      progressBar.style.width = `${percent}%`;
    }
  });

  function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  // Marker logic
  markerButton.addEventListener("click", () => {
    if (remainingMarkers <= 0 || audio.paused || audio.currentTime === 0) return;

    const duration = audio.duration;
    const currentTime = audio.currentTime;
    const percent = (currentTime / duration) * 100;

    const marker = document.createElement("div");
    marker.className = "marker-bar";
    marker.style.left = `${percent}%`;
    markerContainer.appendChild(marker);

    remainingMarkers--;
    markerButton.textContent = remainingMarkers;
    markerLabel.textContent = `/10 markers left`;
  });

  // Speed control
  const slider = document.getElementById("playbackRate");
  const rateDisplay = document.getElementById("rateDisplay");

  slider.addEventListener("input", function () {
    const rate = parseFloat(this.value);
    audio.playbackRate = rate;
    rateDisplay.textContent = `${rate.toFixed(1)}x`;
  });

  // SEEKING via progress bar
  progressBarContainer.addEventListener("click", (event) => {
    const rect = progressBarContainer.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const percent = x / rect.width;
    const seekTime = audio.duration * percent;
    audio.currentTime = seekTime;
  });
  // Spacebar to play/pause
document.addEventListener("keydown", function (event) {
  if (event.code === "Space") {
    event.preventDefault(); // Prevent scrolling
    playButton.click();     // Simulate click on play button
  }
  });

</script>

</body>
</html>
""")






