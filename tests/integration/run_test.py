import asyncio
import logging
from multiprocessing import Process

import pytest

from src.client.client import TranslationStatus, VideoTranslationClient
from src.server.app import run_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("translation.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("client")


@pytest.mark.asyncio
async def test_translation_status_single_job():
    logger.info("Starting translation status test")

    server_process = Process(target=run_server, kwargs={"port": 5000})
    server_process.start()
    logger.info("Server process started")

    await asyncio.sleep(1)  # Small delay to ensure server starts

    try:
        client = VideoTranslationClient(base_url="http://localhost:5000")
        logger.info("Client initialized")

        job_id = await client.create_translation_job()
        result = await client.get_translation_status(job_id)
        logger.info("Got translation status: %s", result.status)

        assert result.status in [
            TranslationStatus.PENDING,
            TranslationStatus.COMPLETED,
            TranslationStatus.ERROR,
        ]

    finally:
        server_process.terminate()
        server_process.join()
        logger.info("Server process terminated")
