"use client";

interface ResearchReportProps {
  result: Record<string, unknown>;
  onBack: () => void;
}

interface Citation {
  citation_id?: string;
  source_id?: string;
  title?: string;
  url?: string;
  domain?: string;
}

interface Finding {
  statement?: string;
  confidence?: number;
  citation_ids?: string[];
}

interface FinalReport {
  title?: string;
  executive_summary?: string;
  findings?: Finding[];
  citations?: Citation[];
}

export default function ResearchReport({
  result,
  onBack,
}: ResearchReportProps) {
  const report =
    result.final_report &&
    typeof result.final_report === "object"
      ? (result.final_report as FinalReport)
      : null;

  if (!report) {
    return (
      <main className="min-h-screen px-6 py-10">
        <div className="mx-auto max-w-4xl">
          <button
            onClick={onBack}
            className="mb-8 text-sm text-slate-400 transition hover:text-white"
          >
            ← Start New Research
          </button>

          <div className="rounded-2xl border border-red-400/20 bg-red-400/5 p-6">
            <h1 className="text-xl font-semibold text-white">
              Report unavailable
            </h1>

            <p className="mt-2 text-sm text-slate-400">
              The research completed, but a final report was not generated.
            </p>
          </div>
        </div>
      </main>
    );
  }

  const findings = report.findings ?? [];
  const citations = report.citations ?? [];

  const citationMap = new Map(
    citations.map((citation) => [
      citation.citation_id,
      citation,
    ])
  );

  return (
    <main className="min-h-screen px-6 py-10">
      <div className="mx-auto max-w-5xl">
        {/* Header */}

        <button
          onClick={onBack}
          className="mb-8 text-sm text-slate-400 transition hover:text-white"
        >
          ← Start New Research
        </button>

        <div className="mb-10">
          <div className="mb-3 text-sm font-medium text-indigo-400">
            ResearchPilot
          </div>

          <h1 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
            {report.title ?? "Research Report"}
          </h1>
        </div>

        {/* Executive Summary */}

        <section className="mb-6 rounded-2xl border border-white/10 bg-slate-900/70 p-6">
          <h2 className="mb-4 text-xl font-semibold text-white">
            Executive Summary
          </h2>

          <p className="leading-8 text-slate-300">
            {report.executive_summary}
          </p>
        </section>

        {/* Key Findings */}

        <section className="mb-6 rounded-2xl border border-white/10 bg-slate-900/70 p-6">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-white">
              Key Findings
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Evidence-backed findings from the research.
            </p>
          </div>

          {findings.length === 0 ? (
            <p className="text-slate-400">
              No findings were generated.
            </p>
          ) : (
            <div className="space-y-5">
              {findings.map((finding, index) => (
                <article
                  key={`${finding.statement}-${index}`}
                  className="rounded-xl border border-white/10 bg-slate-950/50 p-5"
                >
                  <div className="flex gap-4">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-indigo-500/15 text-sm font-semibold text-indigo-300">
                      {index + 1}
                    </div>

                    <div className="min-w-0 flex-1">
                      <p className="leading-7 text-slate-200">
                        {finding.statement}
                      </p>

                      <div className="mt-3 flex flex-wrap items-center gap-3">
                        {typeof finding.confidence ===
                          "number" && (
                          <span className="text-xs text-slate-500">
                            Confidence:{" "}
                            {Math.round(
                              finding.confidence * 100
                            )}
                            %
                          </span>
                        )}

                        {(finding.citation_ids ?? []).map(
                          (citationId) => {
                            const citation =
                              citationMap.get(
                                citationId
                              );

                            if (!citation) {
                              return null;
                            }

                            return (
                              <a
                                key={citationId}
                                href={citation.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="rounded-md bg-indigo-400/10 px-2 py-1 text-xs font-medium text-indigo-300 transition hover:bg-indigo-400/20"
                              >
                                [{citationId.replace(
                                  "source-",
                                  ""
                                )}]
                              </a>
                            );
                          }
                        )}
                      </div>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {/* Sources */}

        <section className="mb-8 rounded-2xl border border-white/10 bg-slate-900/70 p-6">
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-white">
              Sources
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Sources referenced during the research.
            </p>
          </div>

          {citations.length === 0 ? (
            <p className="text-slate-400">
              No sources were available.
            </p>
          ) : (
            <div className="space-y-3">
              {citations.map((citation, index) => (
                <a
                  key={
                    citation.citation_id ??
                    citation.source_id ??
                    index
                  }
                  href={citation.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block rounded-xl border border-white/10 bg-slate-950/50 p-4 transition hover:border-indigo-400/30 hover:bg-slate-950"
                >
                  <div className="flex items-start gap-4">
                    <span className="text-sm text-indigo-300">
                      [{index + 1}]
                    </span>

                    <div className="min-w-0 flex-1">
                      <h3 className="font-medium text-white">
                        {citation.title ??
                          "Untitled source"}
                      </h3>

                      {citation.domain && (
                        <p className="mt-1 text-xs text-indigo-300">
                          {citation.domain}
                        </p>
                      )}

                      <p className="mt-2 break-all text-xs text-slate-500">
                        {citation.url}
                      </p>
                    </div>
                  </div>
                </a>
              ))}
            </div>
          )}
        </section>

        {/* Footer */}

        <div className="flex justify-center">
          <button
            onClick={onBack}
            className="rounded-xl border border-white/10 bg-slate-900 px-6 py-3 text-sm font-medium text-slate-200 transition hover:bg-slate-800"
          >
            Start New Research
          </button>
        </div>
      </div>
    </main>
  );
}