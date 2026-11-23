# Production Architecture Review — Customer CLV Analysis

**Work item:** W12D1  
**Review status:** Design review prepared; production deployment not verified  
**Overall assessment:** Prototype / pre-production

## 1. Executive summary
The Customer CLV Analysis project demonstrates an analytical workflow for data preparation, customer segmentation, future-revenue prediction experiments, business-impact analysis, and stakeholder-facing reporting. The available evidence is not sufficient to call it production-ready.

The highest-priority gaps are data-quality controls, reproducibility, model validation/governance, customer-data security, monitoring, and deployment/rollback procedures. The recommended target architecture separates ingestion, validation, curated storage, feature generation, model training, artifact management, scoring, user interface, and observability.

## 2. Scope and known evidence
Known project facts from prior project work:
- 1,000 transactions and 200 customers.
- Transaction period: 2 July 2024 to 28 June 2026.
- 42 date inconsistencies were reported during data-quality checks.
- Customer IDs were reported as matched across the profile/transaction check.
- K-Means used Recency and Monetary features; selected K=3.
- Reported silhouette score: 0.4175.
- Segment counts: 62 High-Value, 92 Regular, 46 At-Risk.
- Latest reported prediction validation: MAE ₹8,934.36 and RMSE ₹10,831.92.
- A Streamlit-facing experience was included in the project scope.

Not verified: live repository structure, actual deployment platform, database topology, authentication, authorization, CI/CD, runtime telemetry, traffic, cloud cost, and legal/compliance obligations. The logical current-state flow below is reconstructed from known project context, not verified source code.

## 3. Current logical architecture
1. Customer profile and transaction data are collected.
2. Cleaning and data-quality checks produce analysis-ready datasets.
3. Customer-level features, including Recency and Monetary, are calculated.
4. K-Means produces three customer segments.
5. A future-revenue prediction experiment is trained and evaluated.
6. Results are summarized in charts, business insights, and a planned Streamlit-facing interface.

This describes the analytical flow only; it does not claim the steps are automated services today.

## 4. Recommended target architecture
| Layer | Responsibility | Required controls |
|---|---|---|
| Data sources | Approved customer/profile and transaction feeds | Source ownership and schema contracts |
| Ingestion | Land immutable raw snapshots | Idempotency, retries, audit metadata |
| Validation | Check schema, keys, dates, nulls, duplicates, ranges | Quarantine bad batches and alert owner |
| Curated storage | Store cleaned, versioned analytical tables | Least privilege, encryption, retention |
| Feature pipeline | Generate customer-level features | Shared train/serve transformations |
| Training/evaluation | Train segmentation and prediction models | Reproducible runs and time-based validation |
| Artifact registry | Store approved model and preprocessing artifacts | Versioning, approval state, rollback |
| Scoring/API | Produce approved batch scores or predictions | Authentication and input validation |
| UI/BI | Present insights to approved users | Role-based access and safe exports |
| Observability | Track pipeline, data, model, and service health | Metrics, alerts, incident ownership |

### Architecture principles
- Keep raw source data immutable; separate raw, curated, and feature layers.
- Make pipeline stages repeatable and safe to rerun.
- Version datasets, feature definitions, code, models, and evaluation results.
- Use identical feature transformations for training and inference.
- Do not expose unrestricted customer-level data or database credentials to the UI.
- Treat predictions as decision support, not unquestioned automated decisions.
- Separate development, staging, and production environments.

## 5. Risk assessment
| Area | Risk | Rationale | Priority |
|---|---|---|---|
| Data quality | High | 42 date inconsistencies were previously reported; date errors affect recency and future windows | P0 |
| Reproducibility | High | Undocumented/manual steps can cause inconsistent outputs | P0 |
| Model validation | High | Current metrics do not establish production usefulness or full-lifetime CLV accuracy | P0 |
| Security/privacy | High | Customer-level data requires controlled access and secure secrets | P0 |
| Monitoring | High | Drift, stale outputs, segment movement, and service failures may go unnoticed | P1 |
| Deployment/rollback | High | No verified release or rollback process is evidenced | P1 |
| Scalability | Medium | 200 customers and 1,000 transactions do not demonstrate production capacity | P1 |
| Business controls | Medium | Scenario uplift must not be reported as realized revenue | P1 |

