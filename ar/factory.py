from flask import Flask, current_app
from ar import config
# import os
from ar import db
import logging
import logging.config
from ar import mylogging


def create_app(config_obj=None):
    app = Flask(__name__)
    app.logger.info(f'flask app is up by Lance!')
    app.config.from_object(config)

    # if config_obj:
    #     app.config.from_object(config_obj)

    with app.app_context():
        db.init_app(app)
        # app.logger.debug(f"app.config['CLEAN_TABLE'] {app.config['CLEAN_TABLE']}")
        # if app.config['CLEAN_TABLE']:
        #     db.drop_all()
        #     app.logger.debug('drop all tables')
        db.create_all()
        db.session.commit()
        from ar.api.v1.endpoints import bp as endpoints_bp
        app.register_blueprint(endpoints_bp, url_prefix='/v1')

    return app

