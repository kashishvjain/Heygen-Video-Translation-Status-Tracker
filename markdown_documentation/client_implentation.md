# Client Library Documentation

## Introduction

This document describes the Heygen Video Translation Client Library, a Python library designed to interact with the Heygen Video Translation Status Tracker Server. This library allows users to create translation jobs and monitor their progress asynchronously.

## Classes

### `TranslationStatus` Enum

This enum defines the possible statuses of a translation job:

-   `PENDING`: The job is waiting to be processed.
-   `COMPLETED`: The translation has finished successfully.
-   `ERROR`: An error occurred during the translation process.
-   `TIMEOUT`: The translation job exceeded the maximum allowed time.

### `TranslationResult` Dataclass

This dataclass represents the result of a translation status check:

-   `status`: The status of the translation job (`TranslationStatus` enum).
-   `error_message`: An optional error message if the status is `ERROR`.

### `VideoTranslationClient` Class

This class provides the main functionality for interacting with the translation server.

#### Constructor (`__init__`)

```python
def __init__(
    self,
    base_url: str,
    max_retries: int = 15,
    initial_backoff: float = 0.5,
    max_timeout: float = 300.0,
):
```


Initializes a new `VideoTranslationClient` instance.

-   `base_url`: The base URL of the translation server.
-   `max_retries`: The maximum number of retries for failed requests (default: 15).
-   `initial_backoff`: The initial backoff time in seconds for retries (default: 0.5).
-   `max_timeout`: The maximum timeout in seconds for a translation job (default: 300.0).

#### `create_translation_job` Method

```python
async def create_translation_job(self):
```

Asynchronously creates a new translation job on the server.

-   **Returns:** The job ID of the created job (string).

#### `get_translation_status` Method

```python
async def get_translation_status(self, job_id) -> TranslationResult:
```

Asynchronously retrieves the status of a translation job.

-   `job_id`: The ID of the job to check.
-   **Returns:** A `TranslationResult` object containing the status and any error message.

#### `get_bulk_translation_statuses` Method

```python
async def get_bulk_translation_statuses(
    self, job_ids: List[str], concurrent_limit: Optional[int] = None
) -> Dict[str, TranslationResult]:
```

Asynchronously retrieves the status of multiple translation jobs concurrently.

-   `job_ids`: A list of job IDs to check.
-   `concurrent_limit`: The maximum number of concurrent status checks (optional). If `None`, all jobs are checked concurrently.
-   **Returns:** A dictionary mapping job IDs to their corresponding `TranslationResult` objects.

## Usage Example

```python
import asyncio

async def main():
    client = VideoTranslationClient(base_url="http://localhost:5000")
    job_id = await client.create_translation_job()
    print(f"Created job with ID: {job_id}")

    result = await client.get_translation_status(job_id)
    print(f"Job status: {result.status}")

    bulk_results = await client.get_bulk_translation_statuses([job_id])
    print(f"Bulk job statuses: {bulk_results}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling

The client library includes retry logic with exponential backoff to handle transient network errors. It also includes a timeout mechanism to prevent jobs from running indefinitely.

## Logging

The library uses the `logging` module to log events and errors. You can configure the logging level and output to suit your needs.

