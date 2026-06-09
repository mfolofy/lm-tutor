"""Tests for the devops class — proves each rule's FAIL/PASS behaviour.

For each rule with a check_regex, a FAIL snippet MUST produce that rule's
violation and a PASS snippet MUST NOT. Teaching-only rules (no checker) are
tested for syllabus content presence only.

Run with: pytest tests/
"""

import pytest

from tutor.eval import grade
from tutor.eval.harness import load_syllabus


def _rules_for(submission: str) -> set[str]:
    result = grade(submission, "devops")
    return {v.rule for v in result.violations}


# ── CI PIPELINE GATES ──────────────────────────────────────────────────────────

CI_CASES = [
    # --no-verify bypass
    ("ci-pipeline-gates",
     "git commit --no-verify -m urgent",
     "git commit -m 'fix: resolve timeout'"),
    # skip-ci label
    ("ci-pipeline-gates",
     "[skip ci]",
     "CI: all checks passed"),
    # skip-checks
    ("ci-pipeline-gates",
     "git push origin main --skip-checks",
     "git push origin main"),
    # bypass CI gate
    ("ci-pipeline-gates",
     "bypass CI tests",
     "CI pipeline: lint, test, build, security"),
    # bypass build
    ("ci-pipeline-gates",
     "bypass build gate",
     "Build stage: docker build ."),
    # skip tests
    ("ci-pipeline-gates",
     "skip-tests",
     "Test stage: pytest tests/ -v"),
    # skip pipeline
    ("ci-pipeline-gates",
     "skip pipeline",
     "Pipeline: [lint, test, build, deploy]"),
    # skip checks
    ("ci-pipeline-gates",
     "skip-checks",
     "All checks passed"),
    # bypass lint
    ("ci-pipeline-gates",
     "bypass lint check",
     "Lint: eslint . --fix"),
    # [skip tests]
    ("ci-pipeline-gates",
     "[skip tests]",
     "Tests: 247 passed, 0 failed"),
    # bypass security
    ("ci-pipeline-gates",
     "bypass security gate",
     "Security: trivy scan passed"),
    # skip gate
    ("ci-pipeline-gates",
     "skip-gate",
     "Gate status: all green"),
    # [skip tests] different phrasing
    ("ci-pipeline-gates",
     "[skip tests]",
     "Test results: PASS"),
    # [skip ci] with bracket
    ("ci-pipeline-gates",
     "[skip-ci]",
     "Deploy: canary rollout successful"),
]


@pytest.mark.parametrize("rule_id,fail,passing", CI_CASES)
def test_ci_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CI_CASES)
def test_ci_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── CD DEPLOYMENT PATTERNS ─────────────────────────────────────────────────────

CD_CASES = [
    # direct to prod
    ("cd-deployment-patterns",
     "deploy directly to production",
     "deploy to canary then production"),
    # strategy: recreate
    ("cd-deployment-patterns",
     "strategy: Recreate",
     "strategy: RollingUpdate"),
    # push-to-prod
    ("cd-deployment-patterns",
     "push-to-prod",
     "deploy: blue-green to production"),
    # deploy directly to prod
    ("cd-deployment-patterns",
     "deploy direct to prod",
     "deploy canary to prod at 10% traffic"),
    # update-prod-directly
    ("cd-deployment-patterns",
     "update-prod-directly",
     "update-prod-via-canary"),
    # helm upgrade --force
    ("cd-deployment-patterns",
     "helm upgrade myapp --install --force",
     "helm upgrade myapp --install"),
    # kubectl set image --all on prod
    ("cd-deployment-patterns",
     "kubectl set image deploy/app app=app:v2 --all",
     "kubectl set image deploy/canary app=app:v2"),
    # direct to production
    ("cd-deployment-patterns",
     "deploy directly to prod",
     "deploy: strategy blue-green, target production"),
    # recreate strategy
    ("cd-deployment-patterns",
     "strategy: Recreate # causes downtime",
     "strategy: RollingUpdate maxSurge=1 maxUnavailable=0"),
]


@pytest.mark.parametrize("rule_id,fail,passing", CD_CASES)
def test_cd_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CD_CASES)
def test_cd_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── MONITORING & OBSERVABILITY ─────────────────────────────────────────────────

MONITOR_CASES = [
    # print("log ...") unstructured
    ("monitoring-observability",
     'print("log: user created")',
     'logger.info("user created", user_id=42)'),
    # format: text
    ("monitoring-observability",
     "format: text",
     "format: json"),
    # logging: print
    ("monitoring-observability",
     "logging: print",
     "logging: json"),
    # logging: echo (shell)
    ("monitoring-observability",
     "logging: echo 'started'",
     "logging: json format"),
    # console.log debugging
    ("monitoring-observability",
     "console.log('request received')",
     "structuredLogger.info('request received')"),
    # console.info
    ("monitoring-observability",
     "console.info('order placed')",
     "logger.info('order placed', order_id=123)"),
]


