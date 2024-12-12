# Integration Tests

The integration tests for the Heygen Video Translation Status Tracker Client Library are designed to verify the functionality of the client library and its interaction with the server. These tests ensure that the client can create translation jobs, query their statuses, and handle multiple jobs concurrently.

## Test Cases

1.  **Single Job Translation Status Test**

    This test verifies the status of a single translation job.

    -   **Test Function**: `test_translation_status_single_job`

    -   **Description**:

        -   Starts the server process.
        -   Initializes the client.
        -   Creates a translation job.
        -   Queries the status of the created job.
        -   Asserts that the status is one of `TranslationStatus.PENDING`, `TranslationStatus.COMPLETED`, or `TranslationStatus.ERROR`.

    -   **Log Output**: Logs the initialization, job creation, status retrieval, and server termination.

2.  **Bulk Jobs Translation Status Test**

    This test verifies the statuses of multiple translation jobs.

    -   **Test Function**: `test_translation_status_bulk_jobs`

    -   **Description**:

        -   Starts the server process.
        -   Initializes the client.
        -   Creates multiple translation jobs.
        -   Queries the statuses of the created jobs in bulk.
        -   Asserts that the number of results matches the number of job IDs.
        -   Asserts that each job ID in the results is valid and its status is one of `TranslationStatus.PENDING`, `TranslationStatus.COMPLETED`, or `TranslationStatus.ERROR`.
        -   Optionally tests with a concurrent limit.

    -   **Log Output**: Logs the initialization, job creation, bulk status retrieval, and server termination.

3.  **Empty Bulk Translation Status Test**

    This test verifies the behavior when querying the statuses of an empty list of job IDs.

    -   **Test Function**: `test_bulk_translation_status_empty_list`

    -   **Description**:

        -   Starts the server process.
        -   Initializes the client.
        -   Queries the statuses of an empty list of job IDs.
        -   Asserts that the result is an empty dictionary.

    -   **Log Output**: Logs the initialization, empty list check, and server termination.

## Running the Tests

To run the integration tests, use the following command:

```bash
python -m pytest -v -s
```

````

Alternatively, you can use the provided batch script:

```bash
.\run_tests.bat
```
````
