from ar.factory import create_app
from ar import db
from ar import models
# from ar import tasks
from flask_script import Server, Shell, Manager
from sys import argv

app = create_app()


if __name__ == '__main__':

    def _make_context():
        return dict(app=app, db=db, models=models)

    manager = Manager(app)
    manager.add_command("runserver", Server(
        host='0.0.0.0', port=8900))
    manager.add_command("shell", Shell(make_context=_make_context))
    app.config['DEBUG'] = None

    if argv[1] == 'runserver':
        app.logger.info(f'init flask in debug mode')
    elif argv[1] == 'shell':
        app.logger.info(f'enter flask shell mode')

    manager.run()

else:
    app.logger.info(f'init flask in production mode')

'''
# issues
Flask CLI throws 'OSError: [Errno 8] Exec format error' when run through docker-compose

https://stackoverflow.com/questions/55271912/flask-cli-throws-oserror-errno-8-exec-format-error-when-run-through-docker

'''
