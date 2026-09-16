"use client";

interface ResearchProgressProps {
  progress: number;
  step: number;
  currentStep: string;
  currentDescription: string;
}

const steps = [
  {
    title: "Understanding your question",
    description: "Analyzing the research objective",
  },
  {
    title: "Creating research plan",
    description: "Breaking the question into research topics",
  },
  {
    title: "Searching the web",
    description: "Finding relevant sources",
  },
  {
    title: "Analyzing sources",
    description: "Reading and processing source material",
  },
  {
    title: "Extracting evidence",
    description: "Identifying useful evidence and claims",
  },
  {
    title: "Checking research gaps",
    description: "Determining whether more research is needed",
  },
  {
    title: "Preparing report",
    description: "Synthesizing the research findings",
  },
];

export default function ResearchProgress({
  progress,
  step,
  currentStep,
  currentDescription,
}: ResearchProgressProps) {
  return (
    <div className="w-full max-w-2xl mx-auto">

      <div className="text-center mb-10">

        <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl border border-indigo-500/30 bg-indigo-500/10">

          <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-400/30 border-t-indigo-400" />

        </div>

        <h1 className="text-3xl font-bold text-white">
          {currentStep || "Researching..."}
        </h1>

        <p className="mt-3 text-sm text-slate-400">
          {currentDescription ||
            "ResearchPilot is investigating your question across multiple sources."}
        </p>

      </div>

      <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-7 shadow-2xl">

        <div className="mb-7">

          <div className="mb-3 flex items-center justify-between">

            <span className="text-xs font-medium text-slate-400">
              Research progress
            </span>

            <span className="text-xs text-slate-500">
              {progress}%
            </span>

          </div>

          <div className="h-1.5 overflow-hidden rounded-full bg-slate-800">

            <div
              className="h-full rounded-full bg-indigo-400 transition-all duration-700 ease-out"
              style={{
                width: `${Math.min(
                  Math.max(progress, 0),
                  100,
                )}%`,
              }}
            />

          </div>

        </div>

        <div className="space-y-5">

          {steps.map((item, index) => {

            const stepNumber = index + 1;

            const completed =
              stepNumber < step;

            const active =
              stepNumber === step;

            return (
              <div
                key={item.title}
                className="flex items-start gap-4"
              >

                <div
                  className={[
                    "mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border text-xs transition-all",
                    completed
                      ? "border-emerald-500/60 bg-emerald-500/10 text-emerald-400"
                      : active
                        ? "border-indigo-400/60 bg-indigo-500/10 text-indigo-300"
                        : "border-slate-700 bg-slate-900 text-slate-600",
                  ].join(" ")}
                >
                  {completed ? "✓" : active ? "•" : ""}
                </div>

                <div className="min-w-0">

                  <p
                    className={[
                      "text-sm font-medium",
                      completed || active
                        ? "text-white"
                        : "text-slate-600",
                    ].join(" ")}
                  >
                    {item.title}
                  </p>

                  <p
                    className={[
                      "mt-1 text-xs",
                      completed || active
                        ? "text-slate-500"
                        : "text-slate-700",
                    ].join(" ")}
                  >
                    {item.description}
                  </p>

                </div>

              </div>
            );
          })}

        </div>

      </div>
    </div>
  );
}