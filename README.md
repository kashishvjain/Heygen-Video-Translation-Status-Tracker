# Heygen Video Translation Status Tracker Client Library

## Overview

The Heygen Video Translation Status Tracker Client Library is designed to interact with a video translation backend server to check the status of translation jobs. This library provides an efficient and user-friendly way to query the status of translation jobs, minimizing delays and server load.

## Features

### 1. Asynchronous HTTP Requests

The client library uses asynchronous HTTP requests to interact with the server, ensuring non-blocking operations and improved performance.

### 2. Exponential Backoff with Jitter

To avoid overwhelming the server with frequent requests, the client library implements an exponential backoff strategy with jitter. This technique involves waiting for progressively longer intervals between retries, with a random variation (jitter) added to prevent synchronization issues when multiple clients retry simultaneously.

**Implementation Details**:

```python
current_backoff = self.initial_backoff  # e.g., 0.5 seconds
max_backoff = 30.0  # Maximum backoff time in seconds

# Inside the retry loop
sleep_time = min(current_backoff, max_backoff) * (0.5 + random.random() / 2)
await asyncio.sleep(sleep_time)
current_backoff *= 2  # Exponential increase
```

### 3. Capped Maximum Backoff Time

A cap is placed on the maximum backoff time to ensure that the delay between retries does not become excessively long. This balances the need to reduce server load with the need to provide timely responses.

**Implementation Details**:

```python
max_backoff = 30.0  # Cap the maximum backoff time

# Ensure sleep_time does not exceed max_backoff
sleep_time = min(current_backoff, max_backoff) * (0.5 + random.random() / 2)
```

### 4. Total Timeout Limit

A total timeout limit (

max_timeout

) is set to abort the operation if it takes too long, preventing indefinite waiting periods.

**Implementation Details**:

```python
# Check if the total elapsed time exceeds max_timeout
elapsed_time = time.time() - self.start_time
if elapsed_time > self.max_timeout:
    return TranslationResult(
        status=TranslationStatus.ERROR,
        error_message="Total timeout exceeded",
    )
```

### 5. Efficient Use of

ClientSession

By reusing the same

ClientSession

for all HTTP requests within the method, the client reduces overhead and improves efficiency.

**Implementation Details**:

```python
async with aiohttp.ClientSession() as session:
    # Reuse session for multiple requests
    while retries < self.max_retries:
        # Make HTTP requests using the same session
```

### 6. Bulk Query Support

The client library supports querying the status of multiple translation jobs concurrently. This feature allows users to check the status of multiple jobs in a single operation, improving efficiency and reducing the number of HTTP requests.

**Implementation Details**:

```python
async def get_bulk_translation_statuses(
    self, job_ids: List[str], concurrent_limit: Optional[int] = None
) -> Dict[str, TranslationResult]:
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
```

### 7. Robust Exception Handling

Comprehensive exception handling is included to catch and log potential errors, allowing the client to retry or fail gracefully.

**Implementation Details**:

```python
try:
    # Make HTTP request
    async with session.get(f"{self.base_url}/status/{job_id}") as response:
        # Process response
except aiohttp.ClientError as e:
    logger.error("Client error: %s", e)
except asyncio.TimeoutError as e:
    logger.error("Timeout error: %s", e)
    # Implement retry logic
```

## Usage

### Installation

To install the client library, run:

```sh
pip install -r requirements.txt
```

### Example Usage

```python
import asyncio
from src.client.client import VideoTranslationClient

async def main():
    client = VideoTranslationClient(base_url="http://localhost:5000")

    # Create a translation job
    job_id = await client.create_translation_job()
    print(f"Created job ID: {job_id}")

    # Get the status of the translation job
    result = await client.get_translation_status(job_id)
    print(f"Translation status: {result.status}")

    # Get the status of multiple translation jobs
    job_ids = [job_id, await client.create_translation_job()]
    results = await client.get_bulk_translation_statuses(job_ids)
    for job_id, result in results.items():
        print(f"Job ID: {job_id}, Status: {result.status}")

asyncio.run(main())
```

### Integration Test

An integration test is provided to demonstrate the usage of the client library and to verify its functionality.

```python
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
```

## Conclusion

The Heygen Video Translation Status Tracker Client Library provides a robust and efficient way to interact with a video translation backend server. By implementing features such as exponential backoff with jitter, capped maximum backoff time, total timeout limits, efficient use of

ClientSession

, bulk query support, and robust exception handling, the library ensures minimal delays and reduced server load while providing timely responses to users.
