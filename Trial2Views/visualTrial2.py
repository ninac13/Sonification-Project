# ViewsDEMO/visualDEMO.py
from flask import Blueprint, render_template_string, request, url_for
from Bio import SeqIO
import os

bp = Blueprint("visual_trial2", __name__, url_prefix="/visual/trial2")

# Path to your FASTA file inside sonification/data_visual/
SET1_FASTA = os.path.join(
    os.path.dirname(__file__),
    os.pardir, "sonification", "data_visual", "set2.fasta"
)

@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # Load both records from the FASTA
        records = {rec.id: str(rec.seq) for rec in SeqIO.parse(SET1_FASTA, "fasta")}
        nonmut = records["trial2_original"]
        mut    = records["trial2_mutated"]

        return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Visual Trial 2</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4f4f4;
      padding: 20px;
      margin: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .container {
      background: #fff;
      padding: 20px;
      margin: 20px 0;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      width: 90%;
      max-width: 800px;
      text-align: center;
    }
    .label {
      font-weight: bold;
      color: #333;
      display: block;
      margin-top: 10px;
    }
    /* non-mutated: no scrollbar */
    #nonmut-box {
      width: 1ch;
      overflow-x: hidden;
      white-space: nowrap;
      border: 1px solid #ddd;
      padding: 5px;
      background: #fafafa;
      font-family: monospace;
      font-size: 80px;   /* larger letters */
      margin: 0 auto;
    }
    /* mutated: shows scrollbar */
    #mut-box {
      width: 1ch;
      overflow-x: auto;
      white-space: nowrap;
      border: 1px solid #ddd;
      padding: 5px;
      background: #fafafa;
      font-family: monospace;
      font-size: 80px;   /* larger letters */
      margin: 0 auto;
    }
    .nav-buttons {
      margin-top: 20px;
    }
    .nav-buttons button {
      margin: 0 10px;
      padding: 10px 20px;
      font-size: 14px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      background: #007BFF;
      color: #fff;
      transition: background .2s;
    }
    .nav-buttons button:hover {
      background: #0056b3;
    }
  </style>
</head>
<body>
  <div class="container">
    <span class="label">Trial 2 Nonmutated Sequence BELOW</span>
    <div id="nonmut-box">{{ nonmut }}</div>
    <div id="mut-box">{{ mut }}</div>
    <span class="label" style="margin-top: 10px;">Trial 2 Mutated Sequence ABOVE</span>
  </div>

  <div class="container nav-buttons">
    <button onclick="location.href='{{ url_for('visual_trial3.index') }}'">
      Finished Trial 2 and Go to Trial 3 →
    </button>
  </div>

  <script>
    // Only the mutated box is scrollable; sync the nonmutated box
    const nonmut = document.getElementById('nonmut-box');
    const mut    = document.getElementById('mut-box');
    mut.addEventListener('scroll', () => {
      nonmut.scrollLeft = mut.scrollLeft;
    });
  </script>
</body>
</html>
        """, nonmut=nonmut, mut=mut)

    # GET: show the start button only
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Visual Trial 2 Activity</title>
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
  </style>
</head>
<body>
  <div class="container">
    <h1>Trial 2 DNA Visual Analysis</h1>
    <form method="post">
      <button type="submit" class="button">
        Start analyzing your second set of DNA Sequences
       </button>
    </form>
  </div>
</body>
</html>
    """)
