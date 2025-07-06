<<<<<<< Updated upstream
from flask import session
from flask import Blueprint, render_template_string, url_for, request
import time
import csv
import os

TRIAL_RESULTS_FILE = "trial_results.csv"
=======
from flask import Blueprint, render_template_string, url_for, request, redirect
import os
import csv
>>>>>>> Stashed changes

bp = Blueprint("sonify_trial1", __name__, url_prefix="/sonification/trial1")
TRIAL_RESULTS_FILE = "TrialResults/sonification_trial_results.csv"

@bp.route("/", methods=("GET", "POST"))
def index():
    participant = request.args.get("participant")

<<<<<<< Updated upstream
    if participant:
        session['participant_id'] = participant
    else:
        participant = session.get('participant_id')

    if not participant:
        return "Participant ID missing", 400
=======
    if request.method == "POST":
        markers = request.form.get("markers", "")
        timestr = request.form.get("timeTaken", "0")
        try:
            marker_times = [float(m) for m in markers.split(",") if m]
        except:
            marker_times = []
        time_taken = float(timestr)

        mutation_intervals = [
            (5,9), (61,65), (91,95), (125,129),
            (187,191), (247,251), (271,275)
        ]
        correct = sum(any(start <= t <= end for (start,end) in mutation_intervals)
                      for t in marker_times)
        misplaced = len(marker_times) - correct

        os.makedirs("TrialResults", exist_ok=True)
        exists = os.path.isfile(TRIAL_RESULTS_FILE)
        with open(TRIAL_RESULTS_FILE, "a", newline="") as f:
            w = csv.writer(f)
            if not exists:
                w.writerow(["Participant","Trial","TimeTaken","MarkersUsed","MutationsFound","MisplacedMarkers"])
            w.writerow([participant, "1",
                        f"{int(time_taken//60)}:{int(time_taken%60):02}",
                        len(marker_times), correct, misplaced])

        return redirect(url_for("sonify_trial2.index", participant=participant))
>>>>>>> Stashed changes

    return render_template_string("""
    ...
    """, participant=participant)
