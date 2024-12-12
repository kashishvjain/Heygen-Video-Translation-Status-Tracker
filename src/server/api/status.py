from api.create_job import server
from cache import cache  # Import the cache object
from flask import jsonify
from flask.views import MethodView


class StatusAPI(MethodView):
    @cache.cached(timeout=10, query_string=True)
    def get(self, job_id):
        """
        Return the status of the translation job as a JSON object.

        Args:
            job_id (str): The ID of the job to get the status for

        Returns:
            JSON object with key "result" mapping to the status of the job
                ("pending", "completed", "error", or "Job ID not found")
        """
        status = server.get_status(job_id)
        return jsonify({"result": status})
