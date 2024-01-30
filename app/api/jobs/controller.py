from flask import request
from flask_restful import Resource

from app import db
from app.api.jobs.models import Job
from app.api.jobs.schemas import JobSchema


class JobResource(Resource):
    def get(self):
        schema = JobSchema(many=True)
        jobs = Job.query.all()
        return schema.dump(jobs), 200

    def post(self):
        schema = JobSchema()
        job = schema.load(request.json)

        db.session.add(job)
        db.session.commit()

        return schema.dump(job)


class SingleJobResource(Resource):
    def get(self, id):
        job = Job.query.get_or_404(id)
        return JobSchema().dump(job), 200

    def put(self, id):
        schema = JobSchema()
        job = Job.query.get(id)

        if not job:
            return {
                "message": "Job not found"
            }, 404

        job = schema.load(request.json, instance=job)

        db.session.add(job)
        db.session.commit()

        return schema.dump(job)

    def delete(self, id):
        job = Job.query.get_or_404(id)
        db.session.delete(job)
        db.session.commit()
        return {"message": f"Job {job.title} deleted"}, 200