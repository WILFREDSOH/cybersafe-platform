# Analysis API

## Overview

The Analysis API exposes security analysis capabilities to authenticated CyberSafe users.

The API follows a REST-oriented design and is versioned under:


	/api/v1

Analysis execution may be asynchronous. Creating an analysis does not guarantee that its result is immediately available.


*Authentication*


All Analysis endpoints require an authenticated user.

Authentication is handled by the Identity domain.

The Analysis API must not implement a separate authentication mechanism.

The authenticated user's identity is obtained from the application security context.

Clients must not provide a *user_id* in analysis creation requests.

The server determines the owner of an analysis from the authenticated session.


*Authorization*


A user may access only analyses they are authorized to access.

For standard users:

  - an analysis can only be retrieved by its owner
  - analysis results can only be retrieved by authorized users
  - an analysis cannot be modified by another user
  - cancellation is only allowed when the analysis belongs to the authenticated user

Administrative access will be handled by the Administration domain.


*Endpoints *

*Create an Analysis*
```http
POST /api/v1/analyses
```
Creates a new analysis request.


 *Request*
```json
{
  "type": "URL",
  "target": "https://example.com"
}
```

 *Supported Types *
```
URL
PASSWORD
FILE
ACCOUNT_COMPROMISE
```

 *Validation *

The API must validate:

 - analysis type
 - target format
 - target size
 - required fields
 - supported analysis capabilities

Validation rules depend on the analysis type.

Examples:

- URL analysis requires a valid URL
- Password analysis requires a password value but must never persist it
- File analysis requires a valid uploaded file reference
- Account compromise analysis requires the appropriate account identifier

 *Response*
```http
201 Created
```

Example:
```json
{
  "id": "analysis-uuid",
  "type": "URL",
  "status": "REQUESTED",
  "created_at": "2026-08-10T10:00:00Z"
}
```
The response must not expose sensitive input values unnecessarily.

The server determines the analysis owner from the authenticated user.


  *Get an Analysis *
```http
GET /api/v1/analyses/{analysis_id}
```
Returns the current state of an analysis.

*Response*
```http
200 OK
```
Example:
```json
{
  "id": "analysis-uuid",
  "type": "URL",
  "status": "RUNNING",
  "created_at": "2026-08-10T10:00:00Z",
  "started_at": "2026-08-10T10:00:03Z",
  "completed_at": null
}
```
The API must not expose internal execution details that are not intended for clients.


 *List Analyses *
```http
GET /api/v1/analyses
```
Returns analyses accessible to the authenticated user.


*Query Parameters*
```
page
page_size
type
status
```
Example:
```http
GET /api/v1/analyses?page=1&page_size=20&status=COMPLETED
```

*Response*
```http
200 OK
```
Example:
```json
{
  "items": [
    {
      "id": "analysis-uuid",
      "type": "URL",
      "status": "COMPLETED",
      "created_at": "2026-08-10T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```
The API must return only analyses accessible to the authenticated user.

Pagination limits must be enforced server-side.

Clients must not be allowed to request unlimited result sets.


 *Get Analysis Results*
```http
GET /api/v1/analyses/{analysis_id}/results
```
Returns the normalized result of an analysis.

 *Successful Response*
```http
200 OK
```
Example:
```json
{
  "analysis_id": "analysis-uuid",
  "risk_score": 72,
  "risk_level": "HIGH",
  "summary": "Several security indicators were detected.",
  "indicators": [
    {
      "id": "indicator-uuid",
      "type": "SUSPICIOUS_REDIRECT",
      "severity": "HIGH",
      "title": "Suspicious redirect",
      "description": "The target redirects through an unexpected domain."
    }
  ]
}
```

*Result Availability*

If the analysis has not completed yet, the API must not return a fake or partial final result.

The response should indicate that the result is not yet available.

Recommended response:
```http
409 Conflict
```
Example:
```json
{
  "code": "ANALYSIS_RESULT_NOT_READY",
  "message": "The analysis result is not available yet."
}
```
The exact error response format will be standardized across the API.


 *Cancel an Analysis*
```http
POST /api/v1/analyses/{analysis_id}/cancel
```
Requests cancellation of an analysis that has not reached a terminal state.

