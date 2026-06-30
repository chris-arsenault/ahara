# TrueNAS Deploy Guide

> **AUDIENCE**: AI agents deploying Docker Compose services to TrueNAS via Komodo.

## Overview

TrueNAS-hosted services are deployed as Docker Compose stacks managed by [Komodo](https://github.com/moghingold/komodo). The deploy flow:

1. Terraform creates AWS resources (Lambda, SSM params, Cognito client)
2. Project-owned Docker images are built and pushed to GHCR when the stack has them
3. Komodo pulls the compose file from GitHub, sets environment from SSM, and deploys

The shared reusable workflow handles steps 2-3 automatically when `truenas: true` is set in `platform.yml`. Config-only stacks set `truenas_images: false` to skip the image build while keeping the same Komodo deploy path.

---

## Project Layout

### Single-image project (e.g., nas-sonarqube)

```
<project>/
  compose.yaml           # Docker Compose for TrueNAS
  Dockerfile             # Single image (root level)
  secret-paths.yml       # SSM paths for compose environment variables
  backend/               # Rust Lambda (if any)
  infrastructure/
    terraform/
  platform.yml
  Makefile
  CLAUDE.md
```

### Vendor project (upstream images)

```
<project>/
  compose.yaml           # References upstream images directly
  .env.example           # Placeholder values for compose validation
  secret-paths.yml       # SSM paths for compose environment variables
  config/                # Mounted service config
  dashboards/            # Provisioned dashboards, if applicable
  platform.yml
  Makefile
  AGENTS.md
```

Use this layout for platform services such as observability stacks where the
repo owns configuration for third-party services and wrapping official images
would add no value.

### Multi-image project (e.g., airwave)

```
<project>/
  compose.yaml           # References both images
  backend/               # Rust source + Dockerfile
    Dockerfile
    Cargo.toml
    src/
  frontend/              # TypeScript source + Dockerfile
    Dockerfile
    package.json
    src/
  secret-paths.yml
  infrastructure/
    terraform/
  platform.yml
  Makefile
  CLAUDE.md
```

Each component directory has its own `Dockerfile`. The directory name is the component name used in the image path.

---

## Dockerfiles must not compile

The shared workflow compiles Rust and builds frontends before the Docker step. Dockerfiles must COPY pre-built artifacts from the CI workspace — **not** compile from source.

The shared workflow builds the backend and copies the release binary into `dist/` inside the component directory. The frontend `pnpm run build` also outputs to `dist/`. Dockerfiles COPY from `dist/` — a clean directory with only deployable artifacts, unaffected by `.dockerignore` patterns on `target/`.

**Rust backend Dockerfile:**

```dockerfile
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
COPY dist/<binary> /usr/local/bin/<binary>
CMD ["<binary>"]
```

**Frontend Dockerfile:**

```dockerfile
FROM nginx:alpine
COPY dist/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
```

**Do NOT use multi-stage builds that compile from source.** The shared workflow already compiled everything. The Dockerfile is a packaging step, not a build step.

Note: the Rust binary is compiled for linux-amd64 (GitHub runner architecture), which must match the target container's architecture.

---

## platform.yml

### Vendor upstream-image stack

```yaml
project: <name>
prefix: <name>
stack:
  - vendor
truenas: true
truenas_images: false
truenas_compose_path: compose.yaml
truenas_compose_check_paths:
  - compose.yaml
```

Deploys the Compose file through Komodo without building or pushing any GHCR
images. `secret-paths.yml` is still resolved into the Komodo stack environment.
Include `.env.example` with safe placeholder values so `docker compose config`
can validate the file in CI.

### Single image

```yaml
project: <name>
prefix: <name>
stack:
  - rust
  - terraform
truenas: true
```

Builds from root → `ghcr.io/chris-arsenault/<project>:<sha>`

### Multi-image

```yaml
project: <name>
prefix: <name>
stack:
  - rust
  - typescript
truenas: true
images:
  - api
  - web
```

Builds each component from its directory → `ghcr.io/chris-arsenault/<project>/<component>:<sha>`

The `truenas: true` flag tells the shared workflow to:
1. Build Docker image(s) when `truenas_images` is not false — single from root, or one per entry in `images`
2. Push built images to GHCR at `ghcr.io/chris-arsenault/<project>[/<component>]:<sha>`
3. Validate each Compose path in `truenas_compose_check_paths`, or `truenas_compose_path` when the check list is omitted
4. Read `secret-paths.yml` for Komodo environment variables
5. Call the `deploy-truenas` action with stack name = project name and Compose file = `truenas_compose_path` or `compose.yaml`

---

## secret-paths.yml

Maps compose environment variable names to SSM parameter paths. These are **paths, not values** — safe to commit:

```yaml
DB_USER: /ahara/truenas-db/<stack-name>/<database-id>/username
DB_PASSWORD: /ahara/truenas-db/<stack-name>/<database-id>/password
ADMIN_PASSWORD: /ahara/<name>/admin-password
```

The `deploy-truenas` action reads this file, resolves the SSM values via the Komodo proxy Lambda, and sets them in the Komodo stack environment. Compose reads them as `${DB_USER}`, `${DB_PASSWORD}`, etc.

---

## AWS Access from TrueNAS Services

Use IAM Roles Anywhere for TrueNAS workloads that need AWS API access, such as S3 sync or Lambda invocation. The platform owns the trust anchor, profile, private CA, and enrollment endpoint. Each app owns its per-use-case IAM role and runtime policy.

Private keys are generated by the service on first boot and stay on the service's persistent volume. The deploy workflow only injects a one-hour, single-use enrollment token and public Roles Anywhere discovery values.

### platform.yml

Declare each TrueNAS workload identity under `truenas_roles_anywhere`:

```yaml
project: <name>
prefix: <name>
truenas: true
truenas_roles_anywhere:
  backup:
    env_prefix: AWS_RA_BACKUP
```

The shared deploy workflow creates the enrollment token automatically and sets these Compose environment variables for the workload:

```text
AWS_RA_BACKUP_WORKLOAD_ID
AWS_RA_BACKUP_ENROLLMENT_TOKEN
AWS_RA_BACKUP_ENROLLMENT_URL
AWS_RA_BACKUP_TRUST_ANCHOR_ARN
AWS_RA_BACKUP_PROFILE_ARN
AWS_RA_BACKUP_ENTRY_ROLE_ARN
AWS_RA_BACKUP_ROLE_ARN
```

### Terraform

Create one workload role per use case in the app repo:

```hcl
module "truenas_backup_role" {
  source = "git::https://github.com/chris-arsenault/ahara-infra.git//infrastructure/terraform/modules/truenas-roles-anywhere-workload?ref=main"

  prefix = "<prefix>"
  name   = "backup"

  policy_json = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = "arn:aws:s3:::<bucket>"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "arn:aws:s3:::<bucket>/<prefix>/*"
      }
    ]
  })
}
```

The module creates `<prefix>-truenas-<name>`, restricts trust to the matching certificate SAN URI (`spiffe://ahara/truenas/<prefix>/<name>`), and registers the role ARN in SSM for the deploy workflow.

### Container boot

Install `aws_signing_helper`, `openssl`, `curl`, and `python3` in the image. Copy the shared bootstrap helper into the image or include the same logic in the service entrypoint:

```dockerfile
COPY bin/truenas-roles-anywhere-bootstrap /usr/local/bin/truenas-roles-anywhere-bootstrap
```

Run the helper before the service process and mount its identity directory on persistent storage:

```yaml
services:
  backup:
    image: ghcr.io/chris-arsenault/<project>:${IMAGE_TAG}
    restart: unless-stopped
    volumes:
      - /mnt/apps/apps/<project>/aws-identity:/var/lib/ahara/aws-identity
    command:
      - /usr/local/bin/truenas-roles-anywhere-bootstrap
      - AWS_RA_BACKUP
      - --
      - /usr/local/bin/<service>
```

After enrollment, the helper execs the service with `AWS_CONFIG_FILE` and `AWS_PROFILE` set. AWS SDKs and the AWS CLI then use `credential_process` to get temporary credentials through Roles Anywhere, then assume the app-owned workload role.

---

## compose.yaml

Standard Docker Compose with `${VAR}` references to environment variables set by Komodo.

### Single image

```yaml
services:
  app:
    image: ghcr.io/chris-arsenault/<project>:${IMAGE_TAG}
    restart: unless-stopped
    ports:
      - "<host-port>:8080"
    environment:
      DB_USER: "${DB_USER}"
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:8080/health"]
      interval: 15s
      timeout: 5s
      retries: 20
      start_period: 60s
```

### Multi-image

```yaml
services:
  api:
    image: ghcr.io/chris-arsenault/<project>/api:${IMAGE_TAG}
    restart: unless-stopped
    environment:
      DB_USER: "${DB_USER}"
    healthcheck:
      test: ["CMD-SHELL", "curl -sf http://localhost:8080/health"]
      interval: 15s
      timeout: 5s
      retries: 20
      start_period: 60s

  web:
    image: ghcr.io/chris-arsenault/<project>/web:${IMAGE_TAG}
    restart: unless-stopped
    depends_on:
      api:
        condition: service_healthy
```

`IMAGE_TAG` is set automatically by the deploy action to the git SHA. All images in the stack share the same tag.

---

## TrueNAS Database

TrueNAS services use a separate PostgreSQL instance on TrueNAS (192.168.66.3:5432), not the shared RDS. Database management is handled by the `ahara-db-migrate-truenas` Lambda in the `ahara-infra` services layer.

To register TrueNAS databases for a stack, add them to `var.truenas_db_stacks` in `ahara-infra/infrastructure/terraform/services/db-migrate-truenas.tf`:

```hcl
variable "truenas_db_stacks" {
  default = {
    <stack-name> = {
      databases = {
        <database-id> = {
          db_name = "<database-name>"
        }
      }
    }
  }
}
```

Each deploy for `<stack-name>` ensures every registered database ID owned by that stack. The Lambda creates the database, an application role named `<stack-name>_<database-id>_app`, and publishes credentials to SSM at `/ahara/truenas-db/<stack-name>/<database-id>/username` and `/ahara/truenas-db/<stack-name>/<database-id>/password`.

---

## Networking

TrueNAS services are reached via WireGuard VPN. The reverse proxy (nginx on EC2) routes traffic from the shared ALB to TrueNAS:

- **ALB** → **CloudFront** → **ALB** → **nginx reverse proxy** → **WireGuard** → **TrueNAS**
- Routes are defined in `ahara-infra/infrastructure/terraform/network/locals.tf` under `reverse_proxy_routes`
- Each route needs: `address` (TrueNAS IP), `port` (container host port), `auth` (cognito/passthrough)
- Optional: `max_body_size` for routes that handle large uploads

To add a new reverse proxy route, add an entry to `reverse_proxy_routes` in the `ahara-infra` network layer.

---

## Custom Post-Deploy Steps

If a service needs steps after the standard deploy (e.g., bootstrapping tokens, seeding data), add them as a separate job in the caller workflow:

```yaml
jobs:
  ci:
    uses: chris-arsenault/ahara/.github/workflows/ci.yml@main
    secrets: inherit

  bootstrap:
    if: github.ref == 'refs/heads/main'
    needs: [ci]
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v6
        with:
          role-to-assume: ${{ secrets.OIDC_ROLE }}
          role-session-name: GitHubActions-${{ github.run_id }}
          aws-region: us-east-1
      # ... custom steps ...
```

---

## WAF Considerations

The ALB has a WAF with `AWSManagedRulesCommonRuleSet`. The `SizeRestrictions_BODY` rule blocks request bodies over 8KB. If your service accepts large uploads through the reverse proxy:

1. Add `max_body_size` to the route in `reverse_proxy_routes` (nginx layer)
2. The WAF has an exemption for `sonar.ahara.io/api/ce/submit` — similar exemptions can be added in `ahara-infra/infrastructure/terraform/network/waf.tf`
