from translation_job import TranslationJob


class TranslationService:
    def __init__(self):
        """
        Initialize the TranslationService.

        The TranslationService is responsible for managing and tracking the
        status of translation jobs.

        :param self: The TranslationService instance
        """
        self.jobs = {}

    def create_job(self):
        """
        Create a new translation job and return the job ID.

        Returns:
            str: The ID of the created job
        """
        job = TranslationJob()
        self.jobs[job.id] = job
        return job.id

    def get_status(self, job_id):
        """
        Return the status of the job as a string.

        Args:
            job_id (str): The ID of the job to get the status for

        Returns:
            str: The status of the job
        """
        job = self.jobs.get(job_id)
        if job:
            return job.get_status()
        else:
            return "Job ID not found"
