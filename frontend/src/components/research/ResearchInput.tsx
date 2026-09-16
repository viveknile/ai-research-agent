"use client";

import { useState } from "react";
import {
  createResearch,
  type ResearchDepth,
} from "@/lib/api";

interface ResearchInputProps {
  onResearchStarted: (researchId: string) => void;
}

export default function ResearchInput({
  onResearchStarted,
}: ResearchInputProps) {
  const [query, setQuery] = useState("");
  const [depth, setDepth] =
    useState<ResearchDepth>("standard");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (query.trim().length < 5) {
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const result = await createResearch({
        query: query.trim(),
        depth,
      });

      onResearchStarted(result.research_id);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="relative flex min-h-screen items-center justify-center overflow-hidden px-6 py-16">
      {/* Background decoration */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/2 top-[-180px] h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-indigo-500/10 blur-3xl" />

        <div className="absolute bottom-[-160px] left-[-100px] h-[350px] w-[350px] rounded-full bg-purple-500/10 blur-3xl" />

        <div className="absolute right-[-100px] top-1/3 h-[300px] w-[300px] rounded-full bg-blue-500/10 blur-3xl" />
      </div>

      <div className="relative z-10 w-full max-w-3xl">
        {/* Header */}
        <div className="mb-10 text-center">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300 backdrop-blur">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            Autonomous AI Research
          </div>

          <h1 className="text-5xl font-semibold tracking-tight text-white sm:text-6xl">
            Research
            <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Pilot
            </span>
          </h1>

          <p className="mx-auto mt-5 max-w-xl text-base leading-7 text-slate-400 sm:text-lg">
            Ask a question. ResearchPilot searches the web,
            analyzes sources, cross-checks evidence, and builds a
            cited research report.
          </p>
        </div>

        {/* Research form */}
        <form
          onSubmit={handleSubmit}
          className="rounded-3xl border border-white/10 bg-white/[0.04] p-5 shadow-2xl shadow-black/20 backdrop-blur-xl sm:p-7"
        >
          <label
            htmlFor="research-query"
            className="mb-3 block text-sm font-medium text-slate-200"
          >
            What do you want to research?
          </label>

          <textarea
            id="research-query"
            value={query}
            onChange={(event) =>
              setQuery(event.target.value)
            }
            placeholder="Example: Compare the major AI agent frameworks available in 2026 and recommend one for a Python backend."
            rows={6}
            maxLength={1000}
            disabled={isSubmitting}
            className="w-full resize-none rounded-2xl border border-white/10 bg-slate-950/60 px-5 py-4 text-sm leading-6 text-white outline-none transition placeholder:text-slate-600 focus:border-indigo-400/50 focus:ring-2 focus:ring-indigo-400/10 disabled:cursor-not-allowed disabled:opacity-60"
          />

          <div className="mt-3 flex justify-end">
            <span className="text-xs text-slate-600">
              {query.length}/1000
            </span>
          </div>

          {/* Research depth */}
          <div className="mt-7">
            <p className="mb-3 text-sm font-medium text-slate-200">
              Research depth
            </p>

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              {[
                {
                  value: "quick" as const,
                  title: "Quick",
                  description: "Fast overview",
                },
                {
                  value: "standard" as const,
                  title: "Standard",
                  description: "Balanced research",
                },
                {
                  value: "deep" as const,
                  title: "Deep",
                  description: "More sources & analysis",
                },
              ].map((option) => {
                const selected =
                  depth === option.value;

                return (
                  <button
                    key={option.value}
                    type="button"
                    disabled={isSubmitting}
                    onClick={() =>
                      setDepth(option.value)
                    }
                    className={`rounded-2xl border p-4 text-left transition ${
                      selected
                        ? "border-indigo-400/50 bg-indigo-500/10"
                        : "border-white/10 bg-white/[0.02] hover:border-white/20 hover:bg-white/[0.04]"
                    } disabled:cursor-not-allowed disabled:opacity-60`}
                  >
                    <div className="flex items-center gap-3">
                      <span
                        className={`flex h-5 w-5 items-center justify-center rounded-full border ${
                          selected
                            ? "border-indigo-400"
                            : "border-slate-600"
                        }`}
                      >
                        {selected && (
                          <span className="h-2.5 w-2.5 rounded-full bg-indigo-400" />
                        )}
                      </span>

                      <span className="font-medium text-white">
                        {option.title}
                      </span>
                    </div>

                    <p className="mt-2 pl-8 text-xs text-slate-500">
                      {option.description}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={
              isSubmitting ||
              query.trim().length < 5
            }
            className="mt-7 flex w-full items-center justify-center gap-2 rounded-2xl bg-indigo-500 px-5 py-4 text-sm font-semibold text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {isSubmitting
              ? "Starting Research..."
              : "Start Research"}

            {!isSubmitting && (
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              >
                <path d="M5 12h14" />
                <path d="m13 6 6 6-6 6" />
              </svg>
            )}
          </button>

          {/* Error */}
          {error && (
            <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/5 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}
        </form>

        <p className="mt-5 text-center text-xs text-slate-600">
          ResearchPilot uses multiple sources to build
          evidence-backed answers.
        </p>
      </div>
    </section>
  );
}