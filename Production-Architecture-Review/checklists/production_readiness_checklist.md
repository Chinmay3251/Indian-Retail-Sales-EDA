# Production Readiness Checklist

Tick only when evidence is available.

## Data
- [ ] Input schemas and data owners documented
- [ ] Raw snapshots retained with load metadata
- [ ] Date inconsistencies resolved or quarantined
- [ ] Null, duplicate, key, range, and freshness checks automated
- [ ] Failed batches alert an owner and can be safely rerun

## ML and analytics
- [ ] Feature definitions versioned
- [ ] Time-based validation and baseline comparison completed
- [ ] Metrics documented with target horizon and sample count
- [ ] Segment definitions and limitations approved
- [ ] Preprocessing and model artifacts versioned together
- [ ] Drift and segment-migration monitoring defined
- [ ] Human review and action policy documented

## Security and privacy
- [ ] Secrets are not stored in Git
- [ ] Authentication and server-side authorization enabled
- [ ] Least-privilege service/database accounts configured
- [ ] Encryption configured as applicable
- [ ] Customer exports restricted and audited
- [ ] Retention/deletion policy approved
- [ ] Development/test data synthetic or masked

## Reliability and operations
- [ ] Health checks and structured logs available
- [ ] Pipeline/service alerts tested
- [ ] Backup and restore tested
- [ ] Rollback to previous approved release tested
- [ ] Runbook and support owner documented
- [ ] Staging sign-off completed

## Performance and release
- [ ] Expected volumes and refresh cadence agreed
- [ ] Load tests completed against agreed targets
- [ ] Latency targets defined and measured
- [ ] Release approval recorded
- [ ] Business owner approves use of predictions and segments
