# Observability & Telemetry Ingest

How Ahara collects metrics, logs, and traces, and how producers authenticate to
the TrueNAS-local observability backends. Owned by
[`ahara-observability`](https://github.com/chris-arsenault/ahara-observability)
(the TrueNAS stack) and [`ahara-infra`](https://github.com/chris-arsenault/ahara-infra)
(the AWS edge collector, Cognito M2M identity, and network).

- **System** — the stack, the two Alloy collectors, dashboards, metric naming.
- **Ingest auth** — the reusable Cognito M2M + Envoy JWT gateway pattern.
- **Producer integration** — how to send authenticated telemetry.
- **Operational patterns** — deploy ordering and the gotchas that bit us.

---

## System

The stack runs on TrueNAS via Komodo (see [TRUENAS-DEPLOY.md](TRUENAS-DEPLOY.md)),
all upstream images, config-only.

| Service | Role | Port (TrueNAS `192.168.66.3`) |
|---|---|---|
| Grafana | Dashboards, Explore, alerting (Cognito OIDC) | `30038` |
| Alloy (local router) | Receives OTLP, routes logs→Loki, metrics→VM, traces→Tempo | internal `12345`; OTLP via gateway |
| vmagent | Scrapes the local stack + host, remote-writes to VM | internal |
| VictoriaMetrics (VM) | Prometheus-compatible metrics backend | via gateway `8428` |
| Loki | Log backend (`auth_enabled: false` — see auth below) | via gateway `3100` |
| Tempo | Trace backend; runs the span-metrics + service-graph generator | internal only |
| InfluxDB | Compatibility store for sensor history (token auth) | `18086` |
| ingest-gateway (Envoy) | JWT-validating front door for VM/Loki/OTLP | publishes `8428/3100/4317/4318` |

### Two Alloy collectors

Telemetry flows through **two** Grafana Alloy instances — don't confuse them:

1. **Edge gateway** — on the AWS reverse-proxy EC2 host (`ahara-infra`,
   `network/templates/alloy_config.alloy.tpl`). Lambdas send OTLP to the
   AWS-private endpoint (`/ahara/observability/otlp-http-endpoint`); the edge
   batches and forwards across the WireGuard VPN to TrueNAS. It exports metrics
   (remote_write→VM), logs (loki.write→Loki), and traces (OTLP→local Alloy).
   It self-scrapes with `instance="reverse-proxy-gateway"`.
2. **Local router** — in the `ahara-observability` compose (`config/alloy/local.alloy`),
   `instance="alloy:12345"`. Receives OTLP (from the edge and TrueNAS-LAN
   producers) and routes to the backends over the internal Docker network.

NAT and WireGuard hosts run Alloy only to ship their own host logs, and they push
to the **reverse proxy's** Loki gateway (not TrueNAS directly). Only the reverse
proxy writes to TrueNAS.

```
Lambdas ─OTLP─▶ edge Alloy ─(VPN)─┬─ remote_write ─▶ [gateway] ─▶ VictoriaMetrics
                                  ├─ loki.write ────▶ [gateway] ─▶ Loki
NAT/WG host logs ─▶ edge loki gw ─┘
                                  └─ OTLP traces ───▶ [gateway] ─▶ local Alloy ─▶ Tempo
LAN producers (house-sensors) ─OTLP─────────────────▶ [gateway] ─▶ local Alloy ─▶ VM/Loki/Tempo
```

### Dashboards

Platform dashboards ship from `ahara-observability/dashboards/*.json` (Grafana
file provider, `Ahara` folder). Product repos own their own dashboards via
`observability.dashboards` in `platform.yml` — deployed by the shared dashboard
Lambda without redeploying Grafana (see [CI-WORKFLOW.md](CI-WORKFLOW.md)).

### Metric naming (OTLP → Prometheus)

- App metrics: `ahara_*` with labels `service_name`, `operation_type`
  (`user_interaction`/`polling`/`background`/`health`), `operation_name`,
  `operation_outcome`. HTTP adds `http_request_method`, `http_response_status_code`,
  `url_path`.
- **Duration histograms carry a `_milliseconds_` infix**:
  `ahara_http_server_request_duration_ms_milliseconds_bucket` (a frequent
  dashboard footgun). Span-metrics latency (`traces_spanmetrics_latency_bucket`)
  is in **seconds**.
- `service_namespace` is **not** emitted — filter on `service_name`.
- Span RED from Tempo's generator: `traces_spanmetrics_calls_total` /
  `_latency_*` with `service`, `span_name`, `span_kind`, `status_code`.

---

## Ingest authentication (the reusable pattern)

**Goal:** identity comes from Cognito, not a shared secret. The backends
(VM/Loki/OTLP) are unauthenticated services, so they are **not published**;
instead an Envoy gateway validates a Cognito **machine-to-machine
(client-credentials) JWT** on every external request.

### Cognito M2M identity — `ahara-infra/services/observability-ingest.tf`

- `aws_cognito_resource_server "observability"` on the shared pool, scope
  `ingest` → scope string **`observability/ingest`**.
- `aws_cognito_user_pool_client "observability_ingest"` — confidential
  (`generate_secret = true`), `allowed_oauth_flows = ["client_credentials"]`,
  `allowed_oauth_scopes = ["observability/ingest"]`. This is distinct from the
  human `code`-flow clients in `identity.tf`.
- Published to SSM (public + secret):

  | SSM parameter | Type | Consumer |
  |---|---|---|
  | `/ahara/observability/ingest-client-id` | String | producers |
  | `/ahara/observability/ingest-client-secret` | SecureString | producers |
  | `/ahara/observability/ingest-scope` | String | producers / gateway |
  | `/ahara/observability/ingest-token-url` | String | producers |
  | `/ahara/observability/ingest-issuer` | String | gateway |
  | `/ahara/observability/ingest-jwks-uri` | String | gateway |

  Token endpoint: `https://auth.services.ahara.io/oauth2/token`.

> The deployer role needs `cognito-idp:CreateResourceServer` (+ Describe/Update/
> Delete). It lives in `control/modules/policy-library/cognito-pool`. The
> workload boundary only denies `CreateUserPool*`/`Admin*`, so it does not block
> resource servers.

### Envoy gateway — `ahara-observability/config/envoy/envoy.yaml`

The `ingest-gateway` service is the **only** thing that publishes `8428/3100/4317/4318`.
Per listener it runs `jwt_authn` (Cognito `remote_jwks` + issuer) and an `rbac`
filter requiring the `scope` claim to contain `observability/ingest`, then proxies
to the internal backend.

**Key property — internal traffic bypasses the gateway.** Grafana datasources,
vmagent remote-write, and Tempo's generator reach `victoriametrics:8428` /
`loki:3100` / `tempo:3200` directly over the Docker network. Only external
producers hit the published (authenticated) ports. So enabling auth requires
**zero changes to internal clients**.

The gateway needs only Cognito's **public** issuer/JWKS/scope, injected via
`secret-paths.yml` (no ingest secret is stored on TrueNAS):

```yaml
# ahara-observability/secret-paths.yml
COGNITO_ISSUER:   /ahara/observability/ingest-issuer
COGNITO_JWKS_URI: /ahara/observability/ingest-jwks-uri
INGEST_SCOPE:     /ahara/observability/ingest-scope
```

Envoy has no native env substitution, so the compose `entrypoint` `sed`-renders
those into the config at start. Missing/placeholder values ⇒ Envoy crash-loops.

---

## Producer integration

Any workload that ships telemetry to TrueNAS must present a Cognito M2M bearer
token with scope `observability/ingest`. Two supported paths:

### Grafana Alloy (native OAuth2)

Alloy's HTTP clients fetch and auto-refresh the token themselves. The edge
collector uses all three:

```river
prometheus.remote_write "victoriametrics" {
  endpoint {
    url = "http://192.168.66.3:8428/api/v1/write"
    oauth2 {
      client_id     = sys.env("OBS_INGEST_CLIENT_ID")
      client_secret = sys.env("OBS_INGEST_CLIENT_SECRET")
      token_url     = "https://auth.services.ahara.io/oauth2/token"
      scopes        = ["observability/ingest"]
    }
  }
}
loki.write "default" { endpoint { /* url + same oauth2 block */ } }

otelcol.auth.oauth2 "ingest" { /* same four fields */ }
otelcol.exporter.otlp "tempo" {
  client { endpoint = "192.168.66.3:4317", auth = otelcol.auth.oauth2.ingest.handler }
}
```

Credentials are fetched from SSM **at boot** into the Alloy env file (see
`network/templates/common_user_data.sh.tpl`), so the secret never lands in the
launch-template user-data. The EC2 role needs `ssm:GetParameter` +
`kms:Decrypt` on `/ahara/observability/ingest-*`
(`network/observability-ingest-iam.tf`).

### OpenTelemetry SDK (token-refreshing session)

For app SDKs (e.g. the Python collectors in `house-sensors`), inject a
credential that refreshes before expiry. Pattern
(`house-sensors/collectors/*/app_telemetry.py`):

```python
class _CognitoClientCredentialsAuth:  # requests.auth callable
    def __call__(self, request):
        if self._token is None or time.monotonic() >= self._expires_at:
            self._refresh()  # POST token_url, Basic(id,secret), grant=client_credentials
        request.headers["Authorization"] = f"Bearer {self._token}"
        return request

session = requests.Session(); session.auth = _CognitoClientCredentialsAuth(...)
OTLPMetricExporter(session=session)   # exporter uses the authed session
```

`OBS_INGEST_CLIENT_ID/SECRET` come from SSM via the compose service's
`secret-paths.yml`; `token_url`/`scope` are non-secret constants. When no
credentials are set (local/dev) the code sends unauthenticated, so nothing breaks
outside the deployed environment.

> A **static bearer header does not work** — client-credentials tokens expire
> (~1h). Always refresh.

---

## Operational patterns & gotchas

Hard-won, in the order they bite.

### Deploy ordering (producers first, enforcement second)

An open (unauthenticated) backend **ignores** a bearer token, so tokens are a
no-op until enforcement flips on. Therefore:

1. Deploy the Cognito M2M identity + all producers (edge, LAN, SDK apps) first —
   they start attaching tokens harmlessly.
2. Deploy the Envoy gateway (unpublishing raw backends) last.

Reverse it and you take an ingestion outage. Rollback = revert the gateway
(enforcement) commit; the raw backends re-publish and ingestion resumes.

### EC2 user-data 16 KiB limit

Adding the Alloy OAuth2 blocks pushed the reverse-proxy launch template over
EC2's hard 16384-byte user-data limit. Fix: `base64gzip(var.user_data)` in the
launch template — cloud-init on AL2023 auto-decompresses gzipped user-data
(`network/modules/ec2_instance/launch_template.tf`).

### Network hosts and `instance_refresh`

- `enable_instance_refresh` (module default `true`) rolls an ASG when its launch
  template changes. It was once set `false` on nat/proxy/wireguard to stop
  telemetry changes cycling critical network boxes — but that also means config
  changes never reach them. Keep it `true`; the Alloy install is wrapped in
  `run_optional` so a bad telemetry bootstrap is non-fatal.
- **Only the reverse proxy writes to TrueNAS.** NAT/WireGuard push to the
  proxy's Loki gateway, and the proxy reaches TrueNAS *through* the WireGuard
  tunnel — so never force-roll WireGuard/NAT to pick up ingest config; roll only
  the reverse proxy (change something inside the `otlp_gateway_enabled` template
  block, which is empty on the other hosts).
- **Baseline-on-add:** re-enabling `instance_refresh` does *not* retroactively
  roll an already-drifted instance; only a *subsequent* launch-template change
  triggers a refresh.

### Envoy → backend DNS: pin IPv4

The Docker network is dual-stack. Envoy's default `dns_lookup_family: AUTO`
resolved backends to their **IPv6** address. VictoriaMetrics
(`-httpListenAddr=:8428`) binds **IPv4 only**, so its IPv6 endpoint returns
`503 connection refused` while Loki/Alloy (dual-stack) worked. Pin
`dns_lookup_family: V4_ONLY` on the backend clusters. (Grafana masks this —
its Go client falls back to IPv4.)

Also: recreating the gateway and a backend in the **same** deploy can leave
Envoy with a stale backend IP. Prefer changing the gateway alone, or bounce it
after.

### Verification recipe

```bash
# mint a token
CID=$(aws ssm get-parameter --region us-east-1 --name /ahara/observability/ingest-client-id --query Parameter.Value --output text)
CS=$(aws ssm get-parameter --region us-east-1 --with-decryption --name /ahara/observability/ingest-client-secret --query Parameter.Value --output text)
TOK=$(curl -s -u "$CID:$CS" -d grant_type=client_credentials -d scope=observability/ingest \
      https://auth.services.ahara.io/oauth2/token | jq -r .access_token)

curl -s -o /dev/null -w '%{http_code}\n' 'http://192.168.66.3:8428/api/v1/query?query=up'                 # anonymous -> 401
curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOK" \
     'http://192.168.66.3:8428/api/v1/query?query=up'                                                     # authed    -> 200
```

To read a backend while debugging without a token, go through Grafana's internal
datasource proxy (bypasses the gateway), authenticating with the break-glass
admin password at `/ahara/observability/grafana-admin-password`:

```bash
GPW=$(aws ssm get-parameter --region us-east-1 --with-decryption --name /ahara/observability/grafana-admin-password --query Parameter.Value --output text)
curl -s -u "admin:$GPW" 'http://192.168.66.3:30038/api/datasources/proxy/uid/victoriametrics/api/v1/query?query=up'
```
