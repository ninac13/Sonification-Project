from flask import Blueprint, render_template_string

bp = Blueprint("visual", __name__, url_prefix="/visual")

@bp.route("/")
def index():
    return render_template_string("""
      <div style="text-align:center; margin-top:2em;">
        <h1>Welcome to the Visual Analysis Group!</h1>
      </div>
    """)