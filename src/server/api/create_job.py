from flask import jsonify
from flask.views import MethodView
from translation_service import TranslationService

server = TranslationService()


class CreateJobAPI(MethodView):
    def post(self):
        """
        Create a new translation job and return the job ID.

        Returns:
            JSON object with key "job_id" mapping to the ID of the created job
        """
        job_id = server.create_job()
        return jsonify({"job_id": job_id})
