# Modular UX BRD (Python + Streamlit)

## 1) Business Requirement Document (BRD)

### 1.1 Purpose
Build a complex input UX as a collection of mini form parts (modules) that can be developed independently by different contributors, tested independently (human and AI-agent driven), and then embedded into one unified Streamlit experience.

### 1.2 Vision
Deliver a modular form platform where:
- One team/member can build Part A and validate it in isolation.
- Another team/member can build Part B in parallel.
- Both parts are composable into a single host UX without rework.

### 1.3 Technology Constraints (Confirmed)
- Language: Python
- UI Framework: Streamlit
- Database: PostgreSQL
- DB Hosting: Aiven PostgreSQL

### 1.4 Problem Statement
Complex forms with dependency-heavy validations become slow to build and hard to maintain when implemented as one monolith. We need a modular architecture that supports parallel development, isolated validation, and controlled integration.

---

## 2) Goals and Objectives

### 2.1 Primary Goals
1. Support independent development of form mini-parts.
2. Enable isolated testing of each mini-part by humans and AI agents.
3. Embed mini-parts into a host Streamlit UX with predictable behavior.
4. Centralize data persistence and rule consistency via PostgreSQL on Aiven.

### 2.2 Success Criteria
- Any module can run standalone with mock/real dependencies.
- Modules can be plugged into host UX through a standard interface contract.
- Cross-module dependencies and validations work consistently in host mode.
- Data captured in modules is persisted in PostgreSQL with audit-ready structure.

---

## 3) Scope

### 3.1 In Scope
- Modular form architecture definition.
- Streamlit host app for embedding modules.
- Module contract (input/output/state/validation hooks).
- Synchronous and deferred validation handling.
- Shared persistence layer in Aiven PostgreSQL.
- Standalone module testing harness.

### 3.2 Out of Scope (Initial Phase)
- Native mobile apps.
- Multi-tenant billing logic.
- Advanced analytics dashboards (beyond basic operational metrics).

---

## 4) Users and Stakeholders

### 4.1 User Types
- End users filling complex forms.
- Form designers/product owners defining dependencies.
- Developers building mini-parts.
- QA/human testers and AI agents executing module test scenarios.

### 4.2 Stakeholders
- Product owner
- Engineering lead
- Module developers
- QA lead
- Data/compliance representative

---

## 5) Functional Requirements

### FR-1 Modular Composition
- The system shall support multiple independently developed form modules.
- The host Streamlit UX shall embed modules in configurable sequence.

### FR-2 Standard Module Contract
Each module shall expose:
- `module_id`
- `render(context) -> ui_state_delta`
- `validate(context) -> validation_result`
- `serialize() -> payload`
- `load(payload)`

### FR-3 Dependency Management
- Modules shall read dependency values from shared context.
- Changes in upstream modules shall trigger downstream re-validation.
- Dependency graph shall prevent circular dependencies.

### FR-4 Validation Framework
- Field-level validation (required, type, range, format).
- Cross-field validation within a module.
- Cross-module validation across dependent modules.
- Blocking vs non-blocking validation severity.

### FR-5 Standalone Module Runtime
- Any module shall run independently in a local Streamlit test harness.
- Harness shall support mock context injection.
- Harness shall support synthetic dependency snapshots for AI-agent testing.

### FR-6 Data Persistence
- User session data, module payloads, and validation outcomes shall be stored in PostgreSQL.
- Database shall be hosted in Aiven PostgreSQL.
- Writes shall support transactional integrity for multi-module submit.

### FR-7 Embedding and Integration
- Host UX shall dynamically discover/register available modules.
- Host UX shall render module output and validation status consistently.
- Integration shall not require module code rewrites if contract is respected.

### FR-8 Observability
- Capture structured logs for module load, validation failures, and submit events.
- Record module version metadata for traceability.

---

## 6) Non-Functional Requirements

### NFR-1 Maintainability
- Modules must be loosely coupled and independently deployable in code.

### NFR-2 Testability
- Every module must be testable standalone by human testers and AI agents.

### NFR-3 Performance
- Initial host screen load target: <= 2 seconds under normal load.
- Module validation feedback target: <= 300 ms for local rule checks.

### NFR-4 Reliability
- No data loss on partial failures; transaction rollback for failed final submission.

### NFR-5 Security
- Use secure connection (`sslmode=require`) to Aiven PostgreSQL.
- Secrets managed via environment variables / secure secret manager.
- Input sanitization and parameterized queries only.

### NFR-6 Scalability
- Architecture should support growing module count without redesign.

---

## 7) High-Level Architecture

### 7.1 Components
1. Streamlit Host Application
2. Module Registry
3. Individual Form Modules (mini-parts)
4. Shared Validation Engine
5. Persistence Adapter (PostgreSQL/Aiven)
6. Standalone Module Harness

### 7.2 Data Flow
1. Host loads enabled modules from registry.
2. Module renders UI and updates shared context.
3. Validation engine evaluates local and cross-module rules.
4. On submit, host composes payload and persists atomically to PostgreSQL.

---

## 8) Delivery Model (Parallel Team Development)

### 8.1 Development Pattern
- Each contributor owns one mini-part in a separate module directory.
- Module owner delivers:
	- module code
	- contract-compliance tests
	- standalone harness test scenarios

### 8.2 Integration Pattern
- Integrator registers module in host registry.
- Host executes integration smoke checks.
- Cross-module dependency tests are run before release.

### 8.3 Testing Pattern
- Human testing: exploratory and scripted scenarios.
- AI-agent testing: deterministic scenario packs with expected outcomes.
- Regression suite includes standalone + integrated paths.

---

## 9) Data and Database Requirements (Aiven PostgreSQL)

### 9.1 Core Data Entities
- `form_session`
- `module_submission`
- `validation_event`
- `audit_event`

### 9.2 Data Integrity
- Foreign keys between session and module submissions.
- Idempotent submission key per final submit request.
- Timestamps and actor metadata for auditability.

### 9.3 Operational Requirements
- Backup and restore policy aligned with Aiven defaults + business RPO/RTO.
- Migrations managed through versioned schema tooling.

---

## 10) Risks and Mitigations

- Risk: Contract drift across teams.
	- Mitigation: Contract tests mandatory in CI.
- Risk: Dependency loops between modules.
	- Mitigation: Enforce DAG validation in registry.
- Risk: Integration surprises despite standalone passing.
	- Mitigation: Shared integration harness and smoke suite.
- Risk: DB contention on final submission.
	- Mitigation: Transaction tuning + index strategy + retry policy.

---

## 11) Acceptance Criteria (Release Gate)

1. At least two independently developed modules run standalone and in host UX.
2. Cross-module dependency validation is demonstrably functional.
3. End-to-end submission persists correctly in Aiven PostgreSQL.
4. Human and AI-agent test suites pass for both standalone and integrated modes.
5. Logging and audit entries are available for failed and successful submissions.

---

## 12) Next Build Step

Implement the project skeleton with:
- Streamlit host app
- module interface base class/protocol
- example modules (`part_a`, `part_b`)
- registry and dependency graph validator
- PostgreSQL repository layer for Aiven
- standalone module test harness
