---
name: multi-agent-swarm
version: 1.0.0
category: persona
description: Orchestrates a strict 3-phase multi-agent swarm with Parallel Pathfinding
  & Fast Pivoting for building complex features.
---

# Multi-Agent Swarm Orchestration

Use this skill whenever you are asked to build a complex feature. You must orchestrate a strict 3-phase multi-agent swarm with **Parallel Pathfinding & Fast Pivoting**:

## Core Efficiency Rules:
- **Parallel Processing:** Maximize concurrency. Always invoke independent sub-agents in parallel during each phase.
- **Multi-Swarm Orchestration:** If a request involves multiple distinct problems or independent features, spin up separate, concurrent swarms to tackle each problem simultaneously. Do not serialize independent workloads.
- **Dynamic Pathfinding (Fast Pivot):** Do not get stuck on a single failing approach. If an implementation, debugging session, or investigation takes too much time or hits a dead-end (e.g., >3 failed attempts), **drop it immediately**. Re-evaluate the architecture and pivot to an alternative route or library if multiple exist.

## The 3-Phase Workflow

1. We are going to implement a new feature: [FEATURE_NAME / BRIEF DESCRIPTION].
2. To ensure high quality and velocity, we will use a strict 3-Phase Multi-Agent Swarm workflow. Please orchestrate the following sub-agents to complete the entire lifecycle.

### Phase 1: Planning (Run Concurrently)
Invoke `@role-pm`, `@role-analyst`, and `@role-architect` in parallel to plan the feature.
- ** `@role-pm`:** Write the PRD (Scope, Goals, Business Value). Save to `internal-docs/[FEATURE_NAME]/01_prd.md`.
- ** `@role-analyst`:** Write Functional Requirements (Flow steps, data mapping, acceptance criteria). Save to `internal-docs/[FEATURE_NAME]/02_functional_requirements.md`.
- ** `@role-architect`:** Write the Technical Design (Architecture, Pydantic/DB schemas, system boundaries). **Must explicitly identify primary technical paths and potential fallback routes.** Save to `internal-docs/[FEATURE_NAME]/03_technical_design.md`.

Wait for Phase 1 to complete before moving to Phase 2.

### Phase 2: Development (Run Concurrently with Pathfinding)
Invoke `@role-dev`, `@role-solo-dev`, and `@role-ux-designer` in parallel to build the feature based on Phase 1 docs.
- ** `@role-dev`:** Implement foundational database schemas, repository layers, and core data models.
- ** `@role-solo-dev`:** Implement the core business logic, services, API endpoints, or background jobs. **Rule: If a specific library or logic path fails repeatedly, pivot to the fallback route.**
- ** `@role-ux-designer`:** (If applicable) Update the frontend UI/components to expose the new functionality to the user.

Wait for Phase 2 to complete before moving to Phase 3.

### Phase 3: Validation (Run Concurrently)
Invoke `@role-solo-dev` (or QA automation), `@role-creative-problem-solver`, and `@role-qa` in parallel.
- ** `@role-solo-dev`:** Write and execute automated integration/unit tests for the new code. Ensure `pytest` (or relevant test runner) passes. If tests reveal deep structural flaws, trigger a fast pivot rather than endless patching.
- ** `@role-creative-problem-solver`:** Analyze the end-to-end implementation for hidden edge cases, systemic risks, or architecture gaps. Document findings in `internal-docs/[FEATURE_NAME]/04_validation_analysis.md`. Do not write code.
- ** `@role-qa`:** Validate the code against the Acceptance Criteria. Once tests pass, update the `CHANGELOG.md` and execute a `git commit` summarizing the work. Do not push.

Please begin with Phase 1.
