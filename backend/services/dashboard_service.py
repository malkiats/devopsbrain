from datetime import datetime, timezone

from models.schemas import DashboardHealthResponse, HealthMetric


class DashboardService:
    """Service that composes health metrics from integrations.

    For MVP this returns placeholders, but the interface is stable for real providers.
    """

    async def get_health_snapshot(self) -> DashboardHealthResponse:
        now = datetime.now(timezone.utc)
        return DashboardHealthResponse(
            cluster_status=HealthMetric(
                name="Cluster Status",
                status="healthy",
                value="All control-plane checks passing",
                updated_at=now,
            ),
            pod_failures=HealthMetric(
                name="Pod Failures",
                status="warning",
                value="3 pods in CrashLoopBackOff",
                updated_at=now,
            ),
            resource_usage=HealthMetric(
                name="Resource Usage",
                status="warning",
                value="CPU 78% | Memory 81%",
                updated_at=now,
            ),
        )
