from tasks.workers import celery
import requests
from models.acedemic_model import AcedemicModel
import time


@celery.task()
def url_method(acedemic_details_id):
    result = AcedemicModel.query.filter_by(acedemic_details_id=acedemic_details_id).first()
    response = {
                    "student_name": result.student_name,
                    "gained_marks": result.gained_marks,
                    "student_grade": result.student_grade
               }
    print(response)

    time.sleep(10)
    requests.post(url=f"http://127.0.0.1:5002/acedemicresult/{acedemic_details_id}", json=response)




