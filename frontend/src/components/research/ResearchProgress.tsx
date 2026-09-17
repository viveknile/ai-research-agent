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
  const safeProgress = Math.min(
    100,
    Math.max(0, progress)
  );

  const safeStep = Math.min(
    steps.length,
    Math.max(1, step)
  );

  return (
    <main className="min-h-screen overflow-x-hidden bg-slate-950 px-4 py-8 sm:px-6 sm:py-12">
      <div className="mx-auto w-full max-w-2xl">

        {/* Header */}

        <div className="mb-8 text-center sm:mb-10">
          <div className="mb-3 text-sm font-medium text-indigo-400">
            ResearchPilot
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
            Research in progress
          </h1>

          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-400 sm:text-base">
            Your research agent is investigating the topic.
          </p>
        </div>

        {/* Progress Card */}

        <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-5 shadow-2xl sm:p-7">

          {/* Current Step */}

          <div className="mb-6">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

              <div className="min-w-0">
                <p className="break-words text-base font-semibold text-white sm:text-lg">
                  {currentStep}
                </p>

                <p className="mt-1 break-words text-sm leading-6 text-slate-400">
                  {currentDescription}
                </p>
              </div>

              <span className="shrink-0 text-sm font-medium text-indigo-300">
                {Math.round(safeProgress)}%
              </span>

            </div>
          </div>

          {/* Progress Bar */}

          <div className="mb-7 h-2 overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full rounded-full bg-indigo-500 transition-all duration-500"
              style={{
                width: `${safeProgress}%`,
              }}
            />
          </div>

          {/* Steps */}

          <div className="space-y-4">
            {steps.map((item, index) => {
              const stepNumber = index + 1;

              const isCompleted =
                stepNumber < safeStep;

              const isCurrent =
                stepNumber === safeStep;

              return (
                <div
                  key={item.title}
                  className="flex items-start gap-3 sm:gap-4"
                >

                  {/* Step Indicator */}

                  <div
                    className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-semibold transition ${
                      isCompleted
                        ? "bg-indigo-500 text-white"
                        : isCurrent
                          ? "border border-indigo-400/50 bg-indigo-400/10 text-indigo-300"
                          : "border border-white/10 bg-slate-950 text-slate-600"
                    }`}
                  >
                    {isCompleted ? "✓" : stepNumber}
                  </div>

                  {/* Step Information */}

                  <div className="min-w-0 flex-1 pt-0.5">
                    <p
                      className={`break-words text-sm font-medium ${
                        isCurrent || isCompleted
                          ? "text-slate-200"
                          : "text-slate-500"
                      }`}
                    >
                      {item.title}
                    </p>

                    <p className="mt-0.5 break-words text-xs leading-5 text-slate-600">
                      {item.description}
                    </p>
                  </div>

                </div>
              );
            })}
          </div>

        </div>

        {/* Step Counter */}

        <p className="mt-6 text-center text-xs text-slate-600">
          Step {safeStep} of {steps.length}
        </p>

      </div>
    </main>
  );
}