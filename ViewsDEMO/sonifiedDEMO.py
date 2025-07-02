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
<style>
  .audio-wrapper {
    position: relative;
    width: fit-content;
    margin-top: 20px;
  }
  .audio-wrapper audio {
  width: 100%;
  }


  #markerOverlay {
    position: absolute;
    top: -20px; /* place above audio bar */
    left: 0;
    width: 100%;
    height: 20px;
    pointer-events: none;
  }

 .marker {
  position: absolute;
  top: 100%; /* below the audio bar */
  color: red;
  font-size: 18px;
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
</style>

<!-- Audio and overlay container -->
<div class="audio-wrapper">
  <audio id="dnaAudio" controls style="width: 100%;">
    <source src="{{ url_for('static', filename='demo_sonification.wav') }}" type="audio/wav">
    Your browser does not support the audio element.
  </audio>

  <!-- Overlay for markers -->
  <div id="markerOverlay"></div>
</div>

<!-- Marker Button -->
<button id="markerButton" title="Click to drop marker">10</button>
<span id="markerLabel">/10 markers left</span>

<script>
  const audio = document.getElementById("dnaAudio");
  const markerButton = document.getElementById("markerButton");
  const markerLabel = document.getElementById("markerLabel");
  const markerOverlay = document.getElementById("markerOverlay");

  const maxMarkers = 10;
  let remainingMarkers = maxMarkers;

  markerButton.addEventListener("click", () => {
    if (remainingMarkers <= 0 || audio.currentTime === 0 || audio.paused) return;

    const currentTime = audio.currentTime;
    const duration = audio.duration;

    const audioRect = audio.getBoundingClientRect();
    const overlayRect = markerOverlay.getBoundingClientRect();

    const percentage = currentTime / duration;
    const overlayWidth = overlayRect.width;
    const leftPosition = percentage * overlayWidth;

    const marker = document.createElement("div");
    marker.classList.add("marker");
    marker.textContent = "↓"; // Down arrow
    marker.style.left = `${leftPosition}px`;

    markerOverlay.appendChild(marker);

    remainingMarkers--;
    markerButton.textContent = remainingMarkers;
    markerLabel.textContent = `/10 markers left`;
  });
</script>



<!-- Speed Control Slider -->
<label for="playbackRate">Speed:</label>
<input type="range" id="playbackRate" min="0.5" max="2" step="0.1" value="1">
<span id="rateDisplay">1x</span>

<script>
  const audio = document.getElementById("dnaAudio");
  const slider = document.getElementById("playbackRate");
  const rateDisplay = document.getElementById("rateDisplay");

  slider.addEventListener("input", function () {
    const rate = parseFloat(this.value);
    audio.playbackRate = rate;
    rateDisplay.textContent = `${rate.toFixed(1)}x`;
  });
</script>
                        

                         
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