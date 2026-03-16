from dataclasses import dataclass


@dataclass
class PrometheusIntegration:
    """Prometheus query abstraction to keep API layer decoupled."""

    async def get_resource_usage_summary(self) -> str:
        return "CPU 78% | Memory 81%"
