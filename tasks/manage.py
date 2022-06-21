import traceback
import sys

from db import db


def manage_session(f):
    def inner(*args, **kwargs):

        # MANUAL PRE PING
        try:
            db.session.execute("SELECT 1;")
            db.session.commit()
        except:
            db.session.rollback()

        # SESSION COMMIT, ROLLBACK
        try:
            res = f(*args, **kwargs)
            db.session.commit()
            return res
        except Exception as e:
            db.session.rollback()
            sys.stderr.write(traceback.format_exc())
            raise e
            #return {"Error": "There has been an error. Please contact Peppo Team"}
    return inner