@pytest.mark.parametrize("rule_id,fail,passing", MONITOR_CASES)
def test_monitor_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", MONITOR_CASES)
def test_monitor_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SLO / SLI ──────────────────────────────────────────────────────────────────

SLO_CASES = [
    # slo: 99.9% without rationale
    ("slo-sli",
     "slo: 99.9%",
     "slo: 99.95%  # 99.9% external SLA requires headroom"),
    # missing SLO
    ("slo-sli",
     "missing service level objective definition",
     "slo: { availability: 99.95%, rationale: 'business requirement' }"),
    # error_budget: none
    ("slo-sli",
     "error_budget: none",
     "error_budget: { monthly: 21m, remaining: 12m }"),
    # no SLO defined
    ("slo-sli",
     "no SLO defined for user-api",
     "SLO: latency_p99 < 200ms, availability > 99.95%"),
    # error_budget: null
    ("slo-sli",
     "error_budget: null",
     "error_budget: { monthly: 21m }"),
    # error_budget: 0
    ("slo-sli",
     "error_budget: 0",
     "error_budget: { monthly: 21m, consumed: 9, remaining: 12 }"),
    # error_budget: missing
    ("slo-sli",
     "error_budget: missing",
     "error_budget: { monthly_minutes: 21 }"),
    # slo: 99.9 on its own line
    ("slo-sli",
     "slo: 99.9",
     "sli: latency_p99 < 200ms, availability > 99.95%"),
    # no slos defined
    ("slo-sli",
     "no slos defined for billing",
     "slos defined for billing: latency, availability, error_rate"),
    # missing SLO
    ("slo-sli",
     "missing SLO",
     "SLO defined and documented"),
]


@pytest.mark.parametrize("rule_id,fail,passing", SLO_CASES)
def test_slo_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SLO_CASES)
def test_slo_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── INFRASTRUCTURE AS CODE ─────────────────────────────────────────────────────

IAC_CASES = [
    # ssh into prod to edit config
    ("infrastructure-as-code",
     "ssh ubuntu@prod-01 'sudo vi /etc/config/app.conf'",
     "ansible-playbook -i prod deploy.yml"),
    # manual change to infra
    ("infrastructure-as-code",
     "manual change to production infra detected",
     "terraform apply -auto-approve infra/production"),
    # ssh prod to setup
    ("infrastructure-as-code",
     "ssh deployer@production-server 'setup nginx'",
     "kubectl apply -f k8s/prod/"),
    # manual provision server
    ("infrastructure-as-code",
     "manual provision of config file on server",
     "terraform plan infra/production"),
    # manual edit of production env
    ("infrastructure-as-code",
     "manual edit of production environment config",
     "helm upgrade myapp --values values/prod.yaml"),
    # patch running instance
    ("infrastructure-as-code",
     "patch running instance prod-web-01 with latest security fix",
     "Rolling update: replaced all instances with new AMI"),
    # drift disabled
    ("infrastructure-as-code",
     "drift: disabled",
     "drift_detection: { enabled: true, schedule: '0 */6 * * *' }"),
    # drift off
    ("infrastructure-as-code",
     "drift: off",
     "drift: { enabled: true, auto_remediate: true }"),
    # patch running server
    ("infrastructure-as-code",
     "patch running production server",
     "Blue-green deploy: new instance group created"),
]


@pytest.mark.parametrize("rule_id,fail,passing", IAC_CASES)
def test_iac_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", IAC_CASES)
def test_iac_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── CONTAINERIZATION ───────────────────────────────────────────────────────────

CONTAINER_CASES = [
    # ssh into container
    ("containerization",
     "ssh into container",
     "kubectl exec app-5d7f8 -- cat /var/log/app.log"),
    # privileged: true
    ("containerization",
     "privileged: true",
     "privileged: false"),
    # bash as entrypoint
    ("containerization",
     'entrypoint: ["bash"]',
     'command: ["./app"]'),
    # /bin/sh as entrypoint
    ("containerization",
     'entrypoint: ["/bin/sh"]',
     'entrypoint: ["/app/server"]'),
    # readOnlyRootFilesystem: false
    ("containerization",
     "readOnlyRootFilesystem: false",
     "readOnlyRootFilesystem: true"),
    # docker exec -it
    ("containerization",
     "docker exec -it myapp bash",
     "docker logs myapp"),
    # ssh to docker
    ("containerization",
     "ssh to docker container for debugging",
     "kubectl exec -it app-5d7f8 -- ls /tmp"),
    # ssh into pod
    ("containerization",
     "ssh into pod for manual fix",
     "kubectl logs app-5d7f8 -c app"),
    # securityContext without readOnlyRootFilesystem
    ("containerization",
     "securityContext: { runAsNonRoot: true, capabilities: { drop: [ALL] } }",
     "securityContext: { readOnlyRootFilesystem: true, runAsNonRoot: true }"),
    # sh entrypoint
    ("containerization",
     'entrypoint: ["sh"]',
     'entrypoint: ["./server"]'),
]


