```markdown

# Analysis Engine Architecture

## Purpose

The Analysis Engine is responsible for executing cybersecurity analyses requested through the Analysis domain.

It receives a validated analysis request, selects the appropriate analysis strategy, executes the required checks, normalizes the findings and produces a structured analysis result.

The engine must remain independent from HTTP concerns and should not directly depend on frontend code.

---

## High-Level Architecture

```text
                         ┌─────────────────┐
                         │     Client      │
                         └────────┬────────┘
                                  │
                                  │ HTTP
                                  v
                         ┌─────────────────┐
                         │ Analysis API    │
                         │ Controller      │
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │ Analysis        │
                         │ Application     │
                         │ Service         │
                         └────────┬────────┘
                                  │
                                  | enqueue
                                  v
                         ┌─────────────────┐
                         │ Analysis Worker │
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │ Analysis Engine │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    v             v             v
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ URL      │  │ Password │  │ File     │
              │ Analyzer │  │ Analyzer │  │ Analyzer │
              └────┬─────┘  └────┬─────┘  └────┬─────┘
                   │              │              │
                   └──────────────|──────────────┘
                                  v
                         ┌─────────────────┐
                         │ Result          │
                         │ Normalizer      │
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │ Risk Evaluation │
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │ Result          │
                         │ Persistence     │
                         └─────────────────┘
```

**Components**
**Analysis API Controller**

The controller is the HTTP entry point.

Responsibilities:

- parse HTTP requests
- validate request schemas
- authenticate the caller through the application security context
- authorize access
- call the application service
- translate application results into HTTP responses

The controller must not:

- execute security scans
- calculate risk scores
- access the database directly
- contain analysis-specific business rules
 

**Analysis Application Service**

The application service coordinates the analysis use cases.

Responsibilities:

- create analysis requests
- retrieve analyses
- request cancellation
- validate high-level business rules
- create analysis jobs
- coordinate repositories and workers

The service acts as the application boundary between the API layer and the domain logic.


**Analysis Repository**

The repository provides persistence operations for the Analysis domain.

Responsibilities:

- create analysis records
- retrieve analysis records
- update analysis state
- persist analysis results
- persist indicators
- retrieve analysis results

The repository hides database implementation details from the application layer.

The application layer must not depend directly on SQL queries.


**Analysis Worker**

The worker executes analysis jobs outside the HTTP request lifecycle.

A worker receives an analysis job containing an analysis identifier.

Conceptually:
```
Analysis API
     |
     | enqueue
     v
   Queue
     |
     v
  Worker
     |
     v
Analysis Engine
```

The worker is responsible for:

1. loading the analysis
2. validating that execution is still allowed
3. changing the analysis state to RUNNING
4. invoking the appropriate analyzer
5. collecting findings
6. normalizing findings
7. calculating the risk score
8. persisting the final result
9. marking the analysis as COMPLETED

If execution fails, the worker must record a safe failure state.


**Analysis Engine**

The Analysis Engine is the central orchestration component.

It selects an analyzer based on the analysis type.

Example:
```
Analysis Type
     |
     |─ URL
     |     |--> UrlAnalyzer
     |
     |─ PASSWORD
     │     |--> PasswordAnalyzer
     |
     |─ FILE
     |     |--> FileAnalyzer
     |
     |─ ACCOUNT_COMPROMISE
           |-─> AccountCompromiseAnalyzer
```

The engine should not contain the detailed implementation of every analysis type.

Instead, it delegates execution to specialized analyzers.


**Analyzer Interface**

Each analyzer follows a common contract.

Conceptually:
```
Analyzer
   |
   |-- supports(type)
   |
   |-- analyze(input)
          |
          v
       Findings
```
An analyzer should:

- receive validated input
- execute the required checks
- produce normalized findings
- avoid persistence concerns
- avoid HTTP concerns

The analyzer should not directly modify the final analysis status.

That responsibility remains with the worker/application layer.


**URL Analyzer**

The URL analyzer is responsible for inspecting URLs.

Initial checks may include:

- URL syntax
- HTTPS availability
- TLS certificate
- certificate validity period
- hostname
- redirects
- final destination
- domain age when reliable data is available
- suspicious characteristics
- reputation checks where an approved intelligence source is available

The analyzer produces findings rather than a final score.

Example:
```
HTTPS_ENABLED
CERTIFICATE_VALID
SUSPICIOUS_REDIRECT
RECENT_DOMAIN
```

**Password Analyzer**

The Password Analyzer evaluates password strength.

Possible checks include:

- length
- character diversity
- repeated characters
- common patterns
- dictionary exposure
- estimated resistance to guessing
- entropy-related characteristics

The raw password must remain in memory only for as long as necessary.

It must never be:

- stored in the database
- written to logs
- returned in API responses
- included in exceptions
- sent to external services unless explicitly required and securely designed

The analyzer returns security findings without exposing the password itself.


**File Analyzer**

The File Analyzer evaluates uploaded files.

Initial checks may include:

- file type
- MIME type
- file size
- cryptographic hash
- metadata
- suspicious characteristics
- malware reputation through approved external intelligence sources

Files must be processed in a controlled environment.

The analysis service must never execute untrusted uploaded files.


**Account Compromise Analyzer**

The Account Compromise Analyzer checks whether an account identifier appears in approved compromise intelligence sources.

The analyzer must:

- minimize transmitted information
- use approved external services
- handle unavailable intelligence sources gracefully
- avoid storing unnecessary personal data
- distinguish between "not found", "found", and "source unavailable"

External intelligence must never be treated as infallible.


**Finding Model**

Analyzers produce findings.

A finding contains:
```
type
severity
title
description
value
evidence
```
Example:
```json
{
  "type": "SUSPICIOUS_REDIRECT",
  "severity": "HIGH",
  "title": "Suspicious redirect",
  "description": "The URL redirects to a different domain.",
  "value": {
    "redirect_count": 2
  }
}
```
Sensitive evidence must be minimized.


**Result Normalization**

Different analyzers may produce different raw observations.

The Result Normalizer converts them into a common internal representation.
```
Analyzer
   |
   v
