import json

from ai.base import AIEngine
from ai.prompt_builder import build_kubernetes_prompt, build_log_analysis_prompt
from models.schemas import AIAnalysisResult


class MockAIEngine(AIEngine):
    """Fallback mock — used when no LLM provider is configured."""

    async def analyze_logs(self, logs: str, context: str | None = None) -> AIAnalysisResult:
        _ = build_log_analysis_prompt(logs=logs, context=context)

        lowered = logs.lower()
        if "outofmemory" in lowered or "oomkilled" in lowered:
            root_cause = "Container exceeded memory limits and was OOM-killed."
            fixes = [
                "Increase pod/container memory limits and requests.",
                "Profile memory usage and optimize memory-intensive code paths.",
                "Add VPA/HPA policies to absorb load spikes.",
            ]
        elif "imagepullbackoff" in lowered:
            root_cause = "Container image could not be pulled due to auth/tag/registry issues."
            fixes = [
                "Validate image name/tag and ensure the tag exists in the registry.",
                "Verify image pull secret in namespace and service account.",
                "Check network connectivity from node to registry endpoint.",
            ]
        elif "permission denied" in lowered:
            root_cause = "Insufficient permissions for the attempted operation."
            fixes = [
                "Review IAM/RBAC permissions for the principal running the task.",
                "Validate filesystem permissions and container user IDs.",
                "Audit recent policy changes in CI/CD or cluster roles.",
            ]
        else:
            root_cause = "General runtime or configuration failure requiring targeted validation."
            fixes = [
                "Check application configuration, secrets, and environment variables.",
                "Verify recent deployment and infrastructure changes.",
                "Correlate logs with metrics and events to isolate timing of failure.",
            ]

        return AIAnalysisResult(
            summary="Log analysis completed with heuristic inference.",
            probable_root_cause=root_cause,
            confidence=0.72,
            suggested_fixes=fixes,
            follow_up_checks=[
                "Confirm fix in a staging environment.",
                "Set alert rules for recurrence indicators.",
                "Capture post-incident notes for runbook updates.",
            ],
        )

    async def troubleshoot_kubernetes(self, describe_output: str, pod_logs: str | None = None) -> AIAnalysisResult:
        _ = build_kubernetes_prompt(describe_output=describe_output, pod_logs=pod_logs)
        combined = f"{describe_output}\n{pod_logs or ''}".lower()

        if "crashloopbackoff" in combined:
            root_cause = "Application repeatedly crashes after startup, causing CrashLoopBackOff."
            fixes = [
                "Inspect startup command/args and validate container entrypoint.",
                "Confirm required env vars/secrets/config maps are mounted and valid.",
                "Increase startup probe grace period if app boot is slow.",
            ]
        elif "failedscheduling" in combined:
            root_cause = "Scheduler cannot place pod due to resource or affinity constraints."
            fixes = [
                "Check node capacity and resource requests/limits.",
                "Review node selectors, taints/tolerations, and affinity rules.",
                "Scale node pool or relax constraints.",
            ]
        else:
            root_cause = "Kubernetes workload instability likely tied to config, resources, or dependencies."
            fixes = [
                "Review Events section in describe output for first failure signal.",
                "Validate service endpoints/dependencies and DNS resolution.",
                "Correlate pod restarts with cluster resource pressure.",
            ]

        return AIAnalysisResult(
            summary="Kubernetes troubleshooting analysis completed.",
            probable_root_cause=root_cause,
            confidence=0.74,
            suggested_fixes=fixes,
            follow_up_checks=[
                "Run kubectl get events --sort-by=.lastTimestamp.",
                "Check node and namespace quotas.",
                "Create/update runbook with confirmed fix.",
            ],
        )


class OpenAIEngine(AIEngine):
    """Real OpenAI-backed engine using the Chat Completions API."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        from openai import AsyncOpenAI  # pyright: ignore[reportMissingImports]

        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def analyze_logs(self, logs: str, context: str | None = None) -> AIAnalysisResult:
        _ = build_log_analysis_prompt(logs=logs, context=context)

        system_prompt = (
            "You are DevOpsBrain, an expert DevOps AI assistant specialising in Kubernetes, Docker, "
            "CI/CD pipelines, and Linux systems. Analyze the provided log text and respond ONLY with "
            "a valid JSON object using exactly these keys:\n"
            '{"summary": "<one-sentence summary>", '
            '"probable_root_cause": "<concise root cause>", '
            '"confidence": <float 0.0-1.0>, '
            '"suggested_fixes": ["<fix 1>", "<fix 2>", "..."], '
            '"follow_up_checks": ["<check 1>", "<check 2>", "..."]}'
        )
        user_content = logs if not context else f"{context}\n\n---\n{logs}"

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=1024,
        )

        data = json.loads(response.choices[0].message.content or "{}")
        return AIAnalysisResult(
            summary=data.get("summary", "Analysis complete."),
            probable_root_cause=data.get("probable_root_cause", "Unable to determine root cause."),
            confidence=float(min(max(data.get("confidence", 0.7), 0.0), 1.0)),
            suggested_fixes=data.get("suggested_fixes", []),
            follow_up_checks=data.get("follow_up_checks", []),
        )

    async def troubleshoot_kubernetes(self, describe_output: str, pod_logs: str | None = None) -> AIAnalysisResult:
        _ = build_kubernetes_prompt(describe_output=describe_output, pod_logs=pod_logs)

        system_prompt = (
            "You are DevOpsBrain, an expert Kubernetes SRE AI. Analyze the kubectl describe and log "
            "output to diagnose issues such as CrashLoopBackOff, ImagePullBackOff, OOMKilled, "
            "FailedScheduling, and liveness/readiness probe failures. Include specific kubectl "
            "commands in suggested_fixes where helpful. Respond ONLY with a valid JSON object using "
            "exactly these keys:\n"
            '{"summary": "<one-sentence summary>", '
            '"probable_root_cause": "<concise root cause>", '
            '"confidence": <float 0.0-1.0>, '
            '"suggested_fixes": ["<fix or kubectl command>", "..."], '
            '"follow_up_checks": ["<check 1>", "..."]}'
        )
        user_content = f"kubectl describe output:\n{describe_output}"
        if pod_logs:
            user_content += f"\n\nkubectl logs output:\n{pod_logs}"

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=1024,
        )

        data = json.loads(response.choices[0].message.content or "{}")
        return AIAnalysisResult(
            summary=data.get("summary", "Kubernetes analysis complete."),
            probable_root_cause=data.get("probable_root_cause", "Unable to determine root cause."),
            confidence=float(min(max(data.get("confidence", 0.7), 0.0), 1.0)),
            suggested_fixes=data.get("suggested_fixes", []),
            follow_up_checks=data.get("follow_up_checks", []),
        )


def create_ai_engine(provider: str, api_key: str | None = None, model: str = "gpt-4o-mini") -> AIEngine:
    """Provider-aware factory. Returns OpenAIEngine when provider='openai' and api_key is set."""
    if provider == "openai" and api_key:
        return OpenAIEngine(api_key=api_key, model=model)
    return MockAIEngine()
