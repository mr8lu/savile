# DOTSP Hackathon: MERCER Problem Statement

## The Problem Statement
**"How might we govern and measure the efficacy of Enterprise AI logic (Prompts, Personas, and Frameworks) across thousands of practitioners, ensuring that our usage of OpenAI models is auditable, structurally secure, and mathematically cost-effective?"**

---

## 1. The Context
In the rapid adoption of GenAI within the Deloitte GPS and Commercial practices, "Prompt Engineering" has emerged as a critical, yet entirely ungoverned, discipline. Today, a brilliant consultant crafts a highly effective prompt that unlocks a billion-dollar insight. Tomorrow, that prompt is gone—lost in a Teams chat history, saved in an isolated Word document, or hardcoded directly into unversioned Python scripts.

## 2. The Core Pain Points (The "Ghosts in the Machine")

### A. Prompt Drift (The Technical Debt)
Prompts are treated as ephemeral text rather than **first-class code artifacts**. When an underlying model updates (e.g., GPT-4 to GPT-4o), previously functional prompts can suddenly hallucinate or fail. Because prompts are not version-controlled or regression-tested, this "drift" goes unnoticed until it hits a client deliverable.

### B. Blind Spending (The FinOps Gap)
Deloitte invests heavily in OpenAI API tokens. However, without centralized governance, there is zero visibility into which organizational prompts are cost-effective and which are wastefully token-heavy. Teams are frequently "re-prompting" the exact same use cases (e.g., Code Review, SOW Generation) in silos, leading to massive redundant API spend.

### C. Shadow AI (The Security Risk)
The rise of "Agentic AI" (agents taking action on behalf of a human) introduces severe InfoSec hurdles. When logic and tool-access are hardcoded locally, there is no centralized Identity and Access Management (IAM) to ensure an AI agent only executes tools the human is authorized to use.

---

## 3. The Objective
We need a **Centralized AI Governance Platform** that bridges the gap between technical execution and business oversight. The solution must:
1.  Provide a **Sovereign Logic Vault** to version-control intelligence.
2.  Utilize **OpenAI (GPT-4o)** not just for generation, but as an *Auditor* to grade and rank prompts before they are deployed globally.
3.  Implement an **Enterprise Gateway** with Role-Based Access Control (RBAC) to secure agentic tool execution.
