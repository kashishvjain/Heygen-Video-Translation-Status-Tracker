from flask import Flask, jsonify
import random
import time

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
    return jsonify({"result": server.get_status()})


def run_server(port=5000):
    app.run(port=port)
