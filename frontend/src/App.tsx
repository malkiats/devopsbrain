import { useState } from "react";

import AnalyzerPage from "../pages/AnalyzerPage";
import AssistantPage from "../pages/AssistantPage";
import DashboardPage from "../pages/DashboardPage";

type Page = "dashboard" | "analyzer" | "assistant";

export default function App() {
  const [page, setPage] = useState<Page>("dashboard");

  return (
    <main className="mx-auto max-w-7xl px-4 py-8 md:px-8">
      <header className="mb-6 rounded-3xl bg-steel p-6 text-white shadow-card">
        <p className="text-xs font-bold uppercase tracking-[0.2em] text-mint">DevOpsBrain</p>
        <h1 className="mt-2 text-3xl font-extrabold md:text-4xl">AI-Powered DevOps Command Center</h1>
        <p className="mt-2 max-w-3xl text-sm text-white/85">
          Diagnose incidents, explain CI/CD failures, and troubleshoot Kubernetes from one modular interface.
        </p>

        <nav className="mt-5 flex flex-wrap gap-2">
          {[
            { key: "dashboard", label: "Health Dashboard" },
            { key: "analyzer", label: "Analyzers" },
            { key: "assistant", label: "AI Assistant" },
          ].map((item) => (
            <button
              key={item.key}
              type="button"
              onClick={() => setPage(item.key as Page)}
              className={`rounded-full px-4 py-2 text-sm font-bold transition ${
                page === item.key ? "bg-mint text-steel" : "bg-white/20 text-white"
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </header>

      {page === "dashboard" && <DashboardPage />}
      {page === "analyzer" && <AnalyzerPage />}
      {page === "assistant" && <AssistantPage />}
    </main>
  );
}
