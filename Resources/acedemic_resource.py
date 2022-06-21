
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from models.acedemic_model import AcedemicModel
from tasks.celery_task import url_method
from tasks.manage import manage_session

acedemic_args = reqparse.RequestParser()
acedemic_args.add_argument("acedemic_details_id", type=int, help="student id is required", required=True)
acedemic_args.add_argument("student_name", type=str, help="student name is required", required=True)
acedemic_args.add_argument("gained_marks", type=int, help="gained marks field is required", required=True)
acedemic_args.add_argument("student_grade", type=str, help="grade is required", required=True)

resource_fields = {
    "acedemic_details_id": fields.Integer,
    "student_name": fields.String,
    "gained_marks": fields.Integer,
    "student_grade": fields.String
}

resource_fields1 = {
                        'student_id': fields.Integer,
                        'student_name': fields.String,
                        'student_class': fields.String,
                        'student_age': fields.Integer,
                        'student_address': fields.String
                 }


class AcedemicDetails(Resource):

    @manage_session
    def get(self, acedemic_details_id):
        url_method.apply_async(args=(acedemic_details_id,))
        return "success"
        # result = AcedemicModel.query.filter_by(student_id=student_id).first()
        # response = requests.get(url=f"http://127.0.0.1:5002/studentdetails/{student_id}")
        # return response.json()
        # return {"message": "success"}

    @marshal_with(resource_fields)
    def post(self, acedemic_details_id):
        args = acedemic_args.parse_args()
        result = AcedemicModel.query.filter_by(acedemic_details_id=acedemic_details_id).first()

        if result:
            abort(404, message='student id is already available')
        acedemic_details = AcedemicModel(acedemic_details_id=acedemic_details_id, student_name=args['student_name'],
                                         gained_marks=args['gained_marks'],
                                         student_grade=args['student_grade'])

        acedemic_details.save_to_db()
        return acedemic_details, 201


