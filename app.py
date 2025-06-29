from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Import and register your blueprints
    from views.sonifyView import bp as sonify_bp
    from views.visualView import bp as visual_bp

    app.register_blueprint(sonify_bp)
    app.register_blueprint(visual_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    create_app().run(debug=True)