import time
import random
from flask import Flask, jsonify


app = Flask(__name__)


class TranslationStatus:
    def __init__(self, completion_time=10, error_probability=0.1):
        """
        Simulate a translation job with configurable completion time and error probability.

        Args:
            completion_time (int): Seconds until job completes
            error_probability (float): Probability of job failing
        """
        self.started_at = time.time()
        self.completion_time = completion_time
        self.error_probability = error_probability
        self.status = "pending"

    def get_status(self):
        """
        Return the status of the job. If the job has completed, also sets status
        to "completed" or "error" randomly with probability given by error_probability.

        Returns:
            str: "pending", "completed", or "error"
        """
        elapsed_time = time.time() - self.started_at

        if elapsed_time >= self.completion_time:
            if random.random() < self.error_probability:
                self.status = "error"
            else:
                self.status = "completed"

        return self.status


server = TranslationStatus()


@app.route("/status")
def get_status():
    """
    Return the status of the translation job as a JSON object.

    Returns:
        JSON object with key "result" mapping to the status of the job
            ("pending", "completed", or "error")
    """

    return jsonify({"result": server.get_status()})


def run_server(port=5000):
    """
    Run the Flask server on the given port.

    Args:
        port (int): The port to run the server on. Defaults to 5000.
    """
    app.run(port=port)
