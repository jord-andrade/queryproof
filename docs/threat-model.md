# Threat model

This document describes the security and privacy boundary of the public demo.

## Assets

- integrity of the answer and its evidence;
- availability of the low-cost public endpoint;
- assurance that no private record enters the repository or response;
- source and deployment integrity.

## Trust boundaries

| Boundary | Untrusted input | Control |
|---|---|---|
| Browser → API | Question text and headers | Pydantic validation, 300-character maximum |
| Classifier → executor | Selected intent | Only a `QuerySpec` from the in-process catalog is accepted |
| Repository → dataset | Committed CSV | Seeded regeneration, hash evidence, privacy test |
| API → browser | Error details | Stable generic exception response |

## Primary abuse cases

### SQL injection or arbitrary execution

User text is never concatenated into SQL. The only executable statements are
constant strings in `queryproof/catalog.py`. Unsupported questions return before
the database connection is created.

### Resource exhaustion

Question length is bounded, the dataset contains 960 rows, the catalog has six
aggregate queries, DuckDB uses one thread, and API output is capped at 50 chart
rows. Platform-level function limits provide an additional bound.

### Accidental personal-data publication

The dataset is created from code and excludes identity, contact, and free-text
fields by design. CI checks the schema and scans public textual values for email
and phone patterns. Screenshots use only this fixture.

### Misleading evidence

Each successful response includes the exact SQL, source label, SHA-256 digest,
rows scanned, rows returned, and a query ID. CI verifies that all 24 evaluation
questions map to their declared intent.

### Information leakage through errors

The public exception handler omits stack traces and internal paths. Response
headers include a bounded request identifier and processing duration for support
without returning request content.

## Out of scope for this version

- authentication and tenant isolation;
- arbitrary SQL, Python, uploads, or user-provided datasets;
- write queries or persistent databases;
- confidential, regulated, or production operational data;
- guarantees against platform-wide denial of service.

A production multi-tenant implementation would add per-principal quotas,
authentication, durable lineage, workload isolation, audit retention, and
platform monitoring.
