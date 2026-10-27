# Ahara Platform and Engineering Practice

Front door for Chris Arsenault's personal Ahara platform and reusable agentic
engineering practice. Contains documentation, CI tooling, shared workflows,
orchestration scripts, and practice guides.

## Audiences and boundaries

- Start with [README.md](README.md) to choose the platform or practice path.
- Ahara integration instructions apply to the owner's projects and infrastructure.
  Ahara is not a platform offered for other people or client organizations to use.
- [Agentic engineering practice](docs/agentic-engineering.md) is primarily for
  agents working across environments. Keep guides concise and self-contained:
  principles, reasons, and decision criteria. Use task-based navigation; do not
  require loading the whole collection. Keep anecdotes and research citations
  in the optional human field report. Include examples only when they clarify
  an action or distinction the agent needs.
- Keep the practice guides and optional field report tool-neutral. Extract
  organizing concepts and principles; do not reference the owner's personal
  tools, repositories, commands, or APIs. Keep environment-specific instructions
  in the separate platform documentation and skills. Distinguish recommended
  properties from behavior guaranteed by a particular implementation.
- Practice guidance does not install rules or grant access. The destination
  project's instructions, tools, and authorization govern work there.

## Contents

- `docs/agentic-engineering.md` — task-based entry point for agents
- `docs/working-with-coding-agents.md` — optional human field report
- `docs/coding-agents/` — focused agent guides, including sustained intent,
  domain-native work, meta-harness tooling, JIT documentation, and workflows
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
