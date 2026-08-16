# Platform

Index repo for the Ahara platform: shared cloud infrastructure, household
network appliances, identity, observability, deployment tooling, and standards.

## Repos

| Repo | Purpose | Path |
|------|---------|------|
| [ahara-infra](https://github.com/chris-arsenault/ahara-infra) | Consolidated AWS control, network, and service infrastructure; Rust platform Lambdas; platform migrations | `../ahara-infra` |
| [ahara-tf-patterns](https://github.com/chris-arsenault/ahara-tf-patterns) | Reusable Terraform modules for applications on the shared AWS infrastructure | `../ahara-tf-patterns` |
| [ahara-standards](https://github.com/chris-arsenault/ahara-standards) | Shared engineering standards, ADRs, implementation patterns, and lint rules | `../ahara-standards` |
| [ahara-observability](https://github.com/chris-arsenault/ahara-observability) | TrueNAS-hosted Grafana, Alloy, VictoriaMetrics, Loki, Tempo, and compatibility InfluxDB | `../ahara-observability` |
| [ahara-access](https://github.com/chris-arsenault/ahara-access) | Shared access grants and private asset delivery | `../ahara-access` |
| [ahara-business](https://github.com/chris-arsenault/ahara-business) | Business systems plus operator administration for users and app authorizations | `../ahara-business` |
| [ahara-portal](https://github.com/chris-arsenault/ahara-portal) | Public Ahara website and project portfolio | `../ahara-portal` |
| [ahara-vpn](https://github.com/chris-arsenault/ahara-vpn) | Declarative gateway, firewall, DNS, and WireGuard appliance | `../ahara-vpn` |
| [ahara-trust](https://github.com/chris-arsenault/ahara-trust) | LAN machine-identity authority and shared internal-certificate issuer | `../ahara-trust` |
| [ahara-collector](https://github.com/chris-arsenault/ahara-collector) | IoT-LAN device discovery, polling, inventory, and constrained transport | `../ahara-collector` |
| [nas-falkordb](https://github.com/chris-arsenault/nas-falkordb) | FalkorDB on TrueNAS, deployed through Komodo | `../nas-falkordb` |
| [nas-text-embeddings-inference](https://github.com/chris-arsenault/nas-text-embeddings-inference) | Text Embeddings Inference on TrueNAS, deployed through Komodo | `../nas-text-embeddings-inference` |

## Deploy Order

```
ahara-infra   (single Terraform apply; control, network, and services resolve through the module DAG)
       │
       └── consuming projects (websites, svap, tastebase, dosekit, etc.)
```

Deploy: `cd ../ahara-infra && ./scripts/deploy.sh`

## This Repo Also Contains

- `INTEGRATION.md` — canonical instructions for AI agents integrating projects with the platform
- `CI-WORKFLOW.md` — shared reusable CI/CD workflow, platform.yml, governance, Qlty, and engineering reporting
- `TRUENAS-DEPLOY.md` — TrueNAS deploy pattern (Docker, Komodo, secret-paths.yml)
- `OBSERVABILITY.md` — telemetry stack, the Cognito M2M + Envoy JWT ingest-auth pattern, and how producers send authenticated metrics/logs/traces
- `.github/workflows/ci.yml` — shared reusable CI/CD workflow (called by all standard projects)
- `.github/actions/` — `collect-engineering-report`, `report-build`, `governance-check`, `run-migrations`, `deploy-truenas`

## Integration

See [INTEGRATION.md](INTEGRATION.md) for full instructions.
