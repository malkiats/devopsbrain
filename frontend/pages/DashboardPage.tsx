import { useEffect, useState } from "react";

import MetricCard from "../components/MetricCard";
import { fetchDashboardHealth, type DashboardHealth } from "../services/api";

export default function DashboardPage() {
  const [health, setHealth] = useState<DashboardHealth | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardHealth().then(setHealth).catch((err: Error) => setError(err.message));
  }, []);

  return (
    <section className="space-y-5">
      <header>
        <h2 className="text-2xl font-extrabold text-steel">Infrastructure Health Dashboard</h2>
        <p className="text-sm text-steel/80">Cluster status, pod failures, and resource usage at a glance.</p>
      </header>
      {error && <p className="rounded-xl bg-rose-100 px-4 py-2 text-rose-700">{error}</p>}
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard
          label={health?.cluster_status.name ?? "Cluster Status"}
          value={health?.cluster_status.value ?? "Loading..."}
          status={health?.cluster_status.status ?? "unknown"}
        />
        <MetricCard
          label={health?.pod_failures.name ?? "Pod Failures"}
          value={health?.pod_failures.value ?? "Loading..."}
          status={health?.pod_failures.status ?? "unknown"}
        />
        <MetricCard
          label={health?.resource_usage.name ?? "Resource Usage"}
          value={health?.resource_usage.value ?? "Loading..."}
          status={health?.resource_usage.status ?? "unknown"}
        />
      </div>
    </section>
  );
}
