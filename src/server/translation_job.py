import random
import time
import uuid


class TranslationJob:
    def __init__(self, completion_time=60, error_probability=0.1):
        """
        Simulate a translation job with configurable completion time and error probability.

        Args:
            completion_time (int): Seconds until job completes
            error_probability (float): Probability of job failing
        """
        self.job_id = str(uuid.uuid4())
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
        if self.status in ["completed", "error"]:
            return self.status

        elapsed_time = time.time() - self.started_at

        if elapsed_time >= self.completion_time:
            if random.random() < self.error_probability:
                self.status = "error"
            else:
                self.status = "completed"

        return self.status