## 6. Model and analytics governance
### Segmentation
The reported K=3 solution achieved silhouette 0.4175. This is an experimental result, not proof of highly separated or stable production segments. Before release:
- Define business meaning and action rules for each segment.
- Test cluster stability across time windows and resampled data.
- Monitor segment sizes and customer migration.
- Define handling for new customers and missing features.
- Version scaling, feature definitions, cluster centers, and label mapping.
- Do not describe At-Risk as confirmed churn without validated churn labels.

### Future-revenue prediction
The latest reported MAE was ₹8,934.36 and RMSE ₹10,831.92. These must be interpreted against the target horizon, revenue distribution, and baseline. The available evidence does not establish a full-lifetime CLV model.
- Use time-based train/validation/test splits to avoid future leakage.
- Compare against simple baselines.
- Report metrics with target horizon, sample count, and evaluation dates.
- Evaluate errors by segment and value band.
- Define retraining triggers and business approval thresholds.
- Record model version and input snapshot for every scoring run.

## 7. Security and privacy
- Keep credentials in environment-specific secret management; never commit `.env`, passwords, tokens, or private keys.
- Use separate service identities and least-privilege database permissions.
- Encrypt data in transit and at rest where supported.
- Restrict customer-level views and exports by role.
- Log administrative access and exports without logging sensitive values.
- Define retention/deletion rules and approved data purpose.
- Use synthetic or masked data in development and tests.
- Enforce authorization server-side; UI hiding is not access control.
Applicable legal requirements must be confirmed by the organization; this is not a legal determination.

## 8. Reliability and operations
- Schedule or trigger pipelines with bounded retries and idempotent loads.
- Track each batch as started, completed, failed, or quarantined.
- Alert on stale data, failed jobs, schema changes, abnormal row counts, and quality breaches.
- Provide health checks and structured logs for serving components.
- Apply timeouts, request-size limits, and safe error handling.
- Back up persistent data and approved artifacts; test restoration.
- Retain a last-known-good model and application release for rollback.
- Document owners, support contacts, and incident escalation.

## 9. Performance and scalability
Do not infer capacity from prototype dataset size. Agree on expected customer count, transaction volume, refresh cadence, concurrent users, response-time target, and retention. Load-test full refreshes, feature generation, scoring, dashboard/API reads, and exports. Start with batch scoring unless measured requirements justify online prediction or distributed infrastructure.

## 10. Implementation roadmap
**Phase 1 — Stabilize data:** formalize schemas, resolve or quarantine the 42 date issues, automate quality checks, and make cleaning/features deterministic.

**Phase 2 — Govern models:** add time-based evaluation and baselines, persist run metadata and artifacts, document segment meanings, and agree on approval thresholds.

**Phase 3 — Secure application:** separate UI from storage/model execution, add authentication and role-based authorization, move secrets out of source control, and audit exports.

**Phase 4 — Operate reliably:** add monitoring and alerts, document runbooks, test backup/restore and rollback, load-test representative volumes, and release through staging.

## 11. Production release gates
Do not label the system production-ready until:
1. Data-quality failures are visible, handled, and below agreed thresholds.
2. Training and scoring are reproducible from versioned inputs and code.
3. Model evaluation is time-aware and approved against a business baseline.
4. Customer data access is authenticated, authorized, and auditable.
5. Monitoring, alerting, backup/restore, and rollback are tested.
6. Performance is measured against agreed service targets.
7. Business owners approve segment definitions and prediction use.

## 12. Conclusion
The project is a useful analytical prototype with stakeholder-facing outputs. Production readiness requires more than hosting a dashboard: the data and model workflow must become reproducible, secure, measurable, and supportable. Prioritize data quality, model validation, access controls, and operational ownership before production release.
