![Github Actions](https://github.com/kashishvjain/Heygen-Video-Translation-Status-Tracker/actions/workflows/pylint.yml/badge.svg)
![Docs](https://img.shields.io/readthedocs/heygen-video-translation-status-tracker)

# Heygen Video Translation Status Tracker Client Library

## Repo Start and Setup

This section provides instructions on how to get started with the Heygen Video Translation Status Tracker Client Library.

**Prerequisites:**

-   Python 3.7 or higher
-   `pip` package manager

**Installation:**

1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```
2. Navigate to the project directory:
    ```bash
    cd <project_directory>
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Overview

The Heygen Video Translation Status Tracker Client Library is designed to interact with a video translation backend server to check the status of translation jobs. This library provides an efficient and user-friendly way to query the status of translation jobs, minimizing delays and server load.

## Features

### 1. Asynchronous HTTP Requests

The client library uses asynchronous HTTP requests to interact with the server, ensuring non-blocking operations and improved performance.

### 2. Exponential Backoff with Jitter

To avoid overwhelming the server with frequent requests, the client library implements an exponential backoff strategy with jitter. This technique involves waiting for progressively longer intervals between retries, with a random variation (jitter) added to prevent synchronization issues when multiple clients retry simultaneously.

### 3. Capped Maximum Backoff Time

A cap is placed on the maximum backoff time to ensure that the delay between retries does not become excessively long. This balances the need to reduce server load with the need to provide timely responses.

**Implementation Details**:

```python
max_backoff = 30.0  # Cap the maximum backoff time

# Ensure sleep_time does not exceed max_backoff
sleep_time = min(current_backoff, max_backoff) * (0.5 + random.random() / 2)
```

### 4. Total Timeout Limit

A total timeout limit (`max_timeout`) is set to abort the operation if it takes too long, preventing indefinite waiting periods.

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

### 5. Efficient Use of `ClientSession`

By reusing the same `ClientSession` for all HTTP requests within the method, the client reduces overhead and improves efficiency.

**Implementation Details**:

```python
async with aiohttp.ClientSession() as session:
    # Reuse session for multiple requests
    while retries < self.max_retries:
        # Make HTTP requests using the same session
```

### 6. Bulk Query Support

The client library supports querying the status of multiple translation jobs concurrently. This feature allows users to check the status of multiple jobs in a single operation, improving efficiency and reducing the number of HTTP requests.

### 7. Robust Exception Handling

Comprehensive exception handling is included to catch and log potential errors, allowing the client to retry or fail gracefully.

### 8. Reporting Metrics

-   The client library includes functionality to report metrics such as the number of requests made, the delay between the actual completion and when the client get to know a task is complete, the average response time, and the success/failure rate of requests. These metrics can provide valuable insights into the performance and reliability of the client library and the backend server.

## Usage

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

An integration test is provided to demonstrate the usage of the client library and to verify its functionality. When the test is run, we also display how many requests to the server each request took and the delay between the actual completion of the task and the client getting the information.

## Conclusion

The Heygen Video Translation Status Tracker Client Library provides a robust and efficient way to interact with a video translation backend server. By implementing features such as exponential backoff with jitter, capped maximum backoff time, total timeout limits, efficient use of `ClientSession`, bulk query support, and robust exception handling, the library ensures minimal delays and reduced server load while providing timely responses to users.

