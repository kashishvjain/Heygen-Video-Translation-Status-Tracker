![Github Actions](https://github.com/kashishvjain/Heygen-Video-Translation-Status-Tracker/actions/workflows/pylint.yml/badge.svg)
![Github Actions](https://github.com/kashishvjain/Heygen-Video-Translation-Status-Tracker/actions/workflows/tests.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/heygen-video-translation-status-tracker/badge/?version=latest)](https://heygen-video-translation-status-tracker.readthedocs.io/en/latest/?badge=latest)
# Heygen Video Translation Status Tracker Client Library

## Table of Contents

1. [Overview](#overview)
2. [Repo Start and Setup](#repo-start-and-setup)
3. [Optimizations](#optimizations)
4. [Documentation](#documentation)
5. [Features](#features)
6. [Usage](#usage)
7. [Conclusion](#conclusion)

## Overview

The Heygen Video Translation Status Tracker Client Library is designed to interact with a video translation backend server to check the status of translation jobs. This library provides an efficient and user-friendly way to query the status of translation jobs, minimizing delays and server load. Some salient features:

-   Start multiple client jobs and for the same server and query based on job id
-   Client optimization with techniches like exponential back off and asynchronization
-   Track important metrics such as information delay, number of requests and status
-   Asynchronously query the server to get status of multiple jobs
-   Integrated CI pipeline
-   Documentation for all APIs and client side library hosted
-   Logs generated and saved in client.log and server.log

## Repo Start and Setup

This section provides instructions on how to get started with the Heygen Video Translation Status Tracker Client Library.

**Prerequisites:**

-   Python 3.7
-   `pip` package manager

**Installation:**

1. Clone the repository:
    ```bash
    git clone https://github.com/kashishvjain/Heygen-Video-Translation-Status-Tracker.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Heygen-Video-Translation-Status-Tracker
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. To run the integration tests:
    ```bash
    .\run_tests.bat
    ```
    OR
    ```bash
    python -m pytest -v -s
    ```
5. To just start the server 4. To run the integration tests:
    ```bash
    .\run_server.bat
    ```
    OR
    Run the app file with flask in src/server

## Optimizations

1. [Client Optimizations](markdown_documentation/client_optimizations.md)

2. [Server Optimizations](markdown_documentation/server_optimizations.md)

## Documentations

1. [Server Documentation](markdown_documentation/server_implementation.md)

2. [Client Documentation](markdown_documentation/client_implementation.md)

3. [Integration Test Documentation](markdown_documentation/integration_test_implementation.md)

## Features

### 1. Extensive Documentation

The documentation is comprehensive, covering all aspects of the client library and server apis, including setup, usage, and optimization techniques. Each section provides detailed information and examples to help users understand and utilize the library effectively.

### 2. Asynchronous HTTP Requests

The client library uses asynchronous HTTP requests to interact with the server, ensuring non-blocking operations and improved performance.

### 3. Exponential Backoff with Jitter

To avoid overwhelming the server with frequent requests, the client library implements an exponential backoff strategy with jitter. This technique involves waiting for progressively longer intervals between retries, with a random variation (jitter) added to prevent synchronization issues when multiple clients retry simultaneously.

### 4. Capped Maximum Backoff Time

A cap is placed on the maximum backoff time to ensure that the delay between retries does not become excessively long. This balances the need to reduce server load with the need to provide timely responses.

### 5. Total Timeout Limit

A total timeout limit (`max_timeout`) is set to abort the operation if it takes too long, preventing indefinite waiting periods.

### 6. Efficient Use of `ClientSession`

By reusing the same `ClientSession` for all HTTP requests within the method, the client reduces overhead and improves efficiency.

### 7. Bulk Query Support

The client library supports querying the status of multiple translation jobs concurrently. This feature allows users to check the status of multiple jobs in a single operation, improving efficiency and reducing the number of HTTP requests.

### 8. Robust Exception Handling

Comprehensive exception handling is included to catch and log potential errors, allowing the client to retry or fail gracefully.

### 9. Reporting Metrics

The client library includes functionality to report metrics such as the number of requests made, the delay between the actual completion and when the client get to know a task is complete, the average response time, and the success/failure rate of requests. These metrics can provide valuable insights into the performance and reliability of the client library and the backend server. I ensure that the time for each job is reandom between 20-60 seconds to ensure a realistic environment.

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
