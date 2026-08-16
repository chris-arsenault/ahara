# Platform

Index repo for the platform layer. Contains documentation, CI tooling, shared workflows, and orchestration scripts.

## Contents

- `INTEGRATION.md` — canonical integration guide for AI agents
- `skills/repo-docs/` — repository documentation conventions skill, mirrored to `~/.claude/skills/repo-docs/` for active use
- `CI-WORKFLOW.md` — shared reusable CI/CD workflow, platform.yml, governance, Qlty, and engineering reporting
- `TRUENAS-DEPLOY.md` — TrueNAS deploy pattern (Docker, Komodo, networking)
- `.github/workflows/ci.yml` — shared reusable workflow (called by all standard projects)
- `.github/actions/` — collect-engineering-report, report-build, governance-check, run-migrations, deploy-truenas

## Do not add infrastructure here

Terraform and application code belong in `ahara-infra`, under the appropriate layer:
- `infrastructure/terraform/control/` — IAM roles, OIDC, deployer roles, policy library
- `infrastructure/terraform/network/` — VPC, ALB, WireGuard VPN, NAT, DNS, WAF
- `infrastructure/terraform/services/` — Cognito, RDS, database migrations, CI ingest, auth-trigger, CORS, komodo-proxy, OG server, observability

All three layers share a single Terraform state (`ahara/infra.tfstate`) and deploy via one `terraform apply`.

## Related repos (sibling directories)

- `ahara-infra` — single consolidated infrastructure repo; Rust Lambda workspace in `backend/`, platform migrations in `db/migrations/`, one OIDC deployer role for the whole stack
- `ahara-standards` — shared standards, ADRs, patterns, and lint rules
- `ahara-observability` — Grafana runtime, platform dashboards, and engineering-quality reporting
- `ahara-business` — business systems plus operator user and app-authorization administration
- `ahara-portal` — public Ahara website and project portfolio
- `ahara-vpn` — household gateway, firewall, DNS, and WireGuard appliance
- `ahara-trust` — LAN machine identity and shared internal-certificate appliance
- `ahara-collector` — IoT-LAN device discovery, polling, and constrained transport
- `nas-falkordb` — FalkorDB on TrueNAS, upstream-image Komodo stack
- `nas-text-embeddings-inference` — Text Embeddings Inference on TrueNAS, upstream-image Komodo stack
