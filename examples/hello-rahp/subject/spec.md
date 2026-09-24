# Hello RAHP sample specification

## Purpose

A service accepts a request from an authenticated operator and records a durable approval.

## Requirements

1. Only an authenticated operator may submit an approval.
2. The approval record must identify the subject, the approving operator, and the effective time.
3. Repeating the same approval request must not create a second authoritative approval record.
4. If the service cannot determine whether an approval already exists, it must not report the request as successfully approved.

## Deliberate assurance questions

A RAHP review can ask whether the requirements provide enough evidence to support the intended authorization, auditability, idempotency and indeterminate-state claims.

This sample is intentionally small. It is not a production specification and does not require DPIP or the Trust Protocol Interop Lab.
