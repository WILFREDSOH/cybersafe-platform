# Analysis Domain

## Purpose

The Analysis domain is responsible for evaluating security-related targets and producing structured security findings.

It does not make final user or system decisions. Decision-making belongs to the Decision Engine domain.

## Supported Analysis Types

The initial CyberSafe version defines the following analysis types:

- URL / Website Analysis
- Password Analysis
- File Analysis
- Email / Account Compromise Analysis

The architecture must allow additional analysis types to be introduced without redesigning the entire analysis subsystem.

## Core Concepts

### Analysis

Represents a requested security analysis.

An analysis has:

- an identifier
- an analysis type
- a status
- a creation timestamp
- a completion timestamp
- an owner/user context
- a target reference where applicable

### Analysis Result

Represents the structured output produced by an analysis.

An analysis may produce multiple results.

### Indicator

Represents an individual security observation discovered during an analysis.

Examples:

- HTTPS enabled
- suspicious redirect
- weak password pattern
- suspicious file metadata
- known account exposure

Indicators contain structured information such as:

- type
- severity
- value
- description
- evidence where appropriate

### Risk Score

Represents an aggregated assessment derived from analysis findings.

The scoring model must be documented, deterministic where appropriate, and independently testable.

## Analysis Lifecycle


REQUESTED

    |
    
QUEUED

    |
    
RUNNING

    |
    |------> FAILED
    |
    
COMPLETED

A cancellation state may be introduced when asynchronous processing is implemented.

# Architectural Boundaries

The Analysis domain is responsible for:

- validating analysis requests
- orchestrating analysis execution
- collecting findings
- normalizing findings
- producing analysis results
- calculating analysis-level risk information

The Analysis domain is not responsible for:

- final remediation decisions
- user notification policies
- administrative management
- learning content selection
- platform-wide monitoring

Those responsibilities belong to other domains.

# Relationship with Decision Engine

The Analysis domain produces evidence and risk information.

The Decision Engine consumes this information to determine appropriate actions.

Analysis -> Findings / Risk -> Decision Engine -> Action

# Security Principles

The Analysis domain must follow:

- least privilege
- strict input validation
- secure handling of user-provided data
- no unnecessary storage of sensitive information
- no execution of untrusted files
- controlled access to external intelligence services
- auditability of security-sensitive operations


## Use Cases

### UC-AN-01 - Create Analysis

The authenticated user requests a new security analysis.

Input:

- analysis type
- target appropriate to the analysis type
- optional analysis parameters

The system must:

1. authenticate the user
2. authorize access to the requested operation
3. validate the request 
4. validate the target according to the analysis type
5. create the analysis record
6. assign the initial status
7. return the analysis identifier and status

The system must never trsut client-provided analysis result or risk scores.

Initial status:

REQUESTED 


UC-AN-02 — Get Analysis


The authenticated user retrieves an analysis.

The system must:

   1. authenticate the user
   2. verify that the user is authorized to access the analysis
   3. retrieve the analysis
   4. return its current state and metadata

The response must not expose sensitive internal implementation details.


UC-AN-03 — Execute Analysis


The application executes an analysis according to its analysis type.

The system must:


  1. load the analysis
  2. verify that it can be executed
  3. transition the analysis to RUNNING
  4. invoke the appropriate analysis service
  5. collect normalized findings
  6. calculate the analysis result
  7. calculate the risk information
  8. transition the analysis to COMPLETED

If execution fails:


RUNNING -> FAILED


Failure information must be stored safely without exposing sensitive internal details to end users.


UC-AN-04 — Get Analysis Results


The authenticated user retrieves the results of a completed analysis.

The response may contain:

   - analysis metadata
   - findings
   - indicators
   - severity levels
   - evidence where appropriate
   - risk information
   - execution timestamps

Results must be read-only from the client perspective.


UC-AN-05 — Get Risk Score


The system exposes the risk assessment associated with an analysis.

The score must be produced by trusted server-side logic.

The client must never be allowed to submit or modify the final score.

The score should be accompanied by structured information explaining the main contributing findings.


UC-AN-06 — Get Analysis History


