import asyncio
import logging
import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional

import aiohttp


class TranslationStatus(Enum):
    PENDING = auto()
    COMPLETED = auto()
    ERROR = auto()


@dataclass
class TranslationResult:
    status: TranslationStatus
    error_message: Optional[str] = None


logger = logging.getLogger("client")


class VideoTranslationClient:
    def __init__(
        self,
        base_url: str,
        max_retries: int = 15,
        initial_backoff: float = 0.5,
        max_timeout: float = 300.0,
    ):
        """
        Initializes the client with the given parameters.

        Args:
            base_url (str): The base URL for the client.
            max_retries (int, optional): The maximum number of retries for requests. Defaults to 15.
            initial_backoff (float, optional): The initial backoff time in seconds for retries. Defaults to 1.0.
            max_timeout (float, optional): The maximum timeout in seconds for requests. Defaults to 300.0.
        """
        self.base_url = base_url
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_timeout = max_timeout
        self.start_time = None
        self.last_status = None

    async def create_translation_job(self):
        """
        Asynchronously creates a translation job by sending a POST request to the specified endpoint.

        Returns:
            str: The job ID of the created translation job.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/create_job") as response:
                data = await response.json()
                return data.get("job_id")

    async def get_translation_status(self, job_id) -> TranslationResult:
        """
        Asynchronously checks the translation status of a given job ID.

        Args:
            job_id (str): The ID of the translation job to check.

        Returns:
            TranslationResult: An object containing the status of the translation job.
        """
        self.start_time = time.time()
        current_backoff = self.initial_backoff
        max_backoff = 30.0  # Cap the maximum backoff time
        retries = 0

        async with aiohttp.ClientSession() as session:
            while retries < self.max_retries:
                elapsed_time = time.time() - self.start_time
                if elapsed_time > self.max_timeout:
                    return TranslationResult(
                        status=TranslationStatus.ERROR,
                        error_message="Total timeout exceeded",
                    )

                try:
                    async with session.get(
                        f"{self.base_url}/status/{job_id}"
                    ) as response:
                        data = await response.json()
                        status = data.get("result", "error")
                        self.last_status = status

                        if status == "completed":
                            return TranslationResult(status=TranslationStatus.COMPLETED)

                        if status == "error":
                            return TranslationResult(
                                status=TranslationStatus.ERROR,
                                error_message="Translation job failed",
                            )

                    # Add jitter to the backoff time
                    sleep_time = min(current_backoff, max_backoff) * (
                        0.5 + random.random() / 2
                    )
                    await asyncio.sleep(sleep_time)
                    current_backoff *= 2
                    retries += 1

                except aiohttp.ClientError as client_error:
                    logger.error("Client error: %s", client_error)
                except asyncio.TimeoutError as timeout_error:
                    logger.error("Timeout error: %s", timeout_error)
                    sleep_time = min(current_backoff, max_backoff)
                    await asyncio.sleep(sleep_time)
                    current_backoff *= 2
                    retries += 1

            return TranslationResult(
                status=TranslationStatus.ERROR, error_message="Max retries exceeded"
            )

    async def get_bulk_translation_statuses(
        self, job_ids: List[str], concurrent_limit: Optional[int] = None
    ) -> Dict[str, TranslationResult]:
        """
        Asynchronously checks the translation status of multiple job IDs concurrently.

        Args:
            job_ids (List[str]): A list of job IDs to check.
            concurrent_limit (Optional[int]): Maximum number of concurrent status checks.
                If None, all job IDs are processed concurrently.

        Returns:
            Dict[str, TranslationResult]: A dictionary mapping job IDs to their translation results.
        """
        if not job_ids:
            return {}

        # If no concurrent limit is specified, use the number of job IDs
        if concurrent_limit is None:
            concurrent_limit = len(job_ids)

        # Use asyncio.Semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(concurrent_limit)

        async def check_job_status_with_semaphore(job_id):
            async with semaphore:
                return job_id, await self.get_translation_status(job_id)

        # Use asyncio.gather to run status checks concurrently
        results = await asyncio.gather(
            *[check_job_status_with_semaphore(job_id) for job_id in job_ids]
        )

        # Convert results to a dictionary
        return dict(results)
