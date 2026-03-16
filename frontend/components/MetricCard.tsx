type MetricCardProps = {
  label: string;
  value: string;
  status: string;
};

function badgeColor(status: string): string {
  switch (status) {
    case "healthy":
      return "bg-emerald-100 text-emerald-700";
    case "warning":
      return "bg-amber-100 text-amber-700";
    case "critical":
      return "bg-rose-100 text-rose-700";
    default:
      return "bg-slate-100 text-slate-700";
  }
}

export default function MetricCard({ label, value, status }: MetricCardProps) {
  return (
    <article className="panel min-h-40">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wide text-steel/80">{label}</h3>
        <span className={`rounded-full px-3 py-1 text-xs font-bold ${badgeColor(status)}`}>{status}</span>
      </div>
      <p className="mt-5 text-xl font-bold text-steel">{value}</p>
    </article>
  );
}