The authenticated user can retrieve their previous analyses.

The system must:

   - return only analyses accessible to the authenticated user
   - support pagination
   - support filtering by analysis type
   - support filtering by status
   - support chronological ordering

Administrative users may have broader access through the Administration domain.


UC-AN-07 — Cancel Analysis


An analysis may be cancelled while it is still cancellable.

A cancellation request must be validated server-side.

A completed or failed analysis cannot be cancelled.

The exact cancellation behavior depends on whether the analysis is queued or already running.

The system must prevent race conditions between cancellation and execution.


## Domain Model

### Analysis

"Analysis" represents a security analysis requested by an authenticated user.

Core attributes:

- 'id': unique identifier
- 'user_id': identifier of the requesting user
- 'type': analysis type
- 'status': lifecycle status
- 'target': normalized analysis target when safe to persist
- 'created_at': creation timestamp
- 'started_at': execution start timestamp
- 'completed_at': completion timestamp
- 'failure_code': safe internal failure classification when applicable

Supported analysis types:


URL
PASSWORD
FILE
ACCOUNT_COMPROMISE

Supported initial statuses:

REQUESTED
QUEUED
RUNNING
COMPLETED
FAILED
CANCELLED

The system must enforce valid state transitions.

## AnalysisResult

"AnalysisResult" represents the normalized output of an analysis execution.

Core attributes:

    - id
    - analysis_id
    - summary
    - risk_score
    - risk_level
    - created_at

An analysis may have one final result in the initial version.

The model must remain extensible to support multiple result versions in the future.


## Indicator

"Indicator" represents an individual security observation produced by an analysis.

Core attributes:

    - id
    - analysis_result_id
    - type
    - severity
    - title
    - description
    - value
    - evidence
    - created_at

Indicator severity levels:

     INFO
     LOW
     MEDIUM
     HIGH
     CRITICAL

Indicators must be normalized so that different analysis engines can produce a common representation.


## Sensitive Data Handling

Analysis targets may contain sensitive information.

The system must classify targets according to their sensitivity before persistence.


## Password Analysis

Raw passwords must not be persisted.

The password should be processed in memory and discarded after analysis.

The system must not:

  - store the plaintext password
  - log the plaintext password
  - include the plaintext password in API responses
  - include the plaintext password in error messages
  - persist the plaintext password in analysis history

## File Analysis

Uploaded files must not be executed.

Files must be handled through controlled storage and analysis mechanisms.

The system should persist safe metadata and cryptographic hashes where appropriate.


## URL Analysis

URLs may contain credentials, tokens, query parameters or other sensitive information.

URLs must therefore be sanitized before being stored in persistent history or logs.


## Account Compromise Analysis

Personally identifiable information and external-service responses must be minimized and protected according to the application's privacy requirements.



## Domain Invariants

The following rules must always hold:

	1. An analysis must belong to an authenticated user.
	2. An analysis type must be supported by the system.
	3. An analysis status must be a valid lifecycle state.
	4. Invalid status transitions must be rejected.
	5. A completed analysis must have a valid result.
	6. A failed analysis must not be presented as successfully completed.
	7. Client-provided risk scores must never be trusted.
	8. Sensitive analysis targets must not be persisted in plaintext when persistence is unnecessary.
	9. Analysis results must be immutable from the client perspective.
	10. Users must only access analyses they are authorized to access.


## Relationship with Asset Management

Analysis may operate on assets previously registered in the Asset Management domain.

Examples:

Asset
  |
   - URL
  |
   - Domain
  |
   - File
  |
   - Account

An analysis may therefore reference an existing asset when applicable.

However, an analysis request should also support a one-time target when the target does not need to become a persistent asset.

This prevents unnecessary duplication between Asset Management and Analysis.



## Relationship with Decision Engine

Analysis produces evidence.

Decision Engine consumes evidence.

Analysis
    |
    - > Result
           |
             -> Indicators
           |
             -> Risk Score -> Decision Engine

Analysis must not directly execute business decisions such as:

  - blocking a user
  - sending a notification
  - assigning training content
  - changing account permissions

Those responsibilities belong to downstream domains.
