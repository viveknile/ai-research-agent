"use client";

import { useEffect, useState } from "react";

import ResearchInput from "@/components/research/ResearchInput";
import ResearchProgress from "@/components/research/ResearchProgress";
import ResearchReport from "@/components/research/ResearchReport";

import {
  getResearch,
  type ResearchResult,
} from "@/lib/api";


export default function Home() {

  const [researchId, setResearchId] =
    useState<string | null>(null);

  const [researchResult, setResearchResult] =
    useState<ResearchResult | null>(null);

  const [error, setError] =
    useState<string | null>(null);


  /*
   * Called by ResearchInput after
   * the backend successfully creates
   * a research job.
   */
  const handleResearchStarted = (
    id: string,
  ) => {

    setError(null);

    setResearchId(id);

    setResearchResult(null);
  };


  /*
   * Poll the backend while research
   * is running.
   */
  useEffect(() => {

    if (!researchId) {
      return;
    }


    let cancelled = false;

    let timeoutId:
      ReturnType<typeof setTimeout> | null =
      null;


    const pollResearch = async () => {

      try {

        const result =
          await getResearch(
            researchId,
          );


        if (cancelled) {
          return;
        }


        setResearchResult(result);


        /*
         * Research completed.
         */
        if (
          result.status ===
          "completed"
        ) {

          return;
        }


        /*
         * Research failed.
         */
        if (
          result.status ===
          "failed"
        ) {

          setError(
            result.error ||
              "Research failed.",
          );

          return;
        }


        /*
         * Research is still running.
         *
         * Poll again after 1.5 seconds.
         */
        timeoutId =
          setTimeout(
            pollResearch,
            1500,
          );

      } catch (err) {

        if (cancelled) {
          return;
        }


        setError(
          err instanceof Error
            ? err.message
            : "Failed to check research status.",
        );

      }
    };


    pollResearch();


    return () => {

      cancelled = true;

      if (timeoutId) {
        clearTimeout(timeoutId);
      }

    };

  }, [researchId]);


  /*
   * Start a new research.
   */
  const handleBack = () => {

    setResearchId(null);

    setResearchResult(null);

    setError(null);
  };


  /*
   * Show the research report
   * after the backend completes.
   */
  if (
    researchResult?.status ===
    "completed"
  ) {

    return (
      <ResearchReport
        result={
          researchResult.result ?? {}
        }
        onBack={handleBack}
      />
    );
  }


  /*
   * Show research progress while
   * the backend is running.
   */
  if (researchId) {

    return (
      <main className="min-h-screen bg-slate-950 px-6 py-12">

        <ResearchProgress
          progress={
            researchResult?.progress ??
            0
          }

          step={
            researchResult?.step ??
            1
          }

          currentStep={
            researchResult?.current_step ??
            "Understanding your question"
          }

          currentDescription={
            researchResult?.current_description ??
            "Analyzing the research objective"
          }
        />


        <p className="mt-8 text-center text-xs text-slate-700">
          Research ID: {researchId}
        </p>


        {error && (
          <div className="mx-auto mt-6 max-w-2xl rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-300">
            {error}
          </div>
        )}

      </main>
    );
  }


  /*
   * Initial research input screen.
   */
  return (
    <ResearchInput
      onResearchStarted={
        handleResearchStarted
      }
    />
  );
}