Raw Findings
   |
   v
Result Normalizer
   |
   v
Normalized Findings
```
This allows the rest of CyberSafe to work with a consistent result format regardless of the analysis type.


**Risk Evaluation**

The Risk Evaluation component converts normalized findings into a risk score and risk level.

Example:
```
Findings
   |
   |-- LOW
   |-- MEDIUM
   |__ HIGH
        |
        v
Risk Evaluation
        |
        |-- score
        |__ level
```
The risk score must be calculated server-side.

Clients cannot provide or override the score.

The exact scoring algorithm will be defined separately and will eventually become part of the Decision Engine domain.

For Sprint 3, Analysis is responsible for producing normalized evidence and findings.

The Decision Engine will later become responsible for more advanced security decisions.



**Separation from Decision Engine**

Analysis answers:
```
	What did we observe?
```
Decision Engine will answer:
```
	What should CyberSafe recommend or do based on what we observed?
```
Example:
```
Analysis
    |
    |__ "Password appears in a known common pattern"
                |
                v
Decision Engine
                |
                |__ "Recommend changing the password"
```
This separation is intentional.

Analysis must not contain recommendation logic.


**Error Handling**

The engine must distinguish between:

**Expected analysis failure**

Example:
```
  Target unavailable
```
The analysis may transition to:
```
  FAILED
```
with a safe failure code.

**External dependency failure**

Example:
```
  Reputation service unavailable
```
The analyzer should determine whether the analysis can continue with reduced confidence.


**Unexpected internal error**

Unexpected exceptions must:

- be logged internally
- avoid exposing sensitive data
- mark the analysis as failed when appropriate
- provide a safe error classification to the client


**Logging**

Logs must support troubleshooting without exposing sensitive information.

The following must never be logged:

- passwords
- authentication tokens
- API keys
- complete sensitive URLs containing credentials
- raw uploaded file contents
- unnecessary personal information

Each analysis execution should have a correlation identifier.

Example:
```
analysis_id=...
```
This allows operators to trace an analysis through the system without logging its sensitive input.



**Execution Flow**

A complete URL analysis follows this flow:
```
1. Client submits URL
          |
          v
2. API validates request
          |
          v
3. Analysis record created
          |
          v
4. Job added to queue
          |
          v
5. Worker receives job
          |
          v
6. Analysis becomes RUNNING
          |
          v
7. URL Analyzer executes
          |
          v
8. Findings generated
          |
          v
9. Findings normalized
          |
          v
10. Risk evaluated
          |
          v
11. Result persisted
          |
          v
12. Analysis becomes COMPLETED
```


**Retry Strategy**

Analysis jobs may require retries when a temporary infrastructure or external service failure occurs.

Retries must not be unlimited.

The worker should use a bounded retry strategy.

Example:
```
Attempt 1
   |
   |__ failure
        |
        v
Attempt 2
        |
        |__ failure
             |
             v
Attempt 3
             |
             |__ failure
                  |
                  v
                FAILED
```
Permanent validation errors must not be retried.



**Timeouts**

Each analyzer must have execution limits.

This prevents a malicious or unavailable target from consuming resources indefinitely.

Timeouts should be:

- configurable
- enforced server-side
- different when justified by analysis type
- recorded as safe failure reasons


**Resource Isolation**

Expensive or potentially dangerous analysis operations must be isolated from the main API process when required.

In particular:

- untrusted files must not be executed directly by the API
- external network requests must have strict timeouts
- resource-intensive operations should run in workers
- worker concurrency must be controlled


**Future Extensions**

The architecture should allow new analyzers to be added without modifying the existing API contract.

Potential future analyzers include:
```
IPAnalyzer
DomainAnalyzer
EmailAnalyzer
HeaderAnalyzer
ConfigurationAnalyzer
```
A new analyzer should implement the common analyzer contract and register its supported analysis type.


**Architectural Principles**


The Analysis Engine follows these principles:

1. HTTP concerns stay in the API layer.
2. Persistence concerns stay behind repositories.
3. Long-running operations run asynchronously.
4. Analysis types are implemented by specialized analyzers.
5. Findings are normalized before persistence.
6. Risk calculation is server-side.
7. Sensitive data is minimized.
8. External dependencies are isolated behind adapters.
9. Timeouts and resource limits are mandatory.
10. Analysis does not contain recommendation logic.
11. The architecture should remain simple enough for the V1.
12. New analysis types should not require rewriting the existing engine.
