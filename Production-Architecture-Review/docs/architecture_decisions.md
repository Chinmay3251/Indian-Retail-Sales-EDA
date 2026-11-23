# Architecture Decision Records

## ADR-001 — Separate raw, curated, and feature data
**Decision:** Preserve immutable raw snapshots and create separately validated curated and feature datasets.  
**Reason:** Supports auditability, reruns, debugging, and consistent training.  
**Trade-off:** Requires additional storage and pipeline management.

## ADR-002 — Version model artifacts and preprocessing together
**Decision:** Treat preprocessing, feature definitions, cluster label mapping, and model files as one versioned release unit.  
**Reason:** A model without matching transformations can produce inconsistent outputs.  
**Trade-off:** Requires artifact metadata and release discipline.

## ADR-003 — Prefer batch scoring until online latency is required
**Decision:** Start with scheduled batch scoring unless a confirmed use case requires real-time predictions.  
**Reason:** The known workflow is analytics/reporting oriented; online serving adds operational complexity.  
**Trade-off:** Results are only as fresh as the agreed batch schedule.

## ADR-004 — Enforce access controls server-side
**Decision:** Authenticate users and authorize customer-level data and exports at the API/data layer.  
**Reason:** UI-only restrictions can be bypassed.  
**Trade-off:** Requires identity integration and role administration.

## ADR-005 — Release through staging with rollback
**Decision:** Promote approved artifacts through development, staging, and production, retaining the last known-good release.  
**Reason:** Reduces deployment risk and enables recovery.  
**Trade-off:** Requires release automation and environment configuration.
