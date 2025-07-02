from flask import Blueprint, render_template_string, request, url_for
from Bio import SeqIO
import os

bp = Blueprint("visual_demo", __name__, url_prefix="/visual/demo")

# Path to your FASTA file inside sonification/data_visual/
DEMO_FASTA = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "sonification", "data_visual", "demo.fasta"
)

@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # Load both records from the FASTA
        records = {rec.id: str(rec.seq) for rec in SeqIO.parse(DEMO_FASTA, "fasta")}
        nonmut = records["HBB_sickle_cell_demo_nonmutated"]
        mut    = records["HBB_sickle_cell_demo_mutated"]

        return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Visual Demo Activity</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; margin: 0; display: flex; flex-direction: column; align-items: center; }
    .container { background: #fff; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 90%; max-width: 800px; text-align: center; }
    .label { font-weight: bold; color: #333; display: block; margin-top: 10px; }
    #nonmut-box { letter-spacing: 1.182ch; width: 30ch; overflow-x: hidden; white-space: nowrap; border: 1px solid #ddd; padding: 5px; background: #fafafa; font-family: monospace; font-size: 40px; margin: 0 auto; }
    #mut-box { width: 30ch; overflow-x: auto; white-space: nowrap; border: 1px solid #ddd; padding: 5px; background: #fafafa; font-family: monospace; font-size: 40px; margin: 0 auto; }
    .nav-buttons { margin-top: 20px; }
    .nav-buttons button { margin: 0 10px; padding: 10px 20px; font-size: 14px; border: none; border-radius: 4px; cursor: pointer; background: #007BFF; color: #fff; transition: background .2s; }
    .nav-buttons button:hover { background: #0056b3; }
    .mut-letter { display: inline-block; position: relative; padding: 0 2px; cursor: default; }
    #marker-pool { text-align: center; }
    #markers { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; padding: 5px; border: 1px solid #ddd; background: #fff; position: relative; height: auto; min-height: 3rem; }
    .marker {
      width: 4ch; height: 4ch; line-height: 2ch; text-align: center; background-color: transparent !important;
      border: 2px solid #007BFF; border-radius: 50%; font-size: 1.2rem; background-image: none !important;
      background: #fff; cursor: grab; user-select: none;
    }
    .marker.dragging { opacity: 0.7; cursor: grabbing; }
    #count { font-weight: bold; margin-top: 10px; }
  </style>
</head>
<body>
  <div class="container">
    <span class="label">Sickle Cell Nonmutated Sequence BELOW</span>
    <div id="nonmut-box">{{ nonmut }}</div>
    <div id="mut-box">
      {% for base in mut %}
        <span class="mut-letter" data-index="{{ loop.index0 }}">{{ base }}</span>
      {% endfor %}
    </div>
    <!-- horizontal scroll slider -->
    <input
      id="scroll-slider"
      type="range"
      min="0"
      value="0"
      style="width: 80ch; margin-top: 10px;"
    />
    <span class="label" style="margin-top: 10px;">Sickle Cell Mutated Sequence ABOVE</span>
  </div>
  <div id="marker-pool" class="container">
    <span class="label">Drag these markers onto the mutated sequence:</span></br>
    <div id="markers">
      {% for i in range(10) %}
        <div class="marker" draggable="true"></div>
      {% endfor %}
    </div>
    <div id="count">You have <span id="remaining">10</span> markers left.</div>
  </div>
  <div class="container nav-buttons">
    <button onclick="location.href='{{ url_for('visual_trial1.index') }}'">
      Finished Demo and Go to Trial 1 →
    </button>
  </div>

  <script>
    const nonmut = document.getElementById('nonmut-box');
    const mut    = document.getElementById('mut-box');
    const slider = document.getElementById('scroll-slider');
    mut.addEventListener('scroll', () => nonmut.scrollLeft = mut.scrollLeft);

    function updateSlider() {
      const maxScroll = mut.scrollWidth - mut.clientWidth;
      slider.max = maxScroll;
      slider.value = mut.scrollLeft;
    }

    slider.addEventListener('input', e => {
      mut.scrollLeft = e.target.value;
      nonmut.scrollLeft = e.target.value;
    });

    mut.addEventListener('scroll', () => {
      nonmut.scrollLeft = mut.scrollLeft;
      slider.value = mut.scrollLeft;
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
        if (e.clientX >= mRect.left && e.clientX <= mRect.right
            && e.clientY >= mRect.top && e.clientY <= mRect.bottom) {
          delete marker.dataset.snappedTo;
          markersDiv.appendChild(marker);
          marker.style.position = '';
          marker.style.left = '';
          marker.style.top = '';
          marker.style.transform = '';
          if (wasSnapped) { remaining++; updateCount(); }
        } else {
          let closest = null, bestDist = Infinity;
          letters.forEach(letter => {
            const r = letter.getBoundingClientRect();
            const cx = r.left + r.width/2;
            const cy = r.top + r.height/2;
            const d = Math.hypot(e.clientX - cx, e.clientY - cy);
            if (d < bestDist) { bestDist = d; closest = letter; }
          });
          if (closest) {
            closest.appendChild(marker);
            marker.style.position  = 'absolute';
            marker.style.left      = '50%';
            marker.style.top       = '50%';
            marker.style.transform = 'translate(-50%, -50%)';
            if (!wasSnapped) { remaining--; updateCount(); }
            marker.dataset.snappedTo = closest.dataset.index;
          }
        }
      });
    });

    document.body.addEventListener('dragover', e => e.preventDefault());
  </script>
</body>
</html>
        """, nonmut=nonmut, mut=mut)

    # GET: show the start button only (unchanged)
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Visual Demo Activity</title>
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
    <h1>Visual Demonstration Activity</h1>
  </div></br>                                
  <div class="container">
    <h2>Read Before Starting</h2>
    <ul class="instructions">
      <li>Try your best to finish finding the mutation(s), if there are any at all, as quickly as you can.</li>
      <li>There are <strong>10 markers</strong> you can use to drag onto a letter of a sequence.</li>
      <li>You do <em>not</em> need to use all 10—only mark the letter where you think a mutation exists.</li>
      <li>Markers can only be placed on letters in the mutated sequence.</li>
      <li>You can drag markers back to the pool to reuse them.</li>
      <li>If you made a mistake, you can drag a marker from one letter to the next.</li>
    </ul>
  </div>
    <form method="post">
      <button type="submit" class="button">
        Start practicing analyzing visual DNA sequences
      </button>
    </form>
</body>
</html>
    """)
