# Scheduled data pipelines

Accepted design, updated 2026-10-17. Implementation is a child of the
[Atlas plan](../../atlas/docs/ATLAS-PLAN.md#ahara-pipeline-framework-sub-plan),
Sulion `1ab94d8f-1834-4c2b-879c-34df49c7fef6`. Shared services and the client
module are implemented locally; deployment remains a separate action.

Use EventBridge Scheduler to start native Step Functions Standard workflows
whose work runs in Lambda. Keep centralized DynamoDB registration and job
status. Reuse Ahara's existing OTEL/Grafana observability. CI tests and deploys
code and infrastructure; production data refresh runs independently.

## Platform and client ownership

Reusable infrastructure code and centrally owned resources are distinct.
The shared pipeline module lives in `ahara-tf-patterns`, but clients instantiate
it in their own Terraform state and own the resulting workflow and schedule.

| Owner | Responsibility |
| --- | --- |
| `ahara-infra/control` | Project admission, deployer permissions, pipeline permission bundle, and project-scoped access to shared registration. |
| `ahara-infra/services` | Shared DynamoDB registration/job tables, execution-status recorder, and discovery parameters. |
| `ahara-tf-patterns/modules/pipeline` | Reusable client module for native workflow, schedule, IAM roles, delivery DLQ, and registration item. |
| Client repository, initially `atlas` | Module invocation, workflow definition, workers, schedule settings, inputs, transformations, output storage, validation, and publication. |
| `ahara-observability` | Cross-project pipeline/job dashboards and failure alerts. |
| Client repository | Domain dashboards, such as language coverage and rejected Atlas records. |
| `ahara` | Integration documentation and ordinary code-deployment tooling. |

This follows the existing registration split: a control-layer `managed-project`
entry admits a repository and grants deployment scope; client Terraform then
creates its resources through shared modules and registers with platform services.
The reviewed examples are [Ahara Business's admission](../../ahara-infra/infrastructure/terraform/control/project-ahara-business.tf),
[its client provisioning/registration](../../ahara-business/infrastructure/terraform/cognito.tf),
and [the shared auth service](../../ahara-infra/infrastructure/terraform/services/auth-trigger.tf).
The Cognito module itself creates the client; its consumer publishes the
registration. Pipeline registration uses DynamoDB rather than copying that
SSM mechanism.

## Shared registration and job status

The platform owns two on-demand DynamoDB tables and their schemas:

- Registrations contain project, pipeline name, description, workflow ARN,
  schedule, and owner. The client pipeline module writes its registration item
  through client Terraform. The platform publishes table identifiers through
  SSM/platform context for discovery. SSM is not a second registration store.
- Jobs contain execution ARN, pipeline identity, status, start/end times, and
  bounded failure information. A shared status recorder consumes execution-status
  events and writes these summaries. Clients do not write arbitrary job statuses.

Keep deployed definitions and runtime job records separate so applying client
Terraform cannot overwrite status. Restrict client registration writes to the
client's own project scope. The recorder accepts only registered workflows,
handles repeated events idempotently, and prevents older events from replacing
terminal status. Step Functions retains the detailed task history; the job table
does not duplicate every task transition.

Status events are a mirror of AWS execution state, not another execution engine.
If delivery is missed, operators inspect the execution with DescribeExecution
and repair that record through the ordinary support path. A continuously polling
reconciliation service is outside the initial implementation.

## Reusable client module

The module accepts the client's project/name, native Amazon States Language
definition, worker ARNs, schedule/timezone/enabled setting, registration metadata,
and shared platform context. It creates:

1. The client's Step Functions Standard workflow and scoped execution role.
2. Its EventBridge Scheduler schedule and invocation role.
3. A standard Scheduler delivery DLQ.
4. Its registration item in the shared DynamoDB table.

Workers, code packaging, source credentials, and artifact buckets are supplied
by the client using existing infrastructure patterns. Extend a shared Lambda
module only for a concrete packaging requirement encountered during adoption.
Do not require a generic worker SDK, stage envelope, lifecycle Lambda, or a new
manifest language. Native Retry/Catch/Map/Parallel states express client behavior.

Start, stop, inspect, and retry through AWS CLI/console. Manage schedule settings
in client Terraform. Overlapping executions are allowed initially; workers should
tolerate retries and use separate output paths where appropriate. There is no
distributed lease, deduplication ledger, or cross-trigger exactly-once guarantee.

Standard workflows can last up to a year; an ordinary Lambda invocation still
has its own 900-second limit. These are different limits. Implement the stages
and adjust from normal execution results; there is no preliminary feasibility
study, benchmark suite, or 12-minute acceptance gate.

## Observability

The shared recorder and client workers use existing Ahara telemetry paths into
Loki, Tempo, and VictoriaMetrics. Include project, pipeline, and execution identity
in logs/traces. Keep execution IDs out of metric labels. Use a shared Grafana
view for pipeline/job health and existing alert routing for failures and delivery
problems. Registry entries exist before the first run, so inventory must not
equate "no jobs yet" with an unregistered pipeline.

Detailed input/output counters belong to the client. Atlas's source coverage,
record rejection, data ages, and publication result are Atlas concerns, not new
platform job states. Existing telemetry adapters remain the instrumentation
boundary; no parallel telemetry framework or CloudWatch product dashboard is added.

## Atlas adoption

Atlas instantiates the pipeline module and owns its native workflow:

1. Fetch pinned Glottolog/Atlas sources and Atlas's curated historical inputs.
2. Reconcile identifiers and normalize observations with their dates and sources.
3. Produce catalogue/search/temporal indexes and geographic tiles.
4. Validate complete source accounting, references, geometry, dates, and tile reads.
5. Write a complete immutable S3 release and update the static manifest only after
   validation succeeds. Failure before that update leaves the previous manifest.

Source versions, checksums, citations, and linguistic uncertainty remain Atlas
requirements. Its bucket, retention, cadence, manifest schema, and publication
policy live in Atlas. The platform neither interprets Glottocodes/PMTiles nor
coordinates dataset promotion. There is no publication outbox, channel-generation
database, approval service, or automatic rollback coordinator.

The static frontend reads the manifest and immutable files through CloudFront;
its build/deployment does not invoke the data pipeline. Any reusable website
data-origin/cache support needed for this is implemented during Atlas adoption
in `ahara-tf-patterns`, while Atlas owns its instance and output objects. Frontend
Terraform must not upload or prune pipeline-produced data. Domain fixtures test
adapters and browser contracts in CI; a separate full-source run establishes
global dataset coverage. The public application still has no backend request path.

## Scope and execution

Implement shared tables/status recording and permissions first, then the client
module, shared observability/docs, and Atlas adoption. The matching four phases
are recorded in the Atlas sub-plan. Test actual behavior and applicable repository
checks; inspect ordinary run logs and change the implementation as needed.

The removed initial scopes are custom lifecycle/lease machinery, transactional
publication, continuous reconciliation, custom operator CLI, worker SDK, and
measurement-first planning. Prior unstarted phases are superseded in Sulion;
their history is not evidence that those features were implemented.

Before adding AWS resources, apply `ahara-infra/AGENTS.md` cost-review requirements
using current service pricing and a reasonable usage estimate. Use ordinary
on-demand services and existing network/observability resources. Cost review
does not require a separate performance-measurement phase. External publication,
infrastructure applies, and pushes retain the user's existing authorization
boundaries; updating this design performs none of them.

## Integration and operations

Admit the client with the `pipeline` managed-project bundle and the `lambda`
bundle for its workers. Instantiate `platform-context` with
`pipelines_enabled = true`, then pass `module.ctx.pipelines` to the `pipeline`
module. Existing consumers leave discovery disabled until they adopt pipelines.
The module defaults its schedule to disabled; the client controls activation.

The discovery parameters are `/ahara/pipelines/registry-table` and
`/ahara/pipelines/jobs-table`. The registry partition key is `workflow_arn`;
the job partition key is `execution_arn`. Registry rows are inventory even when
no job exists. Clients manage only their own registry keys through Terraform.
Operators use the existing AWS role and ordinary tools:

```bash
aws dynamodb scan --table-name ahara-pipeline-registry
aws dynamodb get-item --table-name ahara-pipeline-jobs --key '{"execution_arn":{"S":"EXECUTION_ARN"}}'
aws stepfunctions start-execution --state-machine-arn WORKFLOW_ARN --input '{}'
aws stepfunctions describe-execution --execution-arn EXECUTION_ARN
aws stepfunctions get-execution-history --execution-arn EXECUTION_ARN
aws stepfunctions stop-execution --execution-arn EXECUTION_ARN
aws stepfunctions redrive-execution --execution-arn EXECUTION_ARN
```

In the managed development environment, ordinary `aws` is already broker-wrapped;
use `with-cred --` for other secret-backed commands. Other installations use
their configured AWS role credentials. Task inputs/history can contain private
data: the shared recorder stores summaries and bounded AWS error identifiers,
never input/output/cause payloads. A new redrive may reopen a terminal execution;
older events within the same attempt cannot do so.

The recorder supplies Alloy's `loki.attribute.labels` hint for bounded
`event_name`, `project`, `pipeline`, and `status` labels. The Ahara Scheduled
Pipelines dashboard queries these logs; `execution_arn` stays in the log payload
for correlation. Failure rules use
the existing Grafana notification policy. No execution ARN becomes a metric
label. Scheduler delivery failures have a native SQS backlog alarm routed to
the existing Ahara SNS alarm topic; CloudWatch is this AWS runtime fallback,
not a second product dashboard. Inspect the delivery queue before deleting any
messages. Status delivery is best effort; inspect native task history when a
summary is missing. Shared tables intentionally have no automatic retention
policy in this first version.

Apply shared services/admission first, publish the shared module version, then
deploy the client's workers and workflow. Confirm the schedule and output
publication policy in the client repository. Test/deploy jobs in CI must never
start a production refresh as a side effect.
