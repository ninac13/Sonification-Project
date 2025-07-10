from flask import Blueprint, render_template_string, request, url_for, redirect
from Bio import SeqIO
import os
import time
import csv

TRIAL_RESULTS_FILE = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "TrialResults", "visual_trial_results.csv"
)

bp = Blueprint("visual_trial3", __name__, url_prefix="/visual/trial3")

# Path to your FASTA file inside sonification/data_visual/
SET3_FASTA = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "sonification", "data_visual", "set3.fasta"
)

@bp.route("/", methods=("GET", "POST"))
def index():
    participant = request.args.get("participant")
    if not participant:
        return "Error: Missing participant ID in URL.", 400
    def format_time(ms):
      total_ms = int(ms)
      minutes = total_ms // 60000
      seconds = (total_ms % 60000) // 1000
      millis = total_ms % 1000
      return f"{minutes:02}:{seconds:02}:{millis:03}"

    if request.method == "POST":
        raw_time = request.form.get("time_taken")
        time_taken = format_time(raw_time)
        markers_used = request.form.get("markers_used")
        mutations_found = request.form.get("mutations_found")

        if time_taken and markers_used and mutations_found is not None:
            misplaced = int(markers_used) - int(mutations_found)
            records = {rec.id: str(rec.seq) for rec in SeqIO.parse(SET3_FASTA, "fasta")}
            nonmut = records["trial3_original"]
            mut    = records["trial3_mutated"]

            file_exists = os.path.isfile(TRIAL_RESULTS_FILE)
            with open(TRIAL_RESULTS_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Participant", "Trial", "TimeTaken", "MarkersUsed", "MutationsFound", "MisplacedMarkers"])
                writer.writerow([participant, 3, time_taken, markers_used, mutations_found, misplaced])

            return redirect(url_for("finished_view.index", participant=participant))

        return "Error: Missing form data", 400

    records = {rec.id: str(rec.seq) for rec in SeqIO.parse(SET3_FASTA, "fasta")}
    nonmut = records["trial3_original"]
    mut    = records["trial3_mutated"]
    mutation_indexes = [i for i, (a, b) in enumerate(zip(nonmut, mut)) if a != b]

    return render_template_string("""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>Visual Trial 3</title>
      <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; margin: 0; display: flex; flex-direction: column; align-items: center; }
        .container { background: #fff; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 90%; max-width: 800px; text-align: center; }
        .label { font-weight: bold; color: #333; display: block; margin-top: 10px; }
        #nonmut-box {width: 30ch; overflow-x: hidden; white-space: nowrap; border: 1px solid #ddd; padding: 5px; background: #fafafa; font-family: monospace; font-size: 40px; margin: 0 auto; }
        #mut-box { width: 30ch; overflow-x: auto; white-space: nowrap; border: 1px solid #ddd; padding: 5px; background: #fafafa; font-family: monospace; font-size: 40px; margin: 0 auto; }
        .nav-buttons { margin-top: 20px; }
        .nav-buttons button { margin: 0 10px; padding: 10px 20px; font-size: 14px; border: none; border-radius: 4px; cursor: pointer; background: #007BFF; color: #fff; transition: background .2s; }
        .nav-buttons button:hover { background: #0056b3; }
        .mut-letter {
          display: inline-block;
          position: relative;
          width: 1ch;
          text-align: center;
        }
        #marker-pool { text-align: center; }
        #markers { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; padding: 5px; border: 1px solid #ddd; background: #fff; position: relative; height: auto; min-height: 3rem; }
        .marker {
          width: 4ch; height: 4ch; line-height: 2ch; text-align: center; background-color: transparent !important;
          border: 2px solid #007BFF; border-radius: 50%; font-size: 1.2rem; background-image: none !important;
          background: #fff; cursor: grab; user-select: none;
        }
        .nonmut-letter {
          display: inline-block;
          width: 1ch;
          text-align: center;
        }
        .marker.dragging { opacity: 0.7; cursor: grabbing; }
        #count { font-weight: bold; margin-top: 10px; }
      </style>
    </head>
    <body>
      <script>let trialStart = Date.now();</script>
      <div class="container">
        <span class="label">Trial 3 Nonmutated Sequence BELOW</span>
        <div id="nonmut-box">
          {% for base in nonmut %}
            <span class="nonmut-letter">{{ base }}</span>
          {% endfor %}
        </div>        
        <div id="mut-box">
          {% for base in mut %}
            <span class="mut-letter" data-index="{{ loop.index0 }}">{{ base }}</span>
          {% endfor %}
        </div>
        <input id="scroll-slider" type="range" min="0" value="0" style="width: 80ch; margin-top: 10px;" />
        <span class="label" style="margin-top: 10px;">Trial 3 Mutated Sequence ABOVE</span>
      </div>
      <div id="marker-pool" class="container">
        <span class="label">Drag these markers onto the mutated sequence:</span><br />
        <div id="markers">
          {% for i in range(10) %}<div class="marker" draggable="true"></div>{% endfor %}
        </div>
        <div id="count">You have <span id="remaining">10</span> markers left.</div>
      </div>
      <div class="container nav-buttons">
        <button onclick="submitTrial()">Finished Trial 2 and Go to Trial 3 →</button>
      </div>
      <script>
        const mutationIndexes = {{ mutation_indexes|tojson }};
        const nonmut = document.getElementById('nonmut-box');
        const mut = document.getElementById('mut-box');
        const slider = document.getElementById('scroll-slider');

        function updateSlider() {
          const maxScroll = mut.scrollWidth - mut.clientWidth;
          slider.max = maxScroll;
          slider.value = mut.scrollLeft;
        }
        mut.addEventListener('scroll', () => {
          nonmut.scrollLeft = mut.scrollLeft;
          slider.value = mut.scrollLeft;
        });
        slider.addEventListener('input', e => {
          mut.scrollLeft = e.target.value;
          nonmut.scrollLeft = e.target.value;
        });
        window.addEventListener('load', updateSlider);
        window.addEventListener('resize', updateSlider);

        const markersDiv = document.getElementById('markers');
        const letters = Array.from(document.querySelectorAll('.mut-letter'));
        let remaining = 10;
        const remainingEl = document.getElementById('remaining');

        function updateCount() { remainingEl.textContent = remaining; }
        document.querySelectorAll('.marker').forEach(marker => {
          let wasSnapped = false;
          marker.addEventListener('dragstart', e => {
            wasSnapped = !!marker.dataset.snappedTo;
            marker.classList.add('dragging');
            const rect = marker.getBoundingClientRect();
            e.dataTransfer.setDragImage(marker, e.clientX - rect.left, e.clientY - rect.top);
          });
          marker.addEventListener('dragend', e => {
            marker.classList.remove('dragging');
            const mRect = markersDiv.getBoundingClientRect();
            if (e.clientX >= mRect.left && e.clientX <= mRect.right && e.clientY >= mRect.top && e.clientY <= mRect.bottom) {
              delete marker.dataset.snappedTo;
              markersDiv.appendChild(marker);
              marker.style.position = marker.style.left = marker.style.top = marker.style.transform = '';
              if (wasSnapped) { remaining++; updateCount(); }
            } else {
              let closest = null, bestDist = Infinity;
              letters.forEach(letter => {
                const r = letter.getBoundingClientRect();
                const d = Math.hypot(e.clientX - (r.left + r.width/2), e.clientY - (r.top + r.height/2));
                if (d < bestDist) { bestDist = d; closest = letter; }
              });
              if (closest) {
                closest.appendChild(marker);
                marker.style.position = 'absolute';
                marker.style.left = '50%';
                marker.style.top = '50%';
                marker.style.transform = 'translate(-50%, -50%)';
                if (!wasSnapped) { remaining--; updateCount(); }
                marker.dataset.snappedTo = closest.dataset.index;
              }
            }
          });
        });
        document.body.addEventListener('dragover', e => e.preventDefault());

        function submitTrial() {
          const trialEnd = Date.now();
          const timeTaken = trialEnd - trialStart;
          const markersUsed = 10 - remaining;
          let found = 0;
          document.querySelectorAll('.marker').forEach(marker => {
            if (mutationIndexes.includes(parseInt(marker.dataset.snappedTo))) {
              found++;
            }
          });

          const form = document.createElement("form");
          form.method = "POST";
          form.action = window.location.href;

          const tInput = document.createElement("input");
          tInput.type = "hidden";
          tInput.name = "time_taken";
          tInput.value = timeTaken;

          const mInput = document.createElement("input");
          mInput.type = "hidden";
          mInput.name = "markers_used";
          mInput.value = markersUsed;

          const fInput = document.createElement("input");
          fInput.type = "hidden";
          fInput.name = "mutations_found";
          fInput.value = found;

          form.appendChild(tInput);
          form.appendChild(mInput);
          form.appendChild(fInput);
          document.body.appendChild(form);
          form.submit();
        }
      </script>
    </body>
    </html>
    """, nonmut=nonmut, mut=mut, mutation_indexes=mutation_indexes)

    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Visual Trial 3 Activity</title>
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
    }
    .container {
      text-align: center;
      background: #fff;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      width: 90%;
      max-width: 600px;
    }
    .button {
      padding: 12px 24px;
      font-size: 16px;
      color: #fff;
      background: #007BFF;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      transition: background 0.2s;
      margin-top: 20px;
    }
    .button:hover {
      background: #0056b3;
    }
    .instructions {
      text-align: left;
      margin-top: 20px;
      line-height: 1.5;
    }
    .instructions li {
      margin-bottom: 8px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Trial 3 Visual DNA Sequences</h1>
  </div><br />                                
  <div class="container">
    <h2>Read Before Starting</h2>
    <ul class="instructions">
      <li>Try your best to finish finding the mutation(s), if there are any at all, as quickly as you can.</li>
      <li>The visual trial 3 will be in the same format as the previous trial.</li>
      <li>The same instructions from the demonstration activity apply.</li>
      <li>If you have any questions, let Lea or Nina know BEFORE STARTING THE THIRD TRIAL.</li>
    </ul>
  </div>
    <form method="post" action="{{ url_for('visual_trial2.index') }}?participant={{ participant }}">
      <button type="submit" class="button">
        Start analyzing your last set of DNA Sequences
      </button>
    </form>
</body>
</html>
    """, participant=participant)
