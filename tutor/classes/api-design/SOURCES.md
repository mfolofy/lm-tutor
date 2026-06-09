# SOURCES — api-design (REST, GraphQL, and gRPC API Design Standards)

All rules in `class.yaml` derive from the foundational REST dissertation, major
industry API design guides, and the specifications for JSON:API, OpenAPI, GraphQL,
and gRPC. Every rule cites a specific standard or authoritative guide. No rule
exists without a source.

## Primary standards

- **Fielding, Roy T. — Architectural Styles and the Design of Network-based
  Software Architectures** (Ph.D. dissertation, UC Irvine, 2000).
  <https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm>
  - REST architectural constraints (uniform interface, statelessness, cacheability,
    layered system, code-on-demand)
  - Hypermedia as the Engine of Application State (HATEOAS)
  - All resource-naming, http-methods, hateoas, and content-type rules reference
    Fielding's REST constraints.

- **Google API Design Guide** (google.aip.dev / AIP). Google, 2017-ongoing.
  <https://google.aip.dev/>
  - Resource-oriented design (AIP-121), standard methods (AIP-131-135),
    custom methods (AIP-136), pagination (AIP-158), errors (AIP-193),
    versioning (AIP-21), long-running operations (AIP-151)
  - All resource-naming, pagination, error-format, and versioning rules reference
    the Google AIPs.

- **Microsoft REST API Guidelines**. Microsoft, 2016-ongoing.
  <https://github.com/microsoft/api-guidelines>
  - URL structure, HTTP methods, status codes, versioning, pagination,
    filtering/sorting, error responses, CORS, rate limiting
  - All filtering-sorting, status-codes, cors-policy, and authentication rules
    reference the Microsoft guidelines.

## Specification references

- **JSON:API 1.1 Specification**. jsonapi.org, 2024.
  <https://jsonapi.org/format/>
  - Resource identifier/document structure, error objects, pagination links
    (first/prev/next/last), sparse fieldsets, filtering, sorting
  - All error-format, pagination, hateoas, and filtering-sorting rules reference
    the JSON:API document structure for consistency.

- **OpenAPI 3.1 Specification**. OpenAPI Initiative, 2021.
  <https://spec.openapis.org/oas/v3.1.0>
  - API description format: paths, operations, parameters, request/response bodies,
    schemas, security schemes, links
  - All api-documentation, content-type, and authentication rules reference
    OpenAPI's semantic model for API descriptions.

- **GraphQL Specification (October 2021)**. GraphQL Foundation.
  <https://spec.graphql.org/October2021/>
  - Type system, naming conventions (PascalCase types, camelCase fields),
    input types, enum values (UPPERCASE), query/mutation separation,
    subscription model
  - All graphql-naming rules reference the GraphQL spec.

- **gRPC Specification**. gRPC Authors / CNCF.
  <https://grpc.io/docs/guides/>
  - Service definition (Protocol Buffers), package naming, message field numbering,
    streaming patterns (unary, server-streaming, client-streaming, bidirectional),
    error handling (google.rpc.Code, google.rpc.Status)
  - All grpc-patterns rules reference the gRPC spec.

## Supporting references

- **Stripe API Reference** (stripe.com/docs/api).
  <https://stripe.com/docs/api>
  - Idempotency keys (Idempotency-Key header), pagination (cursor-based),
    error format, rate limiting, versioning
  - Industry exemplar for idempotency, pagination, and error-format rules.

- **GitHub REST API Documentation** (docs.github.com/en/rest).
  <https://docs.github.com/en/rest>
  - Pagination (Link header, page/cursor pagination), media types (version via
    Accept header), rate limiting (X-RateLimit-* headers), HATEOAS links
  - Industry exemplar for versioning, rate-limiting, and hateoas rules.

- **Twilio API Best Practices** (twilio.com/docs/usage/api-request).
  <https://www.twilio.com/docs/usage/api-request>
  - Idempotency keys, rate limiting (Retry-After), pagination, error responses
  - Industry exemplar for idempotency and rate-limiting rules.

- **Zalando RESTful API Guidelines** (opensource.zalando.com/restful-api-guidelines).
  <https://opensource.zalando.com/restful-api-guidelines/>
  - Resource naming, HTTP methods, status codes, pagination, error handling,
    security, documentation requirements
  - Supplementary reference for resource-naming and authentication rules.

- **RFC 7231 — HTTP/1.1 Semantics and Content**. IETF, 2014.
  <https://datatracker.ietf.org/doc/html/rfc7231>
  - HTTP methods (GET, POST, PUT, DELETE, PATCH), status codes, headers
  - All http-methods and status-codes rules reference RFC 7231 semantics.

- **RFC 7807 — Problem Details for HTTP APIs**. IETF, 2016.
  <https://datatracker.ietf.org/doc/html/rfc7807>
  - Standard error response format: type, title, status, detail, instance
  - All error-format rules follow RFC 7807's problem details specification.

