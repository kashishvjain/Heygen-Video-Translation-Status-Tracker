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


@pytest.mark.asyncio
async def test_translation_status_bulk_jobs():
    logger.info("Starting bulk translation status test")

    server_process = Process(target=run_server, kwargs={"port": 5000})
    server_process.start()
    logger.info("Server process started")

    await asyncio.sleep(1)  # Small delay to ensure server starts

    try:
        client = VideoTranslationClient(base_url="http://localhost:5000")
        logger.info("Client initialized")

        # Create multiple job IDs
        job_ids = []
        for _ in range(5):
            job_id = await client.create_translation_job()
            job_ids.append(job_id)
        logger.info(f"Created {len(job_ids)} job IDs")

        # Check bulk job statuses
        results = await client.get_bulk_translation_statuses(job_ids)
        logger.info("Got bulk translation statuses")

        # Verify results
        assert len(results) == len(
            job_ids
        ), "Number of results should match number of job IDs"

        for job_id, result in results.items():
            assert job_id in job_ids, f"Unexpected job ID: {job_id}"
            assert result.status in [
                TranslationStatus.PENDING,
                TranslationStatus.COMPLETED,
                TranslationStatus.ERROR,
            ], f"Invalid status for job {job_id}"

        # Optional: Test with concurrent limit
        limited_results = await client.get_bulk_translation_statuses(
            job_ids, concurrent_limit=2
        )
        logger.info("Got bulk translation statuses with concurrent limit")

        assert len(limited_results) == len(
            job_ids
        ), "Number of limited results should match number of job IDs"

    finally:
        server_process.terminate()
        server_process.join()
        logger.info("Server process terminated")


@pytest.mark.asyncio
async def test_bulk_translation_status_empty_list():
    logger.info("Starting empty bulk translation status test")

    server_process = Process(target=run_server, kwargs={"port": 5000})
    server_process.start()
    logger.info("Server process started")

    await asyncio.sleep(1)  # Small delay to ensure server starts

    try:
        client = VideoTranslationClient(base_url="http://localhost:5000")
        logger.info("Client initialized")

        # Test with empty list of job IDs
        results = await client.get_bulk_translation_statuses([])
        logger.info("Checked empty job ID list")

        assert (
            results == {}
        ), "Results should be an empty dictionary for an empty job ID list"

    finally:
        server_process.terminate()
        server_process.join()
        logger.info("Server process terminated")
