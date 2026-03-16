import type { AnalysisResult } from "../services/api";

type AnalysisResultCardProps = {
  title: string;
  result: AnalysisResult | null;
  loading?: boolean;
  error?: string | null;
};

export default function AnalysisResultCard({ title, result, loading, error }: AnalysisResultCardProps) {
  return (
    <section className="panel">
      <h3 className="text-lg font-extrabold text-steel">{title}</h3>
      {loading && <p className="mt-4 text-sm text-steel/70">Analyzing logs with AI engine...</p>}
      {error && <p className="mt-4 text-sm text-rose-700">{error}</p>}
      {!loading && !error && !result && (
        <p className="mt-4 text-sm text-steel/70">Submit logs or questions to view AI diagnostics.</p>
      )}
      {!loading && result && (
        <div className="mt-4 space-y-4 text-sm text-steel">
          <div>
            <p className="font-bold">Summary</p>
            <p>{result.summary}</p>
          </div>
          <div>
            <p className="font-bold">Probable Root Cause</p>
            <p>{result.probable_root_cause}</p>
          </div>
          <div>
            <p className="font-bold">Suggested Fixes</p>
            <ul className="mt-2 list-disc space-y-1 pl-5">
              {result.suggested_fixes.map((fix) => (
                <li key={fix}>{fix}</li>
              ))}
            </ul>
          </div>
          <div>
            <p className="font-bold">Follow-up Checks</p>
            <ul className="mt-2 list-disc space-y-1 pl-5">
              {result.follow_up_checks.map((check) => (
                <li key={check}>{check}</li>
              ))}
            </ul>
          </div>
          <p className="font-semibold">Confidence: {(result.confidence * 100).toFixed(0)}%</p>
        </div>
      )}
    </section>
  );
}
