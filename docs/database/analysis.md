# Analysis Database Model

## Overview

The Analysis domain uses three primary persistence entities:

users

  |
  | 1:N
  
analyses

  |
  | 1:1

analysis_results

  |
  | 1:N
  |

analysis_indicators

The users table belongs to the Identity domain and is referenced by Analysis.

Assets belong to the Asset Management domain and may optionally be referenced by an analysis.

## analyses

Represents an analysis request.

### Fields

Field	             Type	        Constraints	     Description

id	             UUID	        PK	             Unique analysis identifier
user_id	             UUID	        FK, NOT NULL	     Requesting user
asset_id             UUID	        FK, NULL	     Optional associated asset
type	             VARCHAR            NOT NULL	     Analysis type
status	             VARCHAR	        NOT NULL	     Analysis lifecycle state
target_reference     TEXT	        NULL	             Sanitized target reference
created_at           TIMESTAMPTZ	NOT NULL	     Creation timestamp
started_at           TIMESTAMPTZ	NULL	             Execution start
completed_at	     TIMESTAMPTZ	NULL	             Completion time
failure_code	     VARCHAR	        NULL	             Safe failure classification


### Constraints
    - id is the primary key.
    - user_id references the Identity user.
    - asset_id references an Asset when applicable.
    - type must represent a supported analysis type.
    - status must represent a valid analysis state.
    - Sensitive raw targets must never be persisted.
    - completed_at must not be set before execution starts.


## analysis_results

Represents the final normalized result of an analysis.

### Fields

Field	         Type	          Constraints	              Description

id	         UUID	          PK	                      Unique result identifier
analysis_id	 UUID	          FK, UNIQUE, NOT NULL	      Related analysis
summary	         TEXT	          NOT NULL	              Human-readable result summary
risk_score	 INTEGER	  NOT NULL	              Normalized risk score
risk_level	 VARCHAR	  NOT NULL	              Risk classification
created_at	 TIMESTAMPTZ	  NOT NULL	              Result creation timestamp

### Constraints

    - analysis_id references analyses.
    - One analysis has at most one final result in V1.
    - risk_score must remain within the defined score range.
    - The client cannot directly create or modify the risk score.
    - Results are immutable from the client perspective.


## analysis_indicators

Represents individual security findings.

### Fields

Field	                Type	                Constraints	               Description

id	                UUID	                PK	                       Unique indicator identifier
analysis_result_id	UUID	                FK, NOT NULL	               Related result
type	                VARCHAR	                NOT NULL	               Indicator type
severity	        VARCHAR	                NOT NULL	               Severity level
title	                VARCHAR	                NOT NULL	               Short indicator title
description	        TEXT	                NOT NULL	               Explanation
value	                JSONB	                NULL	                       Structured indicator value
evidence	        JSONB	                NULL	                       Supporting evidence
created_at	        TIMESTAMPTZ	        NOT NULL	               Creation timestamp

### Constraints
     - analysis_result_id references analysis_results.
     - severity must be a supported severity level.
     - Sensitive evidence must be minimized.
     - Evidence must never contain secrets such as plaintext passwords.


# Analysis Types

Initial supported values:

	URL
	PASSWORD
	FILE
	ACCOUNT_COMPROMISE

The implementation should use a controlled enumeration rather than accepting arbitrary strings from clients.


# Analysis Statuses

Initial supported values:

	REQUESTED
	QUEUED
	RUNNING
	COMPLETED
	FAILED
	CANCELLED

State transitions must be validated by the application layer.


# Indicator Severity

Supported values:

	INFO
	LOW
	MEDIUM
	HIGH
	CRITICAL


Relationships

User -> Analysis

One user can request many analyses.

	User (1 ---- N) Analysis

Asset -> Analysis

One asset may have many analyses.

	Asset (1 ---- N) Analysis

The relationship is optional because one-time analyses may not belong to a persistent asset.


Analysis -> Analysis Result

One analysis has at most one final result in V1.

	Analysis (1 ---- 0..1) AnalysisResult

Analysis Result -> Indicators

One result can contain many indicators.

	AnalysisResult (1 ---- N) Indicator


# Sensitive Data Rules
### Password

Raw passwords are never persisted.


### URL

Sensitive URL components such as credentials and tokens must be sanitized before persistence.


### File

Uploaded files must never be executed by the analysis service.

Safe metadata and cryptographic hashes may be persisted where justified.


### Account Compromise

External intelligence responses must be minimized and stored only when necessary.


### Indexing Strategy

The initial implementation should consider indexes on:

	- analyses.user_id
	- analyses.asset_id
	- analyses.type
	- analyses.status
	- analyses.created_at
	- analysis_results.analysis_id
	- analysis_indicators.analysis_result_id
	- analysis_indicators.severity

Composite indexes will be introduced only when supported by actual query patterns.


## Important Architectural Decision

The Analysis domain must not duplicate Identity or Asset Management data.

It references those domains through identifiers and well-defined interfaces.


	Identity ---------> Analysis ----------> Asset Management
	          user_id            asset_id


The database schema must preserve these boundaries as much as practical.
