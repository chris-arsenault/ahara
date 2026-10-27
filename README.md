# Ahara: Platform and Agentic Engineering

Two related bodies of work by Chris Arsenault live here: the operating guide
for my personal Ahara platform, and a reusable collection of agentic engineering
practices, patterns, and essays drawn from building with agents.

## Start Here

| What brings you here? | Start with |
| --- | --- |
| Working with agents in your own project or a client environment | [Agentic engineering practice](docs/agentic-engineering.md): the reading map, practical patterns, and how to adapt them |
| Understanding how I work with coding agents | [What has worked for me](docs/working-with-coding-agents.md): the field report and its supporting articles |
| Integrating or operating one of my Ahara projects | [Platform integration](INTEGRATION.md) and [platform architecture](docs/architecture.md) |
| Editing this repository | [Agent instructions](AGENTS.md) and [documentation index](docs/README.md) |

The practice material is intended for reuse, including my work across client
environments. It can be used with your own repositories, tools, and delivery
platform. Examples identify their source systems; adopting a practice does not
require access to those systems.

Ahara itself is my personal CI/CD and infrastructure platform. It is not offered
as a service or a platform for others to join or deploy onto. Its account,
identity, network, and deployment instructions apply to my projects. The
practice guides use those systems as examples where relevant.

## Ahara Platform

Ahara provides shared cloud infrastructure, household network appliances,
identity, observability, deployment tooling, and standards for my projects.

| Task | Guide |
| --- | --- |
| Integrate a project | [INTEGRATION.md](INTEGRATION.md) |
| Understand the platform | [Architecture and diagrams](docs/architecture.md) |
| Configure shared CI/CD | [CI-WORKFLOW.md](CI-WORKFLOW.md) |
| Deploy an owner-only TrueNAS workload | [TRUENAS-DEPLOY.md](TRUENAS-DEPLOY.md) |
| Send metrics, logs, and traces | [OBSERVABILITY.md](OBSERVABILITY.md) |
| Add scheduled data processing | [Data pipelines](docs/data-pipelines.md) |

### Platform Repositories

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

### Deploy Order

```
ahara-infra   (single Terraform apply; control, network, and services resolve through the module DAG)
       │
       └── consuming projects (websites, svap, tastebase, dosekit, etc.)
```

Deploy: `cd ../ahara-infra && ./scripts/deploy.sh`

### Tooling in This Repository

- [Documentation conventions](skills/repo-docs/SKILL.md) and planning skills in `skills/`; see the [practice index](docs/agentic-engineering.md#adapting-the-practice) for their environment dependencies
- [Repository line-count snapshot](docs/repository-line-counts.md)
- `.github/workflows/ci.yml` — shared reusable CI/CD workflow (called by all standard projects)
- `.github/actions/` — `collect-engineering-report`, `report-build`, `governance-check`, `run-migrations`, `deploy-truenas`
