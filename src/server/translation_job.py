import logging
import random
import time
import uuid

logger = logging.getLogger("logger")


class TranslationJob:
    def __init__(self, error_probability=0.1):
        """
        Simulate a translation job with configurable completion time and error probability.

        Args:
            completion_time (int): Seconds until job completes
            error_probability (float): Probability of job failing
        """
        self.job_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.completion_time = random.randint(20, 40)
        self.error_probability = error_probability
        self.status = "pending"
        self.elapsed_time = None
        self.request_count = 0

    def log_metrics(self):
        """
        Log the metrics of the job, including the number of requests, status, total time, and delay.
        """

        delay_time = self.elapsed_time - self.completion_time
        logger.info(
            "Translation metrics - Requests: %d, Status: %s, Total time: %.2fs, Delay: %.2fs",
            self.request_count,
            self.status,
            self.elapsed_time,
            delay_time,
        )

    def get_status(self):
        """
        Return the status of the job. If the job has completed, also sets status
        to "completed" or "error" randomly with probability given by error_probability.

        Returns:
            str: "pending", "completed", or "error"
        """
        self.request_count += 1

        if self.status in ["completed", "error"]:
            return self.status

        self.elapsed_time = time.time() - self.start_time

        if self.elapsed_time >= self.completion_time:
            self.log_metrics()
            if random.random() < self.error_probability:
                self.status = "error"
            else:
                self.status = "completed"
        return self.status
