import asyncio
import logging
import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

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
        max_retries: int = 10,
        initial_backoff: float = 1.0,
        max_timeout: float = 300.0,
    ):
        self.base_url = base_url
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_timeout = max_timeout
        self.start_time = None
        self.last_status = None

    async def create_translation_job(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/create_job") as response:
                data = await response.json()
                return data.get("job_id")

    async def get_translation_status(self, job_id) -> TranslationResult:
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
