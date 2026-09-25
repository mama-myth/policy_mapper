# Phase 1 Demonstration Narrative — Policy-to-Code Mapper

## Overview
This demo script outlines a 2–3 minute walkthrough demonstrating the core user experience and human-centered design of **Policy-to-Code Mapper** using the Phase 1 Mock Policy Guidance Prototype.

---

## 1. Scenario Introduction (0:00 – 0:45)
**Presenter:**
> "Hello! Today we are demonstrating **Policy-to-Code Mapper**, a context-aware IDE guidance system designed to bridge the gap between organizational security policies and everyday software development.
>
> In many organizations, developers write code under tight deadlines. Security and compliance policies—such as secure logging guidelines or GDPR requirements—are stored in disconnected intranet wikis or long PDFs. As a result, policy considerations are often identified late in code reviews, security audits, or after incidents."

---

## 2. Point-of-Action Developer Workflow (0:45 – 1:30)
**Presenter:**
> "Let's look at a common coding scenario in Python. Here, a developer is implementing a authentication function in `examples/unsafe_credential_logging.py`:
>
> ```python
> def login_user(username, password):
>     logger.info("Login attempt for %s with password %s", username, password)
>     return True
> ```
>
> Notice that the raw `password` argument is logged directly. Instead of waiting for a security review or blocking the developer from saving their code, Policy-to-Code Mapper intervenes at the **point of action**."

---

## 3. Advisory Guidance & Policy Traceability (1:30 – 2:30)
**Presenter:**
> "Policy-to-Code Mapper surfaces an advisory guidance prompt right inside the developer's workspace.
>
> Let's view the generated Guidance Card (accessible via `/mock-guidance`):
>
> 1. **Potential Consideration:** The system flags that the log statement appears to include authentication credentials.
> 2. **Relevant Internal Policy:** It cites `SEC-LOG-001: Sensitive Data Must Not Be Logged`.
> 3. **Why It Matters:** It explains that logging credentials can expose secrets through monitoring systems, support tools, or backups.
> 4. **Supporting Regulatory Context:** It references `GDPR Article 32 (Security of processing)` as supporting context, without making legal declarations or legal judgments.
> 5. **Suggested Developer Action & Safer Example:** It provides an immediate, actionable safe code alternative:
>    `logger.info("Login attempt for user_id=%s", user_id)`
> 6. **Traceability Chain:** A transparent chain connects `password → logger.info()` to `SEC-LOG-001` and `GDPR Article 32`."

---

## 4. Key Takeaways & Research Values (2:30 – 3:00)
**Presenter:**
> "Notice the tone and boundaries:
> - The guidance is **advisory, non-blocking, and supportive**.
> - The system **never** declares 'This code is illegal' or 'GDPR violation detected'.
> - Developers retain full autonomy to inspect the policy, view safer examples, or dismiss the guidance.
>
> This completes the Phase 1 prototype demonstration."