- **RFC 6585 — Additional HTTP Status Codes**. IETF, 2012.
  <https://datatracker.ietf.org/doc/html/rfc6585>
  - Status codes: 428 (Precondition Required), 429 (Too Many Requests),
    431 (Request Header Fields Too Large), 511 (Network Authentication Required)
  - Status-code rule references 429 for rate limiting.

## Rule-to-standard map

| Rule ID | Primary Standard | Secondary Sources | Notes |
|---------|-----------------|-------------------|-------|
| `rest-resource-naming` | Google AIP-121 (Resource-oriented design) | Fielding REST, Microsoft Guidelines, Zalando | Plural nouns, no verbs, consistent casing, max 3 levels |
| `http-methods` | RFC 7231 — HTTP Methods | Fielding REST, Google AIP-131 to AIP-135 | GET read-only; POST create; PUT replace; PATCH partial |
| `status-codes` | RFC 7231 — Status Codes | RFC 6585, Microsoft Guidelines | Precisely chosen codes; no 200 for errors |
| `error-format` | RFC 7807 — Problem Details | JSON:API, Google AIP-193, Stripe API | Consistent code+message+details+request_id+timestamp |
| `versioning` | Google AIP-21 (API Versioning) | Microsoft Guidelines, GitHub API | URL path or Accept header; no versionless public APIs |
| `idempotency` | Stripe API (Idempotency-Key) | Google AIP-151, Twilio Best Practices | PUT/DELETE inherently idempotent; POST supports key |
| `pagination` | Google AIP-158 (Pagination) | JSON:API, GitHub API, Stripe API | Cursor-based preferred; default 20, max 100 |
| `authentication` | OpenAPI 3.1 Security Schemes | Microsoft Guidelines, OAuth 2.0 (RFC 6749) | Bearer tokens in Authorization header; revocable, time-limited |
| `content-type` | RFC 7231 — Content Negotiation | Google AIP, OpenAPI 3.1 | JSON preferred; Content-Type and Accept required |
| `cors-policy` | Microsoft REST Guidelines — CORS | Fetch Standard (WHATWG) | Explicit origins; no wildcard with credentials |
| `hateoas` | Fielding REST (Hypermedia) | JSON:API, GitHub API | Self/next/prev/related links in responses |
| `api-documentation` | OpenAPI 3.1 Specification | Google AIP, Microsoft Guidelines | Every endpoint documented; schemas, params, auth |
| `deprecation-policy` | Google AIP-36 (Deprecation) | Sunset header (RFC 8594) | Deprecation/Sunset headers; migration guide; 6-month transition |
| `rate-limiting` | Microsoft API Guidelines | RFC 6585 (429), GitHub API, Stripe | Retry-After on 429; X-RateLimit-* headers on all responses |
| `filtering-sorting` | Google AIP-132 (Standard Query Parameters) | JSON:API, Microsoft Guidelines | Consistent operator syntax; documented fields |
| `graphql-naming` | GraphQL Spec (October 2021) | Relay Connection Spec, DataLoader | PascalCase types, camelCase fields, UPPERCASE enums; input types; connection pagination |
| `grpc-patterns` | gRPC Spec / Protocol Buffers | google.rpc.Code / google.rpc.Status | Package naming; field numbering; streaming; canonical status codes |
| `request-validation` | Google AIP — Input Validation | OpenAPI 3.1 — Schema Validation | Validate at boundary before business logic |

## Coverage honesty

**Layer 1 (regex) rules** cover codifiable API anti-patterns with high precision:
verbs embedded in URL paths (createUser, getOrders), mutating operations via GET,
error responses exposing stack traces, unversioned API paths, API keys leaked in
query strings, PascalCase violations in GraphQL type names, and 200 OK wrapping
errors. These patterns have a unique textual signature that a single regex can
capture with near-zero false positives in practice.

**Teaching-only rules (no checker)** cover standards that require semantic
judgement beyond regex scope: pagination strategy choice, idempotency correctness,
CORS policy semantics, rate limit configuration quality, HATEOAS completeness,
documentation coverage, deprecation policy adherence, and gRPC error code
appropriateness. These are deferred to the LLM judge (Layer 2, Phase 1) or
specialized tooling (OpenAPI lint, protobuf lint).

The honest coverage boundary:
- ~33% of rules (6/18) are codifiable at Layer 1 via regex
- ~67% (12/18) need human or LLM judgement — documented as teaching-only rules
  with no checker

## Verification

Each rule with a `check_regex` is FAIL/PASS tested in
`tests/test_api_design.py`. Teaching-only rules (no checker) are tested for
content presence only. A rule cannot ship without its test pair — see CONTRIBUTING.md.