("""
<!doctype html>
<html lang="en">
<head>
 <meta charset="utf-8">
 <title>Sonified Trial 1</title>
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
     cursor: pointer;
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
   <h1>Sonified Trial 1</h1>
   <p>When you hear a mutation (two notes playing at the same time) click the red button in order to mark where you have heard the mutation. However, you will NOT be told how many mutations there are and whether you got them correct. There are ten markers provided and you may use all or none of them. Only place the markers appropriately when you hear a mutation. </p>

   <div class="audio-controls">
     <button id="playButton">Play</button>
     <span id="timeDisplay">0:00 / 0:00</span>
   </div>

   <div id="progressBarContainer">
     <div id="progressBar"></div>
     <div id="markerContainer"></div>
   </div>

   <button id="markerButton">10</button>
   <span id="markerLabel">/10 markers left</span>

   <div class="speed-controls">
     <label for="playbackRate">Speed:</label>
     <input type="range" id="playbackRate" min="0.5" max="2" step="0.1" value="1">
     <span id="rateDisplay">1x</span>
   </div>

   <audio id="dnaAudio" hidden>
     <source src="{{ url_for('static', filename='trial1_sonification.wav') }}" type="audio/wav">
     Your browser does not support the audio element.
   </audio>
 </div>

<<<<<<< Updated upstream
  <div class="container">
    <h1>Ready to Move to Trial 2?</h1>
    <p>When you’re set, click below to begin Trial 2.</p>
    <a href="{{ url_for('sonify_trial2.index') }}?participant={{ participant }}" class="button" id="goToTrial2">Go to Sonification Trial 2 →</a>
  </div>
  <input type="hidden" id="participant-id" value="{{ participant }}">

=======
 <div class="container">
   <h1>Ready to Move to Trial 2?</h1>
   <p>When you’re set, click below to begin Trial 2.</p>
   <a href="#" class="button" id="submitButton">Go to Sonification Trial 2 →</a>
 </div>
>>>>>>> Stashed changes

<script>
 const audio = document.getElementById("dnaAudio");
 const playButton = document.getElementById("playButton");
 const timeDisplay = document.getElementById("timeDisplay");
 const progressBar = document.getElementById("progressBar");
 const markerButton = document.getElementById("markerButton");
 const markerLabel = document.getElementById("markerLabel");
 const markerContainer = document.getElementById("markerContainer");
 const progressBarContainer = document.getElementById("progressBarContainer");
 const rateSlider = document.getElementById("playbackRate");
 const rateDisplay = document.getElementById("rateDisplay");
 const submitButton = document.getElementById("submitButton");

 const maxMarkers = 10;
 let remainingMarkers = maxMarkers;
 let markers = [];
 let started = false;
 let startTime = 0;

<<<<<<< Updated upstream
  const placedMarkers = [];
  let firstPlayTime = null;
  let trialStartTime = null;

  playButton.addEventListener("click", () => {
    if (!firstPlayTime) {
      firstPlayTime = new Date();
      trialStartTime = audio.currentTime;
    }

    if (audio.paused) {
      audio.play();
      playButton.textContent = "Pause";
    } else {
      audio.pause();
      playButton.textContent = "Play";
    }
  });
=======
 function formatTime(seconds) {
   const m = Math.floor(seconds / 60);
   const s = Math.floor(seconds % 60);
   return m + ":" + (s < 10 ? "0" : "") + s;
 }
>>>>>>> Stashed changes

 audio.addEventListener("loadedmetadata", () => {
   timeDisplay.textContent = "0:00 / " + formatTime(audio.duration);
 });

 audio.addEventListener("timeupdate", () => {
   const pct = (audio.currentTime / audio.duration) * 100;
   progressBar.style.width = pct + "%";
   timeDisplay.textContent = formatTime(audio.currentTime) + " / " + formatTime(audio.duration);
 });

 playButton.addEventListener("click", () => {
   if (!started) {
     started = true;
     startTime = Date.now();
   }
   if (audio.paused) {
     audio.play();
     playButton.textContent = "Pause";
   } else {
     audio.pause();
     playButton.textContent = "Play";
   }
 });

 rateSlider.addEventListener("input", () => {
   audio.playbackRate = parseFloat(rateSlider.value);
   rateDisplay.textContent = rateSlider.value + "x";
 });

 progressBarContainer.addEventListener("click", e => {
   const rect = progressBarContainer.getBoundingClientRect();
   const pct = (e.clientX - rect.left) / rect.width;
   audio.currentTime = pct * audio.duration;
 });

 markerButton.addEventListener("click", () => {
   if (remainingMarkers > 0) {
     const t = audio.currentTime;
     markers.push(t);
     const bar = document.createElement("div");
     bar.className = "marker-bar";
     bar.style.left = (t / audio.duration) * 100 + "%";
     bar.title = formatTime(t);
     markerContainer.appendChild(bar);
     remainingMarkers -= 1;
     markerButton.textContent = remainingMarkers;
     markerLabel.textContent = "/10 markers left";
   }
 });

<<<<<<< Updated upstream
    markerContainer.appendChild(marker);
    placedMarkers.push(currentTime);
    remainingMarkers--;
    markerButton.textContent = remainingMarkers;
    markerLabel.textContent = `/10 markers left`;
  });

  const slider = document.getElementById("playbackRate");
  const rateDisplay = document.getElementById("rateDisplay");

  slider.addEventListener("input", function () {
    const rate = parseFloat(this.value);
    audio.playbackRate = rate;
    rateDisplay.textContent = `${rate.toFixed(1)}x`;
  });

  progressBarContainer.addEventListener("click", (event) => {
    const rect = progressBarContainer.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const percent = x / rect.width;
    const seekTime = audio.duration * percent;
    audio.currentTime = seekTime;
  });

  document.addEventListener("keydown", function (event) {
    if (event.code === "Space") {
      event.preventDefault();
      playButton.click();
    }
  });

  document.getElementById("goToTrial2").addEventListener("click", async (e) => {
    e.preventDefault();

    if (!firstPlayTime) {
      alert("Please play the audio at least once before continuing.");
      return;
    }

    const trialEndTime = new Date();
    const elapsed = (trialEndTime - firstPlayTime) / 1000;

    let participant = null;

    const urlParams = new URLSearchParams(window.location.search);
    participant = urlParams.get("participant");

    if (!participant) {
      const hiddenInput = document.getElementById("participant-id");
      if (hiddenInput) {
        participant = hiddenInput.value;
      }
    }

    if (!participant) {
      alert("Participant ID missing. Cannot submit results.");
      return;
    }

    await fetch("/sonification/trial1/submit_trial1", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        participant: participant,
        markers: placedMarkers,
        elapsed: elapsed
      })
    });

    window.location.href = e.target.href;
  });
=======
 submitButton.addEventListener("click", () => {
   const elapsed = (Date.now() - startTime) / 1000;
   const form = document.createElement("form");
   form.method = "POST";
   form.action = window.location.href;
   form.append(Object.assign(document.createElement("input"), {
     type: "hidden", name: "markers", value: markers.join(",")
   }));
   form.append(Object.assign(document.createElement("input"), {
     type: "hidden", name: "timeTaken", value: elapsed
   }));
   document.body.appendChild(form);
   form.submit();
 });
>>>>>>> Stashed changes
</script>
</body>
</html>
<<<<<<< Updated upstream
""")

@bp.route('/submit_trial1', methods=["POST"])
def submit_trial1():
    data = request.get_json()
    participant = data.get("participant")
    markers = data.get("markers", [])
    elapsed = data.get("elapsed", 0)

    mutation_windows = [
        (5, 9), (61, 65), (91, 95),
        (125, 129), (187, 191), (247, 251), (271, 275)
    ]

    correct = 0
    used_windows = set()

    for m in markers:
        for i, (start, end) in enumerate(mutation_windows):
            if i in used_windows:
                continue
            if start <= m <= end:
                correct += 1
                used_windows.add(i)
                break

    misplaced = len(markers) - correct

    file_path = "TrialResults/sonification_trial_results.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "Participant", "Trial", "Total Markers",
                "MutationsFound", "MisplacedMarkers", "TimeTaken"
            ])
        writer.writerow([
            participant, 1, len(markers),
            correct, misplaced, round(elapsed, 2)
        ])

    return {"success": True}

=======
""", participant=participant)
>>>>>>> Stashed changes

