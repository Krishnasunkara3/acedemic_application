from flask import Flask
from flask_restful import Api
from db import db
from tasks import workers
from Resources.acedemic_resource import AcedemicDetails


from datetime import timedelta
from flask_jwt_extended import JWTManager



def create_app(db_location):

    # Starting the flask
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/1"
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = db_location
    db.init_app(app)
    @app.before_first_request
    def create_tables():
        db.create_all()
    api = Api(app)
    celery = workers.celery
    workers.celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )

    celery.Task = workers.ContextTask

    api.add_resource(AcedemicDetails, '/acedemicdetails/<string:acedemic_details_id>')
    app.app_context().push()

    return app, celery


app, celery = create_app("postgresql://postgres:123@localhost:5432/Flask")
if __name__ == "__main__":
    app.run(port=5001, debug=True, threaded=True)