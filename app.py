from flask import Flask, render_template, session
from ParticipantInfoView.participantInfoView import bp as participant_info_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'  # Required for session handling

    # Existing blueprint imports…
    from SelectModeViews.sonifyView      import bp as sonify_bp
    from SelectModeViews.visualView      import bp as visual_bp
    from ViewsDEMO.visualDEMO            import bp as visual_demo_bp
    from ViewsDEMO.sonifiedDEMO          import bp as sonify_demo_bp
    from Trial1Views.visualTrial1        import bp as visual_trial1_bp
    from Trial1Views.sonifyTrial1        import bp as sonify_trial1_bp
    from Trial2Views.sonifyTrial2        import bp as sonify_trial2_bp
    from Trial2Views.visualTrial2        import bp as visual_trial2_bp
    from Trial3Views.visualTrial3        import bp as visual_trial3_bp
    from Trial3Views.sonifyTrial3        import bp as sonify_trial3_bp
    from FINISHEDVIEW.finishedview       import bp as finished_view_bp

    # Register all blueprints
    app.register_blueprint(participant_info_bp)  # Make this handle "/"
    app.register_blueprint(sonify_bp)
    app.register_blueprint(visual_bp)
    app.register_blueprint(visual_demo_bp)
    app.register_blueprint(sonify_demo_bp)
    app.register_blueprint(visual_trial1_bp)
    app.register_blueprint(visual_trial2_bp)
    app.register_blueprint(visual_trial3_bp)
    app.register_blueprint(sonify_trial1_bp)
    app.register_blueprint(sonify_trial2_bp)
    app.register_blueprint(sonify_trial3_bp)
    app.register_blueprint(finished_view_bp)

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
