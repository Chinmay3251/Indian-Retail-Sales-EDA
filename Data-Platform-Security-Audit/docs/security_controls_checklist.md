# Data Platform Security Controls Checklist

Mark Pass only when supported by evidence. Use Not Assessed when access or evidence is unavailable.

## Identity and access
- [ ] MFA enabled for privileged and remote access
- [ ] Role-based access control applied
- [ ] Least-privilege database and service accounts
- [ ] Joiner/mover/leaver access process defined
- [ ] Periodic access reviews completed
- [ ] Privileged actions logged and reviewed

## Secrets and configuration
- [ ] Secrets stored in approved secret manager
- [ ] No credentials committed to source control
- [ ] Secret rotation and revocation process tested
- [ ] Separate configuration for dev/staging/production
- [ ] Debug mode disabled in production

## Data protection
- [ ] Sensitive data classified and inventoried
- [ ] Encryption in transit enforced
- [ ] Encryption at rest enabled where required
- [ ] Backups protected and restore tested
- [ ] Retention and deletion policies defined
- [ ] Data exports restricted and audited
- [ ] Non-production data masked or synthetic

## Application and dependencies
- [ ] Dependencies scanned and patched
- [ ] Input validation and parameterized SQL used
- [ ] Authentication and authorization enforced server-side
- [ ] CORS and API exposure restricted
- [ ] Error messages do not leak secrets or internal details
- [ ] Security tests included in CI

## Infrastructure and operations
- [ ] Network ingress restricted to required sources
- [ ] Databases not publicly exposed unless explicitly justified
- [ ] TLS certificates valid and verification enabled
- [ ] Logs centralized with access controls
- [ ] Alerts cover suspicious access and service failures
- [ ] Incident response and escalation runbook exists
- [ ] Vulnerability remediation SLAs defined
