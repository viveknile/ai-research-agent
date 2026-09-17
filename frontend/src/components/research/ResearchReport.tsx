"use client";

interface ResearchReportProps {
  result?: Record<string, unknown>;
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
  const safeResult = result ?? {};

  const report =
    safeResult.final_report &&
    typeof safeResult.final_report === "object"
      ? (safeResult.final_report as FinalReport)
      : null;

  if (!report) {
    return (
      <main className="min-h-screen overflow-x-hidden px-4 py-8 sm:px-6 sm:py-10">
        <div className="mx-auto w-full max-w-4xl">

          <button
            onClick={onBack}
            className="mb-6 min-h-10 text-sm text-slate-400 transition hover:text-white sm:mb-8"
          >
            ← Start New Research
          </button>

          <div className="rounded-2xl border border-red-400/20 bg-red-400/5 p-5 sm:p-6">
            <h1 className="text-xl font-semibold text-white">
              Report unavailable
            </h1>

            <p className="mt-2 text-sm leading-6 text-slate-400">
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
    <main className="min-h-screen overflow-x-hidden px-4 py-8 sm:px-6 sm:py-10">
      <div className="mx-auto w-full max-w-5xl">

        {/* Header */}

        <button
          onClick={onBack}
          className="mb-6 min-h-10 text-sm text-slate-400 transition hover:text-white sm:mb-8"
        >
          ← Start New Research
        </button>

        <div className="mb-8 sm:mb-10">
          <div className="mb-2 text-sm font-medium text-indigo-400">
            ResearchPilot
          </div>

          <h1 className="break-words text-2xl font-bold tracking-tight text-white sm:text-3xl md:text-4xl">
            {report.title ?? "Research Report"}
          </h1>
        </div>

        {/* Executive Summary */}

        <section className="mb-4 rounded-2xl border border-white/10 bg-slate-900/70 p-5 sm:mb-6 sm:p-6">
          <h2 className="mb-3 text-lg font-semibold text-white sm:mb-4 sm:text-xl">
            Executive Summary
          </h2>

          <p className="break-words text-sm leading-7 text-slate-300 sm:text-base sm:leading-8">
            {report.executive_summary ??
              "No executive summary was generated."}
          </p>
        </section>

        {/* Key Findings */}

        <section className="mb-4 rounded-2xl border border-white/10 bg-slate-900/70 p-5 sm:mb-6 sm:p-6">
          <div className="mb-5 sm:mb-6">
            <h2 className="text-lg font-semibold text-white sm:text-xl">
              Key Findings
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Evidence-backed findings from the research.
            </p>
          </div>

          {findings.length === 0 ? (
            <p className="text-sm text-slate-400">
              No findings were generated.
            </p>
          ) : (
            <div className="space-y-4 sm:space-y-5">
              {findings.map((finding, index) => (
                <article
                  key={`${finding.statement ?? "finding"}-${index}`}
                  className="rounded-xl border border-white/10 bg-slate-950/50 p-4 sm:p-5"
                >
                  <div className="flex items-start gap-3 sm:gap-4">

                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-indigo-500/15 text-sm font-semibold text-indigo-300">
                      {index + 1}
                    </div>

                    <div className="min-w-0 flex-1">

                      <p className="break-words text-sm leading-7 text-slate-200 sm:text-base">
                        {finding.statement ??
                          "No finding statement available."}
                      </p>

                      <div className="mt-3 flex flex-wrap items-center gap-2 sm:gap-3">

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

                            if (
                              !citation ||
                              !citation.url
                            ) {
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
                                [
                                {citationId.replace(
                                  "source-",
                                  ""
                                )}
                                ]
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

        <section className="mb-6 rounded-2xl border border-white/10 bg-slate-900/70 p-5 sm:mb-8 sm:p-6">
          <div className="mb-5 sm:mb-6">
            <h2 className="text-lg font-semibold text-white sm:text-xl">
              Sources
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Sources referenced during the research.
            </p>
          </div>

          {citations.length === 0 ? (
            <p className="text-sm text-slate-400">
              No sources were available.
            </p>
          ) : (
            <div className="space-y-3">
              {citations.map((citation, index) => {
                if (!citation.url) {
                  return null;
                }

                return (
                  <a
                    key={
                      citation.citation_id ??
                      citation.source_id ??
                      index
                    }
                    href={citation.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block min-w-0 rounded-xl border border-white/10 bg-slate-950/50 p-4 transition hover:border-indigo-400/30 hover:bg-slate-950"
                  >
                    <div className="flex min-w-0 items-start gap-3 sm:gap-4">

                      <span className="shrink-0 text-sm text-indigo-300">
                        [{index + 1}]
                      </span>

                      <div className="min-w-0 flex-1">

                        <h3 className="break-words text-sm font-medium text-white sm:text-base">
                          {citation.title ??
                            "Untitled source"}
                        </h3>

                        {citation.domain && (
                          <p className="mt-1 break-words text-xs text-indigo-300">
                            {citation.domain}
                          </p>
                        )}

                        <p className="mt-2 break-all text-xs leading-5 text-slate-500">
                          {citation.url}
                        </p>

                      </div>
                    </div>
                  </a>
                );
              })}
            </div>
          )}
        </section>

        {/* Footer */}

        <div className="flex justify-center">
          <button
            onClick={onBack}
            className="min-h-11 w-full rounded-xl border border-white/10 bg-slate-900 px-6 py-3 text-sm font-medium text-slate-200 transition hover:bg-slate-800 sm:w-auto"
          >
            Start New Research
          </button>
        </div>

      </div>
    </main>
  );
}