@pytest.mark.parametrize("rule_id,fail,passing", CONTAINER_CASES)
def test_container_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", CONTAINER_CASES)
def test_container_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SECRETS MANAGEMENT ─────────────────────────────────────────────────────────

SECRETS_CASES = [
    # password hardcoded
    ("secrets-management",
     'password: "s3cr3t-p@ss!"',
     'password: ${DB_PASSWORD}'),
    # api_key hardcoded
    ("secrets-management",
     'api_key: "sk_live_abc123def456"',
     'api_key: ${STRIPE_SECRET_KEY}'),
    # token hardcoded
    ("secrets-management",
     'token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0"',
     'token = os.getenv("AUTH_TOKEN")'),
    # secret with long value
    ("secrets-management",
     'secret: "my-super-secret-key-change-me"',
     'secret_file: /run/secrets/app'),
    # credential hardcoded
    ("secrets-management",
     'credential: "A1B2C3D4E5F6G7H8I9J0"',
     'credential: ${AWS_CREDENTIAL}'),
    # passwd hardcoded
    ("secrets-management",
     'passwd = "admin123!"',
     'password: ${VAULT_PASSWORD}'),
    # api-key with hyphen
    ("secrets-management",
     'api-key: "sk-test-abcdefghijklmnop"',
     'api_key: ${STRIPE_TEST_KEY}'),
    # DEFAULT_PASSWORD
    ("secrets-management",
     'DEFAULT_PASSWORD=changeme',
     'password: ${VAULT_SECRET}'),
    # pwd hardcoded
    ("secrets-management",
     'pwd = "hunter2!"',
     'pwd: ${DB_PASSWORD}'),
    # hardcoded password
    ("secrets-management",
     'hardcoded password found in config.py',
     'password retrieved from vault'),
    # hardcoded key
    ("secrets-management",
     'hardcoded secret key',
     'secret key loaded from secret store'),
]


@pytest.mark.parametrize("rule_id,fail,passing", SECRETS_CASES)
def test_secrets_fail_triggers_rule(rule_id, fail, passing):
    assert rule_id in _rules_for(fail), f"{rule_id}: FAIL example did not trigger"


@pytest.mark.parametrize("rule_id,fail,passing", SECRETS_CASES)
def test_secrets_pass_does_not_trigger_rule(rule_id, fail, passing):
    assert rule_id not in _rules_for(passing), f"{rule_id}: PASS example triggered"


# ── SENTINEL / INTEGRATION CHECKS ──────────────────────────────────────────────


def test_syllabus_loads_and_has_rules():
    cls = load_syllabus("devops")
    assert cls["class"]["id"] == "devops"
    assert cls["class"]["version"] == "1.0.0"
    assert len(cls["rules"]) == 17


def test_clean_pipeline_passes():
    clean = (
        'pipeline:\n'
        '  stages: [lint, test, build, security]\n'
        'logging:\n'
        '  format: json\n'
        '  correlation_id: x-request-id\n'
        'metrics:\n'
        '  - latency_p99\n'
        '  - requests_per_second\n'
        '  - error_rate\n'
        '  - cpu_utilization\n'
        'deploy:\n'
        '  strategy: blue-green\n'
        'containers:\n'
        '  - command: ["./app"]\n'
        '    securityContext:\n'
        '      readOnlyRootFilesystem: true\n'
        '      runAsNonRoot: true\n'
        'secrets:\n'
        '  password: ${DB_PASSWORD}\n'
        'slo:\n'
        '  availability: 99.95%\n'
        '  rationale: "headroom against 99.9% SLA"\n'
    )
    result = grade(clean, "devops")
    assert result.passed, result.violations


def test_unknown_class_is_graceful():
    result = grade("print('log: test')", "no-such-class")
    assert result.error is not None
    assert result.passed is False


def test_all_checkable_rules_have_test_coverage():
    """Every rule with check_regex should have a FAIL/PASS test pair."""
    cls = load_syllabus("devops")
    checkable = {r["id"] for r in cls["rules"] if "check_regex" in r}
    assert len(checkable) == 7, f"Expected 7 checkable rules, got {len(checkable)}"
    # Verify each checkable rule appears in at least one test case
    tested_rules = set()
    for cases in [CI_CASES, CD_CASES, MONITOR_CASES, SLO_CASES,
                  IAC_CASES, CONTAINER_CASES, SECRETS_CASES]:
        for rule_id, _, _ in cases:
            tested_rules.add(rule_id)
    # Map test group rule_ids that may have typos
    assert checkable == tested_rules, (
        f"Missing tests for: {checkable - tested_rules}. "
        f"Extra tests: {tested_rules - checkable}"
    )