*Successful Response*
```http
200 OK
```

Example:
```json
{
  "id": "analysis-uuid",
  "status": "CANCELLED"
}
```
Cancellation must be handled server-side.

The API must prevent cancellation of analyses that are already:

```
COMPLETED
FAILED
CANCELLED
```

If cancellation is no longer possible:
```http
409 Conflict
```
Example:
```json
{
  "code": "ANALYSIS_NOT_CANCELLABLE",
  "message": "The analysis can no longer be cancelled."
}
```

*HTTP Status Codes*

The Analysis API uses standard HTTP status codes.

Status	Meaning
200	Successful operation
201	Resource successfully created
400	Invalid request
401	Authentication required
403	Operation not authorized
404	Resource not found or inaccessible
409	Operation conflicts with current state
422	Request violates validation rules
429	Rate limit exceeded
500	Unexpected internal error
503	Analysis service temporarily unavailable


*Error Format*

Errors should use a consistent structure.

Example:
```json
{
  "code": "ANALYSIS_NOT_FOUND",
  "message": "The requested analysis could not be found.",
  "details": null
}
```
Validation errors may provide structured details:
```json
{
  "code": "VALIDATION_ERROR",
  "message": "The request contains invalid fields.",
  "details": {
    "target": [
      "A valid URL is required."
    ]
  }
}
```
Internal implementation details must not be exposed through error responses.

Stack traces, database errors, credentials, tokens and sensitive input values must never be returned to clients.



**Analysis Lifecycle**

The API reflects the following lifecycle:
```
                                   -> COMPLETED
                                  |
REQUESTED -> QUEUED -> RUNNING -> + ------- + -> FAILED
```

Cancellation may occur while an analysis is cancellable:
```
REQUESTED ------> QUEUED ------> RUNNING ------> CANCELLED
```
The backend is responsible for validating every transition.

Clients cannot directly set the analysis status.


**Asynchronous Execution**

Analysis execution is asynchronous by design.

The API request creates the analysis but does not execute the complete analysis inside the HTTP request lifecycle.

Conceptually:
```
Client -------------- > API -------------- > Analysis ------------ > Worker -------------- > Analysis Result
       POST /analysis       create analysis              enqueue                execute
```

This design prevents long-running security operations from blocking HTTP requests.
 
The exact queue and worker implementation will be defined during the implementation phase.


**Security Requirements**

The API must enforce the following rules:

1. All endpoints require authentication unless explicitly documented otherwise.
2. Users cannot specify another user's identifier when creating an analysis.
3. Users cannot access analyses belonging to another user.
4. Client-provided risk scores are ignored.
5. Client-provided final analysis statuses are ignored.
6. Sensitive values must not be written to logs.
7. Password values must never be persisted.
8. Uploaded files must be handled through controlled storage.
9. User-controlled input must be validated before analysis.
10. Analysis operations must be protected against abuse and excessive resource consumption.
11. Rate limiting must be applied to expensive analysis operations.
12. Internal errors must not expose implementation details.


**Idempotency**

Analysis creation is potentially an expensive operation.

The API should support an idempotency mechanism for analysis creation.

A future implementation may accept:
```http
Idempotency-Key: <unique-client-generated-key>
```
This prevents accidental duplicate analysis requests caused by retries.

The exact persistence and expiration strategy will be defined during implementation.


**Rate Limiting**

Different analysis types may have different resource costs.

Rate limits should therefore be configurable by analysis type.

For example:
```
URL
PASSWORD
FILE
ACCOUNT_COMPROMISE
```
must not necessarily share the same limits.

The exact limits will be determined after the first implementation and performance tests.


**Versioning**

The initial API version is:
```
/api/v1
```
Breaking changes must result in a new API version.

Non-breaking changes may be introduced within the same version when compatible with existing clients.


*API Boundary*

The Analysis API is responsible for:

 - receiving analysis requests
 - validating requests
 - authorizing access
 - creating analysis records
 - exposing analysis state
 - exposing analysis results
 - requesting cancellation

The Analysis API is not responsible for:

 - authentication implementation
 - user management
 - asset ownership management
 - notifications
 - learning recommendations
 - administrative management
 - system monitoring

These responsibilities belong to other CyberSafe domains.
