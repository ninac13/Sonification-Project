from flask import Flask, render_template, redirect, url_for


def create_app():
   app = Flask(__name__)


   # existing blueprint imports…
   from ParticipantInfoView.participantInfoView import bp as participant_info_bp
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



   # register all blueprints
   app.register_blueprint(participant_info_bp)
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





   @app.route('/')
   def index():
        # send everyone to your new form
      return redirect(url_for('participant_info.participant_info'))

   return app

if __name__ == "__main__":
    create_app().run(debug=True)






