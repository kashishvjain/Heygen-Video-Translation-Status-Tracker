````markdown
# Server Documentation

## Introduction

The Heygen Video Translation Status Tracker Server is a backend server designed to manage and track the status of video translation jobs. It exposes a set of API endpoints that allow clients to create new translation jobs and query the status of existing ones. The server is built using Python and Flask, providing a lightweight and efficient solution for handling asynchronous translation tasks.

## Architecture Overview

The server follows a modular architecture, separating concerns into different packages and modules. The main components include:

-   **API Endpoints**: Defined under the `server/api` package.
-   **Application Initialization**: Handled by the `src.server.app` module.
-   **Translation Job Management**: Implemented in the `src.server.translation_job` module.
-   **Translation Service Logic**: Located in the `src.server.translation_service` module.

## Modules and Packages

### `src.server` Package

The `src.server` package contains all server-side code responsible for handling requests and managing translation jobs.

#### Subpackages

-   `src.server.api`: Contains the API endpoints exposed by the server.

#### Modules

##### `src.server.app` Module

The `src.server.app` module initializes the Flask application and registers the API blueprint.

##### `src.server.translation_job` Module

The `src.server.translation_job` module defines the `TranslationJob` class, which encapsulates data and behavior related to a translation job.

##### `src.server.translation_service` Module

The `src.server.translation_service` module simulates the translation process and updates the status of translation jobs over time.

## Key Components

### API Endpoints

The server exposes two primary API endpoints under the `src.server.api` package:

#### 1. `POST /create_job`

-   **Description**: Creates a new translation job.
-   **Implementation**: Defined in the `src.server.api.create_job` module.
-   **Response**: Returns a JSON object containing the `job_id`.

**Example Response**:

```json
{
    "job_id": "a649581d-c511-4d0b-9ddc-0f74f61d2fe0"
}
```
````

#### 2. `GET /status/<job_id>`

-   **Description**: Retrieves the status of a translation job.
-   **Implementation**: Defined in the `src.server.api.status` module.
-   **Response**: Returns a JSON object containing the `status` and optional `error_message`.

**Example Response**:

```json
{
    "status": "completed"
}
```

### `TranslationJob` Class

Defined in the `src.server.translation_job` module, the `TranslationJob` class represents a translation task with attributes such as:

-   `job_id`: A unique identifier for the job.
-   `status`: The current status (`pending`, `in_progress`, `completed`, `error`).
-   `created_at`: Timestamp when the job was created.
-   `updated_at`: Timestamp when the job was last updated.

**Methods**:

-   `update_status()`: Updates the job status based on simulated translation progress.

### Application Initialization

The `src.server.app` module initializes the Flask application, registers blueprints, and starts the server.

**Key Functions**:

-   `create_app()`: Creates and configures the Flask application instance.
-   `register_blueprints(app)`: Registers API blueprints with the application.

### Translation Service Simulation

The `src.server.translation_service` module contains logic to simulate the translation process by:

-   Managing a queue of translation jobs.
-   Updating job statuses over time.
-   Logging translation metrics for analysis.

## Logging and Metrics

The server logs important events and metrics to `server.log`. This includes:

-   API requests and responses.
-   Translation job creation and status updates.
-   Metrics such as the number of requests, status, total processing time, and delays.

**Example Log Entries** (from `server.log`):

```
INFO - 127.0.0.1 - - [11/Dec/2024 18:10:45] "POST /create_job HTTP/1.1" 200 -
INFO - 127.0.0.1 - - [11/Dec/2024 18:10:46] "GET /status/47ed4606-42d6-4436-8bd5-ef05a9b90546 HTTP/1.1" 200 -
INFO - Translation metrics - Requests: 7, Status: pending, Total time: 42.26s, Delay: 19.26s
```

## Error Handling

The server includes robust error handling to ensure stability and provide meaningful responses to clients.

-   **Graceful Failures**: The server handles exceptions and returns appropriate HTTP status codes.
-   **Error Messages**: Descriptive error messages are provided in JSON responses when applicable.
-   **Logging**: All errors are logged with detailed information for debugging purposes.

## Conclusion

The Heygen Video Translation Status Tracker Server is a modular and efficient backend solution for managing video translation jobs. Its clear separation of concerns and robust implementation allows for easy maintenance and scalability. By providing well-defined API endpoints and comprehensive logging, it facilitates seamless integration with client applications.

For more details, refer to the source code and documentation in the following files:

-   `src.server.rst`
-   `src.server.api.rst`
-   `app.py`
-   `translation_job.py`
-   `translation_service.py`

```

```
