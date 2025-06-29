from flask import Flask, render_template, request, send_file
from mapper import map_sequence_to_notes
from player import play_sonification
from visual.linear import render_linear
import io

app = Flask(__name__)

@app.route("/", methods=("GET", "POST"))
def index():
    sonified_audio = None
    visual_output = None

    if request.method == "POST":
        seq = request.form.get("sequence", "").strip()

        if "sonify" in request.form:
            notes = map_sequence_to_notes(seq)
            audio_bytes = play_sonification(notes)
            # wrap bytes in a file-like for Flask to send
            sonified_audio = io.BytesIO(audio_bytes)

        if "visualize" in request.form:
            visual_output = render_linear(seq)

    return render_template(
        "index.html",
        sonified_audio=sonified_audio,
        visual_output=visual_output,
    )

if __name__ == "__main__":
    app.run(debug=True)