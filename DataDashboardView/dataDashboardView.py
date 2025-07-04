from flask import Blueprint, render_template_string
import csv

bp = Blueprint('data_dashboard', __name__, url_prefix='/data_dashboard')

DATA_FILE = 'collected_data.csv'

@bp.route('/')
def show_data():
    rows = []
    try:
        with open(DATA_FILE, newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except FileNotFoundError:
        rows = [['No data found.']]

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Participant Data Dashboard</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          padding: 2rem;
          background: #f4f6f9;
        }
        h2 {
          text-align: center;
          margin-bottom: 1rem;
        }
        table {
          border-collapse: collapse;
          margin: 0 auto;
          width: 80%;
          background: white;
          box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        th, td {
          padding: 0.75rem;
          border: 1px solid #ddd;
          text-align: center;
        }
        th {
          background-color: #6c8efb;
          color: white;
        }
      </style>
    </head>
    <body>
      <h2>Participant Information Collected</h2>
      <table>
        {% for row in rows %}
          <tr>
            {% for item in row %}
              <{{ 'th' if loop.parent.loop.index0 == 0 else 'td' }}>{{ item }}</{{ 'th' if loop.parent.loop.index0 == 0 else 'td' }}>
            {% endfor %}
          </tr>
        {% endfor %}
      </table>
    </body>
    </html>
    """, rows=rows)
