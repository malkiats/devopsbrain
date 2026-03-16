from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class LogAnalysisRequest(BaseModel):
    source: Literal["log_file", "pipeline", "kubernetes", "linux"] = "log_file"
    content: str = Field(..., min_length=10, description="Raw logs or error output")
    context: str | None = Field(default=None, description="Optional environment metadata")


class TroubleshootingRequest(BaseModel):
    cluster_name: str | None = None
    namespace: str | None = None
    resource_type: str = "pod"
    resource_name: str | None = None
    describe_output: str | None = None
    pod_logs: str | None = None


class DevOpsLogAnalysisRequest(BaseModel):
    raw_log_text: str = Field(..., min_length=10, description="Raw logs from Kubernetes, Docker, CI/CD, or Linux")


class DevOpsLogAnalysisResponse(BaseModel):
    summary: str
    root_cause: str
    recommended_fix: str
    confidence: Literal["low", "medium", "high"]


class KubernetesTroubleshootRequest(BaseModel):
    kubectl_describe_output: str = Field(..., min_length=10)
    kubectl_logs_output: str | None = None


class KubernetesIssueSuggestion(BaseModel):
    issue: str
    root_cause: str
    recommended_fix: str
    kubectl_commands: list[str]
    confidence: Literal["low", "medium", "high"]


class KubernetesTroubleshootResponse(BaseModel):
    summary: str
    detected_issues: list[str]
    suggestions: list[KubernetesIssueSuggestion]


class AIAnalysisResult(BaseModel):
    summary: str
    probable_root_cause: str
    confidence: float = Field(ge=0.0, le=1.0)
    suggested_fixes: list[str]
    follow_up_checks: list[str]


class HealthMetric(BaseModel):
    name: str
    status: Literal["healthy", "warning", "critical", "unknown"]
    value: str
    updated_at: datetime


class DashboardHealthResponse(BaseModel):
    cluster_status: HealthMetric
    pod_failures: HealthMetric
    resource_usage: HealthMetric


class APIResponse(BaseModel):
    ok: bool = True
    message: str = "success"
