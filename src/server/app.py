import logging

from api.create_job import CreateJobAPI
from api.status import StatusAPI
from flask import Flask

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler(),
    ],
)

app = Flask(__name__)

# Register the class-based views with the Flask app
app.add_url_rule("/create_job", view_func=CreateJobAPI.as_view("create_job_api"))
app.add_url_rule("/status/<job_id>", view_func=StatusAPI.as_view("status_api"))


def run_server(port=5000):
    """
    Run the Flask server on the given port.

    Args:
        port (int): The port to run the server on. Defaults to 5000.
    """
    app.run(port=port)
