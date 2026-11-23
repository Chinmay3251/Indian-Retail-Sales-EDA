# Security Audit Methodology

## 1. Objective
Assess the security posture of a data platform across application code, data storage, identity, infrastructure, operations, and governance. The provided scripts support repository-level triage; platform controls require authorized manual inspection.

## 2. Scope
- Application and repository security hygiene
- Secrets and configuration management
- Dependency vulnerability management
- Authentication, authorization, and least privilege
- Database security and data protection
- Network exposure and encryption
- Logging, monitoring, backups, and incident response

## 3. Process
1. Confirm written authorization, platform owner, environment, and audit boundaries.
2. Inventory repositories, services, databases, data stores, identities, and integrations.
3. Run the static repository scanner against the authorized project directory.
4. Review dependency vulnerabilities using `pip-audit` or the organization's approved scanner.
5. Manually inspect IAM roles, database grants, network ingress/egress, TLS, encryption, secrets storage, backups, logs, and retention.
6. Validate each finding, collect minimal evidence, assign severity and an owner.
7. Recommend remediation and retest after fixes.
8. Produce a signed-off report with residual risks and accepted exceptions.

## 4. Severity guidance
- **Critical:** confirmed exploitable exposure with major data/system impact; immediate containment.
- **High:** likely compromise path or sensitive-data exposure; prioritize urgent remediation.
- **Medium:** meaningful weakness requiring planned remediation.
- **Low:** hygiene/documentation issue with limited direct impact.
- **Informational:** improvement suggestion or observation.

Severity must be determined from validated impact and likelihood, not scanner output alone.

## 5. Evidence handling
Do not paste credentials, tokens, customer records, or private keys into the report. Record file/setting references and redact sensitive values. Store evidence in approved restricted locations.

## 6. Limitations
The static scanner is pattern-based. It does not validate exploitability, inspect a live cloud account or database, enumerate IAM permissions, test network exposure, verify encryption, or perform penetration testing. Dependency audit requires network/package-index access and a supported environment.
